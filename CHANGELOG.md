# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive repository cleanup and reorganization
- Development tooling (pre-commit hooks, setup scripts)
- GitHub Actions workflow for CI/CD
- EditorConfig and Stylelint configuration
- 404 error page with branded styling
- Security.txt for responsible disclosure
- Makefile for easier development commands
- Contributing guidelines
- HTML testing with html-proofer
- Automated sitemap generation

### Changed
- **BREAKING**: Moved images from `/img/` to `/assets/images/`
- Updated all image references to use new path
- Reorganized Jekyll configuration with better defaults
- Enhanced README with comprehensive setup instructions
- Improved Gemfile with development dependencies
- Updated package.json with additional scripts

### Fixed
- Image path references in presskit and includes
- Jekyll configuration optimization
- Build process improvements

### Removed
- Unused migration plan files from excludes
- Duplicate image directory structure

## [1.0.0] - 2025-11-16

### Added
- Initial Jekyll site structure
- Posts system replacing separate Guides and ML Tools
- Minima theme customization
- Responsive image optimization system
- Visual regression testing with Playwright

### Features
- Personal website with ML research focus
- Technical guides and tools documentation
- Optimized image delivery system
- SEO optimization
- Mobile-responsive design
