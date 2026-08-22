# 🔭 Insight Radar

> **学术论文洞察工作流，关注：SDC 与 Research Agent**

Insight Radar 是一个全自动化的 arXiv 论文追踪、筛选与解读系统。通过 GitHub Actions 定时检索、AI 辅助结构化解读、人工审核发布，帮助研究者和开发者高效追踪人工智能与系统可靠性领域的前沿动态。

---

## 🎯 项目目的

1. **追踪前沿**：每周自动检索 arXiv 上最新论文，覆盖 SDC（静默数据损坏）和 Research Agents（自主研究智能体）两大核心方向
2. **智能解读**：基于 OCAR 框架（Opening & Challenge / Action / Resolution）对论文进行结构化提炼，快速把握核心贡献
3. **人工审核**：候选池生成后由人工勾选，确保发布内容的高质量与相关性
4. **建立影响力**：通过定期发布学术洞察，构建个人/团队的技术品牌与专业影响力

---

## 🏗️ 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                      Insight Radar                          │
├─────────────────────────────────────────────────────────────┤
│  定时触发 / 手动触发                                          │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────┐     ┌─────────────────┐               │
│  │ Generate        │     │ arXiv API       │               │
│  │ Candidates      │────▶│ 论文检索        │               │
│  │ (GitHub Actions)│     │ + PDF 单位提取  │               │
│  └─────────────────┘     └─────────────────┘               │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────┐                                       │
│  │ candidates/     │  ◄── 人工勾选 (- [ ] → - [x])         │
│  │ 候选论文池      │                                       │
│  └─────────────────┘                                       │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────┐     ┌─────────────────┐               │
│  │ Publish         │────▶│ OpenCode        │               │
│  │ Selected        │     │ DeepSeek 解读   │               │
│  │ (GitHub Actions)│     │ OCAR 结构化输出 │               │
│  └─────────────────┘     └─────────────────┘               │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────────┐     ┌─────────────────┐               │
│  │ _posts/         │────▶│ GitHub Pages    │               │
│  │ 博客文章        │     │ 自动部署        │               │
│  └─────────────────┘     └─────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 工作流程

### Step 1: 生成候选池（Generate Candidates）

**触发方式**：每周二 15:00（北京时间）自动触发，或手动触发

**执行内容**：
- 根据预设关键词（`weekly_auto` / `sdc_reliability` / `research_agents`）检索 arXiv
- 下载论文 PDF 提取作者单位信息（优先通讯作者，最多3个）
- 基于 OCAR 框架对摘要进行结构化提炼
- 生成 `candidates/YYYY-MM-DD-HHMM-candidates.md`

**关键词预设**：

| 预设 | 覆盖方向 | 说明 |
|------|---------|------|
| `weekly_auto` | SDC + Agents | 定时任务默认，双方向同时检索 |
| `sdc_reliability` | SDC 方向 | 静默数据损坏、软错误、容错计算等 |
| `research_agents` | Agents 方向 | AI Scientist、自主科研、多智能体等 |

### Step 2: 人工审核与勾选

1. 打开 `candidates/` 目录下最新的 `.md` 文件
2. 浏览每篇论文的 OCAR 结构化摘要
3. 将想发布的论文前面的 `- [ ]` 改为 `- [x]`
4. Commit 保存

### Step 3: 发布到博客（Publish Selected）

**触发方式**：手动触发（支持单文件发布或多文件合并发布）

**执行内容**：
- 读取被勾选的论文
- 调用 DeepSeek 模型进行 OCAR 深度解读
- 自动判断论文所属专栏（SDC / Agents / 两者兼有）
- 生成 `_posts/YYYY-MM-DD-insight-radar-xxx.md`
- GitHub Pages 自动构建并部署

---

## 📋 OCAR 内容模板

每篇论文严格按照 **OCAR 框架**呈现：

### 🔍 Opening & Challenge
- 这篇文章研究的是什么领域？
- 面临的核心问题或挑战是什么？

### ⚙️ Action
- 文章采取了什么具体行动？
- 用了什么方法、技术或框架来应对挑战？

### ✅ Resolution
- 最终达成了什么效果？
- 解决了什么问题？产生了什么影响？

---

## 🗂️ 项目结构

```
InsightRadar/
├── .github/workflows/
│   ├── generate-candidates.yml    # 生成候选池工作流
│   └── publish-selected.yml       # 发布已勾选论文工作流
├── scripts/
│   ├── generate_candidates.py     # 检索 + PDF单位提取 + OCAR提炼
│   └── publish_selected.py        # 读取勾选 + LLM解读 + 生成博客文章
├── _posts/                        # 发布的博客文章（自动生成）
├── candidates/                    # 候选论文池（人工勾选）
├── logs/                          # 检索排查日志
├── _pages/
│   ├── about.md                   # 关于页面
│   └── columns/
│       ├── sdc.md                 # SDC 专栏聚合页
│       └── agents.md              # Agents 专栏聚合页
├── _config.yml                    # Jekyll 博客配置
└── index.md                       # 博客首页
```

---

## 🚀 快速开始

### 1. 配置 Secrets

仓库 → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| Secret Name | Value |
|-------------|-------|
| `OPENCODE_API_KEY` | 你的 OpenCode API Key |

### 2. 启用 GitHub Pages

仓库 → **Settings** → **Pages** → **Source**: Deploy from a branch → **Branch**: main / (root)

### 3. 运行工作流

- **Actions** → **Generate Candidates** → **Run workflow**
- 等待 2-3 分钟，查看 `candidates/` 目录
- 人工勾选论文后，运行 **Publish Selected**

---

## 📊 双专栏设计

### 🔧 SDC 专栏
关注：静默数据损坏、软错误、硬件容错、数据完整性、分布式系统可靠性

### 🤖 Self Research Agents 专栏
关注：AI Scientist、自主科研、自动化实验、多智能体协作、科学发现

每篇论文根据标题/摘要关键词**自动判断**所属专栏，支持同时归入两个专栏。

---

## 🛠️ 技术栈

| 组件 | 技术 |
|------|------|
| 论文检索 | arXiv API (HTTP 直连) |
| PDF 解析 | pdfplumber + LLM 提取 |
| AI 解读 | DeepSeek via OpenCode Zen |
| 内容框架 | OCAR (Opening / Action / Resolution) |
| 博客框架 | Jekyll + Minimal Mistakes |
| 部署托管 | GitHub Pages |
| 自动化 | GitHub Actions |

---

## 👤 关于作者

**ComplexLychee**

PhD in Mathematics and Statistics, Network Science; Currently working on silent data corruption (SDC) and research agents

---

## 📮 订阅方式

- 🌐 博客主页：https://complexlychee.github.io/InsightRadar
- 📡 RSS 订阅：https://complexlychee.github.io/InsightRadar/feed.xml
- 🐙 源码仓库：https://github.com/ComplexLychee/InsightRadar

---

*本项目由 GitHub Actions 全自动驱动，论文经人工筛选，解读由 AI 辅助完成。*
