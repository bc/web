source "https://rubygems.org"

# Jekyll
gem "jekyll", "~> 4.3"
gem "minima", "~> 2.5"

# Jekyll plugins
group :jekyll_plugins do
  gem "jekyll-feed", "~> 0.17"
  gem "jekyll-seo-tag", "~> 2.8"
  gem "jekyll-sitemap", "~> 1.4"
  gem "jekyll-paginate", "~> 1.1"
end

# Development dependencies
group :development, :test do
  gem "webrick", "~> 1.8"
  gem "html-proofer", "~> 5.0" # For testing generated HTML
end

# Windows and JRuby support
platforms :mingw, :x64_mingw, :mswin, :jruby do
  gem "tzinfo", ">= 1", "< 3"
  gem "tzinfo-data"
end

# Performance booster for watching directories on Windows
gem "wdm", "~> 0.1.1", :platforms => [:mingw, :x64_mingw, :mswin]
