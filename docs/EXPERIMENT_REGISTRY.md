# Experiment Registry

This document records the canonical experiment families used by the paper.

## Tiny-ViT

- `V1`: FP32 digital baseline
- `V2`: quantized deployment without explicit noise-aware training
- `V3`: standard noisy deployment without HAT
- `V4`: canonical HAT result under uniform noise
- `V6`: physical frontend experiments
- `V8`: retention-aware retraining

Stress and extension tasks:

- `Task 34`: proportional-noise HAT
- `Task 35`: nonlinear-write HAT
- `Task 37`: Ensemble HAT for fresh-instance robustness

## ConvNeXt

- `C1`: FP32 digital baseline
- `C3`: standard noisy deployment without HAT
- `C4`: canonical HAT result

Stress and extension tasks:

- `Task 36`: proportional-noise HAT

## Datasets

- `CIFAR-10`: low-complexity calibration regime
- `CIFAR-100`: medium-complexity cross-dataset validation
- `Flowers-102`: low-data boundary condition

## Reporting Discipline

- `best` and Monte Carlo `mean ± std` must never be mixed
- fresh-instance results and literature-profile transfer results must remain
  distinct
- Flowers-102 discussion must remain hypothesis-level rather than causal proof
