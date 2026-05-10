<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Pre-Submission Checklist — Branch A Canonical

**Date**: 2026-04-23  
**Target**: Paper + Thesis + Defense materials

## Code

- [ ] `ab56c2d` is the canonical commit
- [ ] `analog_layers.py`: first-order `(...)^(NL-1)`, no multiplier
- [ ] `analog_layers.py`: second-order `-0.5 * nl * (nl-1)`
- [ ] `run_tinyvit_groupwise_nl_comp.py`: auto δg_eff from module config
- [ ] All experiments run on `ab56c2d` or later
- [ ] No `c3dbeb3` (multiplier commit) in experiment history

## Paper (`paper/latex_gpt/`)

- [ ] `01_intro.tex`: No pre-Branch-A numbers cited as canonical
- [ ] `03_methodology.tex`: Equation S2 explanation matches Branch A
- [ ] `05_results.tex`: All 86.37% tagged `[INVALID]` or removed
- [ ] `05_results.tex`: K4R result inserted as canonical fresh-instance baseline
- [ ] `06_discussion.tex`: 86.37% tagged `[INVALID]`
- [ ] `08_appendix.tex`: Sensitivity sweep tagged `[INVALID]`
- [ ] Supplementary: No K-series / parity probes / MLP-linearized cited as canonical
- [ ] All `[INVALID]` / `[PENDING]` tags converted to comments or removed before submission
- [ ] `
- [ ] `main.tex`: `
- [ ] Compile clean (no errors)

## Thesis (`paper/thesis/`)

- [ ] `chapter_1_hat_instance_overfitting.tex`: 86.37% / 86.33% tagged `[INVALID]`
- [ ] `chapter_1_hat_instance_overfitting.tex`: 32.60% / 87.79% tagged `[INVALID]`
- [ ] `chapter_5_mitigation.tex`: Stub expanded or removed
- [ ] `chapter_6_physical_realism.tex`: Stub expanded or removed
- [ ] `chapter_7_deployment.tex`: Stub expanded or removed
- [ ] `chapter_8_outlook.tex`: Stub expanded or removed
- [ ] All chapters compile clean

## Defense

- [ ] Beamer slides compile to PDF
- [ ] All `[INVALID]` tags preserved in speaker notes
- [ ] Timing table matches 45-min slot
- [ ] Visual placeholders replaced with actual figures

## Public Comms

- [ ] Blog draft: No pre-Branch-A numbers as canonical
- [ ] FAQ: K4R marked pending (update when result arrives)
- [ ] Both documents proofread

## Data & Reproducibility

- [ ] All JSON eval outputs archived
- [ ] Checkpoint metadata includes `git_commit`, `nl_ltp`, `nl_ltd`, `use_second_order_ste`
- [ ] `scripts/_gpt/launch_cx_k4r_fresh_eval.sh` reproducible
- [ ] README updated with Branch A setup instructions
