# Local GPU Drift-Aware Protection 10x3 — Seed123

Date: 2026-05-14 01:25 CST
Owner: Codex
Evidence grade: provisional

## Goal

Close the third TinyViT V4 CIFAR-100 checkpoint on the drift-aware retention/protection lane, so the local heuristic is no longer supported by only two checkpoints.

## Inputs

Checkpoint:

- `checkpoints/_ensemble/cifar100_seed123/V4_hybrid_standard_noise_hat_best.pt`

Drift-aware ranking:

- `thesis/results/drift_aware_sam/drift_aware_ranking_seed123_1000s_20260514_011900.tsv`

Protocol:

- protected K: `0, 30, 42`
- retention times: `0, 1000, 10000 s`
- `10` fresh instances × `3` MC
- `--recalibrate_scale --scale_d2d`
- base seed: `20260521`

Outputs:

- raw:
  `thesis/results/drift_aware_sam/drift_aware_protection_seed123_10x3_20260514_011900.tsv`
- summary:
  `thesis/results/drift_aware_sam/drift_aware_protection_seed123_10x3_summary_20260514_011900.tsv`
- log:
  `logs/local_gpu_drift_aware_seed123_batch_20260514_011900.log`

## Result summary

- `fresh_all_analog`
  - `0s`: `63.2497±0.8280%`
  - `1000s`: `60.9010±0.8102%`
  - `10000s`: `60.9537±0.7880%`
- `freeze_top30_d2d`
  - `0s`: `66.4673±0.3097%`
  - `1000s`: `64.0343±0.4215%`
  - `10000s`: `64.0320±0.3494%`
- `freeze_top42_d2d`
  - `0s`: `67.2830±0.1062%`
  - `1000s`: `64.8983±0.1137%`
  - `10000s`: `65.0227±0.1121%`

## Delta vs fresh-all baseline

- `top30`
  - `0s`: `+3.2176 pp`
  - `1000s`: `+3.1333 pp`
  - `10000s`: `+3.0783 pp`
- `top42`
  - `0s`: `+4.0333 pp`
  - `1000s`: `+3.9973 pp`
  - `10000s`: `+4.0690 pp`

## Interpretation

This closes the checkpoint loop cleanly:

- seed789 gave the first matched `10×3` comparison against the older D2D-sensitivity ranking;
- seed456 confirmed the same direction on a stronger checkpoint family;
- seed123 now shows that the uplift is still present on the earliest checkpoint of the same CIFAR-100 lane.

The absolute gain is larger here than on seed456/seed789 when measured against the within-run `fresh_all` baseline, which suggests the heuristic is not narrowly tuned to a single checkpoint geometry.

The old seed123 sensitivity-based fresh-instance run used a different instance draw, so this report does not treat the `0s` comparison as a strict matched A/B against the old ranking. The important point is narrower and safer: the drift-aware ranking remains clearly positive across all three tested retention horizons on a third checkpoint.

## Verdict

Positive provisional closure.

The local drift-aware retention lane now has three checkpoints pointing in the same direction. The next high-value step is no longer more heuristic confirmation; it is a first drift-aware optimization or SAM-style training intervention.
