# Figure Caption Drafts (GPT)

These are submission-oriented draft captions for the English manuscript.

They are intentionally concise and should be adapted to the final venue style, but the scientific boundaries should remain stable.

Use together with:
- `paper/FIGURE_PLAN.md`
- `paper/FIGURE_CAPTION_LOCK_gpt.md`
- `paper/FIG1_FIG2_BRIEF_gpt.md`

## Fig.1

**Hybrid analog/digital system overview for organic optoelectronic CIM inference.** Static dense projections are mapped to differential-pair crossbar arrays, whereas dynamic attention products (`QK^T`, `AV`), softmax, LayerNorm, activation functions, and other control-heavy operators remain in the digital domain. The figure emphasizes that the platform is a hybrid CIM system rather than a fully analog transformer.

## Fig.2

**Behavioral weight-to-conductance mapping and readout abstraction.** Floating-point weights are split into positive and negative branches, mapped into the device conductance window, quantized into discrete states, perturbed by device effects, and read out through differential subtraction with optional digital scale recovery. This schematic represents the first-order behavioral abstraction used in the simulator and does not imply pulse-accurate circuit or programming dynamics.

## Fig.3

**Analytical SNR trends under inverse-gamma compensation.** Reconstructed signal-to-noise curves illustrate how inverse-gamma preprocessing can improve dark-region separability while amplifying bright-region noise variance. The plot is an analytical visualization derived from the same physical assumptions used in the simulator, not a direct empirical measurement.

## Fig.4

**Cross-dataset accuracy comparison under FP32, standard-noise, and hardware-aware training.** Results are shown for ConvNeXt-Tiny and Tiny-ViT-5M on CIFAR-10, CIFAR-100, and Flowers-102. The figure highlights that the effect of analog non-idealities is weak on CIFAR-10, becomes severe on CIFAR-100, and interacts strongly with low-data regularization on Flowers-102.

## Fig.5

**Complexity-dependent degradation and HAT recovery across datasets.** Left: accuracy drop from FP32 to the standard-noise regime. Right: recovery from the standard-noise regime to HAT. FP32 baselines are shown as references so that recovery is interpreted together with the absolute task difficulty of each dataset and architecture.

## Fig.6

**Physical front-end compensation trade-off under phototransistor nonlinearity and dark current.** Inverse-gamma compensation improves low-signal recovery in dark or high-dark-current regimes, but it also amplifies bright-region noise. The figure summarizes this trade-off through accuracy gains and robustness trends rather than presenting compensation as a free improvement.

## Fig.7

**Canonical retention behavior for ConvNeXt C9 and corrected Tiny-ViT V4.** The Tiny-ViT retention curve shows a rapid early drop followed by a broad plateau near 79% once gain recalibration and D2D co-decay are included in the inference path. Shaded bands denote `±1 std` across Monte Carlo runs. Superseded legacy V7 retention results are intentionally excluded.

## Fig.8

**Energy-accuracy Pareto summary under the current operation-count model.** Hybrid analog deployment reduces dense-projection energy substantially, but the final frontier remains conditioned on digital attention overheads, peripheral assumptions, and future measured-device calibration.

## Fig.9

**Continuous noise sensitivity and ADC threshold evidence.** The left and middle panels summarize accuracy under continuous `(\sigma_{C2C}, \sigma_{D2D})` sweeps, while the right panel highlights the sharp Tiny-ViT accuracy transition around 6-bit ADC resolution. Together, these views separate benign stochastic noise from genuinely limiting peripheral precision.

## Fig.10

**Zero-shot hardware transferability across device profiles.** Organic-HAT checkpoints are evaluated under alternative device assumptions at inference time without retraining. The figure should be interpreted as a test of cross-instance and cross-profile transferability, not as a comparison of device-specific peak performance.

## Fig.11

**Hybrid energy breakdown under the present profiler assumptions.** The total cost is decomposed into analog MACs, converters, digital operations, and memory traffic. The figure is intended as a first-order system-model estimate rather than a measured silicon power report.

## Fig.12

**Qualitative attention-map comparison across canonical and stressed Tiny-ViT checkpoints.** Representative examples illustrate how analog non-idealities and HAT alter spatial focus patterns. The figure is qualitative and should not be interpreted as a statistically exhaustive visualization.
