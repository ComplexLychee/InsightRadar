import arxiv
from openai import OpenAI
import os
import json
import time
from datetime import datetime, timedelta
from jinja2 import Template

# ==================== 配置区（按需修改） ====================
SEARCH_CONFIG = [
    {"query": "cat:cs.AI AND (large language model OR LLM OR transformer)", "name": "大模型"},
    {"query": "cat:cs.CV AND (multimodal OR vision language model OR VLM)", "name": "多模态"},
    {"query": "cat:cs.LG AND (reinforcement learning OR RLHF OR alignment)", "name": "强化学习"},
]
MAX_RESULTS = 5
SITE_URL = os.getenv("SITE_URL", "https://你的用户名.github.io")
# arXiv API 官方建议：任何自动化脚本请求间隔 ≥ 3 秒
# 这里设 5 秒更保守，避免 429/503
ARXIV_DELAY = 5
MAX_RETRIES = 3
# ===========================================================

def get_last_week_range():
    today = datetime.now()
    last_monday = today - timedelta(days=today.weekday() + 7)
    last_sunday = last_monday + timedelta(days=6)
    return last_monday, last_sunday

def search_papers():
    """
    使用 arxiv.Client 内置 delay 自动处理请求间隔，
    同时在外层加指数退避重试，应对 429/503。
    """
    last_monday, last_sunday = get_last_week_range()
    seen_ids = set()
    all_papers = []
    
    for cfg in SEARCH_CONFIG:
        print(f"🔍 检索: {cfg['name']} ...")
        
        # 每次搜索用新的 Client，内置 delay_seconds 自动节流
        client = arxiv.Client(
            delay_seconds=ARXIV_DELAY,
            page_size=MAX_RESULTS,  # 减少分页请求次数
        )
        
        search = arxiv.Search(
            query=cfg["query"],
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
            max_results=MAX_RESULTS,
        )
        
        for attempt in range(MAX_RETRIES):
            try:
                for result in client.results(search):
                    if result.entry_id in seen_ids:
                        continue
                    seen_ids.add(result.entry_id)
                    
                    pub_date = result.published.date()
                    if last_monday.date() <= pub_date <= last_sunday.date():
                        all_papers.append({
                            "raw": result,
                            "category_name": cfg["name"],
                            "category_code": result.primary_category,
                        })
                
                print(f"   ✅ {cfg['name']} 完成，找到 {len([p for p in all_papers if p['category_name'] == cfg['name']])} 篇")
                break  # 成功，跳出重试循环
                
            except arxiv.HTTPError as e:
                status = getattr(e, 'status', None)
                if status in (429, 503):
                    retry_count = attempt + 1
                    if retry_count < MAX_RETRIES:
                        # 指数退避：5s, 10s, 20s
                        wait_time = ARXIV_DELAY * (2 ** attempt)
                        print(f"   ⚠️ arXiv 限流 (HTTP {status})，等待 {wait_time} 秒后重试 ({retry_count}/{MAX_RETRIES})...")
                        time.sleep(wait_time)
                    else:
                        print(f"   ❌ {cfg['name']} 超过最大重试次数，跳过")
                        break
                else:
                    print(f"   ❌ {cfg['name']} 请求失败: {e}")
                    break
            except Exception as e:
                print(f"   ❌ {cfg['name']} 异常: {e}")
                break
    
    return all_papers, last_monday, last_sunday

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
            "why_matters": "该论文属于本周新发布的研究",
            "audience": paper_info["category_name"] + "研究者",
            "tags": [paper_info["category_name"]],
            "score": 5,
        }

def generate_post(papers_data, week_start, week_end):
    week_num = week_start.isocalendar()[1]
    year = week_start.year
    date_str = week_start.strftime("%Y-%m-%d")
    
    papers_data.sort(key=lambda x: x.get("score", 5), reverse=True)
    
    all_tags = set(["arXiv", "AI", "论文周刊"])
    for p in papers_data:
        all_tags.update(p.get("tags", []))
    
    template = Template("""---
title: "AI 论文周刊 · 第 {{ week_num }} 期 ({{ year }})"
date: {{ date_str }} 08:00:00 +0800
categories:
  - 论文周刊
tags:
{% for tag in tags %}  - {{ tag }}
{% endfor %}
toc: true
toc_sticky: true
---

> 📅 **本周范围**：{{ week_start }} ~ {{ week_end }}  
> 📊 **本期精选**：{{ papers|length }} 篇论文  
> 🏷️ **覆盖领域**：{% for c in categories %}{{ c }} {% endfor %}
> 
> 每周一早上 8 点更新，追踪 AI 前沿动态。  
> 欢迎 [RSS 订阅]({{ site_url }}/feed.xml) 🔖

---

{% for paper in papers %}
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
{% endfor %}

## 📮 订阅方式

| 方式 | 链接 |
|------|------|
| 🌐 博客主页 | {{ site_url }} |
| 📡 RSS 订阅 | {{ site_url }}/feed.xml |
| 🐙 源码仓库 | https://github.com/你的用户名/你的用户名.github.io |

---

*本周刊由 GitHub Actions 自动生成，解读由 AI 辅助完成，仅供参考。*
""")
    
    categories = list(set([p["category_name"] for p in papers_data]))
    
    return template.render(
        papers=papers_data,
        week_num=week_num,
        year=year,
        date_str=date_str,
        week_start=week_start.strftime("%Y-%m-%d"),
        week_end=week_end.strftime("%Y-%m-%d"),
        tags=sorted(all_tags),
        categories=categories,
        site_url=SITE_URL,
    )

def main():
    print("=" * 50)
    print("🚀 arXiv 论文周刊生成器")
    print("=" * 50)
    
    papers_raw, week_start, week_end = search_papers()
    print(f"\n📚 共找到 {len(papers_raw)} 篇上周论文")
    
    if not papers_raw:
        print("⚠️ 本周无论文，跳过生成")
        return
    
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
    
    md_content = generate_post(papers_data, week_start, week_end)
    
    os.makedirs("_posts", exist_ok=True)
    filename = f"_posts/{week_start.strftime('%Y-%m-%d')}-weekly-arxiv-{week_start.isocalendar()[1]}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"\n✅ 成功生成: {filename}")
    print(f"📄 共 {len(papers_data)} 篇论文")

if __name__ == "__main__":
    main()
