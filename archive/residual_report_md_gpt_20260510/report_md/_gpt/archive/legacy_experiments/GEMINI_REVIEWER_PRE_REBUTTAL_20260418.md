# GEMINI REVIEWER PRE-REBUTTAL PREP — 2026-04-18

**Reread of canonical state:** Based on the locked manuscript (15pp main, 21pp supp) and the framing of Option B in the cover letter. This memo anticipates structural, device, and evaluation objections from reviewers.

## 1. "Framework" Objections
**Objection 1.1: Simplistic Noise Models.** *"The use of fixed Gaussian distributions for C2C and D2D noise ignores the spatially correlated and heavy-tailed noise profiles typical of organic arrays."*
- **Counter:** The manuscript explicitly frames Gaussian injection as a first-order behavioral proxy designed to establish lower-bound sensitivity limits. Section 3 and the Limitations paragraph formally defer spatially correlated noise to future circuit-aware extensions. The Ensemble HAT recovery proves the framework can diagnose mismatch overfitting even with simplified noise geometries.

**Objection 1.2: STE Backward Surrogate.** *"Approximating nonlinear write dynamics via a Straight-Through Estimator (STE) scaling factor oversimplifies complex pulse accumulation."*
- **Counter:** STE is the established standard for large-scale DNN hardware simulation where pulse-level modeling is computationally prohibitive ($O(N^3)$ overhead). The NL mitigation supplementary table (Table SX.N) directly bounds the failure modes of this surrogate, providing empirical guardrails for its usage.

**Objection 1.3: Hybrid Analog/Digital Split.** *"Assuming digital LayerNorm and Softmax alongside analog MACs ignores the severe ADC/DAC conversion overheads required to move data between domains."*
- **Counter:** The framework adopts a pragmatic mixed-signal architecture, which is the most plausible near-term deployment path for CIM. The analytical energy model in the Supplementary Information explicitly accounts for ADC/DAC and digital buffer costs, proving the hybrid approach retains an ~11× energy advantage.

## 2. "Device" Objections
**Objection 2.1: Calibration Constants.** *"The choice of OPECT device parameters feels arbitrary and may not represent the broader class of organic optoelectronics."*
- **Counter:** The parameters are strictly anchored to the 2025 OPECT literature (Zhang et al.). Furthermore, the supplementary proxy-sensitivity sweeps and the zero-shot transferability case study (Figure 7) demonstrate that the behavioral conclusions (e.g., Ensemble HAT superiority) hold across diverse literature-calibrated profiles.

**Objection 2.2: Cycle Endurance.** *"Organic materials suffer from rapid degradation over write cycles, which this framework completely ignores."*
- **Counter:** Edge-vision CIM targets inference-heavy workloads where weight updates (writes) are infrequent. Consequently, state retention (which we extensively model in V8) is the primary temporal bottleneck, while endurance is a secondary concern deferred to future work.

**Objection 2.3: Temperature Dependence.** *"Organic mobilities are highly temperature-sensitive; evaluating at a nominal 300K masks real-world edge deployment failures."*
- **Counter:** We acknowledge this in the Limitations section. The present paper isolates optical, spatial, and quantizing variables to establish a clear baseline. Thermal scaling (T-dependence) is a complex, coupled multi-physics problem slated for the next phase of the simulator's evolution.

## 3. "Evaluation" Objections
**Objection 3.1: Task Complexity.** *"Evaluating on CIFAR-100 and Tiny-ImageNet is insufficient; state-of-the-art architectures should be benchmarked on ImageNet-1K."*
- **Counter:** Simulating hardware-aware training on ImageNet-1K with full MC statistics requires massive GPU clusters unavailable to most materials-science groups. CIFAR-100 serves as a rigorous, mathematically valid proxy for task-complexity scaling, successfully demonstrating the fragility of foundational models under analog noise.

**Objection 3.2: Best-Checkpoint Reporting.** *"Reporting the best epoch accuracy rather than the final epoch masks training instability."*
- **Counter:** Best-checkpoint reporting is the standard protocol in noisy HAT literature, as analog deployment inherently involves early-stopping to prevent over-adaptation to specific noise draws. This is explicitly disclosed in Section 5.1 for full transparency.

**Objection 3.3: Missing MC Statistics on Baselines.** *"Figure 4 mixes deterministic point estimates (ResNet) with MC error bars (Tiny-ViT), which is statistically sloppy."*
- **Counter:** The caption transparently discloses which bars carry MC statistics. The computational cost of 10-run MC sweeps across all architectures was triaged in favor of deeper ablations on the flagship Tiny-ViT model. (If pressed, we will provide the ResNet MC runs in the rebuttal phase).