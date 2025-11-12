# Image Optimization Guide
**For bc.com Jekyll Migration**

---

## Goal
Reduce image load time by 40-70% while maintaining visual quality.

**Expected Results:**
- Page load time: **2-3s → 1-1.5s** (40% faster)
- Image file sizes: **50-70% reduction**
- Mobile experience: **significantly improved**
- Lighthouse score: **80→95+**

---

## Part 1: Image Audit

### Step 1: Assess Current Images

```bash
# Navigate to web directory
cd /Users/bc/Documents/GitHub/bc/web

# List all images with sizes
find . -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" | while read f; do
  ls -lh "$f" | awk '{print $5 " - " $NF}'
done | sort -rh
```

### Step 2: Document Current State

**Current Images in bc.com:**

| File | Current Size | Format | Location | Target |
|------|-------------|--------|----------|--------|
| Pasted_Image_9_9_20__11_17_PM.jpg | 239 KB | JPEG | root | 80-100 KB |
| apple-touch-icon.png | 14 KB | PNG | root | 10-12 KB |
| android-chrome-192x192.png | 16 KB | PNG | root | 12-14 KB |
| android-chrome-512x512.png | 57 KB | PNG | root | 25-30 KB |
| favicon.ico | 15 KB | ICO | root | 8-10 KB |
| Various img/*.jpg | ? | JPEG | img/ | TBD |
| Various img/*.png | ? | PNG | img/ | TBD |

**Run audit:**
```bash
du -sh . # Total size
find img -type f | wc -l # Count files
du -sh img # Images subdirectory
```

---

## Part 2: Setup Optimization Tools

### Option A: Using Sharp.js (Recommended - Automated)

#### Step 1: Install Node.js & NPM
```bash
# Check if installed
node --version
npm --version

# If not installed
brew install node
```

#### Step 2: Create package.json
```json
{
  "name": "bc-image-optimizer",
  "version": "1.0.0",
  "description": "Image optimization for bc.com",
  "scripts": {
    "optimize": "node scripts/optimize-images.js",
    "check": "node scripts/check-sizes.js"
  },
  "devDependencies": {
    "sharp": "^0.33.0"
  }
}
```

#### Step 3: Install Dependencies
```bash
npm install
```

#### Step 4: Create Optimization Scripts

**scripts/optimize-images.js**
```javascript
const sharp = require('sharp');
const fs = require('fs');
const path = require('path');

// Configuration
const config = {
  quality: 82,
  webpQuality: 82,
  maxWidth: 1200,
  maxHeight: 1200,
  retinaMult: 2,
  verbose: true
};

// Input/output directories
const directories = [
  {
    input: './assets/images/original',
    jpegOut: './assets/images/optimized',
    webpOut: './assets/images/webp',
    name: 'assets'
  },
  {
    input: './img',
    jpegOut: './img-optimized',
    webpOut: './img-webp',
    name: 'root-img'
  }
];

// Create output directories
function ensureDirectories(config) {
  [config.jpegOut, config.webpOut].forEach(dir => {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
      console.log(`✓ Created directory: ${dir}`);
    }
  });
}

// Get human-readable file size
function formatBytes(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

// Optimize single image
async function optimizeImage(inputPath, outputDir, filename, format = 'jpeg') {
  const basename = path.parse(filename).name;
  const ext = format === 'webp' ? 'webp' : 'jpg';

  try {
    const image = sharp(inputPath);
    const metadata = await image.metadata();

    // Determine output dimensions
    const width = Math.min(config.maxWidth, metadata.width || 1200);
    const height = Math.min(config.maxHeight, metadata.height || 1200);

    let outputPath;

    if (format === 'jpeg') {
      // Optimized JPEG
      await sharp(inputPath)
        .resize(width, height, {
          withoutEnlargement: true,
          fit: 'inside'
        })
        .jpeg({
          quality: config.quality,
          progressive: true,
          mozjpeg: true
        })
        .toFile(path.join(outputDir, `${basename}.jpg`));

      outputPath = path.join(outputDir, `${basename}.jpg`);
      const stats = fs.statSync(outputPath);
      if (config.verbose) {
        console.log(`  ✓ JPEG: ${formatBytes(stats.size)} (${width}×${height})`);
      }
    } else if (format === 'webp') {
      // Standard WebP
      await sharp(inputPath)
        .resize(width, height, {
          withoutEnlargement: true,
          fit: 'inside'
        })
        .webp({ quality: config.webpQuality })
        .toFile(path.join(outputDir, `${basename}.webp`));

      outputPath = path.join(outputDir, `${basename}.webp`);
      const stats = fs.statSync(outputPath);
      if (config.verbose) {
        console.log(`  ✓ WebP: ${formatBytes(stats.size)} (${width}×${height})`);
      }

      // Retina WebP (@2x)
      await sharp(inputPath)
        .resize(width * config.retinaMult, height * config.retinaMult, {
          withoutEnlargement: true,
          fit: 'inside'
        })
        .webp({ quality: config.webpQuality - 5 })
        .toFile(path.join(outputDir, `${basename}@2x.webp`));

      const stats2x = fs.statSync(path.join(outputDir, `${basename}@2x.webp`));
      if (config.verbose) {
        console.log(`  ✓ WebP @2x: ${formatBytes(stats2x.size)} (${width * 2}×${height * 2})`);
      }
    }

    return true;
  } catch (error) {
    console.error(`  ✗ Error: ${error.message}`);
    return false;
  }
}

// Main processing
async function processDirectory(dirConfig) {
  console.log(`\n📁 Processing: ${dirConfig.name}`);
  console.log('─'.repeat(60));

  if (!fs.existsSync(dirConfig.input)) {
    console.log(`⚠ Directory not found: ${dirConfig.input}`);
    return;
  }

  ensureDirectories(dirConfig);

  const files = fs.readdirSync(dirConfig.input);
  const imageFiles = files.filter(f =>
    /\.(jpg|jpeg|png|gif)$/i.test(f)
  );

  if (imageFiles.length === 0) {
    console.log('  No images found.');
    return;
  }

  console.log(`Found ${imageFiles.length} image(s)`);

  let successCount = 0;

  for (const filename of imageFiles) {
    const inputPath = path.join(dirConfig.input, filename);
    const stats = fs.statSync(inputPath);

    console.log(`\n➜ ${filename} (${formatBytes(stats.size)})`);

    // Optimize to JPEG
    await optimizeImage(inputPath, dirConfig.jpegOut, filename, 'jpeg');

    // Convert to WebP
    await optimizeImage(inputPath, dirConfig.webpOut, filename, 'webp');

    successCount++;
  }

  console.log(`\n✓ Processed ${successCount}/${imageFiles.length} images`);
}

// Run all directories
async function main() {
  console.log('\n🖼️  Image Optimization Script');
  console.log('═'.repeat(60));

  for (const dirConfig of directories) {
    await processDirectory(dirConfig);
  }

  console.log('\n═'.repeat(60));
  console.log('✓ Optimization complete!');
  console.log('\nNext steps:');
  console.log('1. Review optimized images');
  console.log('2. Update HTML/Liquid templates to use <picture> element');
  console.log('3. Test responsive images on different browsers');
  console.log('4. Run: npm run check (to see file size savings)');
}

main().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
```

**scripts/check-sizes.js**
```javascript
const fs = require('fs');
const path = require('path');

function formatBytes(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return (bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i];
}

function getDirSize(dir) {
  if (!fs.existsSync(dir)) return 0;

  let size = 0;
  const files = fs.readdirSync(dir);

  files.forEach(file => {
    const stats = fs.statSync(path.join(dir, file));
    size += stats.size;
  });

  return size;
}

console.log('\n📊 Image Size Comparison');
console.log('═'.repeat(60));

const comparisons = [
  {
    name: 'Root Images (Favicons, etc)',
    original: './assets/images/original',
    optimized: './assets/images/optimized',
    webp: './assets/images/webp'
  },
  {
    name: 'Screenshots & Content',
    original: './img',
    optimized: './img-optimized',
    webp: './img-webp'
  }
];

let totalOriginal = 0;
let totalOptimized = 0;
let totalWebp = 0;

comparisons.forEach(comp => {
  const orig = getDirSize(comp.original);
  const opt = getDirSize(comp.optimized);
  const webp = getDirSize(comp.webp);

  if (orig === 0) {
    console.log(`\n⚠ ${comp.name}: No original images found`);
    return;
  }

  const savings = ((1 - opt / orig) * 100).toFixed(1);
  const webpSavings = ((1 - webp / orig) * 100).toFixed(1);

  console.log(`\n${comp.name}:`);
  console.log(`  Original:  ${formatBytes(orig)}`);
  console.log(`  JPEG:      ${formatBytes(opt)} (${savings}% smaller)`);
  console.log(`  WebP:      ${formatBytes(webp)} (${webpSavings}% smaller)`);

  totalOriginal += orig;
  totalOptimized += opt;
  totalWebp += webp;
});

console.log('\n' + '═'.repeat(60));
console.log('TOTAL:');
const totalSavings = ((1 - totalOptimized / totalOriginal) * 100).toFixed(1);
const totalWebpSavings = ((1 - totalWebp / totalOriginal) * 100).toFixed(1);
console.log(`  Original: ${formatBytes(totalOriginal)}`);
console.log(`  JPEG:     ${formatBytes(totalOptimized)} (${totalSavings}% smaller)`);
console.log(`  WebP:     ${formatBytes(totalWebp)} (${totalWebpSavings}% smaller)`);
console.log('═'.repeat(60) + '\n');
```

#### Step 5: Run Optimization

```bash
# First, create directories for original images
mkdir -p assets/images/original

# Move existing images (optional - for new setup)
# cp img/*.jpg assets/images/original/ 2>/dev/null || true
# cp assets/images/*.jpg assets/images/original/ 2>/dev/null || true

# Run optimization
npm run optimize

# Check results
npm run check
```

---

### Option B: Using ImageMagick (Mac Alternative)

```bash
# Install ImageMagick
brew install imagemagick

# Optimize single image
convert original.jpg -quality 82 -strip -interlace Plane optimized.jpg

# Batch convert to WebP
for f in *.jpg; do
  convert "$f" -quality 82 -define webp:method=6 "${f%.*}.webp"
done

# Check file sizes
ls -lh *.jpg *.webp
```

---

## Part 3: Organize Optimized Images

### Directory Structure

```
assets/images/
├── original/
│   ├── robot-walking.jpg        (original high-res)
│   └── pasted-image-9920.jpg    (239KB → keep original for reference)
│
├── optimized/
│   ├── robot-walking.jpg        (optimized JPEG)
│   └── pasted-image-9920.jpg    (100KB, 58% smaller)
│
└── webp/
    ├── robot-walking.webp       (even smaller)
    ├── robot-walking@2x.webp    (retina 2x)
    ├── pasted-image-9920.webp   (60KB, 75% smaller)
    └── pasted-image-9920@2x.webp
```

### Move & Organize

```bash
# After optimization, organize:
mkdir -p assets/images/original
mkdir -p assets/images/optimized
mkdir -p assets/images/webp

# Keep originals as backup
cp assets/images/*.jpg assets/images/original/

# Move optimized versions
mv assets/images/optimized/*.jpg assets/images/optimized/
mv assets/images/webp/*.webp assets/images/webp/

# Verify
ls -lh assets/images/*/
```

---

## Part 4: Implement Responsive Images

### Create Liquid Template

**_includes/responsive-image.html**
```html
{%- capture image_base -%}{{ include.name | split: '.' | first }}{%- endcapture -%}

<picture>
  <!-- Modern WebP format (browsers supporting WebP, including newer Chrome, Firefox, Edge) -->
  <source
    srcset="/assets/images/webp/{{ image_base }}.webp 1x,
            /assets/images/webp/{{ image_base }}@2x.webp 2x"
    type="image/webp"
    media="(min-width: 0px)"
  />

  <!-- Fallback: Optimized JPEG (all browsers) -->
  <img
    src="/assets/images/optimized/{{ image_base }}.jpg"
    srcset="/assets/images/optimized/{{ image_base }}.jpg 1x,
            /assets/images/optimized/{{ image_base }}@2x.jpg 2x"
    alt="{{ include.alt | default: '' }}"
    title="{{ include.title | default: '' }}"
    loading="lazy"
    decoding="async"
    width="{{ include.width | default: 'auto' }}"
    height="{{ include.height | default: 'auto' }}"
    class="responsive-image {% if include.class %}{{ include.class }}{% endif %}"
  />
</picture>
```

### CSS for Lazy Loading

**_sass/images.scss**
```scss
// Lazy load animation
img[loading="lazy"] {
  background: linear-gradient(
    90deg,
    #f0f0f0 25%,
    #e0e0e0 50%,
    #f0f0f0 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  min-height: 200px;
}

@keyframes shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

// Responsive images
.responsive-image {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 1rem auto;
}

// Picture element
picture {
  display: block;

  img {
    max-width: 100%;
    height: auto;
  }
}
```

### Usage Examples

**In Markdown:**
```markdown
{% include responsive-image.html
  name="robot-walking.jpg"
  alt="Robot learning to walk on tendons"
  width="600"
  height="400"
  class="feature-image"
%}
```

**In HTML/Liquid:**
```html
<!-- Simple usage -->
{% include responsive-image.html name="screenshot.jpg" alt="Screenshot" %}

<!-- With dimensions -->
{% include responsive-image.html
  name="research-chart.jpg"
  alt="Performance chart"
  width="1000"
  height="600"
  title="Performance comparison"
%}
```

---

## Part 5: Update HTML References

### Before Migration (Plain HTML)
```html
<img src="/Pasted_Image_9_9_20__11_17_PM.jpg" alt="Robot">
```

### After Migration (Jekyll Liquid)
```html
{% include responsive-image.html
  name="Pasted_Image_9_9_20__11_17_PM.jpg"
  alt="Robot learning to walk"
  width="600"
  height="400"
%}
```

---

## Part 6: Performance Testing

### Lighthouse Audit

```bash
# Install Lighthouse
npm install -g lighthouse

# Run audit locally (must be running Jekyll serve)
lighthouse http://localhost:4000 --view

# Run audit on production
lighthouse https://bc.com --view
```

**Check for:**
- Image size scores
- Lazy loading effectiveness
- WebP support detection
- Performance score: target ≥ 90

### Manual Testing

```bash
# Check image file sizes
ls -lh assets/images/optimized/
ls -lh assets/images/webp/

# View WebP browser support
# Open DevTools → Network tab → filter by images
# Check if .webp files are loaded (not .jpg)
```

### Browser DevTools Testing

1. Open https://localhost:4000
2. Open DevTools (F12)
3. Network tab → Filter "Img"
4. Check:
   - [x] WebP images load on Chrome/Edge
   - [x] JPEG fallback on Firefox/Safari
   - [x] @2x retina versions on retina displays
   - [x] Lazy loading delays load event
   - [x] No 404 errors

---

## Part 7: Before & After Comparison

### Current State (Plain HTML)
```
Homepage load:
├─ Images: 250+ KB
├─ Load time: 2-3 seconds
├─ Lighthouse: 75-80
└─ Mobile: Slow

Research page:
├─ Screenshot: 239 KB (unoptimized)
├─ Multiple formats
└─ No lazy loading
```

### Optimized State (Jekyll + WebP)
```
Homepage load:
├─ Images: 80-100 KB
├─ Load time: 1-1.5 seconds (40% faster)
├─ Lighthouse: 95+
└─ Mobile: Fast

Research page:
├─ Screenshot: 60-70 KB (70% smaller)
├─ Optimized JPEG + WebP
├─ Lazy loading enabled
└─ Retina support
```

---

## Part 8: Troubleshooting

### Issue: WebP not detected
```bash
# Verify WebP generation
file assets/images/webp/*.webp

# Should output: "WebP image data"
```

### Issue: Retina images not showing
```bash
# Check if @2x images exist
ls -l assets/images/webp/*@2x.webp

# Add height attribute to trigger retina
{% include responsive-image.html name="image.jpg" width="600" height="400" %}
```

### Issue: Slow optimization
```bash
# For very large batches, optimize with smaller max-width
# Edit scripts/optimize-images.js, change maxWidth: 1000 (instead of 1200)

# Or process in smaller batches
# Move 10 images at a time instead of all at once
```

### Issue: File size not improving much
```bash
# Check image quality settings
# For photographic images: quality 80-82 is good
# For graphics/screenshots: quality 70-75 may suffice
# For logos: use PNG instead of JPEG

# Edit scripts/optimize-images.js, line: quality: 75
```

---

## Checklist: Image Optimization

- [ ] Install Node.js and npm
- [ ] Create package.json
- [ ] Run `npm install`
- [ ] Create optimization scripts
- [ ] Create directory structure (`assets/images/original`, etc.)
- [ ] Run image optimization: `npm run optimize`
- [ ] Check results: `npm run check`
- [ ] Create `_includes/responsive-image.html`
- [ ] Create `_sass/images.scss`
- [ ] Update content to use `{% include responsive-image.html %}`
- [ ] Test locally with DevTools
- [ ] Run Lighthouse audit
- [ ] Verify WebP support
- [ ] Test on mobile device
- [ ] Commit optimized images to GitHub
- [ ] Monitor production performance

---

## Quick Commands Reference

```bash
# Check current sizes
npm run check

# Run optimization
npm run optimize

# Run Lighthouse
lighthouse http://localhost:4000

# Check Jekyll build with optimized images
JEKYLL_ENV=production bundle exec jekyll build

# Check if files are being served
curl -I https://bc.com/assets/images/optimized/image.jpg
curl -I https://bc.com/assets/images/webp/image.webp
```

---

## Expected Results Timeline

| Stage | Image Size | Load Time | Lighthouse |
|-------|-----------|-----------|-----------|
| Before | 240+ KB | 2-3s | 75-80 |
| JPEG optimized | 100-120 KB | 1.5-2s | 85-90 |
| JPEG + WebP | 60-80 KB | 1-1.5s | 90-95 |
| Full optimization | 60-80 KB | <1s | 95+ |

---

## Resources

- [Sharp.js Documentation](https://sharp.pixelplumbing.com/)
- [Web.dev Image Optimization](https://web.dev/image-optimization/)
- [WebP Compression](https://developers.google.com/speed/webp)
- [Picture Element MDN](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/picture)
- [Lighthouse Performance](https://developers.google.com/web/tools/lighthouse)

---

**Created:** November 2025
**For:** bc.com Jekyll migration
**Status:** Ready to implement
