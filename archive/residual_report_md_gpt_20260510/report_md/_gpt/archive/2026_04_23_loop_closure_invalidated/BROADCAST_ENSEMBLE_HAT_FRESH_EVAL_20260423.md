# Broadcast: Ensemble HAT Post-Fix Fresh Eval COMPLETE

**Date:** 2026-04-23 23:47 CST
**Experiment:** Ensemble HAT severe-NL (NL=2.0), post-fix clean code
**Checkpoint:** `checkpoints/_gpt/postfix_reruns/V4_hybrid_standard_noise_hat_best.pt` (epoch 10, best same-instance 81.72%)

---

## Fresh-Instance Eval Results (POST-FIX, CLEAN)

| Instance | Accuracy | Seed |
|:---|:---|:---|
| 1 | 80.09% | 42 |
| 2 | 82.11% | 142 |
| 3 | 81.66% | 242 |
| 4 | 81.77% | 342 |
| 5 | 82.49% | 442 |
| 6 | 81.32% | 542 |
| 7 | 82.40% | 642 |
| 8 | 81.80% | 742 |
| 9 | 81.57% | 842 |
| 10 | 81.74% | 942 |

**Statistics:**
- **Mean:** 81.69%
- **Std:** 0.64%
- **Range:** 80.09% -- 82.49%
- **Protocol:** 10 fresh D2D instances × 5 MC eval runs per instance

---

## Interpretation

**Ensemble HAT achieves near-perfect fresh-instance transfer under severe NL=2.0.**

Same-instance best: **81.72%**
Fresh-instance mean: **81.69%**
Gap: **0.03 percentage points** (within statistical noise)

Cross-instance std is only **0.64%**, indicating the epoch-resampled training distribution is broad enough to prevent hardware-instance overfitting.

---

## Comparison

| Configuration | Same-Instance | Fresh-Instance | Fresh Std |
|:---|:---|:---|:---|
| Pre-fix Standard HAT (NL=1.0, invalid) | ~91% | 10.00% | 0.00% |
| R1 Standard HAT (NL=1.0, post-fix) | 91.50% | 34.56% | 8.79% |
| **Ensemble HAT (NL=2.0, post-fix)** | **81.72%** | **81.69%** | **0.64%** |

**Conclusion:** Ensemble HAT solves the hardware-instance overfitting problem. Even under severe write nonlinearity (NL=2.0), fresh-instance transfer matches same-instance accuracy to within statistical noise.

---

## Next Steps

1. Codex cross-review of this result (in progress)
2. Standard HAT fresh eval (after it reaches platform)
3. Proportional-noise HAT training (in progress)
4. OPECT transfer eval (using this checkpoint)

---

*This result is from post-fix code (git HEAD 33bed9c) and is safe to cite.*
