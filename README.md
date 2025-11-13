# bc.com

Personal site built with Jekyll and GitHub Pages.

## Setup

```bash
uv venv
source .venv/bin/activate
uv add -p 3.12 @playwright/test
bundle install
```

## Run

```bash
bundle exec jekyll serve  # Start dev server at http://localhost:4000
npm test                   # Run visual tests
```

## Build

```bash
bundle exec jekyll build   # Output to _site/
```

---

Served at https://briancohn.com · Hosted on Cloudflare
