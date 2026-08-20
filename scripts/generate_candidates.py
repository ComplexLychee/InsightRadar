import os
import re
import time
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# ==================== 配置 ====================
KEYWORD_PRESETS = {
    "default": [
        {"query": "ti:llm OR ti:transformer OR abs:transformer", "name": "大模型"},
        {"query": "ti:multimodal OR ti:VLM OR abs:vision language", "name": "多模态"},
        {"query": "ti:reinforcement learning OR abs:RLHF", "name": "强化学习"},
    ],
    "llm_only": [
        {"query": "ti:llm OR ti:transformer OR ti:GPT OR abs:large language model", "name": "大模型"},
    ],
    "vision_only": [
        {"query": "ti:multimodal OR ti:VLM OR ti:diffusion OR abs:vision language", "name": "多模态与视觉"},
    ],
    "rl_only": [
        {"query": "ti:reinforcement learning OR ti:RLHF OR abs:reinforcement learning", "name": "强化学习与智能体"},
    ],
    "sdc_reliability": [
        {"query": 'ti:"silent data corruption" OR abs:"silent data corruption"', "name": "SDC精确短语"},
        {"query": 'ti:"soft error" OR abs:"soft error" OR ti:SEU OR abs:SEU', "name": "软错误"},
        {"query": "ti:corruption AND (ti:hardware OR ti:memory OR abs:hardware)", "name": "硬件数据损坏"},
        {"query": 'ti:"fault tolerance" OR abs:"fault tolerance" OR ti:"error resilience"', "name": "容错计算"},
        {"query": 'ti:"hardware fault" OR abs:"hardware fault" OR ti:"transient fault"', "name": "硬件故障"},
    ],
    "all_areas": [
        {"query": "cat:cs.AI", "name": "人工智能"},
        {"query": "cat:cs.CV", "name": "计算机视觉"},
        {"query": "cat:cs.LG", "name": "机器学习"},
        {"query": "cat:cs.CL", "name": "计算语言学"},
        {"query": "cat:cs.RO", "name": "机器人"},
    ],
}

SDC_KEYWORDS = [
    "silent data corruption", "soft error", "data corruption", 
    "hardware fault", "fault tolerance", "error resilience",
    "transient fault", "SEU", "memory error", "bit flip"
]

ARXIV_DELAY = 5
MAX_RETRIES = 3
MAX_RESULTS_PER_QUERY = 100
NS = {
    'atom': 'http://www.w3.org/2005/Atom',
    'arxiv': 'http://arxiv.org/schemas/atom'
}
# ===========================================================

def parse_time_range(time_str):
    time_str = time_str.strip().lower()
    match = re.match(r'^(\d+)\s*([a-z]+)$', time_str)
    if not match:
        end = datetime.now()
        start = end - timedelta(days=7)
        return start, end, "过去1周"
    
    num, unit_raw = int(match.group(1)), match.group(2)
    unit_map = {'d':'day','day':'day','days':'day','w':'week','week':'week','weeks':'week',
                'm':'month','month':'month','months':'month','y':'year','year':'year','years':'year'}
    unit = unit_map.get(unit_raw)
    if not unit:
        end = datetime.now()
        start = end - timedelta(days=7)
        return start, end, "过去1周"
    
    days = num if unit == 'day' else num*7 if unit == 'week' else num*30 if unit == 'month' else num*365
    end = datetime.now()
    start = end - timedelta(days=days)
    display = f"过去{num}{'天' if unit=='day' else '周' if unit=='week' else '个月' if unit=='month' else '年'}"
    return start, end, display

def get_search_config():
    preset = os.getenv("KEYWORD_PRESET", "sdc_reliability")
    custom = os.getenv("CUSTOM_QUERY", "").strip()
    
    print(f"   [DEBUG] KEYWORD_PRESET='{preset}'")
    print(f"   [DEBUG] CUSTOM_QUERY='{custom}'")
    
    if custom:
        query = f'ti:"{custom}" OR abs:"{custom}"'
        print(f"   [DEBUG] 使用自定义查询（自动补全）: {query}")
        return [{"query": query, "name": "自定义检索"}]
    
    if preset in KEYWORD_PRESETS:
        print(f"   [DEBUG] 使用预设: {preset}")
        return KEYWORD_PRESETS[preset]
    
    print(f"   [DEBUG] 回退到 sdc_reliability")
    return KEYWORD_PRESETS["sdc_reliability"]

def is_relevant_paper(title, summary, keywords):
    text = (title + " " + summary).lower()
    for kw in keywords:
        if kw.lower() in text:
            return True, kw
    return False, None

import requests
import json

def translate_summary(text, api_key):
    """直接用 requests 调用 OpenCode API，无需 openai 包"""
    if not text or not text.strip():
        return "（无摘要）"
    
    text = text[:500].strip()
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-v4-flash",
        "messages": [{
            "role": "user",
            "content": f"将以下学术论文摘要翻译成简洁流畅的中文（保留专业术语英文原文），只输出翻译结果，不要解释：\n\n{text}"
        }],
        "temperature": 0.3,
        "max_tokens": 400
    }
    
    try:
        resp = requests.post(
            "https://opencode.ai/zen/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"   ⚠️ 翻译失败: {e}")
        return text[:200] + "..."  # 失败时返回原文截断

def parse_arxiv_xml(xml_content):
    root = ET.fromstring(xml_content)
    entries = []
    
    for entry in root.findall('atom:entry', NS):
        entry_id = entry.find('atom:id', NS)
        entry_id = entry_id.text if entry_id is not None else ""
        
        title_elem = entry.find('atom:title', NS)
        title = title_elem.text.replace('\n', ' ').strip() if title_elem is not None else "无标题"
        
        authors_list = []
        for author in entry.findall('atom:author', NS):
            name_elem = author.find('atom:name', NS)
            name = name_elem.text if name_elem is not None else "Unknown"
            aff_elem = author.find('arxiv:affiliation', NS)
            aff = aff_elem.text if aff_elem is not None else None
            if aff:
                authors_list.append(f"{name} ({aff})")
            else:
                authors_list.append(f"{name} (单位未提供)")
        
        authors_str = ", ".join(authors_list[:5])
        if len(authors_list) > 5:
            authors_str += f" 等（共{len(authors_list)}人）"
        
        pub_elem = entry.find('atom:published', NS)
        published = pub_elem.text if pub_elem is not None else ""
        
        cat_elem = entry.find('arxiv:primary_category', NS)
        category = cat_elem.get('term', 'unknown') if cat_elem is not None else "unknown"
        
        sum_elem = entry.find('atom:summary', NS)
        summary = sum_elem.text if sum_elem is not None else ""
        summary_clean = summary[:600].replace('\n', ' ')
        
        pdf_url = ""
        for link in entry.findall('atom:link', NS):
            if link.get('title') == 'pdf':
                pdf_url = link.get('href', '')
                break
        
        entries.append({
            "entry_id": entry_id,
            "title": title,
            "authors": authors_str,
            "published_raw": published,
            "category": category,
            "summary": summary,
            "summary_clean": summary_clean,
            "pdf_url": pdf_url,
        })
    
    return entries

def search_arxiv_api(query, max_results=100):
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    
    for attempt in range(MAX_RETRIES):
        try:
            print(f"   [DEBUG] 请求: {url}?search_query={query.replace(' ', '+')}")
            resp = requests.get(url, params=params, timeout=60)
            print(f"   [DEBUG] HTTP状态: {resp.status_code}")
            
            if resp.status_code == 200:
                entries = parse_arxiv_xml(resp.content)
                print(f"   [DEBUG] 解析到 {len(entries)} 条结果")
                return entries
            elif resp.status_code in (429, 503):
                if attempt < MAX_RETRIES - 1:
                    wait_time = ARXIV_DELAY * (2 ** attempt)
                    print(f"   ⚠️ 限流，等待 {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    return []
            else:
                return []
        except Exception as e:
            print(f"   ❌ 请求异常: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(ARXIV_DELAY * (2 ** attempt))
            else:
                return []
    return []

def search_papers():
    search_config = get_search_config()
    start, end, display = parse_time_range(os.getenv("TIME_RANGE", "1 week"))
    preset = os.getenv("KEYWORD_PRESET", "sdc_reliability")
    
    use_filter = (preset == "sdc_reliability")
    filter_keywords = SDC_KEYWORDS if use_filter else []
    
    print(f"📅 检索区间: {start.date()} ~ {end.date()} ({display})")
    print(f"🔧 关键词预设: {preset}")
    print(f"🔍 客户端二次过滤: {'开启' if use_filter else '关闭'}")
    print("=" * 60)
    
    seen_ids = set()
    all_papers = []
    log_records = []
    
    for cfg in search_config:
        print(f"🔍 {cfg['name']}: {cfg['query']}")
        
        category_log = {
            "category_name": cfg["name"],
            "query": cfg["query"],
            "raw_results": 0,
            "kept": [],
            "excluded": [],
            "error": None,
        }
        
        entries = search_arxiv_api(cfg["query"], MAX_RESULTS_PER_QUERY)
        
        if not entries:
            category_log["error"] = "API无返回"
            log_records.append(category_log)
            continue
        
        category_log["raw_results"] = len(entries)
        count_kept = 0
        
        for e in entries:
            entry_id = e["entry_id"]
            
            try:
                pub_date = datetime.fromisoformat(e["published_raw"].replace('Z', '+00:00')).date()
            except:
                pub_date = datetime.now().date()
            
            if not (start.date() <= pub_date <= end.date()):
                category_log["excluded"].append({
                    "entry_id": entry_id.split("/")[-1] if "/" in entry_id else entry_id,
                    "title": e["title"],
                    "published": pub_date.strftime("%Y-%m-%d"),
                    "reason": "超出时间范围"
                })
                continue
            
            if entry_id in seen_ids:
                category_log["excluded"].append({
                    "entry_id": entry_id.split("/")[-1] if "/" in entry_id else entry_id,
                    "title": e["title"],
                    "published": pub_date.strftime("%Y-%m-%d"),
                    "reason": "重复"
                })
                continue
            
            if use_filter:
                relevant, matched_kw = is_relevant_paper(e["title"], e["summary"], filter_keywords)
                if not relevant:
                    category_log["excluded"].append({
                        "entry_id": entry_id.split("/")[-1] if "/" in entry_id else entry_id,
                        "title": e["title"],
                        "published": pub_date.strftime("%Y-%m-%d"),
                        "reason": "客户端过滤：标题/摘要不包含SDC关键词"
                    })
                    continue
                print(f"   ✓ 关键词命中: '{matched_kw}' -> {e['title'][:50]}...")
            
            seen_ids.add(entry_id)
            count_kept += 1
            category_log["kept"].append({
                "entry_id": entry_id.split("/")[-1] if "/" in entry_id else entry_id,
                "title": e["title"],
                "published": pub_date.strftime("%Y-%m-%d"),
            })
            
            all_papers.append({
                "entry_id": entry_id,
                "title": e["title"],
                "authors": e["authors"],
                "published": pub_date.strftime("%Y-%m-%d"),
                "category": e["category"],
                "area": cfg["name"],
                "summary": e["summary_clean"],
                "pdf_url": e["pdf_url"],
            })
        
        print(f"   ✅ 原始返回 {len(entries)} 篇，时间过滤后保留 {count_kept} 篇")
        log_records.append(category_log)
        time.sleep(ARXIV_DELAY)
    
    # ========== 新增：翻译摘要 ==========
    if all_papers:
        print(f"\n🌐 开始翻译 {len(all_papers)} 篇论文摘要...")
        
        api_key = os.getenv("OPENCODE_API_KEY")
        for i, p in enumerate(all_papers, 1):
            print(f"   📝 翻译 {i}/{len(all_papers)}: {p['title'][:40]}...")
            p["summary_zh"] = translate_summary(p["summary"], api_key)
            
        print("✅ 翻译完成")
    # ====================================
    
    all_papers.sort(key=lambda x: x["published"], reverse=True)
    return all_papers, start, end, display, log_records

def generate_candidates_md(papers, start, end, display):
    date_str = end.strftime("%Y-%m-%d")
    lines = [
        f"# 📋 候选论文池 · {display}",
        f"",
        f"> **检索区间**: {start.date()} ~ {end.date()}",
        f"> **候选总数**: {len(papers)} 篇",
        f"> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"",
        f"## ✅ 使用说明",
        f"1. 浏览下方论文列表（摘要已翻译为中文）",
        f"2. 将想发布的论文前面的 `- [ ]` 改为 `- [x]`",
        f"3. 保存文件（Commit）",
        f"4. 手动运行 **Publish Selected** workflow",
        f"",
        f"---",
        f"",
    ]
    
    for i, p in enumerate(papers, 1):
        lines.extend([
            f"## 论文 {i}",
            f"- [ ] **发布**",
            f"- **标题**: {p['title']}",
            f"- **作者**: {p['authors']}",
            f"- **发表日期**: {p['published']}",
            f"- **所属领域**: {p['area']} (`{p['category']}`)",
            f"- **arXiv链接**: [{p['entry_id'].split('/')[-1]}]({p['pdf_url']})",
            f"- **摘要预览（中文）**: {p.get('summary_zh', p['summary'])}...",
            f"",
            f"---",
            f"",
        ])
    
    return "\n".join(lines)

def generate_log_md(log_records, start, end, display, total_kept):
    lines = [
        "# 🔍 检索排查日志",
        f"",
        f"> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"> **检索区间**: {start.date()} ~ {end.date()} ({display})",
        f"> **关键词预设**: {os.getenv('KEYWORD_PRESET', 'sdc_reliability')}",
        f"> **最终保留**: {total_kept} 篇",
        f"",
        f"---",
        f"",
    ]
    
    for rec in log_records:
        lines.extend([
            f"## 📂 分类: {rec['category_name']}",
            f"",
            f"**查询语句**:",
            f"```",
            f"{rec['query']}",
            f"```",
            f"",
        ])
        
        if rec.get("error"):
            lines.extend([f"⚠️ **错误**: {rec['error']}", f""])
            continue
        
        lines.extend([
            f"**原始返回**: {rec['raw_results']} 篇",
            f"**保留**: {len(rec['kept'])} 篇 | **排除**: {len(rec['excluded'])} 篇",
            f"",
        ])
        
        if rec['kept']:
            lines.append("### ✅ 保留的论文")
            for p in rec['kept'][:20]:
                lines.append(f"- `{p['published']}` [{p['entry_id']}] {p['title']}")
            if len(rec['kept']) > 20:
                lines.append(f"- ... 等共 {len(rec['kept'])} 篇")
            lines.append("")
        
        if rec['excluded']:
            reasons = {}
            for p in rec['excluded']:
                r = p['reason']
                reasons[r] = reasons.get(r, 0) + 1
            lines.append("### ❌ 被排除的统计")
            for r, c in reasons.items():
                lines.append(f"- {r}: {c} 篇")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    total_raw = sum(r['raw_results'] for r in log_records)
    lines.extend([
        f"## 📊 汇总统计",
        f"",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| 分类数 | {len(log_records)} |",
        f"| 原始返回总数 | {total_raw} |",
        f"| 去重后保留 | {total_kept} |",
        f"| 时间范围 | {start.date()} ~ {end.date()} |",
        f"",
        f"---",
        f"",
        f"*此日志用于排查检索匹配度问题。*",
    ])
    
    return "\n".join(lines)

def main():
    print("=" * 60)
    print("🚀 Insight Radar · 候选池生成器（中文摘要版）")
    print("=" * 60)
    
    papers, start, end, display, log_records = search_papers()
    print(f"\n📚 总计候选: {len(papers)} 篇")
    
    os.makedirs("candidates", exist_ok=True)
    md_content = generate_candidates_md(papers, start, end, display)
    candidate_file = f"candidates/{end.strftime('%Y-%m-%d')}-candidates.md"
    with open(candidate_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"✅ 候选清单: {candidate_file}")
    
    os.makedirs("logs", exist_ok=True)
    log_content = generate_log_md(log_records, start, end, display, len(papers))
    log_file = f"logs/{end.strftime('%Y-%m-%d-%H%M')}-search-log.md"
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(log_content)
    print(f"✅ 排查日志: {log_file}")

if __name__ == "__main__":
    main()
