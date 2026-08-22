import os
import re
import json
import requests
from datetime import datetime, timedelta
from jinja2 import Template

SITE_URL = os.getenv("SITE_URL", "https://complexlychee.github.io/InsightRadar")
API_BASE = "https://opencode.ai/zen/v1"

def find_latest_candidate():
    if not os.path.exists("candidates"):
        raise FileNotFoundError("candidates/ 目录不存在")
    files = [f for f in os.listdir("candidates") if f.endswith("-candidates.md")]
    if not files:
        raise FileNotFoundError("没有找到候选文件")
    files.sort(reverse=True)
    return os.path.join("candidates", files[0])

def list_candidate_files():
    if not os.path.exists("candidates"):
        return []
    files = [f for f in os.listdir("candidates") if f.endswith("-candidates.md")]
    files.sort(reverse=True)
    return files

def parse_selected_papers(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = re.split(r'\n---\n', content)
    selected = []

    for block in blocks:
        if not re.search(r'- \[[xX]\]\s*\*\*发布\*\*', block):
            continue

        title = re.search(r'- \*\*标题\*\*:\s*(.+)', block)
        authors = re.search(r'- \*\*作者\*\*:\s*(.+)', block)
        published = re.search(r'- \*\*发表日期\*\*:\s*(\d{4}-\d{2}-\d{2})', block)
        area = re.search(r'- \*\*所属领域\*\*:\s*(.+?)\s*\(', block)
        category = re.search(r'- \*\*所属领域\*\*:.*?\(`(.+?)`\)', block)
        pdf_url = re.search(r'- \*\*arXiv链接\*\*:\s*\[.*?\]\((.+?)\)', block)

        # 提取 OCAR 结构化摘要
        ocar_match = re.search(
            r'- \*\*OCAR 结构化摘要\*\*:\s*\n(.*?)(?=\n- |\n## |\n---\s*$)',
            block, re.DOTALL
        )
        summary_ocar = ""
        if ocar_match:
            summary_ocar = ocar_match.group(1).strip()

        # 兼容旧格式：结构化摘要
        if not summary_ocar:
            old_match = re.search(
                r'- \*\*结构化摘要\*\*:\s*\n(.*?)(?=\n- |\n## |\n---\s*$)',
                block, re.DOTALL
            )
            if old_match:
                summary_ocar = old_match.group(1).strip()

        # 兼容更旧格式：摘要预览
        if not summary_ocar:
            old_summary = re.search(r'- \*\*摘要预览.*?\*\*:\s*(.+)', block)
            if old_summary:
                summary_ocar = old_summary.group(1).strip()

        if title:
            selected.append({
                "title": title.group(1).strip(),
                "authors": authors.group(1).strip() if authors else "未知",
                "published": published.group(1) if published else "未知",
                "area": area.group(1).strip() if area else "未知",
                "category_code": category.group(1) if category else "cs.AI",
                "pdf_url": pdf_url.group(1) if pdf_url else "",
                "summary_ocar": summary_ocar,
                "source_file": os.path.basename(filepath),
            })

    return selected

def call_opencode(prompt, api_key, response_format=None):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": "deepseek-v4-flash", "messages": [{"role": "user", "content": prompt}],
               "temperature": 0.5, "max_tokens": 800}
    if response_format:
        payload["response_format"] = response_format
    try:
        resp = requests.post(f"{API_BASE}/chat/completions", headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ API 调用失败: {e}")
        return None

def analyze_paper_ocar(paper):
    """基于 OCAR 模板进行深度解读"""
    api_key = os.getenv("OPENCODE_API_KEY")
    context = paper.get("summary_ocar", "") or paper["title"]

    prompt = f"""请对以下学术论文进行 OCAR 结构化解读，只输出 JSON：

标题：{paper['title']}
作者：{paper['authors']}
发表日期：{paper['published']}
所属领域：{paper['area']}
背景信息：
{context}

请严格按照 OCAR 框架输出：
- opening_challenge: 这篇文章研究什么领域？面临的核心问题/挑战是什么？（40字以内，中文）
- action: 文章采取了什么具体行动、方法或技术方案？（60字以内，中文）
- resolution: 最终达成了什么效果、解决了什么问题？（40字以内，中文）
- highlights: 3个核心创新点（每条20字以内，中文数组）
- why_matters: 为什么值得关注（60字左右，中文）
- audience: 适合什么背景的读者（中文）
- tags: 相关技术标签数组（中文或英文）
- score: 重要性评分（1-10，整数）

注意：基于提供的背景信息判断。"""

    content = call_opencode(prompt, api_key, {"type": "json_object"})
    if content:
        try:
            data = json.loads(content)
            for key in ["opening_challenge", "action", "resolution", "highlights", "why_matters", "audience", "tags", "score"]:
                if key not in data:
                    if key in ("tags", "highlights"):
                        data[key] = []
                    elif key == "score":
                        data[key] = 5
                    else:
                        data[key] = ""
            if not isinstance(data["highlights"], list):
                data["highlights"] = [str(data["highlights"])]
            if not isinstance(data["tags"], list):
                data["tags"] = [paper["area"]]
            
            # 确保 score 是整数
            try:
                data["score"] = int(data["score"])
            except (ValueError, TypeError):
                data["score"] = 5
            
            return data
        except json.JSONDecodeError:
            print(f"❌ JSON 解析失败")

    # 失败回退：基于已有 OCAR 摘要生成基础字段
    return {
        "opening_challenge": "请阅读原文了解详情",
        "action": "请阅读原文了解详情",
        "resolution": "请阅读原文了解详情",
        "highlights": ["请阅读原文了解详情"],
        "why_matters": "该论文属于本期精选研究",
        "audience": paper["area"] + "研究者",
        "tags": [paper["area"]],
        "score": 5,
    }

def auto_tag_paper(paper, analysis_tags):
    text = (paper.get('title', '') + ' ' + 
            paper.get('summary_ocar', '') + ' ' + 
            paper.get('area', '') + ' ' +
            ' '.join(analysis_tags)).lower()

    auto_tags = set()
    sdc_keywords = [
        "silent data corruption", "soft error", "sdc", "hardware fault",
        "fault tolerance", "error resilience", "transient fault", "seu",
        "memory error", "bit flip", "data integrity", "corruption detection",
        "硬件故障", "软错误", "容错", "数据损坏", "可靠性", "硬件架构",
        "分布式系统可靠性", "ml训练可靠性"
    ]
    if any(kw in text for kw in sdc_keywords):
        auto_tags.add('SDC')

    agent_keywords = [
        "research agent", "ai scientist", "self-research", "self evolving",
        "self-evolving", "autonomous research", "automated discovery",
        "scientific discovery", "ai for science", "agentic",
        "omni-scientist", "ai for science", "automated discovery"
    ]
    if any(kw in text for kw in agent_keywords):
        auto_tags.add('Agents')

    return sorted(auto_tags)

def generate_post(papers_data, range_display, start_date, end_date, source_files):
    date_str = end_date.strftime("%Y-%m-%d")
    
    # 修复：确保所有 score 都是整数
    for p in papers_data:
        try:
            p["score"] = int(p.get("score", 5))
        except (ValueError, TypeError):
            p["score"] = 5
    
    papers_data.sort(key=lambda x: x.get("score", 5), reverse=True)

    all_tags = set(["arXiv", "AI", tag_label])
    all_auto_tags = set()
    for p in papers_data:
        llm_tags = p.get("tags", [])
        auto_tags = auto_tag_paper(p, llm_tags)
        p["auto_tags"] = auto_tags
        all_tags.update(llm_tags)
        all_tags.update(auto_tags)
        all_auto_tags.update(auto_tags)

    column_badges = ""
    if "SDC" in all_auto_tags:
        column_badges += "<span style='background:#dbeafe;color:#1e40af;padding:2px 8px;border-radius:12px;font-size:0.8em;margin-right:6px;'>🔧 SDC</span>"
    if "Agents" in all_auto_tags:
        column_badges += "<span style='background:#ede9fe;color:#5b21b6;padding:2px 8px;border-radius:12px;font-size:0.8em;'>🤖 Agents</span>"

    source_info = " | ".join([f"`{f}`" for f in source_files])

    # OCAR 模板博客文章
    template = Template("""{% for paper in papers %}
## {{ loop.index }}. {{ paper.title }} {% if paper.score >= 8 %}🔥{% endif %}

**作者**：{{ paper.authors }}  
**发表日期**：{{ paper.published }}  
**arXiv**：[{{ paper.arxiv_id }}]({{ paper.pdf_url }})  
**领域**：{{ paper.area }} (`{{ paper.category_code }}`)  
**来源**：{{ paper.source_file }}  
**标签**：{% for tag in paper.tags %}`{{ tag }}` {% endfor %}{% if paper.auto_tags %}{% for atag in paper.auto_tags %}<span style="background:{% if atag == 'SDC' %}#dbeafe{% else %}#ede9fe{% endif %};color:{% if atag == 'SDC' %}#1e40af{% else %}#5b21b6{% endif %};padding:1px 6px;border-radius:10px;font-size:0.75em;margin-left:4px;">{{ atag }}</span>{% endfor %}{% endif %}

### 🔍 Opening & Challenge
{{ paper.opening_challenge }}

### ⚙️ Action
{{ paper.action }}

### ✅ Resolution
{{ paper.resolution }}

### ✨ 核心亮点
{% for h in paper.highlights %}
- {{ h }}
{% endfor %}

### 🎯 为什么关注
{{ paper.why_matters }}

### 👥 适合读者
{{ paper.audience }}

---
{% endfor %}""")

    content_body = template.render(papers=papers_data) if papers_data else "> ⚠️ 未勾选任何论文"

    md = f"""---
title: "{title}"
date: {date_str} 08:00:00 +0800
categories:
  - {tag_label}
tags:
"""
    for tag in sorted(all_tags):
        md += f"  - {tag}\n"

    md += f"""toc: true
toc_sticky: true
---

> 📅 **检索范围**：{range_display} ({start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')})  
> 📊 **本期精选**：{len(papers_data)} 篇论文（人工筛选）  
> 📁 **来源文件**：{source_info}  
> {column_badges}
> 
> Insight Radar 定期追踪 AI 前沿动态。  
> 欢迎 [RSS 订阅]({SITE_URL}/feed.xml) 🔖

{content_body}

## 📮 订阅方式

| 方式 | 链接 |
|------|------|
| 🌐 博客主页 | {SITE_URL} |
| 📡 RSS 订阅 | {SITE_URL}/feed.xml |
| 🔧 SDC 专栏 | {SITE_URL}/columns/sdc/ |
| 🤖 Agents 专栏 | {SITE_URL}/columns/agents/ |
| 🐙 源码仓库 | https://github.com/ComplexLychee/InsightRadar |

---

*本报告由 GitHub Actions 自动生成，论文经人工筛选，解读由 AI 辅助完成。*
"""
    return md

def main():
    print("=" * 60)
    print("🚀 Insight Radar · 发布已勾选的论文（OCAR 模板）")
    print("=" * 60)

    candidate_input = os.getenv("CANDIDATE_FILE", "").strip()
    merge_input = os.getenv("MERGE_MULTIPLE", "").strip()

    all_papers = []
    source_files = []

    if merge_input:
        file_names = [f.strip() for f in merge_input.split(",") if f.strip()]
        print(f"📁 合并发布 {len(file_names)} 个候选文件:")
        for fname in file_names:
            fpath = os.path.join("candidates", fname)
            if not os.path.exists(fpath):
                print(f"   ❌ 文件不存在: {fname}，跳过")
                continue
            papers = parse_selected_papers(fpath)
            print(f"   ✅ {fname}: 勾选 {len(papers)} 篇")
            all_papers.extend(papers)
            source_files.append(fname)
    elif candidate_input:
        fpath = os.path.join("candidates", candidate_input)
        if not os.path.exists(fpath):
            raise FileNotFoundError(f"指定文件不存在: {fpath}")
        all_papers = parse_selected_papers(fpath)
        source_files = [candidate_input]
        print(f"📂 使用指定文件: {candidate_input}")
        print(f"✅ 勾选了 {len(all_papers)} 篇论文")
    else:
        candidate_file = find_latest_candidate()
        all_papers = parse_selected_papers(candidate_file)
        source_files = [os.path.basename(candidate_file)]
        print(f"📂 使用最新文件: {os.path.basename(candidate_file)}")
        print(f"✅ 勾选了 {len(all_papers)} 篇论文")

    if not all_papers:
        print("⚠️ 没有勾选的论文，跳过发布")
        print("👉 提示：请打开 candidates/ 下的文件，将 `- [ ]` 改为 `- [x]`")
        return

    # 去重
    seen_titles = set()
    unique_papers = []
    for p in all_papers:
        if p["title"] not in seen_titles:
            seen_titles.add(p["title"])
            unique_papers.append(p)
    if len(unique_papers) < len(all_papers):
        print(f"📝 去重后: {len(unique_papers)} 篇（原 {len(all_papers)} 篇）")
    all_papers = unique_papers

    # 提取日期范围
    first_file = os.path.join("candidates", source_files[0])
    with open(first_file, "r", encoding="utf-8") as f:
        content = f.read()

    range_match = re.search(r'\*\*检索区间\*\*:\s*(\d{4}-\d{2}-\d{2})\s*~\s*(\d{4}-\d{2}-\d{2})', content)
    display_match = re.search(r'# 📋 候选论文池 · (.+)', content)

    if range_match:
        start_date = datetime.strptime(range_match.group(1), "%Y-%m-%d")
        end_date = datetime.strptime(range_match.group(2), "%Y-%m-%d")
    else:
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

    range_display = display_match.group(1).strip() if display_match else "精选"

    # LLM OCAR 解读
    papers_data = []
    for p in all_papers:
        print(f"\n📝 OCAR 解读: {p['title'][:60]}...")
        analysis = analyze_paper_ocar(p)
        papers_data.append({**p, **analysis})
        auto_tags = auto_tag_paper(p, analysis.get("tags", []))
        if auto_tags:
            print(f"   🏷️ 自动标签: {', '.join(auto_tags)}")

    md_content = generate_post(papers_data, range_display, start_date, end_date, source_files)

    os.makedirs("_posts", exist_ok=True)
    range_slug = range_display.replace("过去", "").replace(" ", "_")
    filename = f"_posts/{end_date.strftime('%Y-%m-%d')}-insight-radar-{range_slug}.md"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"\n✅ 成功发布: {filename}")
    print(f"📄 共 {len(papers_data)} 篇论文")
    print(f"🌐 博客地址: {SITE_URL}")

if __name__ == "__main__":
    main()
