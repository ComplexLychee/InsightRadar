import os
import re
import json
import requests
from datetime import datetime, timedelta
from jinja2 import Template

SITE_URL = os.getenv("SITE_URL", "https://complexlychee.github.io/InsightRadar")
API_BASE = "https://opencode.ai/zen/v1"

def find_latest_candidates():
    """找到最新的候选文件"""
    if not os.path.exists("candidates"):
        raise FileNotFoundError("candidates/ 目录不存在")

    files = [f for f in os.listdir("candidates") if f.endswith("-candidates.md")]
    if not files:
        raise FileNotFoundError("没有找到候选文件")

    files.sort(reverse=True)
    return os.path.join("candidates", files[0])

def parse_selected_papers(filepath):
    """解析被勾选的论文"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 按 "---" 分割每篇论文区块
    blocks = re.split(r'\n---\n', content)
    selected = []

    for block in blocks:
        # 检查是否有 - [x] 标记
        if not re.search(r'- \[[xX]\]\s*\*\*发布\*\*', block):
            continue

        title = re.search(r'- \*\*标题\*\*:\s*(.+)', block)
        authors = re.search(r'- \*\*作者\*\*:\s*(.+)', block)
        published = re.search(r'- \*\*发表日期\*\*:\s*(\d{4}-\d{2}-\d{2})', block)
        area = re.search(r'- \*\*所属领域\*\*:\s*(.+?)\s*\(', block)
        category = re.search(r'- \*\*所属领域\*\*:.*?\(`(.+?)`\)', block)
        pdf_url = re.search(r'- \*\*arXiv链接\*\*:\s*\[.*?\]\((.+?)\)', block)
        summary = re.search(r'- \*\*摘要预览.*?\*\*:\s*(.+)', block)

        if title:
            selected.append({
                "title": title.group(1).strip(),
                "authors": authors.group(1).strip() if authors else "未知",
                "published": published.group(1) if published else "未知",
                "area": area.group(1).strip() if area else "未知",
                "category_code": category.group(1) if category else "cs.AI",
                "pdf_url": pdf_url.group(1) if pdf_url else "",
                "summary": summary.group(1).strip() if summary else "",
            })

    return selected

def call_opencode(prompt, api_key, response_format=None):
    """使用 requests 调用 OpenCode API"""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek-v4-flash",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.5,
        "max_tokens": 800
    }

    if response_format:
        payload["response_format"] = response_format

    try:
        resp = requests.post(
            f"{API_BASE}/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"❌ API 调用失败: {e}")
        return None

def analyze_paper(paper):
    """调用 LLM 深度解读"""
    api_key = os.getenv("OPENCODE_API_KEY")

    prompt = f"""请对以下学术论文进行结构化解读，只输出 JSON：

标题：{paper['title']}
作者：{paper['authors']}
发表日期：{paper['published']}
所属领域：{paper['area']}
摘要：{paper['summary']}

输出字段：
- one_sentence: 一句话概括核心贡献（30字以内，中文）
- highlights: 3个核心创新点（每条20字以内，中文数组）
- why_matters: 为什么值得关注（60字左右，中文）
- audience: 适合什么背景的读者（中文）
- tags: 相关技术标签数组（中文或英文）
- score: 重要性评分（1-10，整数）

注意：摘要可能截断，请基于已有信息判断。"""

    content = call_opencode(prompt, api_key, {"type": "json_object"})

    if content:
        try:
            data = json.loads(content)
            for key in ["one_sentence", "highlights", "why_matters", "audience", "tags", "score"]:
                if key not in data:
                    data[key] = "" if key != "tags" else []
            if not isinstance(data["highlights"], list):
                data["highlights"] = [str(data["highlights"])]
            if not isinstance(data["tags"], list):
                data["tags"] = [paper["area"]]
            return data
        except json.JSONDecodeError:
            print(f"❌ JSON 解析失败，返回原始内容")

    # 失败回退
    return {
        "one_sentence": paper["title"],
        "highlights": ["请阅读原文了解详情"],
        "why_matters": "该论文属于本期精选研究",
        "audience": paper["area"] + "研究者",
        "tags": [paper["area"]],
        "score": 5,
    }

def auto_tag_paper(paper, analysis_tags):
    """
    根据论文标题、摘要、领域自动判断专栏标签。
    返回要加入 frontmatter 的专栏标签列表（如 ['SDC'] 或 ['Agents'] 或两者都有）。
    """
    text = (paper.get('title', '') + ' ' + 
            paper.get('summary', '') + ' ' + 
            paper.get('area', '') + ' ' +
            ' '.join(analysis_tags)).lower()

    auto_tags = set()

    # SDC 关键词库
    sdc_keywords = [
        'silent data corruption', 'soft error', 'sdc', 'hardware fault',
        'fault tolerance', 'error resilience', 'transient fault', 'seu',
        'memory error', 'bit flip', 'data integrity', 'corruption detection',
        '硬件故障', '软错误', '容错', '数据损坏', '可靠性', '硬件架构',
        '分布式系统可靠性', 'ml训练可靠性'
    ]
    if any(kw in text for kw in sdc_keywords):
        auto_tags.add('SDC')

    # Agents 关键词库
    agent_keywords = [
        'agent', 'ai scientist', 'self-research', 'autonomous research',
        'research agent', 'scientific discovery', 'auto-design', 'auto-design',
        'multi-agent', '智能体', '自主科研', '自动化研究', 'agentic',
        'omni-scientist', 'ai for science', 'automated discovery'
    ]
    if any(kw in text for kw in agent_keywords):
        auto_tags.add('Agents')

    return sorted(auto_tags)

def generate_post(papers_data, range_display, start_date, end_date):
    """生成博客文章，frontmatter 中自动加入专栏标签"""
    date_str = end_date.strftime("%Y-%m-%d")

    if range_display == "过去1周":
        title = f"Insight Radar · 周刊 {date_str}"
        tag_label = "论文周刊"
    else:
        title = f"Insight Radar · {range_display}精选 ({start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')})"
        tag_label = "论文洞察"

    papers_data.sort(key=lambda x: x.get("score", 5), reverse=True)

    # 基础标签
    all_tags = set(["arXiv", "AI", tag_label])

    # 收集所有自动专栏标签
    all_auto_tags = set()
    for p in papers_data:
        # 合并 LLM 返回的标签和自动判断的标签
        llm_tags = p.get("tags", [])
        auto_tags = auto_tag_paper(p, llm_tags)
        p["auto_tags"] = auto_tags
        all_tags.update(llm_tags)
        all_tags.update(auto_tags)
        all_auto_tags.update(auto_tags)

    # 如果有专栏标签，在标题里提示
    column_badges = ""
    if "SDC" in all_auto_tags:
        column_badges += "<span style='background:#dbeafe;color:#1e40af;padding:2px 8px;border-radius:12px;font-size:0.8em;margin-right:6px;'>🔧 SDC</span>"
    if "Agents" in all_auto_tags:
        column_badges += "<span style='background:#ede9fe;color:#5b21b6;padding:2px 8px;border-radius:12px;font-size:0.8em;'>🤖 Agents</span>"

    template = Template("""{% for paper in papers %}
## {{ loop.index }}. {{ paper.title }} {% if paper.score >= 8 %}🔥{% endif %}

**作者**：{{ paper.authors }}  
**发表日期**：{{ paper.published }}  
**arXiv**：[{{ paper.arxiv_id }}]({{ paper.pdf_url }})  
**领域**：{{ paper.area }} (`{{ paper.category_code }}`)  
**标签**：{% for tag in paper.tags %}`{{ tag }}` {% endfor %}{% if paper.auto_tags %}{% for atag in paper.auto_tags %}<span style="background:{% if atag == 'SDC' %}#dbeafe{% else %}#ede9fe{% endif %};color:{% if atag == 'SDC' %}#1e40af{% else %}#5b21b6{% endif %};padding:1px 6px;border-radius:10px;font-size:0.75em;margin-left:4px;">{{ atag }}</span>{% endfor %}{% endif %}

### 💡 一句话总结
{{ paper.one_sentence }}

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
    print("🚀 Insight Radar · 发布已勾选的论文")
    print("=" * 60)

    candidate_file = find_latest_candidates()
    print(f"📂 读取候选文件: {candidate_file}")

    papers = parse_selected_papers(candidate_file)
    print(f"✅ 勾选了 {len(papers)} 篇论文")

    if not papers:
        print("⚠️ 没有勾选的论文，跳过发布")
        print("👉 提示：请打开 candidates/ 下的最新文件，将 `- [ ]` 改为 `- [x]`")
        return

    # 从文件内容提取日期范围
    with open(candidate_file, "r", encoding="utf-8") as f:
        content = f.read()

    range_match = re.search(r'\*\*检索区间\*\*:\s*(\d{4}-\d{2}-\d{2})\s*~\s*(\d{4}-\d{2}-\d{2})', content)
    display_match = re.search(r'# 📋 候选论文池 · (.+)', content)

    # 修复：字符串转 datetime
    if range_match:
        start_date = datetime.strptime(range_match.group(1), "%Y-%m-%d")
        end_date = datetime.strptime(range_match.group(2), "%Y-%m-%d")
    else:
        # 备用：从文件名解析
        basename = os.path.basename(candidate_file).replace("-candidates.md", "")
        try:
            end_date = datetime.strptime(basename, "%Y-%m-%d")
            start_date = end_date - timedelta(days=7)
        except ValueError:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)

    range_display = display_match.group(1).strip() if display_match else "精选"

    # LLM 解读
    papers_data = []
    for p in papers:
        print(f"\n📝 解读: {p['title'][:60]}...")
        analysis = analyze_paper(p)
        papers_data.append({**p, **analysis})

        # 打印自动标签（调试用）
        auto_tags = auto_tag_paper(p, analysis.get("tags", []))
        if auto_tags:
            print(f"   🏷️ 自动标签: {', '.join(auto_tags)}")

    md_content = generate_post(papers_data, range_display, start_date, end_date)

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
