# K4R Fresh-Instance Evaluation Report

**Generated:** 1776880931.2076266
**Checkpoint:** `/home/qiaosir/projects/compute_vit/checkpoints/_gpt/cx_k4_alpha/k4_alpha_0p25/V4_hybrid_standard_noise_hat_k4_alpha_0p25_best.pt`
**Train best:** 91.62% (epoch 89)

## Configuration

| Parameter | Value |
|:----------|:------|
| Fresh instances | 10 |
| MC runs / instance | 5 |
| Dataset | cifar10 |
| Branch | A canonical (`ab56c2d`) |
| Group | `all` uniform-NL |
| Second-order α | 0.25 |

## Cross-Instance Summary

**34.99 ± 10.70%** across 10 fresh instances × 5 MC runs

## Comparison with Pre-Branch-A Baseline

| Metric | Pre-Branch-A `[INVALID]` | K4R (Branch A) |
|:-------|:-------------------------|:---------------|
| Fresh-instance mean | 86.37% [INVALID] | 34.99% |
| Fresh-instance std  | 1.54% [INVALID]  | 10.70% |
| Same-instance (V4)  | ~91.3%           | 91.62% (train best) |

> **Note:** The pre-Branch-A 86.37% figure was produced with incorrect second-order Taylor signs (positive `+0.5` instead of negative `-0.5`) and is **invalid** under Branch A semantics. K4R is the first canonical experiment.

## Instance-by-Instance Breakdown

| Instance | Seed | Mean Acc (%) | Std (%) | Min | Max |
|:---------|:-----|:-------------|:--------|:----|:----|
| 1 | 42 | 33.57 | 0.81 | 32.46 | 34.36 |
| 2 | 142 | 18.79 | 0.53 | 17.93 | 19.22 |
| 3 | 242 | 49.38 | 1.17 | 47.67 | 50.77 |
| 4 | 342 | 31.13 | 1.16 | 29.53 | 32.80 |
| 5 | 442 | 31.15 | 2.23 | 28.65 | 34.49 |
| 6 | 542 | 41.05 | 0.51 | 40.46 | 41.73 |
| 7 | 642 | 52.62 | 1.59 | 51.14 | 54.65 |
| 8 | 742 | 22.68 | 1.41 | 21.58 | 25.07 |
| 9 | 842 | 38.59 | 1.86 | 36.09 | 41.34 |
| 10 | 942 | 30.94 | 1.47 | 29.49 | 33.42 |

## Distribution Statistics

- **Mean of instance means:** 34.99%
- **Std of instance means:** 10.70%
- **Min instance mean:** 18.79%
- **Max instance mean:** 52.62%
- **Range:** 33.83 pp

## Interpretation

❌ **Result falls well below the pre-Branch-A nominal threshold.** The sign-corrected second-order brake may be too aggressive, or additional regularization (domain randomization, larger ensemble) may be needed.

## Recommended Next Steps

1. Compare with `group=mlp` diagnostic run to isolate NL sensitivity.
2. Sweep α ∈ {0.1, 0.25, 0.5, 1.0} to identify optimal brake strength.
3. If result < 85%, consider joint MLP-linear + Ensemble HAT training.
4. Archive this report and update `CODEX` with the canonical number.
