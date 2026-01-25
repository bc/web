# CLAUDE.md - AI Assistant Guide for briancohn.com

This document provides context and conventions for AI assistants working on this Jekyll-based personal website for Brian Cohn, Ph.D.

## Project Overview

**Type:** Static Jekyll website (personal portfolio + technical content)
**URL:** https://briancohn.com
**Hosting:** Cloudflare Pages
**Repository:** https://github.com/bc/web

## Quick Reference Commands

```bash
# Development
npm run dev              # Start dev server with livereload (http://localhost:4000)
npm run build            # Production build
npm run clean            # Clean Jekyll cache

# Testing
npm test                 # Run Playwright visual tests
npm run test:html        # HTML validation with htmlproofer
npm run lint:css         # SCSS linting

# Setup
npm run setup            # Initial environment setup
npm run optimize:images  # Optimize images with responsive sizes
```

## Directory Structure

```
├── _config.yml          # Jekyll configuration (theme, plugins, site settings)
├── _includes/           # Reusable HTML components (image.html, cal-embed.html)
├── _layouts/            # Page templates (default.html)
├── _pages/              # Static pages (home.md, research.md, posts.md, meet.md)
├── _posts/              # Blog posts (YYYY-MM-DD-title.md format)
├── assets/
│   ├── css/style.scss   # Main stylesheet (SCSS)
│   └── images/          # Optimized images (WebP with responsive sizes)
├── scripts/             # Utility scripts (setup, pre-commit, optimize_images.py)
├── tests/               # Playwright visual tests
├── .github/workflows/   # CI/CD (build-test.yml, deploy.yml)
└── .well-known/         # Web standards (security.txt)
```

## Technology Stack

- **Static Site Generator:** Jekyll 4.3 with Minima theme
- **Templating:** Liquid + Kramdown Markdown
- **Styling:** SCSS (Playfair Display + Inter fonts)
- **Runtime:** Ruby 3.0+, Node.js 18+
- **Testing:** Playwright (visual), html-proofer (validation), Stylelint (CSS)
- **CI/CD:** GitHub Actions → Cloudflare Pages

## File Conventions

### Creating New Posts

Posts go in `_posts/` with format `YYYY-MM-DD-slug-title.md`:

```yaml
---
layout: post
title: "Post Title"
description: "SEO description for search engines"
date: 2025-11-12
author: "Brian Cohn"
excerpt: "Short excerpt for listings and previews"
---

Post content in Markdown...
```

### Creating New Pages

Pages go in `_pages/` with required front matter:

```yaml
---
layout: page
title: "Page Title"
description: "SEO description"
permalink: /custom-path/
---
```

### Adding Images

1. Place source images in `assets/images/`
2. Run `npm run optimize:images` to generate responsive sizes
3. Use the include helper in Markdown:

```liquid
{% include image.html src="image-name" alt="Description" classes="optional-classes" %}
```

This generates responsive `<picture>` elements with WebP and lazy loading.

## Code Style Conventions

### Markdown
- Use ATX-style headers (`#`, `##`, etc.)
- One sentence per line for easier diffs
- Use fenced code blocks with language specifiers

### YAML Front Matter
- Always include: `layout`, `title`, `description`
- Use double quotes for strings
- Order: layout, title, description, date, author, excerpt, permalink

### SCSS (assets/css/style.scss)
- 2-space indentation
- BEM-inspired class naming
- Use existing color variables: `$primary-color`, `$accent-color`, `$dark`, `$light`

### HTML (_includes, _layouts)
- Semantic HTML5 elements
- Include `alt` text for all images
- Preserve accessibility attributes

## Git Commit Conventions

Format: `type(scope): brief description`

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Formatting (no code change)
- `refactor`: Code restructuring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(posts): add new article on ML inference
fix(css): correct mobile navigation alignment
docs(readme): update development instructions
```

## Testing Requirements

Before committing changes:

1. **Build must succeed:** `npm run build`
2. **Visual tests pass:** `npm test`
3. **HTML is valid:** `npm run test:html`
4. **CSS is valid:** `npm run lint:css`

The pre-commit hook validates builds and checks for TODO/FIXME comments.

## Common Tasks

### Add a new blog post
1. Create `_posts/YYYY-MM-DD-slug.md` with proper front matter
2. Add any images and run `npm run optimize:images`
3. Test locally with `npm run dev`
4. Commit with `feat(posts): add post about X`

### Modify styling
1. Edit `assets/css/style.scss`
2. Run `npm run lint:css` to check for issues
3. Test responsive design at mobile breakpoint (375px)
4. Run `npm test` to verify visual regression

### Update site configuration
1. Modify `_config.yml`
2. Restart dev server (changes require restart)
3. Run full test suite

## Key Files Reference

| File | Purpose |
|------|---------|
| `_config.yml` | Jekyll settings, plugins, site metadata |
| `assets/css/style.scss` | All site styling (405 lines) |
| `_layouts/default.html` | Main page template with header/footer |
| `_includes/image.html` | Responsive image component |
| `_pages/home.md` | Homepage content |

## Things to Avoid

- **Don't edit `_site/`** - This is generated output
- **Don't commit large images** - Always optimize first
- **Don't skip front matter** - Required for Jekyll processing
- **Don't use inline styles** - Use SCSS classes
- **Don't break responsive design** - Test at 375px width
- **Don't remove SEO tags** - description and title are critical

## Deployment

- **Trigger:** Push to `master` branch
- **Pipeline:** GitHub Actions → Build → Deploy to Cloudflare Pages
- **URL:** https://briancohn.com

Production builds include image optimization and HTML validation. Failed builds will not deploy.

## External Integrations

- **Cal.com** - Meeting scheduling (embedded via `_includes/cal-embed.html`)
- **Google Scholar** - Research citations linked in research page
- **GitHub/LinkedIn** - Social links in footer

## Useful Links

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [Liquid Templating](https://shopify.github.io/liquid/)
- [Kramdown Syntax](https://kramdown.gettalong.org/syntax.html)
- [Playwright Testing](https://playwright.dev/)
