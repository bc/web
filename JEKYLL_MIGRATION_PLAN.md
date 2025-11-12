# Jekyll Migration & Image Optimization Plan
**Website:** bc.com | **Current:** Plain HTML + GitHub Pages | **Target:** Jekyll + Optimized Images

---

## Executive Summary

This plan outlines the migration from static HTML to Jekyll with automated deployment via GitHub Pages, including comprehensive image optimization for fast loading.

**Timeline:** 11-18 hours total | **Phases:** 7 | **Risk Level:** Low

---

## PHASE 1: ASSESSMENT & PREPARATION (2-3 hours)

### 1.1 Current Site Audit

**Files to assess:**
- ✓ index.html (10 KB)
- ✓ research.html (35 KB)
- ✓ ml-tools.html (24 KB)
- ✓ presskit.html (4.8 KB)
- ✓ meet.html (redirect)

**Assets to migrate:**
- Images: favicon (14-57KB), screenshots, PNG files
- CSS: Imported from CDN (new.css, Inter font)
- JavaScript: Cal.com embeds only
- External dependencies: Cal.com, Google Fonts

**Current strengths to preserve:**
- Responsive design (already mobile-friendly)
- Clean navigation structure
- Professional styling
- Cal.com integration

### 1.2 Choose Jekyll Theme

**Recommended: Minima (Jekyll's official minimal theme)**

Why:
- Lightweight base (~10 KB)
- Full SCSS customization
- Perfect for research/documentation site
- Excellent Jekyll learning curve
- Active maintenance

**Alternative: Chirpy** (if want advanced features)
- Professional design
- Built-in search, dark mode, TOC
- Better for discovery

### 1.3 Environment Preparation

```bash
# Check current Ruby version
ruby --version

# Install Ruby 3.x if needed
brew install ruby

# Install Jekyll & Bundler
gem install bundler jekyll
```

---

## PHASE 2: JEKYLL SETUP (1-2 hours)

### 2.1 Create Directory Structure

```
bc-website/
│
├── _config.yml                 # Jekyll configuration
├── Gemfile                      # Ruby dependencies
│
├── _data/                       # Dynamic data files
│   ├── navigation.yml          # Site navigation
│   └── tools.yml               # ML tools database
│
├── _includes/                  # Reusable components
│   ├── header.html
│   ├── footer.html
│   ├── nav.html
│   ├── cal-embed.html         # Cal.com embed
│   ├── contact.html           # Contact section
│   └── tool-card.html         # Tool card component
│
├── _layouts/                   # Page templates
│   ├── default.html           # Base layout
│   ├── page.html              # Standard page
│   ├── research.html          # Research with TOC
│   └── tool-showcase.html     # ML tools layout
│
├── _sass/                      # Stylesheets
│   ├── minima/                # Theme SCSS
│   │   ├── _base.scss
│   │   ├── _layout.scss
│   │   └── _syntax.scss
│   └── custom.scss            # Your customizations
│
├── _pages/                     # Main pages
│   ├── home.md
│   ├── research.md
│   ├── ml-tools.md
│   └── presskit.md
│
├── _research/                  # Research collection
│   ├── lipnet-quick-reference.md
│   ├── performance-benchmarks.md
│   └── performance-quick-ref.md
│
├── assets/
│   ├── css/
│   │   └── style.scss         # Main stylesheet
│   ├── images/
│   │   ├── original/          # Original high-res
│   │   ├── optimized/         # Optimized JPEG/PNG
│   │   ├── webp/              # WebP versions
│   │   ├── favicons/
│   │   ├── screenshots/
│   │   └── icons/
│   └── js/
│       └── main.js            # Custom JS
│
├── .github/
│   └── workflows/
│       └── build.yml          # GitHub Actions CI/CD
│
├── scripts/
│   └── optimize-images.js     # Image optimization script
│
├── CNAME                       # Custom domain
├── README.md
└── .gitignore
```

### 2.2 Create Gemfile

```ruby
source "https://rubygems.org"

gem "jekyll", "~> 4.3"
gem "minima", "~> 2.5"

# Plugins
group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.17"
  gem "jekyll-seo-tag", "~> 2.8"
  gem "jekyll-sitemap", "~> 1.4"
  gem "jekyll-paginate", "~> 1.1"
  gem "jekyll-compress-images" # Image optimization
end

group :development do
  gem "webrick", "~> 1.8"
end
```

### 2.3 Create _config.yml

```yaml
# Site metadata
title: Brian Cohn Ph.D.
tagline: Biologist. Product Developer. ML Researcher.
description: >
  Leveraging statistical modeling, machine learning, and closed-loop DSP hardware
  to solve healthcare and biotechnology challenges.

url: https://bc.com
baseurl: ""
email: briancohn@kaspect.com

# Theme
theme: minima

# Plugins
plugins:
  - jekyll-feed
  - jekyll-seo-tag
  - jekyll-sitemap
  - jekyll-paginate

# Collections
collections:
  research:
    output: true
    permalink: /research/:name

# Markdown
markdown: kramdown

# Build settings
exclude:
  - .github
  - Gemfile
  - Gemfile.lock
  - node_modules
  - scripts

# Compression
sass:
  style: compressed

# Image settings
image_dir: /assets/images

# SEO
social:
  name: Brian Cohn
  links:
    - https://github.com/bc
    - https://www.linkedin.com/in/cohn/
    - https://scholar.google.com/citations?user=0obwS54AAAAJ&hl=en&oi=sra
```

---

## PHASE 3: CONTENT MIGRATION (3-4 hours)

### 3.1 Create Data Files

**_data/navigation.yml**
```yaml
- title: Home
  url: /

- title: Schedule a chat
  url: "#"
  external: true
  data_cal_link: "bcohn/meet-brian"

- title: CV.pdf
  url: https://raw.githubusercontent.com/bc/resume/main/briancohn.pdf
  external: true

- title: Papers
  url: https://scholar.google.com/citations?user=0obwS54AAAAJ&hl=en&oi=sra
  external: true

- title: LinkedIn
  url: https://www.linkedin.com/in/cohn/
  external: true

- title: GitHub
  url: https://github.com/bc
  external: true

- title: Press Kit
  url: /presskit/

- title: Research & Whitepapers
  url: /research/

- title: ML Tools
  url: /ml-tools/
```

**_data/tools.yml** (sample structure for ML Tools)
```yaml
- category: Model Visualization
  tools:
    - name: Netron
      url: https://netron.app/
      badges: [free, open-source, web-app]
      description: Neural network model visualization for 40+ formats
      use_cases:
        - Debug model architecture
        - Verify layer connections
        - Analyze quantization effects

- category: Browser Inference
  tools:
    - name: TensorFlow.js
      url: https://www.tensorflow.org/js
      badges: [free, open-source, library]
      description: ML library for JavaScript with GPU acceleration
```

### 3.2 Convert HTML to Markdown

**_pages/home.md**
```markdown
---
layout: default
permalink: /
title: Brian Cohn Ph.D.
---

# Brian Cohn Ph.D.

I'm a biologist with a penchant for product development—leveraging statistical modeling,
machine learning research, and closed loop DSP hardware to solve issues in healthcare
and biotechnology.

## My Roles

1. Director of Research at ObvioHealth
2. Chief Scientist at Kaspect
3. Co-Founder of Adventure Biofeedback

## Recent Projects

* [A robot that learns to walk on its own using tendons](https://www.nature.com/articles/s42256-019-0029-0)
  - Published in Nature Machine Intelligence, 2020
* Algorithm for neurophysiology analysis from muscle signals
* AI tool for speech-language pathologists
* VR game mechanic that redesigns targets based on player ability

...
```

**_pages/research.md**
```markdown
---
layout: research
permalink: /research/
title: Research & Whitepapers
---

# Research & Whitepapers

Comprehensive technical research on LipNet, avatar animation, and real-time lip-sync
performance benchmarking.

## LipNet + Avatar Integration Quick Reference

### Top 7 Libraries

#### 1. Kalidokit

| Property | Rating |
|----------|--------|
| LipNet Integration | ⭐⭐⭐⭐ |
| Performance | 60 FPS |
| Setup | Medium difficulty |

...
```

### 3.3 Create Layout Templates

**_layouts/default.html**
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{% if page.title %}{{ page.title }} - {% endif %}{{ site.title }}</title>

  <link rel="apple-touch-icon" href="/assets/images/favicons/apple-touch-icon.png">
  <link rel="icon" type="image/png" href="/assets/images/favicons/favicon.png">

  <link rel="stylesheet" href="https://fonts.xz.style/serve/inter.css">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@exampledev/new.css@1.1.2/new.min.css">
  <link rel="stylesheet" href="{{ '/assets/css/style.css' | relative_url }}">

  {% seo %}
</head>
<body>
  {% include header.html %}

  <main>
    {{ content }}
  </main>

  {% include footer.html %}
  {% include cal-embed.html %}
</body>
</html>
```

**_layouts/research.html**
```html
---
layout: default
---

<div class="research-container">
  <div class="research-toc">
    <!-- Auto-generated TOC by Jekyll -->
    {{ content | toc_only }}
  </div>

  <div class="research-content">
    {{ content }}
  </div>
</div>
```

### 3.4 Create Includes

**_includes/header.html**
```html
<header>
  <nav class="site-nav">
    <strong>
      <a href="{{ '/' | relative_url }}" class="site-title">
        {{ site.title }}
      </a>
    </strong>

    {% for nav_item in site.data.navigation %}
      {% if nav_item.external %}
        <a href="{{ nav_item.url }}"
           {% if nav_item.data_cal_link %}data-cal-link="{{ nav_item.data_cal_link }}"{% endif %}>
          {{ nav_item.title }}
        </a>
      {% else %}
        <a href="{{ nav_item.url | relative_url }}">
          {{ nav_item.title }}
        </a>
      {% endif %}
    {% endfor %}
  </nav>
</header>
```

**_includes/tool-card.html**
```html
<div class="tool-card">
  <h3>{{ include.tool.name }}</h3>

  <div class="tool-meta">
    {% for badge in include.tool.badges %}
      <span class="badge badge-{{ badge }}">{{ badge }}</span>
    {% endfor %}
  </div>

  <p>{{ include.tool.description }}</p>

  <h4>Use Cases:</h4>
  <ul>
    {% for use_case in include.tool.use_cases %}
      <li>{{ use_case }}</li>
    {% endfor %}
  </ul>

  <a href="{{ include.tool.url }}" class="tool-link" target="_blank">
    → Learn More
  </a>
</div>
```

### 3.5 Convert Research Content

**_research/lipnet-quick-reference.md**
```markdown
---
title: LipNet + Avatar Integration Quick Reference
layout: post
collection: research
---

# Top 7 Libraries at a Glance

## 1. Kalidokit

| Property | Rating |
|----------|--------|
| LipNet Integration | ⭐⭐⭐⭐ (4/5) |
| Performance | ⭐⭐⭐⭐ (60 FPS) |
| Setup | ⭐⭐⭐ (Medium) |

...
```

---

## PHASE 4: GITHUB PAGES & DEPLOYMENT (1-2 hours)

### 4.1 GitHub Pages Configuration

**Create .github/workflows/build.yml**
```yaml
name: Build and Deploy Jekyll

on:
  push:
    branches: [master, main]
  pull_request:
    branches: [master, main]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Setup Ruby
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.2'
          bundler-cache: true

      - name: Build Jekyll site
        run: |
          bundle exec jekyll build --strict_front_matter
        env:
          JEKYLL_ENV: production

      - name: Optimize images (optional)
        run: npm run image:optimize || true

      - name: Upload to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./_site
          cname: bc.com
```

### 4.2 Create CNAME File

```
bc.com
```

### 4.3 GitHub Settings

1. Go to repository Settings → Pages
2. Source: Deploy from a branch
3. Branch: gh-pages
4. Custom domain: bc.com
5. Enable "Enforce HTTPS"

---

## PHASE 5: IMAGE OPTIMIZATION (2-3 hours)

### 5.1 Current Image Audit

```bash
# Run from bc-website directory
find assets/images -type f | while read f; do
  size=$(du -h "$f" | cut -f1)
  echo "$size - $f"
done

# Sort by size
find assets/images -type f -exec du -h {} + | sort -rh | head -20
```

**Expected findings:**
- Pasted_Image_9_9_20__11_17_PM.jpg: 239 KB → Target: 80-100 KB
- Favicon PNGs: 14-57 KB → Already reasonable
- Screenshots: Varies → Need assessment

### 5.2 Setup Image Optimization

**Create package.json**
```json
{
  "name": "bc-website",
  "version": "1.0.0",
  "description": "bc.com Jekyll site",
  "scripts": {
    "image:optimize": "node scripts/optimize-images.js",
    "image:check": "sh scripts/check-image-sizes.sh"
  },
  "devDependencies": {
    "sharp": "^0.33.0"
  }
}
```

**Create scripts/optimize-images.js**
```javascript
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

const inputDir = './assets/images/original';
const jpegDir = './assets/images/optimized';
const webpDir = './assets/images/webp';

// Create directories if they don't exist
[jpegDir, webpDir].forEach(dir => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
});

// Process each image
const files = fs.readdirSync(inputDir);
let processed = 0;

files.forEach(async (file) => {
  const ext = path.extname(file).toLowerCase();
  if (!['.jpg', '.jpeg', '.png', '.gif'].includes(ext)) return;

  const inputPath = path.join(inputDir, file);
  const basename = path.parse(file).name;

  try {
    // Convert to optimized JPEG
    await sharp(inputPath)
      .resize(1200, 1200, {
        withoutEnlargement: true,
        fit: 'inside'
      })
      .jpeg({
        quality: 82,
        progressive: true,
        mozjpeg: true
      })
      .toFile(path.join(jpegDir, `${basename}.jpg`));

    console.log(`✓ JPEG: ${basename}.jpg`);

    // Convert to WebP (smaller size)
    await sharp(inputPath)
      .resize(1200, 1200, {
        withoutEnlargement: true,
        fit: 'inside'
      })
      .webp({ quality: 82 })
      .toFile(path.join(webpDir, `${basename}.webp`));

    console.log(`✓ WebP: ${basename}.webp`);

    // Create 2x retina version for WebP
    await sharp(inputPath)
      .resize(2400, 2400, {
        withoutEnlargement: true,
        fit: 'inside'
      })
      .webp({ quality: 75 })
      .toFile(path.join(webpDir, `${basename}@2x.webp`));

    console.log(`✓ 2x WebP: ${basename}@2x.webp`);

    processed++;
  } catch (error) {
    console.error(`✗ Error processing ${file}:`, error.message);
  }
});

console.log(`\n📊 Optimization complete. Processed: ${processed} files`);
```

**Create scripts/check-image-sizes.sh**
```bash
#!/bin/bash

echo "Original images size:"
du -sh assets/images/original

echo "\nOptimized JPEG size:"
du -sh assets/images/optimized

echo "\nWebP size:"
du -sh assets/images/webp

echo "\nSize comparison:"
orig=$(du -s assets/images/original | cut -f1)
opt=$(du -s assets/images/optimized | cut -f1)
webp=$(du -s assets/images/webp | cut -f1)

echo "Original: $orig"
echo "JPEG: $opt"
echo "WebP: $webp"
```

### 5.3 Implement Modern Image Serving

**_includes/responsive-image.html**
```html
{% assign basename = include.name | split: '.' | first %}
{% assign alt = include.alt | default: '' %}
{% assign width = include.width | default: 'auto' %}
{% assign height = include.height | default: 'auto' %}

<picture>
  <!-- Modern WebP format first -->
  <source
    srcset="/assets/images/webp/{{ basename }}.webp 1x,
            /assets/images/webp/{{ basename }}@2x.webp 2x"
    type="image/webp"
  />

  <!-- Fallback to optimized JPEG -->
  <img
    src="/assets/images/optimized/{{ basename }}.jpg"
    alt="{{ alt }}"
    loading="lazy"
    width="{{ width }}"
    height="{{ height }}"
    decoding="async"
  />
</picture>
```

**Usage in Markdown/HTML:**
```html
{% include responsive-image.html name="robot-walking" alt="Robot learning to walk" width="600" height="400" %}
```

### 5.4 CSS Lazy Loading Animation

**_sass/custom.scss**
```scss
// Lazy loading placeholder
img[loading="lazy"] {
  background: linear-gradient(
    90deg,
    #f0f0f0 25%,
    #e0e0e0 50%,
    #f0f0f0 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

// Image dimensions
img {
  max-width: 100%;
  height: auto;
  display: block;
}

picture {
  display: block;
}
```

---

## PHASE 6: PERFORMANCE OPTIMIZATION (1-2 hours)

### 6.1 Build Performance

**_config.yml**
```yaml
# Minimize CSS
sass:
  style: compressed

# Enable caching for faster builds
exclude:
  - node_modules
  - .git
  - scripts
  - vendor
```

### 6.2 Create Lighthouse Testing Script

**scripts/audit.sh**
```bash
#!/bin/bash

echo "Building Jekyll site..."
bundle exec jekyll build

echo "\nInstalling Lighthouse..."
npm install -g lighthouse

echo "\nRunning Lighthouse audit on bc.com..."
lighthouse https://bc.com \
  --view \
  --chrome-flags="--headless" \
  --output-path=./lighthouse-report.html

echo "\n✓ Report saved to lighthouse-report.html"
```

### 6.3 SEO & Metadata

**_config.yml additions**
```yaml
plugins:
  - jekyll-sitemap        # Auto-generates sitemap.xml
  - jekyll-seo-tag        # Auto-generates meta tags
  - jekyll-feed           # Auto-generates RSS feed

# Social metadata
social:
  name: Brian Cohn Ph.D.
  links:
    - https://github.com/bc
    - https://www.linkedin.com/in/cohn/
    - https://scholar.google.com/citations?user=0obwS54AAAAJ&hl=en&oi=sra
```

### 6.4 robots.txt

Create **robots.txt** at root:
```
User-agent: *
Allow: /

Sitemap: https://bc.com/sitemap.xml
```

---

## PHASE 7: TESTING & VALIDATION (1-2 hours)

### 7.1 Local Testing

```bash
# Clone or set up local Jekyll
bundle install
bundle exec jekyll serve

# Test at http://localhost:4000
# Check all links, images, responsive design
```

### 7.2 Pre-Deployment Checklist

- [ ] All internal links work
- [ ] All external links accessible
- [ ] Cal.com embed functional
- [ ] Images display correctly
- [ ] Mobile responsive (test on device)
- [ ] 404 page displays
- [ ] Navigation works on all pages
- [ ] CSS/fonts load correctly
- [ ] No console errors in DevTools
- [ ] Search engines can crawl (check sitemap.xml)
- [ ] Meta tags present (check with SEO Checker)
- [ ] Analytics code works (if using)

### 7.3 GitHub Actions Validation

```bash
# Before pushing, test build locally
JEKYLL_ENV=production bundle exec jekyll build --strict_front_matter

# Check for build errors
echo $?  # Should return 0 for success
```

### 7.4 Performance Testing

```bash
# Run Lighthouse
npm install -g lighthouse
lighthouse https://bc.com

# Check PageSpeed Insights
# https://pagespeed.web.dev/?url=bc.com
```

**Target metrics:**
- Performance: ≥ 90
- Accessibility: ≥ 95
- Best Practices: ≥ 90
- SEO: ≥ 95

### 7.5 Image Optimization Validation

```bash
# Compare sizes
du -sh assets/images/original
du -sh assets/images/optimized
du -sh assets/images/webp

# Check for missing WebP versions
ls assets/images/webp | wc -l
```

---

## IMPLEMENTATION STEPS

### Week 1: Setup & Planning
- [ ] Assess current site structure
- [ ] Set up local Jekyll environment
- [ ] Create directory structure
- [ ] Configure _config.yml

### Week 2: Content Migration
- [ ] Create data files (_data/*.yml)
- [ ] Convert HTML → Markdown pages
- [ ] Create layout templates
- [ ] Create reusable includes
- [ ] Test locally

### Week 3: Deployment
- [ ] Push to GitHub
- [ ] Configure GitHub Pages
- [ ] Set up GitHub Actions workflow
- [ ] Update DNS if needed

### Week 4: Optimization
- [ ] Audit current images
- [ ] Set up image optimization pipeline
- [ ] Implement WebP serving
- [ ] Add lazy loading
- [ ] Run Lighthouse audits

### Week 5: Testing & Refinement
- [ ] Functional testing
- [ ] Performance testing
- [ ] SEO validation
- [ ] Monitor GitHub Actions builds

---

## QUICK REFERENCE

### Useful Commands

```bash
# Local development
bundle exec jekyll serve --livereload

# Build for production
JEKYLL_ENV=production bundle exec jekyll build

# Check Jekyll config
bundle exec jekyll doctor

# Install dependencies
bundle install

# Image optimization
npm run image:optimize
npm run image:check

# Lighthouse audit
lighthouse https://bc.com --view
```

### File Locations
- Site config: `_config.yml`
- Navigation: `_data/navigation.yml`
- CSS: `_sass/custom.scss` or `assets/css/style.scss`
- Original images: `assets/images/original/`
- Optimized: `assets/images/optimized/`
- WebP: `assets/images/webp/`

### GitHub Pages Status
- View deploy status: Settings → Pages
- Check Actions: Actions tab
- View live site: https://bc.com

---

## MIGRATION SUCCESS METRICS

✅ **Technical:**
- Zero build errors on every push
- Lighthouse score ≥ 90 on all metrics
- Page load time < 2 seconds
- All images loading
- All links functional

✅ **Content:**
- All pages migrated
- No broken references
- Research content preserved
- ML tools database functional

✅ **User Experience:**
- Site responsive on mobile
- Navigation clear and working
- Cal.com embeds functional
- Search engines can crawl
- Analytics tracking working

---

## ROLLBACK PLAN

If issues arise:
1. Revert commits: `git revert <commit-hash>`
2. Disable GitHub Actions: Settings → Workflows
3. Restore old HTML: `git checkout <branch>`
4. Update DNS to point to old server if needed

**Estimated recovery time: 30 minutes**

---

## Questions / Troubleshooting

### Issue: Jekyll build fails locally
```bash
# Clear cache
rm -rf .jekyll-cache
bundle install
bundle exec jekyll build
```

### Issue: Images not displaying
```bash
# Check relative URLs
grep -r "src=\"/" _includes/
grep -r "src=\"/" _layouts/

# Fix to use relative_url filter
# src="{{ '/assets/images/...' | relative_url }}"
```

### Issue: GitHub Actions workflow fails
- Check workflow file syntax
- Verify Gemfile dependencies
- Check build logs in Actions tab
- Ensure CNAME file exists

---

## Resources

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages & Jekyll](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll)
- [Minima Theme Docs](https://github.com/jekyll/minima)
- [Sharp Image Optimization](https://sharp.pixelplumbing.com/)
- [Web.dev Image Optimization](https://web.dev/image-optimization/)
- [Lighthouse Guide](https://developers.google.com/web/tools/lighthouse)

---

**Last Updated:** November 2025
**Status:** Ready for implementation
**Estimated Total Time:** 11-18 hours
