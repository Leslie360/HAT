# P14-B CIFAR-10 Data-Fraction Ablation Plan

## Goal

Address the reviewer request for a minimal, controlled test of the `data-floor` hypothesis behind HAT failure on small datasets.

The paper-facing design is deliberately small:

- model: `Tiny-ViT-5M`
- dataset: `CIFAR-10`
- experiment: `V4`
- seed: `42`
- fractions: `10%`, `25%`, `50%`, `100%`
- training length: `100 epochs`

This isolates the effect of training-set size while keeping architecture, optimizer family, and analog regime fixed.

## Implementation Status

- `train_tinyvit.py` now supports `--data-fraction`
- the flag subsets the **training split only**
- the held-out test set remains unchanged
- the subset is deterministic for a given seed

## Launch Script

- `/home/qiaosir/projects/compute_vit/scripts/_gpt/run_tinyvit_cifar10_data_ablation_gpt.sh`

## Reviewer-Facing Use

If lower fractions show a monotonic degradation of `V4`, the paper can frame the Flowers-102 result more carefully as:

> a low-data boundary for HAT-like stochastic training, rather than proof that Flowers-102 fails for one single reason.

If the CIFAR-10 ablation stays stable even at low fractions, that would instead weaken the current `data-floor` story and push the explanation toward domain mismatch or recipe mismatch.
