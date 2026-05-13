# Local GPU Drift-Aware Protection 10x3 — Seed789

Date: 2026-05-14 00:36 CST
Owner: Codex
Evidence grade: provisional

## Goal

Upgrade the positive drift-aware protection pilot into a full `10 fresh D2D instances × 3 MC` confirmation on the TinyViT V4 CIFAR-100 seed789 checkpoint, using the same retention/protection harness as the current D2D-sensitivity baseline.

## Inputs

Checkpoint:

- `checkpoints/_ensemble/cifar100_seed789/V4_hybrid_standard_noise_hat_best.pt`

Drift-aware ranking:

- `thesis/results/drift_aware_sam/drift_aware_ranking_1000s_20260513.tsv`

Protocol:

- protected K: `0, 30, 42`
- retention times: `0, 1000, 10000 s`
- `10` fresh instances × `3` MC
- `--recalibrate_scale --scale_d2d`
- base seed aligned to the prior `10×3` retention/protection lane: `20260516`

Outputs:

- raw:
  `thesis/results/drift_aware_sam/drift_aware_protection_10x3_20260514_000408.tsv`
- summary:
  `thesis/results/drift_aware_sam/drift_aware_protection_10x3_summary_20260514_000408.tsv`
- log:
  `logs/local_gpu_drift_aware_protection_10x3_20260514_000408.log`

## Result summary

### Drift-aware ranking lane

- `fresh_all_analog`
  - `0s`: `58.2263±1.3784%`
  - `1000s`: `55.6023±1.2284%`
  - `10000s`: `55.4053±1.2755%`
- `freeze_top30_d2d`
  - `0s`: `63.4317±0.5030%`
  - `1000s`: `60.7837±0.4718%`
  - `10000s`: `60.7303±0.5769%`
- `freeze_top42_d2d`
  - `0s`: `64.9507±0.0985%`
  - `1000s`: `62.2200±0.1012%`
  - `10000s`: `62.2033±0.1237%`

### Previous D2D-sensitivity lane

- `fresh_all_analog`
  - `0s`: `58.2230±1.3856%`
  - `1000s`: `55.5963±1.2285%`
  - `10000s`: `55.4033±1.2715%`
- `freeze_top30_d2d`
  - `0s`: `62.0510±0.5865%`
  - `1000s`: `59.2073±0.6078%`
  - `10000s`: `59.2230±0.6060%`
- `freeze_top42_d2d`
  - `0s`: `62.2477±0.5095%`
  - `1000s`: `59.3923±0.6049%`
  - `10000s`: `59.3910±0.4820%`

## Delta vs previous ranking

- `fresh_all_analog`
  - `0s`: `+0.0033 pp`
  - `1000s`: `+0.0060 pp`
  - `10000s`: `+0.0020 pp`
- `top30`
  - `0s`: `+1.3807 pp`
  - `1000s`: `+1.5764 pp`
  - `10000s`: `+1.5073 pp`
- `top42`
  - `0s`: `+2.7030 pp`
  - `1000s`: `+2.8277 pp`
  - `10000s`: `+2.8123 pp`

## Interpretation

This is no longer just a small pilot. Under the matched `10×3` protocol, the drift-aware ranking reproduces the same fresh-all baseline as the current D2D-sensitivity lane, but improves both protected settings.

The gain is therefore not explained by a favorable instance draw. It appears specifically in the protection ranking:

- moderate gain for `top30`
- large and consistent gain for `top42`

The drift-aware lane also reduces the standard deviation of `top42` sharply, especially at `1000s` and `10000s`, indicating that the protection set is not only stronger in mean accuracy but also more stable across fresh instances.

## Verdict

Positive provisional result.

The next local GPU priority should now be:

1. finish the same drift-aware `10×3` confirmation on `seed456`;
2. if the direction survives seed456, treat drift-aware ranking as the preferred protection heuristic for the thesis/Paper3 retention lane;
3. only after that, implement a heavier drift-aware optimization / SAM-style training intervention.
