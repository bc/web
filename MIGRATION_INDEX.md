# Jekyll Migration Documentation Index

**Status:** 📋 Planning Complete | Ready for Implementation
**Project:** bc.com HTML → Jekyll + GitHub Pages Migration
**Total Effort:** 11-18 hours
**Risk:** Low (can rollback anytime)

---

## 📚 Documentation Map

### 1. **JEKYLL_MIGRATION_SUMMARY.md** ⭐ START HERE
**Quick 5-minute overview**
- What & why of the migration
- Before/after comparison
- Timeline overview
- Key decisions made
- Success metrics
- Next immediate actions

**Read this first to understand the project.**

---

### 2. **JEKYLL_MIGRATION_PLAN.md** 📋 COMPLETE TECHNICAL PLAN
**Detailed 7-phase implementation guide**
- Phase 1: Assessment & Preparation (2-3h)
- Phase 2: Jekyll Setup (1-2h)
- Phase 3: Content Migration (3-4h)
- Phase 4: GitHub Pages & Deployment (1-2h)
- Phase 5: Image Optimization (2-3h)
- Phase 6: Performance Optimization (1-2h)
- Phase 7: Testing & Validation (1-2h)

Includes:
- Complete directory structure
- Code examples for every phase
- Configuration file templates
- GitHub Actions workflow
- Testing procedures
- Rollback plan

**Reference this when implementing each phase.**

---

### 3. **IMAGE_OPTIMIZATION_GUIDE.md** 🖼️ IMAGE OPTIMIZATION PLAYBOOK
**Practical step-by-step image optimization**
- Image audit procedures
- Sharp.js setup & automation
- Complete optimization scripts
- Responsive image templates
- Browser testing procedures
- Performance comparison
- Troubleshooting guide

**Use this for Phase 5 (Image Optimization).**

---

## 🗂️ File Structure

```
bc-website/
│
├── JEKYLL_MIGRATION_SUMMARY.md     ← Start here
├── JEKYLL_MIGRATION_PLAN.md        ← Full technical guide
├── IMAGE_OPTIMIZATION_GUIDE.md     ← Image optimization
├── MIGRATION_INDEX.md              ← This file
│
├── _config.yml                     # Config (from plan)
├── Gemfile                         # Dependencies (from plan)
├── CNAME                           # Custom domain
│
├── _data/                          # Navigation & data files
├── _includes/                      # Reusable components
├── _layouts/                       # Page templates
├── _pages/                         # Main pages (Markdown)
├── _research/                      # Research articles
├── _sass/                          # Stylesheets
│
├── assets/
│   ├── css/style.scss
│   └── images/
│       ├── original/               # Source images
│       ├── optimized/              # Optimized JPEG
│       └── webp/                   # WebP versions
│
├── scripts/
│   ├── optimize-images.js
│   ├── check-sizes.js
│   └── audit.sh
│
└── .github/workflows/build.yml     # GitHub Actions
```

---

## ⏱️ Implementation Timeline

### Week 1: Setup (5 hours)
- [ ] Review JEKYLL_MIGRATION_SUMMARY.md
- [ ] Set up local Jekyll environment
- [ ] Create directory structure
- [ ] Create _config.yml and Gemfile
- [ ] Test local build

**Deliverable:** Working Jekyll site locally

### Week 2: Migration (6 hours)
- [ ] Create _data/navigation.yml
- [ ] Convert HTML → Markdown pages
- [ ] Create layout templates
- [ ] Create reusable includes
- [ ] Test all pages locally

**Deliverable:** Content fully migrated to Jekyll

### Week 3: Deploy (3 hours)
- [ ] Push to GitHub
- [ ] Configure GitHub Pages settings
- [ ] Set up GitHub Actions workflow
- [ ] Verify deployment
- [ ] Update DNS/CNAME

**Deliverable:** Site live on GitHub Pages

### Week 4: Optimize (5 hours)
- [ ] Image audit (reference IMAGE_OPTIMIZATION_GUIDE.md)
- [ ] Set up optimization pipeline
- [ ] Optimize images
- [ ] Implement WebP serving
- [ ] Run Lighthouse audits

**Deliverable:** Optimized site with 40-70% smaller images

---

## 🎯 Quick Reference

### Current State (Plain HTML)
```
Files:      5 HTML files
Hosting:    GitHub Pages (manual)
Images:     Unoptimized (239KB screenshot)
Build:      None
Deploy:     Manual git push
```

### Target State (Jekyll)
```
Files:      Markdown + Layouts + Data files
Hosting:    GitHub Pages (auto-deploy)
Images:     Optimized + WebP (60-80KB)
Build:      Automated Jekyll build
Deploy:     git push = automatic deploy
```

### Performance Gains
```
Load time:  2-3s → 1-1.5s          (40% faster)
Images:     60-70% smaller
Lighthouse: 80 → 95+               (excellent)
Mobile:     Significantly improved
```

---

## 📖 How to Use These Documents

### If you have 5 minutes:
→ Read **JEKYLL_MIGRATION_SUMMARY.md**

### If you have 30 minutes:
→ Read **JEKYLL_MIGRATION_SUMMARY.md** + first section of **JEKYLL_MIGRATION_PLAN.md**

### If you're starting Phase 1 (Assessment):
→ Read Phase 1 section of **JEKYLL_MIGRATION_PLAN.md**

### If you're starting Phase 2 (Jekyll Setup):
→ Read Phase 2 section of **JEKYLL_MIGRATION_PLAN.md**

### If you're starting Phase 5 (Image Optimization):
→ Read **IMAGE_OPTIMIZATION_GUIDE.md**

### If you need a complete reference:
→ Keep **JEKYLL_MIGRATION_PLAN.md** open as you work

---

## ✅ Checklist

### Before Starting
- [ ] Review JEKYLL_MIGRATION_SUMMARY.md
- [ ] Have 11-18 hours available
- [ ] Ruby 3.0+ installed (`ruby --version`)
- [ ] Node.js installed (for image optimization)
- [ ] Backup current site (create branch)

### During Implementation
- [ ] Follow one phase at a time
- [ ] Test locally before pushing
- [ ] Reference appropriate documentation
- [ ] Commit regularly to git

### Before Go-Live
- [ ] All links working
- [ ] Images loading correctly
- [ ] Cal.com embeds functional
- [ ] Mobile responsive
- [ ] Lighthouse ≥90 on all metrics
- [ ] DNS updated if needed

---

## 🆘 Troubleshooting

### Common Issues

**Jekyll build fails**
→ See JEKYLL_MIGRATION_PLAN.md, Phase 7

**Images not showing**
→ See IMAGE_OPTIMIZATION_GUIDE.md, Part 8

**GitHub Actions workflow fails**
→ See JEKYLL_MIGRATION_PLAN.md, Phase 4

**Domain not resolving**
→ See JEKYLL_MIGRATION_PLAN.md, Phase 4

### Getting Help

1. Check the troubleshooting section of relevant document
2. Review complete phase documentation
3. Check GitHub Actions logs for deployment issues
4. Test locally first before assuming production issue

---

## 🔗 Related Resources

### Documentation
- [Jekyll Official Docs](https://jekyllrb.com/docs/)
- [GitHub Pages + Jekyll](https://docs.github.com/en/pages/setting-up-a-github-pages-site-with-jekyll)
- [Minima Theme Docs](https://github.com/jekyll/minima)

### Image Optimization
- [Sharp.js Docs](https://sharp.pixelplumbing.com/)
- [Web.dev Image Optimization](https://web.dev/image-optimization/)
- [WebP Format](https://developers.google.com/speed/webp)

### Performance Testing
- [Lighthouse](https://developers.google.com/web/tools/lighthouse)
- [PageSpeed Insights](https://pagespeed.web.dev/)

---

## 📊 Success Metrics

After migration, you should have:

✅ **Technical**
- Zero Jekyll build errors
- Automatic deployment on git push
- Lighthouse score ≥90 on all categories
- Page load < 1.5 seconds
- Images 60-70% smaller

✅ **Content**
- All 5 pages working
- Navigation complete
- Research content preserved
- ML tools functioning
- Cal.com embeds working

✅ **User Experience**
- Mobile responsive
- Navigation clear
- Fast loading
- Professional appearance
- SEO-friendly (sitemap, RSS, meta tags)

---

## 🚀 Next Steps

### Immediate (Today)
1. ✓ Read JEKYLL_MIGRATION_SUMMARY.md
2. ✓ Review this index
3. ✓ Set up todo tracking

### This Week (Phase 1)
1. Install Jekyll locally
2. Create directory structure
3. Set up _config.yml
4. Test local build

### Later Phases
- Follow the 7-phase plan in order
- One phase per week = 7-week timeline
- Or 2-3 phases per week = 2-3 week timeline

---

## 📝 Document Versions

| Document | Version | Updated | Status |
|----------|---------|---------|--------|
| JEKYLL_MIGRATION_SUMMARY.md | 1.0 | Nov 2025 | ✓ Complete |
| JEKYLL_MIGRATION_PLAN.md | 1.0 | Nov 2025 | ✓ Complete |
| IMAGE_OPTIMIZATION_GUIDE.md | 1.0 | Nov 2025 | ✓ Complete |
| MIGRATION_INDEX.md | 1.0 | Nov 2025 | ✓ Complete |

---

## 💡 Tips for Success

1. **Start small:** Migrate homepage first, then add pages
2. **Test frequently:** Use `bundle exec jekyll serve` to verify locally
3. **Keep backups:** Branch before major changes
4. **Follow the phases:** Don't skip ahead
5. **Reference docs:** Each phase has its own documentation
6. **Commit regularly:** Small commits easier to debug
7. **Ask for help:** GitHub Issues, Jekyll community forums

---

**Created:** November 2025
**For:** bc.com Jekyll Migration Project
**Status:** Ready for Phase 1 Implementation ✓

---

## Quick Start Commands

```bash
# Phase 1: Setup
ruby --version
gem install jekyll bundler
jekyll new bc-website

# Phase 2: Local testing
cd bc-website
bundle install
bundle exec jekyll serve

# Phase 3: Build for production
JEKYLL_ENV=production bundle exec jekyll build

# Phase 5: Image optimization (after npm setup)
npm install
npm run optimize
npm run check

# Phase 7: Testing
lighthouse https://localhost:4000
```

---

**Questions?** Reference the appropriate section above or the full JEKYLL_MIGRATION_PLAN.md
