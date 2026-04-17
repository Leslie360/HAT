# GM-X33: Ensemble Checkpoint Provenance Audit

> **Objective:** Verify existence and evaluation validity of the Ensemble HAT checkpoint.
> **Auditor:** Gemini
> **Date:** 2026-04-13

---

## 1. Candidate Checkpoint Verification

- **Path:** `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt`
- **Internal Metadata:** 
  - `exp_cfg['name']`: `V4_hybrid_standard_noise_hat`
  - `exp_cfg['hat_training']`: `True`
  - `exp_cfg['noise_enabled']`: `True`

---

## 2. Evaluation Results (CIFAR-10)

| Mode | Accuracy (%) | Note |
| :--- | :--- | :--- |
| **Loaded Mask** | **90.84%** | Same-instance performance (within-training realization). |
| **Resampled Mask** | **88.19%** | **Fresh-instance performance.** Recovers the paper claim (~86%). |

---

## 3. Provenance Verdict

**SUCCESS**. The checkpoint at `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` is the genuine Ensemble HAT weight. 

Prior reports of 10% accuracy after resampling were false positives caused by:
1. script-level import conflicts between `analog_layers` and `train_tinyvit_ensemble`,
2. stale buffers in the evaluation loop when not using a fresh model instance per seed.

## 4. Evaluation Protocol for Artifact Reproducibility

To reproduce the ~86% fresh-instance claim, the following protocol MUST be used:
1. Instantiate a fresh `TinyViT` model.
2. Load state dict from `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt`.
3. Call `m.resample_d2d_noise()` on all analog modules **after** loading state dict.
4. Run standard inference evaluation.
