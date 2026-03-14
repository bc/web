# CLAUDE.md

This is a Jekyll-powered personal website for Brian Cohn (briancohn.com), a computational biologist and ML researcher.

## Quick Reference

```bash
make setup          # First-time setup (installs Ruby + Node deps)
make serve          # Dev server with live reload (localhost:4000)
make build          # Production build
npm test            # Playwright visual regression tests
npm run test:html   # HTML validation (requires build first)
npm run lint:css    # SCSS linting
```

## Project Structure

```
_config.yml          # Jekyll configuration (site metadata, plugins, colors)
_layouts/default.html  # Single HTML5 layout template (sticky nav, footer)
_includes/           # Reusable components (cal-embed.html, image.html)
_pages/              # Static pages (home, research, presskit, posts, meet)
_posts/              # Blog posts (YYYY-MM-DD-title.md format)
_sass/               # SCSS partials (imported by assets/css/style.scss)
assets/css/style.scss  # Main stylesheet (variables, components, responsive)
assets/images/       # Optimized images (WebP + responsive variants)
scripts/             # Build utilities (setup, optimize_images.py)
tests/               # Playwright visual regression tests
.github/workflows/   # CI/CD (build-test.yml, deploy.yml)
```

## Tech Stack

- **Generator**: Jekyll 4.3 with Minima theme
- **Ruby**: 3.0+ (Bundler for deps)
- **Node.js**: 18+ (Playwright testing, stylelint)
- **Styling**: SCSS with BEM methodology
- **Testing**: Playwright for visual regression
- **Deployment**: GitHub Pages / Cloudflare Pages
- **Image pipeline**: Python script producing WebP at multiple sizes

## Code Conventions

- **Indentation**: 2 spaces (YAML, HTML, SCSS, JS), 4 spaces (Python), tabs (Makefile)
- **Line endings**: LF
- **Encoding**: UTF-8
- **CSS**: BEM naming, mobile-first responsive, SCSS variables for colors
- **Colors**: Primary coral `#FF9398`, accent teal `#49c5b6`
- **Typography**: Playfair Display (headings), Inter (body)
- **Images**: Always use `{% include image.html filename="name" alt="desc" %}` for responsive WebP with lazy loading

## Content Authoring

### New Posts

Create `_posts/YYYY-MM-DD-title.md` with front matter:

```yaml
---
layout: post
title: "Post Title"
description: "Brief SEO description"
date: YYYY-MM-DD
author: "Brian Cohn"
---
```

### Images

- Place originals in `assets/images/`
- Run `make optimize-images` to generate responsive WebP variants (-small, -medium, -large)
- Reference via the image include, not raw `<img>` tags

## Commit Messages

Format: `type(scope): description`

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## CI/CD

Two GitHub Actions workflows:
- **build-test.yml**: Runs on PRs to main. Builds site, validates HTML, runs Playwright tests.
- **deploy.yml**: Runs on push to master. Optimizes images, builds, tests, deploys to GitHub Pages.

## Testing

- `tests/visual.spec.js` — Basic visual checks (h1, colors, responsive, links)
- `tests/full-site-visual.spec.js` — Full page screenshots across desktop/mobile viewports
- Tests require a built site. Run `make build` before `npm test` if testing locally.

## Key Files to Edit

| Task | File(s) |
|------|---------|
| Site metadata / plugins | `_config.yml` |
| Page layout / nav | `_layouts/default.html` |
| Styling | `assets/css/style.scss` |
| Add a page | `_pages/` (set `permalink` in front matter) |
| Add a blog post | `_posts/YYYY-MM-DD-title.md` |
| Modify image pipeline | `scripts/optimize_images.py` |
| Update tests | `tests/` |
