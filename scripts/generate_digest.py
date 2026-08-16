import arxiv
from openai import OpenAI
import os
import json
import time
import re
from datetime import datetime, timedelta
from jinja2 import Template

# ==================== 关键词预设 ====================
# 注意：arXiv API 中双引号 "phrase" 表示精确短语匹配，避免被拆成单个词
KEYWORD_PRESETS = {
    "default": [
        {"query": 'cat:cs.AI AND (llm OR "large language model" OR transformer)', "name": "大模型"},
        {"query": 'cat:cs.CV AND (multimodal OR "vision language model" OR VLM)', "name": "多模态"},
        {"query": 'cat:cs.LG AND ("reinforcement learning" OR RLHF OR alignment)', "name": "强化学习"},
    ],
    "llm_only": [
        {"query": 'cat:cs.AI AND (llm OR "large language model" OR transformer OR GPT OR reasoning)', "name": "大模型"},
    ],
    "vision_only": [
        {"query": 'cat:cs.CV AND (multimodal OR "vision language model" OR VLM OR diffusion OR "image generation")', "name": "多模态与视觉"},
    ],
    "rl_only": [
        {"query": 'cat:cs.LG AND ("reinforcement learning" OR RLHF OR alignment OR agent OR policy)', "name": "强化学习与智能体"},
    ],
    # SDC 预设：严格使用精确短语，去掉宽泛词，覆盖硬件/分布式/ML/安全/软件工程
    "sdc_reliability": [
        {
            "query": 'cat:cs.AR AND ("silent data corruption" OR "soft error" OR SDC OR "bit flip" OR "memory error" OR "transient fault")',
            "name": "硬件架构可靠性"
        },
        {
            "query": 'cat:cs.DC AND ("silent data corruption" OR "soft error" OR SDC OR "fault tolerance" OR "error resilience" OR checkpoint)',
            "name": "分布式系统可靠性"
        },
        {
            "query": 'cat:cs.LG AND ("silent data corruption" OR "soft error" OR SDC OR "training fault" OR "data integrity")',
            "name": "ML训练可靠性"
        },
        {
            "query": 'cat:cs.SE AND ("silent data corruption" OR "soft error" OR SDC OR "fault injection" OR "error detection")',
            "name": "软件工程可靠性"
        },
        {
            "query": 'cat:cs.CR AND ("silent data corruption" OR "soft error" OR SDC OR "data integrity" OR "corruption detection")',
            "name": "安全与数据完整性"
        },
    ],
    "all_areas": [
        {"query": "cat:cs.AI", "name": "人工智能"},
        {"query": "cat:cs.CV", "name": "计算机视觉"},
        {"query": "cat:cs.LG", "name": "机器学习"},
        {"query": "cat:cs.CL", "name": "计算语言学"},
        {"query": "cat:cs.RO", "name": "机器人"},
    ],
}

# ==================== 配置 ====================
# 默认每分类抓取数量
DEFAULT_MAX_RESULTS = 5
# SDC 预设使用更大的抓取量，因为精确查询结果少，需要多翻几篇才能覆盖时间范围
SDC_MAX_RESULTS = 20
SITE_URL = os.getenv("SITE_URL", "https://complexlychee.github.io")
ARXIV_DELAY = 5
MAX_RETRIES = 3
# ===========================================================

def parse_time_range(time_str):
    time_str = time_str.strip().lower()
    match = re.match(r'^(\d+)\s*([a-z]+)$', time_str)
    if not match:
        print(f"⚠️ 无法解析时间范围 '{time_str}'，默认使用 1 周")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        return start_date, end_date, "过去1周", 7
    
    num = int(match.group(1))
    unit_raw = match.group(2)
    
    unit_map = {
        'd': 'day', 'day': 'day', 'days': 'day',
        'w': 'week', 'week': 'week', 'weeks': 'week',
        'm': 'month', 'month': 'month', 'months': 'month',
        'y': 'year', 'year': 'year', 'years': 'year',
    }
    
    unit = unit_map.get(unit_raw)
    if not unit:
        print(f"⚠️ 未知时间单位 '{unit_raw}'，默认使用 1 周")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        return start_date, end_date, "过去1周", 7
    
    if unit == 'day':
        days = num
        unit_display = f"{num}天" if num > 1 else "1天"
    elif unit == 'week':
        days = num * 7
        unit_display = f"{num}周" if num > 1 else "1周"
    elif unit == 'month':
        days = num * 30
        unit_display = f"{num}个月" if num > 1 else "1个月"
    elif unit == 'year':
        days = num * 365
        unit_display = f"{num}年" if num > 1 else "1年"
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    range_display = f"过去{unit_display}"
    
    print(f"📅 解析时间范围: {time_str} → {range_display} ({days}天)")
    return start_date, end_date, range_display, days

def get_search_config():
    preset = os.getenv("KEYWORD_PRESET", "default")
    custom_query = os.getenv("CUSTOM_QUERY", "").strip()
    
    if custom_query:
        return [{"query": custom_query, "name": "自定义检索"}]
    
    if preset in KEYWORD_PRESETS:
        return KEYWORD_PRESETS[preset]
    
    return KEYWORD_PRESETS["default"]

def get_date_range():
    range_str = os.getenv("TIME_RANGE", "1 week")
    return parse_time_range(range_str)

def get_max_results():
    """根据预设动态调整抓取数量"""
    preset = os.getenv("KEYWORD_PRESET", "default")
    return SDC_MAX_RESULTS if preset == "sdc_reliability" else DEFAULT_MAX_RESULTS

def search_papers():
    search_config = get_search_config()
    start_date, end_date, range_display, days = get_date_range()
    max_results = get_max_results()
    
    print(f"🔧 关键词预设: {os.getenv('KEYWORD_PRESET', 'default')}")
    print(f"📊 每分类抓取: {max_results} 篇")
    if os.getenv("CUSTOM_QUERY"):
        print(f"🔧 自定义查询: {os.getenv('CUSTOM_QUERY')}")
    print(f"📅 检索区间: {start_date.date()} ~ {end_date.date()}")
    print("=" * 50)
    
    seen_ids = set()
    all_papers = []
    
    for cfg in search_config:
        print(f"🔍 检索: {cfg['name']} ...")
        print(f"   查询: {cfg['query'][:80]}...")
        
        client = arxiv.Client(
            delay_seconds=ARXIV_DELAY,
            page_size=max_results,
        )
        
        search = arxiv.Search(
            query=cfg["query"],
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
            max_results=max_results,
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
    date_str = end_date.strftime("%Y-%m-%d")
    
    if range_display == "过去1周":
        title = f"Insight Radar · 周刊 {end_date.strftime('%Y-%m-%d')}"
        tag_label = "论文周刊"
    else:
        title = f"Insight Radar · {range_display}精选 ({start_date.date()} ~ {end_date.date()})"
        tag_label = "论文洞察"
    
    papers_data.sort(key=lambda x: x.get("score", 5), reverse=True)
    
    all_tags = set(["arXiv", "AI", tag_label])
    for p in papers_data:
        all_tags.update(p.get("tags", []))
    
    if not papers_data:
        content_body = """
> ⚠️ **本期未检索到符合条件的论文**
> 
> 可能原因：
> - 该时间范围内该领域暂无新论文发布
> - 关键词过滤条件过于严格
> 
> 建议尝试：
> - 扩大时间范围（如从 1 周改为 1 个月）
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
| 🐙 源码仓库 | https://github.com/ComplexLychee/ComplexLychee.github.io |

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
    range_slug = range_display.replace("过去", "").replace(" ", "_")
    filename = f"_posts/{end_date.strftime('%Y-%m-%d')}-insight-radar-{range_slug}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"\n✅ 成功生成: {filename}")
    print(f"📄 共 {len(papers_data)} 篇论文")

if __name__ == "__main__":
    main()
