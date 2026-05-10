# KIMI Rebuttal Arsenal — v2: Generalization Objections (2026-04-20)

**Scope:** 5 anticipated reviewer objections concerning *generalization* of claims to other workloads, architectures, precision regimes, environmental conditions, and training paradigms.
**Sources:** Manuscript §1, §3, §5, §6; `CLAUDE_REBUTTAL_PREP_20260420.md`; `KIMI_REBUTTAL_ARSENAL_V1_20260420.md`.
**Constraint:** Response-only; no manuscript source edits.

---

## 1. Transfer to Language-Model Workloads

**(a) Objection (reviewer voice).**
"Your entire study is built around Vision Transformers and small-scale image classification. Would any of these conclusions—especially the 6-bit ADC cliff or the Ensemble HAT recipe—transfer to large language models where sequence lengths are orders of magnitude longer and attention mechanisms serve a different grammatical function?"

**(b) Where already addressed.**
Unaddressed for language models specifically. The manuscript scopes itself to vision: §1 states the framework addresses "edge-vision accuracy" and "Vision Transformer (ViT) or convolutional neural network (CNN) backbones." §6.6 explicitly flags that "Extrapolation to ImageNet-scale deployment is also outside the present evidence base: per-epoch D2D resampling would incur substantially higher training overhead, the 6-bit ADC cliff may shift upward for deeper MLP stacks with finer decision boundaries, and the current results do not address fresh large-scale training from random initialization." No mention of autoregressive language workloads appears.

**(c) Ready-to-fire response (3 sentences).**
The manuscript intentionally limits its claims to vision backbones and edge-vision benchmarks (§1: "edge-vision accuracy"), and §6.6 explicitly excludes ImageNet-scale extrapolation, so analog-to-language transfer is outside the present evidence base. That said, the core mechanisms we quantify—matrix-multiplication ADC quantization, D2D mismatch in linear projections, and ensemble resampling for spatial noise—are operator-agnostic and apply wherever dense analog crossbars execute linear layers, including the MLP and attention projections inside transformer language models. Extending the framework to autoregressive workloads would require validation against long-context attention and KV-cache analog retention, which is a natural next step but not one the current manuscript claims to cover.

**(d) New experiment required?**
Yes — would require a new experiment suite on a language-model benchmark (e.g., analog CIM simulation of LLM linear layers) to verify whether the 6-bit ADC cliff and Ensemble HAT recipe survive long-sequence scaling.

---

## 2. Transfer to CNNs Outside the Studied Class

**(a) Objection (reviewer voice).**
"You benchmark ResNet-18, ConvNeXt-Tiny, and Tiny-ViT-5M. But ResNet-18 is an old design, and ConvNeXt is essentially a Transformer-ized CNN. How do we know these conclusions generalize to modern efficient CNNs like EfficientNet or MobileNet that are actually deployed at the edge?"

**(b) Where already addressed.**
Addressed in part but scoped narrowly. §5.1 reports baselines for "ResNet-18, ConvNeXt-Tiny, and Tiny-ViT-5M." §6.2 states: "Comparing the dual testbeds—ConvNeXt (CNN) and Tiny-ViT (Transformer)—reveals that the Transformer architecture is more fragile under the present physical stress tests. Because the two models serve complementary roles (ConvNeXt from scratch versus Tiny-ViT from pre-trained fine-tuning), this result should be read as evidence of a strong architecture-and-training interaction rather than as a universal ranking of all Transformers against all CNNs." No EfficientNet, MobileNet, or other efficient-CNN data are included.

**(c) Ready-to-fire response (3 sentences).**
The manuscript explicitly frames the CNN-vs-Transformer comparison as an architecture-and-training interaction rather than a universal law (§6.2: "this result should be read as evidence of a strong architecture-and-training interaction rather than as a universal ranking of all Transformers against all CNNs"). The analog partition is applied at the dense linear-operator level, so the physical stress model transfers mechanically to any backbone composed of convolutions or feed-forward blocks, but the relative accuracy ranking depends on each architecture's noise-amplification topology. Because the framework's profile-driven interface (§3.4) and operator substitution are backbone-agnostic, testing EfficientNet or MobileNet would require only model-configuration changes, not structural simulator edits.

**(d) New experiment required?**
No — the framework already supports arbitrary backbone substitution via its modular operator mapping; running EfficientNet or MobileNet through the same profile pipeline is a configuration sweep, not a new experiment class (though it would require compute time).

---

## 3. FP8 Digital Inference vs. 4-Bit Analog

**(a) Objection (reviewer voice).**
"You frame 4-bit analog inference as necessary for energy efficiency, but modern digital accelerators are already shipping FP8 inference with minimal accuracy loss. Why should anyone adopt noisy 4-bit analog arrays when an FP8 digital pipeline likely achieves comparable accuracy at lower risk?"

**(b) Where already addressed.**
Unaddressed. The manuscript reports "Digital FP32 baselines" (§5.1) and evaluates analog quantization at "n_states=16 conductance levels" (§3.3), i.e., 4-bit analog weight storage. No FP8 digital baseline or accuracy-energy comparison against low-precision digital inference appears anywhere in §1–§6.

**(c) Ready-to-fire response (3 sentences).**
The manuscript does not benchmark FP8 digital inference, so any claim that analog 4-bit dominates FP8 on accuracy would be unsupported; the present energy comparison is strictly versus FP32 digital (§6.4), where the first-order model projects roughly an order-of-magnitude dense-projection energy reduction. Because the analog energy estimate omits routing overhead, iterative write-verify, and ADC calibration costs that FP8 digital incurs differently, a rigorous analog-vs-FP8 trade-off would require a technology-node-matched energy model and an iso-accuracy throughput comparison that is outside the present scope. The conservative reading of the current results is that analog 4-bit is energy-advantageous relative to full-precision digital, but whether that advantage survives against optimized FP8 remains an open systems question.

**(d) New experiment required?**
Yes — a quantitative accuracy-energy comparison against an FP8 digital baseline on the same workloads and process node would require new modeling and/or experiments.

---

## 4. Temperature Variation Over the Inference Lifetime

**(a) Objection (reviewer voice).**
"Your retention and mismatch experiments assume a fixed nominal temperature, yet in a real edge deployment the chip will heat up during inference, cool during idle, and experience seasonal ambient swings. Does your 79% retention plateau or the 86.37% Ensemble-HAT claim survive dynamic thermal variation over the inference lifetime?"

**(b) Where already addressed.**
Addressed as an explicit limitation. §6.5 states: "Three circuit-level phenomena are not yet modeled explicitly: spatial IR drop (currently a 1% scalar placeholder), sneak-path currents (likewise), and temperature-dependent shifts in photoresponse and mismatch variance." The 79% plateau is reported under uniform double-exponential decay at fixed temperature (§5.3: "a broad plateau near 79% (79.13--79.51%) through 10 000 s"), with no time-varying thermal envelope.

**(c) Ready-to-fire response (3 sentences).**
The manuscript candidly scopes the current study to nominal fixed-temperature conditions and lists dynamic temperature effects among the deferred circuit-level phenomena in §6.5 ("temperature-dependent shifts in photoresponse and mismatch variance"). The 79% plateau and 86.37% Ensemble-HAT figures are therefore upper bounds under isothermal operation, and the profile-driven substitution interface (§3.4) is structured so that temperature-dependent coefficients can be added as new JSON fields once device characterization across temperature is available. Because organic semiconductors are temperature-sensitive, dynamic thermal variation would likely lower both numbers, but the relative risk ranking—ADC resolution first, then D2D mismatch—should persist as long as the temperature coefficients are monotonic across the operating range.

**(d) New experiment required?**
Yes — would require measured temperature-dependent retention, mismatch variance, and photoresponse statistics across the operational temperature range, followed by a time-varying temperature sweep during inference.

---

## 5. Fine-Tuning-Only HAT vs. Training-from-Scratch

**(a) Objection (reviewer voice).**
"Tiny-ViT is fine-tuned from a pretrained checkpoint, whereas ConvNeXt is trained from random initialization. Does this mean HAT only works when combined with expensive pre-training, or can a practitioner take any off-the-shelf pretrained model, apply HAT fine-tuning, and expect the 86.37% fresh-instance transfer you report?"

**(b) Where already addressed.**
Addressed directly. §5.1 states: "ConvNeXt probes analog adaptation from random initialization, whereas Tiny-ViT probes foundation-model deployment." §6.2 adds: "Because the two models serve complementary roles (ConvNeXt from scratch versus Tiny-ViT from pre-trained fine-tuning), this result should be read as evidence of a strong architecture-and-training interaction rather than as a universal ranking of all Transformers against all CNNs." §3.3 describes the Tiny-ViT training protocol as 100-epoch AdamW fine-tuning with HAT noise injected from V3 onward, demonstrating that HAT recovery is achieved without pre-training on analog noise.

**(c) Ready-to-fire response (3 sentences).**
The manuscript explicitly tests both regimes: ConvNeXt is trained from random initialization with HAT (§5.1: "ConvNeXt probes analog adaptation from random initialization"), and Tiny-ViT is fine-tuned from a pretrained digital checkpoint with HAT (§6.2: "ConvNeXt from scratch versus Tiny-ViT from pre-trained fine-tuning"). Both achieve strong HAT recovery—ConvNeXt reaches 60.54% on CIFAR-100 from scratch versus 23.86% without HAT—so pre-training is not a prerequisite for the HAT recipe to function. The 86.37% fresh-instance transfer is specific to Tiny-ViT's higher digital baseline and pre-trained initialization, but the underlying Ensemble HAT mechanism (Eq. 2, §3.2) is training-paradigm agnostic.

**(d) New experiment required?**
No — both from-scratch and fine-tuning-only HAT are already demonstrated in the manuscript; no new experiment is required to answer this objection.

---

## Quick-Reference Summary

| # | Objection | Manuscript status | New experiment? |
|---|-----------|-------------------|-----------------|
| 1 | Language-model transfer | Unaddressed; vision scope disclosed (§1, §6.6) | Yes (LLM benchmark suite) |
| 2 | CNNs outside studied class | Partially addressed; scoped as non-universal (§5.1, §6.2) | No (backbone-agnostic framework) |
| 3 | FP8 digital inference | Unaddressed; only FP32 digital baseline reported (§5.1, §3.3) | Yes (FP8 iso-accuracy comparison) |
| 4 | Dynamic temperature variation | Limitation disclosed (§6.5); isothermal upper bounds | Yes (temp-dependent characterization + sweep) |
| 5 | Fine-tuning-only vs. from-scratch | Addressed directly (§5.1, §6.2, §3.3) | No |

---

*Document generated: 2026-04-20*
*Verified against: manuscript §1, §3, §5, §6; CLAUDE prep; V1 arsenal.*
