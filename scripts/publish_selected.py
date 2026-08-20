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
        return
    
    # 从文件名提取日期（备用）
    basename = os.path.basename(candidate_file).replace("-candidates.md", "")
    
    # 从文件内容提取范围
    with open(candidate_file, "r", encoding="utf-8") as f:
        content = f.read()
    
    range_match = re.search(r'\*\*检索区间\*\*:\s*(\d{4}-\d{2}-\d{2})\s*~\s*(\d{4}-\d{2}-\d{2})', content)
    display_match = re.search(r'# 📋 候选论文池 · (.+)', content)
    
    # 修复：把字符串转为 datetime 对象
    if range_match:
        start_date = datetime.strptime(range_match.group(1), "%Y-%m-%d")
        end_date = datetime.strptime(range_match.group(2), "%Y-%m-%d")
    else:
        # 备用：从文件名解析
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
    
    md_content = generate_post(papers_data, range_display, start_date, end_date)
    
    os.makedirs("_posts", exist_ok=True)
    range_slug = range_display.replace("过去", "").replace(" ", "_")
    filename = f"_posts/{end_date.strftime('%Y-%m-%d')}-insight-radar-{range_slug}.md"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print(f"\n✅ 成功发布: {filename}")
    print(f"📄 共 {len(papers_data)} 篇论文")
