# Kimi 任务单 — Round 3 (Codex/Gemini 下线，Kimi 全面接管)

> **Codex 和 Gemini 已下线。你是当前唯一活跃 agent。**
> **P13 在后台自动运行，不需要你管。**
> **本轮你可以直接编辑所有 .tex 文件。**

---

## 当前论文状态

| 指标 | 值 |
|:--|:--|
| main.pdf | 13 页（含参考文献），编译干净 |
| supplementary_main.pdf | 10 页，独立编译 |
| P13-full | PID 214264 运行中（CPU analog, 2.5h+），watcher 自动接 P14 |
| Coverage | ✅~48/104 (46%) |

---

## 文件权限（本轮扩大）

你现在可以直接编辑以下所有文件：
- `paper/latex_gpt/sections/*.tex` (所有章节)
- `paper/latex_gpt/supplementary.tex`
- `paper/latex_gpt/refs_gpt.bib`
- `report_md/_gpt/*.md` (所有报告文件)

**不要碰的文件：**
- `paper/latex_gpt/main.tex` (编译入口，不要改结构)
- `scripts/_gpt/*.py` 或 `*.sh` (代码是 Codex 的领域)
- `checkpoints/` 或 `logs/` (实验数据)

---

## Task KR1: 接管 Gemini GM-R1 — 继续压缩 [HIGH]

主文 13 页，NC 目标 ~10 页（不含参考文献约 2-3 页，实际内容约 10-11 页）。

**操作：**
1. 读每个 section 文件，找可以进一步精简的段落
2. 重点目标：
   - `01_introduction.tex` (12 行) — 检查是否有可删的 background
   - `05_results.tex` (107 行) — 最长的 section，找重复或冗余描述
   - `06_discussion.tex` (53 行) — 检查是否有与 Results 重复的讨论
3. 压缩手段：
   - 删除重复的 transition 句子
   - 合并短段落
   - 把 detail 移到 Supplementary（但不要新建 section，追加到已有的部分）
4. **目标：总共再砍 1-2 页**

**注意：不要删除以下内容（reviewer 要求的）：**
- Scale masking 解释
- Energy 11.45x qualifier ("first-order, upper-bound-like")
- Ensemble HAT capacity tradeoff
- Intro limitation statement
- C4 三种子 84.75±0.72%

---

## Task KR2: 接管 Gemini GM-R2 — Supplementary 完整性 [MED]

**操作：**
1. 读 `paper/latex_gpt/supplementary.tex` (255 行)
2. 检查：
   - 所有 Table 有 caption 和 label
   - 所有 Figure 有 caption 和 label (S1/S2/S3 已有)
   - `\citep{...}` 引用是否都在 `refs_gpt.bib` 中
   - 从主文移入的内容是否完整（不缺数据）
3. 如果发现问题，直接修复

---

## Task KR3: 接管 Gemini GM-R3 — 措辞确认 [MED]

Codex 在 Round 2 做了两处措辞软化：
1. §5 ADC: 改为 "critical threshold near 6 bits under the present simulator assumptions"
2. §5 Case Study: Zhang 2026 改为 proxy-backed illustration

**操作：**
1. 在 `05_results.tex` 中找到这两处
2. 确认措辞通顺、与上下文一致
3. 如果有不协调的地方，微调

---

## Task KR4: Energy Routing Sensitivity 验证 [MED]

Codex 新增了能量路由 sensitivity 数据：
- 10% overhead → 282.52 µJ (11.10x)
- 30% overhead → 299.70 µJ (10.47x)
- 50% overhead → 316.87 µJ (9.90x)

**操作：**
1. 在 `05_results.tex` 或 `06_discussion.tex` 中找到这段
2. 验证数字一致性（273.94 基准 + overhead = 上述值？）
3. 确认 reviewer #23 (energy interconnect overhead) 已充分回应

---

## Task KR5: Title 候选方案完善 [LOW]

Codex 提出了 3 个候选：
1. Hardware-Aware Simulation of Organic Optoelectronic CIM for Edge Vision Transformers
2. Profile-Driven Hardware-Aware Simulation for Organic Optoelectronic Vision Transformers
3. Organic Optoelectronic CIM Simulation for Edge Vision Transformer Deployment

**操作：**
1. 评估 3 个候选，写出优劣分析
2. 如果有更好的方案，提出 1-2 个替代
3. 写入 AGENT_SYNC，等用户决定

---

## Task KR6: Coverage Matrix 更新 [LOW]

根据 Codex Round 2 的工作（energy sensitivity, caption pass, label fix, split build），更新 `REVIEWER_COVERAGE_MATRIX_gpt.md` 中相关 issue 的状态。

特别关注：
- #23 (energy interconnect overhead) — Codex 加了 sensitivity bounds → 应升级
- #6 (array non-idealities) — 已有 IR drop quantitative → ✅
- #44 (manuscript length) — 13 页 → 进一步升级
- #67 (results fragmented) — 已合并 → ✅

---

## 输出规则

1. **每个任务完成后在 AGENT_SYNC 追加一个 `[Kimi]` block — 只写一次！**
2. 直接编辑 .tex 文件时，记录修改了哪些文件的哪些行
3. 不确定的改动写方案而不是直接改
4. 不要编造数字或文献
