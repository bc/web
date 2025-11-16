# Makefile for Jekyll site development

.PHONY: help install serve build test clean lint

# Default target
help:
	@echo "Available commands:"
	@echo "  install    Install dependencies"
	@echo "  serve      Start development server"
	@echo "  build      Build the site"
	@echo "  test       Run tests"
	@echo "  clean      Clean build artifacts"
	@echo "  lint       Run linting"
	@echo "  setup      Initial development setup"

# Install dependencies
install:
	bundle install
	npm install

# Start development server
serve:
	bundle exec jekyll serve --livereload

# Build the site
build:
	JEKYLL_ENV=production bundle exec jekyll build

# Build for development
build-dev:
	bundle exec jekyll build

# Run tests
test:
	npm test

# Test HTML output
test-html:
	bundle exec htmlproofer ./_site --disable-external

# Clean build artifacts
clean:
	bundle exec jekyll clean
	rm -rf node_modules/.cache
	rm -rf test-results

# Run linting
lint:
	npm run lint:css

# Setup development environment
setup:
	./scripts/setup

# Optimize images
optimize-images:
	python scripts/optimize_images.py

# Bundle update
update:
	bundle update
	npm update
