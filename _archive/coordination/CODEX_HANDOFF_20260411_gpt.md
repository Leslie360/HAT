# Codex Handoff Document - 2026-04-11

> Codex verification note (2026-04-11): this handoff correctly captured the issue families raised by the 4.10 reviewer batch, but it should no longer be treated as a live task board. P13 and several text/consistency fixes referenced below were completed after this file was written. See `KIMI_REVIEW_VERIFICATION_20260411_gpt.md` for the verified current state.

**From:** Kimi (K4)
**To:** Codex
**Subject:** New Reviewer Comments (4.10) - Action Required
**Priority:** HIGH

---

## Executive Summary

New batch of reviewer comments (4.10) received from 6 reviewers (kimi, deepseek, doubao, ds-txun, mimo, Qwen). **Consensus: Major Revision required.**

**Critical Gap:** Statistical rigor - core Tiny-ViT results rely on single-seed training, which is unacceptable for Nature Communications.

---

## Your Tasks (Codex)

### Task 1: Statistical Rigor - Multi-Seed Experiments [CRITICAL]

**Problem:** Core Tiny-ViT results (V4 canonical HAT, V4 Ensemble HAT, NL=2.0 stress test) based on seed=42 only.

**Required Action:**
1. Run Tiny-ViT experiments with seeds 42, 123, 2026:
   - V4 (canonical HAT)
   - V4_Ensemble_HAT
   - V4_NL2_HAT (stress test)
2. Report mean ± std across 3 seeds in Table 2
3. Update text to remove "still being accumulated" language

**Command Template:**
```bash
cd compute_vit
for seed in 42 123 2026; do
  python train_tinyvit.py --dataset cifar10 --experiment V4 --seed $seed ...
done
```

**ETA:** ~6-8 hours (3 experiments × 2 hours each)

---

### Task 2: Energy Model Transparency [HIGH]

**Problem:** ADC energy <0.1% conflicts with CIM literature; E_cell undefined.

**Required Action:**
1. Add to Methods or Fig 5 caption:
   - ADC architecture: SAR, 6-bit, 100 MS/s (assumed)
   - E_cell = 100 fJ per differential-pair MAC (cite source)
2. Add INT8 digital accelerator comparison (Edge TPU/NPU baseline)

**File:** `sections/03_methodology.tex` (energy model subsection)

---

### Task 3: AIHWKIT ViT Comparison [HIGH]

**Problem:** Only ResNet-18 comparison exists (Supplement 1.7).

**Required Action:**
1. Run Tiny-ViT V4 (canonical) in AIHWKIT:
   - Shared regime: 4-bit, σ_C2C=0.05, σ_D2D=0.1, 8-bit ADC
2. Compare accuracy vs our framework
3. Add to Supplementary Section 1.7

**ETA:** ~2-3 hours

---

### Task 4: Parameter Provenance Documentation [MEDIUM]

**Problem:** Canonical profile parameters lack quantitative justification.

**Required Action:**
1. Create new Supplementary subsection:
   - G_max/G_min = 10: extraction from Vincze 2025 Fig.X
   - σ_C2C = 5%: conversion from reported X% variation
   - σ_D2D = 10%: derivation from Y measurement
2. Add table showing literature → parameter mapping

**File:** `supplementary.tex` new subsection

---

### Task 5: Clarity Improvements [MEDIUM]

**Quick Fixes:**
1. Add V1-V8 definition table to main text (Section 4)
2. Fix Table 1 inconsistencies:
   - "98.06%" vs "97.48%" for Tiny-ViT CIFAR-10
   - Define asterisk (*) for 33.22%*
3. Fix reference years:
   - Vincze 2026 → 2025
   - Zhang 2026 → 2025
4. Remove hyphenation artifacts: "mathe-matical", "ampli-tude"

---

### Task 6: Scale Masking Quantitative Support [MEDIUM]

**Problem:** Scale masking presented as hypothesis, not proven mechanism.

**Required Action:**
Add quantitative analysis to Section 5.2:
- Show σ_noise (after scale recovery) < LSB/2 for 4-bit quantization
- Calculation: σ_C2C × (G_max-G_min) × scale_factor < Δ/2

---

## Updated Coverage Matrix

Add new issues to `REVIEWER_COVERAGE_MATRIX_gpt.md`:

| # | Issue | Reviewer | Status | Priority |
|:--:|:------|:---------|:------:|:--------:|
| 110 | Multi-seed validation for Tiny-ViT | deepseek, doubao, ds-txun | ⏳ | P0 |
| 111 | ADC architecture transparency | kimi, deepseek | ⏳ | P1 |
| 112 | E_cell value declaration | deepseek | ⏳ | P1 |
| 113 | AIHWKIT ViT comparison | deepseek, doubao | ⏳ | P2 |
| 114 | Canonical parameter provenance | ds-txun | ⏳ | P3 |
| 115 | V1-V8 notation table | kimi, deepseek | ⏳ | P4 |
| 116 | Scale masking quantitative proof | deepseek | ⏳ | P4 |
| 117 | Ensemble HAT overhead clarification | kimi | ⏳ | P5 |

---

## Communication Protocol

1. **Progress Updates:** Comment on this file with status
2. **Blockers:** Tag @Kimi immediately if experiments fail
3. **Completion:** Update coverage matrix and notify for review

## Files to Modify

1. `sections/05_results.tex` - Table 2 updates, scale masking analysis
2. `sections/03_methodology.tex` - Energy model details
3. `sections/04_experimental_setup.tex` - V1-V8 table
4. `supplementary.tex` - Parameter provenance, AIHWKIT comparison
5. `refs_gpt.bib` - Year corrections
6. `REVIEWER_COVERAGE_MATRIX_gpt.md` - New issues tracking

---

**@Kimi:** Ready for your execution, Codex. Prioritize Task 1 (multi-seed) as it requires compute time and is blocking.
