# 📋 候选论文池 · 过去3个月

> **检索区间**: 2026-05-22 ~ 2026-08-20
> **候选总数**: 43 篇
> **生成时间**: 2026-08-20 07:13

## ✅ 使用说明
1. 浏览下方论文列表
2. 将想发布的论文前面的 `- [ ]` 改为 `- [x]`
3. 保存文件（Commit）
4. 手动运行 **Publish Selected** workflow

---

## 论文 1
- [ ] **发布**
- **标题**: Fault-Tolerant Quantum Computation with Adversarial Errors
- **作者**: Nikolas P. Breuckmann (单位未提供), Louis Golowich (单位未提供), Umesh Vazirani (单位未提供)
- **发表日期**: 2026-08-17
- **所属领域**: 容错计算 (`quant-ph`)
- **arXiv链接**: [2608.16857v1](https://arxiv.org/pdf/2608.16857v1)
- **摘要预览**: We prove a fault-tolerance theorem for quantum computation against adversarial noise. For every quantum circuit on $\bar{N}$ logical qudits of depth $\bar{T}$, we construct a fault-tolerant circuit on $N=\text{poly}(\bar{N})$ physical qudits of depth $\bar{T}\cdot\bar{N}^{o(1)}$, which is robust against an adversary who may arbitrarily choose and corrupt an almost-linear number $N^{1-o(1)}$ of physical qudits at each time step. This robustness significantly improves upon prior fault-tolerance theorems, which assumed corruptions were either local and stochastic, or else only act on a polynomial...

---

## 论文 2
- [ ] **发布**
- **标题**: Universal magic state concentration
- **作者**: Jacopo Rizzo (单位未提供), Lorenzo Leone (单位未提供)
- **发表日期**: 2026-08-13
- **所属领域**: 容错计算 (`quant-ph`)
- **arXiv链接**: [2608.13376v1](https://arxiv.org/pdf/2608.13376v1)
- **摘要预览**: Magic plays a dual role in quantum computation: it promotes stabilizer dynamics from efficient classical simulability to universality, but it presents a central challenge for fault tolerance, since non-stabilizer operations are harder to protect against noise. Magic state distillation addresses this issue; however, existing protocols typically assume prior structure in the input, such as proximity to the target or a specified noise model. Here we introduce universal magic state concentration: a fixed stabilizer protocol that converts a few copies of an unknown pure non-stabilizer qubit state i...

---

## 论文 3
- [ ] **发布**
- **标题**: Efficient Quantum Modular Reduction: Crandall reduction and its Fault-tolerant resource analysis
- **作者**: Changyeol Lee (单位未提供), Sungyeon Kook (单位未提供), Wooyeong Song (单位未提供), Kwangil Bae (单位未提供), Wonhyuk Lee (单位未提供) 等（共6人）
- **发表日期**: 2026-08-12
- **所属领域**: 容错计算 (`quant-ph`)
- **arXiv链接**: [2608.11563v1](https://arxiv.org/pdf/2608.11563v1)
- **摘要预览**: Modular arithmetic is central to quantum algorithms for cryptographic problems, including Shor's algorithm and Grover-based cryptanalysis, with modular reduction contributing substantially to circuit cost. Pseudo-Mersenne moduli $q=2^n-c$ allow classical Crandall reduction to replace division with folding and constant arithmetic, providing a structural opportunity for more efficient quantum modular reduction than Barrett reduction. We translate this advantage into a reversible quantum setting by deriving explicit folding and normalization conditions for $2n$-bit inputs. To the best of our know...

---

## 论文 4
- [ ] **发布**
- **标题**: On the Sensitivity to Errors in Homomorphic Computing: Single Transient Bit-flip Client-side Error Characterization
- **作者**: Matías Mazzanti (单位未提供), Vattana Chan (单位未提供), Karthik Swaminathan (单位未提供), Augusto Vega (单位未提供), Esteban Mocskos (单位未提供) 等（共6人）
- **发表日期**: 2026-08-11
- **所属领域**: SDC精确短语 (`cs.AR`)
- **arXiv链接**: [2608.11155v1](https://arxiv.org/pdf/2608.11155v1)
- **摘要预览**: Homomorphic Encryption (HE) enables computation on encrypted data without decryption and is a key primitive for privacy-preserving computation in sensitive domains such as healthcare, finance, and government. Its security relies on noise injection, which introduces intrinsic error sensitivity and raises concerns about the fault tolerance of HE systems, as hardware- and software-induced faults can evade traditional detection mechanisms and lead to silent data corruption.   In this work, we analyze the sensitivity of HE to bit-level faults, focusing on the CKKS (Cheon--Kim--Kim--Song) scheme wid...

---

## 论文 5
- [ ] **发布**
- **标题**: SCOUT: Symmetric Consensus Outlier Detection for Failure Localization in LLM Pre-Training
- **作者**: Zhuang Wang (单位未提供)
- **发表日期**: 2026-08-11
- **所属领域**: SDC精确短语 (`cs.DC`)
- **arXiv链接**: [2608.11034v1](https://arxiv.org/pdf/2608.11034v1)
- **摘要预览**: In LLM pre-training, synchronization propagates rank-local stalls, slowdowns, and numerical errors into job-wide symptoms, obscuring their origin. Existing diagnosis often relies on in-process monitors that cannot report after the trainer blocks or terminates, or on post-mortem logs that preserve only synchronized symptoms; offline health tests lose the workload and operating conditions that triggered the failure. We present SCOUT, a unified runtime failure-localization framework built on one design principle: identify outliers through strict-majority consensus among equivalent replicas. SCOUT...

---

## 论文 6
- [ ] **发布**
- **标题**: Neural implants and human safety: single-fault detection for DC-coupled recording front ends
- **作者**: Dimitris Antoniadis (单位未提供), Timothy Constandinou (单位未提供)
- **发表日期**: 2026-08-11
- **所属领域**: 容错计算 (`eess.SP`)
- **arXiv链接**: [2608.10361v1](https://arxiv.org/pdf/2608.10361v1)
- **摘要预览**: DC-coupled analogue front ends (AFEs) for neural implants provide a low-area solution. However, removing the coupling capacitor eliminates the intrinsic barrier that protects cortical tissue: a single-fault event, such as gate-oxide breakdown of a low-noise amplifier (LNA) input transistor, can open a direct DC path from the supply rail into the brain. On the stimulation side this hazard is well understood, and single-fault tolerance is enforced by a series DC-blocking capacitor; on the recording side, DC-coupled front ends discard the equivalent safeguard, yet their protection has gone almost...

---

## 论文 7
- [ ] **发布**
- **标题**: MicroEvo: Knowledge-Guided LLM Sampling for Efficient Microarchitecture Design Space Exploration
- **作者**: Jia Xiong (单位未提供), Runkai Li (单位未提供), Chenxu Niu (单位未提供), Guangyuan Gao (单位未提供), Changwen Xing (单位未提供) 等（共14人）
- **发表日期**: 2026-08-06
- **所属领域**: 软错误 (`cs.AI`)
- **arXiv链接**: [2608.06183v1](https://arxiv.org/pdf/2608.06183v1)
- **摘要预览**: Microarchitecture design space exploration suffers from expansive search spaces and expensive PPA evaluation, leaving only a small simulation budget for design decision-making. Existing methods perform blind search without considering microarchitectural dependencies and fail to learn from the iterative search effectively, leading to wasted evaluations and weak Pareto convergence. In this paper, we propose MicroEvo, a knowledge-guided framework that couples off-the-shelf LLMs with Monte Carlo Tree Search (MCTS) for multi-objective microarchitecture optimization. MicroEvo combines LLM-driven evo...

---

## 论文 8
- [ ] **发布**
- **标题**: Quantum error correction with global control
- **作者**: Roberto Menta (单位未提供), Lindsay Bassman Oftelie (单位未提供), Ashkan Abedi (单位未提供), Francesco Cioni (单位未提供), Marco Polini (单位未提供) 等（共8人）
- **发表日期**: 2026-08-06
- **所属领域**: 容错计算 (`quant-ph`)
- **arXiv链接**: [2608.05821v1](https://arxiv.org/pdf/2608.05821v1)
- **摘要预览**: Reaching fault tolerance means scaling qubit counts by orders of magnitude, a jump that conventional superconducting architectures cannot sustain without solving the so-called `wiring problem'. Global control sidesteps this bottleneck, but implementing quantum error correction (QEC) on previously proposed global architectures incurs extremely steep overhead costs, due to the need for separate correction procedures for the computational and auxiliary qubits that comprise the global device. We resolve this by introducing the first globally-controlled architecture with zero qubit overhead. Every ...

---

## 论文 9
- [ ] **发布**
- **标题**: Provably Efficient Self-Calibrating Quantum Fault Tolerance
- **作者**: Weiyuan Gong (单位未提供), Hong-Ye Hu (单位未提供)
- **发表日期**: 2026-08-06
- **所属领域**: 容错计算 (`quant-ph`)
- **arXiv链接**: [2608.05686v1](https://arxiv.org/pdf/2608.05686v1)
- **摘要预览**: Quantum error correction protects logical information only when every physical operation remains below the fault-tolerance threshold, a condition that must be maintained continuously rather than only at the initial calibration. In practice, however, analog control parameters inevitably drift because of environmental fluctuations. As future fault-tolerant quantum computations are expected to run for days or even months, interrupting computation for repeated recalibration becomes fundamentally impractical. A promising alternative is to integrate calibration directly into computation by repurposi...

---

## 论文 10
- [ ] **发布**
- **标题**: Understanding Fault Tolerance of Adversarially Robust Pruned Models
- **作者**: Manali Dangarikar (单位未提供), Cory Merkel (单位未提供)
- **发表日期**: 2026-08-04
- **所属领域**: 容错计算 (`cs.LG`)
- **arXiv链接**: [2608.04173v1](https://arxiv.org/pdf/2608.04173v1)
- **摘要预览**: Deep neural networks (DNNs) deployed on resource-constrained neuromorphic hardware face three concurrent challenges: the need for model compression through pruning, vulnerability to adversarial input perturbations, and susceptibility to hardware-induced weight faults such as stuck-at-zero errors. While each of these factors has been studied in isolation, their combined effects on model reliability have received little attention. This paper presents an empirical investigation of how pruning, adversarial training, and hardware fault injection interact to affect the robustness of convolutional ne...

---

## 论文 11
- [ ] **发布**
- **标题**: The Utility of Sparse Error Detection in Quantum Simulations
- **作者**: Henry Froland (单位未提供), Dorota M. Grabowska (单位未提供), Sebastian Grieninger (单位未提供), Jeremy Hartse (单位未提供), Anne L. Lashbrook (单位未提供) 等（共11人）
- **发表日期**: 2026-08-03
- **所属领域**: 容错计算 (`quant-ph`)
- **arXiv链接**: [2608.02944v1](https://arxiv.org/pdf/2608.02944v1)
- **摘要预览**: The recent success of error detecting codes points toward their potential application to fault-tolerant simulations of nature. In this work, we examine the utility of sparse error detection for simulating lattice gauge theories using quantum computers. In particular, we study the time evolution of the lattice Schwinger model embedded into the Iceberg code family, $[[N+2, N, 2]]$, as well as the Hypercube code family, $[[2^N, N, 2]]$. The lattice of electrons and positrons in the axial gauge is embedded into a single code block or into multiple code blocks, and this work finds that large codebl...

---

## 论文 12
- [ ] **发布**
- **标题**: The Pangaea Architecture: Fault-Tolerant Heterogeneous Topological Codes via a Quantum Bus
- **作者**: Sheir Yarkoni (单位未提供), Chen Scheim (单位未提供), Daniel Hakshuri (单位未提供), Nadav Katz (单位未提供)
- **发表日期**: 2026-08-03
- **所属领域**: 容错计算 (`quant-ph`)
- **arXiv链接**: [2608.01887v2](https://arxiv.org/pdf/2608.01887v2)
- **摘要预览**: We introduce Pangaea, a fault-tolerant quantum architecture that uses a quantum bus to mediate logical operations between remote patches of two-dimensional topological codes. The bus is an auxiliary gauge-code strip whose measurements reconstruct joint logical operators while preserving nearest-neighbor physical connectivity. Enabling native heterogeneous topological codes and multi-qubit Pauli operations, the quantum bus can be interpreted as a three-dimensional generalization of lattice surgery. We require only $O(dN_L)$ physical qubits to implement multi-qubit interactions for $N_L$ distanc...

---

## 论文 13
- [ ] **发布**
- **标题**: CheckOne: Lightweight Fault Detection and Mitigation for Vision Transformers
- **作者**: Mohammad Hasan Ahmadilivani (单位未提供), Sven-Markus Loorits (单位未提供), Jaan Raik (单位未提供)
- **发表日期**: 2026-08-03
- **所属领域**: 容错计算 (`cs.AR`)
- **arXiv链接**: [2608.04035v1](https://arxiv.org/pdf/2608.04035v1)
- **摘要预览**: The wide adoption of Vision Transformers (ViTs) in safety-critical applications raises reliability concerns related to hardware faults. Algorithm-Based Fault Tolerance (ABFT) methods have emerged as lightweight and symmetric protection mechanisms for DNNs. However, they are particularly challenging for ViTs due to their significant computational requirements. This work comprehensively evaluates the reliability of ViTs, emphasizing the need for symmetric protection in their layers. Furthermore, we present CheckOne, a novel, cost-effective method for fault detection and mitigation in ViTs that s...

---

## 论文 14
- [ ] **发布**
- **标题**: PATH-Bench: Path-Dependent Evaluation of Lifelong Agents
- **作者**: Xidong Yang (单位未提供), Xingyi Zhang (单位未提供), Wenhao Li (单位未提供), Wenyan Liu (单位未提供), Junjie Sheng (单位未提供) 等（共10人）
- **发表日期**: 2026-08-02
- **所属领域**: 软错误 (`cs.AI`)
- **arXiv链接**: [2608.01149v1](https://arxiv.org/pdf/2608.01149v1)
- **摘要预览**: Lifelong LLM agents increasingly adapt through external learning states that store past interactions as retrievable memories or reusable skills, yet existing benchmarks rarely account for how the path of accumulated experience shapes what agents transfer and retain. In this work, we establish PATH-Bench, a benchmark for path-dependent evaluation of lifelong agents. PATH-Bench estimates directed task relationships via multi-model in-context learning, constructs probe-centered sequences with controlled helpful and interfering histories, and repeatedly evaluates probe tasks to measure average per...

---

## 论文 15
- [ ] **发布**
- **标题**: Measurement-Based Loss Tolerance in Graph-GKP Codes through Syndrome-Resolved Pauli-Frame Decoding
- **作者**: Seid Koudia (单位未提供), Symeon Chatzinotas (单位未提供)
- **发表日期**: 2026-08-01
- **所属领域**: 容错计算 (`quant-ph`)
- **arXiv链接**: [2608.00830v1](https://arxiv.org/pdf/2608.00830v1)
- **摘要预览**: Graph codes offer multiple physical representatives of logical observables, while Gottesman-Kitaev-Preskill (GKP) codes retain analog information about bosonic displacement noise. We develop a causal framework that unifies these mechanisms for measurement-based loss tolerance under pure loss followed by quantum-limited amplification. In this framework, each local GKP recovery produces a refreshed logical block, a continuous syndrome record, and a confidence score for the inferred Pauli class. Low-confidence outcomes are deliberately converted into located erasures, so the availability pattern ...

---

## 论文 16
- [ ] **发布**
- **标题**: RAID: Towards Robust AI-Generated Image Detection with Bit-Reversed Images
- **作者**: Renxi Cheng (单位未提供), Jie Gui (单位未提供), Hongsong Wang (单位未提供)
- **发表日期**: 2026-07-31
- **所属领域**: 软错误 (`cs.CV`)
- **arXiv链接**: [2607.28974v1](https://arxiv.org/pdf/2607.28974v1)
- **摘要预览**: The rapid advancement of image generation models has made it increasingly difficult for people to distinguish AI-generated images from real ones. To prevent the potential risks associated with the misuse of fake images, AI-generated image detection has gained significant attention. Existing methods neglect the inherent differences between real and fake images, thus lacking robustness and generalization ability. In this work, we innovatively investigate AI-generated image detection using bit-planes, and introduce the bit-reversed image. We propose a simple yet effective pipeline consisting of c...

---

## 论文 17
- [ ] **发布**
- **标题**: Retrieval-Driven Training-Free AI-Generated Video Attribution
- **作者**: Renxi Cheng (单位未提供), Chaolei Han (单位未提供), Jie Gui (单位未提供), Hongsong Wang (单位未提供)
- **发表日期**: 2026-07-31
- **所属领域**: 软错误 (`cs.CV`)
- **arXiv链接**: [2607.28955v1](https://arxiv.org/pdf/2607.28955v1)
- **摘要预览**: AI-generated videos are becoming increasingly realistic and difficult to distinguish from authentic ones, which facilitates malicious misuse and poses growing threats to cybersecurity and social governance. Attributing AI-generated videos to their specific generative sources is therefore of critical importance for forensic investigation and legal regulation. However, most existing visual attribution methods focus on images and particularly rely on the image generation model, thereby lacking the ability to generalize to large-scale AI-generated video data. To address these limitations, we intro...

---

## 论文 18
- [ ] **发布**
- **标题**: Restrictions on non-Clifford fault tolerance and ruling out beyond-SQL quantum metrology
- **作者**: Constantin Cedillo Vayson de Pradenne (单位未提供), Ishaan Kannan (单位未提供), Harald Putterman (单位未提供), Jordan Cotler (单位未提供)
- **发表日期**: 2026-07-29
- **所属领域**: 容错计算 (`quant-ph`)
- **arXiv链接**: [2607.27342v1](https://arxiv.org/pdf/2607.27342v1)
- **摘要预览**: Quantum metrology promises a quadratic speedup over the standard quantum limit (SQL), but signal-aligned noise is expected to preclude this advantage in realistic settings. A potential route around known no-go results is to encode the sensors in a quantum code where the physical signal acts transversally as a logical gate. Understanding restrictions on transversal non-Clifford gates is therefore central to both quantum metrology and fault-tolerant quantum computation. Here, we prove such restrictions and apply them to transversal sensing. For any stabilizer code of distance $d\ge 3$ supporting...

---

## 论文 19
- [ ] **发布**
- **标题**: Improved Methods for Determining Quantum Error Correcting Code Performance and Fault Tolerance
- **作者**: Michael Mullan (单位未提供), Matthew Weippert (单位未提供), Winton Brown (单位未提供)
- **发表日期**: 2026-07-29
- **所属领域**: 容错计算 (`quant-ph`)
- **arXiv链接**: [2607.27153v1](https://arxiv.org/pdf/2607.27153v1)
- **摘要预览**: One of the central challenges in quantum error correction is determining the performance of a code in the low-error regimes needed to implement utility-scale computations. While performance at these error rates is not amenable to direct Monte Carlo simulation, it can be extrapolated from simulations at higher logical error rates, assuming the logical error rate scales predictably with increasing distance or decreasing physical error rate. However, the expected scaling depends sensitively on the minimum weight of uncorrectable error patterns. In many cases, the minimum weight is unknown since i...

---

## 论文 20
- [ ] **发布**
- **标题**: Belayer: Efficient Fault Tolerance for LLM Agentic RL Training
- **作者**: Jiecheng Zhou (单位未提供), Qinghao Hu (单位未提供), Peng Sun (单位未提供), Xingcheng Zhang (单位未提供), Weiming Zhang (单位未提供)
- **发表日期**: 2026-07-28
- **所属领域**: 容错计算 (`cs.DC`)
- **arXiv链接**: [2608.14635v2](https://arxiv.org/pdf/2608.14635v2)
- **摘要预览**: Large language model (LLM) agents are increasingly trained with reinforcement learning in long-horizon, sandboxed environments. Unlike conventional RL, agentic RL couples GPU-intensive rollout engines with stateful environment containers whose actions may produce visible side effects, such as file edits, command execution, and dependency installation. A single trajectory can span many rounds of gen- eration and environment interaction, so a component failure can discard completed work or expose the model to an environment state that is inconsistent with its context. However, existing systems l...

---

## 论文 21
- [ ] **发布**
- **标题**: Absent, Not Faint: Fisher-Information Limits and a Logarithmic Measurement-Design Cure for Passive Characterization of Coherent Qubit Noise
- **作者**: Yi Pan (单位未提供), Meng Hsiu Tsai (单位未提供), Weihang You (单位未提供), Hanqi Jiang (单位未提供), Junhao Chen (单位未提供) 等（共9人）
- **发表日期**: 2026-07-23
- **所属领域**: 硬件故障 (`quant-ph`)
- **arXiv链接**: [2607.21663v1](https://arxiv.org/pdf/2607.21663v1)
- **摘要预览**: Calibrating a quantum processor means estimating error parameters, and estimation theory usually assumes a parameter hard to estimate is faint: its signal is weak but present, so more repetitions or a richer model will recover it. This assumption fails for a leading hardware fault. A coherent over-rotation is a small systematic gate miscalibration. Measured through the cheapest data a device returns--one fixed-basis histogram--it is not faint but absent: to first order it leaves the distribution unchanged, indistinguishable from a compensating stochastic error, exactly as two numbers cannot be...

---

## 论文 22
- [ ] **发布**
- **标题**: An Efficient Fault-Tolerance Scheme for CKKS Computation on CPUs
- **作者**: Jianan Mu (单位未提供), Ge Yu (单位未提供), Tenghui Hua (单位未提供), Liang Kong (单位未提供), Jing Ye (单位未提供) 等（共9人）
- **发表日期**: 2026-07-21
- **所属领域**: SDC精确短语 (`cs.AR`)
- **arXiv链接**: [2607.18720v1](https://arxiv.org/pdf/2607.18720v1)
- **摘要预览**: Fully homomorphic encryption (FHE) enables computation on encrypted data, but its long ciphertext dataflow and high-dimensional modular arithmetic make it vulnerable to silent data corruption caused by transient hardware faults. Existing protection methods either target dedicated accelerators or impose substantial execution, modular-arithmetic, and memory-access overheads on CPUs.   This work presents an efficient fault-tolerance scheme for CPU-based CKKS computation. It checks the input-output consistency of polynomial operators while reducing protection overhead at three levels. First, modul...

---

## 论文 23
- [ ] **发布**
- **标题**: CoG-Guided Weight Correction for Fault-Tolerant Deep Neural Networks
- **作者**: Bahram Parchekani (单位未提供), Samira Nazari (单位未提供), Ali Azarpeyvand (单位未提供), Mohammad Hasan Ahmadilivani (单位未提供), Tara Ghasempouri (单位未提供) 等（共6人）
- **发表日期**: 2026-07-17
- **所属领域**: 硬件故障 (`cs.LG`)
- **arXiv链接**: [2607.15753v1](https://arxiv.org/pdf/2607.15753v1)
- **摘要预览**: Deep Neural Networks (DNNs) used in safety-critical applications are vulnerable to hardware and memory faults that corrupt network weights and degrade reliability. In this paper, we propose a Center of Gravity (CoG) guided weight correction method that restores faulty weights based on their spatial characteristics within each layer. The proposed approach detects and corrects weight faults using distance-aware correction rules, eliminating the need for retraining or architectural modification. The effectiveness of the proposed method in terms of the capability of tolerating hardware faults has ...

---

## 论文 24
- [ ] **发布**
- **标题**: Quality control and quality assurance evaluation of ALFE2, a large-dynamic-range front-end ASIC de-veloped for the ATLAS Liquid Argon Calorimeter high-luminosity LHC upgrade
- **作者**: E. Buschmann (单位未提供), G. Carini (单位未提供), G. Chatzianastasiou (单位未提供), H. Chen (单位未提供), Y. Chen (单位未提供) 等（共20人）
- **发表日期**: 2026-07-11
- **所属领域**: 软错误 (`physics.ins-det`)
- **arXiv链接**: [2607.10458v2](https://arxiv.org/pdf/2607.10458v2)
- **摘要预览**: ALFE2 is a front-end ASIC developed for the ATLAS Liquid Argon (LAr) Calorimeter upgrade during the High-Luminosity Large Hadron Collider (HL-LHC) phase. ALFE2 comprises four preamplifier/shaper channels, each providing two distinct gain outputs to cover a 16-bit dynamic range. A robotic system has been developed for the automatic quality control test of ALFE2, and over 10% of the 80,000 chips have been evaluated by September 2025. The evaluation has allowed us to establish grading criteria. Using these criteria, a yield of over 85% was achieved in the evaluation tests, and these criteria are ...

---

## 论文 25
- [ ] **发布**
- **标题**: Sensitivity to Subjective Expected Utility Maximization: A Methodological Study, with an Illustrative Application to LLM Decision-Making
- **作者**: Jeff Helzner (单位未提供)
- **发表日期**: 2026-07-08
- **所属领域**: 软错误 (`econ.EM`)
- **arXiv链接**: [2607.11920v1](https://arxiv.org/pdf/2607.11920v1)
- **摘要预览**: Evaluating decisions made under uncertainty is hard when labeled outcomes are scarce, costly, or confounded with luck. We treat subjective expected utility (SEU) maximization as a stated standard and define a graded measure -- SEU sensitivity -- of an agent's conformity to it. The vehicle is a softmax choice model with a sensitivity parameter $α$ on SEU-valued alternatives; the contribution is a sequence of identifiability results for $α$ and for belief and utility parameters $(β, δ)$, validated in Stan via prior predictive checks, parameter recovery, and simulation-based calibration (SBC), wi...

---

## 论文 26
- [ ] **发布**
- **标题**: Self-Heating and Radiation Hardness Studies of 3nm GAA-FET-Based SRAM with Different Substrate Isolation Techniques
- **作者**: Albert Lu (单位未提供), Junipero Verbeke (单位未提供), Phil Oldiges (单位未提供), Reza Arghavani (单位未提供), Hiu Yung Wong (单位未提供)
- **发表日期**: 2026-07-07
- **所属领域**: 软错误 (`cs.ET`)
- **arXiv链接**: [2607.05789v1](https://arxiv.org/pdf/2607.05789v1)
- **摘要预览**: In this work, 3D full-domain 3 nm gate-all-around field-effect transistor (GAA-FET) static random access memories (SRAMs) with various substrate isolation techniques are simulated using Technology Computer-Aided Design (TCAD). In addition to the traditional bottom dielectric isolation (BDI), which isolates the source/drain (S/D) from the substrate (dubbed SDBDI), and the punch-through stopper (PTS), a novel channel-BDI (C-BDI) is proposed, allowing S/D-to-substrate connection. The self-heating effect and radiation hardness due to various isolation techniques are studied. It is found that, firs...

---

## 论文 27
- [ ] **发布**
- **标题**: Self-Specializing Vision-Language Transmon Chip Calibration in a Physics-Grounded Environment
- **作者**: Animesh Tripathy (单位未提供), Aswanth Krishnan (单位未提供)
- **发表日期**: 2026-07-03
- **所属领域**: 硬件故障 (`quant-ph`)
- **arXiv链接**: [2607.03193v1](https://arxiv.org/pdf/2607.03193v1)
- **摘要预览**: Calibrating a superconducting transmon chip is a sequential decision problem under noise, drift, and a finite budget: an expert must choose experiments, read ambiguous plots, judge fit quality, and revise stale beliefs as the chip drifts. We study whether a vision-language agent can close this loop and specialize itself to one physical device without weight updates, via three co-designed artifacts. The first is a physics-grounded simulation environment for transmon chips: calibration observables derive from circuit-quantized parameters via scqubits, with realistic flux-line distortion, wall-ti...

---

## 论文 28
- [ ] **发布**
- **标题**: Embodied.cpp: A Portable Inference Runtime of Embodied AI Models on Heterogeneous Robots
- **作者**: Ling Xu (单位未提供), Borui Li (单位未提供), Hao Wu (单位未提供), Chuyu Han (单位未提供), Xiangyu Li (单位未提供) 等（共11人）
- **发表日期**: 2026-07-02
- **所属领域**: 软错误 (`cs.RO`)
- **arXiv链接**: [2607.02501v3](https://arxiv.org/pdf/2607.02501v3)
- **摘要预览**: Embodied AI models now span vision-language-action (VLA) models and world-action models (WAMs), but practical deployment remains fragmented across model-specific Python stacks, backend assumptions, and robot-side glue code, especially on heterogeneous edge devices. Existing inference runtimes are designed mainly for request-response serving and therefore do not satisfy the runtime contract of embodied deployment: multi-rate execution inside closed-loop control, latency-first batch-1 inference on heterogeneous hardware, and extensible embodied interfaces beyond fixed token I/O. We present Embod...

---

## 论文 29
- [ ] **发布**
- **标题**: ProWAFT: A ROMA-LPD Instance for Workload-Aware and Dynamic Fault Tolerance in FPGA-Based CNN Accelerators
- **作者**: Xinxin Chen (单位未提供), Haoran Qiao (单位未提供), Yiming Guo (单位未提供), Kecheng Luo (单位未提供), Siyuan Feng (单位未提供) 等（共6人）
- **发表日期**: 2026-07-02
- **所属领域**: 软错误 (`cs.CL`)
- **arXiv链接**: [2607.01602v1](https://arxiv.org/pdf/2607.01602v1)
- **摘要预览**: SRAM-based FPGAs provide an attractive platform for energy- and latency-constrained CNN inference at the network edge, yet transient faults can lead to silent errors that compromise reliability. Always-on redundancy (e.g., full TMR) improves correctness but incurs substantial performance and energy overhead, while reactive recovery may introduce unacceptable latency on the critical path. We propose \textbf{ProWAFT}, a proactive workload-aware fault-tolerance framework for FPGA-based CNN accelerators that uses partial reconfiguration to selectively apply TMR across reconfigurable partitions. Pr...

---

## 论文 30
- [ ] **发布**
- **标题**: Protecting Futures against Silent Data Corruption -- Efficient Task Replication for Dynamic Data Dependencies
- **作者**: Rüdiger Nather (单位未提供), Claudia Fohry (单位未提供), Mia Reitz (单位未提供)
- **发表日期**: 2026-06-29
- **所属领域**: SDC精确短语 (`cs.DC`)
- **arXiv链接**: [2606.30771v1](https://arxiv.org/pdf/2606.30771v1)
- **摘要预览**: As the size of computational problems grows, so does the likelihood of Silent Data Corruptions (SDCs). A common defense is replication, where the computation is repeated and correct results are determined by majority voting. Asynchronous Many-Task (AMT) runtimes are generally well suited for this approach, since the inputs and outputs of task replicas can be compared, and the tasks can be recomputed if necessary. Most existing SDC protection schemes assume static tasks and dependencies. Dynamic settings are more challenging, especially in clusters, since the tasks/data must be tracked for the ...

---

## 论文 31
- [ ] **发布**
- **标题**: StreamGuard: Low-Overhead Resilience for Real-time HPC Data Streams
- **作者**: Hai Duc Nguyen (单位未提供), Bogdan Nicolae (单位未提供), Tekin Bicer (单位未提供), Amal Gueroudji (单位未提供), Matthieu Dorier (单位未提供) 等（共7人）
- **发表日期**: 2026-06-29
- **所属领域**: 硬件故障 (`cs.DC`)
- **arXiv链接**: [2606.30848v1](https://arxiv.org/pdf/2606.30848v1)
- **摘要预览**: Real-time scientific workflows operate on continuous data streams and must produce timely, high-quality results despite executing on complex, failure-prone infrastructure. Hardware faults, network disruptions, and performance anomalies caused by resource contention or system heterogeneity can severely degrade performance and violate real-time constraints. We focus on strengthening the resilience of the producer-consumer streaming pattern, a fundamental building block of scientific streaming workflows. We present two complementary techniques: (i) a dynamic, asynchronous, non-blocking checkpoint...

---

## 论文 32
- [ ] **发布**
- **标题**: LibEvoBench: Probing Temporal Knowledge Stratification in Code Generation Models
- **作者**: Daniele Cipollone (单位未提供), Sergey Titov (单位未提供), Maliheh Izadi (单位未提供), Egor Bogomolov (单位未提供), Arie van Deursen (单位未提供)
- **发表日期**: 2026-06-24
- **所属领域**: 软错误 (`cs.SE`)
- **arXiv链接**: [2606.25402v1](https://arxiv.org/pdf/2606.25402v1)
- **摘要预览**: Large software projects often depend on older versions of libraries, even as APIs continue to evolve across releases. This creates a challenge for LLMs: they must maintain knowledge of multiple API versions, not merely the latest or most common one. However, current LLMs are trained on temporally mixed corpora and lack explicit mechanisms for such version-specific reasoning, leading to anachronistic errors - calling APIs as they exist in a different library version. To systematically evaluate this phenomenon, we introduce LibEvoBench, a multi-task benchmark spanning multiple versions of widely...

---

## 论文 33
- [ ] **发布**
- **标题**: Single-Event Upsets in 3D Gaussian Splatting Rendering: Bit-Level Criticality, Spatial Extent, and a Parallel Support Guard
- **作者**: Faruk Alpay (单位未提供), Baris Basaran (单位未提供)
- **发表日期**: 2026-06-19
- **所属领域**: SDC精确短语 (`cs.GR`)
- **arXiv链接**: [2606.21791v1](https://arxiv.org/pdf/2606.21791v1)
- **摘要预览**: Three-dimensional Gaussian splatting is a standard real-time scene representation increasingly deployed on hardware exposed to transient faults, such as spaceborne processors and robotic edge devices where silent data corruption occurs. A trained model is a large array of floating-point parameters in GPU memory, where a single-event upset corresponds to a single flipped bit. This paper measures these effects and constructs a defense. A GPU-resident parallel fault-injection engine applies over 3.8 million controlled single-bit upsets across four scenes, six fields, all bit positions, and three ...

---

## 论文 34
- [ ] **发布**
- **标题**: Nanoscale memristive devices: Threats and solutions
- **作者**: Amir M. Hajisadeghi (单位未提供), Javad Talafy (单位未提供), Hamid R. Zarandi (单位未提供)
- **发表日期**: 2026-06-17
- **所属领域**: 软错误 (`cs.ET`)
- **arXiv链接**: [2606.18978v1](https://arxiv.org/pdf/2606.18978v1)
- **摘要预览**: Due to their incentivizing features, memristors are a promising candidate for replacing CMOS-based memories, which are faced with various functional challenges in deep submicron process technologies. Memristors are nonvolatile, have low leakage, and are dense in comparison to CMOS-based memories like SRAM. In this regard, resistive RAM (ReRAM) and spin-transfer-torque RAM (STT-RAM) memristors are distinguished among other memristor-based memory technologies, due to their superiority in process maturity and metrics such as memory operation energy, memory latency, and area. Hence, this chapter f...

---

## 论文 35
- [ ] **发布**
- **标题**: Characterization of nested Walsh parity-check filters in a single-photon eight-mode register on a cloud photonic processor
- **作者**: Emma Tully (单位未提供), Jonathan Washburn (单位未提供), Megan Simons (单位未提供)
- **发表日期**: 2026-06-16
- **所属领域**: 软错误 (`quant-ph`)
- **arXiv链接**: [2606.18408v2](https://arxiv.org/pdf/2606.18408v2)
- **摘要预览**: We characterize two nested Walsh parity-check filters implemented on Quandela's Belenos cloud photonic processor in a single-photon eight-mode spatial register. The modes are indexed by the vertices of the cube $Q_3$. The filters realize the classical $[8,7,2]$ single-parity-check code, the zero-sum neutral subspace $\mathcal{N}$ and the $[8,4,4]$ extended Hamming code, the parity-checked subspace $\mathcal{S}\subset\mathcal{N}$ with one DC and three face-parity syndrome channels. These are first-quantized path/mode encodings of classical codes: the experiment verifies leakage suppression and ...

---

## 论文 36
- [ ] **发布**
- **标题**: Uncovering Vulnerability of Vision-Language-Action Models under Joint-Level Physical Faults
- **作者**: Minsoo Jo (单位未提供), Taeju Kwon (单位未提供), Junha Chun (单位未提供), Youngjoon Jeong (单位未提供), Taesup Kim (单位未提供)
- **发表日期**: 2026-06-09
- **所属领域**: 硬件故障 (`cs.RO`)
- **arXiv链接**: [2606.10501v1](https://arxiv.org/pdf/2606.10501v1)
- **摘要预览**: Deploying Vision-Language-Action (VLA) models in real robotic systems requires robustness not only to semantic and perceptual variations, but also to embodiment-side faults that change how actions are physically realized. Real robots can experience joint-level changes caused by actuator degradation, hardware faults, safety limits, collision damage, or wear-induced friction. These faults are critical because they alter the action-to-motion interface of a policy, disrupting the learned closed-loop relationship between commanded actions, realized motion, and subsequent observations. In this work,...

---

## 论文 37
- [ ] **发布**
- **标题**: Model Poisoning Against Federated Model Adaptation with Chain of Bit-Flips
- **作者**: Bastien Vuillod (单位未提供), Kevin Hector (单位未提供), Pierre-Alain Moellic (单位未提供), Jean-Max Dutertre (单位未提供), Olivier Potin (单位未提供)
- **发表日期**: 2026-06-08
- **所属领域**: 硬件故障 (`cs.CR`)
- **arXiv链接**: [2606.09548v1](https://arxiv.org/pdf/2606.09548v1)
- **摘要预览**: Federated Learning (FL) allows a set of clients to collectively train a global model without sharing local training data. Giving the responsibility of the training to decentralized actors may lead to poisoning attacks: clients controlled by malicious third party potentially poison the training dataset to install a backdoor in neural networks. In FL, these backdoor attacks rely solely on algorithmic approach, however, recent advances in hardware faults threats (e.g, Rowhammer) have widen the overall attack surface. In the context of federated model adaptation, we introduce a novel category of b...

---

## 论文 38
- [ ] **发布**
- **标题**: Not All Errors Are Equal: A Systematic Study of Error Propagation in Large Language Model Inference
- **作者**: Yafan Huang (单位未提供), Sheng Di (单位未提供), Guanpeng Li (单位未提供)
- **发表日期**: 2026-06-01
- **所属领域**: 软错误 (`cs.DC`)
- **arXiv链接**: [2606.02430v1](https://arxiv.org/pdf/2606.02430v1)
- **摘要预览**: Large language models (LLMs) are increasingly integrated into high-performance computing (HPC) workflows, accelerating scientific discovery through diverse perspectives such as code generation and domain-specific decision-making. Yet, how soft errors propagate and affect LLM inference remains largely unexplored. To bridge this gap, we present a comprehensive study on error propagation in LLM inference, enabled by our proposed LLMFI, a configurable and deterministic fault-injection framework. Using LLMFI, we systematically inject faults across three open-weighted LLMs and thirteen representativ...

---

## 论文 39
- [ ] **发布**
- **标题**: Don't Let a Few Network Failures Slow the Entire AllReduce
- **作者**: Peiqing Chen (单位未提供), Jiedong Jiang (单位未提供), Nengneng Yu (单位未提供), Yuefeng Wang (单位未提供), Sixian Xiong (单位未提供) 等（共7人）
- **发表日期**: 2026-06-01
- **所属领域**: 硬件故障 (`cs.DC`)
- **arXiv链接**: [2606.01680v1](https://arxiv.org/pdf/2606.01680v1)
- **摘要预览**: Network failures are among the most frequent hardware faults in large-scale GPU clusters and a leading cause of training-job interruptions. Modern collective communication libraries such as NCCL mitigate network failures by rerouting traffic through surviving NICs on the same server, trading reduced inter-node bandwidth for uninterrupted training. However, the degraded server remains on the critical path of the standard ring algorithm, slowing the entire collective. We present the first information-theoretic lower bound on AllReduce completion time under asymmetric network bandwidth and show t...

---

## 论文 40
- [ ] **发布**
- **标题**: SENTRY: Statistical Reliability Analysis of Vision Transformers Under Soft Errors
- **作者**: Pramit Kumar Bhaduri (单位未提供), Mahdi Taheri (单位未提供), Samira Nazari (单位未提供), Maksim Jenihhin (单位未提供), Christian Herglotz (单位未提供) 等（共6人）
- **发表日期**: 2026-05-30
- **所属领域**: 软错误 (`cs.CV`)
- **arXiv链接**: [2606.07620v1](https://arxiv.org/pdf/2606.07620v1)
- **摘要预览**: With the growth of Vision Transformers in safety-critical domains like autonomous systems and medical imaging, ensuring their reliability against soft errors is paramount. While ViTs offer state-of-the-art accuracy, their massive parameter counts render exhaustive fault injection campaigns infeasible. To bridge this gap, a statistical fault injection framework is presented, leveraging finite-population sampling theory to provide formal reliability guarantees. It is demonstrated that failure rates are bounded within a 1% margin at 99\% confidence using only a few thousand samples, regardless of...

---

## 论文 41
- [ ] **发布**
- **标题**: Silent Data Corruption Protection through Efficient Task Replication
- **作者**: Mia Reitz (单位未提供), Claudia Fohry (单位未提供)
- **发表日期**: 2026-05-28
- **所属领域**: SDC精确短语 (`cs.DC`)
- **arXiv链接**: [2605.29506v1](https://arxiv.org/pdf/2605.29506v1)
- **摘要预览**: The trend of increasing cluster sizes of supercomputers leads to a growing susceptibility to Silent Data Corruption (SDC) that can invalidate program results. A common strategy for SDC protection is replication, where the computation is repeated, and the correct result is determined as the one that is the same in at least two different computations. Applying replication to Asynchronous Many-Task (AMT) runtimes on clusters is challenging due to dynamic task spawning and work stealing, which complicate the identification of replicated tasks.   To address the challenge, this paper introduces a no...

---

## 论文 42
- [ ] **发布**
- **标题**: FT-Pilot: Automated Fault-Tolerant RTL Rewriting via Vulnerability-Guided LLMs
- **作者**: Weixing Liu (单位未提供), Zizhen Liu (单位未提供), Jing Ye (单位未提供), Naixing Wang (单位未提供), Cheng Liu (单位未提供) 等（共7人）
- **发表日期**: 2026-05-27
- **所属领域**: 软错误 (`cs.AR`)
- **arXiv链接**: [2605.28169v1](https://arxiv.org/pdf/2605.28169v1)
- **摘要预览**: As integrated circuit technologies continue to scale toward advanced process nodes, the continual reduction in node capacitance and supply voltage has made digital systems increasingly vulnerable to soft errors. Although traditional full-chip hardening methods can improve reliability, they often incur unacceptable area and power overhead, making selective hardening a more practical engineering solution. However, existing approaches typically rely on time-consuming fault-injection simulation to determine hardening locations through vulnerability analysis, and still depend heavily on manual stra...

---

## 论文 43
- [ ] **发布**
- **标题**: Robust Quantum-MUSIC for DoA Estimation Using Rydberg Atomic Receiver Arrays
- **作者**: Sourav Banerjee (单位未提供), Neel Kanth Kundu (单位未提供), Prajwalita Borah (单位未提供)
- **发表日期**: 2026-05-25
- **所属领域**: 硬件故障 (`eess.SP`)
- **arXiv链接**: [2605.25688v1](https://arxiv.org/pdf/2605.25688v1)
- **摘要预览**: Quantum wireless sensing using Rydberg atomic receivers enables high-sensitivity signal acquisition direction-of-arrival (DoA) estimation. However, it suffers from a fundamental limitation, where only the magnitude of the received signal is observable. The recently proposed Quantum-MUSIC algorithm addresses this problem by recovering phase information through alternating minimization and subsequently applying the MUSIC algorithm for DoA estimation. However, the existing approach relies on an $\ell_2$-norm phase retrieval step, making it highly sensitive to outlier measurements produced by hard...

---
