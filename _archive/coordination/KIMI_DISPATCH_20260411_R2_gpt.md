# Kimi 任务单 — Round 2 (2026-04-11, Claude 审阅后)

> **上一轮表现优秀！KM5/KM7 发现的 CRITICAL 问题非常有价值。**
> **本轮任务：扩展校对范围 + 最终质量门。**

---

## 上一轮问题

**AGENT_SYNC 报告重复了 5 次。** KM1-KM4 的内容在 AGENT_SYNC 中出现了多次相同的 block。下次写入时请检查是否已有相同内容，避免重复追加。

**KM5 Supp Fig 问题已解决。** Gemini 已在 supplementary.tex 中定义了 S1/S2/S3 图表环境。

---

## KM-R1: §5 Results 全文校对 [HIGH]

**这是论文最核心的章节，之前未校对。**

**检查文件：** `paper/latex_gpt/sections/05_results.tex`

**检查项：**
- 所有数字与 Locked Numbers 一致
- `\ref{fig:...}` 引用是否指向正确的 figure label
- Supplementary Fig S1/S2/S3 引用格式一致
- 数学公式格式（`\textbf{}` 中的数字是否正确）
- 段落之间的逻辑连贯性
- 被 Gemini 合并的 subsections（§5.2-5.4 → "Quantization and Noise Resilience"、§5.8-5.9 → "NL Writing and HAT"）内容是否完整

**交付：** 问题清单，写入 AGENT_SYNC（只写一次！不要重复）

---

## KM-R2: §3 Methodology + §6 Discussion 校对 [MED]

**检查文件：**
- `paper/latex_gpt/sections/03_methodology.tex`
- `paper/latex_gpt/sections/06_discussion.tex`

**检查项：**
- 数字精度统一（10.00% not 10%）
- 术语一致性
- Codex 新增的措辞修改（ADC 软化、Zhang 软化）是否通顺
- §6 压缩后逻辑是否完整

---

## KM-R3: Supplementary 全文校对 [MED]

**检查文件：** `paper/latex_gpt/supplementary.tex`

**检查项：**
- 从主文移入的内容是否完整（Table、Figure、数据）
- Caption 是否清晰
- 交叉引用是否解析（与主文 label 匹配）
- 数字一致性

---

## KM-R4: 最终编译检查 [LOW]

如果可以的话，尝试编译 main.tex 并检查：
- 有无 `??` 未解析引用
- 有无 LaTeX warning
- 总页数

如果无法编译，跳过此项。

---

## 规则（重申）

1. **不要直接改 .tex 文件** — 只提建议
2. **AGENT_SYNC 只写一次** — 不要重复追加相同内容
3. **数字只对照 Locked Numbers** — 不要用外部来源
