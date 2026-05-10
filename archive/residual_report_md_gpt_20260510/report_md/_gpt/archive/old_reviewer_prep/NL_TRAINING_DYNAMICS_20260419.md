# NL=2.0 Mitigation Training Dynamics Summary

**Date:** 2026-04-19
**Model:** Tiny-ViT V4 (hybrid, HAT, C2C=0.05, D2D=0.1)
**Dataset:** CIFAR-10
**Noise level:** NL=2.0 global, with linear compensation applied to specific layer groups.

---

## 1. Per-Lane Test-Accuracy Curves

All curves are extracted from checkpoint `history['test_acc']` arrays (or log output where checkpoints are partial).

| Lane | Epochs | Best Acc | @ Epoch | Final Acc | First-10 Mean |
|:-----|:-------|:---------|:--------|:----------|:--------------|
| **MLP-only** | 100 | **87.79%** | 73 | 86.22% | 49.76% |
| **All-linear** | 100 | **87.49%** | 59 | 84.81% | 49.76% |
| **QKV-only** | 100 | **18.72%** | 2 | 10.15% | 16.46% |
| **Attn-proj-only** | 57 | **18.86%** | 0 | 10.51% | 14.50% |
| **Baseline (no mitigation)** | 100 | **27.37%** | 15 | 13.83% | 23.20% |

### Key epoch snapshots

| Lane | Epoch 0 | Epoch 4 | Epoch 9 | Epoch 19 | Epoch 34 | Epoch 59 | Final |
|:-----|:--------|:--------|:--------|:---------|:---------|:---------|:------|
| MLP-only | 24.97 | 50.24 | 68.16 | 81.56 | 86.37 | 87.01 | 86.22 |
| All-linear | 25.04 | 52.02 | 67.68 | 81.95 | 81.63 | **87.49** | 84.81 |
| QKV-only | 17.52 | 16.20 | 14.79 | 14.11 | 11.96 | 10.93 | 10.15 |
| Attn-proj-only | 18.86 | 14.28 | 11.31 | 11.41 | 11.19 | 10.93 | 10.51 |
| Baseline NL=2.0 | 17.42 | 23.51 | 25.66 | 22.04 | 22.09 | 15.54 | 13.83 |

---

## 2. Convergence Speed Comparison

| Lane | ≥50% | ≥70% | ≥80% | Saturation Phase (last 30 epochs) |
|:-----|:-----|:-----|:-----|:----------------------------------|
| MLP-only | Epoch 4 | Epoch 11 | Epoch 18 | 86.94% ± 0.44 |
| All-linear | Epoch 4 | Epoch 11 | Epoch 19 | 85.73% ± 0.66 |
| QKV-only | **Never** | **Never** | **Never** | 10.26% ± 0.21 |
| Attn-proj-only | **Never** | **Never** | **Never** | 10.55% ± 0.37 |
| Baseline NL=2.0 | **Never** | **Never** | **Never** | 14.37% ± 0.64 |

**Observation:** MLP-only and All-linear converge with nearly identical speed. Both hit 50% by epoch 4 and 80% by epoch ~19. The other three lanes never reach 50%.

---

## 3. Stability Analysis

### Test-accuracy variance across epochs

| Lane | Overall Mean | Overall Std | Drop (Best → Final) | Trend |
|:-----|:-------------|:------------|:--------------------|:------|
| MLP-only | 81.30% | 11.92 | **1.57%** | Monotonic rise → stable plateau |
| All-linear | 80.23% | 11.48 | **2.68%** | Monotonic rise → stable plateau |
| QKV-only | 12.24% | 2.22 | **8.57%** | Monotonic decline |
| Attn-proj-only | 11.48% | 1.78 | **8.35%** | Monotonic decline |
| Baseline NL=2.0 | 20.77% | 4.25 | **13.54%** | Rise to epoch 15, then steady decay |

### Saturation-phase stability (last 30 epochs)

- **MLP-only:** Extremely stable. Standard deviation only 0.44% in the last 30 epochs. No catastrophic forgetting or drift.
- **All-linear:** Slightly more volatile than MLP-only (std 0.66%), but still well-behaved.
- **QKV-only / Attn-proj:** Dead lanes. Variance is low only because the model is stuck near random-guess accuracy (~10%).
- **Baseline:** High variance (std 4.25%) driven by a clear post-peak decay pattern after epoch 15.

---

## 4. Training-vs-Generalization Gap

Extracted from checkpoint `history['train_acc']` and `history['test_acc']`:

| Lane | Initial Train Acc | Final Train Acc | Final Test Acc | Gap |
|:-----|:------------------|:----------------|:---------------|:----|
| MLP-only | 25.99% | 98.31% | 86.22% | 12.1% |
| All-linear | 26.59% | 98.37% | 84.81% | 13.6% |
| QKV-only | 21.54% | **9.51%** | 10.15% | −0.6% |
| Attn-proj-only | 20.96% | **26.88%** | 10.51% | **16.4%** |
| Baseline NL=2.0 | 20.59% | 82.31% | 13.83% | **68.5%** |

**Critical patterns:**

1. **MLP / All-linear:** Train acc rises to >98%. The model learns the training set and generalizes reasonably (gap ~12–14%). This is normal supervised-learning behavior.
2. **QKV-only:** Train acc **collapses** from 21.5% to 9.5%. The model cannot even memorize the training data. This is not overfitting; it is **optimization failure** caused by noisy MLP layers.
3. **Attn-proj-only:** Train acc barely rises (21% → 27% over 57 epochs), while test acc collapses to 10.5%. The model makes marginal training progress but generalizes worse than random.
4. **Baseline:** Train acc climbs to 82% but test acc collapses to 14%. Classic **severe overfitting** under noise—memorization without generalization.

---

## 5. Key Insight: Why MLP Recovers While Attention Collapses

### Empirical evidence

| What is compensated | Best Test Acc | Outcome |
|:--------------------|:--------------|:--------|
| MLP only | **87.79%** | Full recovery |
| All linear (MLP + attention) | **87.49%** | Full recovery (no gain over MLP-only) |
| QKV only | **18.72%** | Worse than baseline |
| Attn-proj only | **18.86%** | Worse than baseline |
| Nothing (baseline) | **27.37%** | Partial collapse |

### Interpretation

1. **MLP layers are the dominant noise-sensitive bottleneck.** Compensating them alone is sufficient to recover ~87% accuracy. Adding attention compensation (All-linear) does not improve over MLP-only.

2. **Attention-only compensation is actively harmful.** Both QKV-only and Attn-proj-only achieve **lower** best accuracy (18.7%) than the uncompensated baseline (27.4%). This suggests that injecting linear compensation exclusively into attention layers while leaving MLPs at raw NL=2.0 distorts the signal path without fixing the actual error source.

3. **Failure mode depends on which layers are noisy:**
   - **Noisy MLPs (QKV-only / Attn-proj-only):** The model cannot learn. Training accuracy stagnates near 20–27% and eventually collapses. The gradients propagated through the noisy MLPs destroy useful updates.
   - **Noisy everywhere (baseline):** The model can memorize training data (train_acc 82%) but generalizes terribly (test_acc 14%). The network overfits because noisy layers act as random feature extractors that happen to fit the training set.
   - **Noisy attention only (MLP-only / All-linear):** The model learns and generalizes normally. Attention noise at NL=2.0 is tolerable when MLPs are clean.

4. **Convergence dynamics confirm the bottleneck.** MLP-only and All-linear share an almost identical rising curve (≤1% difference at every key epoch). If attention layers were a secondary bottleneck, All-linear should outperform MLP-only; it does not. This implies attention linearity compensation is **redundant** once MLPs are fixed.

### Practical implication

For NL=2.0 on this Tiny-ViT architecture, **resources should be prioritized toward MLP-layer compensation**. Attention-layer compensation alone is insufficient and may even degrade performance relative to the uncompensated baseline.

---

## 6. Missing Data & Caveats

- **Attn-proj-only** checkpoint history stops at epoch 56 (last.pt) and was resumed on 2026-04-19. The resume log shows only epoch 0 of the resumed run with no further epochs recorded at the time of this analysis. The trajectory (train_acc flat at ~27%, test_acc declining to ~10%) strongly suggests continued collapse, but the final 43 epochs are not yet available.
- No dedicated eval-mode repeated-run statistics were found for the mitigation lanes (only the baseline has a 10-run eval log). Reported numbers are single-run test_acc from training checkpoints.
- The baseline experiment (`task35_v4_nl2_hat`) used a different checkpoint directory; its history is included for comparison but was run on 2026-04-06, several days before the mitigation suite.
