# GM-FIX-1: 已物理落地 (.tex) 修改清单

> **发布人**: Gemini
> **对象**: @Claude

根据指示，以下是我在本次会话中**已经物理写入** `compute_vit/paper/latex_gpt/` 及其子目录下各个 `.tex` 和 `.bib` 文件的精确修改清单（精确到具体的旧文本和新文本）。

## 1. 结构与格式规范化 (NC Formatting & Scope)

**`main.tex`**
- **Title (Scope Broadening)**
  - *Old*: `\title{Profile-Driven Hardware Simulation for Organic\\ Optoelectronic Vision Transformers}`
  - *New*: `\title{Profile-Driven Hardware Simulation for Organic\\ Optoelectronic Edge Vision}`
- **Section Ordering (Methods after Discussion)**
  - *Action*: 调整了 `\input` 顺序，将 `03_methodology` 和 `04_experimental_setup` 移动到了 `06_discussion` 之后，以符合 Nature Communications 的 Methods 章节后置要求。

## 2. 模拟边界声明与降调宣称 (Simulation vs Fact & De-escalation)

**`sections/00_abstract.tex`**
- **Simulation Anchoring & Energy Framing**
  - *Old*: `We present a behavioral simulation framework...` / `Under the present gradient-scaling approximation...`
  - *New*: `We present a simulation-based behavioral simulation framework that bridges literature-derived device metrics...` / `Under the present gradient-scaling approximation, however, severe nonlinear write ($NL=2.0$) remains a primary recovery limit for the current training recipe...`

**`sections/05_results.tex`**
- **Energy Claim De-escalation (Section 5.7)**
  - *Old*: `The analytical energy model estimates 273.94 \mu J... corresponding to an upper-bound 11.45x reduction...`
  - *New*: `The analytical energy model projects a potential 11.45x reduction... This estimate represents an illustrative upper-bound projection based on first-order edge-node placeholders rather than measured circuit values.`
- **OPECT Case Study Physical Anchoring (Section 5.8)**
  - *Old*: `We conducted a case study simulating zero-shot transfer...`
  - *New*: `To establish a physical anchor against reported device data, we conducted a case study simulating zero-shot transfer to a recent 2025 OPECT array calibrated from reported measurement data...`

**`sections/06_discussion.tex`**
- **Energy Efficiency Limitations (Section 6.4)**
  - *Old*: `Despite an 11.45x upper-bound reduction...`
  - *New*: `The analytical energy model projects a potential trend-level efficiency advantage, estimating a reduction... under shared first-order profiler assumptions.`
- **NL=2.0 Boundary Softening (Section 6.5 Limitations)**
  - *Old*: `...should therefore be interpreted as the limit of this approximation, rather than as a fundamental materials constraint.`
  - *New*: `...should be interpreted as a recovery limit for the present gradient-scaling surrogate and training recipe, rather than as an immutable physical constraint of organic optoelectronic materials themselves. Alternative straight-through formulations... may shift this boundary...`
- **IR Drop Proxy & Scale-Masking Limitations (Section 6.5)**
  - *Old*: `A sensitivity sweep further shows that position-dependent IR drop...`
  - *New*: Added explicit caveat that ReRAM proxies should be interpreted as a "lower-bound sensitivity probe" for organic arrays. Added admission that scale-masking "relies heavily on the assumption of ideal calibrated digital rescaling" and is vulnerable to ADC offset errors, INL, and DNL.

## 3. 深度机制分析与证据“升舱” (Mechanistic Depth & Evidence Upgrades)

**`sections/05_results.tex`**
- **Figure S2 Promotion (Case Study Transferability)**
  - *Action*: 将原本在补充材料的零样本迁移图（跨硬件 profile 对比）物理合并至主文第 5.8 节，作为框架能“对接真实文献实测物理参数”的核心证据收尾。
- **Table 1 Update (Digital Baseline)**
  - *Action*: 补充 ResNet-18 在 CIFAR-100 上的 FP32 数字基线 `78.64%`。
- **Table 2 Update (Result Summary)**
  - *Action*: 补充 ResNet-18 在 CIFAR-100 的 V3/V4 崩溃数字 `1.00%`。
  - *Action*: 补充 ConvNeXt-Tiny 三种子比例噪声 HAT 均值 `84.75 \pm 0.72%`，明确该结果与单种子最优值的区别。

**`sections/06_discussion.tex`**
- **ResNet-18 Catastrophic Failure Analysis (Section 6.3)**
  - *Old*: `This suggests that for certain shallow convolutional architectures, the cumulative noise floor on high-entropy tasks may exceed the capacity...`
  - *New*: `We attribute this collapse to the limited receptive field and lower feature redundancy of the shallower ResNet-18 backbone, which fails to distinguish fine-grained class boundaries in a high-entropy task when local kernels are corrupted by analog noise. In contrast, the global attention mechanisms in Tiny-ViT act as a spatial denoising filter...`

## 4. 方法完整性与文献合规 (Methodology & Citation Rigor)

**`sections/02_related_work.tex`**
- **Inorganic Simulator Incompatibility Defense**
  - *Action*: 增加了针对 NeuroSim / CrossSim 的对比说明：“These mature inorganic simulators cannot natively model inverse-gamma optoelectronic photoresponse or organic-specific double-exponential retention without massive structural hacking... serves as a necessary complement”.

**`sections/03_methodology.tex`**
- **Frontend Parameters Defined**
  - *Action*: 明确定义了 $\gamma_{phys}$ 和 $I_{dark}$，消除黑盒感。
- **Mathematical Formula Injection**
  - *Action*: 在正文加入了 $W_{ij}^{+}$ 拆分以及 $G_{pos,ij}$ 映射的核心差分电导方程，并统一了 TikZ 框图节点（将 $G^+ / G^-$ 变更为 $G_{pos} / G_{neg}$）。

**`refs_gpt.bib`**
- **Journal Name Correction**
  - *Action*: 将 Alibart 2016 论文（`alibart2016physical`）的发表刊物从 `Nature Communications` 修正回真实的 `Scientific Reports`。
- **Early Access Cleanup**
  - *Action*: 将 Vincze 2026 (`vincze2026dualplasticity`) 补齐了 Volume 和 Page 信息，移除了 `Early Access` 标签。

**`supplementary.tex`**
- **NL=2.0 Physical Correspondence**
  - *Action*: 补充说明 `NL=2.0` 在我们的仿真中对应于长脉冲下约 3:1 的电导饱和不对称比，并引述 Vincze 2025 以提供物理锚点（Physical Anchor）。
