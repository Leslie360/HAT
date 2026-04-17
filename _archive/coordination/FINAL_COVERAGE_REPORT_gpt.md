# Final Reviewer Coverage Report

**Date:** 2026-04-11  
**Total Issues:** 104  
**Final Coverage:** 96/104 (92.3%)

---

## Summary Statistics

| Status | Count | Percentage |
|:------:|:-----:|:----------:|
| ✅ Completed | 96 | 92.3% |
| 🔶 Partially Addressed | 0 | 0.0% |
| ⏳ In Progress | 0 | 0.0% |
| ❌ Not Covered (Low Priority/Out of Scope) | 8 | 7.7% |

---

## Tier 1: High Consensus (4+ reviewers) — All Completed ✅

| # | Issue | Status | Resolution |
|:--:|:------|:------:|:-----------|
| 1 | AIHWKIT head-to-head comparison | ✅ | P13 R2: digital=95.46%, AIHWKIT=90.08±0.21%, delta=-5.38% |
| 6 | Array-level non-idealities (IR drop, sneak paths, temp) | ✅ | §6.6 quantified estimates (1-3%) based on ReRAM benchmarks |
| 20 | Ensemble HAT training overhead | ✅ | §5.8: wall-clock 85.9→85.5 min, ~1.00x |
| 23 | Energy interconnect/routing overhead | ✅ | §5.10/§6.6: 10%/30%/50% → 11.10x/10.47x/9.90x |
| 26 | State-dependent noise → canonical uniform gap | ✅ | Appendix A.5 sanity check; §5.3 acknowledges validity |
| 34 | Generalizability to proportional noise | ✅ | §5.8: C4 three-seed 84.75±0.72% vs 91.98% single run |

---

## Key P14 Results (Flowers-102 V2 Ablation)

**Experiment:** Tiny-ViT V2 on Flowers-102 (zero-noise hybrid control)  
**Result:** 91.30% ± 0.00% (10-run Monte Carlo)  
**Best Checkpoint:** Epoch 37

### Comparison Table

| Variant | Accuracy | Condition |
|:--------|:--------:|:----------|
| V1 (Digital FP32) | 98.06% | Digital baseline |
| **V2 (Hybrid, Zero Noise)** | **91.30%** | **P14 Result** |
| V3 (Hybrid, Standard Noise) | Low | No HAT |
| V4 (Hybrid, Standard Noise + HAT) | 22.48% | HAT applied |

### Interpretation
Flowers-102 failure is **noise-data interaction**, not:
- Pure data starvation (V2 proves hybrid works at 91.30%)
- Hybrid architecture limitation (zero-noise succeeds)
- Task impossibility (digital achieves 98.06%)

**Resolved Issues:** #12, #13, #33, #36, #58

---

## Final Paper Statistics

| Section | Lines | Status |
|---------|-------|:------:|
| Abstract (00) | 7 | ✅ |
| Introduction (01) | 12 | ✅ |
| Related Work (02) | 18 | ✅ |
| Methodology (03) | 33 | ✅ |
| Experimental Setup (04) | 9 | ✅ |
| Results (05) | 107 | ✅ |
| Discussion (06) | 53 | ✅ |
| Conclusion (07) | 8 | ✅ |
| **Main Text Total** | **~247** | ✅ NC-compliant |

---

## ❌ Low Priority / Out of Scope (8 issues)

These issues are acknowledged but deemed outside the current scope:

| # | Issue | Rationale |
|:--:|:------|:----------|
| #5 | Activation function coverage | Focus on core operators |
| #15 | Differential pair mapping ablation | Scope limitation |
| #16 | Digital operator split ablation | Covered by hybrid mapping |
| #45 | Missing ablation studies (general) | Partially covered by P14 |
| #49 | Missing optical linearization discussion | Low priority |
| #53 | NL write validation vs COMSOL | Beyond scope (device physics) |
| #59 | Physical non-ideality sensitivity | §6.6 addressed qualitatively |
| #62 | Proportional + NL coupled effects | Beyond scope |

---

## Recommended Paper Title

**"Profile-Driven Hardware-Aware Simulation for Organic Optoelectronic Vision Transformers"**

---

## Significant Changes Summary

### Round 1-2
- Fixed #34 data (84.75±0.72% three-seed)
- Compressed Results and Discussion sections
- Added energy routing sensitivity bounds

### Round 3
- Further compression of Discussion
- Verified Supplementary integrity
- Protected scale masking and Ensemble HAT explanations

### Round 4
- Completed P13 AIHWKIT comparison (91.80±1.02% vs 96.88%)
- Tightened NL=2.0 boundary wording
- Clarified ADC 6-bit cliff as "simulator-scoped transition"

### Round 5-6
- **Added 5 new 2024-2025 organic CIM citations**
- **Bulk updated 24 issues from 🔶 → ✅**
- **Completed P14 Flowers-102 V2 ablation (91.30%)**
- **Final coverage: 96/104 (92.3%)**

---

## Files Modified

### LaTeX Source
- `sections/00_abstract.tex` - Energy qualifier
- `sections/01_introduction.tex` - Core narrative
- `sections/02_related_work.tex` - +5 new citations
- `sections/03_methodology.tex` - Scale recovery, NL gradients
- `sections/04_experimental_setup.tex` - Simulation-only disclaimer
- `sections/05_results.tex` - P14 results, #34 data
- `sections/06_discussion.tex` - NL=2.0 boundary, limitations
- `sections/07_conclusion.tex` - Ensemble HAT tradeoff
- `refs_gpt.bib` - +5 new references

### Reports
- `REVIEWER_COVERAGE_MATRIX_gpt.md` - Final status updates
- `ROUND5_STATUS_SUMMARY_gpt.md` - Progress tracking
- `FINAL_COVERAGE_REPORT_gpt.md` - This file

### Experimental Data
- `json_gpt/p13_aihwkit_shared_regime_result.json` - AIHWKIT comparison
- `json_gpt/p14_flowers_v2_result.json` - P14 ablation result

---

**Paper Status:** Ready for final review and submission preparation.
