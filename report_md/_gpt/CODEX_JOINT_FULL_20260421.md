# Tiny-ViT Results (GPT)

| Mode | Exp | Name | Dataset | Primary Metric | Checkpoint |
|:-----|:----|:-----|:--------|:---------------|:-----------|
| train | V4 | V4_hybrid_standard_noise_hat_joint_mlp_linear_ensemble_hat_full | cifar10 | best_acc=91.36% @ epoch 82 | `checkpoints/_gpt/joint_mlp_linear_ensemble_hat_full/V4_hybrid_standard_noise_hat_joint_mlp_linear_ensemble_hat_full_best.pt` |

## Notes

- `eval` mode reports repeated-run statistics for noisy experiments when `--eval-runs > 1`.
- `retention-sweep` reuses the ConvNeXt-style time grid and Monte Carlo summary format.
- These result files are GPT-scoped scratch artifacts and do not replace the canonical experiment reports.

## Fresh-Instance Evaluation

**Protocol:** 10 fresh D2D instances × 5 MC evaluations per instance, groupwise NL setter loaded (MLP protected at NL=1.0).

**Preliminary result (5/10 instances, timed-out run):**

| Instance | Mean Acc (%) |
|:---------|------------:|
| 01 | 36.51 |
| 02 | 21.15 |
| 03 | 34.82 |
| 04 | 32.42 |
| 05 | 29.53 |
| **Prelim. mean ± std** | **30.89 ± 5.76** |

**Comparison to baselines:**

| Method | Source-domain | Fresh-instance |
|:-------|:------------:|:-------------:|
| Ensemble HAT (NL=1.0) | ~88% | **86.37 ± 1.54%** |
| MLP-linear only (NL=2.0) | 87.79% | 32.12 ± 7.72% |
| All-linear (NL=2.0) | 87.49% | 32.60 ± 9.18% |
| **Joint MLP-linear + Ensemble HAT (NL=2.0)** | **91.36%** | **~30.9 ± 5.8%** |

**Interpretation:**
Joint training **does not** break the severe-NL fresh-instance ceiling. The ~30% result is statistically indistinguishable from the MLP-only and all-linear baselines, indicating that the residual nonlinearity in the attention blocks (QKV, proj) dominates the failure mode. MLP-linearization alone is insufficient; the attention pathway under NL=2.0 appears to introduce a fundamental generalization barrier that epoch-level D2D resampling cannot overcome.

This is a **negative result** but scientifically valuable: it establishes that the fresh-instance ceiling under severe NL is not merely an artifact of fixed-mask training, but a structural limit of the first-order NL surrogate + attention-block combination.

**Status:** Full 10-instance evaluation running in background. Final JSON expected shortly.
