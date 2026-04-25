<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Kimi Round 2 Reports (KM-R1 to KM-R4)

> Codex verification note (2026-04-11): this proofreading report remains useful, but two flagged issues are now known to be stale/false-positive in the current manuscript state. The `fig:energy-pareto` unresolved-reference claim does not apply to the present source tree, and the `10%` vs `10.00%` wording issue in `06_discussion.tex` has already been fixed.

**Date:** 2026-04-11
**Task Source:** KIMI_DISPATCH_20260411_R2_gpt.md (Claude)

---

## [Kimi] KM-R1 — §5 Results 全文校对 [HIGH]

### Status
- 完成

### Critical Issues Found

| Issue | Severity | Details | Location |
|-------|----------|---------|----------|
| **Unresolved reference** | **HIGH** | `Fig.~\ref{fig:energy-pareto}` referenced but label does not exist. Actual label is `fig:energy-metrics` | Sec 5.7, line "estimates a total inference cost..." |
| Fig 3 order violation | MED | Fig 3 (snr-curves) defined at start of 05_results.tex but first mentioned in Sec 5.5. Figs 4-5 defined in Sec 5.2. LaTeX will number Fig 3 after Figs 4-5 | 05_results.tex structure |

### Detailed Findings

**数字一致性 (与 Locked Numbers 对比):**
| Number | Locked | Results Section | Match? |
|--------|--------|-----------------|--------|
| V1 FP32 | 98.06% | Not explicitly stated | N/A |
| V2 | 97.39% | "V2 still attains 97.39%" | ✓ |
| V3 CIFAR-100 | 44.06% | "drops from 86.94% to 44.06%" | ✓ |
| V4 CIFAR-100 HAT | 65.48% | "recovers the model to 65.48%" | ✓ |
| V4 fresh-instance | 10.00% | "collapses to 10.00%" | ✓ |
| Ensemble HAT | 86.37 ± 1.54% | "maintains an average accuracy of 86.37 ± 1.54%" | ✓ |
| Proportional HAT | 97.37 ± 0.05% | "retains 97.37 ± 0.05%" | ✓ |
| Nonlinear write NL=2 | 27.72 ± 0.82% | "evaluation remains at 27.72 ± 0.82%" | ✓ |
| Zhang 2026 OPECT | 88.53% | "maintained an accuracy of 88.53%" | ✓ |
| Energy | 273.94 μJ | "estimates a total inference cost of 273.94 μJ" | ✓ |
| Energy reduction | 11.45x | "corresponding to an 11.45x reduction" | ✓ |
| Digital attention cost | 57.9% | "Digital attention operations... still account for 57.9%" | ✓ |

**引用一致性:**
- Supplementary Fig.~S1 → referenced in Sec 5.2 ✓
- Supplementary Fig.~S2 → referenced in Sec 5.4 ✓
- Supplementary Fig.~S3 → referenced in Sec 5.7 ✓
- fig:accuracy-comparison → Fig 4 ✓
- fig:hat-recovery → Fig 5 ✓
- fig:retention-curve → Fig 7 ✓
- fig:frontend-compensation → Fig 6 ✓
- fig:energy-pareto → **DOES NOT EXIST** (actual label is fig:energy-metrics) ✗

**数学公式格式:**
- `$NL=2.0$` used consistently ✓
- `$	au_1, 	au_2, A_0$` in retention section ✓
- `$	heta_{	ext{phys}}$` properly formatted ✓

**段落逻辑:**
- Sec 5.2 (Quantization and Noise Resilience) 逻辑连贯，涵盖 V2/V3/V4/C2/C3/C4
- Sec 5.6 (NL Writing and HAT) 合并后内容完整，涵盖 Task 34/35/36/37
- Sec 5.8 (Case Study) 独立完整

### Recommended Fixes
1. **[CRITICAL]** Change `\ref{fig:energy-pareto}` to `\ref{fig:energy-metrics}` in Sec 5.7, or rename the figure label to match the reference.

---

## [Kimi] KM-R2 — §3 Methodology + §6 Discussion 校对 [MED]

### Status
- 完成

### Findings

**03_methodology.tex:**
- **术语一致性:** HAT, C2C, D2C, NL_LTP/NL_LTD, profile interface 使用一致 ✓
- **数字精度:** 无需要统一精度的数字（主要是概念描述）
- **引用检查:**
  - `\citep{wu2023bwq,wang2024epim,ge2024allspark}` ✓
  - `\citep{gebregiorgis2023organiccim,zhang2026opect}` ✓
  - `\citep{vincze2026dualplasticity}` ✓
  - `\citep{yoon2025adc}` ✓
- **Claude 提及的 ADC 软化:** Sec 3.5 "following the spirit of configurable mixed-precision converter studies" — 措辞已软化，通顺 ✓
- **Claude 提及的 Zhang 软化:** No explicit Zhang mention in Methodology; main discussion in Results.

**06_discussion.tex:**
- **术语一致性:** ✓
- **数字精度:**
  - "10% accuracy" in Sec 6.1 — **SHOULD BE** "10.00%" for consistency
  - "86.37 ± 1.54%" ✓
  - "97.37 ± 0.05%" ✓
  - "27.72 ± 0.82%" ✓
  - "11.45x" ✓
  - "57.9%" ✓
- **引用修复确认:** `\ref{subsec:limitations}` correctly used (was "Section~6" in intro, but that's acceptable)
- **逻辑完整性:** §6 压缩后逻辑完整，从瓶颈分析 → Transformer敏感性 → 任务复杂性 → 能量效率 → 限制 → 未来方向

### Recommended Fixes
1. [LOW] Change "10% accuracy" to "10.00% accuracy" in 06_discussion.tex Sec 6.1 for consistency with Results section.

---

## [Kimi] KM-R3 — Supplementary 全文校对 [MED]

### Status
- 完成

### Findings

**内容完整性 (从主文移入的内容):**
| Content | In Main Text | In Supplementary | Status |
|---------|--------------|------------------|--------|
| tab:v4-rerun-sanity | Not directly cited | Defined in Supp | ✓ (Supp-only table) |
| tab:provenance | Referenced via subsec | Defined in Supp | ✓ |
| tab:sensitivity | Not directly cited | Defined in Supp | ✓ (Supp-only table) |
| tab:sensitivity-ci | Not directly cited | Defined in Supp | ✓ (Supp-only table) |
| tab:retention-comparison | Referenced via subsec | Defined in Supp | ✓ |
| fig:supp-noise-sensitivity (S1) | Referenced as "Supplementary Fig.~S1" | Defined with label | ✓ |
| fig:supp-zero-shot-transfer (S2) | Referenced as "Supplementary Fig.~S2" | Defined with label | ✓ |
| fig:supp-attention-maps (S3) | Referenced as "Supplementary Fig.~S3" | Defined with label | ✓ |

**交叉引用验证:**
- `\label{sec:supplementary}` — defined, referenced from 04_experimental_setup.tex ✓
- `\label{subsec:parameter-provenance}` — defined, referenced from 05_results.tex ✓
- `\label{tab:provenance}` — defined, referenced within Supp ✓
- `\label{tab:sensitivity}` — defined, referenced within Supp ✓
- `\label{tab:sensitivity-ci}` — defined, referenced within Supp ✓
- `\label{tab:retention-comparison}` — defined, referenced within Supp ✓
- `\label{fig:supp-noise-sensitivity}` — defined (S1) ✓
- `\label{fig:supp-zero-shot-transfer}` — defined (S2) ✓
- `\label{fig:supp-attention-maps}` — defined (S3) ✓

**Caption 清晰度:**
- Table captions are descriptive ✓
- Figure captions for S1/S2/S3 include "Supplementary Figure SX" prefix for clarity ✓

**数字一致性:**
- Zhang 2026 parameters in tab:provenance match main text ✓
- Retention values in tab:retention-comparison match main text ✓
- Sensitivity analysis values internally consistent ✓

### Recommended Fixes
- None required. Supplementary is complete and consistent with main text.

---

## [Kimi] KM-R4 — 最终编译检查 [LOW]

### Status
- 跳过 (无法直接编译)

### Notes
- 在 KM-R1 中发现的 `\ref{fig:energy-pareto}` 未解析引用需要在编译前修复。
- 其他交叉引用经检查均应解析正确。

---

## Summary of Critical Issues (Round 2)

| Issue | Severity | File | Action Required |
|-------|----------|------|-----------------|
| Unresolved `\ref{fig:energy-pareto}` | **CRITICAL** | 05_results.tex | Change to `\ref{fig:energy-metrics}` or rename label |
| "10%" should be "10.00%" | LOW | 06_discussion.tex | Consistency fix |

---

**Report Generated:** 2026-04-11
**Kimi (Proofreading Agent)**
