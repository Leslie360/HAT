# 外部审稿意见完整汇编 — v20260420
**Date:** 2026-04-20
**Source:** 10 independent review perspectives
**Scope:** main.pdf + supplementary_main.pdf

---

# 【评审来源 1】版本 Δ 对比：v20260418 → v20260420

## 已解决的关键问题

### ✅ R1：相关 D2D 应力测试（最高风险，之前 7/10 大改可能性）
新版补充材料包含 Supplementary Note SX.Z 和 Fig. S15，完整 10×5 新鲜实例扫描，可分离 AR1 空间相关 D2D 场。
结果：i.i.d. 基线 ρ=0: 86.33±1.61%; ρ=0.3: 84.57±2.39%(−1.76pp); ρ=0.5: 82.12±3.95%(−4.20pp); 最差实例 73.7%。
评价：完全消除 R1 核心攻击面。

### ✅ R3：标准 HAT 崩溃是单类预测器还是随机输出
新版主文 §3.4 明确：10.00% 是 collapsed single-class predictor，no-AMP 验证 10.00±0.00%。
评价：可直接指向 §3.4 和 JSON 文件名，可追溯性强。

### ✅ MLP 线性化的 Fresh-Instance Transfer 限制
Table S16：MLP-linearized 仅 32.12±7.72% fresh-instance，vs Ensemble HAT 86.37±1.54%。
评价：解决"偷渡第五贡献"风险。

## 主文 Abstract 变化
"constrain edge-vision deployment" → "constrain **simulated** edge-vision deployment"
评价：一字之差，显式 scope 在模拟域内。

## 图 1 Error Bar 问题
新增 "Hatched bars — deterministic or single-run estimates"
评价：解决视觉混淆。

## §4.6 Outlook ImageNet 范围
新增明确 scope-out 声明。
评价：解决 ImageNet 范围质疑。

## 综合评估
- R1（Gaussian D2D）→ 降至 3/10
- R2（无硬件验证）→ 仍 6/10（结构性限制）
- R3（10% 崩溃）→ 降至 1/10
最大剩余风险：R2，靠 cover letter 和 §4.6 管理。

---

# 【评审来源 2】"现在这版"总体判断

## 结论
**可以投 Nature Communications，真正"有竞争力地去投"，不是勉强冲。**
大概率能合理送外审；若进审，最可能轨道仍是 Major Revision。

## 为什么上了一个台阶
1. 10% baseline 被"钉死"（collapsed single-class predictor + no-AMP）
2. Figure 诚实度更高（hatched bars）
3. "还没建模"的问题推进到"做了受控压力测试"（AR(1) D2D、ADC calibration hook）
4. severe NL 定位为 diagnostic 而非 mitigation（32.12% fresh-instance 披露）
5. 更符合"方法学 advance"而非"又一个 simulator"

## 为什么不改成"稳收"
1. 外部锚定有了但还不算厚（CrossSim 1k subset、single-run clean）
2. 能耗仍是全稿最脆的一块（无社区广泛接受的外部对照框架）
3. 物理统计假设仍是主要攻击点（无 measured closure、无重尾、无温度）

**最终评级：Major Revision**（不是因为不够 NC，而是 external anchoring 不够厚 + 能耗与物理闭环未完成）

---

# 【评审来源 3】"结论"块（Accept with minor revision + 5星）

## 核心整体结论
更新后的 manuscript **系统性解决了上一轮所有高风险致命问题**，方法论严谨性、可复现性、透明度、稳健性均达 NC 标准。
当前版本不存在动摇核心贡献的结构性缺陷，仅剩余少量低工作量细节优化。

## 已闭环的高风险问题
1. 空间相关 D2D（AR(1) ρ=0.3/0.5，无灾难性崩溃）
2. 标准 HAT 基线（fixed-mask 领域主流实践 + no-AMP FP32 验证）
3. NL=2.0 消融（MLP-only 32.12% fresh-instance 明确披露）

## 提交前必改细节
1. 主文 §3.4 强化 no-AMP 验证（正文明确说明，非括号引用）
2. 主文 §3.7 强化 Ensemble HAT 统计优势（32% lower std vs per-batch）
3. 主文 Limitations 直接给出 correlated D2D 关键数据（非仅引用补充材料）
4. Table S16 新增 fresh-instance 精度列
5. 摘要结尾句优化

## 预准备 Rebuttal
1. ImageNet 规模验证 → 准备 Tiny-ViT-5M ImageNet-1K 10-epoch 测试
2. 真实硬件验证 → 合作课题组器件数据拟合结果
3. NL=2.0 代理模型真实性 → Vincze 2025 实测 NL 曲线拟合对比图

## 最终 Gut Call
**Accept with minor revision**
核心理由：填补有机光电表征与 ViT 部署的关键方法学空白，Ensemble HAT 解决核心泛化难题，多维度稳健性验证，局限性透明。

---

# 【评审来源 4】EXTERNAL_REVIEW_GPT_20260420.md

## 1. Central Claim Stress Test
Ensemble HAT 86.37±1.54% 可防御。10% baseline  framing 诚实（collapsed single-class predictor + no-AMP）。
建议：Abstract 中加 "(chance level for the balanced 10-class task)"

## 2. Generality vs Over-reach
ImageNet scoping 诚实（§4.6）。建议：加 quantitative footnote（per-epoch resampling wall-clock time）

## 3. Methodological Holes
- Gaussian D2D：SX.Z AR(1) 缓解，但 training-time i.i.d. resampling 假设未测试 correlated maps
- CrossSim：14.43 pp divergence 需要具体 mapping difference 解释
- Energy：consistently hedged，无 creep
- STE + NL gradient scaling 复合效应未分析（新增漏洞）

## 4. Severe-NL Supplementary Ablation
无法完全评估（具体数字不在提供的文本中）。若 MLP-only 87.79% 但 fresh 仅 ~32%，必须在 87.79% 后立刻说明。

## 5. Rebuttal Risk Top 3
1. 设备模型过于理想化（major revision 概率 9/10）→ 用 risk ranking 定位 + 敏感性分析 disarm
2. 无物理硬件验证（7/10）→ 若有任何实测数据即大幅加强；若无，需 concrete timeline
3. Ensemble HAT 改进可能部分来自正则化（5/10）→ 控制实验：training D2D 分布上评估

## 6. Figures
Figure 4 披露足够但建议 visual hatch pattern。
Figure 5 的 10.00% bars 可能因 y-axis 从 0% 开始而几乎不可见，建议直接标注。

## 7. Structure
叙事优先结构适合 NC。建议：将 §3.7 移至 §3.4 后，使问题-解决方案连续。

## 8. One-Liner Verdict
**(b) Major revision needed**
负载理由：设备模型足够理想化，hardware-oriented reviewer 会质疑真实阵列迁移性。AR(1) 仅评估 inference-time correlation，training-time 未测；无 measured-device 验证。

---

# 【评审来源 5】External Reviewer Report (Reviewer #2)
**Recommendation: Minor Revision (Borderline Accept)**

## Executive Summary
修订解决了初评大部分关切。framing 收紧，simulation-only scope 明确披露，quantitative evidence 补充（correlated D2D、no-AMP 10% 确认）。

## 8 点详细回答
1. **Central Claim**：Excellent。10% baseline 有 no-AMP 确认。
2. **ImageNet**：Much improved。建议加 training overhead quantitative footnote。
3. **Methodological Holes**：Gaussian D2D（Low risk）、CrossSim（Very low）、Energy（Low）、Write-verify（Low）。
4. **Severe-NL**：Excellent。32.12% 披露 neutralizes "fifth contribution" risk。
5. **Rebuttal Risk**：Hardware validation（Low）、ADC cliff obvious（Low）、Ensemble HAT = multi-instance（Low）。新潜在 objection：ρ>0.8 未测。
6. **Figures**：Borderline acceptable。建议加 † symbol。
7. **Structure**：Good。
8. **Verdict**：(a) Accept with minor revision。

## Specific Minor Revisions Requested
1. Abstract：10.00% → "10.00% (chance level for the balanced 10-class task)"
2. §4.5 footnote：per-epoch resampling wall-clock time
3. Figure 1：† symbol for deterministic bars
4. §2.3："first-class device primitives" → "native profile parameters"

---

# 【评审来源 6】中文评审意见（Reviewer #3）
** verdict：需要大修**

## 8 点回答
1. **中心主张**：可防御。10% 基线是 collapsed single-class predictor，有 FP32 验证。
2. **泛化性**：诚实。ImageNet 局限明确。
3. **方法论漏洞**：
   - 固定高斯 D2D：SX.Z 有 ρ=0.3 测试，但未考虑重尾
   - CrossSim：披露充分（1k 子集、throughput 限制）
   - 能量：一致回避，无过度营销
4. ** severe-NL**：诚实。MLP-only 87.79%，QKV/attn-proj ~18%，定位为训练诊断工具。
5. **反驳风险**：
   - 硬件过拟合已知问题，Ensemble HAT 新颖性不足（中-高）
   - 设备模型过于简化（高）
   - 结果限于小型数据集（中）
6. **图表**：披露基本足够，建议 visual style 区分。
7. **结构**：叙事优先符合 NC，可接受。
8. **一句话裁决**：**需要大修**。方法学简化 + 限于小型数据集，需更广泛评估或更强实验验证。

---

# 【评审来源 7】增量差异评估（v(file:9/8) vs 上一版）

## 已关闭（P1-P5）
- P1 CrossSim SX.Y：完整段落 ✅
- P2 MC 层级披露：§5.2 Eq.4 后明确说明 ✅
- P3 MLP fresh-instance：Table S16 报告 32.12% ✅
- P4 D2D 空间相关：§4.5 前置 + SX.Z ✅
- P5 Figure 1 视觉区分：hatching ✅

## 仍存在的问题
1. SX.Y/SX.Z 占位符编号未替换真实章节号（格式问题）
2. 能源数字在结论中限定语改善（可接受）
3. **Figure 4(c) 误差棒不一致**：主文 86.37±**1.62%**，其他所有位置 86.37±**1.54%**

## 提交准备度
接近 minor revision/accept。纯格式问题 + 数字一致性问题，30 分钟内可完成。

---

# 【评审来源 8】最终质量评估（April 20 vs April 18）

## Checklist 完成
P1 SX.Y ✅ | P2 MC 层级 ✅ | P3 MLP 32.12% ✅ | P4 D2D ✅ | P5 Figure 1 hatching ✅
48 小时内解决 5 项，新增 2 个完整 Supplementary Note。

## 新增高光内容
- SX.Y：CrossSim 完整披露（Wilson CI + t-CI + σ=2.67%）
- SX.Z：AR(1) 压力测试（ρ=0.3/0.5，bounded degradation）
- Table S16：完整 scoping（32.12% / 32.60% fresh-instance）

## 剩余风险（<5%）
- i.i.d. Gaussian D2D：<1%（SX.Z 实证）
- CrossSim n=3：0%（SX.Y CI）
- CIFAR scope：10%（§4.6 ImageNet 局限）
- MLP overclaim：0%（Table S16）

## NC 投稿准备度：⭐⭐⭐⭐⭐（5/5）
技术严谨性 + 科学诚实性 + 审稿人防御 + 投稿策略均达标。
**最终推荐：今晚提交。**

---

# 【评审来源 9】External Review（Major Revision 视角）

## 1. Central Claim
可防御，但需说明 single-class predictor 机制（哪个 class、是否依赖 D2D seed）。

## 2. ImageNet
6-bit ADC cliff 可能上移。建议：CIFAR-100 ADC sweep 一句话量化。

## 3. Methodological Holes
- **最大漏洞**：Gaussian D2D。AR(1) 仅 inference-time，training-time 仍 i.i.d.
- CrossSim 14.43 pp divergence 需具体 mapping difference 解释
- STE + NL gradient scaling 复合效应未分析

## 4. Severe-NL
具体数字（87.79%, ~18%, ~32%）不在提供文本中。若在补充材料，必须在 87.79% 后立即说明 ~32% fresh-instance。

## 5. Rebuttal Risk
1. 设备模型过于理想化（9/10）→ risk ranking 定位
2. 无硬件验证（7/10）→ 实测数据或 concrete timeline
3. Ensemble HAT 可能部分来自正则化（5/10）→ training D2D 分布控制实验

## 6. Figures
Figure 4 建议 visual differentiation。
Figure 5 的 10.00% bars 可能几乎不可见（y-axis 从 0% 开始）。

## 7. Structure
建议 §3.7 移至 §3.4 后，使 collapse → recovery 连续。

## 8. Verdict
**(b) Major revision needed**
负载理由：设备模型足够理想化，hardware-oriented reviewer 会质疑。AR(1) 仅 inference-time；无 measured-device 验证。

---

# 【评审来源 10】"读完最新版本的两份 PDF"增量 diff

## P1-P5 全部关闭
与评审来源 7 一致。

## 残留问题
1. SX.Y/SX.Z 占位符 → 需替换真实编号
2. 能源限定语 → 已改善，可接受
3. **Figure 4(c) 86.37±1.62% vs ±1.54% 不一致**（新发现，check_locked_numbers.py 可能未覆盖图内数字）

## 提交准备度
接近 minor revision/accept。两条遗留项均不涉及实验数据，30 分钟可完成。
