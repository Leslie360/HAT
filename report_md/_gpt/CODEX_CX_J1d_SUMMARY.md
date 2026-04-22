# CX-J1d Summary (Second-Order Taylor STE)
**Date:** 2026-04-21
**Executor:** Codex
**Status:** ✅ COMPLETE — AMBIGUOUS RESULT

---

## Experiment Configuration

| Parameter | Value |
|:---|:---|
| Name | `V4_hybrid_standard_noise_hat_second_order_ste` |
| Base config | V4 (hybrid, standard noise, Ensemble HAT) |
| Modification | Second-order Taylor-corrected STE in `StraightThroughQuantize.backward` |
| Protected group | MLP only (`fc1`, `fc2`) at `NL=1.0` |
| Unprotected groups | QKV, proj, patch_embed at `NL=2.0` |
| Delta-g_eff | 0.0 |
| Warm-start | From `V4_hybrid_standard_noise_hat_best.pt` (weights only) |
| Training | 100 epochs, AMP on |

---

## Training Results

| Metric | Value |
|:---|:---|
| Best test accuracy | **91.02%** @ epoch 78 |
| Final test accuracy (epoch 99) | 89.49% |
| Training time | ~3 hours (epoch rate ~1.8 min/epoch) |

**Key observation**: Training best (91.02%) significantly exceeds:
- MLP-only linearization fresh train best: ~87.79%
- Full-linearization fresh train best: ~87.49%
- Canonical Ensemble HAT (NL=1.0): ~97% (but this is the NL=1.0 baseline, not a fair comparison)

---

## Fresh-Instance Eval (10 × 5 MC)

| Metric | Value |
|:---|:---|
| **Cross-instance mean** | **41.53%** |
| **Cross-instance std** | **8.87%** |
| Range | 27.51% – 51.62% |
| Median | 43.90% |

### Per-instance results

| # | Seed | Mean Acc |
|:---:|:---:|:---:|
| 1 | 42 | 27.51% |
| 2 | 142 | 47.65% |
| 3 | 242 | 47.22% |
| 4 | 342 | 28.03% |
| 5 | 442 | 42.21% |
| 6 | 542 | 33.88% |
| 7 | 642 | **51.62%** |
| 8 | 742 | 44.59% |
| 9 | 842 | **50.99%** |
| 10 | 942 | 41.60% |

---

## Branch Decision

Per BROADCAST_FINAL_AUTONOMOUS_20260420 §1.2:

**Mean = 41.53% → 35–50% AMBIGUOUS ZONE**

- ⏸ **STOP GPU QUEUE**
- ❌ **Do NOT launch Tier-2 (J2/J3/J4)**
- 📝 Write `CODEX_J1D_AMBIGUOUS_REPORT.md`
- ⏳ **Await Friday 2026-04-24 18:00 Claude review**

---

## Files

- Checkpoint: `checkpoints/_gpt/second_order_ste/V4_hybrid_standard_noise_hat_second_order_ste_best.pt`
- JSON results: `report_md/_gpt/json_gpt/cx_j1d_fresh_eval.json`
- Training log: `logs/_gpt/cx_j1d_20260421.stdout`
- Eval log: `logs/_gpt/cx_j1d_fresh_eval_20260421.log`
- This summary: `report_md/_gpt/CODEX_CX_J1d_SUMMARY.md`
- Ambiguous report: `report_md/_gpt/CODEX_J1D_AMBIGUOUS_REPORT.md`
