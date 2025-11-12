# Jekyll Migration - Quick Summary

## The Ask
Move bc.com from plain HTML to Jekyll + GitHub Pages with optimized images for fast loading.

## Current State
- **Static HTML:** 5 pages (index, research, ml-tools, presskit, meet)
- **Hosting:** GitHub Pages (manual)
- **Build:** None (just push HTML)
- **Images:** Unoptimized (239KB screenshot, mixed sizes)
- **Dev:** Requires direct HTML editing

## Target State
```
Plain HTML                          →    Jekyll + GitHub Pages

index.html                          →    _pages/home.md
research.html                       →    _pages/research.md
ml-tools.html                       →    _pages/ml-tools.md
(CSS inline in HTML)                →    _sass/custom.scss

Manual deploy                       →    Auto-deploy on git push
No build process                    →    GitHub Actions CI/CD
Unoptimized images (239KB)          →    Optimized (80-100KB) + WebP
```

---

## Why Jekyll?

| Benefit | Details |
|---------|---------|
| **Free** | GitHub Pages included with repo |
| **Version Control** | Full git history of all content |
| **Automatic Deploy** | `git push` = live update |
| **Better Performance** | Static files, instant caching |
| **SEO Friendly** | Auto sitemap, RSS, meta tags |
| **Secure** | No database, no server vulnerabilities |
| **Professional** | Standard for tech docs/blogs |

---

## Image Optimization Benefits

### Current State
- Research screenshot: **239 KB** (PNG)
- Multiple image formats
- No WebP support
- No lazy loading

### Optimized State
- JPEG: **80-100 KB** (same image, 60% smaller)
- WebP: **50-70 KB** (modern browsers, 70% smaller)
- Auto lazy loading
- Responsive versions (1x, 2x)
- Result: **~2x faster page loads**

---

## Implementation Timeline

```
Week 1: Setup          (5 hours)
├─ Local Jekyll install
├─ Directory structure
├─ _config.yml & Gemfile
└─ Theme selection

Week 2: Migration      (6 hours)
├─ Create data files
├─ Convert HTML → Markdown
├─ Build layouts/includes
└─ Local testing

Week 3: Deploy         (3 hours)
├─ Push to GitHub
├─ GitHub Actions setup
├─ Domain config
└─ Verify live

Week 4: Optimization   (5 hours)
├─ Image audit
├─ Optimize images
├─ WebP generation
├─ Lazy loading setup
└─ Performance testing

Total: 11-18 hours
```

---

## Key Decisions Made

### 1. Jekyll Theme: Minima ✓
- Lightweight (~10 KB base)
- Full customization
- Perfect for research content
- Active maintenance

### 2. Image Optimization: Sharp.js ✓
- Node.js library (easy automation)
- Batch processing
- WebP generation
- Responsive variants

### 3. Deployment: GitHub Actions ✓
- Auto-build on push
- Free
- Integrated with Pages
- Perfect for Jekyll

### 4. Image Formats
```
Original (High-res)
├─ JPEG (82% quality, progressive) → optimized/
├─ WebP (82% quality) → webp/
└─ WebP @2x (retina) → webp/

Serving priority:
1. WebP (modern browsers) - 50KB
2. JPEG fallback (all browsers) - 100KB
3. Original only as last resort
```

---

## Critical Files to Create

### Configuration
- `Gemfile` - Ruby dependencies
- `_config.yml` - Jekyll config
- `.github/workflows/build.yml` - Auto-deploy

### Content
- `_data/navigation.yml` - Navigation menu
- `_pages/*.md` - Main pages (Markdown)
- `_research/*.md` - Research articles
- `_includes/*.html` - Reusable components
- `_layouts/*.html` - Page templates

### Images
- `assets/images/original/` - Source images
- `assets/images/optimized/` - JPEG output
- `assets/images/webp/` - WebP output
- `scripts/optimize-images.js` - Optimization script

---

## Performance Expectations

### Before Migration
- Load time: 2-3 seconds
- Lighthouse: 75-80
- Image size: Large/unoptimized

### After Migration
- Load time: 1-1.5 seconds **40% faster**
- Lighthouse: 95+ **excellent**
- Image size: 50-70% smaller
- Mobile: Much faster load
- Global: Cached on GitHub's CDN

---

## Step-by-Step for Phase 1 (This Week)

```bash
# 1. Verify Ruby installed
ruby --version  # Should be 3.0+

# 2. Create Jekyll site locally
jekyll new bc-site

# 3. Install theme dependencies
cd bc-site
bundle install

# 4. Start local server
bundle exec jekyll serve

# 5. Visit http://localhost:4000
# Should see blank Jekyll site

# Next: Create _config.yml
```

---

## Backup/Rollback Plan

If anything goes wrong:
```bash
# Keep current working site as backup
git branch backup-html-version

# If needed, revert:
git checkout backup-html-version
git push -u origin backup-html-version

# Restore old version to production:
git push origin backup-html-version:master
```

**Time to recover: ~30 minutes**

---

## Success Metrics

After migration, verify:

### Technical ✓
- [ ] Jekyll builds with 0 errors
- [ ] GitHub Actions deploy successful
- [ ] Lighthouse: ≥90 (all categories)
- [ ] Page load: < 1.5 seconds
- [ ] Images load correctly
- [ ] Favicons display

### Content ✓
- [ ] All 5 pages working
- [ ] Navigation complete
- [ ] Research content preserved
- [ ] ML tools database working
- [ ] Cal.com embeds functional

### Performance ✓
- [ ] Sitemap.xml auto-generated
- [ ] RSS feed working
- [ ] Meta tags present
- [ ] Mobile responsive
- [ ] No console errors

---

## Common Issues & Fixes

### Issue: Build fails locally
**Fix:** `bundle install && rm -rf .jekyll-cache`

### Issue: Images not showing
**Fix:** Use `relative_url` filter: `src="{{ '/assets/images/...' | relative_url }}"`

### Issue: GitHub Actions workflow fails
**Fix:** Check workflow syntax, verify Gemfile, check build logs

### Issue: Domain not pointing to Jekyll
**Fix:** Create `CNAME` file with `bc.com`, update DNS to GitHub Pages IP

---

## Resources to Reference

- [Full Plan Document](JEKYLL_MIGRATION_PLAN.md) - Complete technical details
- [Jekyll Docs](https://jekyllrb.com/docs/) - Official documentation
- [GitHub Pages + Jekyll](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll)
- [Sharp.js Docs](https://sharp.pixelplumbing.com/) - Image optimization

---

## Next Actions

### Immediately (Today)
1. Review this summary
2. Read full plan document
3. Set todo tracking

### This Week (Phase 1)
1. Install Jekyll locally
2. Create directory structure
3. Configure _config.yml
4. Set up Gemfile

### Next Week (Phase 2)
1. Create data files
2. Convert HTML to Markdown
3. Build layouts/includes
4. Test locally

---

## Questions?

Key decision points:
- **Theme choice:** Minima (minimal) vs Chirpy (featured) ← Go with Minima
- **Start date:** When ready to commit ~15 hours
- **Parallel work:** Can work on image optimization while building Jekyll
- **Testing:** Should test locally before committing to GitHub

---

**Status:** Ready for Phase 1 ✓
**Risk Level:** Low (can rollback anytime)
**Effort:** 11-18 hours
**Payoff:** Professional setup, 40%+ faster, future-proof
