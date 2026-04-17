# Gemini 任务单 — Round 2 (2026-04-11, Claude 审阅后)

> **上一轮结构重构质量好。本轮聚焦：收尾压缩 + 交叉引用修复。**

---

## 当前状态确认

- §4: 8 行 ✅（内容在 Supplementary）
- §5: 144 行, 8 subsections ✅
- §6: 52 行 ✅
- supplementary.tex: 14974 bytes, Supp Fig S1/S2/S3 已定义 ✅
- 主文引用 Supplementary Fig S1/S2/S3 ✅ 已确认正确

---

## GM-R1: 主文继续压缩到 NC 目标 [HIGH]

当前 ~14 页，NC 目标 8-10 页（不含 Methods/Supp）。

**检查并执行以下压缩：**
1. §1 Introduction: 如果超过 2 页，压缩 background 段落
2. §3 Methodology: 检查是否有可移入 Supplementary Methods 的数学推导
3. §5 Results: 检查是否还有可以移入 Supp 的非核心 subsection
4. §7 Conclusion: 确认 <1 页

**注意：** 不要删除 reviewer 要求的内容（已验证的 ✅ 项）。只压缩冗余文字。

---

## GM-R2: Supplementary 完整性检查 [MED]

1. 确认 Supplementary 中的所有 `\ref{...}` 和 `\citep{...}` 都解析正确
2. 确认从主文移入的 Table/Figure 在 Supplementary 中有完整的 caption
3. 检查 Supplementary 是否需要自己的 `\bibliography`（如果是独立 .tex 的话）

---

## GM-R3: 新 Review 措辞修复确认 [LOW]

Codex 吸收了 mimo-v2-pro + GLM-5.1 review 并做了 2 处措辞修改：
1. §5.4 ADC 措辞软化
2. Zhang case-study 措辞软化

请在以下文件中确认这些修改与周围文字一致：
- `05_results.tex` — ADC 段落
- `05_results.tex` — Case Study 段落

---

## 不要做的事

- 不要碰 `refs_gpt.bib`（已由 Kimi 审计通过 + Codex 补 DOI）
- 不要改 Locked Numbers 中的任何数字
- 不要 overclaim 完成度（上轮 #34 教训）