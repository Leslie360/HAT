<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 9cdbe77 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# PhD Defense Q&A Prep — Organic Optoelectronic CIM Simulation

**Date:** 2026-04-20  
**Format:** 25 anticipated questions across 8 categories. Each answer = 3 sentences (claim, evidence, nuance).

---

## 1. Methodology Rigor (4)

**Q1. Why CIFAR-10 instead of ImageNet or a custom sensor dataset?**

CIFAR-10 lets us separate noise interactions from data-scaling effects, because the core question is whether the simulator ranks failure modes, not whether it chases SOTA. Cross-dataset ablations on CIFAR-100 and Flowers-102 confirm that the 6-bit ADC cliff and Ensemble HAT recovery replicate across complexity levels. ImageNet remains outside the evidence base because per-epoch D2D resampling would require substantially higher training overhead, and this work targets methodological foundations before scale demonstrations.

**Q2. Why Tiny-ViT V4 as the canonical backbone?**

Tiny-ViT-5M is the smallest pretrained ViT that still exhibits attention-driven sensitivity to analog non-idealities, training to 98.06% on CIFAR-10 in under two hours on one A100. The manuscript validates the same trends for ConvNeXt-Tiny and ResNet-18, so the choice is a narrative anchor rather than an architecture-specific claim. A larger transformer would increase compute cost without changing the failure-mode ranking, because ADC resolution, instance overfitting, and front-end nonlinearity are analog-layer properties.

**Q3. Why ten fresh hardware instances and five Monte Carlo passes per instance?**

Ten instances yield a standard error of ~0.49 pp, tight enough to distinguish 86.37% from chance with p < 10^-15. Five MC passes per instance average out cycle-to-cycle fluctuations while preserving between-instance variance, since D2D mismatch—not C2C noise—is the binding transfer risk. We report the standard deviation across the ten instance means rather than across all fifty forward passes pooled together, because the latter would understate true instance-to-instance spread.

**Q4. What is the statistical power of n = 10?**

With n = 10, a one-sample t-test against the 10.00% chance baseline yields a t-statistic exceeding 150, and the 95% confidence interval is [85.27%, 87.47%]. The OPECT zero-shot transfer corroborates this, reaching 88.53 ± 0.08% under a different noise law without retraining. That said, n = 10 is modest for tail risks: we cannot rule out rare outlier arrays below 80%, so we frame the result as a distributional mean rather than a worst-case guarantee.

---

## 2. Novelty Relative to Prior Work (4)

**Q5. What is new versus Lin et al. (2016)?**

Lin et al. performed a Monte Carlo sweep for a single-layer organic-memristive perceptron on MNIST; we extend that variability-aware perspective to modern deep-learning software, CIFAR-scale tasks, and Vision Transformers. Our framework additionally introduces a replaceable JSON profile interface, inverse-gamma photoresponse compensation, and structured D2D resampling cadences. We treat Lin et al. as the foundational Monte Carlo precedent and build the system-level layers above it.

**Q6. What is new versus CrossSim?**

CrossSim is an excellent inorganic toolkit with lookup-table training models and GPU-accelerated parasitic solvers, but it does not natively expose inverse-gamma optoelectronic photoresponse or organic-specific double-exponential retention. Our preliminary comparison shows consistent clean baselines (86.2% ours versus 83.7% CrossSim at 8-bit ADC) but a 14.43 pp divergence under noise injection, demonstrating that the noise-to-conductance mapping is framework-sensitive. We position our work as an organic-specific complement, not a replacement.

**Q7. What is new versus AIHWKIT?**

AIHWKIT is calibrated for PCM and ReRAM, and its noise injection is primarily per-batch stochastic variation rather than structured spatial D2D resampling per hardware instance. Our shared-regime sanity check confirms qualitative agreement on ResNet-18 (90.08 ± 0.21% AIHWKIT versus 86.57% ours), but AIHWKIT has no canonical baseline for epoch-level structured mismatch-map resampling. Ensemble HAT—resampling a complete spatial D2D field each epoch—is the load-bearing novelty, and we treat AIHWKIT as a methodological consistency anchor.

**Q8. Why isn't this just domain randomization?**

Domain randomization randomizes i.i.d. texture or lighting parameters, whereas D2D mismatch is a spatially correlated fixed field that persists across all forward passes on a given instance. Our ablation shows that i.i.d. per-epoch noise drops fresh-instance accuracy to ~75%, while structured spatial resampling reaches 86.37%, confirming that correlation structure matters. Ensemble HAT is augmentation matched to the deployment distribution, with a block-stationary schedule that gives the optimizer enough stability to descend under each instance before the field changes.

---

## 3. Scope Limitations (3)

**Q9. Why only first-order behavioral models?**

First-order behavioral models trade physical fidelity for gradient-path flexibility and computational tractability, which is essential when sweeping hundreds of training runs across architectures, datasets, and noise regimes. A full SPICE simulation of a 128 × 128 crossbar with 13.3 million devices would require weeks per forward pass, making the core cadence ablations and iso-accuracy sweeps practically impossible. The manuscript explicitly states this scope boundary and frames the framework as a risk-ranking tool, not a chip-predictive emulator.

**Q10. What about sneak paths?**

Sneak paths are acknowledged as an unmodeled circuit-level phenomenon; we include only a 1% scalar placeholder derived from ReRAM literature, not a spatially resolved parasitic solver. Sneak-path severity depends on array geometry, selector device presence, and wiring resistance, none of which are yet standardized for our target technology. Future work will replace the placeholder with a geometry-aware circuit layer once measured array layouts become available.

**Q11. Why defer full IR-drop and thermal modeling?**

Spatial IR drop and temperature-dependent shifts are omitted because the parameter base is literature-derived, and most organic optoelectronic papers report room-temperature characteristics without array-level voltage or thermal maps. We include a 1% scalar IR-drop placeholder to signal sensitivity, but a resolved model would need fabrication-specific line resistance and power density estimates that do not yet exist. The framework accepts these extensions via the profile interface without code changes once data arrive.

---

## 4. The Physics Gap (3)

**Q12. How do we know organic RRAM behaves like our model?**

We do not claim that it does; canonical parameters are literature-derived or proxy-calibrated, and the manuscript labels the framework as a simulation baseline under literature priors. The Zhang 2025 OPECT case study provides a partial bridge: substituting their reported metrics into the same JSON profile yields 88.53 ± 0.08% zero-shot transfer, suggesting the mapping from reported physics to accuracy is internally consistent. True physical closure requires hardware-in-the-loop validation, which is explicitly deferred to future work.

**Q13. What calibration data exists for the nonlinear-write surrogate?**

The NL = 2.0 parameter is anchored to measured DNTT transients reported by Vincze et al. (2025), but the gradient-scaling STE surrogate is a first-order approximation, not a pulse-faithful write model. We frame the 27.72% result not as a material bound but as an approximation-boundary: if true physical write dynamics deviate from the surrogate, actual accuracy could differ. Direct nonlinear-write measurements on fabricated organic arrays are the highest-priority calibration gap.

**Q14. What if the device physics changes?**

That is precisely why the profile-driven interface exists: the digital backbone remains fixed while the JSON parameter bundle is swapped, so a new semiconductor requires only a new profile, not new code. We demonstrated this with the OPECT zero-shot transfer, where substituting Zhang 2025 parameters changed accuracy from 86.37% to 88.53% without retraining. The limitation is that the framework supports only the modeled non-idealities; a failure mode outside the eight-layer physics stack would require interface extension.

---

## 5. Reproducibility (3)

**Q15. Can someone else reproduce 86.37%?**

Yes; the exact command is in the repository README, and all code, configs, logs, and a Tier-A checkpoint subset (~1.5 GB) are archived with SHA-256 manifests for Zenodo deposition. Fresh-instance evaluation uses the same canonical uniform-noise profile and ten-instance protocol reported in the paper. The only non-determinism comes from GPU floating-point ordering across CUDA versions, which we bound to within ±0.3 pp through seed-locked regression tests.

**Q16. What varies across seeds?**

Across three independent seeds for canonical V4 HAT, CIFAR-10 accuracy varies by ~±0.5 pp, while the Ensemble HAT fresh-instance mean varies by ~±1.0 pp; both are small compared to the architecture and noise-regime effects that drive the narrative. The dominant variance source is the D2D mismatch realization itself, not weight initialization, which is why the protocol reports instance-level spread (1.54 pp) rather than seed-level spread. Canonical seeds are locked in the release manifest for exact numerical reproduction.

**Q17. What hardware does a replicator need?**

A single NVIDIA A100 or equivalent GPU with 40 GB VRAM is sufficient for all training; Tiny-ViT trains in under two hours, and the full ensemble ablation suite completes in roughly one GPU day. Inference evaluation requires only a consumer GPU or CPU, since MC passes are embarrassingly parallel and the models are small. The conda environment is fully specified in `environment.yml` with Python 3.11, PyTorch ≥ 2.1, and CUDA 12.1.

---

## 6. What-If Scenarios (3)

**Q18. What if you used ResNet-18 instead of Tiny-ViT?**

ResNet-18 reaches 95.46% digital on CIFAR-10 but degrades sharply under analog noise, with canonical HAT falling to ~86.57% and collapsing further under higher noise because BatchNorm statistics are corrupted during analog layer conversion. The manuscript reports this as a negative result and uses ResNet as an entry validation platform, while Tiny-ViT serves as the deployment-oriented transformer testbed. The takeaway is that Transformers are more fragile under front-end distortion but more recoverable under HAT, whereas CNNs suffer from analog-specific statistical shifts that are harder to train out.

**Q19. What if D2D were 20% instead of 10%?**

Our 63-point iso-accuracy sweep shows that at 6-bit ADC and above, 20% D2D reduces Tiny-ViT accuracy to 71–77%, while 10% D2D maintains above 84%. Sobol analysis confirms that in the operational envelope, D2D accounts for 92% of residual accuracy variance, so doubling D2D is damaging. The mitigating factor is that the OPECT literature reports D2D closer to 3%, suggesting 10% is already conservative for state-of-the-art organic arrays.

**Q20. What if NL were 3.0?**

We did not test NL = 3.0 because NL = 2.0 already reduces accuracy to 27.72 ± 0.82%, indicating the gradient-scaling surrogate is near its breaking point; extrapolation would likely drive accuracy to chance level. The more important question is whether physical devices actually enter this regime: the DNTT anchor suggests NL ≈ 2.0 is plausible but not universal, and we treat this as an approximation-limited boundary rather than a proven material limit. Corrected parameters can be absorbed immediately through the profile interface once direct measurements are available.

---

## 7. Industrial Applicability (3)

**Q21. Would a chip company use this?**

A chip company would use it in the pre-tapeout risk-ranking phase, when device parameters are still emerging and system architects must decide which non-idealities deserve transistor-level investment. The 6-bit ADC cliff and instance-overfitting result directly inform this trade-off: they tell designers to secure readout precision before chasing marginal conductance improvements. The framework is not a replacement for final sign-off simulators, but it is faster and requires no custom netlists, making it useful for architecture–device co-design loops.

**Q22. What is the path to silicon?**

The path has three stages: replace literature profiles with measured characterizations from fabricated test structures; validate that simulated accuracy ranking matches hardware-in-the-loop measurements on small arrays; scale to full reticles using the same profile interface with updated geometry and parasitic parameters. We are currently at stage one, with raw doctoral measurement exports available and a round-trip auto-fitter validated to within 2% parameter error. The modular architecture means each stage requires only profile substitution, not framework rewrite.

**Q23. What about yield?**

Yield is not modeled explicitly: we assume fully functional arrays with parametric variation, not hard defects or stuck-at faults. This is deliberate because yield statistics for organic optoelectronic crossbars at the 128 × 128 scale are not yet available in the literature; introducing a defect model would require guessing an unanchored defect density. Once fabrication data arrive, the framework can be extended with a defect-aware profile field, but for now we focus on parametric risk ranking.

---

## 8. Future Research Directions (2)

**Q24. What is the most important next experiment?**

Hardware-in-the-loop validation: correlating simulator predictions against measured organic array conductance distributions and task-level accuracy on a physical prototype. This closes the literature-prediction gap and either validates or recalibrates the entire profile-substitution workflow. Every other next step—including ImageNet scaling, thermal modeling, or new architectures—is secondary until we know whether the first-order behavioral mapping is physically predictive.

**Q25. If you had 10× the compute, what would you do?**

I would run ImageNet-scale fresh-instance HAT with per-epoch D2D resampling across five seeds, because the 6-bit ADC cliff and MLP-path NL bottleneck may shift when decision boundaries are finer and the MLP stack is deeper. I would also train a surrogate model that maps device-profile parameters directly to accuracy without full neural-network training, enabling real-time co-optimization during materials discovery. The remaining compute would go to spatially resolved IR-drop and thermal simulations coupled with array geometry, turning the current placeholder scalars into physics-informed spatial fields.

---

*End of document — 25 questions, ~2,100 words.*
