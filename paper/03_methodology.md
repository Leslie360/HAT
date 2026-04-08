# 3. Methodology

## 3.1 System Architecture Overview

We study a hybrid analog/digital inference stack in which dense linear operators are executed on differential-pair crossbar arrays, while control-heavy or utilization-poor operators remain on a digital coprocessor. The target architecture for heterogeneous deployment is Tiny-ViT-5M. Following the mapping rules fixed in the project handbook, analog execution is assigned to the patch-embedding convolutions, the attention projection matrices $\mathbf{W}_Q$, $\mathbf{W}_K$, $\mathbf{W}_V$, the attention output projection, and the two feed-forward matrices in each transformer block. By contrast, MBConv blocks, downsampling paths, local depthwise convolutions, the dynamic $\mathbf{QK}^\top$ and $\mathbf{AV}$ products, softmax, LayerNorm, activation functions, and the final classification head are executed digitally.

This split is motivated by array utilization. Dense operators map naturally to crossbars because their weight tensors can be flattened into large matrix tiles with high occupancy, whereas depthwise convolutions and dynamic attention products either have poor output-unit utilization or require input-dependent matrices that cannot be pre-programmed into non-volatile arrays \citep{wu2023bwq,wang2024epim}. For Tiny-ViT-5M, the resulting mapping sends $4{,}730{,}016$ parameters to the analog domain and leaves $662{,}748$ parameters digital, corresponding to an analog-mapped parameter ratio of $87.7\%$. Under a $128 \times 128$ physical array constraint and differential-pair storage, this mapping requires 812 arrays and $13{,}303{,}808$ individual devices.

The analog footprint is concentrated in the transformer stages rather than in the MBConv stem. Patch embedding contributes only 8 differential-pair arrays, Stage 1 contributes 48 arrays, Stage 2 contributes 384 arrays, and Stage 3 contributes 372 arrays. This distribution is consistent with the fact that the late dense projections dominate the parameter count even though some early convolutional stages dominate digital MACs. Accordingly, the analog-mapped parameter ratio should not be conflated with the analog MAC ratio: Tiny-ViT places most static weights in analog arrays, yet a substantial share of runtime operations still resides in digital MBConv, downsampling, local depthwise convolution, and attention-special kernels. 

The $\mathbf{Q}\mathbf{K}^\top$ attention score computation and the $\mathbf{A}\mathbf{V}$ product are dynamic, input-dependent matrix multiplications. Unlike static model weights, these dynamic operands cannot be pre-programmed into fixed non-volatile crossbar arrays. Consequently, these operations, along with softmax normalization, must remain in the digital domain. This architectural split creates a fundamental "analog ceiling" for Transformer CIM deployment: even if all static linear projections are perfectly accelerated by the crossbar fabric, the digital attention operations still dictate a hard lower bound on system-level latency and energy. The system architecture therefore couples an analog crossbar fabric for high-density static weights with a digital back-end for normalization, dynamic attention, activation, and low-utilization convolutional paths.

At the circuit level, the CIM benefit comes from programming a static conductance matrix once and then reusing Kirchhoff-current accumulation to evaluate many matrix-vector products in parallel. This is why stored dense projections are natural CIM targets, whereas token-dependent attention kernels are not. The present platform should therefore be interpreted as a hybrid CIM system rather than a fully analog transformer. That distinction matters for honest claims of acceleration: analog arrays remove the cost of repeatedly reading stored weights, but they do not eliminate the digital burden of dynamic attention.

## 3.2 Analog Crossbar Simulation

Each analog-mapped weight tensor $\mathbf{W}$ is converted into a differential-pair conductance representation. Let
$$
\mathbf{W}^{+} = \max(\mathbf{W}, 0), \qquad
\mathbf{W}^{-} = \max(-\mathbf{W}, 0).
$$
To avoid propagating gradients through the normalization constant, we compute
$$
s_W = \lVert \mathbf{W} \rVert_{\infty}^{\mathrm{detach}} + \varepsilon,
$$
and normalize both branches by $s_W$. The positive and negative components are then mapped to the physical conductance range $[G_{\min}, G_{\max}]$:
$$
\mathbf{G}^{+} = G_{\min} + \frac{\mathbf{W}^{+}}{s_W}(G_{\max} - G_{\min}),
\qquad
\mathbf{G}^{-} = G_{\min} + \frac{\mathbf{W}^{-}}{s_W}(G_{\max} - G_{\min}).
$$
The programmed conductances are quantized to $n_{\text{states}}$ discrete levels with a straight-through estimator (STE),
$$
\widetilde{\mathbf{G}} = \operatorname{STEQuantize}(\mathbf{G}; n_{\text{states}}, G_{\min}, G_{\max}),
$$
so that the forward path observes discrete conductance states while the backward path passes gradients as identity.

The effective analog weight used for vector-matrix multiplication is the differential conductance
$$
\mathbf{W}_{\text{eff}} = \widetilde{\mathbf{G}}^{+} - \widetilde{\mathbf{G}}^{-},
$$
optionally followed by scale recovery,
$$
\widehat{\mathbf{W}}_{\text{eff}} = \mathbf{W}_{\text{eff}} \cdot \frac{\lVert \mathbf{W} \rVert_{\infty}^{\mathrm{detach}}}{G_{\max} - G_{\min}}.
$$
The scale-recovery factor corresponds to the `restore_weight_scale` option in the implementation. This distinction is important because the A2 CNN pipeline did not require explicit scale restoration, whereas the A3 Tiny-ViT pipeline enables it by default. Empirically, transformer projections were markedly more sensitive to the shrinkage induced by operating purely in the conductance domain. Restoring the original digital weight scale after quantization, retention, and noise operations therefore became necessary to preserve a stable activation range in Tiny-ViT, while ResNet-18 and ConvNeXt-Tiny remained trainable without this correction.

This same mechanism is also one of the key physical simplifications of the present work. Scale recovery is implemented as an ideal post-array digital rescaling step using layer-wise floating-point factors. That is a useful first-order behavioral abstraction for algorithm-device co-design, but it implicitly assumes that the peripheral readout chain can realize the required gain calibration with negligible quantization or control overhead. In the paper we therefore treat scale recovery as a calibrated digital post-processing primitive rather than as a claim of zero-cost physical circuitry.

Convolutional analog layers follow the same procedure after flattening each kernel to an equivalent $(M,N)$ crossbar shape, where $M$ is the number of output channels and $N$ is the input-channel-by-kernel product. The actual forward pass still uses the native tensor layout, but the quantization and conductance operations are defined on the same physical interpretation as for linear layers.

## 3.3 Device Variability Modeling

We model two sources of device variability. Device-to-device mismatch is treated as a static perturbation sampled once at initialization:
$$
\boldsymbol{\epsilon}_{\text{D2D}} \sim \mathcal{N}\left(0, \sigma_{\text{D2D}}^{2} \Delta G^{2}\right),
\qquad \Delta G = G_{\max} - G_{\min}.
$$
This perturbation is stored as a persistent buffer and is applied to every subsequent forward pass. It captures fixed manufacturing mismatch across programmed devices on the array.

Cycle-to-cycle variation is modeled as a zero-mean Gaussian perturbation resampled on each forward pass:
$$
\boldsymbol{\epsilon}_{\text{C2C}}^{(t)} \sim \mathcal{N}\left(0, \sigma_{\text{C2C}}^{2} \Delta G^{2}\right).
$$
The noisy effective weight becomes
$$
\widehat{\mathbf{W}}^{(t)} =
\left(\widetilde{\mathbf{G}}^{+} - \widetilde{\mathbf{G}}^{-}\right)
 + \boldsymbol{\epsilon}_{\text{D2D}}
 + \boldsymbol{\epsilon}_{\text{C2C}}^{(t)},
$$
with the C2C term disabled when the experiment calls for clean or D2D-only evaluation.

We use three operating regimes anchored to the handbook and associated literature priors. The optimistic regime uses $(\sigma_{\text{C2C}}, \sigma_{\text{D2D}}) = (1\%, 3\%)$, the standard regime uses $(5\%, 10\%)$, and the pessimistic regime uses $(10\%, 20\%)$. The standard setting is the main deployment target, while the pessimistic setting is reserved for survival-style stress testing. In all cases, the variances are applied in the conductance domain rather than directly in the digital weight domain so that noise magnitude scales with the physical dynamic range.

Historically, the canonical R/C/V experiment families used a state-independent Gaussian model referenced to the global conductance window. This is useful for continuity with the earlier handbook-derived baselines, but it remains only a first-order approximation. Real devices often exhibit state-dependent variance, for example $\sigma \propto G$ or $\sigma \propto \sqrt{G}$. To explore this effect, we implement an optional **proportional-noise mode** where the noise magnitude scales with the instantaneous conductance state:
$$
\boldsymbol{\epsilon}^{(t)}_{\text{prop}} \sim \mathcal{N}\left(0, \sigma^2 \lvert \mathbf{G}_{\text{current}} \rvert^2\right).
$$
While the primary results in this manuscript use the simpler window-referenced model, we perform dedicated stress tests (Task 24) to evaluate the impact of this more physically realistic noise distribution on Transformer stability.

## 3.4 Hardware-Aware Training

Hardware-aware training (HAT) is implemented by keeping quantization in the forward path through the STE and exposing the model to realistic device variability during optimization. In the HAT setting, D2D mismatch is fixed for the entire run and C2C noise is resampled at each forward pass, which turns device variability into a stochastic regularizer aligned with the deployment distribution. The backward path uses the STE approximation through quantization so that optimization remains feasible despite the piecewise-constant conductance states.

We distinguish three training modes in this project. First, standard digital training runs without analog replacement and serves as the FP32 baseline. Second, standard hybrid training without HAT uses the analog layer replacements but does not perform full noise-aware optimization. For Tiny-ViT, this setting was refined into a D2D-adapted protocol in which fixed D2D mismatch remains active during training while C2C resampling is disabled; this corresponds to the final definition of experiment V3, labeled "Standard train w/ fixed D2D." Third, full HAT activates both fixed D2D mismatch and per-forward C2C resampling during training. This third regime is used for the main robust hybrid baselines and directly reflects the intended inference conditions.

The revised implementation also exposes nonlinear programming coefficients `NL_LTP` and `NL_LTD`, which modulate the STE backward pass according to the current conductance position. In this manuscript that feature should be interpreted as a first-order behavioral proxy for asymmetric potentiation and depression dynamics rather than as a pulse-accurate write simulator. Its practical purpose is to ensure that measured nonlinearity coefficients can enter the optimization path through the same profile interface used by the inference-only experiments.

Concretely, if a weight update would increase conductance, the surrogate gradient is scaled as
$$
\frac{\partial \mathcal{L}}{\partial G}\Big|_{\mathrm{LTP}}
\propto
\left(\frac{G_{\max}-G}{G_{\max}-G_{\min}}\right)^{\mathrm{NL}_{\mathrm{LTP}}-1},
$$
whereas a conductance-decreasing update is scaled as
$$
\frac{\partial \mathcal{L}}{\partial G}\Big|_{\mathrm{LTD}}
\propto
\left(\frac{G-G_{\min}}{G_{\max}-G_{\min}}\right)^{|\mathrm{NL}_{\mathrm{LTD}}|-1}.
$$
When `NL_LTP = 1` and `NL_LTD = -1`, the model reduces to the identity STE used in the nominal experiments. Larger magnitudes increase the dependence of the update on the current conductance position: potentiation becomes weaker near $G_{\max}$ and depression becomes weaker near $G_{\min}$. This is still an optimizer-side abstraction rather than a pulse-by-pulse device simulator, but it provides a direct way to inject measured write asymmetry into training-time robustness studies.

Inference under variability is evaluated by Monte Carlo sampling. For a fixed checkpoint, the model is run repeatedly with fresh C2C draws, and accuracy is reported as mean $\pm$ standard deviation across $N$ stochastic forward passes. This allows us to separate the accuracy of a single trained set of weights from the uncertainty induced by hardware variability at deployment time.

## 3.5 Physical Frontend Compensation

To model the organic phototransistor front end, we use a sub-linear photocurrent response
$$
I_{\text{photo}} = \alpha P^{\gamma_{\text{phys}}} + I_{\text{dark}} + \eta_{\text{shot}},
$$
where $P$ denotes the incident optical signal, $\alpha$ is a responsivity scale, $\gamma_{\text{phys}}$ captures the non-linear transfer characteristic, $I_{\text{dark}}$ is dark current, and $\eta_{\text{shot}}$ is a signal-dependent stochastic term. The compensation mechanism applies an inverse-gamma preprocessing step
$$
P_{\text{in}} = X^{1/\gamma_{\text{phys}}},
$$
so that the subsequent device response becomes approximately linear in the original normalized input $X$.

This compensation is not treated as a universally beneficial transformation. Because shot-noise variance scales with photocurrent, inverse-gamma preprocessing also reshapes the noise statistics. The project’s A2.3 analysis shows that for $\gamma_{\text{phys}} < 1$, noise variance is amplified across the entire intensity range, even though dark-region signal differences may become relatively easier to separate. Consequently, the benefit of compensation must be interpreted as a task- and regime-dependent trade-off rather than as a free robustness improvement. In the current workflow, this front-end is used explicitly in the V6 Tiny-ViT experiment and analyzed separately from the weight-noise robustness experiments so that frontend compensation and hardware-aware training are not conflated.

## 3.6 Retention Decay Model

Post-programming weight drift is modeled with a double-exponential retention law. For a programmed conductance $G$ and elapsed inference time $t$, the decayed conductance is
$$
G(t) = G_{\min} + \left(G - G_{\min}\right)
\left[A_1 \exp\left(-t/\tau_1\right) + A_2 \exp\left(-t/\tau_2\right) + A_0\right],
$$
with $A_1 = A_2 = (1-A_0)/2$ and $A_0 = 0.6$. The default parameters are $\tau_1 = 140$ ms and $\tau_2 = 610$ ms, taken from the handbook’s device prior based on the DNTT retention measurements of Vincze et al. \citep{vincze2026dualplasticity}. This form captures an initial fast drop, an intermediate slower decay, and a non-zero persistent fraction. The codebase now additionally supports true state-dependent retention where high-conductance states decay faster, but the canonical evaluations in this paper isolate the uniform-decay behavior to maintain an analyzable physical baseline.

Retention is applied after conductance quantization and before the stochastic noise terms in the analog forward model. This ordering reflects the interpretation that weights are first programmed to discrete conductance levels, then drift in time, and are finally observed under fixed mismatch and read-time variability. In practice, retention sweeps are evaluated at logarithmically spaced times such as $t \in \{0,1,10,100,1000,10000\}$ s to reveal both the rapid early drop and the long-time plateau.

### First-Order Behavioral Measurement-to-Simulator Pipeline

The framework is designed so that literature priors and measured device statistics enter through the same parameter interface. This is important for a materials-facing workflow because early characterization rarely arrives as a single "device score." Instead, it is distributed across several measurement modalities such as multilevel programming, repeated same-state reads, cross-device statistics, retention fitting, and photoresponse characterization. The simulator therefore treats these measurements as structured calibration inputs rather than as informal narrative context.

Table 3 summarizes the direct mapping currently supported by the code path. In practical use, a literature-derived profile and an in-house measured profile are interchangeable objects: both populate the same conductance window, state count, variability, retention, and photoresponse fields, and therefore drive the same training or post-training evaluation scripts. This lets the present study serve as a baseline under literature priors while preserving a clean pathway for later device-specific recalibration.

| Measurement | Typical characterization method | Simulator parameter(s) |
|:--|:--|:--|
| Conductance window | Multilevel programming I-V sweep | `G_min`, `G_max`, `dynamic_range` |
| Resolvable state count | Programming resolution / histogram separability | `n_states` |
| Cycle-to-cycle variability | Repeated read/program at fixed target state | `sigma_c2c` |
| Device-to-device mismatch | Cross-device or cross-array statistics | `sigma_d2d` |
| Retention dynamics | Time-decay curve fit | `A_0`, `tau_1`, `tau_2` |
| Photoresponse nonlinearity | $I_{\text{photo}}$ vs intensity | `gamma_phys`, `responsivity_alpha`, `I_dark` |

## 3.7 Energy Estimation Model

Hybrid energy is estimated by summing analog MAC cost, ADC cost, DAC cost, digital MAC cost, special-operation cost, and memory-access cost:
$$
E_{\text{total}} =
E_{\text{analog}} + E_{\text{ADC}} + E_{\text{DAC}} + E_{\text{digital}} + E_{\text{buffer}}.
$$
For an analog layer with output dimension $M$, input dimension $N$, and $B$ effective input vectors (batch-size times token count), the current `EnergyProfiler` implementation accumulates
$$
E_{\text{analog}} = B M N \, E_{\text{analog-MAC}}, \qquad
E_{\text{ADC}} = B M \, E_{\text{ADC}}, \qquad
E_{\text{DAC}} = B N \, E_{\text{DAC}}.
$$
This means the present paper model charges one ADC conversion per output element and one DAC conversion per input element, rather than a more detailed tiling-aware term such as $BM\lceil N/128 \rceil$. The latter would be appropriate for a finer-grained peripheral model, but it is not what the current code implements. We therefore keep the manuscript aligned with the actual profiler and treat array-tiling overhead as future refinement rather than silently folding it into the reported numbers.

ADC non-idealities are modeled separately from the energy counts. For an $b$-bit converter, the continuous current is first quantized to $2^b$ nominal codes, and differential non-linearity (DNL) is injected by perturbing each step width:
$$
\Delta_{\text{actual}}[i] = \Delta_{\text{ideal}} \left(1 + \mathcal{N}(0, \sigma_{\text{DNL}}^2)\right),
$$
with $\sigma_{\text{DNL}} = 0.5$ LSB in the default configuration. In the implementation this perturbation is instantiated as a fixed per-ADC offset table, so the converter behaves analogously to a static D2D imperfection rather than fresh C2C noise. This DNL model is the theoretical basis for the ADC stress experiments C7 and C8, where the system is evaluated under aggressively quantized readout conditions.

Conductance quantization itself is still modeled as ideal uniform rounding rather than as a measured codebook with explicit integral non-linearity (INL). Accordingly, the present code should be described as a first-order behavioral simulation framework, not as a full physics-predictive emulator for arbitrary multilevel programming trajectories. Extending the framework toward measured level tables and explicit INL remains future work.

Digital convolution, dense residual paths, and attention-special operators are accumulated separately. Softmax and LayerNorm are charged per element, while optional SRAM or DRAM traffic is modeled through read counts.

Table 2 summarizes the constants used throughout the study. All values are anchored to the handbook’s 28 nm assumptions and should be interpreted as first-order system-model estimates rather than final silicon measurements.

| Component | Energy constant |
|:--|--:|
| Analog MAC | 100 fJ / MAC |
| Conservative analog MAC | 150 fJ / MAC |
| 8-bit ADC | 25 fJ / conversion |
| 8-bit DAC | 30 fJ / conversion |
| INT8 digital MAC | 0.4 pJ / MAC |
| FP32 digital MAC | 2.5 pJ / MAC |
| Softmax | 15 pJ / element |
| LayerNorm | 8 pJ / element |
| SRAM read (32-bit) | 5 pJ / access |
| DRAM read | 1300 pJ / access |

Array-to-digital interconnect energy is absorbed into the SRAM read/write cost terms in this model. Dedicated routing overhead, including data marshaling between the analog output bus and the digital coprocessor, is not separately itemized and represents a limitation of the present first-order estimate.
Position-dependent IR drop along crossbar wordlines and bitlines, as well as sneak-path currents in passive arrays, are not modeled in the current framework. These effects introduce systematic, input-pattern-dependent weight distortion that is distinct from the stochastic variability captured by our C2C and D2D terms. Incorporating SPICE-calibrated positional bias models is a natural extension for future work targeting specific array geometries.

Using these constants, the current Tiny-ViT dry-run estimates $273.94~\mu$J per hybrid inference versus $3137.14~\mu$J for the FP32 digital baseline, corresponding to an estimated $11.45\times$ energy reduction under the present mapping and operation-count assumptions. This estimate is intentionally separated from final accuracy results so that the eventual Pareto analysis can combine measured accuracy with the same accounting model.

## 3.8 Physical Modeling Simplifications (First-Order Behavioral Assumptions)

While this framework provides a robust bridge between device parameters and system accuracy, it is fundamentally a **first-order behavioral simulation framework**. To maintain computational tractability, several complex physical realities of organic optoelectronic devices are abstracted:

1. **Digital Overhead of Scale Masking**: The digital scale recovery mechanism (multiplying analog outputs by $\lVert \mathbf{W} \rVert_{\infty} / \Delta G$) is modeled as an exact floating-point operation in the digital domain. In physical hardware, this would require either high-precision digital multipliers or finely programmable TIA/ADC gains for every layer, which introduces hidden energy and area overheads not fully penalized in the current energy model.
2. **State-Independent Noise**: Cycle-to-cycle noise is injected as a global Gaussian perturbation scaled by the total dynamic range ($\Delta G$). In real devices, read and programming noise are strongly state-dependent (e.g., variance proportional to the conductance state).
3. **Idealized Uniform Quantization**: The conductance mapping assumes perfectly linear, uniformly spaced discrete levels. Actual crossbar arrays exhibit Integral Non-Linearity (INL) and Differential Non-Linearity (DNL). The current simulation does not use non-linear, measured conductance lookup tables.
4. **Uniform Retention Drift**: The double-exponential retention model decays the entire conductance contrast uniformly. Physical retention drift is typically state-dependent, with high-conductance states relaxing faster than low-conductance states.

These idealizations imply that the reported hardware-aware training (HAT) recovery and robustness limits represent an upper bound on performance. Future integrations with measured device data must explicitly address these non-idealities to move beyond behavioral estimation.

<!-- DATA_DEPENDENCY: Numerical mapping counts and dry-run energy estimates are fixed; this section is no longer blocked by pending training runs. -->
