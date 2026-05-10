<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Conference Abstract Package — 3 Venues
**Date:** 2026-04-21
**Scope:** One-page workshop abstracts for NeurIPS/ICML/MLSys tracks.
**Constraint:** All numbers locked to canonical results; no unpublished-source disclosure.

---

## Venue A — NeurIPS Workshop on Machine Learning for Systems

**Title:** Ensemble HAT: Closing the Hardware-Instance Generalization Gap in Analog CIM

Analog compute-in-memory (CIM) promises orders-of-magnitude energy efficiency for edge inference by executing matrix-vector multiplications inside memory arrays, yet standard hardware-aware training (HAT) catastrophically overfits to a single fixed device-to-device (D2D) mismatch map. We identify this collapse as a new systems-level generalization gap—hardware-instance overfitting—and propose Ensemble HAT, a training protocol that resamples the spatial mismatch map at each epoch to match the deployment distribution rather than optimizing for a single instance. The key insight is that D2D mismatch is spatially structured and fixed per fabricated array, so treating it as a distribution over instances rather than as i.i.d. noise changes the training objective fundamentally. Evaluated on Tiny-ViT-5M with an organic optoelectronic device profile, Ensemble HAT raises fresh-instance accuracy from a 10.00% chance-level collapse to **86.37 ± 1.54%** across ten unseen arrays, with no measurable wall-clock overhead relative to fixed-mask HAT (85.5 vs. 85.9 min). Supplementary ablations confirm that per-batch i.i.d. noise underperforms epoch-level structured resampling (86.16% vs. 88.41%), indicating the gain is genuinely distributional and not merely stronger regularization. The result suggests that treating fixed spatial hardware maps as a distribution-matching problem, rather than a noise-augmentation problem, is the load-bearing design choice for reliable analog inference systems.

- Frames hardware-instance overfitting as a distinct generalization failure mode for analog inference systems.
- Introduces epoch-level spatial-mismatch resampling as a zero-shot transfer remedy with negligible training cost.
- Validates via a 10-instance × 5-MC protocol that structured resampling dominates fixed-mask and i.i.d. baselines.

**Future work:** Extending the distribution-matching objective to higher-order device nonlinearity surrogates and spatially correlated mismatch maps is the next step.

---

## Venue B — ICML Workshop on Hardware-Aware Machine Learning

**Title:** Where HAT Hits a Wall: A Falsification Study of Severe Nonlinearity in Analog CIM

Hardware-aware training (HAT) has demonstrated impressive accuracy recovery under moderate analog device stress, but its limits under severe write nonlinearity remain largely unexplored. We adopt a falsification stance within a profile-driven behavioral simulation framework for organic optoelectronic compute-in-memory, systematically testing three independent mitigation strategies—MLP-only linearization, full linearization, and joint MLP-linear training coupled with Ensemble HAT—under severe nonlinearity (NL = 2.0). The underlying hypothesis was straightforward: if the MLP blocks, which carry twice the analog parameter budget of the attention pathway, dominate the accuracy loss, then linearizing them while protecting attention should break the ceiling. All three strategies restore source-domain accuracy above 87%, yet fresh-instance evaluation across ten unseen hardware realizations converges on the same approximate ceiling: the joint recipe reaches only **30.53 ± 7.07%**, statistically indistinguishable from MLP-only (32.12 ± 7.72%) and all-linear (32.60 ± 9.18%). Because removing nonlinearity from the larger MLP block yields no benefit, the bottleneck is not raw capacity but functional structure in the attention pathway. This convergence signals a structural generalization barrier that first-order conductance surrogates cannot train through, regardless of architectural partitioning or distributional resampling, and it redefines what hardware-aware ML can realistically promise under aggressive device stress.

- Provides the first falsification study mapping the deployment-envelope boundary for hardware-aware vision transformers on analog arrays.
- Demonstrates that block-heterogeneous linearization and distributional resampling fail to break the severe-NL ceiling.
- Introduces a pre-registered diagnostic protocol (CX-J1b/c/d) to guide future surrogate-model development.

**Future work:** Higher-order or physics-informed conductance surrogates and attention-free architectures are needed to push past the observed structural limit.

---

## Venue C — MLSys Workshop on ML for Edge Computing

**Title:** Viable Zones for Organic Optoelectronic CIM: A Profile-Driven Edge Deployment Study

Organic optoelectronic synaptic devices offer multilevel conductance tuning, optical sensitivity, and ultra-low static power, but materials researchers currently lack a systematic way to decide whether reported device metrics are already sufficient for modern edge-vision deployment. We present a profile-driven behavioral simulation framework that maps literature-derived organic parameters—quantization, cycle-to-cycle and device-to-device variability, retention drift, ADC precision, and nonlinear write—directly into task-level accuracy and energy for ResNet-18, ConvNeXt-Tiny, and Tiny-ViT-5M. Rather than asking whether a device is "good" in isolation, the framework asks which parameters dominate the failure risk once mapped onto a realistic hybrid analog-digital inference path. Our analysis reveals that nominal quantization is rarely the dominant bottleneck; instead, converter precision, hardware-instance overfitting, and severe write nonlinearity dictate go/no-go decisions. Ensemble HAT establishes a viable zone by recovering fresh-instance Tiny-ViT accuracy to **86.37 ± 1.54%** under moderate stress, while severe nonlinearity (NL = 2.0) traps all tested mitigations near 30%. A first-order energy decomposition estimates an upper-bound 11.45× reduction versus FP32 for the hybrid stack, with explicit sensitivity bounds showing the qualitative conclusion survives even 50% unmodeled interconnect overhead, giving edge system designers actionable trade-off data before tape-out.

- Delivers a transparent materials-to-system decision bridge for organic CIM edge deployment before fabrication commitment.
- Identifies ADC precision and instance overfitting—not quantization—as the primary accuracy bottlenecks in the studied regime.
- Bounds the energy-accuracy trade-off with explicit sensitivity to unmodeled interconnect and peripheral costs.

**Future work:** Integrating measured organic-array profiles and scaling the framework to ImageNet-scale edge tasks will sharpen the viable-zone boundaries.
