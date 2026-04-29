# Next Steps: Round R11 Completion & Paper Integration

**Date:** 2026-04-27
**Status:** R11 experiments complete, paper integration pending

---

## Completed Experiments (R11 Round)

| Experiment | Result | Status |
|-----------|--------|--------|
| R10E (8-bit baseline, IdealDevice) | 87.28 ± 0.13% | ✅ canonical |
| R11D-1 (4-bit AIHWKit) | 14.64 ± 0.11% | ✅ collapses |
| R11D-2 (σ=0.20 AIHWKit) | 87.52 ± 0.05% | ✅ robust |
| R11D-3 (σ=0.30 AIHWKit) | 87.40 ± 0.05% | ✅ robust |
| R11D-4 PCM (AnalogSGD, PCMPresetUnitCell) | 61.10% train, 60.85 ± 0.17% fresh | ✅ complete |
| Ensemble HAT (4-bit, 3-seed) | 86.16 ± 0.19% | ✅ canonical |

---

## Pending Tasks (Priority Order)

### Task 1: R11D-4 PCM Paper Integration [HIGHEST]
**Goal:** Integrate PCM training/eval results into manuscript.

**Required edits:**
1. `paper/latex_gpt/sections/05_results.tex` — add R11D-4 PCM results paragraph (~100 words)
   - Training: 61.10% (100 epochs, AnalogSGD + PCMPresetUnitCell)
   - Fresh eval: 60.85 ± 0.17% (10 instances, D2D stable)
   - Drift eval: 60.83% → 61.07% → 60.56% (0s/1h/24h, drift negligible)
   - Contrast with R10E 87.28% to show PCM non-linearity penalty
2. `paper/latex_gpt/supplementary.tex` — add PCM comparison table
   - Rows: IdealDevice 8-bit / PCM 8-bit / Ensemble HAT 4-bit
   - Columns: Training best / Fresh mean / Fresh std / Drift impact
3. `paper/latex_gpt/sections/06_discussion.tex` — extend AIHWKit comparison paragraph
   - Note PCM pulse-update physics as orthogonal stress axis
   - Frame finding: PCM training collapse (~26 pp gap) vs inference stability
4. `paper/latex_gpt/cover_letter.tex` — add 1 sentence on PCM realism

**Compile gate:** `latexmk -pdf main.tex` RC 0, zero undefined refs.

---

### Task 2: R11D-5 PCM Hyperparameter Sweep [MEDIUM]
**Goal:** Attempt to improve PCM training accuracy via LR/momentum tuning.

**Rationale:** R11D-4 achieved 61.10% with lr=5e-4, momentum=0. Literature suggests AnalogSGD benefits from higher LR for PCM devices.

**Experiments:**
| Run | LR | Momentum | Optimizer | Expected Time |
|-----|-----|----------|-----------|---------------|
| R11D-5a | 1e-3 | 0.0 | AnalogSGD | ~1.8h |
| R11D-5b | 5e-3 | 0.0 | AnalogSGD | ~1.8h |
| R11D-5c | 1e-3 | 0.9 | AnalogSGD | ~1.8h |

**Decision rule:** If any run exceeds 70% test accuracy, run fresh + drift eval. If all ≤ 65%, report negative result and conclude PCM pulse-update physics fundamentally limits ViT accuracy regardless of hyperparameters.

---

### Task 3: Paper Figure/Table Consolidation [HIGH]
**Goal:** Update all figures and tables to include complete R11D results.

**Checklist:**
- [ ] Main text Fig 1-3: verify no broken refs
- [ ] Supplementary Fig S3-S8: verify captions match R11D data
- [ ] Table in supp: 4-row comparison (Standard HAT / AIHWKit 8-bit / AIHWKit 4-bit / Ensemble HAT 4-bit) — already exists, verify R11D-1 number
- [ ] New table: PCM vs IdealDevice comparison (Task 1 output)
- [ ] `fig11_energy_breakdown.pdf` — either has ref or move to deprecated

**Verification:** `latexmk -pdf supplementary_main.tex` RC 0.

---

### Task 4: Final Compile & Submission Prep [HIGH]
**Goal:** Produce clean build for Nature Electronics submission.

**Checklist:**
- [ ] `latexmk -pdf main.tex` RC 0, zero undefined refs
- [ ] `latexmk -pdf supplementary_main.tex` RC 0, zero undefined refs
- [ ] Main body word count ≤ 5,700
- [ ] All locked numbers verified (22/22)
- [ ] Banned wording scan clean
- [ ] Cover letter compiles
- [ ] Submission bundle: main.pdf + supp.pdf + cover_letter.pdf

---

## Recommendation

**Start with Task 1 (R11D-4 PCM Paper Integration).** Data is ready, GPU is free, and this is the last substantive content gap before submission. Task 2 (hyperparameter sweep) is optional — 61.10% is already a meaningful finding for the paper.

**Pipeline task file:** `tasks/r11d4_pcm_paper_integration.md`
