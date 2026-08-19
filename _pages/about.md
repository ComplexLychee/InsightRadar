---
title: "关于 Insight Radar"
permalink: /about/
layout: single
---

Insight Radar 是一个全自动化的 arXiv 论文追踪与解读系统。

## 工作流

1. **候选生成**：GitHub Actions 定期检索 arXiv 最新论文
2. **人工筛选**：从候选池中勾选感兴趣的论文
3. **AI 解读**：调用 DeepSeek 模型生成结构化摘要
4. **自动发布**：生成 Markdown 并部署到博客

## 技术栈

- **检索**：arXiv API
- **解读**：DeepSeek via OpenCode
- **博客**：Jekyll + Minimal Mistakes
- **部署**：GitHub Pages
