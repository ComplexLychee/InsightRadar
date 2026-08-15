import arxiv
from openai import OpenAI
import os
import json
import time
from datetime import datetime, timedelta
from jinja2 import Template

# ==================== 关键词预设 ====================
KEYWORD_PRESETS = {
    "default": [
        {"query": "cat:cs.AI AND (large language model OR LLM OR transformer)", "name": "大模型"},
        {"query": "cat:cs.CV AND (multimodal OR vision language model OR VLM)", "name": "多模态"},
        {"query": "cat:cs.LG AND (reinforcement learning OR RLHF OR alignment)", "name": "强化学习"},
    ],
    "llm_only": [
        {"query": "cat:cs.AI AND (large language model OR LLM OR transformer OR GPT OR reasoning)", "name": "大模型"},
    ],
    "vision_only": [
        {"query": "cat:cs.CV AND (multimodal OR vision language model OR VLM OR diffusion OR image generation)", "name": "多模态与视觉"},
    ],
    "rl_only": [
        {"query": "cat:cs.LG AND (reinforcement learning OR RLHF OR alignment OR agent OR policy)", "name": "强化学习与智能体"},
    ],
    "all_areas": [
        {"query": "cat:cs.AI", "name": "人工智能"},
        {"query": "cat:cs.CV", "name": "计算机视觉"},
        {"query": "cat:cs.LG", "name": "机器学习"},
        {"query": "cat:cs.CL", "name": "计算语言学"},
        {"query": "cat:cs.RO", "name": "机器人"},
    ],
}

TIME_RANGE_DAYS = {
    "1_week": 7,
    "1_month": 30,
    "3_months": 90,
    "6_months": 180,
}

# ==================== 配置 ====================
MAX_RESULTS = 5
SITE_URL = os.getenv("SITE_URL", "https://ComplexLychee.github.io")
ARXIV_DELAY = 5
MAX_RETRIES = 3
# ===========================================================

def get_search_config():
    """根据环境变量返回搜索配置"""
    preset = os.getenv("KEYWORD_PRESET", "default")
    custom_query = os.getenv("CUSTOM_QUERY", "").strip()
    
    if custom_query:
        # 自定义查询：单分类模式
        return [{"query": custom_query, "name": "自定义检索"}]
    
    if preset in KEYWORD_PRESETS:
        return KEYWORD_PRESETS[preset]
    
    return KEYWORD_PRESETS["default"]

def get_date_range():
    """根据环境变量返回搜索日期范围"""
    range_key = os.getenv("TIME_RANGE", "1_week")
    days = TIME_RANGE_DAYS.get(range_key, 7)
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # 格式化显示
    range_display = {
        "1_week": "过去1周",
        "1_month": "过去1个月",
        "3_months": "过去3个月",
        "6_months": "过去6个月",
    }.get(range_key, f"过去{days}天")
    
    return start_date, end_date, range_display

def search_papers():
    search_config = get_search_config()
    start_date, end_date, range_display = get_date_range()
    
    print(f"📅 时间范围: {range_display} ({start_date.date()} ~ {end_date.date()})")
    print(f"🔧 关键词预设: {os.getenv('KEYWORD_PRESET', 'default')}")
    if os.getenv("CUSTOM_QUERY"):
        print(f"🔧 自定义查询: {os.getenv('CUSTOM_QUERY')}")
    print("=" * 50)
    
    seen_ids = set()
    all_papers = []
    
    for cfg in search_config:
        print(f"🔍 检索: {cfg['name']} ...")
        
        client = arxiv.Client(
            delay_seconds=ARXIV_DELAY,
            page_size=MAX_RESULTS,
        )
        
        search = arxiv.Search(
            query=cfg["query"],
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
            max_results=MAX_RESULTS,
        )
        
        for attempt in range(MAX_RETRIES):
            try:
                count = 0
                for result in client.results(search):
                    if result.entry_id in seen_ids:
                        continue
                    seen_ids.add(result.entry_id)
                    
                    pub_date = result.published.date()
                    if start_date.date() <= pub_date <= end_date.date():
                        all_papers.append({
                            "raw": result,
                            "category_name": cfg["name"],
                            "category_code": result.primary_category,
                        })
                        count += 1
                
                print(f"   ✅ {cfg['name']} 完成，找到 {count} 篇")
                break
                
            except arxiv.HTTPError as e:
                status = getattr(e, 'status', None)
                if status in (429, 503):
                    if attempt < MAX_RETRIES - 1:
                        wait_time = ARXIV_DELAY * (2 ** attempt)
                        print(f"   ⚠️ 限流(HTTP {status})，等待 {wait_time}s 后重试...")
                        time.sleep(wait_time)
                    else:
                        print(f"   ❌ {cfg['name']} 超过重试次数，跳过")
                        break
                else:
                    print(f"   ❌ {cfg['name']} 请求失败: {e}")
                    break
            except Exception as e:
                print(f"   ❌ {cfg['name']} 异常: {e}")
                break
    
    return all_papers, start_date, end_date, range_display

def analyze_paper(paper_info):
    paper = paper_info["raw"]
    client = OpenAI(
        api_key=os.getenv("OPENCODE_API_KEY"),
        base_url="https://opencode.ai/zen/v1",
    )
    
    authors = ", ".join([a.name for a in paper.authors[:5]])
    if len(paper.authors) > 5:
        authors += " 等"
    
    prompt = f"""请对以下学术论文进行结构化解读，只输出 JSON：

标题：{paper.title}
作者：{authors}
摘要：{paper.summary[:2000]}
领域：{paper_info['category_name']}

输出字段：
- one_sentence: 一句话概括核心贡献（30字以内，中文）
- highlights: 3个核心创新点（每条20字以内，中文数组）
- why_matters: 为什么值得关注（60字左右，中文）
- audience: 适合什么背景的读者（中文）
- tags: 相关技术标签数组（中文或英文）
- score: 重要性评分（1-10，整数）

注意：摘要可能截断，请基于已有信息判断。"""

    try:
        resp = client.chat.completions.create(
            model="deepseek-v4-flash",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.5,
            max_tokens=800,
        )
        data = json.loads(resp.choices[0].message.content)
        for key in ["one_sentence", "highlights", "why_matters", "audience", "tags", "score"]:
            if key not in data:
                data[key] = "" if key != "tags" else []
        if not isinstance(data["highlights"], list):
            data["highlights"] = [str(data["highlights"])]
        if not isinstance(data["tags"], list):
            data["tags"] = [paper_info["category_name"]]
        return data
    except Exception as e:
        print(f"❌ LLM 解读失败: {e}")
        return {
            "one_sentence": paper.title,
            "highlights": ["请阅读原文了解详情"],
            "why_matters": "该论文属于本期检索范围内的研究",
            "audience": paper_info["category_name"] + "研究者",
            "tags": [paper_info["category_name"]],
            "score": 5,
        }

def generate_post(papers_data, start_date, end_date, range_display):
    # 生成唯一标识：用日期+时间范围
    date_str = end_date.strftime("%Y-%m-%d")
    range_slug = range_display.replace("过去", "").replace(" ", "_")
    
    # 标题根据时间范围调整
    if range_display == "过去1周":
        title = f"AI 论文周刊 · {end_date.strftime('%Y-%m-%d')}"
        tag_label = "论文周刊"
    else:
        title = f"AI 论文洞察 · {range_display}精选 ({start_date.date()} ~ {end_date.date()})"
        tag_label = "论文洞察"
    
    papers_data.sort(key=lambda x: x.get("score", 5), reverse=True)
    
    all_tags = set(["arXiv", "AI", tag_label])
    for p in papers_data:
        all_tags.update(p.get("tags", []))
    
    # 如果没有论文，生成提示性内容
    if not papers_data:
        content_body = """
> ⚠️ **本期未检索到符合条件的论文**
> 
> 可能原因：
> - 该时间范围内该领域暂无新论文发布
> - 关键词过滤条件过于严格
> 
> 建议尝试：
> - 扩大时间范围（如从1周改为1个月）
> - 切换关键词预设（如从"大模型"改为"全部领域"）
> - 使用自定义查询扩大检索范围
"""
    else:
        template = Template("""{% for paper in papers %}
## {{ loop.index }}. {{ paper.title }} {% if paper.score >= 8 %}🔥{% endif %}

**作者**：{{ paper.authors }}  
**arXiv**：[{{ paper.arxiv_id }}]({{ paper.pdf_url }})  
**领域**：{{ paper.category_name }} (`{{ paper.category_code }}`)  
**标签**：{% for tag in paper.tags %}`{{ tag }}` {% endfor %}

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
        
        content_body = template.render(papers=papers_data)
    
    # 组装完整 Markdown
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

> 📅 **检索范围**：{range_display} ({start_date.date()} ~ {end_date.date()})  
> 📊 **本期精选**：{len(papers_data)} 篇论文  
> 🔧 **检索配置**：{os.getenv('KEYWORD_PRESET', 'default')}  
> 
> Insight Radar 定期追踪 AI 前沿动态。  
> 欢迎 [RSS 订阅]({SITE_URL}/feed.xml) 🔖

{content_body}

## 📮 订阅方式

| 方式 | 链接 |
|------|------|
| 🌐 博客主页 | {SITE_URL} |
| 📡 RSS 订阅 | {SITE_URL}/feed.xml |
| 🐙 源码仓库 | https://github.com/你的用户名/你的用户名.github.io |

---

*本报告由 GitHub Actions 自动生成，解读由 AI 辅助完成，仅供参考。*
"""
    return md

def main():
    print("=" * 50)
    print("🚀 Insight Radar 论文报告生成器")
    print("=" * 50)
    
    papers_raw, start_date, end_date, range_display = search_papers()
    print(f"\n📚 共找到 {len(papers_raw)} 篇论文")
    
    papers_data = []
    for info in papers_raw:
        print(f"\n📝 解读: {info['raw'].title[:60]}...")
        analysis = analyze_paper(info)
        
        paper = info["raw"]
        authors = ", ".join([a.name for a in paper.authors[:5]])
        if len(paper.authors) > 5:
            authors += " 等"
            
        papers_data.append({
            "title": paper.title.replace("\n", " "),
            "authors": authors,
            "arxiv_id": paper.entry_id.split("/")[-1],
            "pdf_url": paper.pdf_url,
            "category_name": info["category_name"],
            "category_code": info["category_code"],
            "published": paper.published.strftime("%Y-%m-%d"),
            **analysis
        })
    
    md_content = generate_post(papers_data, start_date, end_date, range_display)
    
    os.makedirs("_posts", exist_ok=True)
    # 文件名包含时间范围，避免覆盖
    range_slug = range_display.replace("过去", "").replace(" ", "_")
    filename = f"_posts/{end_date.strftime('%Y-%m-%d')}-insight-radar-{range_slug}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"\n✅ 成功生成: {filename}")
    print(f"📄 共 {len(papers_data)} 篇论文")

if __name__ == "__main__":
    main()
