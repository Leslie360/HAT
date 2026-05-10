<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# K4R Interim Analysis — Epoch 74/100

**Generated**: 2026-04-23
**Log parsed**: `logs/_gpt/cx_k4r_alpha_0p25_20260422_231615.log`

## Training Curve Summary

| Metric | Value | Epoch |
|:-------|:------|:------|
| Train best acc | 99.59% | 74 (current) |
| Test best acc | 91.20% | 69 |
| Current test acc | 90.64% | 74 |
| Generalization gap | 8.95 pp | — |

## Observations

1. **Plateau detected**: Last 10 epochs test std = 0.48%. The model has converged on the held-out test set.
2. **No overfitting collapse**: Train acc continues to rise (99.59%) but test acc holds steady ~90.6–91.2%. No degradation.
3. **Best epoch was 69**: Test acc peaked at 91.20% and has not improved in the last 5 epochs.

## Fresh-Instance Forecast

Based on V4 behavior:
- V4 train best: ~91.1%
- V4 same-instance MC: ~91.3%
- V4 fresh-instance: 10.00% (fixed-mask overfitting)

K4R uses Ensemble HAT (per-epoch D2D resampling) + second-order brake (α=0.25).
Expected fresh-instance mean:

| Scenario | Fresh-instance mean | Basis |
|:---------|:--------------------|:------|
| Optimistic | 88–91% | Second-order brake helps; ensemble training prevents overfitting |
| Nominal | 85–88% | Brake is neutral; ensemble effect dominates |
| Pessimistic | 80–85% | Brake is slightly harmful; some accuracy loss vs. pre-Branch-A |
| Failure | <80% | Brake is strongly harmful or ensemble insufficient |

**Most likely**: 85–90% range. The second-order brake with α=0.25 is mild enough that it should not catastrophically degrade transfer, but the sign correction (negative = brake) may shave 1–3 pp relative to a first-order-only ensemble.

## Decision Preview

| Fresh-instance result | P1 Path | Rationale |
|:----------------------|:--------|:----------|
| ≥ 88% | P1-A (parity) | Sign-corrected brake is benign or helpful |
| 85–88% | P1-A/B (near parity) | Marginal effect; sweep α to optimize |
| 80–85% | P1-B (near parity) | Brake is slightly harmful; tune down |
| < 80% | P1-C (degradation) | Brake is too aggressive; revisit theory |

## Recommendations

1. **Do not stop training early**: Even though test acc plateaued at epoch 69, the fresh-instance protocol may benefit from later-epoch checkpoints if ensemble diversity improves. The auto-eval will use `*_best.pt`, which is epoch 69.
2. **Monitor for divergence**: If test_acc drops below 89% in final epochs, consider using epoch 69 checkpoint instead of epoch 100.
3. **Reserve GPU**: Do not launch other experiments until fresh-instance eval completes (~40 min eval after training finishes).
