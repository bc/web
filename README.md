# Brian Cohn's Personal Website

A Jekyll-powered personal website showcasing ML research, tools, and technical guides.

## 🚀 Quick Start

### Prerequisites
- Ruby 3.0+
- Node.js 18+
- Bundler

### Development Setup

```bash
# Install Ruby dependencies
bundle install

# Install Node.js dependencies (for testing)
npm install

# Start development server
bundle exec jekyll serve
# Site available at http://localhost:4000
```

### Alternative Setup with UV (Python)
```bash
uv venv
source .venv/bin/activate
uv add -p 3.12 @playwright/test
bundle install
```

## 🛠️ Development Commands

```bash
# Development
bundle exec jekyll serve          # Start dev server with auto-reload
bundle exec jekyll serve --drafts # Include draft posts

# Testing  
npm test                          # Run Playwright visual tests
npm run test:ui                   # Run tests with UI

# Building
bundle exec jekyll build          # Generate static site to _site/
JEKYLL_ENV=production bundle exec jekyll build  # Production build
```

## 📁 Project Structure

```
├── _config.yml           # Jekyll configuration
├── _layouts/             # Page templates
├── _includes/            # Reusable components
├── _pages/               # Static pages
├── _posts/               # Blog posts & guides
├── _sass/                # Stylesheets
├── assets/               # Static assets
├── img/                  # Optimized images
├── tests/                # Playwright tests
└── scripts/              # Build & optimization scripts
```

## 🎯 TODO: Repository Improvements

### High Priority
- [ ] **Consolidate Image Assets**: Merge `/img` and `/assets` directories
- [ ] **Optimize Jekyll Configuration**: Remove unused plugins and streamline config
- [ ] **Implement Content Strategy**: Organize posts by category/type
- [ ] **Add Development Tooling**: Pre-commit hooks, linting, automated formatting
- [ ] **Performance Optimization**: Implement lazy loading, optimize images

### Medium Priority  
- [ ] **Testing Infrastructure**: Expand visual regression tests
- [ ] **SEO Enhancement**: Improve structured data and meta tags
- [ ] **Accessibility Audit**: Ensure WCAG compliance
- [ ] **Content Management**: Add front matter validation
- [ ] **Build Optimization**: Implement asset minification pipeline

### Low Priority
- [ ] **Documentation**: Add contributing guidelines
- [ ] **Automation**: GitHub Actions for deployment and testing
- [ ] **Analytics**: Implement privacy-focused analytics
- [ ] **Progressive Enhancement**: Add offline capabilities
- [ ] **Internationalization**: Prepare for multi-language support

### Code Quality
- [ ] **Lint Configuration**: Add Jekyll linting rules
- [ ] **Asset Pipeline**: Modernize CSS/JS handling
- [ ] **Error Handling**: Improve 404 and error pages
- [ ] **Security**: Add CSP headers and security.txt

## 🔧 Configuration

### Environment Variables
- `JEKYLL_ENV`: Set to `production` for production builds

### Key Configuration Files
- `_config.yml`: Main Jekyll configuration
- `Gemfile`: Ruby dependencies
- `package.json`: Node.js dependencies and scripts
- `playwright.config.js`: Test configuration

## 🌐 Deployment

Site is deployed to **briancohn.com** and hosted on **Cloudflare Pages**.

### Manual Build
```bash
JEKYLL_ENV=production bundle exec jekyll build
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `npm test`
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.

---

**Links**: [Live Site](https://briancohn.com) • [GitHub](https://github.com/bc/web)
