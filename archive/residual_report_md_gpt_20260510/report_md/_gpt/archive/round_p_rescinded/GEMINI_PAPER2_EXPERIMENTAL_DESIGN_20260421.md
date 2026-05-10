# Paper-2 Experimental Design: Structural Limits Under Severe Write Nonlinearity

**Objective.** Falsify the hypothesis that the ~30 % fresh-instance ceiling under NL = 2.0 is a training artifact. Six experiments anchor the falsification study.

---

## E1 — Ensemble HAT Positive Control (NL = 1.0)

**Hypothesis.** Epoch-level D2D resampling preserves hardware-instance generalization under moderate nonlinearity.

**Protocol.** Tiny-ViT V4 fine-tuned on CIFAR-10 with per-epoch spatially correlated D2D resampling (σ_d2d = 0.1) and NL = 1.0. AdamW, lr = 1e-4, batch = 128, cosine schedule, 100 epochs. Evaluated on 10 fresh D2D instances × 5 MC forward passes.

**Expected outcome + interpretation.** 86.37 ± 1.54 % fresh-instance. Validates the canonical protocol and sets the transferable-accuracy reference.

**Compute budget.** ~12 GPU-hours per seed.

**Status.** Done.

---

## E2 — MLP-Linear Severe-NL

**Hypothesis.** Linearizing the MLP path removes the dominant gradient-distortion site under NL = 2.0.

**Protocol.** MLP blocks use NL = 1.0 surrogate; QKV and projection retain NL = 2.0. Otherwise identical to E1.

**Expected outcome + interpretation.** Source 87.79 %, fresh-instance 32.12 ± 7.72 %. The elevated std (7.72 % vs. ~1.5 %) signals erratic instance-dependent behavior. Localizes surrogate failure to the MLP path but confirms MLP linearization alone does not restore deployment-grade transfer.

**Compute budget.** ~12 GPU-hours per seed.

**Status.** Done.

---

## E3 — All-Linear Severe-NL

**Hypothesis.** Linearizing every trainable layer outside attention provides an upper bound on recovery without altering the softmax dot-product.

**Protocol.** Patch-embed, MLP, and head linearized; attention QKV and projection at NL = 2.0.

**Expected outcome + interpretation.** Source 87.49 %, fresh-instance 32.60 ± 9.18 %. Negligible gain over E2 (Δ = 0.48 pp, overlapping CI) demonstrates the bottleneck is not in feed-forward blocks; the attention pathway imposes the ceiling.

**Compute budget.** ~12 GPU-hours per seed.

**Status.** Done.

---

## E4 — Joint MLP-Linear + Ensemble HAT Severe-NL

**Hypothesis.** Coupling MLP linearization with epoch-level D2D resampling breaks the severe-NL fresh-instance ceiling.

**Protocol.** Warm-start from E1 checkpoint, reset optimizer, fine-tune with MLP at NL = 1.0 and attention at NL = 2.0 under per-epoch D2D resampling.

**Expected outcome + interpretation.** Source 91.36 %, fresh-instance 30.53 ± 7.07 %. Statistically indistinguishable from E2–E3 (one-way ANOVA, p > 0.05), falsifying the joint-recovery hypothesis. The ceiling is structural, not an artifact of fixed-mask training.

**Compute budget.** ~15 GPU-hours per seed.

**Status.** Done.

---

## E5 — QKV-Only Linearization (CX-J1b)

**Hypothesis.** Protecting only the QKV arrays isolates whether the barrier resides in the QKV MACs or in the attention block as a functional unit.

**Protocol.** QKV at NL = 1.0; MLP, projection, and softmax at NL = 2.0. Same seeds and eval protocol.

**Expected outcome + interpretation.** ~30 % fresh-instance or lower. A negative result confirms the softmax-normalized dot-product and its projection interaction—not merely QKV MAC nonlinearity—constitute the rate-limiting factor.

**Compute budget.** ~15–20 GPU-hours.

**Status.** Planned.

---

## E6 — Full-Attention Linearization (CX-J1c)

**Hypothesis.** Linearizing both QKV and projection layers tests the extreme upper bound of structural recovery.

**Protocol.** QKV and projection at NL = 1.0; MLP at NL = 2.0. Softmax retained.

**Expected outcome + interpretation.** If fresh-instance accuracy remains ~30 %, the structural limit is confirmed irrespective of attention-subblock linearization. Any lift would instead implicate the QKV or projection MACs as the primary barrier.

**Compute budget.** ~15–20 GPU-hours.

**Status.** Planned.

---

## Controls

Fairness is ensured by holding constant: architecture (Tiny-ViT V4); dataset and augmentation (CIFAR-10); optimizer and schedule (AdamW, cosine, 100 epochs); D2D profile (σ_d2d = 0.1, correlation length 4 arrays); checkpoint provenance (same pretrained digital backbone); and eval protocol (10 fresh instances × 5 MC passes, identical instance RNG seeds). Only layer-wise NL assignment and D2D resampling cadence vary.

---

## Replication

Training: 3 seeds (42, 123, 456) per condition. Evaluation: 10 fresh instances per checkpoint, 5 MC passes each; the reported statistic is the mean of per-instance means. The two-level hierarchy is disclosed in all reporting.

---

## Statistics

Comparisons use Welch two-sample t-tests between each severe-NL condition and E1, and pairwise between severe-NL conditions. One-way ANOVA tests the null that all severe-NL mitigations share a common mean. Effect size is Cohen’s d. All tests use α = 0.05 (two-tailed) with 95 % bootstrap CIs (10 000 resamples) to account for the hierarchical MC structure.
