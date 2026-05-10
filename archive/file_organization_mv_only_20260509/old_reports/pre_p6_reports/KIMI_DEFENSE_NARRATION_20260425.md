# Defense Slide Narration Script

**Date:** 2026-04-25  
**For:** `KIMI_DEFENSE_BEAMER_20260425.tex`  
**Timing:** ~20 minutes for 20 slides

---

## Slide 1: Title
"Good morning, committee. My thesis asks: how do we deploy Vision Transformers on organic optoelectronic compute-in-memory arrays when every multiply-accumulate is threatened by device variability, nonlinear write, and limited ADC resolution? I'll show that hardware-instance overfitting is the dominant risk, and that Ensemble Hardware-Aware Training solves it."

---

## Slide 2: Outline
"I'll walk through the simulation framework, the Ensemble HAT methodology, its theoretical foundation, empirical mechanism evidence, results across three scenarios, and limitations."

---

## Slide 3: The Analog CIM Opportunity
"The energy wall is real. Data movement between memory and compute dominates inference cost. Analog CIM performs matrix-vector products in-place via Kirchhoff current laws, offering theoretical 10-to-100x savings. Organic optoelectronics add wafer-scale fabrication and photosensitivity. But the catch is variability, nonlinearity, and drift. We need to evaluate before fabrication."

---

## Slide 4: Four Deployment Constraints
"Our framework identifies four constraints. ADC resolution dominates: below 6 bits, transformers collapse. The phototransistor front end is sublinear; we compensate with inverse-gamma preprocessing. Standard HAT overfits one hardware instance and collapses on fresh arrays. And severe nonlinear write—NL equals 2—recovers only to the 80-to-82 percent band. The central claim is that Ensemble HAT raises fresh-instance accuracy from 10 percent to 86.37 plus-minus 1.54 percent."

---

## Slide 5: Hybrid Stack
"Our hybrid deployment maps dense linear operators to analog crossbars: patch embedding, QKV projections, output projections, and MLP layers. Control-heavy operators stay digital: softmax, layer norm, GELU, and the dynamic attention products. About 88 percent of parameters are analog-mapped, but roughly 60 percent of energy remains digital due to attention. This analog ceiling is fundamental."

---

## Slide 6: Profile-Driven Simulation
"The forward path converts weights to differential conductance, quantizes via straight-through estimator, injects D2D mismatch and C2C noise, applies ADC conversion, then scale recovery. All device physics enter through a JSON profile. Swap the profile, change the technology, no code changes. This is the extensibility mechanism."

---

## Slide 7: Standard vs Ensemble HAT
"Standard HAT fixes one D2D mask for the entire training run. The model learns to compensate for that specific spatial pattern—essentially memorizing it. When evaluated on a fresh mask, it collapses to 10 percent. Ensemble HAT resamples the mask at each epoch, forcing the optimizer to minimize expected loss under the full manufacturing distribution. This is the critical distinction."

---

## Slide 8: Theoretical Foundation
"The second-order Taylor expansion reveals an implicit regularizer: a Fisher-weighted gradient-L2 penalty proportional to sigma-D2D squared. This is structurally analogous to stochastic Sharpness-Aware Minimization along the mismatch direction. A PAC-Bayes bound provides generalization theory. And crucially, no extra hyperparameters: the regularization strength is set by the physical device variance."

---

## Slide 9: D2D Loss Landscape
"We interpolate from the training mask toward fresh masks. At alpha equals one—the fresh mask—Standard HAT collapses to 10 percent while Ensemble HAT maintains 88.39 percent: a 78 percentage-point gap. Even at three times extrapolated mismatch, Ensemble still outperforms Standard by 17.5 points. This is the strongest empirical evidence for D2D-directional robustness."

---

## Slide 10: Per-Layer Sensitivity
"We perturb one analog layer at a time. Four of the five most sensitive layers are MLP layers, with stages-two-blocks-four-mlp-fc-two showing the largest single-layer drop of 1.38 percentage points. The patch embedding is also critical. This supports the main-text claim: severe nonlinear write failure localizes to the MLP path."

---

## Slide 11: Canonical Results
"Under canonical NL-equals-one, Ensemble HAT preserves 86.37 plus-minus 1.54 percent across ten fresh instances. The OPECT literature-calibrated profile reaches 88.53 plus-minus 0.08 percent without retraining. Under severe NL-equals-two, all routes recover to the 80-to-82 percent band. Standard versus Ensemble do not separate under severe nonlinearity, and proportional noise offers no special advantage."

---

## Slide 12: The 6-Bit ADC Cliff
"Sobol analysis reveals a two-phase hierarchy. Over the full grid, ADC explains 98 percent of variance. But within the operational envelope—six bits or more, D2D below 15 percent—the hierarchy inverts: D2D explains 92 percent of residual variance. The design rule is sequential: secure six-bit ADC first, then minimize device-to-device mismatch."

---

## Slide 13: Zero-Shot Transfer
"The OPECT case study uses a completely different profile: 3 percent D2D, 2 percent C2C, 34 states, conductance ratio 47.3. Standard HAT collapses across all profiles. Ensemble HAT reaches 88.53 percent with no retraining. Same framework, different JSON file."

---

## Slide 14: Limitations
"Four limitations. First, the framework is behavioral, not circuit-accurate. IR drop and sneak paths are scalar placeholders. Second, dataset scale is CIFAR; ImageNet is future work. Third, energy is a first-order estimate, not silicon measurement. Fourth, device profiles are literature-calibrated; measured calibration awaits collaborator data. The framework's purpose is risk ranking before fabrication."

---

## Slide 15: Summary
"To summarize: we built the first profile-driven behavioral simulator for organic optoelectronic CIM with ViT backbones. We discovered that hardware-instance overfitting—not nominal quantization—is the dominant risk. Ensemble HAT solves this with per-epoch D2D resampling, raising fresh-instance accuracy from 10 to 86.37 percent. The theory provides three converging lenses: implicit regularizer, SAM analogue, and PAC-Bayes bound. And the design rules give engineers a sequential thresholding strategy."

---

## Slide 16: Thank You
"Thank you. I'm happy to take questions."

---

## Backup Slide B1: M-Series Detail
"The M-series spans three independent seeds across three HAT variants. All nine models converge to the 80-to-82 percent band. Cross-seed standard deviation is under one percent for most configurations, confirming stable post-fix behavior."

---

## Backup Slide B2: Correlated D2D
"Under spatially correlated mismatch, the canonical checkpoint tolerates moderate correlation without catastrophic failure. At rho equals 0.5, accuracy degrades by 4.2 percentage points but no instance collapses below 74 percent."

---

## Backup Slide B3: Cadence Ablation
"Empirical ablation confirms epoch-level resampling is load-bearing: 88.41 percent versus 87.18 for fixed and 86.16 for per-batch. The optimizer needs epoch-scale consistency to build stable curvature estimates."

---

## Backup Slide B4: Hessian Nuance
"Full-parameter-space Hessian shows Standard HAT with lower top eigenvalue than Ensemble—counter-intuitively appearing flatter. But this flatness is mask-specific. Standard collapses on fresh masks, proving global curvature is not the right metric. D2D-directional sensitivity is."

---

## Backup Slide B5: Checkpoint Averaging
"Naive parameter-space averaging of two Standard checkpoints yields exactly 10 percent on fresh instances. Simple smoothing does not recover generalization. The training objective—per-epoch resampling—is load-bearing."
