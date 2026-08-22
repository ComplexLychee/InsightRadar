---
title: "🔧 SDC 专栏"
permalink: /columns/sdc/
layout: archive
author_profile: false
---

> **Silent Data Corruption (SDC)** 是 Insight Radar 的核心追踪方向之一。
> 
> 关注：硬件故障、软错误、数据完整性、容错计算、分布式系统可靠性

---

{% assign sdc_posts = site.posts | where_exp: "post", "post.tags contains 'SDC'" %}

{% if sdc_posts.size == 0 %}
> ⚠️ 该专栏暂无文章，请稍后再来。
{% else %}
**本专栏共 {{ sdc_posts.size }} 篇文章**

{% for post in sdc_posts %}
<article class="archive__item" style="margin-bottom: 1.5em; padding: 1em; border-left: 4px solid #2563eb; background: #eff6ff;">
  <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
  <p>📅 {{ post.date | date: "%Y-%m-%d" }} · {{ post.excerpt | strip_html | truncate: 120 }}</p>
</article>
{% endfor %}
{% endif %}
