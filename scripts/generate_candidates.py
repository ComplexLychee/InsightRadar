import os
import re
import time
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

# ==================== 配置 ====================
KEYWORD_PRESETS = {
    "default": [
        {"query": "all:llm OR all:transformer", "name": "大模型"},
        {"query": "all:multimodal OR all:VLM", "name": "多模态"},
        {"query": "all:reinforcement learning", "name": "强化学习"},
    ],
    "llm_only": [
        {"query": "all:large language model OR all:GPT", "name": "大模型"},
    ],
    "vision_only": [
        {"query": "all:vision language model OR all:diffusion", "name": "多模态与视觉"},
    ],
    "rl_only": [
        {"query": "all:reinforcement learning OR all:RLHF", "name": "强化学习与智能体"},
    ],
    # 核心修复：直接用 HTTP 请求，不再依赖 arxiv 库
    "sdc_reliability": [
        {"query": "all:silent data corruption", "name": "SDC精确短语"},
        {"query": "all:soft error", "name": "软错误"},
        {"query": "all:data corruption", "name": "数据损坏"},
        {"query": "all:hardware fault", "name": "硬件故障"},
        {"query": "all:fault tolerance", "name": "容错计算"},
    ],
    "all_areas": [
        {"query": "cat:cs.AI", "name": "人工智能"},
        {"query": "cat:cs.CV", "name": "计算机视觉"},
        {"query": "cat:cs.LG", "name": "机器学习"},
        {"query": "cat:cs.CL", "name": "计算语言学"},
        {"query": "cat:cs.RO", "name": "机器人"},
    ],
}

ARXIV_DELAY = 5
MAX_RETRIES = 3
MAX_RESULTS_PER_QUERY = 20

# arXiv API 命名空间
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
    if custom:
        return [{"query": custom, "name": "自定义检索"}]
    return KEYWORD_PRESETS.get(preset, KEYWORD_PRESETS["sdc_reliability"])

def parse_arxiv_xml(xml_content):
    """解析 arXiv API 返回的 Atom XML"""
    root = ET.fromstring(xml_content)
    entries = []
    
    for entry in root.findall('atom:entry', NS):
        # entry_id
        entry_id = entry.find('atom:id', NS)
        entry_id = entry_id.text if entry_id is not None else ""
        
        # title
        title_elem = entry.find('atom:title', NS)
        title = title_elem.text.replace('\n', ' ').strip() if title_elem is not None else "无标题"
        
        # authors
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
        
        # published
        pub_elem = entry.find('atom:published', NS)
        published = pub_elem.text if pub_elem is not None else ""
        
        # primary_category
        cat_elem = entry.find('arxiv:primary_category', NS)
        category = cat_elem.get('term', 'unknown') if cat_elem is not None else "unknown"
        
        # summary
        sum_elem = entry.find('atom:summary', NS)
        summary = sum_elem.text[:400].replace('\n', ' ') if sum_elem is not None else ""
        
        # pdf_url
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
            "pdf_url": pdf_url,
        })
    
    return entries

def search_arxiv_api(query, max_results=20):
    """直接请求 arXiv API，绕过 arxiv Python 库"""
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
            print(f"   [DEBUG] 请求URL: {url}?search_query={query.replace(' ', '+')}")
            resp = requests.get(url, params=params, timeout=30)
            print(f"   [DEBUG] HTTP状态: {resp.status_code}")
            
            if resp.status_code == 200:
                entries = parse_arxiv_xml(resp.content)
                print(f"   [DEBUG] 解析到 {len(entries)} 条结果")
                return entries
            elif resp.status_code in (429, 503):
                if attempt < MAX_RETRIES - 1:
                    wait_time = ARXIV_DELAY * (2 ** attempt)
                    print(f"   ⚠️ 限流(HTTP {resp.status_code})，等待 {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    print(f"   ❌ 超过重试次数")
                    return []
            else:
                print(f"   ❌ HTTP错误: {resp.status_code}")
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
    
    print(f"📅 检索区间: {start.date()} ~ {end.date()} ({display})")
    print(f"🔧 关键词预设: {os.getenv('KEYWORD_PRESET', 'sdc_reliability')}")
    print("=" * 60)
    
    seen_ids = set()
    all_papers = []
    log_records = []
    
    for cfg in search_config:
        print(f"🔍 {cfg['name']}: {cfg['query']}")
        
        category_log = {
            "category_name": cfg["name"],
            "query": cfg["query"],
            "raw_results": [],
            "kept": [],
            "excluded": [],
            "error": None,
        }
        
        # 直接请求 API
        entries = search_arxiv_api(cfg["query"], MAX_RESULTS_PER_QUERY)
        
        if entries is None:
            category_log["error"] = "API请求失败"
            log_records.append(category_log)
            continue
        
        count_kept = 0
        for e in entries:
            entry_id = e["entry_id"]
            
            # 解析发表日期
            try:
                pub_date = datetime.fromisoformat(e["published_raw"].replace('Z', '+00:00')).date()
            except:
                pub_date = datetime.now().date()
            
            duplicate = entry_id in seen_ids
            if not duplicate:
                seen_ids.add(entry_id)
            
            in_range = start.date() <= pub_date <= end.date()
            
            paper_info = {
                "entry_id": entry_id.split("/")[-1] if "/" in entry_id else entry_id,
                "title": e["title"],
                "published": pub_date.strftime("%Y-%m-%d"),
                "primary_category": e["category"],
                "is_duplicate": duplicate,
                "in_time_range": in_range,
            }
            
            category_log["raw_results"].append(paper_info)
            
            if duplicate:
                category_log["excluded"].append({
                    **paper_info,
                    "reason": "重复（已在其他分类中检索到）"
                })
            elif not in_range:
                category_log["excluded"].append({
                    **paper_info,
                    "reason": f"超出时间范围（目标: {start.date()}~{end.date()}）"
                })
            else:
                category_log["kept"].append(paper_info)
                all_papers.append({
                    "entry_id": entry_id,
                    "title": e["title"],
                    "authors": e["authors"],
                    "published": pub_date.strftime("%Y-%m-%d"),
                    "category": e["category"],
                    "area": cfg["name"],
                    "summary": e["summary"],
                    "pdf_url": e["pdf_url"],
                })
                count_kept += 1
        
        print(f"   ✅ 原始返回 {len(entries)} 篇，保留 {count_kept} 篇")
        log_records.append(category_log)
        time.sleep(ARXIV_DELAY)
    
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
        f"1. 浏览下方论文列表",
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
            f"- **摘要预览**: {p['summary']}...",
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
        f"> **自定义查询**: {os.getenv('CUSTOM_QUERY', '无')}",
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
            lines.extend([
                f"⚠️ **错误**: {rec['error']}",
                f"",
            ])
            continue
        
        lines.extend([
            f"**原始返回**: {len(rec['raw_results'])} 篇",
            f"**保留**: {len(rec['kept'])} 篇 | **排除**: {len(rec['excluded'])} 篇",
            f"",
        ])
        
        if rec['kept']:
            lines.append("### ✅ 保留的论文（在时间范围内）")
            for p in rec['kept']:
                lines.append(f"- `{p['published']}` [{p['entry_id']}] {p['title']}")
            lines.append("")
        
        if rec['excluded']:
            lines.append("### ❌ 被排除的论文")
            for p in rec['excluded']:
                lines.append(f"- `{p['published']}` [{p['entry_id']}] {p['title']} — **原因**: {p['reason']}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    total_raw = sum(len(r['raw_results']) for r in log_records)
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
        f"*此日志用于排查检索匹配度问题，每次生成候选池时自动更新。*",
    ])
    
    return "\n".join(lines)

def main():
    print("=" * 60)
    print("🚀 Insight Radar · 候选池生成器（HTTP直连版）")
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
    
    print("\n👉 请打开 candidates/ 目录下的文件，勾选想发布的论文")
    print("👉 同时查看 logs/ 目录下的日志，排查匹配度问题")

if __name__ == "__main__":
    main()
