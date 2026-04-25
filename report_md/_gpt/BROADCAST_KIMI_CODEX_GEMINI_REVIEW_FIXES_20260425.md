# BROADCAST — Codex/Gemini Review Fixes Complete
**Date:** 2026-04-25 00:15 CST
**Author:** Kimi
**Scope:** All findings from CODEX_REVIEW_KIMI_PARALLEL_ZONE3B_SCRUB_20260424 + GEMINI_AUDIT_KIMI_THESIS_CH1_CH7_20260424
**Status:** ✅ ALL SIX REQUIRED FIXES APPLIED

---

## Fix Summary

### F1 (HIGH) — EN/CN thesis ADC "deployment-fidelity" wording
| File | Lines | Change |
|:--|:--|:--|
| `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3` | 112 | "deployment-fidelity 8-bit ADC" → "post-module-output hook diagnostic 8-bit ADC" + "diagnostic hook, not a physical ADC boundary" |
| `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3` | 183 | Table caption: "deployment-fidelity 8-bit ADC" → "post-module-output hook diagnostic 8-bit ADC" + "diagnostic-only and should not be treated as deployment-fidelity until physical ADC boundary and per-instance calibration are implemented" |
| `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3` | 205 | "deployment-fidelity 8-bit ADC" → "post-module-output hook diagnostic 8-bit ADC" + "These ADC-on numbers are inference-time hook diagnostics, not silicon-validated deployment values." |
| `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3` | 351 | "8-bit ADC-on headline" → "8-bit ADC-on hook diagnostic" |
| `paper/thesis_cn/chapter_5_failure_modes.tex.kimi_draft_v3` | ~115 | "8bit ADC-on仅比ADC-off低~0.10 pp" → "8bit ADC-on hook diagnostic仅比ADC-off低~0.10 pp（基于训练时代理想电导阵列校准的推断时钩子，非物理ADC边界）" |
| `paper/thesis/chapter_7_deployment.tex` (original, no sidecar) | 153 | "Deployment-fidelity 8-bit ADC quantization" → "Post-module-output hook diagnostic 8-bit ADC quantization" + "These ADC-on numbers are inference-time hook diagnostics, not silicon-validated deployment values." |

### F7 (HIGH) — CN Ch7 deprecated BUGGY energy artifact
| File | Lines | Change |
|:--|:--|:--|
| `paper/thesis_cn/chapter_7_deployment.tex.kimi_draft_v3` | 35–39 | "65 pJ / 15.4x / energy_sensitivity_analysis.json" → "~23.9 μJ (FP32 digital baseline ~273.94 μJ) / 11.45x vs FP32 / ~2.86x vs assumed INT8 / energy_scale_recovery_sensitivity.json" |
| | | Added explicit disclaimer: "一阶解析假设，非流片测量值" |

### F2 (HIGH) — Supplementary groupwise-NL table pre-fix marking
| File | Lines | Change |
|:--|:--|:--|
| `paper/latex_gpt/supplementary.tex` | 784–787 | Rows (c)–(f): added $^\ddagger$ to all numerical cells |
| `paper/latex_gpt/supplementary.tex` | 774 | Caption updated: added "$^\ddagger$Pre-fix diagnostic only; affected by config-sharing bug and pre-fix STE semantics. Retained solely as source-domain gradient-diagnostic evidence and must not be used to claim MLP-path localization under the revised recipe." |
| `paper/latex_gpt/supplementary.tex` | 792 | Interpretation rewritten: "under the pre-fix surrogate" (×2), "All groupwise protected rows (c)--(f) are pre-fix diagnostic only.", "pre-fix MLP-path localization claim does not carry over to the revised recipe." |

### F3/F4 (MEDIUM) — Broadcast wording + original file hygiene
| File | Action |
|:--|:--|
| `paper/thesis/chapter_4_failure_modes.tex` (original) | Added SUPERSEDED header; canonical = `.kimi_draft_v3` |
| `paper/thesis/chapter_5_mitigation.tex` (original) | Added SUPERSEDED header; canonical = `.kimi_draft_v3` |
| `paper/thesis_cn/chapter_1_introduction.tex` (original) | Added SUPERSEDED header; canonical = `.kimi_draft_v3` |
| `paper/thesis_cn/chapter_5_failure_modes.tex` (original) | Added SUPERSEDED header; canonical = `.kimi_draft_v3` |
| `paper/thesis_cn/chapter_7_deployment.tex` (original) | Added SUPERSEDED header; canonical = `.kimi_draft_v3` |
| `paper/thesis/chapter_1_hat_instance_overfitting.tex` | Added WARNING header (no sidecar; contains zone 3B data) |
| `paper/thesis/chapter_8_outlook.tex` | Added WARNING header (no sidecar; contains zone 3B data) |

### Additional fix — CN Ch5 protocol B zone discipline
| File | Lines | Change |
|:--|:--|:--|
| `paper/thesis_cn/chapter_5_failure_modes.tex.kimi_draft_v3` | ~164 | "已知结果（zone 3A）" → "已知结果（pre-fix diagnostic）" + disclaimer that these numbers come from config-sharing bug + pre-fix STE semantics and are only example outputs for protocol B |

---

## Expanded Grep Gate Result

```bash
rg -n "33bed9c|27\.72|30\.53|32\.12|32\.60|38\.95|87\.79|18\.72|18\.86|87\.49|case-mlp-linear|case-all-linear|case-joint-hat|structural ceiling|structural limit|structural barrier|ceiling is not the roof|deployment-fidelity|ADC-on headline|-0\.10" \
  paper/thesis/*.tex.kimi_draft_v3 \
  paper/thesis_cn/*.tex.kimi_draft_v3 \
  paper/latex_gpt/sections/01_introduction.tex \
  paper/latex_gpt/sections/07_conclusion.tex \
  paper/latex_gpt/supplementary.tex
```

**Result:** Only supplementary Table rows (b)–(f) match, and all are explicitly footnoted:
- Row (b): $^\dagger$Zone 3B (pre-fix, invalidated)
- Rows (c)–(f): $^\ddagger$Pre-fix diagnostic only

**Zero un-scrubbed zone 3B claims remain in any `.kimi_draft_v3` sidecar or selected paper canonical file.**

---

## Narrowed canonical scope statement

- **Sidecars (`.kimi_draft_v3`)** are canonical for integration: EN Ch4/5, CN Ch1/5/6/7.
- **Selected paper canonical files** are scrubbed: `01_introduction.tex`, `07_conclusion.tex`, `supplementary.tex`.
- **Original thesis `.tex` files with sidecars** are SUPERCEDED history; their headers now block ingestion.
- **Original thesis `.tex` files WITHOUT sidecars** (EN Ch1, EN Ch7, EN Ch8) remain ACTIVE but carry WARNING headers due to residual zone 3B content. These await Round-4 sidecar creation or direct rewrite.

---

## Required follow-up

1. **Codex/Gemini re-review** of the six fixes listed above.
2. **Claude signal** for integration of sidecars + selected paper canonical files.
3. **Round-4 dispatch** (gated on user signal or PhD data landing) to create sidecars for EN Ch1/Ch7/Ch8.

*End of broadcast.*
