"""
gh-image-upload: Upload images to GitHub issues/comments via the
undocumented user-attachments API.

GitHub's web UI uploads images through a 3-step flow:
  1. POST /upload/policies/assets  → get S3 presigned URL + form fields
  2. POST to S3                    → upload the file binary
  3. PUT  /upload/assets/{id}      → confirm upload, get final URL

This tool replicates that flow using session cookies extracted from
a browser session.

The resulting URL (https://github.com/user-attachments/assets/{uuid})
can be embedded in any issue body or comment via `gh issue create/edit`
or `gh issue comment`.
"""

from __future__ import annotations

import argparse
import mimetypes
import re
import subprocess
import sys
from pathlib import Path

import httpx
from rich.console import Console

console = Console()

# ── GitHub web endpoints ────────────────────────────────────────────
UPLOAD_POLICIES_URL = "https://github.com/upload/policies/assets"
UPLOAD_ASSETS_URL = "https://github.com/upload/assets/{asset_id}"

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36"
)


def get_repo_id(owner: str, repo: str) -> int:
    """Get the numeric repository ID via the gh CLI."""
    result = subprocess.run(
        ["gh", "api", f"repos/{owner}/{repo}", "--jq", ".id"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        console.print(f"[red]Failed to get repo ID: {result.stderr}[/red]")
        sys.exit(1)
    return int(result.stdout.strip())


def upload_image(
    image_path: Path,
    repo_id: int,
    session_cookie: str,
    owner: str,
    repo: str,
) -> str:
    """Upload an image through GitHub's 3-step upload protocol.

    Returns the final user-attachments URL.

    The critical insight is that GitHub's Rails backend uses a _gh_sess
    cookie (encrypted session) that is set on every response and must
    be sent back on the next request. We use httpx's cookie jar to
    handle this automatically — the client accumulates cookies from
    responses and sends them on subsequent requests to the same domain.
    """
    file_size = image_path.stat().st_size
    content_type = mimetypes.guess_type(str(image_path))[0] or "application/octet-stream"
    file_name = image_path.name

    # Use a cookie jar so _gh_sess flows automatically between requests
    cookies = httpx.Cookies()
    cookies.set("user_session", session_cookie, domain="github.com")
    cookies.set("logged_in", "yes", domain=".github.com")

    with httpx.Client(cookies=cookies, follow_redirects=True, timeout=60) as client:
        # ── Preflight: load a GitHub page to establish _gh_sess ─────
        console.print("[dim]Preflight: establishing session...[/dim]")

        preflight_resp = client.get(
            f"https://github.com/{owner}/{repo}",
            headers={"User-Agent": BROWSER_UA},
        )

        if preflight_resp.status_code != 200:
            console.print(f"[red]Preflight failed ({preflight_resp.status_code})[/red]")
            sys.exit(1)

        # Extract the fetch nonce from the HTML meta tag
        nonce_match = re.search(
            r'<meta\s+name="fetch-nonce"\s+content="([^"]+)"',
            preflight_resp.text,
        )
        if not nonce_match:
            console.print("[red]Could not find fetch-nonce in page[/red]")
            sys.exit(1)

        nonce = nonce_match.group(1)
        console.print(f"  [green]✓[/green] Session established, nonce: [dim]{nonce[:20]}...[/dim]")

        # Common headers for GitHub API-like requests.
        # The Sec-Fetch-* headers are critical — GitHub validates them
        # as part of CSRF protection. Without them, you get 422.
        gh_headers = {
            "X-Requested-With": "XMLHttpRequest",
            "GitHub-Verified-Fetch": "true",
            "Accept": "application/json",
            "X-Fetch-Nonce": nonce,
            "Origin": "https://github.com",
            "Referer": f"https://github.com/{owner}/{repo}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": BROWSER_UA,
        }

        # ── Step 1: Get upload policy ───────────────────────────────
        console.print(
            f"\n[cyan]Step 1:[/cyan] Requesting upload policy for "
            f"[bold]{file_name}[/bold] ({file_size:,} bytes)"
        )

        policy_resp = client.post(
            UPLOAD_POLICIES_URL,
            files={
                "repository_id": (None, str(repo_id)),
                "name": (None, file_name),
                "size": (None, str(file_size)),
                "content_type": (None, content_type),
            },
            headers=gh_headers,
        )

        if policy_resp.status_code != 201:
            console.print(f"[red]Upload policy failed ({policy_resp.status_code}):[/red]")
            # Try to show useful error info
            try:
                console.print(policy_resp.json())
            except Exception:
                console.print(policy_resp.text[:500])
            sys.exit(1)

        policy = policy_resp.json()
        upload_url = policy["upload_url"]
        form_fields = policy["form"]
        asset_id = policy["asset"]["id"]
        asset_upload_token = policy["asset_upload_authenticity_token"]

        console.print(f"  [green]✓[/green] Got S3 upload URL and asset ID [bold]{asset_id}[/bold]")
        console.print(f"  [dim]S3 bucket: {upload_url}[/dim]")

        # ── Step 2: Upload file to S3 ──────────────────────────────
        console.print("[cyan]Step 2:[/cyan] Uploading to S3...")

        # Build multipart form: all policy fields + file last
        # S3 requires fields in a specific order with 'file' last
        s3_files: list[tuple[str, tuple]] = [
            (k, (None, v)) for k, v in form_fields.items()
        ]
        s3_files.append(("file", (file_name, image_path.read_bytes(), content_type)))

        s3_resp = client.post(upload_url, files=s3_files)

        if s3_resp.status_code not in (200, 201, 204):
            console.print(f"[red]S3 upload failed ({s3_resp.status_code}):[/red]")
            console.print(s3_resp.text[:500])
            sys.exit(1)

        console.print(f"  [green]✓[/green] Uploaded to S3 ({s3_resp.status_code})")

        # ── Step 3: Confirm upload ─────────────────────────────────
        console.print("[cyan]Step 3:[/cyan] Confirming upload...")

        confirm_url = UPLOAD_ASSETS_URL.format(asset_id=asset_id)
        confirm_resp = client.put(
            confirm_url,
            files={"authenticity_token": (None, asset_upload_token)},
            headers=gh_headers,
        )

        if confirm_resp.status_code != 200:
            console.print(f"[red]Upload confirmation failed ({confirm_resp.status_code}):[/red]")
            try:
                console.print(confirm_resp.json())
            except Exception:
                console.print(confirm_resp.text[:500])
            sys.exit(1)

        result = confirm_resp.json()
        final_url = result["href"]
        console.print("  [green]✓[/green] Upload confirmed!")
        console.print(f"\n[bold green]Image URL:[/bold green] {final_url}")

        return final_url


def main():
    parser = argparse.ArgumentParser(
        description="Upload images to GitHub and get markdown-ready URLs",
        epilog="The resulting URL can be used in `gh issue create/edit` or `gh issue comment`.",
    )
    parser.add_argument("image", type=Path, help="Path to the image file to upload")
    parser.add_argument(
        "--repo",
        required=True,
        help="Repository in owner/name format (e.g., bc/web)",
    )
    parser.add_argument(
        "--cookie",
        help="GitHub user_session cookie value (or set GH_USER_SESSION env var)",
    )
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Output markdown image tag instead of raw URL",
    )
    parser.add_argument(
        "--issue",
        type=int,
        help="Automatically add the image as a comment on this issue number",
    )
    parser.add_argument(
        "--issue-body",
        type=int,
        help="Append the image to this issue's body",
    )
    parser.add_argument(
        "--alt",
        default="Image",
        help="Alt text for the image (default: Image)",
    )

    args = parser.parse_args()

    if not args.image.exists():
        console.print(f"[red]File not found: {args.image}[/red]")
        sys.exit(1)

    # Get session cookie
    import os

    session_cookie = args.cookie or os.environ.get("GH_USER_SESSION", "")
    if not session_cookie:
        console.print(
            "[yellow]No session cookie provided.[/yellow]\n"
            "Use --cookie or set GH_USER_SESSION env var.\n"
            "Extract it from browser DevTools → Application → Cookies → github.com → user_session"
        )
        sys.exit(1)

    # Parse repo
    parts = args.repo.split("/")
    if len(parts) != 2:
        console.print("[red]--repo must be in owner/name format[/red]")
        sys.exit(1)
    owner, repo = parts

    # Get repo ID
    repo_id = get_repo_id(owner, repo)
    console.print(f"[dim]Repository: {owner}/{repo} (ID: {repo_id})[/dim]\n")

    # Upload
    url = upload_image(args.image, repo_id, session_cookie, owner, repo)

    # Format output
    if args.markdown:
        md = f"![{args.alt}]({url})"
        console.print(f"\n[bold]Markdown:[/bold]\n{md}")
        # Also print raw for piping
        print(md, file=sys.stderr)

    # Auto-comment on issue
    if args.issue:
        console.print(f"\n[cyan]Adding comment to issue #{args.issue}...[/cyan]")
        body = f"![{args.alt}]({url})"
        result = subprocess.run(
            ["gh", "issue", "comment", str(args.issue),
             "--repo", f"{owner}/{repo}",
             "--body", body],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            console.print(f"[green]✓[/green] Comment added to issue #{args.issue}")
        else:
            console.print(f"[red]Failed to add comment: {result.stderr}[/red]")

    # Append to issue body
    if args.issue_body:
        console.print(f"\n[cyan]Appending image to issue #{args.issue_body} body...[/cyan]")
        # Get current body
        result = subprocess.run(
            ["gh", "issue", "view", str(args.issue_body),
             "--repo", f"{owner}/{repo}",
             "--json", "body", "--jq", ".body"],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            console.print(f"[red]Failed to get issue body: {result.stderr}[/red]")
            sys.exit(1)

        current_body = result.stdout.rstrip()
        new_body = f"{current_body}\n\n![{args.alt}]({url})"

        result = subprocess.run(
            ["gh", "issue", "edit", str(args.issue_body),
             "--repo", f"{owner}/{repo}",
             "--body", new_body],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            console.print(f"[green]✓[/green] Image appended to issue #{args.issue_body} body")
        else:
            console.print(f"[red]Failed to update issue body: {result.stderr}[/red]")


if __name__ == "__main__":
    main()
