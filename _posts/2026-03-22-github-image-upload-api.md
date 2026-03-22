---
layout: default
title: "Reverse Engineering GitHub's Image Upload API"
description: "How GitHub's drag-and-drop image upload works under the hood: a 3-step S3 presigned URL flow, and a Python tool to replicate it from the command line."
date: 2026-03-22
excerpt: "GitHub has no public API for uploading images to issues. I used Playwright to intercept the browser's network traffic, reverse-engineered the 3-step upload protocol, and built a CLI tool that replicates it."
---

# Reverse Engineering GitHub's Image Upload API

**GitHub has no public API for uploading images to issues.** When you drag an image into the comment box, it appears as a `![image](https://github.com/user-attachments/assets/...)` URL — but there's no documented way to do this programmatically. The `gh` CLI can create issues and comments with text, but can't attach images.

I wanted to fix that. Here's how I reverse-engineered the upload protocol and built a tool to replicate it.

---

## The Problem

If you're automating GitHub workflows — creating issues from CI, attaching screenshots to bug reports, or building tools that generate visual content — you hit a wall. The GitHub REST API and `gh` CLI accept markdown text, but the `user-attachments` URLs that render inline images can only be created through the web interface.

## Intercepting the Browser

I used [Playwright](https://playwright.dev/) to open the GitHub issue page, set up network request interception, then triggered a file upload through the comment box's file input. Three requests appeared:

```
[POST] github.com/upload/policies/assets        → 201
[POST] github-production-user-asset-*.s3.amazonaws.com  → 204
[PUT]  github.com/upload/assets/567411350        → 200
```

## The 3-Step Protocol

### Step 1: Request an Upload Policy

```
POST https://github.com/upload/policies/assets
Content-Type: multipart/form-data

repository_id=293454135
name=screenshot.png
size=644596
content_type=image/png
```

The server responds with a JSON payload containing:

- **`upload_url`**: An S3 bucket URL (`github-production-user-asset-6210df.s3.amazonaws.com`)
- **`form`**: Pre-signed form fields (AWS credential, policy, signature, key path)
- **`asset.id`**: A numeric asset ID
- **`asset.href`**: The final `user-attachments` URL (already assigned, but not yet valid)
- **`asset_upload_authenticity_token`**: A CSRF token for step 3

The `form` fields are a textbook [S3 presigned POST](https://docs.aws.amazon.com/AmazonS3/latest/API/sigv4-post-example.html). GitHub generates the signature server-side with their AWS credentials, so you never see their secret key. The policy encodes constraints like exact file size and content type.

### Step 2: Upload to S3

```
POST https://github-production-user-asset-6210df.s3.amazonaws.com/
Content-Type: multipart/form-data

key=13772726/567411350-uuid.png
acl=private
policy=eyJ...base64...
X-Amz-Algorithm=AWS4-HMAC-SHA256
X-Amz-Credential=AKIAV.../us-east-1/s3/aws4_request
X-Amz-Date=20260322T000000Z
X-Amz-Signature=eb1288ba...
Content-Type=image/png
Cache-Control=max-age=2592000
x-amz-meta-Surrogate-Control=max-age=31557600
file=@screenshot.png
```

No GitHub auth needed here — the AWS signature in the form fields handles authorization. S3 returns `204 No Content` on success.

The `key` path is `{user_id}/{asset_id}-{uuid}.{ext}`, and the `Surrogate-Control` header tells CDN caches to hold the asset for a year.

### Step 3: Confirm the Upload

```
PUT https://github.com/upload/assets/567411350
Content-Type: multipart/form-data

authenticity_token=4MXf-qfex...
```

This tells GitHub the S3 upload completed. The server responds with the final asset metadata:

```json
{
  "id": 567411350,
  "name": "screenshot.png",
  "size": 644596,
  "content_type": "image/png",
  "href": "https://github.com/user-attachments/assets/6b4c1a98-..."
}
```

The `href` URL now works anywhere in GitHub markdown.

## The Authentication Puzzle

The hardest part wasn't understanding the protocol — it was authenticating. GitHub's upload endpoint uses **four layers of protection**:

1. **Session cookie** (`user_session`): Identifies the logged-in user
2. **Rails session** (`_gh_sess`): An encrypted, rotating session cookie that changes with every response. You must use the cookie from your most recent response — it's a chain.
3. **Fetch nonce** (`X-Fetch-Nonce`): Embedded in the page HTML as `<meta name="fetch-nonce">`, ties requests to a specific page load
4. **`Sec-Fetch-*` headers**: The browser's built-in headers that tell the server "this is a same-origin request"

The `Sec-Fetch-*` headers were the non-obvious blocker. Without `Sec-Fetch-Site: same-origin`, `Sec-Fetch-Mode: cors`, and `Sec-Fetch-Dest: empty`, GitHub returns 422 — even with valid cookies and nonce. These headers are normally set automatically by browsers and can't be spoofed by cross-origin JavaScript, making them an effective CSRF defense. But `httpx` (or `curl`) can set them freely.

The `gh` CLI's OAuth token (`gho_...`) does **not** work for this endpoint. It authenticates against `api.github.com`, but the upload flow lives on `github.com` and requires web session auth.

## The Tool

I packaged this into a Python CLI tool using `uv`:

```bash
# Upload an image and get the URL
gh-image-upload screenshot.png --repo owner/repo

# Upload and automatically comment on an issue
gh-image-upload screenshot.png --repo owner/repo --issue 42

# Upload and append to an issue body
gh-image-upload screenshot.png --repo owner/repo --issue-body 42
```

The tool:
1. Makes a preflight GET request to establish the `_gh_sess` cookie chain and extract the fetch nonce
2. Executes the 3-step upload protocol
3. Optionally uses `gh issue comment` or `gh issue edit` to embed the image

### Result

Here's what it looks like — the fffuel.co screenshot was uploaded entirely from the command line:

![GitHub issue with uploaded image](https://github.com/user-attachments/assets/38b5c77e-0f42-48b6-a66e-8e9007ae14e8)

And the comment with the image:

![GitHub issue comment with uploaded image](https://github.com/user-attachments/assets/1efe310c-bdb7-4aa3-aca8-f45375442f22)

## Architecture Diagram

```
┌─────────────────┐     ┌──────────────────┐     ┌──────────────┐
│  Your Machine   │     │   github.com     │     │   AWS S3     │
│                 │     │  (Rails + CDN)   │     │              │
│  ┌───────────┐  │     │                  │     │              │
│  │ gh-image  │──┼──1──▶ /upload/policies │     │              │
│  │ -upload   │  │     │  /assets         │     │              │
│  │           │◀─┼──┐  │  ↓               │     │              │
│  │           │  │  │  │  Returns:        │     │              │
│  │           │  │  │  │  • S3 signed URL │     │              │
│  │           │  │  │  │  • form fields   │     │              │
│  │           │  │  │  │  • asset ID      │     │              │
│  │           │──┼──┼──┼──────────────────┼──2──▶ Upload file  │
│  │           │  │  │  │                  │     │ to presigned │
│  │           │◀─┼──┼──┼──────────────────┼─────│ URL          │
│  │           │  │  │  │                  │     │ (204)        │
│  │           │──┼──┼──▶ /upload/assets/  │     │              │
│  │           │  │  │  │  {id}            │     │              │
│  │           │  │  │  │  (PUT confirm)   │     │              │
│  │           │◀─┼──┘  │  ↓               │     │              │
│  │           │  │  3  │  Returns:        │     │              │
│  │           │  │     │  asset href URL  │     │              │
│  └───────────┘  │     │                  │     │              │
│                 │     │                  │     │              │
│  ┌───────────┐  │     │                  │     │              │
│  │ gh CLI    │──┼──4──▶ REST API:        │     │              │
│  │           │  │     │  create comment  │     │              │
│  │           │  │     │  with ![img](url)│     │              │
│  └───────────┘  │     │                  │     │              │
└─────────────────┘     └──────────────────┘     └──────────────┘
```

## Caveats

- **Session cookies expire.** The `user_session` cookie has a limited lifetime. You'll need to refresh it periodically by logging in through a browser.
- **This is undocumented.** GitHub could change the upload protocol at any time. The endpoint URLs, required headers, and authentication flow are all implementation details.
- **Rate limits are unknown.** Since this isn't a public API, there are no documented rate limits. Don't abuse it.

## Source Code

The full tool is at [`tools/gh-image-upload`](https://github.com/bc/web/tree/master/tools/gh-image-upload) in this site's repo. Install with:

```bash
cd tools/gh-image-upload
uv sync
export GH_USER_SESSION="<your cookie>"
uv run gh-image-upload photo.png --repo owner/repo --issue 1
```

---

*Built with [httpx](https://www.python-httpx.org/), [Playwright](https://playwright.dev/), and curiosity about what browsers actually do when you drag a file onto a text box.*
