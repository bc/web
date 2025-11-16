---
layout: default
permalink: /posts/
title: "Posts"
description: "Technical guides, ML tools, and deep dives on machine learning, avatars, and browser-based inference."
---

# Posts

Collection of technical guides, ML tools, and resources covering machine learning, avatar animation, and real-time inference in browsers.

{% if site.posts.size > 0 %}
{% for post in site.posts %}
<article class="post-preview">
  <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
  
  {% if post.date %}
  <p class="post-meta">
    <time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: "%B %d, %Y" }}</time>
  </p>
  {% endif %}
  
  {% if post.excerpt %}
  <div class="post-excerpt">
    {{ post.excerpt | markdownify | strip_html | truncate: 200 }}
  </div>
  {% endif %}
  
  <p><a href="{{ post.url | relative_url }}">Read more →</a></p>
</article>

{% unless forloop.last %}<hr>{% endunless %}
{% endfor %}
{% else %}
<p>No posts available yet.</p>
{% endif %}

---

**Questions or suggestions?** [Schedule a meeting](/meet/) or [contact us](mailto:brian.cohn@kaspect.com)
