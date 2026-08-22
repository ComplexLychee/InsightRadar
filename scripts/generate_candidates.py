import os
import re
import time
import io
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta

try:
    import pdfplumber
    PDFPLUMBER_OK = True
except ImportError:
    PDFPLUMBER_OK = False

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
    "research_agents": [
        {"query": 'ti:"research agent" OR abs:"research agent" OR ti:"AI scientist" OR abs:"AI scientist"', "name": "Research Agents"},
        {"query": 'ti:"self-research" OR abs:"self-research" OR ti:"self evolving" OR abs:"self evolving" OR ti:"self-evolving" OR abs:"self-evolving"', "name": "Self-Evolving Agents"},
        {"query": 'ti:"autonomous research" OR abs:"autonomous research" OR ti:"automated discovery" OR abs:"automated discovery"', "name": "Autonomous Research"},
        {"query": 'ti:"scientific discovery" OR abs:"scientific discovery" OR ti:"AI for science" OR abs:"AI for science"', "name": "AI for Science"},
        {"query": 'ti:"agent" AND (ti:"scientific" OR ti:"research" OR abs:"scientific" OR abs:"research")', "name": "Scientific Agents"},
        {"query": 'ti:"multi-agent" OR abs:"multi-agent" OR ti:"multiagent" OR abs:"multiagent" OR ti:"agentic" OR abs:"agentic"', "name": "Multi-Agent Systems"},
    ],
    "weekly_auto": [
        {"query": 'ti:"silent data corruption" OR abs:"silent data corruption"', "name": "SDC精确短语"},
        {"query": 'ti:"soft error" OR abs:"soft error" OR ti:SEU OR abs:SEU', "name": "软错误"},
        {"query": 'ti:"fault tolerance" OR abs:"fault tolerance" OR ti:"error resilience"', "name": "容错计算"},
        {"query": 'ti:"research agent" OR abs:"research agent" OR ti:"AI scientist" OR abs:"AI scientist"', "name": "Research Agents"},
        {"query": 'ti:"self-research" OR abs:"self-research" OR ti:"self evolving" OR abs:"self evolving" OR ti:"self-evolving" OR abs:"self-evolving"', "name": "Self-Evolving Agents"},
        {"query": 'ti:"autonomous research" OR abs:"autonomous research" OR ti:"automated discovery" OR abs:"automated discovery"', "name": "Autonomous Research"},
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

AGENTS_KEYWORDS = [
    "research agent", "ai scientist", "self-research", "self evolving",
    "self-evolving", "autonomous research", "automated discovery",
    "scientific discovery", "ai for science", "scientific agent",
    "multi-agent", "multiagent", "agentic"
]

ARXIV_DELAY = 5
MAX_RETRIES = 3
MAX_RESULTS_PER_QUERY = 100
PDF_DELAY = 2
NS = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}


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
    preset = os.getenv("KEYWORD_PRESET", "weekly_auto")
    custom = os.getenv("CUSTOM_QUERY", "").strip()
    print(f"   [DEBUG] KEYWORD_PRESET='{preset}'")
    print(f"   [DEBUG] CUSTOM_QUERY='{custom}'")
    if custom and custom in KEYWORD_PRESETS:
        print(f"   [WARN] 自定义框填的是预设名 '{custom}'，自动使用该预设")
        return KEYWORD_PRESETS[custom]
    if custom:
        query = f'ti:"{custom}" OR abs:"{custom}"'
        print(f"   [DEBUG] 使用自定义查询: {query}")
        return [{"query": query, "name": "自定义检索"}]
    if preset in KEYWORD_PRESETS:
        print(f"   [DEBUG] 使用预设: {preset}")
        return KEYWORD_PRESETS[preset]
    print(f"   [DEBUG] 回退到 weekly_auto")
    return KEYWORD_PRESETS["weekly_auto"]


def is_relevant_paper(title, summary, keywords):
    text = (title + " " + summary).lower()
    for kw in keywords:
        if kw.lower() in text:
            return True, kw
    return False, None


def call_opencode(prompt, api_key, max_tokens=400, temperature=0.3):
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": "deepseek-v4-flash", "messages": [{"role": "user", "content": prompt}],
               "temperature": temperature, "max_tokens": max_tokens}
    try:
        resp = requests.post("https://opencode.ai/zen/v1/chat/completions", headers=headers, json=payload, timeout=60)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"   ⚠️ API 失败: {e}")
        return None


def extract_affiliations_from_pdf(pdf_url, api_key):
    if not PDFPLUMBER_OK:
        return []
    try:
        resp = requests.get(pdf_url, timeout=15)
        if resp.status_code != 200:
            return []
        with pdfplumber.open(io.BytesIO(resp.content)) as pdf:
            if len(pdf.pages) == 0:
                return []
            text = pdf.pages[0].extract_text()
            if not text or len(text) < 50:
                return []
            text = text[:3000]
            prompt = f"""从以下学术论文 PDF 首页文本中，提取作者所属单位信息。
要求：
1. 最多列出 3 个单位
2. 优先提取通讯作者（通常用 * 或 † 标记）的单位
3. 如果无法判断通讯作者，提取前三个不同单位
4. 只输出单位名称，用 | 分隔，不要解释
5. 如果没有找到单位信息，输出 "未找到"

PDF 文本：
{text}

输出格式：单位1 | 单位2 | 单位3"""
            result = call_opencode(prompt, api_key, max_tokens=200, temperature=0.3)
            if not result or result == "未找到":
                return []
            affs = [a.strip() for a in result.split("|") if a.strip() and a.strip() != "未找到"]
            return affs[:3]
    except Exception as e:
        print(f"   ⚠️ PDF 解析失败: {e}")
        return []


def distill_summary(text, api_key):
    if not text or not text.strip():
        return "（无摘要）"
    text = text[:800].strip()
    prompt = f"""请对以下学术论文摘要进行结构化提炼，用中文输出：

### 研究问题
文章要解决/回答的核心问题是什么？

### 方法技术
文章用了什么方法、技术或框架来解决这个问题？

### 效果影响
最终取得了什么效果？对领域有什么影响或意义？

原文摘要：
{text}

请严格按上述三个部分输出，每部分用 ### 开头，内容简洁（每部分不超过80字）。"""
    result = call_opencode(prompt, api_key, max_tokens=500, temperature=0.3)
    if result:
        return result
    return text[:200] + "..."


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
            # 修复：arXiv 没提供单位时，只保留作者名，不显示"单位未提供"
            if aff and aff.strip():
                authors_list.append(f"{name} ({aff.strip()})")
            else:
                authors_list.append(name)

        authors_str = ", ".join(authors_list[:5])
        if len(authors_list) > 5:
            authors_str += f" 等（共{len(authors_list)}人）"

        pub_elem = entry.find('atom:published', NS)
        published = pub_elem.text if pub_elem is not None else ""
        cat_elem = entry.find('arxiv:primary_category', NS)
        category = cat_elem.get('term', 'unknown') if cat_elem is not None else "unknown"
        sum_elem = entry.find('atom:summary', NS)
        summary = sum_elem.text if sum_elem is not None else ""
        summary_clean = summary[:800].replace('\n', ' ')

        pdf_url = ""
        for link in entry.findall('atom:link', NS):
            if link.get('title') == 'pdf':
                pdf_url = link.get('href', '')
                break

        entries.append({
            "entry_id": entry_id, "title": title, "authors": authors_str,
            "published_raw": published, "category": category,
            "summary": summary, "summary_clean": summary_clean, "pdf_url": pdf_url,
        })
    return entries


def search_arxiv_api(query, max_results=100):
    url = "http://export.arxiv.org/api/query"
    params = {"search_query": query, "start": 0, "max_results": max_results,
              "sortBy": "submittedDate", "sortOrder": "descending"}
    for attempt in range(MAX_RETRIES):
        try:
            print(f"   [DEBUG] 请求: {url}?search_query={query.replace(' ', '+')}")
            resp = requests.get(url, params=params, timeout=60)
            print(f"   [DEBUG] HTTP状态: {resp.status_code}")
            if resp.status_code == 200:
                entries = parse_arxiv_xml(resp.content)
                print(f"   [DEBUG] 解析到 {len(entries)} 条结果")
                return entries
            elif resp.status_code in (429, 503) and attempt < MAX_RETRIES - 1:
                wait_time = ARXIV_DELAY * (2 ** attempt)
                print(f"   ⚠️ 限流，等待 {wait_time}s...")
                time.sleep(wait_time)
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
    preset = os.getenv("KEYWORD_PRESET", "weekly_auto")

    if preset == "sdc_reliability":
        use_filter, filter_keywords = True, SDC_KEYWORDS
        print(f"🔍 客户端过滤: SDC 严格模式")
    elif preset == "research_agents":
        use_filter, filter_keywords = True, AGENTS_KEYWORDS
        print(f"🔍 客户端过滤: Agents 严格模式")
    elif preset == "weekly_auto":
        use_filter, filter_keywords = True, SDC_KEYWORDS + AGENTS_KEYWORDS
        print(f"🔍 客户端过滤: SDC + Agents 合并模式")
    else:
        use_filter, filter_keywords = False, []
        print(f"🔍 客户端过滤: 关闭")

    print(f"📅 检索区间: {start.date()} ~ {end.date()} ({display})")
    print(f"🔧 关键词预设: {preset}")
    print("=" * 60)

    seen_ids = set()
    all_papers = []
    log_records = []

    for cfg in search_config:
        print(f"🔍 {cfg['name']}: {cfg['query']}")
        category_log = {"category_name": cfg["name"], "query": cfg["query"],
                        "raw_results": 0, "kept": [], "excluded": [], "error": None}
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
                category_log["excluded"].append({"entry_id": entry_id.split("/")[-1] if "/" in entry_id else entry_id,
                    "title": e["title"], "published": pub_date.strftime("%Y-%m-%d"), "reason": "超出时间范围"})
                continue
            if entry_id in seen_ids:
                category_log["excluded"].append({"entry_id": entry_id.split("/")[-1] if "/" in entry_id else entry_id,
                    "title": e["title"], "published": pub_date.strftime("%Y-%m-%d"), "reason": "重复"})
                continue
            if use_filter:
                relevant, matched_kw = is_relevant_paper(e["title"], e["summary"], filter_keywords)
                if not relevant:
                    category_log["excluded"].append({"entry_id": entry_id.split("/")[-1] if "/" in entry_id else entry_id,
                        "title": e["title"], "published": pub_date.strftime("%Y-%m-%d"), "reason": "客户端过滤：标题/摘要不包含目标关键词"})
                    continue
                print(f"   ✓ 命中: '{matched_kw}' -> {e['title'][:50]}...")
            seen_ids.add(entry_id)
            count_kept += 1
            category_log["kept"].append({"entry_id": entry_id.split("/")[-1] if "/" in entry_id else entry_id,
                "title": e["title"], "published": pub_date.strftime("%Y-%m-%d")})
            all_papers.append({"entry_id": entry_id, "title": e["title"], "authors": e["authors"],
                "published": pub_date.strftime("%Y-%m-%d"), "category": e["category"],
                "area": cfg["name"], "summary": e["summary_clean"], "pdf_url": e["pdf_url"]})
        print(f"   ✅ 原始返回 {len(entries)} 篇，保留 {count_kept} 篇")
        log_records.append(category_log)
        time.sleep(ARXIV_DELAY)

    # PDF 提取单位
    api_key = os.getenv("OPENCODE_API_KEY")
    if all_papers and api_key and PDFPLUMBER_OK:
        print(f"\n🏫 提取 {len(all_papers)} 篇论文的作者单位...")
        for i, p in enumerate(all_papers, 1):
            print(f"   📄 [{i}/{len(all_papers)}] {p['title'][:40]}...")
            affs = extract_affiliations_from_pdf(p["pdf_url"], api_key)
            if affs:
                p["affiliations"] = affs
                # 修复：如果 PDF 提取到单位，显示 "作者名 | 单位: xxx"
                # 如果 arXiv 已经提供了单位（authors 里有括号），优先用 PDF 的
                p["authors_display"] = f"{p['authors']} | 单位: {'; '.join(affs)}"
                print(f"      ✓ {'; '.join(affs)}")
            else:
                p["affiliations"] = []
                # 修复：如果没有提取到单位，只显示作者名（不显示"单位未提供"）
                p["authors_display"] = p["authors"]
                print(f"      - 无单位信息")
            time.sleep(PDF_DELAY)
        print("✅ 单位提取完成")
    else:
        for p in all_papers:
            p["affiliations"] = []
            p["authors_display"] = p["authors"]

    # 结构化提炼摘要
    if all_papers and api_key:
        print(f"\n🌐 提炼 {len(all_papers)} 篇论文摘要...")
        for i, p in enumerate(all_papers, 1):
            print(f"   📝 [{i}/{len(all_papers)}] {p['title'][:40]}...")
            p["summary_distilled"] = distill_summary(p["summary"], api_key)
        print("✅ 摘要提炼完成")
    else:
        for p in all_papers:
            p["summary_distilled"] = p["summary"][:200] + "..."

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
        f"1. 浏览下方论文列表（摘要已按模板提炼）",
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
            f"- **作者**: {p['authors_display']}",
            f"- **发表日期**: {p['published']}",
            f"- **所属领域**: {p['area']} (`{p['category']}`)",
            f"- **arXiv链接**: [{p['entry_id'].split('/')[-1]}]({p['pdf_url']})",
            f"- **结构化摘要**:",
        ])
        for line in p.get("summary_distilled", "").split("\n"):
            lines.append(f"  {line}")
        lines.extend([f"", f"---", f""])
    return "\n".join(lines)


def generate_log_md(log_records, start, end, display, total_kept):
    lines = [
        "# 🔍 检索排查日志",
        f"",
        f"> **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"> **检索区间**: {start.date()} ~ {end.date()} ({display})",
        f"> **关键词预设**: {os.getenv('KEYWORD_PRESET', 'weekly_auto')}",
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
    print("🚀 Insight Radar · 候选池生成器（PDF单位提取 + 结构化摘要版）")
    print("=" * 60)
    papers, start, end, display, log_records = search_papers()
    print(f"\n📚 总计候选: {len(papers)} 篇")
    os.makedirs("candidates", exist_ok=True)
    md_content = generate_candidates_md(papers, start, end, display)
    
    # 关键改动：文件名从 2026-08-22-candidates.md 改为 2026-08-22-1430-candidates.md
    candidate_file = f"candidates/{end.strftime('%Y-%m-%d-%H%M')}-candidates.md"
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
