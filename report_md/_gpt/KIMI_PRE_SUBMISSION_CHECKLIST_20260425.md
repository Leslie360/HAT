# Pre-Submission Checklist — Round-5 Post-Stage-2 State
**Date**: 2026-04-25
**Target**: Nature Electronics manuscript + Supplementary
**Canonical commit**: `9cdbe77`

## Code (Standing)

- [x] `analog_layers.py`: first-order `(...)^(NL-1)`, no multiplier ✅ `9cdbe77`
- [x] `analog_layers.py`: second-order `-0.5 * (nl-1) * (...)^(nl-2)` ✅ `9cdbe77`
- [x] `analog_layers.py`: NL-guard for `1 < NL < 2` ✅
- [x] `analog_layers.py`: AMP decorators `@custom_fwd` / `@custom_bwd` ✅
- [x] Test suite green: `test_analog_layers.py` (79) + `test_dual_bug_fix.py` (7) + `test_adc_perinstance_calibration.py` (1) + `test_groupwise_nl_wrapper.py` (9) = 96/96 ✅
- [x] All experiments run on `9cdbe77` or later ✅
- [ ] `COMPILE_PRECHECK.md` adopted as pre-compile workflow ⏳

## Paper — Numbers & Zone Discipline

- [x] `05_results.tex`: Table 1 Stage-2 per-instance numbers (81.89/80.37/80.64/80.67/80.37/81.04) ✅
- [x] `05_results.tex`: Zero zone-3B language (no 30%, 32%, ceiling) ✅
- [x] `05_results.tex`: ADC wording = "hook diagnostic" ✅
- [x] `chapter_5_mitigation.tex`: Stage-2 synced to 05_results.tex ✅
- [x] Cover letter v6: `[STAGE2_ADC_ENSEMBLE_HEADLINE]` resolved ✅
- [x] Ch7: `[PENDING_STAGE2_ADC_NUMBERS]` removed ✅
- [x] Supplementary: `tab:adc-nonideality` 81.87 confirmed as correct context (ADC gain ±5%) ✅
- [ ] `03_methodology.tex`: `eq:hat-ensemble` label added (Round-5 integration)
- [ ] `03_methodology.tex`: `subsec:methodology-nl` label added (Round-5 integration)

## Paper — Theory (Phase 1)

- [ ] §S.7 Higher-order corrections (~600 words)
- [ ] §S.8 PAC-Bayes generalization bound (~1200 words)
- [ ] §S.9 Flat minima / SAM connection (~900 words)
- [ ] §S.10 Limitations (~300 words)
- [ ] 6 new bib entries (Roberts 2022, Dziugaite 2017, Pérez-Ortiz 2021, Foret 2021, Keskar 2017, Andriushchenko 2022)
- [ ] `06_discussion.tex` theory paragraph drafted as `.kimi_draft`

## Paper — Compilation

- [x] `latexmk` produces `main.pdf` (19 pages, 460 KB) ✅
- [ ] Compile warnings = 0 (currently 4 undefined refs, Round-5 scope)
- [ ] Figure QA: all figures referenced, no orphans

## Pending Triggers

- [ ] 8×40GB cross-arch results integration (T1 trigger)
- [ ] Measured-D2D Supp Note S-HW population (T3 trigger)
- [ ] Hostile-review v2 pass (Round-7)
- [ ] Final `pdflatex` compile + figure QA pass
- [ ] Zenodo bundle preparation
- [ ] Reviewer + editor suggestion list
- [ ] PhD defense clearance for submission gate

## Removed / Stale

- [x] ~~K4R as canonical baseline~~ ❌ REMOVED (superseded by post-fix M-series)
- [x] ~~86.37% tagged `[INVALID]`~~ ❌ REMOVED (now zone 3A bug-immune, unchanged)
- [x] ~~`ab56c2d` canonical commit~~ ❌ REMOVED (superseded by `9cdbe77`)
- [x] ~~Pre-Branch-A narrative~~ ❌ REMOVED
