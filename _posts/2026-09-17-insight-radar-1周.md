---
title: "Insight Radar · 周刊 2026-09-17"
date: 2026-09-17 08:00:00 +0800
categories:
  - 论文周刊
tags:
  - AI
  - AI Scientist
  - AI4Science
  - Agentic Search
  - Agents
  - Auto-RecSys
  - AutoML
  - Automated Algorithm Discovery
  - Automation
  - Autonomous Research
  - CNN推理
  - Code as Action
  - Conversational AI
  - Dialogue System
  - Experience-Driven
  - Industry-Scale
  - LLM
  - Lifelong Learning
  - Long-Term Conversation
  - Memory Learning
  - Policy Refinement
  - Probabilistic Latent Memory
  - Recommender System
  - Research Agents
  - Resource Allocation
  - SDC
  - Scientific Workflow
  - Self-Evolving Agents
  - Trading
  - arXiv
  - benchmark
  - evaluation
  - long-horizon
  - multimodal
  - research agents
  - 基准测试
  - 多模态
  - 故障检测
  - 智能体
  - 校验和
  - 科学推理
  - 论文周刊
  - 证据推理
  - 软错误
  - 边缘计算
toc: true
toc_sticky: true
---

> 📅 **检索范围**：过去1周 (2026-09-10 ~ 2026-09-17)  
> 📊 **本期精选**：11 篇论文（人工筛选）  
> 📁 **来源文件**：`2026-09-17-1347-candidates.md`  
> <span style='background:#dbeafe;color:#1e40af;padding:2px 8px;border-radius:12px;font-size:0.8em;margin-right:6px;'>🔧 SDC</span><span style='background:#ede9fe;color:#5b21b6;padding:2px 8px;border-radius:12px;font-size:0.8em;'>🤖 Agents</span>
> 
> Insight Radar 定期追踪 AI 前沿动态。  
> 欢迎 [RSS 订阅](https://complexlychee.github.io/InsightRadar/feed.xml) 🔖


## 1. Carry-Through Checksum: A Lightweight Fault-Detection for CNN Inference at the Edge 🔥

**作者**：Kyrylo Nazarevych, Mohammad Hasan Ahmadilivani, Krister Kaldre, Davide Bertozzi, Jaan Raik | 单位: Tallinn University of Technology; University of Manchester  
**发表日期**：2026-09-15  
**arXiv**：[](https://arxiv.org/pdf/2609.16742v1)  
**领域**：软错误 (`cs.AR`)  
**来源**：2026-09-17-1347-candidates.md  
**标签**：`软错误` `CNN推理` `故障检测` `边缘计算` `校验和` <span style="background:#dbeafe;color:#1e40af;padding:1px 6px;border-radius:10px;font-size:0.75em;margin-left:4px;">SDC</span>

### 🔍 Opening & Challenge
边缘CNN推理面临软错误导致的可靠性挑战，需轻量级故障检测。

### ⚙️ Action
提出Carry-Through Checksum方法，利用校验和传播实现CNN推理过程中的轻量级故障检测。

### ✅ Resolution
实现了对CNN推理的高效故障检测，降低开销，保障边缘部署可靠性。

### ✨ 核心亮点

- 轻量级校验和设计

- 适用于CNN推理

- 边缘软错误检测


### 🎯 为什么关注
边缘设备可靠性关键，该方法以极低开销提升CNN推理容错能力，助力AI安全部署。

### 👥 适合读者
面向边缘计算、硬件可靠性、CNN加速器设计研究者。

---

## 2. PrimeScientist: Strategic Allocation of Research Effort in Autonomous Research 🔥

**作者**：Xinle Yu, Fan Bai, Kaiser Sun, Hengshuo Miao, Abhay Anand 等（共8人） | 单位: UCSanDiego  
**发表日期**：2026-09-15  
**arXiv**：[](https://arxiv.org/pdf/2609.17846v1)  
**领域**：Research Agents (`cs.CL`)  
**来源**：2026-09-17-1347-candidates.md  
**标签**：`Research Agents` `Autonomous Research` `Resource Allocation` `AI Scientist` <span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:10px;font-size:0.75em;margin-left:4px;">Agents</span>

### 🔍 Opening & Challenge
自主科研中如何战略分配研究精力，提升科研效率。

### ⚙️ Action
提出PrimeScientist框架，通过策略性分配研究资源与注意力，优化自主研究过程。

### ✅ Resolution
实现科研精力的高效配置，显著提升自主研究产出与质量。

### ✨ 核心亮点

- 战略分配研究精力

- 自主研究流程优化

- 资源调度新机制


### 🎯 为什么关注
该研究直击自主科研的核心瓶颈——精力分配，为下一代AI科研助手提供了关键策略框架，有望大幅加速科学发现进程。

### 👥 适合读者
AI研究者、科研自动化领域学者、关注智能体科研应用的工程师。

---

## 3. Interactive Memory Learning for Long-Term Conversations 🔥

**作者**：Cai Ke, Jiangyue Yan, Han Zhang, Xin Liu, Zike Yuan 等（共8人） | 单位: Harbin Institute of Technology, Shenzhen; Pengcheng Laboratory  
**发表日期**：2026-09-15  
**arXiv**：[](https://arxiv.org/pdf/2609.17088v1)  
**领域**：Self-Evolving Agents (`cs.AI`)  
**来源**：2026-09-17-1347-candidates.md  
**标签**：`Long-Term Conversation` `Memory Learning` `Self-Evolving Agents` `Dialogue System` <span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:10px;font-size:0.75em;margin-left:4px;">Agents</span>

### 🔍 Opening & Challenge
长期对话中如何持续记忆并利用历史信息，提升多轮交互一致性。

### ⚙️ Action
提出交互式记忆学习方法，通过对话反馈动态更新记忆表征，结合自进化机制优化长期依赖。

### ✅ Resolution
显著增强长期对话中的记忆准确性与响应连贯性，减少遗忘。

### ✨ 核心亮点

- 交互式记忆动态更新

- 自进化机制优化长期依赖

- 多轮一致性显著提升


### 🎯 为什么关注
长期对话是智能体实用化的关键瓶颈，该工作为记忆管理和自进化智能体提供了新范式，推动更自然、持久的交互系统发展。

### 👥 适合读者
对话系统、记忆增强模型、自进化智能体研究者及工程师。

---

## 4. ThinkFlow: Self-Evolving Probabilistic Latent Memory for Lifelong Conversational Agents 🔥

**作者**：Cai Ke, Xin Liu, Han Zhang, Jiangyue Yan, Zike Yuan 等（共9人） | 单位: PengchengLaboratory, China; Harbin Institute of Technology, Shenzhen, China  
**发表日期**：2026-09-15  
**arXiv**：[](https://arxiv.org/pdf/2609.17010v1)  
**领域**：Self-Evolving Agents (`cs.AI`)  
**来源**：2026-09-17-1347-candidates.md  
**标签**：`Self-Evolving Agents` `Probabilistic Latent Memory` `Lifelong Learning` `Conversational AI` <span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:10px;font-size:0.75em;margin-left:4px;">Agents</span>

### 🔍 Opening & Challenge
对话代理如何实现终身学习，克服灾难性遗忘并持续进化？

### ⚙️ Action
提出ThinkFlow，利用概率潜在记忆机制，使对话代理在交互中自进化地积累和更新知识。

### ✅ Resolution
实现了对话代理的终身学习能力，提升了长期对话的一致性与适应性。

### ✨ 核心亮点

- 概率潜在记忆建模

- 自进化知识更新机制

- 面向终身对话场景


### 🎯 为什么关注
该研究针对对话代理的终身学习难题，提出自进化概率记忆框架，为构建可持续交互的智能体提供了新思路，对下一代AI系统具有重要参考价值。

### 👥 适合读者
人工智能、对话系统、终身学习、记忆机制相关领域的研究者和工程师。

---

## 5. EvolveTrade: Experience-Driven Policy Refinement for Self-Evolving LLM Trading Agents 🔥

**作者**：Sehee Kim, Yumin Choi, Minki Kang, Sung Ju Hwang | 单位: KAIST; DeepAuto.ai  
**发表日期**：2026-09-15  
**arXiv**：[](https://arxiv.org/pdf/2609.17632v1)  
**领域**：Self-Evolving Agents (`cs.AI`)  
**来源**：2026-09-17-1347-candidates.md  
**标签**：`Self-Evolving Agents` `LLM` `Trading` `Policy Refinement` `Experience-Driven` <span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:10px;font-size:0.75em;margin-left:4px;">Agents</span>

### 🔍 Opening & Challenge
LLM交易代理如何从经验中持续自我进化，优化交易策略以应对动态市场。

### ⚙️ Action
提出EvolveTrade框架，通过经验驱动的策略细化机制，让LLM交易代理从历史交易中学习并自动调整决策策略。

### ✅ Resolution
实现交易策略的自主进化，提升LLM代理在复杂市场环境下的决策性能。

### ✨ 核心亮点

- 经验驱动策略细化

- 自我进化学习机制

- 面向LLM交易代理优化


### 🎯 为什么关注
该研究突破传统静态提示限制，使LLM代理具备持续学习能力，为智能交易系统提供新范式，推动自主智能体在金融领域落地。

### 👥 适合读者
关注LLM智能体、自主决策系统、智能交易及金融AI的研究者和工程师。

---

## 6. OpenAI4S: Code as Action, Science as Sessions 🔥

**作者**：Gongbo Zhang, Hao Li, Yu Wang, Mujie Lin, Liuzhenghao Lv 等（共18人） | 单位: PekingUniversityShenzhenGraduateSchool  
**发表日期**：2026-09-14  
**arXiv**：[](https://arxiv.org/pdf/2609.15096v1)  
**领域**：Research Agents (`cs.AI`)  
**来源**：2026-09-17-1347-candidates.md  
**标签**：`Research Agents` `AI4Science` `Code as Action` `Scientific Workflow` <span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:10px;font-size:0.75em;margin-left:4px;">Agents</span>

### 🔍 Opening & Challenge
研究科研自动化智能体领域，面临如何将科学发现过程形式化为可执行、可交互的智能体工作流。

### ⚙️ Action
提出OpenAI4S框架，以代码为行动原语、以会话为科学探索会话，构建研究智能体的执行与交互机制。

### ✅ Resolution
实现了科研任务从代码执行到会话管理的统一编排，提升研究智能体的自主性和可复现性。

### ✨ 核心亮点

- 代码即行动，统一执行接口

- 科学即会话，管理探索流程

- 智能体驱动科研自动化


### 🎯 为什么关注
该工作为科研智能体提供了一种新的范式，将代码执行与科学会话深度融合，有望加速科研发现过程，推动AI for Science的工程化落地。

### 👥 适合读者
AI for Science、研究智能体、自动化科研平台相关的研究者与工程师。

---

## 7. AlgoEvo: Self-Evolving Agentic Search for Automated Algorithm Discovery 🔥

**作者**：Junhao Qiu, Qinglong Hu, Xialiang Tong, Mingxuan Yuan, Liyong Lin 等（共6人） | 单位: Department of Computer Science, City University of Hong Kong; Huawei Noah's Ark Lab; Institute of Advanced Intelligence and Computing, A*STAR  
**发表日期**：2026-09-14  
**arXiv**：[](https://arxiv.org/pdf/2609.15820v1)  
**领域**：Self-Evolving Agents (`cs.AI`)  
**来源**：2026-09-17-1347-candidates.md  
**标签**：`Self-Evolving Agents` `Automated Algorithm Discovery` `Agentic Search` `AutoML` <span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:10px;font-size:0.75em;margin-left:4px;">Agents</span>

### 🔍 Opening & Challenge
算法发现依赖人工设计，自动化搜索效率低且缺乏自适应性。

### ⚙️ Action
提出AlgoEvo，一种自进化智能体搜索框架，通过智能体迭代生成、评估和优化算法。

### ✅ Resolution
实现了算法发现的自动化与持续进化，显著提升搜索效率和算法性能。

### ✨ 核心亮点

- 自进化智能体循环

- 自动化算法搜索

- 持续优化与适应


### 🎯 为什么关注
该研究将智能体与自进化机制结合，突破传统算法发现的瓶颈，为自动化科研提供了新范式，有望加速AI和计算领域的创新。

### 👥 适合读者
人工智能、自动化机器学习、智能体系统及算法设计领域的研究者和工程师。

---

## 8. Mr.LHDR: A Benchmark for Multimodal Real-World Long-Horizon Deep Research Agents 🔥

**作者**：Minghao Guo, Meng Cao, Sui Zhao, Siyu Ning, Xin Wang 等（共13人） | 单位: Mohamed bin Zayed University of Artificial Intelligence; University of Science and Technology of China; Zhejiang University  
**发表日期**：2026-09-10  
**arXiv**：[](https://arxiv.org/pdf/2609.11318v2)  
**领域**：Research Agents (`cs.AI`)  
**来源**：2026-09-17-1347-candidates.md  
**标签**：`benchmark` `multimodal` `long-horizon` `research agents` `evaluation` <span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:10px;font-size:0.75em;margin-left:4px;">Agents</span>

### 🔍 Opening & Challenge
研究智能体领域，面临多模态真实世界长时程深度研究任务缺乏统一基准的核心挑战。

### ⚙️ Action
构建Mr.LHDR基准，包含多模态真实世界长时程深度研究任务，用于系统评估研究智能体的综合能力。

### ✅ Resolution
提供了首个多模态真实世界长时程深度研究基准，填补了该方向评估空白。

### ✨ 核心亮点

- 首个多模态真实世界长时程基准

- 覆盖深度研究全流程任务

- 支持智能体综合能力评估


### 🎯 为什么关注
该基准为研究智能体提供了标准化评估平台，推动多模态理解、长时程规划与真实世界信息检索等关键能力的发展，对AI助手落地有重要价值。

### 👥 适合读者
研究智能体、多模态学习、信息检索、AI评估与基准构建等方向的研究者和工程师。

---

## 9. Sci-MMR: Benchmarking Multi-Step Evidence-Grounded Scientific Reasoning in Multimodal Agents 🔥

**作者**：Jiaqiang Li, Yajie Yang, Zhiheng Xi, Jiadong Chen, Enyu Zhou 等（共18人） | 单位: Fudan NLP Group  
**发表日期**：2026-09-10  
**arXiv**：[](https://arxiv.org/pdf/2609.11243v1)  
**领域**：Research Agents (`cs.AI`)  
**来源**：2026-09-17-1347-candidates.md  
**标签**：`多模态` `科学推理` `基准测试` `智能体` `证据推理` <span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:10px;font-size:0.75em;margin-left:4px;">Agents</span>

### 🔍 Opening & Challenge
多模态智能体在科学推理中缺乏多步证据基础的基准评估

### ⚙️ Action
构建Sci-MMR基准，设计多步证据基础推理任务，评估多模态智能体的科学推理能力

### ✅ Resolution
提供新基准，揭示当前多模态智能体在科学推理中的不足

### ✨ 核心亮点

- 首个多步证据科学推理基准

- 多模态输入与推理结合

- 系统评估多模态智能体


### 🎯 为什么关注
填补多模态智能体科学推理基准空白，推动证据基础推理研究，为未来科学AI评估提供标准

### 👥 适合读者
多模态AI、科学推理、智能体评估领域的研究者

---

## 10. Auto-RecSys: Harnessing Autonomous Research Agents for Industry-Scale Recommender System 🔥

**作者**：Ming Li, Dai Li, Xuying Ning, Bo Sun, Rui Li 等（共14人） | 单位: Meta; University of Illinois Urbana-Champaign  
**发表日期**：2026-09-10  
**arXiv**：[](https://arxiv.org/pdf/2609.10922v1)  
**领域**：Research Agents (`cs.CL`)  
**来源**：2026-09-17-1347-candidates.md  
**标签**：`Auto-RecSys` `Recommender System` `Research Agents` `Automation` `Industry-Scale` <span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:10px;font-size:0.75em;margin-left:4px;">Agents</span>

### 🔍 Opening & Challenge
工业级推荐系统面临规模大、复杂度高、人工调优成本高的问题。

### ⚙️ Action
利用自主研究智能体（Auto-RecSys）自动化推荐系统的设计、调优与评估流程。

### ✅ Resolution
提升推荐系统研发效率与性能，减少人工干预，适应工业规模需求。

### ✨ 核心亮点

- 自主研究智能体驱动

- 面向工业级推荐系统

- 自动化调优与评估流程


### 🎯 为什么关注
该研究将AI智能体引入推荐系统研发，有望大幅降低人工试错成本，加速模型迭代，为大规模工业应用提供自动化解决方案，是推荐系统与智能体结合的前沿探索。

### 👥 适合读者
推荐系统研究者、工业界推荐工程师、AI智能体与自动化机器学习方向从业者。

---

## 11. Agora: Git as Shared Memory for Collective AutoResearch 

**作者**：Yifan Zhang, Yunheng Zou, Shaokun Zhang, Jian Hu, Hao Zhang 等（共8人） | 单位: NVIDIA  
**发表日期**：2026-09-16  
**arXiv**：[](https://arxiv.org/pdf/2609.18094v1)  
**领域**：Autonomous Research (`cs.LG`)  
**来源**：2026-09-17-1347-candidates.md  
**标签**：`Autonomous Research` <span style="background:#ede9fe;color:#5b21b6;padding:1px 6px;border-radius:10px;font-size:0.75em;margin-left:4px;">Agents</span>

### 🔍 Opening & Challenge
请阅读原文了解详情

### ⚙️ Action
请阅读原文了解详情

### ✅ Resolution
请阅读原文了解详情

### ✨ 核心亮点

- 请阅读原文了解详情


### 🎯 为什么关注
该论文属于本期精选研究

### 👥 适合读者
Autonomous Research研究者

---


## 📮 订阅方式

| 方式 | 链接 |
|------|------|
| 🌐 博客主页 | https://complexlychee.github.io/InsightRadar |
| 📡 RSS 订阅 | https://complexlychee.github.io/InsightRadar/feed.xml |
| 🔧 SDC 专栏 | https://complexlychee.github.io/InsightRadar/columns/sdc/ |
| 🤖 Agents 专栏 | https://complexlychee.github.io/InsightRadar/columns/agents/ |
| 🐙 源码仓库 | https://github.com/ComplexLychee/InsightRadar |

---

*本报告由 GitHub Actions 自动生成，论文经人工筛选，解读由 AI 辅助完成。*
