# 5. Results

## 5.1 Baseline Digital Performance

We first establish the digital FP32 baselines for the backbone-dataset pairs that are actually used in the paper. Table 4 summarizes these results. ResNet-18 and Tiny-ViT-5M both perform strongly on CIFAR-10, while Tiny-ViT benefits from transfer learning and reaches the highest accuracy. On CIFAR-100, the gap between the pre-trained Tiny-ViT deployment setting and the from-scratch ConvNeXt training setting widens further, highlighting that the two testbeds serve different but complementary roles: ConvNeXt probes analog adaptation from random initialization, whereas Tiny-ViT probes analog deployment of a compact foundation model. The low-data Flowers-102 regime makes that distinction even sharper: ConvNeXt-Tiny reaches only 33.22% (single-run estimate) from scratch, while Tiny-ViT retains 97.97% after fine-tuning.

| Architecture | Dataset | FP32 Accuracy (%) |
|:--|:--|--:|
| ResNet-18 | CIFAR-10 | 94.98 |
| ConvNeXt-Tiny | CIFAR-10 | 90.74 |
| Tiny-ViT-5M | CIFAR-10 | 98.06 |
| ConvNeXt-Tiny | CIFAR-100 | 64.12 |
| Tiny-ViT-5M | CIFAR-100 | 86.94 |
| ConvNeXt-Tiny | Flowers-102 | 33.22* |
| Tiny-ViT-5M | Flowers-102 | 97.97 |

* ConvNeXt on Flowers-102 is reported as a single-run estimate because we did not run a multi-seed sweep for that low-data from-scratch control.

## 5.2 Quantization and the "Scale Masking" Effect

Evaluation of the 4-bit hybrid models without explicit noise exposure (Experiment V2/C2) shows that quantization alone is a minor penalty under the canonical mapping. For Tiny-ViT, the more surprising observation is that V2 still attains 97.39% when evaluated under the standard uniform-noise setting. Our diagnostic interpretation is what we descriptively call the **scale-masking effect**: digital scale recovery compresses the effective analog perturbation below the 4-bit LSB, so the deployment noise is largely absorbed by the quantized weight bins. Concretely, if the recovered weight is written as `w_eff = s (g+ - g-)`, then perturbations `δg` that remain smaller than the local half-step of the quantized differential state do not change the recovered effective bin after calibration, i.e. `|s δg| < s Δg / 2`. Under that condition, much of the nominal conductance noise is hidden from the task-level model because the digital scale factor rescales it back into the same effective weight bucket. However, this protection is model-specific rather than unconditional. As Section 5.8 will show, it does not survive under proportional state-dependent noise.

## 5.3 Task Complexity Scaling

Figures 4 and 5 show that deployment fragility increases with task complexity and that HAT is most effective on harder tasks. On CIFAR-100, Tiny-ViT improves from 44.06% to 65.48% and ConvNeXt from 23.86% to 60.54%. On Flowers-102, recovery remains limited: Tiny-ViT reaches 22.48%, whereas ConvNeXt does not recover.

## 5.4 ADC and Quantization Thresholds

The ADC sweep places a critical threshold near **6 bits** for Transformer-based CIM under the present simulator assumptions. At 4-bit ADC resolution, accuracy drops to roughly 27%, while a jump to 6-bit restores it to over 80%. This indicates that the attention mechanism is more constrained by the precision of the summation results than by the static weight programming, consistent with prior ViT quantization studies such as PTQ4ViT, Q-ViT, and FQ-ViT.

## 5.5 Retention and Temporal Drift

Fig. 7 shows the corrected V4 retention decay with dynamic scale recalibration and co-decay of the retained D2D buffers. The curve exhibits a two-phase behavior: a rapid early drop from 91.63% to 82.66% at 1 s, followed by a broad plateau near **79% accuracy** from 10 s to $10{,}000$ s (79.13%, 79.05%, 79.35%, and 79.51% at 10, 100, 1000, and $10{,}000$ s, respectively). Under the present first-order retention model, this indicates that long-horizon analog inference remains partially viable once gain recalibration is included in the inference stack. The retention results reported here were obtained under the uniform double-exponential decay model (§3). The codebase now additionally supports true state-dependent retention where high-conductance states decay faster, but the canonical V4 results in this paper use the uniform model. A direct comparison between these two models (Appendix retention comparison table) shows a difference below 0.1 percentage points across the tested time range, validating the uniform model for the present parameter regime. This sanity check is intentionally scoped to the retained V4 Ensemble HAT path that underlies the deployment-facing retention claim; we did not repeat the same model-choice comparison on the collapsing fresh-instance standard-HAT path or on non-HAT checkpoints.

## 5.6 Hardware-Instance Transferability

Experiments on fresh hardware instances reveal a severe weakness in current transformer deployment. Tiny-ViT V4 collapses to chance-level performance (`10.00%`) when evaluated on arrays with a different fixed D2D realization, showing that same-instance robustness and fresh-instance robustness are fundamentally different evaluation targets and motivating multi-instance HAT as the next training step.

The transferability figure now includes a small strip of representative CIFAR-10 deployment inputs so that the cross-profile comparison is visually anchored to the same inference distribution rather than appearing as a context-free device bar chart.

## 5.7 Physical Front-end Compensation

We evaluate the impact of the organic phototransistor's sub-linear response ($\gamma_{\text{phys}}$) and dark current ($I_{\text{dark}}$) on system-level accuracy. The frontend-compensation figure summarizes the ResNet-18 (R4) and Tiny-ViT (V6) results under various frontend configurations.

The inverse-gamma compensation mechanism successfully restores accuracy for high $\gamma_{\text{phys}}$ (e.g., $\gamma=2.0$), providing a gain of up to +5.8 pp compared to the raw physical response. However, we observe that for $\gamma < 1$, the compensation is less effective due to shot-noise amplification. The accompanying SNR analysis confirms that while inverse-gamma preprocessing linearizes the signal, it amplifies noise variance across the entire intensity range when $1/\gamma > 1$.

**Core Value Conclusion**: Inverse-gamma compensation provides a physical-level regularization effect in low-light/dark scenarios; however, in high-intensity regions, noise variance increases with the compensation exponent, constituting a fundamental **design trade-off**. Consequently, the frontend benefit is most pronounced in high-dark-current regimes where signal recovery outweighs noise amplification.

## 5.8 Physical Non-Idealities (Tasks 23 & 24 Evaluation)

Stress testing the "Scale Masking" and "HAT Recovery" conclusions under more realistic device models reveals substantial risks when models are not explicitly trained for these conditions:

1. **State-Dependent Noise Evaluation**: When a model trained under uniform noise (V4) is evaluated under state-dependent proportional noise, accuracy collapses to **10.00%**. This indicates that the uniform window-referenced noise model likely overestimates the intrinsic robustness of cross-device transfer.
2. **Nonlinear Writing Evaluation**: Similarly, evaluating V4 under a non-linear writing constraint ($NL=2.0$) during inference-only tests degrades accuracy to **27.72%**. This confirms that the global attention mechanism is fundamentally sensitive to weight distortions that deviate from the training-time noise distribution and places this stress point outside the recoverable regime of the current first-order recipe.

## 5.9 HAT Recovery under Physical Stress (Tasks 34, 35 & 36)

To test whether hardware-aware training can overcome these hard physical constraints, we performed dedicated retraining under proportional noise and non-linear writing dynamics for both architectures.

1. **Proportional Noise HAT (Task 34 & 36)**: Hardware-aware training can recover performance when the training and evaluation physics are aligned. Under proportional-noise HAT, **Tiny-ViT-5M** reaches **97.48%** in the selected training checkpoint and retains **97.37 ± 0.05%** under proportional-noise Monte Carlo evaluation. This robustness is strongly regime-specific: the same checkpoint falls to **10.38 ± 0.44%** when evaluated under the original uniform-noise semantics. For **ConvNeXt-Tiny**, proportional-noise HAT reaches **91.98%** in the best single-seed checkpoint with **91.91 ± 0.08%** Monte Carlo performance for that checkpoint. Under three-seed reproducibility evaluation (seeds 42, 123, 2026), however, the same proportional-noise HAT recipe yields **84.75 ± 0.72%**. We therefore treat the original 91.98% result as a favorable stochastic basin rather than as the expected population mean. Even so, the proportional-noise retraining result still shows that this regime is recoverable in a way that the canonical uniform-noise checkpoint is not.

2. **Nonlinear Writing HAT (Task 35)**: In contrast, HAT remains unable to recover performance under severe write non-linearity ($NL=2.0$) for the Transformer backbone. Despite 100 epochs of retraining, Tiny-ViT-5M peaks at **27.37%** in the selected single-seed checkpoint, and the corresponding evaluation remains at **27.72 ± 0.82%**. This is only marginally different from the inference-only degradation, indicating that first-order gradient scaling is not sufficient to bridge the non-linearity gap for the current transformer deployment. We therefore interpret this result as the boundary of the *present* gradient-scaling approximation under `NL=2.0`, not as a universal impossibility result for all organic write dynamics.

3. **Ensemble HAT (Task 37)**: Resampling D2D masks during training alleviates instance overfitting. Across 10 fresh hardware instances with different spatial mismatch maps, the Ensemble HAT model maintains **86.37 ± 1.54%** while leaving wall-clock time effectively unchanged relative to standard HAT in our logged single-run timings (**85.5 vs. 85.9 min; ~1.00x**). Deployment still programs one trained checkpoint onto one static physical array; the zero-shot claim is only that the final checkpoint need not be pre-fit to that target array's exact D2D map in advance.

Taken together, these findings revise the physical ranking of bottlenecks. Under the canonical uniform-noise model, standard stochastic device noise is not the dominant limit. Under more realistic extensions, however, the picture becomes regime-dependent: proportional noise can be retrained around, but **nonlinear write dynamics** and **instance-specific mismatch** remain the primary challenges for deploying Transformer-class models.

## 5.10 Energy Efficiency Profile

The analytical energy model (visualized in Fig. 11) estimates **273.94~μJ** per Tiny-ViT-5M inference, corresponding to an upper-bound **11.45x reduction** relative to the FP32 digital reference. Expressed in the same units, this is **273.94~μJ** for the hybrid stack versus **3140~μJ** for the FP32 digital baseline. Adding routing overhead equal to 10%, 30%, or 50% of the analog-MAC budget reduces this gain to about 11.10x, 10.47x, and 9.90x, respectively. The comparison remains FP32-referenced and the cost of post-array scale recovery is still absorbed into the present first-order model. Digital attention operations (QK^T and Softmax) still account for **57.9%** of the total cost, confirming the "analog ceiling" discussed in §6.4.

To supplement the qualitative maps in Fig. 10, we also tracked the mean head-averaged attention entropy for the three representative samples shown there. The displayed columns correspond to **cat**, **truck**, and **automobile** from left to right, while the rows follow **V1**, **V3**, **V4**, and **V6** from top to bottom. Averaged across the samples, the entropy rises from **3.38** in the digital baseline (V1) to **3.61** under standard noisy deployment (V3), indicating a broader and less selective spatial focus. Under HAT (V4), the entropy drops to **3.07**, and the model recovers the correct class label on all three displayed examples, whereas V3 is correct on only one. This is not a full statistical study of attention geometry, but it provides a compact quantitative supplement to the visual argument that HAT restores a sharper task-aligned focus pattern.


## 5.11 Case Study: Zero-Shot Transfer to a Literature-Calibrated Device

To demonstrate the practical utility of our framework for evaluating realistic hardware, we conducted a case study simulating zero-shot transfer to a recent state-of-the-art organic optoelectronic synapse array calibrated directly from literature. We defined a literature-derived profile (`literature_fitted_profile.json`) using parameters fitted from the physical device characterization in Zhang et al., *Nature Communications* **17:197** (2025): a conductance range of $G_{\max}/G_{\min} = 47.3$ with 34 effective programming states, and transparent proxy estimates for programming variability ($\sigma_{\text{C2C}}=2\%$, $\sigma_{\text{D2D}}=3\%$) derived from the reported supplementary cycling-repeatability and threshold voltage ($V_{th}$) uniformity data. These noise values should therefore be read as runtime proxies rather than final measured conductance-domain variance tables, because the source paper reports 8-cycle repeatability and 80-device $V_{th}$ spread, not a full conductance-domain programming-variance distribution.

By loading this literature-derived organic profile into the simulator, we evaluated the pre-trained Tiny-ViT checkpoints without any device-specific fine-tuning. The standard HAT model (V4), having overfitted to its original training instance, collapsed to **10.00%** on the new array parameters. In contrast, the Ensemble HAT model (Task 37) successfully maintained an accuracy of **88.53%**. It is important to note that the modeled variance parameters ($\sigma_{\text{C2C}}=2\%$, $\sigma_{\text{D2D}}=3\%$) are transparent proxy estimates. However, sensitivity analysis indicates that even if these proxies are moderately perturbed, the qualitative gap between the collapsing standard model and the robust Ensemble HAT model remains firmly intact. Under these proxy-backed profile assumptions, this workflow illustrates how the framework can be employed to benchmark the system-level viability of externally characterized CIM materials, effectively bridging the gap between raw device measurements and algorithm deployment.
