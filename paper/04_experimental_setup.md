# 4. Experimental Setup

## 4.1 Models and Datasets

We evaluate three vision backbones that span increasing architectural complexity. ResNet-18 serves as the initial end-to-end validation platform because it is easy to instrument and historically well understood on CIFAR-10. 

To ensure our analog framework's robustness across different deployment paradigms, we utilize two distinct high-capacity testbeds: 
(1) **ConvNeXt-Tiny**, trained entirely **from scratch**, to evaluate analog adaptation and noise robustness from random initialization. Its weights are almost entirely static and therefore naturally compatible with analog mapping.
(2) **Tiny-ViT-5M**, fine-tuned from **ImageNet pre-trained weights**, to evaluate the analog deployment of foundation models. This hybrid architecture combines transformer-style dense projections mapped to the crossbar with a non-trivial set of digital-only operators such as local depthwise convolution, LayerNorm, and dynamic attention products.

The study therefore uses two complementary deployment testbeds rather than one monolithic benchmark. ConvNeXt-Tiny is trained from scratch under analog constraints and serves as a convolutional adaptation-from-random-initialization testbed. Tiny-ViT-5M is fine-tuned from ImageNet pre-trained weights and serves as the deployment-oriented transformer testbed for foundation-model transfer into the analog regime. This distinction is intentional: it lets us test both analog adaptation from scratch and analog deployment of a compact pre-trained model within the same framework.

All primary experiments are conducted on CIFAR-10. CIFAR-100 is reserved as a generalization check for the Tiny-ViT pipeline after the main CIFAR-10 experiments stabilize. Images are resized to match the backbone requirements in the Tiny-ViT path, while the ResNet-18 and ConvNeXt-Tiny pipelines retain standard CIFAR-style augmentation. Across all models, the reported metric is top-1 test accuracy on the official test split.

The core training hyperparameters are summarized below.

| Model | Optimizer | Epochs | Batch size | Learning rate | Weight decay | Scheduler |
|:--|:--|--:|--:|--:|--:|:--|
| ResNet-18 | SGD | 200 | 128 | 0.1 | $5\times10^{-4}$ | Cosine annealing |
| ConvNeXt-Tiny | AdamW | 200 | 256 | $4\times10^{-3}$ | 0.05 | Cosine annealing |
| Tiny-ViT-5M | AdamW | 100 | 64 | $5\times10^{-4}$ | 0.05 | Cosine annealing |

ResNet-18 uses the default training-script batch size of 128 throughout the archived A2.1 package. ConvNeXt-Tiny is a small but important exception: while the script default remains 128, the finalized GPT rerun configuration used for the paper-facing ConvNeXt package adopts batch size 256, and the table above reflects that execution configuration. Tiny-ViT-5M uses the values defined directly in `train_tinyvit.py`, including `weight_decay=0.05`.

Mixed precision is available in the current GPT execution path, but it should not be treated as a universal property of every archived result. For the historical paper-facing ConvNeXt C4 package, the hard evidence recovered so far is: (i) the archived successful canonical log `train_convnext_restart_20260403_2154_gpt.log`, which records the `89.91%` C4 result under the original multi-experiment ConvNeXt suite, and (ii) the canonical checkpoint metadata, which fixes `batch_size=256`. By contrast, an explicit `AMP: off` line is directly confirmed only for the later Task-36 proportional-noise extension, not for the canonical C4 log itself. We therefore treat batch size and checkpoint lineage as the primary historical anchors, while avoiding stronger claims about AMP than the surviving canonical records support. Tiny-ViT retains the CUDA-accelerated mixed-precision path where explicitly enabled. In all cases, the STE-sensitive conductance mapping and scale-recovery steps are protected from unwanted autocasting so that AMP acceleration does not silently alter the analog simulation logic.

At the present stage, all reported device parameters are literature-anchored priors loaded via a JSON-based device profile interface, ensuring the simulator logic is decoupled from hardware-specific assumptions. For the canonical organic optoelectronic experiments in this paper, we synthesized a "Standard Organic Profile" based on recent measurements of state-of-the-art organic synaptic transistors [Guo et al. 2024; Vincze et al. 2025; Xu et al. 2025]. Specifically, we configure: an on/off ratio $G_{\max}/G_{\min}=10$ typical of scalable OPECTs, 4-bit weight resolution ($n_{states}=16$), standard Gaussian noise parameters of $\sigma_{\text{C2C}}=5\%$ and $\sigma_{\text{D2D}}=10\%$ derived from multi-cycle read variability, and a dual-exponential retention drift with time constants $\tau_1=140$ms and $\tau_2=610$ms anchored to empirical retention curves [Vincze et al. 2025]. For physical stress tests, non-linear weight update asymmetry is set to $NL_{LTP}=+2.0$ and $NL_{LTD}=-2.0$. By codifying these parameters in a swappable profile, the framework provides a direct materials-to-system linkage: once future in-house measured device statistics are finalized, the exact same training and inference pipelines can be re-run with measured profiles instead of literature priors.

More broadly, the current experiments should be interpreted as a first-order behavioral simulation campaign under literature-anchored calibration. While the framework is already structured to accept measured device profiles, the reported numbers are not yet claimed as fully predictive of any single fabricated chip without further validation against measured integral non-linearity (INL) tables.

## 4.2 Experiment Matrix

The experimental program is organized into three families. The ResNet family (R-series) establishes the core noise-and-HAT behavior. The ConvNeXt family (C-series) extends that behavior to a larger convolutional model and adds retention analysis. The Tiny-ViT family (V-series) implements the final hybrid analog/digital deployment target.

### ResNet-18 matrix

| Exp | Purpose | Analog? | Noise setting | Training mode |
|:--|:--|:--:|:--|:--|
| R1 | FP32 digital baseline | No | None | Standard |
| R2 | 4-bit quantized, no noise | Yes | None | Standard |
| R3 | Standard noisy deployment baseline | Yes | C2C 5\%, D2D 10\% | Standard |
| R4 | Main HAT result | Yes | C2C 5\%, D2D 10\% | HAT |
| R5 | Pessimistic robustness stress test | Yes | C2C 10\%, D2D 20\% | HAT |
| R6 | Higher state-count sensitivity | Yes | C2C 5\%, D2D 10\%, 6-bit | HAT |

### ConvNeXt-Tiny matrix

| Exp | Purpose | Analog? | Noise / peripheral setting | Training mode |
|:--|:--|:--:|:--|:--|
| C1 | FP32 digital baseline | No | None | Standard |
| C2 | 4-bit quantized, no noise | Yes | None | Standard |
| C3 | Standard noisy deployment baseline | Yes | C2C 5\%, D2D 10\% | Standard |
| C4 | Main HAT result | Yes | C2C 5\%, D2D 10\% | HAT |
| C5 | Pessimistic robustness stress test | Yes | C2C 10\%, D2D 20\% | HAT |
| C6 | State-count sensitivity | Yes | 6-bit, C2C 5\%, D2D 10\% | HAT |
| C7 | ADC stress test | Yes | 4-bit ADC proxy | HAT |
| C8 | Moderate ADC quantization | Yes | 6-bit ADC proxy | HAT |
| C9 | Retention sweep | Yes | Time sweep on C4 checkpoint | Evaluation only |

### Tiny-ViT-5M matrix

| Exp | Purpose | Hybrid? | Noise / frontend setting | Training mode |
|:--|:--|:--:|:--|:--|
| V1 | FP32 digital baseline | No | None | Standard |
| V2 | Hybrid quantized, no noise | Yes | None | Standard |
| V3 | D2D-adapted non-HAT baseline | Yes | Standard noise at eval; fixed D2D during train | Standard train w/ fixed D2D |
| V4 | Main HAT result | Yes | C2C 5\%, D2D 10\% | HAT |
| V5 | Pessimistic robustness stress test | Yes | C2C 10\%, D2D 20\% | HAT |
| V6 | Physical-front-end experiment | Yes | V4 + inverse-gamma phototransistor front end | HAT |
| ~~V7~~ | Legacy retention-aware checkpoint (excluded) | Yes | Preliminary retention path with broken scale semantics | Excluded from canonical results |

The V3 wording is intentionally precise. Following Claude review, V3 should not be described as a direct analog of ConvNeXt C3. Instead, it represents a "Standard train w/ fixed D2D" baseline designed to expose the model to static device mismatch during optimization without enabling full per-forward C2C stochastic training.

V7 is retained only as an implementation-history note. It was trained before the corrected retention fix recalibrated the post-drift weight scale and decayed the D2D buffers consistently. Because that checkpoint does not transfer to the corrected retention path, the canonical Tiny-ViT result family for this paper is V1--V6 plus the corrected V4 retention sweep.

In addition to the canonical matrix above, four physical-extension experiments were conducted on CIFAR-10 to probe richer device models. `V4_proportional_HAT` repeats the V4 protocol for 100 epochs with state-dependent proportional noise (`\sigma \propto |G|`) and is evaluated with 10-run Monte Carlo sweeps under both proportional-noise and uniform-noise semantics. `V4_NL2_HAT` repeats V4 for 100 epochs with nonlinear-write dynamics active during STE gradient computation (`NL_LTP = +2.0`, `NL_LTD = -2.0`) and is likewise evaluated with 10-run Monte Carlo sampling. `V4_Ensemble_HAT` keeps the canonical Tiny-ViT V4 recipe but resamples the fixed D2D realization at each training epoch; its final transferability result is reported on 10 fresh hardware instances with 5 Monte Carlo evaluations per instance. Finally, `C4_proportional_HAT` applies the proportional-noise HAT protocol to ConvNeXt-Tiny for 200 epochs as a cross-architecture comparison. These four experiments are treated as physical-extension studies rather than as part of the canonical grouped cross-dataset figures.

## 4.3 Evaluation Protocol

For each training run, we record the best test accuracy observed across epochs and save both the best checkpoint and the latest checkpoint for crash recovery. When analog noise is active at inference time, evaluation is performed with **10 Monte Carlo sampling runs per setting** so that each checkpoint yields a mean accuracy and standard deviation over repeated stochastic forward passes. The ResNet and ConvNeXt reports already use this protocol for noisy experiments, and the Tiny-ViT path adopts the same convention.

Retention is evaluated by reloading a fixed checkpoint and sweeping the programmed-weight age over logarithmically spaced times, typically $t \in \{0,1,10,100,1000,10000\}$ s. The ConvNeXt C9 experiment uses 20 Monte Carlo draws per time point. The Tiny-ViT implementation now uses the same interface under the corrected retention semantics, including dynamic scale recalibration and decayed D2D buffers during retention evaluation.

Energy estimates are reported separately from training accuracy. The hybrid profiler accumulates layer-wise analog and digital operation counts using the same mapping rules as the deployment code, which prevents inconsistencies between reported analog coverage and claimed energy savings. Final Pareto plots will therefore combine measured accuracy from the completed experiment matrix with energy numbers extracted from the common profiling code path rather than from hand-written spreadsheets.

The same principle applies to future measured-device studies. Once our own OPECT characterization is available, the post-training sweeps can be rerun by loading measured conductance windows, effective state counts, fitted D2D/C2C statistics, and retention constants from a structured profile file. In that way, the experimental protocol remains fixed while only the material-specific calibration layer is changed.

<!-- DATA_DEPENDENCY: The experiment definitions and hyperparameters are fixed. -->

## 4.4 Reproducibility and Transparency

To ensure computational reproducibility, we centralize the execution metadata, checkpoint identities, and Monte Carlo semantics used throughout the paper. The archived train/eval entry points expose explicit seed control together with deterministic cuDNN settings, but we do not claim cross-platform bitwise identity across hardware, drivers, or mixed-precision kernels. The practical target is therefore seeded execution-trace reproducibility through released configs, logs, and checkpoint lineage. The canonical Tiny-ViT V4 path is now locked through a three-seed summary rather than a single rerun sanity check: seed-42, seed-123, and seed-2026 yield noisy-MC means of `87.64 ± 0.48%`, `88.10 ± 0.33%`, and `88.11 ± 0.47%`, giving a cross-seed aggregate of `87.95 ± 0.27%`. Below is the centralized metadata for the experimental execution:
- **Optimization**: ResNet-18 (SGD, LR=$0.1$), ConvNeXt-Tiny (AdamW, LR=$4\times 10^{-3}$), and Tiny-ViT-5M (AdamW, LR=$5\times 10^{-4}$). All utilize Cosine Annealing learning rate schedules. Weight decay is set to $5\times 10^{-4}$ for ResNet-18 and $0.05$ for ConvNeXt/Tiny-ViT.
- **Hardware-Aware Training (HAT)**: The HAT loss function employs Straight-Through Estimators (STE) with additive per-forward standard Gaussian noise injected natively during the training loop.
- **Epochs and Batch Size**: ResNet-18 (200 epochs, batch 128); ConvNeXt-Tiny (200 epochs, batch 256); Tiny-ViT-5M (100 epochs, batch 64).
- **Evaluation Semantics**: All noisy inference evaluations are derived from multi-pass Monte Carlo (MC) sampling (e.g., 10 runs per checkpoint evaluation setting, 20 runs for specific retention sweeps). The reported metrics are exclusively the mean and standard deviation across these repeated stochastic passes.
- **Checkpoint Selection**: Cross-dataset comparisons report the best-epoch checkpoint, while Monte Carlo test metrics report distributions around those locked checkpoints.
- **Code and Data**: The simulation framework, device profile schema, and training scripts will be released as open-source upon publication. A summary of device parameter derivations and source literature is provided in the Appendix to guarantee transparent parameter provenance.
