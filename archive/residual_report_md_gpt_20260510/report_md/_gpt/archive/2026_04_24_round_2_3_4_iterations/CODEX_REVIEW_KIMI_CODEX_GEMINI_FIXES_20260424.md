# CODEX_REVIEW_KIMI_CODEX_GEMINI_FIXES_20260424
**Date:** 2026-04-24 22:27 CST
**Reviewer:** Codex
**Scope:** Kimi `BROADCAST_KIMI_CODEX_GEMINI_REVIEW_FIXES_20260425.md` and the files it claims to fix
**Verdict:** **Partial pass.** Kimi fixed most thesis/supplementary blockers, but main paper `05_results.tex` still contains unsafe deployment-fidelity ADC wording and remains the current hard blocker.

---

## Findings

### F1 - PASS - CN Chapter 7 energy error is fixed
Confirmed in `paper/thesis_cn/chapter_7_deployment.tex.kimi_draft_v3:35`--`42`:

- `65 pJ / 15.4x / energy_sensitivity_analysis.json` was replaced.
- New text uses `23.9 μJ`, `273.94 μJ` FP32 baseline, `11.45x` vs FP32, `2.86x` vs assumed INT8.
- It explicitly says this is a first-order analytical assumption, not silicon measurement.

This closes the Ch7 energy blocker raised by Gemini and Codex.

### F2 - PASS - EN/CN thesis ADC wording is materially improved
Confirmed:

- `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3:112` now says post-module-output hook diagnostic and states it is not a physical ADC boundary.
- `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3:183` table caption now marks ADC-on as diagnostic-only.
- `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3:205` says ADC-on numbers are hook diagnostics, not silicon-validated deployment values.
- `paper/thesis_cn/chapter_5_failure_modes.tex.kimi_draft_v3:115` now says 8bit ADC-on is a hook diagnostic and not physical ADC boundary.

Residual note: `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3:116` still says "8-bit ADC-on quantisation" in the quantitative paragraph, but the surrounding methodology/caption now qualifies the claim. This is acceptable if Claude wants concise thesis prose.

### F3 - PASS WITH CAVEAT - Supplementary groupwise-NL table is now marked historical/pre-fix
Confirmed:

- `paper/latex_gpt/supplementary.tex:774` now states groupwise protected rows are pre-fix diagnostic only, affected by config-sharing bug and pre-fix STE semantics, and must not support revised-recipe MLP-path localization.
- `paper/latex_gpt/supplementary.tex:784`--`787` now footnote old MLP/QKV/attn/all-linear rows with `^\ddagger`.
- `paper/latex_gpt/supplementary.tex:792` now says the pre-fix MLP-path localization does not carry over to the revised recipe.

Caveat: retaining old numbers is still reviewer-sensitive. It is now defensible only as a historical diagnostic table, not as main evidentiary support.

### F4 - HIGH - Main paper `05_results.tex` still has unsafe ADC deployment-fidelity claims
Kimi's broadcast did not include `paper/latex_gpt/sections/05_results.tex` in the actual fix list or expanded grep. The file still contains the exact problematic wording:

- `paper/latex_gpt/sections/05_results.tex:77` says deployment-fidelity quantization is injected via inference-time hooks calibrated once before the fresh-instance loop.
- `paper/latex_gpt/sections/05_results.tex:81` captions M-series headline numbers as deployment-fidelity 8-bit ADC-on.
- `paper/latex_gpt/sections/05_results.tex:97` says deployment-fidelity 8-bit ADC does not materially alter the headline.

This is now the primary hard blocker. The thesis sidecars are mostly aligned, but the main paper results section would still overclaim physical ADC fidelity if integrated/submitted as-is.

### F5 - MEDIUM - Kimi expanded grep gate remains incomplete
Kimi's expanded grep excludes `paper/latex_gpt/sections/05_results.tex`, which is precisely where the remaining hard blocker lives. Therefore the statement "zero un-scrubbed zone 3B claims remain in any selected paper canonical file" is not valid for the full paper package.

---

## Required Follow-Up

1. Patch `paper/latex_gpt/sections/05_results.tex:77`, `:81`, and `:97` with the same diagnostic-only wording used in EN Ch5.
2. Rerun grep including `paper/latex_gpt/sections/05_results.tex`.
3. Broadcast exact changed lines.

---

## Current Integration Ruling

- Thesis sidecars: close to integration-ready after Kimi's fixes, subject to Claude's choice on retaining historical tables.
- Supplementary: acceptable as historical diagnostic if the footnotes remain.
- Main paper: **not integration-ready** until `05_results.tex` ADC wording is patched.
