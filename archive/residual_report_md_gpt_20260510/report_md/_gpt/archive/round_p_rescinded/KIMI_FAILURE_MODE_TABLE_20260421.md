<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Supplementary Table: Failure-Mode Taxonomy of Fresh-Instance Transfer Under Non-Linearity

## Master Table

| # | Mitigation | Source-domain | Fresh-instance | Ceiling broken? |
|:--|:-----------|:------------:|:-------------:|:---------------|
| 1 | Fixed-mask HAT (baseline) | 87.95 ± 0.27% | 10.00% | ❌ |
| 2 | Ensemble HAT (NL=1.0) | ~88% | **86.37 ± 1.54%** | ✅ |
| 3 | MLP-linear only (NL=2.0) | 87.79% | 32.12 ± 7.72% | ❌ |
| 4 | All-linear (NL=2.0) | 87.49% | 32.60 ± 9.18% | ❌ |
| 5 | Joint MLP-linear + Ensemble HAT (NL=2.0) | 91.36% | 30.53 ± 7.07% | ❌ |

**Caption.** The table catalogues five training-recipe mitigations tested to break the fresh-instance transfer ceiling observed in compute-in-memory Vision Transformers under embedded non-linearity (NL). Each row reports source-domain accuracy (CIFAR-10, 10-class) and fresh-instance accuracy (mean ± std over independent weight draws) for the same architectural configuration. "Ceiling broken?" indicates whether the mitigation raises fresh-instance accuracy above the ~30% barrier observed under severe non-linearity (NL=2.0). Fixed-mask HAT (row 1) is the baseline sparse-training protocol; Ensemble HAT (row 2) averages attention masks across an ensemble of source-domain instances. Rows 3–4 progressively linearize the MLP blocks and then the entire network (excluding attention QKV and projection layers). Row 5 combines MLP linearization with Ensemble HAT. All results are obtained with identical hyper-parameters and data augmentation to isolate the effect of each mitigation.

## Interpretation

- **Under mild NL (NL=1.0), Ensemble HAT fully recovers fresh-instance transfer.** Row 2 shows that averaging attention masks across an ensemble collapses the source-to-fresh accuracy gap from ~78 points (row 1) to <2 points, indicating that instance-dependent attention-pattern noise is the dominant failure mode at moderate non-linearity.

- **Under severe NL (NL=2.0), NO training-recipe modification tested breaks the ~30% ceiling.** Rows 3–5 all cluster tightly around 30–33% fresh-instance accuracy despite source-domain accuracies ranging from 87.5% to 91.4%, demonstrating that the bottleneck is not mitigated by linearizing MLPs, linearizing the entire feed-forward pathway, or combining linearization with ensemble attention masks.

- **The ceiling is therefore structural to the attention pathway under severe NL, not an optimization artifact.** Because linearizing every trainable layer outside the attention QKV and projection blocks (row 4) and even augmenting that with ensemble masks (row 5) fails to lift fresh-instance accuracy, the residual non-linearity in the attention mechanism itself—together with the embedded tanh/sigmoid non-linearities in the memristor-based dot-product—appears to impose a hard ceiling on out-of-distribution weight generalization.

## Open Questions

- **Would all-linear + Ensemble HAT break the ceiling?** This combination is currently untested because fully linearizing the attention QKV and projection layers would require replacing the softmax-normalized dot-product with a linear kernel surrogate, a non-trivial architectural change.

- **Would a higher-order NL surrogate break the ceiling?** Experiment CX-J1d is planned to test whether a second-order or piece-wise polynomial approximation of the embedded non-linearity, rather than the first-order Taylor expansion used here, can recover attention-pattern coherence under NL=2.0.
