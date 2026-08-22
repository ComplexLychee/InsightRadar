---
title: "🤖 Self Research Agents 专栏"
permalink: /columns/agents/
layout: archive
author_profile: false
---

> **Self Research Agents** 关注 AI 自主科研、自动化论文阅读、多智能体协作发现新知识。
> 
> 涵盖：AI Scientist、自动化实验、文献综述智能体、科研助手

---

{% assign agent_posts = site.posts | where_exp: "post", "post.tags contains 'Agents'" %}

{% if agent_posts.size == 0 %}
> ⚠️ 该专栏暂无文章，请稍后再来。
{% else %}
**本专栏共 {{ agent_posts.size }} 篇文章**

{% for post in agent_posts %}
<article class="archive__item" style="margin-bottom: 1.5em; padding: 1em; border-left: 4px solid #7c3aed; background: #f5f3ff;">
  <h3><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h3>
  <p>📅 {{ post.date | date: "%Y-%m-%d" }} · {{ post.excerpt | strip_html | truncate: 120 }}</p>
</article>
{% endfor %}
{% endif %}
