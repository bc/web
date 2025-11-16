# Contributing to bc.com

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to Brian Cohn's personal website.

## Development Setup

1. **Prerequisites**
   - Ruby 3.0+
   - Node.js 18+
   - Git

2. **Quick Setup**
   ```bash
   git clone https://github.com/bc/web.git
   cd web
   make setup  # or ./scripts/setup
   ```

3. **Development Server**
   ```bash
   make serve  # or bundle exec jekyll serve
   ```

## Project Structure

```
├── _config.yml           # Jekyll configuration
├── _layouts/             # Page templates
├── _includes/            # Reusable components  
├── _pages/               # Static pages
├── _posts/               # Blog posts & guides
├── _sass/                # Stylesheets
├── assets/               # Static assets
│   └── images/           # Optimized images
├── tests/                # Playwright tests
└── scripts/              # Build & utility scripts
```

## Content Guidelines

### Writing Posts

1. **File Naming**: Use format `YYYY-MM-DD-title.md`
2. **Front Matter**: Include required fields:
   ```yaml
   ---
   layout: post
   title: "Your Post Title"
   description: "Brief description for SEO"
   date: 2025-11-16
   author: "Brian Cohn"
   ---
   ```

### Images

- Place optimized images in `assets/images/`
- Use responsive image include: `{% include image.html filename="example" alt="Description" %}`
- Provide multiple sizes: `-small.webp`, `-medium.webp`, `-large.webp`

### Code Style

- **Markdown**: Use standard formatting
- **YAML**: 2-space indentation
- **HTML**: Follow semantic markup principles
- **CSS/SCSS**: Follow BEM methodology where applicable

## Testing

- **Visual Tests**: `npm test` (Playwright)
- **HTML Validation**: `make test-html`
- **Build Test**: `make build`

## Submitting Changes

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature`
3. **Make** your changes
4. **Test** your changes: `make test`
5. **Commit** with clear messages
6. **Push** to your fork
7. **Submit** a pull request

## Commit Message Format

```
type(scope): brief description

Longer description if needed
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples**:
- `feat(posts): add new ML tools guide`
- `fix(images): correct responsive image paths`
- `docs(readme): update setup instructions`

## Code Review Process

1. Automated checks must pass
2. Manual review by maintainer
3. Address feedback if requested
4. Merge after approval

## Questions?

- Open an issue for bugs or feature requests
- Email: briancohn@kaspect.com
- Check existing issues before creating new ones

Thank you for contributing! 🎉
