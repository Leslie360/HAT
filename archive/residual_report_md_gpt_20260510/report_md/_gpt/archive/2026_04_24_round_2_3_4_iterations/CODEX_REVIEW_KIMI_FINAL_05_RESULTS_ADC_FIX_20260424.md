# CODEX_REVIEW_KIMI_FINAL_05_RESULTS_ADC_FIX_20260424
**Date:** 2026-04-24 22:31 CST
**Reviewer:** Codex
**Scope:** Kimi final patch to `paper/latex_gpt/sections/05_results.tex` after `CODEX_REVIEW_KIMI_CODEX_GEMINI_FIXES_20260424.md`
**Verdict:** **PASS. Remaining hard blocker cleared.**

---

## Findings

### F1 - PASS - Main paper `05_results.tex` ADC wording is now diagnostic-only
Confirmed fixes:

- `paper/latex_gpt/sections/05_results.tex:77` now says post-module-output hook diagnostic quantization is injected via inference-time hooks and adds that ADC-on numbers are inference-time hook diagnostics, not silicon-validated deployment values.
- `paper/latex_gpt/sections/05_results.tex:81` now captions headline numbers as post-module-output hook diagnostic 8-bit ADC quantization and explicitly warns not to treat ADC-on values as deployment-fidelity until physical ADC boundary and per-instance calibration are implemented.
- `paper/latex_gpt/sections/05_results.tex:97` now says post-module-output hook diagnostic ADC does not materially alter the headline and repeats that ADC-on values are hook diagnostics, not silicon-validated deployment values.

This resolves the last hard blocker from `CODEX_REVIEW_KIMI_CODEX_GEMINI_FIXES_20260424.md`.

### F2 - PASS - Prior Kimi fixes remain intact
Spot checks confirm the previously accepted fixes remain present:

- CN Ch7 energy now uses `23.9 μJ`, `273.94 μJ` FP32 baseline, `11.45x` vs FP32, and `2.86x` vs assumed INT8.
- EN/CN thesis Ch5 ADC wording remains diagnostic-only.
- Supplementary groupwise-NL rows remain marked historical/pre-fix with `^\ddagger` and are no longer presented as revised-recipe evidence.

### F3 - CAVEAT - The word `deployment-fidelity` still appears only in negated caveats
The package still contains phrases like "should not be treated as deployment-fidelity". This is acceptable and desirable as a safety caveat. The unsafe positive claims have been removed from the checked files.

---

## Integration Ruling

- Main paper `05_results.tex`: **integration-ready on the ADC wording issue**.
- Thesis sidecars: **integration-ready on the previously flagged energy/ADC/groupwise issues**, subject to Claude's broader thesis integration policy.
- Supplementary groupwise table: acceptable as a historical diagnostic table, with footnotes retained.

---

## No Further Codex Blocker

As of this review, Codex has no remaining blocker on Kimi's latest energy/ADC/groupwise fixes. Claude can proceed with integration review, while preserving the diagnostic-only ADC caveats.
