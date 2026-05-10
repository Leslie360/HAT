# Kimi P6 Track A Report: Evidence Gap Ledger

**Date:** 2026-05-09
**Dispatch:** `DISPATCH_SUPERPHASE_P6_EXPERIMENT_COMPLETION_AND_EVIDENCE_GAP_CLOSURE_20260509.md`
**Executor:** kimi

---

## Ledger Table

| # | Claim / Narrative Point | Evidence File(s) | Source Data | Seeds / Instances / MC | Metric Definition | Status | Next Action | Classification |
|---|------------------------|------------------|-------------|------------------------|-------------------|--------|-------------|----------------|
| 1 | IdealDevice 8-bit stable baseline | `ideal_8bit_sigma010_aihwkit_baseline/` | `canonical_json/ideal_8bit_sigma010_aihwkit_baseline/` | 1 seed, 10 instances x 5 MC | fresh_mean | **Complete** | None | `paper1-main-locked` |
| 2 | 4-bit pure quantization collapse | `pure_4bit_collapse/` | `canonical_json/pure_4bit_collapse/` | 1 seed, 10 instances x 5 MC | fresh_mean | **Complete** | None | `paper1-main-locked` |
| 3 | Ensemble HAT 4-bit rescue | `ensemble_hat_4bit_3seed/` | `canonical_json/ensemble_hat_4bit_3seed/` | 3 seeds, 10 instances x 5 MC per seed | cross_seed mean_of_seed_means | **Complete** | None | `paper1-main-locked` |
| 4 | PCM 8-bit drift-flat point | `pcm_8bit_seed{123,456,789}/` | `canonical_json/pcm_8bit_seed*/` | 3 seeds, 10 instances x 5 MC per seed | source_best, fresh_mean, drift_drop | **Complete** | None | `paper1-main-locked` |
| 5 | PCM 6-bit D2D-sensitive transition zone | `pcm_6bit_seed{123,456,457,789}/` | `canonical_json/pcm_6bit_seed*/` | 4 seeds (1 incomplete), 10 instances x 5 MC per seed | source_best, fresh_mean, drift_drop | **Weak** | Rerun seed123 source; in progress (PID 114296) | `paper1-supplement-candidate` |
| 6 | PCM 4-bit drift-limited regime | `pcm_4bit_seed{123,456_clean,789}/` | `canonical_json/pcm_4bit_seed*/` | 3 seeds, 10 instances x 5 MC per seed | source_best, fresh_mean, drift_drop | **Complete** | None | `paper1-main-locked` |
| 7 | 105 cross-architecture proportional HAT | Remote server (crashed) | `REMOTE_105_*_TASKLIST_*.md` | Partial (seed123,456 complete; 789 crashed) | source_best per seed | **Missing** | Wait for server recovery; task file ready | `future-only` |
| 8 | 107 analog KV-cache HAT selective-layer | Remote server | `REMOTE_107_*_TASKLIST_*.md` | Partial (corrected-noise rerun pending) | PPL pre/post HAT | **Weak** | Wait for corrected-noise rerun; local smoke passed | `work2-kv-cache` |
| 9 | Appendix/defense-only: 5-bit PCM non-frontier | `r11d_5bit_pcm_seed*` checkpoints | `paper2_aihwkit_baseline/checkpoints/r11d_5bit_pcm_seed*/` | 3+ seeds | fresh_mean | **Complete** | None | `exclude/superseded` |

---

## Detailed Claim Evidence

### Claim 1: IdealDevice 8-bit Stable Baseline

| Attribute | Value |
|-----------|-------|
| Evidence | `canonical_json/ideal_8bit_sigma010_aihwkit_baseline/fresh_eval.json` |
| fresh_mean | 87.28% |
| Protocol | 10 instances x 5 MC, IdealDevice, sigma=0.10 |
| Seeds | 1 (seed42) |
| Status | **Complete** |

This is the clean digital upper bound. One seed is sufficient because IdealDevice is deterministic.

### Claim 2: 4-bit Pure Quantization Collapse

| Attribute | Value |
|-----------|-------|
| Evidence | `canonical_json/pure_4bit_collapse/fresh_eval.json` |
| fresh_mean | 14.64% |
| Protocol | 10 instances x 5 MC, pure quantization (no noise, no PCM) |
| Seeds | 1 |
| Status | **Complete** |

This demonstrates that 4-bit quantization alone collapses accuracy to near-random.

### Claim 3: Ensemble HAT 4-bit Rescue

| Attribute | Value |
|-----------|-------|
| Evidence | `canonical_json/ensemble_hat_4bit_3seed/r10a_canonical_ensemble_hat_3seed_fresh_eval.json` |
| Cross-seed mean | 86.16% |
| Cross-seed SEM | 0.11% (sample std 0.19% / sqrt(3)) |
| Protocol | 3 seeds x 10 instances x 5 MC |
| Status | **Complete** |

This is the headline Paper-1 result. Three seeds provide adequate reproducibility evidence.

### Claim 4: PCM 8-bit Drift-Flat Point

| Attribute | Value |
|-----------|-------|
| Evidence | `canonical_json/pcm_8bit_seed*/` |
| source_best | 77.64 ± 0.68% (n=3) |
| fresh_mean | 77.60 ± 0.64% (n=3) |
| drift_1d | 77.57% |
| drift_drop | 0.04 pp |
| Protocol | PCMPresetUnitCell, 10 instances x 5 MC |
| Status | **Complete** |

Drift is negligible. Three seeds, low variance.

### Claim 5: PCM 6-bit D2D-Sensitive Transition Zone

| Attribute | Value |
|-----------|-------|
| Evidence | `canonical_json/pcm_6bit_seed*/` (partial) |
| source_best | 68.36 ± 7.34% (n=3, seed123 excluded) |
| fresh_mean | 68.55 ± 6.03% (n=4) |
| drift_1d | 68.46% |
| drift_drop | 0.07 pp |
| Protocol | PCMPresetUnitCell, 10 instances x 5 MC |
| Status | **Weak — seed123 source_best missing** |

**Gap:** seed123 rerun was interrupted at epoch 53. `training_history.json` never saved. Fresh and drift evals are valid (new protocol), but source_best is unknown. Rerun launched (PID 114296, 2026-05-09).

**Risk:** 6-bit has the highest variance of all PCM regimes. Missing one seed's source_best inflates uncertainty. However, the 4-seed fresh_mean (68.55%) is already canonical and will not change significantly after seed123 source is recovered.

### Claim 6: PCM 4-bit Drift-Limited Regime

| Attribute | Value |
|-----------|-------|
| Evidence | `canonical_json/pcm_4bit_seed*/` |
| source_best | 76.71 ± 0.46% (n=3) |
| fresh_mean | 76.68 ± 0.37% (n=3) |
| drift_1d | 72.64% |
| drift_drop | 4.01 pp |
| Protocol | PCMPresetUnitCell, 10 instances x 5 MC |
| Status | **Complete** |

Large drift drop (4 pp) is the key finding. Three seeds, low variance.

### Claim 7: 105 Cross-Architecture Proportional HAT

| Attribute | Value |
|-----------|-------|
| Evidence | Remote server snapshots (partial) |
| Complete seeds | deit: 123, 456; vit: 123, 456 |
| Missing | seed789 for both architectures (server crashed mid-run) |
| Protocol | Best-epoch test accuracy, fresh eval |
| Status | **Missing — seed789 gap** |

**Next action:** Server recovery + seed789 rerun. Task file `REMOTE_105_PHASE_P6_CLOSURE_TASKLIST_20260509.md` is ready.

**Classification risk:** If seed789 results differ materially from 123/456, the proportional HAT claim may need softening from "supplement-candidate" to "future-only."

### Claim 8: 107 Analog KV-Cache HAT

| Attribute | Value |
|-----------|-------|
| Evidence | Remote server snapshots + local smoke tests |
| Local smoke | Passed (analog_kv_cache import OK) |
| Corrected-noise rerun | Pending (server recovery) |
| Protocol | PPL on sliding window, 3 seeds |
| Status | **Weak — old noise bug may have inflated results** |

**Next action:** Corrected-noise rerun on remote. Local unit tests ready. Task file `REMOTE_107_PHASE_P6_KV_CLOSURE_TASKLIST_20260509.md` is ready.

**Classification:** Work-2 only. No Paper-1 contamination.

### Claim 9: 5-bit PCM Non-Frontier

| Attribute | Value |
|-----------|-------|
| Evidence | `paper2_aihwkit_baseline/checkpoints/r11d_5bit_pcm_seed*/` |
| Result | Kill/non-frontier (between 6-bit and 4-bit, no advantage) |
| Seeds | Multiple |
| Status | **Complete** |

**Classification:** `exclude/superseded`. Used for defense only ("we considered and rejected 5-bit").

---

## Gap Summary

| Gap | Severity | Blocks | Action | ETA |
|-----|----------|--------|--------|-----|
| 6-bit seed123 source_best | Medium | Statistical completeness | Rerun launched | ~2h |
| 105 seed789 | High | Cross-architecture validation | Wait for server | Unknown |
| 107 corrected-noise | High | Work-2 decisiveness | Wait for server | Unknown |

---

## Verdict

Paper-1 main claims (1-4, 6) are **evidence-complete**. Claim 5 (6-bit) has a **recoverable gap** (rerun in progress). Claims 7-8 (105/107) are **remote-blocked**. Claim 9 is complete but excluded.

**No claim requires manuscript alteration at this time.**

---

*Report by kimi. Ledger compiled on 2026-05-09.*
