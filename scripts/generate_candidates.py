import arxiv
import os
import re
import time
from datetime import datetime, timedelta

# ==================== 关键词预设 ====================
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
    # 核心修复：去掉 cat: 前缀，改用全站搜索
    # "sdc_reliability": [
    #     {"query": "silent data corruption", "name": "SDC精确短语"},
    #     {"query": "soft error", "name": "软错误"},
    #     {"query": "data corruption", "name": "数据损坏"},
    #     {"query": "hardware fault", "name": "硬件故障"},
    #     {"query": "fault tolerance", "name": "容错计算"},
    # ],
    "sdc_reliability": [
    {"query": "all:corruption", "name": "损坏（测试API）"},
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

def format_authors(result):
    parts = []
    for author in result.authors:
        name = author.name
        aff = getattr(author, 'affiliation', None)
        if aff and aff.strip():
            parts.append(f"{name} ({aff.strip()})")
        else:
            parts.append(f"{name} (单位未提供)")
    authors_str = ", ".join(parts[:5])
    if len(result.authors) > 5:
        authors_str += f" 等（共{len(result.authors)}人）"
    return authors_str

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
        
        client = arxiv.Client(delay_seconds=ARXIV_DELAY, page_size=MAX_RESULTS_PER_QUERY)
        search = arxiv.Search(
            query=cfg["query"],
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
            max_results=MAX_RESULTS_PER_QUERY,
        )
        
        for attempt in range(MAX_RETRIES):
            try:
                count_kept = 0
                for result in client.results(search):
                    entry_id = result.entry_id
                    pub_date = result.published.date()
                    title = result.title.replace("\n", " ").strip()
                    
                    duplicate = entry_id in seen_ids
                    if not duplicate:
                        seen_ids.add(entry_id)
                    
                    in_range = start.date() <= pub_date <= end.date()
                    
                    paper_info = {
                        "entry_id": entry_id.split("/")[-1],
                        "title": title,
                        "published": pub_date.strftime("%Y-%m-%d"),
                        "primary_category": result.primary_category,
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
                            "raw": result,
                            "entry_id": entry_id,
                            "title": title,
                            "authors": format_authors(result),
                            "published": pub_date.strftime("%Y-%m-%d"),
                            "category": result.primary_category,
                            "area": cfg["name"],
                            "summary": result.summary[:400].replace("\n", " "),
                            "pdf_url": result.pdf_url,
                        })
                        count_kept += 1
                
                print(f"   ✅ 原始返回 {len(category_log['raw_results'])} 篇，保留 {count_kept} 篇")
                break
                
            except arxiv.HTTPError as e:
                status = getattr(e, 'status', None)
                if status in (429, 503) and attempt < MAX_RETRIES - 1:
                    wait_time = ARXIV_DELAY * (2 ** attempt)
                    print(f"   ⚠️ 限流(HTTP {status})，等待 {wait_time}s 后重试...")
                    time.sleep(wait_time)
                else:
                    err_msg = f"HTTP {status}" if status else str(e)
                    category_log["error"] = err_msg
                    print(f"   ❌ 失败: {err_msg}")
                    break
            except Exception as e:
                category_log["error"] = str(e)
                print(f"   ❌ 异常: {e}")
                break
        
        log_records.append(category_log)
    
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
    print("🚀 Insight Radar · 候选池生成器（带日志）")
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
