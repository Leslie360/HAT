# Local GPU Drift-Aware Protection Pilot — 2026-05-13

Date: 2026-05-13 21:59 CST
Owner: Codex
Evidence grade: provisional pilot

## Goal

Test whether a protection ranking derived from measured drift-vector magnitude is more retention-aligned than the current D2D-sensitivity ranking, using the existing TinyViT V4 CIFAR-100 retention/protection harness.

## Setup

Checkpoint:

- `checkpoints/_ensemble/cifar100_seed789/V4_hybrid_standard_noise_hat_best.pt`

Drift ranking source:

- `thesis/results/drift_aware_sam/drift_vectors_profile_20260512_004906.tsv`
- converted to:
  - `thesis/results/drift_aware_sam/drift_aware_ranking_1000s_20260513.tsv`

Protocol:

- dataset: CIFAR-100
- model: TinyViT V4 Ensemble HAT seed789
- protected K: `0, 30, 42`
- retention times: `0, 1000, 10000 s`
- `5` fresh D2D instances × `2` MC
- `--recalibrate_scale --scale_d2d`

Outputs:

- raw:
  `thesis/results/drift_aware_sam/drift_aware_protection_pilot_20260513_214829.tsv`
- summary:
  `thesis/results/drift_aware_sam/drift_aware_protection_pilot_summary_20260513_214829.tsv`

Log:

- `logs/local_gpu_drift_aware_protection_pilot_20260513_214829.log`

## Ranking overlap

Compared with the current D2D-sensitivity top-K source:

- top30 overlap = `21 / 30`
- top42 overlap = `42 / 42`

So the pilot is not a trivial replay of the same top30 subset. The drift-aware ranking pulls in more late-stage MLP/attention layers and drops several earlier patch/attention-projection layers from the top30 set.

## Result summary

### New drift-aware pilot

- `fresh_all_analog`
  - 0s: `58.554±0.473%`
  - 1000s: `55.864±0.423%`
  - 10000s: `55.674±0.729%`
- `top30`
  - 0s: `63.246±0.559%`
  - 1000s: `60.489±0.422%`
  - 10000s: `60.659±0.562%`
- `top42`
  - 0s: `64.888±0.111%`
  - 1000s: `62.169±0.201%`
  - 10000s: `62.160±0.124%`

### Previous D2D-sensitivity 10×3 reference

- `fresh_all_analog`
  - 0s: `58.223±1.386%`
  - 1000s: `55.596±1.229%`
  - 10000s: `55.403±1.272%`
- `top30`
  - 0s: `62.051±0.587%`
  - 1000s: `59.207±0.608%`
  - 10000s: `59.223±0.606%`
- `top42`
  - 0s: `62.248±0.510%`
  - 1000s: `59.392±0.605%`
  - 10000s: `59.391±0.482%`

## Delta vs previous ranking

- `fresh_all_analog`: essentially unchanged (`+0.27` to `+0.33 pp`)
- `top30`: improved by `+1.20`, `+1.28`, `+1.44 pp`
- `top42`: improved by `+2.64`, `+2.78`, `+2.77 pp`

## Verdict

This pilot is positive.

The gain is not caused by a better underlying fresh-all baseline, because `fresh_all_analog` stayed nearly unchanged. The improvement appears specifically in the protected configurations, especially `top42`, which suggests that a drift-informed ranking is more aligned with long-horizon retention stress than the current D2D-sensitivity ranking alone.

This is still only a pilot:

- `5×2`, not the full `10×3`
- one checkpoint family
- no new optimizer yet

But it is strong enough to change the recommended next step:

1. expand this drift-aware protection lane to a full `10×3` confirmation;
2. only then invest in a heavier drift-aware optimization / SAM-style training intervention.
