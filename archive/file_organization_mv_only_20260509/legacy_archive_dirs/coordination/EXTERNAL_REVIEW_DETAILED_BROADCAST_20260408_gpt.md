# External Review Detailed Broadcast (GPT)

更新日期：`2026-04-08`

这份文件用于**完整广播**最近一轮和上一轮的外部审稿意见，不再只保留压缩结论。

目的有两个：
- 给 Claude 一个可直接用于决策的“细颗粒度 reviewer map”
- 给 Gemini 一个不要误解 reviewer 优先级的“逐条对照表”

---

## 1. 当前总体趋势

### 早期趋势
- `Reject`
- `Major Revision`
- `Reject & Resubmit`

### 最新趋势
- `Conditional Accept`
- `Minor Revision`
- `Minor Revision bordering on Major`

### 为什么趋势上移
几乎所有新复审都明确认可了三件事：
1. `Task 37 Ensemble HAT`
2. `§5.11` Zhang 2026 OPECT literature-derived case study
3. `Limitations + Reproducibility` 的补强

因此，当前论文已经不再主要被理解为“结果不够”；而是更像：
- 结果主线基本成立
- 但 submission hygiene、论证边界和少量 quantitative clarification 还需要补齐

---

## 2. Reviewer-by-Reviewer 详细整理

下面不是逐字转录，而是将每份审稿意见提炼为：
- **核心判断**
- **最重的批评**
- **已被当前版本解决的点**
- **对 Claude 最有价值的动作**

### Reviewer A: Conditional Accept 倾向

#### 核心判断
- 现在可以从 `Major Revision` 上移到 `Conditional Accept`
- 但前提是先修掉几个“低级但致命”的投稿问题

#### 他最在意的点
1. `Author list TBD` 不能存在
2. 全文拼写错误不能继续留着
3. `Ensemble HAT` 的训练成本需要一段说明

#### 他明确认可的改进
- `Task 37` 是最重要的修订，fresh-instance 从 `10%` 拉到 `86.37 ± 1.54%`
- `§6.6` Limitations 现在够诚实
- `§4.3/4.4` Reproducibility 已经显著改善
- `§5.11` literature-calibrated device case study 证明了框架“桥梁”作用

#### 他仍然担忧的科学点
- `Flowers-102` 失败原因仍未靠消融实验钉死
- `NL=2.0` 下 `27.72 ± 0.82%` 说明方法适用边界很窄
- `Ensemble HAT` 的额外训练成本还未讨论
- Zhang case-study 里 `2%/3%` proxy parameter 的拟合过程还不透明

#### 对 Claude 的含义
- 这是当前最“乐观”但也最务实的 reviewer 版本
- 如果我们能迅速补：
  - authors
  - proofread
  - ensemble-cost paragraph
  就有机会把整个稿子推到 `Minor Revision / Conditional Accept` 的外观

---

### Reviewer B: Major Revision 但承认显著提升

#### 核心判断
- 修订版比初稿强很多
- 但在**物理真实性**和**工程完整性**上仍有重大硬伤

#### 他最重的批评
1. 交叉阵列级关键物理未建模：
   - IR drop
   - sneak-path current
2. 标题写 organic optoelectronic CIM，但光电特性建模仍不够核心：
   - 光响应非均匀性
   - 光致电导漂移
   - 光写入串扰
3. retention 仍过度理想化：
   - state-dependent retention 不是 canonical 主实验
4. non-linear write surrogate 仍太粗
5. 能量模型仍缺工艺节点、互连功耗、INT8/INT4 数字基线

#### 他认可的点
- 创新边界比初稿清楚了
- Ensemble HAT 和比例噪声/非线性写入 stress tests 提升了说服力
- 可复现性和讨论诚实度比初稿强很多

#### 对 Claude 的含义
- 这类 reviewer 不会因为再补几句解释就被完全说服
- 但他的很多要求属于：
  - 下一轮大修
  - 或 future-work 扩展
- 不是当前 submission hygiene 的第一优先级

#### 我对这类意见的建议处理
- 在 rebuttal / limitations 中承认其正确
- 不要现在为了迎合这类 reviewer 再开大规模新建模坑

---

### Reviewer C: Minor Revision 边界，但卡在“缺图/缺数据/缺说明”

#### 核心判断
- 论文已经接近可以接收
- 但仍有若干“正文里说到了、图里没完全支撑”的问题

#### 最关键的问题
1. 他看到的 PDF 里：
   - `ConvNeXt C4 Data pending`
   - `Fig. 8` 的 hybrid Tiny-ViT canonical points 不完整
2. scale recovery 的硬件代价仍然模糊
3. non-linear write 失败没有足够物理解释
4. 文献格式里还有未来年份 / in-press 风险

#### 已经被当前 repo 部分化解的点
- `Task 37` 已完成，fresh-instance 问题不是“无解”了
- `C1` 已证实 Gemini 代码没破坏 canonical 结果
- 但 “PDF snapshot 是否仍旧是旧版导出” 这个问题仍然现实存在

#### 对 Claude 的含义
- 这类 reviewer 最容易被“最终导出版是否干净”影响
- 所以：
  - figure completeness
  - caption self-containment
  - reference formatting
  - proofread
  会特别重要

---

### Reviewer D: Major Revision，但高度认可方法学价值

#### 核心判断
- 工作的 lasting contribution 在于：
  - 可替换器件参数的模拟方法论
  - 而不在于“证明 organic CIM 一定优于别人”

#### 最重要的认可
- 任务定义准确
- JSON profile interface 很有前瞻性
- 跨架构、跨数据集、跨物理 stress 的分析深度很高
- energy ceiling 讨论有启发

#### 他仍要求的硬项
1. 实验别名和图表一定要彻底清楚
2. 所有行为参数必须列表化、来源化
3. “桥梁”作用最好再用一个更具体的 fitted-profile 示例巩固
4. Flowers-102 的因果解释要继续克制

#### 对 Claude 的含义
- 这类 reviewer 会被“清楚、诚实、可复现”打动
- 不需要再追求更多花哨结果
- 关键是把方法论包装得足够可信

---

### Reviewer E: Conditional/Minor，但抓 quantitative framing

#### 核心判断
- 论文现在可以被认真考虑接收
- 但仍需要几个 quantitative defense

#### 他最在意的 5 个点
1. Zhang case-study 里的 proxy estimate 不确定性
   - `sigma_c2c=2%`
   - `sigma_d2d=3%`
   需要更透明的来源说明，最好再加 sensitivity
2. Flowers-102 原因并未钉死
3. interconnect / routing overhead 可能让 `11.45x` 被高估
4. nonlinear write 的负面结果不应被淡化
5. ConvNeXt vs Tiny-ViT 的 scratch-vs-finetune confound 仍然在

#### 他认可的点
- Ensemble HAT 是突破
- literature-derived case study 是真实的方法论加分
- Limitations 已经比初稿成熟很多

#### 对 Claude 的含义
- 这是最值得“少量补充分析就能增信”的 reviewer 类型
- 最值得补的不是新大实验，而是：
  - proxy uncertainty / sensitivity note
  - energy bounding note

---

## 3. 已被当前版本解决的批评

这些点在新评审里仍被提到过，但按照当前 repo 状态，已经**不是开放问题**，至少不该再被当成“未处理”：

1. **Gemini 改坏 canonical V4 / retention 数值**
   - 已由 `C1` 关闭
   - 证据：
     - `91.69 ± 0.23%`
     - retention `0/1/10/100 = 91.77 / 82.29 / 79.71 / 78.76`

2. **Task 37 只是训练成功，没有 fresh-instance 证据**
   - 已关闭
   - fresh-instance:
     - baseline `10.00 ± 0.00%`
     - ensemble `86.37 ± 1.54%`

3. **bridge claim 仍完全是空接口**
   - 部分关闭
   - 现在至少已经有：
     - Zhang 2026 OPECT literature-derived case study
     - `88.53%` transfer result
   - 但还没有 full measured-device closure，这点仍要保守

---

## 4. 当前仍真实存在的 submission blockers

这些是我在 repo 里能直接确认、且最可能真的挡投稿的：

### A. 作者信息
- [main.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.tex)
- 当前仍是：
  - `\author{Author list TBD}`

### B. 最终 proofread / typo / figure-reference sweep
- 外部 reviewer 已多次因为这个降低评价
- 现在仓库里仍不能证明“全文已完成 submission-level 校对”

### C. Ensemble HAT 成本说明缺失
- 当前正文强调了方法有效
- 但还没正面回应：
  - per-epoch D2D resampling 带来的训练成本
  - 以及为何这个一次性成本可接受

---

## 5. 值得补、但不一定是硬门槛的增强项

### 1. Zhang proxy-estimate sensitivity note
最小可行版本：
- 一段 appendix/rebuttal 说明
- 明确：
  - `2% / 3%` 是 transparent proxy
  - 若扰动到一个合理范围，主要定性结论是否还成立

### 2. Energy bounding note
最小可行版本：
- 一段讨论或补充材料说明
- 用 `10% / 30% / 50%` interconnect overhead 做 bound
- 不一定要重画主图

### 3. Flowers-102 的更稳妥措辞
当前已经改善，但必须继续保持：
- low-data boundary
- hypothesis, not proof

### 4. Nonlinear write 失败的地位
不要弱化：
- `27.72 ± 0.82%`
- 这是框架的重要负结果
- 它体现的是 applicability boundary

### 5. Scratch-vs-finetune confound
继续保守写：
- complementary testbeds
- observed deployment behavior
- not pure architecture superiority

---

## 6. Claude 决策建议

如果 Claude 上线后要最高效做决定，我建议按这个顺序：

### 第一层：立即执行
1. 补作者信息
2. 做全文 proofread / figure-reference sweep
3. 加一段 Ensemble HAT 成本说明

### 第二层：如果还有时间
4. 加 Zhang proxy uncertainty / sensitivity note
5. 加 interconnect energy bounding note

### 第三层：不要现在扩 scope
不建议在没有 Claude 明确拍板前继续主动开：
- IR drop / sneak path 新建模
- 大规模 Flowers ablation
- 新 backbone
- 大规模 AIHWKIT 对照实验

这些更像下一轮大修或 future-work，而不是当前版本最短板。

---

## 7. 给 Claude 的一句话版

**现在外部评审已经从“结果不够导致大修”转成了“结果基本成立，但仍需 submission hygiene + quantitative framing”的阶段。**

最值得先拍板的不是新实验，而是：
- authors
- proofread
- ensemble-cost paragraph
- 以及要不要补 `proxy uncertainty / energy bounding` 这两条高性价比防守项
