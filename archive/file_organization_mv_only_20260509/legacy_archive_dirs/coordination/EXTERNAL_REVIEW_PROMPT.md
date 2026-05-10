# External Model Review Request — Nature Communications Manuscript

## English Version

---

### Context

I am preparing a submission to **Nature Communications** on a simulation framework for organic optoelectronic compute-in-memory (CIM) inference. The manuscript is methodologically complete but lacks measured device validation. I need your critical assessment as an external reviewer with fresh eyes.

### Manuscript Summary

**Title**: Hardware-Aware Simulation of Organic Optoelectronic Compute-in-Memory Inference for Edge Vision

**Core Claims**:
1. **Profile-driven simulation framework**: JSON-based device profile substitution enabling literature-to-deployment evaluation
2. **Ensemble HAT discovery**: Training-time D2D resampling raises fresh-instance accuracy from 10% (chance level) to 86.37±1.54%
3. **Hierarchy of limits**: Quantization is not the bottleneck; converter precision (6-bit cliff), fresh-instance robustness, and nonlinear write dynamics dominate
4. **Physical stress tests**: NL=2.0 nonlinear write is a hard boundary (27.72±0.82%) for gradient-scaling approximation

**Current Status**:
- 106/109 reviewer issues addressed (97.2% coverage)
- All simulation experiments complete (V1-V8, C1-C4, EXP-A/B)
- Manuscript: 16 pages main + 13 pages supplementary
- **No measured device data** — relies on literature proxies (Vincze 2025, Zhang 2025)

### Strategic Decision Needed

Internal multi-model consensus (Kimi, Gemini, Claude, Codex) recommends:
- **Position as pure simulation methodology paper** (AIHWKIT model)
- Submit **without** waiting for measured device validation
- Frame future physical validation as "natural extension, not prerequisite"

**Risk**: Reviewers may question "where is the hardware validation?"

### Your Task

Please review the following aspects and provide brutally honest feedback:

#### 1. Methodological Rigor (Score 1-5)
- Is the simulation framework sufficiently validated against existing tools (AIHWKIT sanity check: 90.08±0.21% vs digital 95.46%)?
- Are the physical simplifications (uniform retention, gradient-scaling NL, no temperature) methodologically acceptable with explicit disclosure?
- Is the "profile-driven" interface a genuine contribution or just a JSON wrapper?

#### 2. Scientific Contribution (Score 1-5)
- Is Ensemble HAT (10%→86% recovery) a novel finding or just data augmentation?
- Does the "6-bit ADC cliff" provide actionable insight for hardware designers?
- Are the conclusions (quantization not dominant, D2D matters most) supported by evidence?

#### 3. Nature Communications Fit (Score 1-5)
- Is this appropriate for NC's interdisciplinary scope (materials + ML systems)?
- Does the simulation-only nature disqualify it, or is the methodology contribution sufficient?
- Would you recommend "Major Revision" requiring hardware validation, or "Minor Revision" accepting current scope?

#### 4. Critical Weaknesses
- What are the top 3 weaknesses that reviewers will attack?
- Which claims are overreached and need softening?
- What additional controls or comparisons are missing?

#### 5. Specific Suggestions
- Should we explicitly state "simulation-only" in the abstract, or is current disclosure sufficient?
- Is the NL=2.0 "hard boundary" framing too strong? Should it be "approximation limit"?
- Should we seek collaborative validation (contact Vincze/Zhang groups) before submission?

### Output Format

```markdown
## Overall Recommendation
[Reject / Major Revision / Minor Revision / Accept as is]

## Scores
- Methodological Rigor: X/5
- Scientific Contribution: X/5
- NC Fit: X/5

## Critical Weaknesses (Top 3)
1. ...
2. ...
3. ...

## Strengths
1. ...

## Specific Recommendations
1. ...

## Final Verdict
Should we:
- (A) Submit now as pure simulation
- (B) Seek collaborative hardware validation first
- (C) Downscope to more specialized venue (e.g., Advanced Intelligent Systems)
```

### Key Documents (if you have access)

- `main.pdf` — Main manuscript (16 pages)
- `supplementary_main.pdf` — Supplementary info (13 pages)
- `MEASURED_DATA_REQUIREMENTS.md` — 6-parameter minimal dataset (simplified per Gemini audit)
- `param_sensitivity_prelim.json` — Parameter impact ranking

---

## 中文版本

---

### 背景

我正在准备向 **Nature Communications** 投稿一篇关于有机光电存算一体（CIM）推理仿真框架的论文。论文在方法学上已完成，但缺少真实器件验证。我需要你以"外部审稿人"的视角提供批判性评估。

### 论文概要

**标题**: Hardware-Aware Simulation of Organic Optoelectronic Compute-in-Memory Inference for Edge Vision

**核心主张**:
1. **Profile-driven仿真框架**: 基于JSON的设备配置文件替换接口，实现文献数据到部署评估的桥接
2. **Ensemble HAT发现**: 训练时D2D重采样将新实例准确率从10%（随机水平）提升至86.37±1.54%
3. **瓶颈层级**: 量化不是瓶颈；转换器精度（6-bit悬崖）、新实例鲁棒性、非线性写入动态才是主导因素
4. **物理压力测试**: NL=2.0非线性写入是梯度缩放近似的硬边界（27.72±0.82%）

**当前状态**:
- 106/109审稿人问题已解决（97.2%覆盖率）
- 所有仿真实验完成（V1-V8, C1-C4, EXP-A/B）
- 正文16页 + 补充材料13页
- **无实测器件数据** — 依赖文献代理值（Vincze 2025, Zhang 2025）

### 需要做出的战略决策

内部多模型共识（Kimi, Gemini, Claude, Codex）建议：
- **定位为纯仿真方法学论文**（AIHWKIT模式）
- **不等**实测器件验证直接投稿
- 将未来物理验证表述为"自然延伸，而非先决条件"

**风险**: 审稿人可能会质疑"硬件验证在哪里？"

### 你的任务

请审阅以下方面并提供坦率反馈：

#### 1. 方法学严谨性（1-5分）
- 仿真框架是否已充分验证（AIHWKIT对照：90.08±0.21% vs 数字95.46%）？
- 物理简化（均匀保持、梯度缩放NL、无温度模型）在明确披露的前提下是否可接受？
- "Profile-driven"接口是真正的贡献还是只是JSON包装器？

#### 2. 科学贡献（1-5分）
- Ensemble HAT（10%→86%恢复）是新发现还是只是数据增强？
- "6-bit ADC悬崖"是否为硬件设计者提供了可操作的洞见？
- 结论（量化不主导、D2D最重要）是否有证据支撑？

#### 3. Nature Communications适合度（1-5分）
- 这是否适合NC的跨学科范围（材料+机器学习系统）？
- 纯仿真性质是否使其不合格，还是方法学贡献已足够？
- 你会推荐"重大修订"（要求硬件验证）还是"小修"（接受当前范围）？

#### 4. 关键弱点
- 审稿人会攻击的前3大弱点是什么？
- 哪些主张过度延伸需要软化？
- 缺少哪些额外的对照或比较？

#### 5. 具体建议
- 我们应该在摘要中明确声明"纯仿真"，还是当前披露已足够？
- NL=2.0"硬边界"的表述是否太强？应该改为"近似极限"吗？
- 我们应该在投稿前寻求合作验证（联系Vincze/Zhang团队）吗？

### 输出格式

```markdown
## 总体建议
[拒稿 / 重大修订 / 小修 / 直接接受]

## 评分
- 方法学严谨性: X/5
- 科学贡献: X/5
- NC适合度: X/5

## 关键弱点（前3）
1. ...
2. ...
3. ...

## 优势
1. ...

## 具体建议
1. ...

## 最终裁决
我们应该：
- (A) 现在作为纯仿真论文投稿
- (B) 先寻求合作硬件验证
- (C) 降级到更专业的期刊（如Advanced Intelligent Systems）
```

### 关键文档（如你可访问）

- `main.pdf` — 主论文（16页）
- `supplementary_main.pdf` — 补充材料（13页）
- `MEASURED_DATA_REQUIREMENTS.md` — 6参数最小数据集（经Gemini审计简化）
- `param_sensitivity_prelim.json` — 参数影响排序

---

## Quick Reference Card

| Aspect | English | 中文 |
|:-------|:--------|:-----|
| Core dilemma | Simulation-only vs hardware validation | 纯仿真 vs 硬件验证 |
| Multi-model consensus | Submit as pure simulation (A+B strategy) | 作为纯仿真投稿（A+B策略）|
| Key risk | Reviewer challenge on "where is hardware?" | 审稿人质疑"硬件在哪里？"|
| Your role | External reviewer with fresh eyes | 外部审稿人，全新视角 |
| Deliverable | Honest assessment + strategic recommendation | 诚实评估 + 战略建议 |

---

*Use this prompt with any external AI model (ChatGPT, Claude, GPT-4, etc.) for independent review.*
