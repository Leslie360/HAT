# R11D Extended Drift Curve Summary

**Date:** 2026-04-29
**Status:** Extended drift complete (all 6 runs x 10 time points). Fresh+drift in progress.

---

## Extended Drift Curves (10 time points: 0s to 3d)

### 4-bit PCM

| Time | seed123 | seed456 | seed789 | Mean | Std |
|:---|---:|---:|---:|---:|---:|
| 0s | 76.59% | 77.04% | 76.27% | 76.63% | 0.39pp |
| 600s | 75.59% | 74.96% | 74.93% | 75.16% | 0.37pp |
| 1800s | 74.87% | 74.14% | 74.30% | 74.44% | 0.37pp |
| 1h | 74.54% | 73.72% | 74.25% | 74.17% | 0.42pp |
| 3h | 73.86% | 72.94% | 74.25% | 73.68% | 0.66pp |
| 6h | 73.33% | 72.33% | 74.05% | 73.24% | 0.86pp |
| 12h | 72.79% | 72.22% | 73.56% | 72.86% | 0.67pp |
| 1d | 72.05% | 72.29% | 73.47% | 72.60% | 0.78pp |
| 2d | 71.51% | 71.83% | 73.69% | 72.34% | 1.12pp |
| 3d | 71.31% | 71.49% | 72.76% | 71.85% | 0.81pp |

**4-bit drift drop (0s -> 3d): 4.78pp**

### 8-bit PCM

| Time | seed123 | seed456 | seed789 | Mean | Std |
|:---|---:|---:|---:|---:|---:|
| 0s | 76.95% | 78.32% | 77.54% | 77.60% | 0.69pp |
| 600s | 76.93% | 78.10% | 77.47% | 77.50% | 0.59pp |
| 1800s | 76.98% | 78.17% | 77.41% | 77.52% | 0.63pp |
| 1h | 77.07% | 78.20% | 77.60% | 77.62% | 0.57pp |
| 3h | 77.11% | 78.34% | 77.47% | 77.64% | 0.63pp |
| 6h | 77.08% | 78.10% | 77.55% | 77.58% | 0.51pp |
| 12h | 76.88% | 78.17% | 77.51% | 77.52% | 0.65pp |
| 1d | 77.02% | 78.18% | 77.47% | 77.56% | 0.58pp |
| 2d | 76.85% | 78.33% | 77.50% | 77.56% | 0.74pp |
| 3d | 77.22% | 78.28% | 77.60% | 77.70% | 0.53pp |

**8-bit drift drop (0s -> 3d): -0.10pp** (essentially flat, within noise)

---

## Key Observations

1. **4-bit PCM degrades monotonically** with log(time) from ~76.6% → ~71.9%. The curve is smooth and consistent across all 3 seeds.

2. **8-bit PCM is drift-immune** across the entire 3-day window. Variations (~±0.5pp) are within single-evaluation measurement noise.

3. **The 4-bit vs 8-bit gap widens from ~0.9pp (fresh) to ~5.8pp (3d)**. This is the core precision-drift trade-off that must be discussed in the paper.

4. **Fresh+drift eval (first result - seed123)**:
   - t=0s: 76.66% ± 0.03% (5 fresh instances, 3 MC repeats each)
   - t=1h: 74.41% ± 0.07%
   - t=1d: 72.22% ± 0.08%
   - Instance-level std is tiny (<0.1pp), confirming PCM model determinism given fixed seed.

---

## Narrative Impact

The extended drift data strengthens the paper's key claim:

> "PCM device physics enable 4-bit training, but precision-drift trade-off must be explicitly quantified."

- Figure opportunity: Extended drift curves (log time axis) showing 4-bit degradation vs 8-bit flat line
- Table opportunity: Summary statistics at 0s, 1h, 24h, 72h for both precisions
- Discussion opportunity: Why 8-bit is drift-immune (higher resolution = smaller relative drift), and whether re-calibration / periodic refresh can close the 4-bit gap
