# GEMINI E1/E2 DESIGN MEMO — 2026-04-18

## Overview
This document specifies the experimental protocols for E1 (Cross-architecture γ scan) and E2 (Cross-dataset γ robustness), intended to broaden the validation of the inverse-gamma frontend compensation.

**Note**: This is a design-only memo; no GPU execution has been initiated.

## E1: Cross-Architecture γ Scan

**Goal:** Verify whether the +5.8 pp accuracy recovery (at γ_phys=2.0) observed in Tiny-ViT (A2.3) holds true across fundamentally different architectural priors (ResNet-18 and ConvNeXt-Tiny). This isolates the compensation benefit from ViT-specific attention map dynamics (T3).

**Checkpoints (HAT-trained on standard noise):**
- **ResNet-18:** `checkpoints/R4_4bit_noise_HAT_best.pt`
- **ConvNeXt-Tiny:** `checkpoints/C4_4bit_noise_HAT_best.pt`

**Parameters:**
- **γ_phys (photoresponse exponent):** [0.5, 0.7, 1.0, 1.5, 2.0]
- **I_dark (dark current):** 10 pA, 100 pA, 1 nA, 10 nA
- **Dataset:** CIFAR-10
- **Noise:** Standard (σ_c2c=0.05, σ_d2d=0.10)

**Execution Protocol:**
- Inference-only evaluation using the 5×4 γ/I_dark grid.
- Two variants per cell: `raw` (no compensation) vs `compensated` (gamma_comp = 1/gamma_phys).
- Metric: 10 Monte Carlo runs per setting (mean ± std).
- **Target Script:** Implement a script, e.g., `run_arch_gamma_sweep.py`, that loads the specified models and iteratively tests them against the frontend simulator.

## E1b: Cross-Architecture with HAT+γ Joint Retraining

**Goal:** Determine if models can actively learn to exploit inverse-gamma compensation during HAT training, moving beyond inference-only transfer.

**Checkpoints:**
- **Missing — needs training** (Initialize from FP32 baselines: R1, C1, V1).

**Parameters:**
- **Architectures:** ResNet-18, ConvNeXt-Tiny, Tiny-ViT
- **γ_phys:** 2.0 (fixed)
- **I_dark:** 10 pA
- **Noise:** Standard (σ_c2c=0.05, σ_d2d=0.10)

**Execution Protocol:**
- Retrain from FP32 baselines with HAT + inverse-gamma frontend enabled.
- 100 epochs, cosine schedule matching the existing HAT recipe, 3 seeds.
- Compare final accuracy against HAT-without-frontend (R4/C4/V4 anchors) and HAT+frontend-inference-only (E1).
- **Target Script / CLI Invocation:** `python scripts/_gpt/run_learnable_gamma_compensation_gpt.py --gamma_phys 2.0 --epochs 100 --seed <seed>` (extended for ResNet/ConvNeXt) or equivalent `train_*.py`.
- **Runtime Estimate:** ~15 GPU-hours (3 arch × 3 seeds × ~1.5 h).
- **Thesis-Chapter Role:** Architecture Generalization (demonstrating whether different topological priors can jointly optimize for both noise and physical frontend compensation).
- **Risks / Gotchas:** Requires extending the inverse-gamma frontend logic into `train_resnet18.py` and `train_convnext.py`.

## E2: Cross-Dataset γ Robustness

**Goal:** Ensure the frontend compensation efficacy scales to more complex tasks and different data distributions, reinforcing the "edge-vision" generalizability claim.

**Checkpoints (Tiny-ViT, HAT-trained):**
- **CIFAR-100:** `checkpoints/_gpt/cifar100/V4_hybrid_standard_noise_hat_best.pt`
- **Flowers-102:** `checkpoints/_gpt/flowers102/V4_hybrid_standard_noise_hat_best.pt`

**Parameters:**
- **Architecture:** Tiny-ViT-5M
- **γ_phys:** [0.5, 0.7, 1.0, 1.5, 2.0]
- **I_dark:** Fixed at 10 pA (or a targeted subset of the grid to save compute)
- **Noise:** Standard (σ_c2c=0.05, σ_d2d=0.10)

**Execution Protocol:**
- Inference-only evaluation using the selected γ/I_dark settings on the CIFAR-100 and Flowers-102 test sets.
- Compare `raw` vs `compensated`.
- Metric: 10 Monte Carlo runs per setting.
- **Target Script:** Can share the same infrastructure as E1, explicitly overriding the dataset loader configuration.

## E2b: Cross-Dataset γ Robustness (TinyImageNet + SVHN)

**Goal:** Extend frontend compensation validation to 200-class and digits data distributions to support broader dataset robustness claims.

**Checkpoints:**
- **TinyImageNet:** **Missing — needs training** (data in `data/tiny-imagenet-200/`).
- **SVHN:** **Missing — needs training** (data in `data/test_32x32.mat`).

**Parameters:**
- **Architecture:** Tiny-ViT-5M
- **γ_phys:** [0.5, 0.7, 1.0, 1.5, 2.0]
- **I_dark:** 10 pA
- **Noise:** Standard (σ_c2c=0.05, σ_d2d=0.10)

**Execution Protocol:**
- Inference-only evaluation using the γ/I_dark grid on the TinyImageNet and SVHN test sets.
- Compare `raw` vs `compensated` with 10 Monte Carlo runs per setting.
- **Target Script / CLI Invocation:** `python run_arch_gamma_sweep.py --dataset tinyimagenet` and `python run_arch_gamma_sweep.py --dataset svhn` (or equivalent).
- **Runtime Estimate:** ~2 GPU-hours (inference only, once checkpoints exist).
- **Thesis-Chapter Role:** Dataset Robustness (proving inverse-gamma compensation benefits scale across highly distinct feature distributions).
- **Risks / Gotchas:** Cannot execute the γ sweep until the prerequisite HAT-trained base checkpoints are generated for TinyImageNet and SVHN.

## E5: Layer-Wise γ Sensitivity on Tiny-ViT

**Goal:** Localize which structural components (patch-embed, MLP, attention) benefit most from inverse-gamma compensation to identify the primary bottleneck.

**Checkpoints:**
- `checkpoints/V4_hybrid_standard_noise_hat_best.pt`

**Parameters:**
- **Dataset:** CIFAR-10
- **γ_phys:** 2.0
- **Compensation Targets:** {Patch-Embed Only, MLP Only, Attention Proj Only, All Analog}

**Execution Protocol:**
- Apply inverse-gamma compensation selectively to specific layer groups while leaving others raw.
- Evaluate accuracy across 3 seeds using the V4 HAT checkpoint.
- **Target Script / CLI Invocation:** E.g., `python scripts/_gpt/run_layer_gamma_sensitivity_gpt.py --layer_target MLP --gamma_phys 2.0` (mimicking `run_nl_gradient_distortion_gpt.py`'s hook/injection pattern).
- **Runtime Estimate:** ~1 GPU-hour (inference ablation).
- **Thesis-Chapter Role:** Layer Localization (pinpointing where photocurrent non-linearity is most destructive within the ViT topology).
- **Risks / Gotchas:** Requires custom forward-hook logic to simulate frontend compensation effects deeply within the network if the photoresponse simulator is strictly placed at the initial image input.

## E6: γ × NL Joint Sweep

**Goal:** Determine whether read-side inverse-gamma compensation interacts with and recovers the severe write-side NL=2.0 failure mode.

**Checkpoints:**
- **Missing — needs training.**

**Parameters:**
- **Architecture:** Tiny-ViT-5M (CIFAR-10)
- **γ_phys:** {1.0, 2.0}
- **NL (LTP/LTD):** {0 (linear), 1.0, 1.5, 2.0}

**Execution Protocol:**
- Retrain 16 conditions: combinations of (no compensation / inverse-gamma / MLP-linear mitigation / both).
- Standard HAT training (100 epochs) across 3 seeds per cell = 48 runs total.
- **Target Script / CLI Invocation:** E.g., `python train_tinyvit_ensemble.py --gamma_phys <gamma> --nl_ltp <nl> --nl_ltd -<nl> --seed <seed> --epochs 100` (incorporating combined mitigation flags).
- **Runtime Estimate:** ~200 GPU-hours (48 runs × ~4 hours).
- **Thesis-Chapter Role:** Mechanism Interaction (exploring whether read-side compensation and write-side non-linearity mitigations stack synergistically or interfere).
- **Risks / Gotchas:** Extremely high compute cost; requires integrating both the InverseGammaPreprocessor and the NL MLP-linear gradient correction into a unified training script.

## Evidence Matrix

| Experiment | Description | Paper Main | Paper Supp | Thesis Only | Priority | Runtime Estimate | Status |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **E1** | Cross-Architecture γ Scan (Inference) | | ✓ | | High | ~2 h | Design Ready |
| **E1b** | Cross-Arch HAT+γ Joint Retraining | | | ✓ | Medium | ~15 h | Needs Training |
| **E2** | Cross-Dataset γ Robustness (CIFAR100/Flowers) | | ✓ | | High | ~2 h | Design Ready |
| **E2b** | Cross-Dataset γ Robustness (TinyImageNet/SVHN) | | | ✓ | Low | ~2 h | Needs Training |
| **E3** | Learnable Frontend Compensation Exponent | ✓ | | | High | ~3 h | Running / Done |
| **E5** | Layer-Wise γ Sensitivity Ablation | | | ✓ | Medium | ~1 h | Design Ready |
| **E6** | γ × NL Joint Sweep (Interaction) | | | ✓ | High | ~200 h | Needs Training |
