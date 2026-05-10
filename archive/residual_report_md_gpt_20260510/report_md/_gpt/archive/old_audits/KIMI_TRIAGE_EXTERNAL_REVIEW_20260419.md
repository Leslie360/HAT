# Kimi 对外审意见的 triage 与行动计划

**Date:** 2026-04-19 22:15
**Source:** `EXTERNAL_REVIEW_COMPILATION_20260419.md` (5 位独立评审人)
**Status:** 待 Claude 确认优先级

---

## 评审共识速览

| 评审人 | 评级 | 核心判断 |
|:---|:---|:---|
| A | Major Revision | 框架张力：标题/摘要过度承诺"部署"，正文正确限定为"模拟" |
| B | Minor Revision | 科学成熟，贡献清晰，只需收紧 framing |
| C | Minor Revision | 2 个具体错误（SX.Y 缺失 + MC 层次未披露）会拉低第一印象 |
| D | Minor Revision | 诚实界定 + 统计严谨 + Ensemble HAT 真实 |
| E | Major (achievable) | i.i.d. Gaussian D2D 是最大漏洞，建议跑空间相关消融 |
| 合成评估 | **Major Revision 轨道，但有竞争力** | 3 个 blocker + 6 个 should-fix |

---

## 🔴 Blockers — 提交前必须修复（低 effort / 高 impact）

### B-1: SX.Y 交叉引用缺失
**问题：** §4.6 引用了 `Supplementary Note~SX.Y`，但该 note 不存在。多位评审人（A、C）标记为 concrete error。
**修复：** 两种选择：
- (a) 写一段 ~100 词的 SX.Y supplementary note（已有 CrossSim correction draft 可用）
- (b) 移除交叉引用，把披露句直接嵌入正文
**建议：** 选 (a)，因为 CrossSim correction draft 已经准备好了。
**耗时：** ~15 分钟

### B-2: 两级 MC 层次未披露
**问题：** 86.37±1.54% 是 10 个 fresh instance 的均值的标准差，但每个 instance 又有 5 次 MC forward-pass。评审人 C 指出这种两级结构（mean-of-means）在正文中未说明。
**修复：** 在 Methods (§5.2, Eq. 4 附近) 加一句：
> "Each fresh-instance mean is itself the mean of 5 forward-pass MC evaluations; the reported ±1.54% is the standard deviation across the 10 per-instance means."
**耗时：** ~5 分钟

### B-3: MLP 线性化的 fresh-instance 转移缺失
**问题：** Table S16 显示 MLP-only 线性化恢复 87.79%（in-distribution），但未披露其 fresh-instance 转移只有 ~32%（远差于 Ensemble HAT 的 86.37%）。评审人 A、C 都认为这会导致 reviewer 误以为我们在"隐藏第五个贡献"。
**修复：** 在 Table S16 的 interpretation note 中加一句：
> "Note that the MLP-linearized model achieves ~32% fresh-instance transfer accuracy under the same 10-array evaluation protocol, compared to 86.37±1.54% for Ensemble HAT, confirming that this ablation is a diagnostic tool rather than a deployment-grade mitigation."
**耗时：** ~10 分钟

---

## 🟡 Should-Fix — 强烈建议（可显著降低 major revision 概率）

### S-1: 空间相关 D2D 消融实验（~1 天）
**问题：** i.i.d. Gaussian D2D 是最大方法学漏洞。评审人 A、C、E 都标记为高风险。评审人 E 说这是"唯一值得在提交前跑的实验"。
**修复：** 跑一个 2D 空间相关 D2D 消融（例如 AR(1) 模型，ρ=0.3 或 0.5），比较 Ensemble HAT 的 fresh-instance 转移是否仍 >80%。即使绝对准确率下降，只要排名不变（Ensemble > Standard），就足以 disarm 该 objection。
**可行性：** 代码基础设施已具备，只需修改 D2D 采样逻辑。GPU 当前空闲。
**耗时：** ~4-8 小时（训练 + 评估）
**建议：** 这是性价比最高的实验投资。强烈建议跑。

### S-2: 标题/摘要 framing 调整
**问题：** 多位评审人（A、E）指出标题和摘要过度承诺"部署"（"edge vision"），而正文正确限定为"模拟决策工具"。
**修复选项：**
- (a) 标题微调：加入 "Simulation Framework" 或 "Behavioral Simulation"
- (b) 摘要首句明确 "We present a simulation framework..."
- (c) 在 Limitations 中明确 "Validation against fabricated organic arrays is deferred to future work"
**建议：** 选 (b) + (c)，改动最小但效果显著。
**耗时：** ~20 分钟

### S-3: Figure 1 视觉区分
**问题：** 确定性基线（无误差棒）与 MC 结果（有误差棒）混合，视觉上传达错误信号。
**修复：** 给确定性 bar 添加斜线填充（hatch）或虚线边框，与 MC bar 区分。
**耗时：** ~30 分钟（修改 matplotlib 脚本 + 重跑）

### S-4: CrossSim 14.43 pp 措辞软化
**问题：** n=1 clean / n=3 noise，1000-image 子集，评审人 C 认为 14.43 pp 差距"不能精确到 ±0.5 pp"。
**修复：** 从 "a 14.43 pp gap" 改为 "a 14.43 pp suggestive gap (n=3, preliminary)" 或 "a large qualitative divergence".
**耗时：** ~5 分钟

### S-5: ImageNet 失败模式预测
**问题：** 评审人 A、C、E 都建议在 Limitations 中明确预测 ImageNet 规模的可能失败模式（token embedding 饱和、D2D mismatch map 规模、ADC cliff 偏移）。
**修复：** 在 §4.5 加一段 3 句话的 ImageNet 外推限制。
**耗时：** ~15 分钟

### S-6: 方程前向引用
**问题：** Results 引用了 Methods 中后面才定义的方程（Eq. 1, 3, 8），造成阅读摩擦。
**修复：** 在 Results 中第一次引用时加 "(formally defined in §5.X)" 或把关键方程移到 Results 前的简短 Model 小节。
**耗时：** ~10 分钟

---

## 🟢 Nice-to-Have

### N-1: 10.00% collapsed predictor 披露
**问题：** 评审人 A 建议明确披露 10.00% 是"单类预测器"（collapsed predictor）而非 uniform random。
**修复：** 在 Methods 或 Supplementary 中确认 per-instance 的 top-1 预测是否全部 degenerate 到同一类。
**可行性：** 可以检查 `fresh_instance_eval.json` 的 raw predictions（如果有保存）。

### N-2: per-batch HAT 基线前移
**问题：** 评审人 E 指出 fixed-mask HAT 可能被质疑为"straw man"，建议把 per-batch 基线（86.16%）移到正文。
**修复：** 在 §3.7 中显式比较 fixed-mask (10.00%) vs. per-batch (86.16%) vs. per-epoch (86.37%)。
**耗时：** ~15 分钟

### N-3: write-verify 开销披露
**问题：** 评审人 A 指出能量模型未考虑 iterative program-and-verify pulses。
**修复：** 在 Limitations 中加一句。
**耗时：** ~5 分钟

### N-4: 能耗 Conclusion 措辞
**问题：** Conclusion 中能量数字缺少 "placeholder" 限定词。
**修复：** 加回限定词。
**耗时：** ~2 分钟

---

## 时间线建议

| 阶段 | 任务 | 耗时 | 优先级 |
|:---|:---|:---|:---|
| **今晚** | B-1, B-2, B-3（3 个 blocker 文本修复） | 30 分钟 | 🔴 |
| **今晚** | S-2, S-4, S-5, S-6, N-2, N-3, N-4（文本修复） | 1.5 小时 | 🟡 |
| **今晚/明早** | S-3（Figure 1 重绘） | 30 分钟 | 🟡 |
| **明早** | S-1（空间相关 D2D 消融）启动 | 4-8 小时 | 🟡 |
| **后天** | 收割 S-1 结果，更新 supplementary，最终编译 | 2 小时 | 🟡 |
| **提交** | 打包 submission bundle | 30 分钟 | — |

---

## Kimi 的立场

**建议采取 Option B（完整路线）的变体：**

1. **今晚先把 3 个 blocker + 所有文本修复全部落地**（~2 小时）
2. **明早启动空间相关 D2D 消融**（GPU 当前空闲，代码基础设施已具备）
3. **后天收割结果并更新 supplementary**
4. **然后提交**

理由：
- 3 个 blocker 是"立等可取"的修复，不修复会立即损害第一印象
- 空间相关 D2D 实验是评审人 E 认定的"唯一值得在提交前跑的实验"，且代码基础设施已具备
- 其余文本修复都是低 effort 高 impact 的操作
- 总耗时控制在 24-48 小时内，不影响提交时间表

**如果 Claude 认为空间相关 D2D 实验不可行，则退而求其次：**
- 在 §5.2 中加一句明确说明 "The framework can ingest an arbitrary spatial covariance matrix; the current i.i.d. Gaussian treatment is a conservative baseline that can be replaced by measured array data."
- 这虽然不是实验证据，但至少表明框架设计上支持该扩展

---

**文件位置：**
- 外审原文：`report_md/_gpt/EXTERNAL_REVIEW_COMPILATION_20260419.md` (34.9 KiB)
- 本 triage 文件：`report_md/_gpt/KIMI_TRIAGE_EXTERNAL_REVIEW_20260419.md`
