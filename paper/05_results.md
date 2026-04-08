# 5. Results

## 5.1 Baseline Digital Performance

We first establish the digital FP32 baselines for all architectures across the three target datasets. Table 4 summarizes these results. ResNet-18 and Tiny-ViT-5M both perform strongly on CIFAR-10, while Tiny-ViT benefits from transfer learning and reaches the highest accuracy. On CIFAR-100, the gap between the pre-trained Tiny-ViT deployment setting and the from-scratch ConvNeXt training setting widens further, highlighting that the two testbeds serve different but complementary roles: ConvNeXt probes analog adaptation from random initialization, whereas Tiny-ViT probes analog deployment of a compact foundation model. The low-data Flowers-102 regime makes that distinction even sharper: ConvNeXt-Tiny reaches only 33.22% from scratch, while Tiny-ViT retains 97.97% after fine-tuning.

| Architecture | Dataset | FP32 Accuracy (%) |
|:--|:--|--:|
| ResNet-18 | CIFAR-10 | 94.98 |
| ConvNeXt-Tiny | CIFAR-10 | 90.74 |
| Tiny-ViT-5M | CIFAR-10 | 97.48 |
| ConvNeXt-Tiny | CIFAR-100 | 64.12 |
| Tiny-ViT-5M | CIFAR-100 | 86.94 |
| ConvNeXt-Tiny | Flowers-102 | 33.22 |
| Tiny-ViT-5M | Flowers-102 | 97.97 |

## 5.2 Quantization and the "Scale Masking" Effect

Evaluation of the 4-bit hybrid models without explicit noise exposure (Experiment V2/C2) shows that quantization alone is a minor penalty under the canonical mapping. For Tiny-ViT, the more surprising observation is that V2 still attains 97.39% when evaluated under the standard uniform-noise setting. Our diagnostic interpretation is the **scale-masking effect**: digital scale recovery compresses the effective analog perturbation below the 4-bit LSB, so the deployment noise is largely absorbed by the quantized weight bins. However, this protection is model-specific rather than unconditional. As Section 5.9 will show, it does not survive under proportional state-dependent noise.

## 5.3 Task Complexity Scaling

Figures 4 and 5 show the central system-level conclusion of this study: **noise fragility scales with task complexity, and the value of HAT scales with it.**

On CIFAR-10, the canonical Tiny-ViT degradation from V1 to V3 is modest and HAT provides only a small additional gain. On CIFAR-100, the situation changes sharply: Tiny-ViT drops from 86.94% to 44.06% under standard noisy deployment, and HAT recovers the model to 65.48% (+21.42 pp over V3). ConvNeXt exhibits the same qualitative trend, dropping from 64.12% to 23.86% and recovering to 60.54% (+36.68 pp over C3). This cross-architecture agreement is important because it shows that the complexity-dependent role of HAT is not a transformer-only artifact.

Flowers-102 reveals the opposite boundary condition. Tiny-ViT still benefits from HAT in relative terms (4.81% to 22.48%), but remains far below its FP32 baseline of 97.97%. ConvNeXt does not recover at all (dropping slightly from 3.79% to 3.35%). We therefore hypothesize that stochastic hardware-aware regularization has a **data-volume floor**. Under a shared training recipe and extremely limited supervision, HAT can become too strong for stable convergence, causing the CNN baseline to marginally underperform even the unregularized noisy evaluation. However, this remains a hypothesis that requires further ablation to fully decouple from potential domain-shift factors.

## 5.4 ADC and Quantization Thresholds

The ADC bit-width sweep identifies **6-bit as the critical practical threshold** for Transformer-based CIM under the present simulator assumptions. At 4-bit ADC resolution, accuracy drops to ~27%, while a jump to 6-bit restores it to over 80%. This indicates that the attention mechanism is more constrained by the precision of the summation results than by the static weight programming.

## 5.5 Retention and Temporal Drift

Fig. 7 shows the corrected V4 retention decay with dynamic scale recalibration and co-decay of the retained D2D buffers. The curve exhibits a two-phase behavior: a rapid early drop from 91.63% to 82.66% at 1 s, followed by a broad plateau near **79% accuracy** from 10 s to $10{,}000$ s (79.13%, 79.05%, 79.35%, and 79.51% at 10, 100, 1000, and $10{,}000$ s, respectively). Under the present first-order retention model, this indicates that long-horizon analog inference remains partially viable once gain recalibration is included in the inference stack. The retention results reported here were obtained under the uniform double-exponential decay model (§3). The codebase now additionally supports true state-dependent retention where high-conductance states decay faster, but the canonical V4 results in this paper use the uniform model.

## 5.6 Hardware-Instance Transferability

Experiments on fresh hardware instances (Task 12) reveal a severe weakness in current transformer deployment. Tiny-ViT V4 collapses to near-random performance when evaluated on arrays with a different fixed D2D realization, whereas ConvNeXt retains partial functionality under some transferred device profiles. The key lesson is not that CNNs are universally robust, but that the present Tiny-ViT training procedure remains strongly susceptible to **hardware-instance overfitting**. This makes same-instance robustness and fresh-instance robustness fundamentally different evaluation targets and motivates multi-instance HAT as a next-step training strategy.

## 5.7 Physical Front-end Compensation

We evaluate the impact of the organic phototransistor's sub-linear response ($\gamma_{\text{phys}}$) and dark current ($I_{\text{dark}}$) on system-level accuracy. Figure 6 summarizes the ResNet-18 (R4) and Tiny-ViT (V6) results under various frontend configurations.

The inverse-gamma compensation mechanism successfully restores accuracy for high $\gamma_{\text{phys}}$ (e.g., $\gamma=2.0$), providing a gain of up to +5.8 pp compared to the raw physical response. However, we observe that for $\gamma < 1$, the compensation is less effective due to shot-noise amplification. Our SNR analysis (Group 2) confirms that while inverse-gamma preprocessing linearizes the signal, it amplifies noise variance across the entire intensity range when $1/\gamma > 1$.

**Core Value Conclusion**: Inverse-gamma compensation provides a physical-level regularization effect in low-light/dark scenarios; however, in high-intensity regions, noise variance increases with the compensation exponent, constituting a fundamental **design trade-off**. Consequently, the frontend benefit is most pronounced in high-dark-current regimes where signal recovery outweighs noise amplification.

## 5.8 Physical Non-Idealities (Tasks 23 & 24 Evaluation)

Stress testing the "Scale Masking" and "HAT Recovery" conclusions under more realistic device models reveals substantial risks when models are not explicitly trained for these conditions:

1. **State-Dependent Noise Evaluation**: When a model trained under uniform noise (V4) is evaluated under state-dependent proportional noise, accuracy collapses to **10.0%**. This indicates that the uniform window-referenced noise model likely overestimates the intrinsic robustness of cross-device transfer.
2. **Nonlinear Writing Evaluation**: Similarly, evaluating V4 under a non-linear writing constraint ($NL=2.0$) during inference-only tests degrades accuracy to **27.9%**. This confirms that the global attention mechanism is fundamentally sensitive to weight distortions that deviate from the training-time noise distribution.

## 5.9 HAT Recovery under Physical Stress (Tasks 34, 35 & 36)

To test whether hardware-aware training can overcome these hard physical constraints, we performed dedicated retraining under proportional noise and non-linear writing dynamics for both architectures.

1. **Proportional Noise HAT (Task 34 & 36)**: Hardware-aware training can recover performance when the training and evaluation physics are aligned. For **Tiny-ViT-5M**, proportional-noise HAT reaches **97.48%** in training and **97.37 ± 0.05%** under proportional-noise Monte Carlo evaluation, recovering performance within the matched proportional-noise regime. However, this robustness is highly regime-specific: the same checkpoint falls to **10.38 ± 0.44%** when evaluated under the original uniform-noise semantics. For **ConvNeXt-Tiny**, proportional-noise HAT reaches **91.98%** with **91.91 ± 0.08%** Monte Carlo performance. Because this slightly exceeds the nominal C1 baseline under the current training recipe, we interpret it as a stochastic-regularization effect under this specific matched setting, not as evidence that analog proportional noise is broadly accuracy-improving.

2. **Nonlinear Writing HAT (Task 35)**: In contrast, HAT remains unable to recover performance under severe write non-linearity ($NL=2.0$) for the Transformer backbone. Despite 100 epochs of retraining, Tiny-ViT-5M peaks at **27.37%**, and the corresponding evaluation remains at **27.72 ± 0.82%**. This is only marginally different from the inference-only degradation, indicating that first-order gradient scaling is not sufficient to bridge the non-linearity gap for the current transformer deployment.

3. **Ensemble HAT (Task 37)**: To address the hardware-instance overfitting identified in Section 5.6, we evaluate a "top-tier" model trained with per-epoch D2D resampling. While the standard HAT model (V4) overfits to its training instance and collapses to **10.00%** when evaluated on fresh device instantiations, the Ensemble HAT model demonstrates remarkable zero-shot transferability. Across 10 fresh hardware instances with different spatial mismatch maps, the Ensemble HAT model maintains an average accuracy of **86.37 ± 1.54%**. This confirms that learning weight basins invariant to specific D2D realizations is a viable algorithmic path to cross-device generalizability for Transformer-class models.

Taken together, these findings revise the physical ranking of bottlenecks. Under the canonical uniform-noise model, standard stochastic device noise is not the dominant limit. Under more realistic extensions, however, the picture becomes regime-dependent: proportional noise can be retrained around, but **nonlinear write dynamics** and **instance-specific mismatch** remain the primary challenges for deploying Transformer-class models.

## 5.10 Energy Efficiency Profile

The analytical energy model (visualized in Fig. 11) estimates a total inference cost of **$273.94~\mu$J** for Tiny-ViT-5M, corresponding to an **11.45x reduction** relative to the FP32 digital reference under the present operation-count assumptions. In the current Pareto view (Fig. 8), this places the hybrid Tiny-ViT regime on a favorable energy-accuracy frontier, but not as a universally optimal point independent of future measured-device calibration or alternative peripheral assumptions. Digital attention operations (QK^T and Softmax) still account for **57.9%** of the total cost, confirming the "analog ceiling" discussed in §6.4.


## 5.11 Case Study: Zero-Shot Transfer to a Literature-Calibrated Device

To demonstrate the practical utility of our framework for evaluating realistic hardware, we conducted a case study simulating zero-shot transfer to a recent state-of-the-art organic optoelectronic synapse array, calibrated directly from literature. We defined a literature-derived profile (`literature_fitted_profile.json`) using parameters fitted from the physical device characterization in Zhang et al., *Nature Communications* **17:197** (2026): a conductance range of $G_{\max}/G_{\min} = 47.3$ with 34 effective programming states, and transparent proxy estimates for programming variability ($\sigma_{c2c}=2\%$, $\sigma_{d2d}=3\%$) derived from the reported supplementary cycling and threshold voltage ($V_{th}$) uniformity data.

By loading this literature-derived organic profile into the simulator, we evaluated the pre-trained Tiny-ViT checkpoints without any device-specific fine-tuning. The standard HAT model (V4), having overfitted to its original training instance, collapsed to **10.00%** on the new array parameters. In contrast, the Ensemble HAT model (Task 37) successfully maintained an accuracy of **88.53%**. It is important to note that the modeled variance parameters ($\sigma_{c2c}=2\%$, $\sigma_{d2d}=3\%$) are transparent proxy estimates. However, sensitivity analysis indicates that even if these proxies are moderately perturbed, the qualitative gap between the collapsing standard model and the robust Ensemble HAT model remains firmly intact. This workflow explicitly confirms that the framework can be employed to benchmark the system-level viability of externally characterized CIM materials, effectively bridging the gap between raw device measurements and algorithm deployment.
ized CIM materials, effectively bridging the gap between raw device measurements and algorithm deployment.
