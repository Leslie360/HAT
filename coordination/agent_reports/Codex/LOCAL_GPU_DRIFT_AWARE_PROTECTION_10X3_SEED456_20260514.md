# Local GPU Drift-Aware Protection 10x3 — Seed456

Date: 2026-05-14 00:52 CST
Owner: Codex
Evidence grade: provisional

## Goal

Cross-check the positive seed789 drift-aware protection result on a stronger TinyViT V4 CIFAR-100 checkpoint, using the same retention/protection harness and the same `10 fresh D2D instances × 3 MC` protocol.

## Inputs

Checkpoint:

- `checkpoints/_ensemble/cifar100_seed456/V4_hybrid_standard_noise_hat_best.pt`

Drift-aware ranking:

- `thesis/results/drift_aware_sam/drift_aware_ranking_seed456_1000s_20260514_001732.tsv`

Protocol:

- protected K: `0, 30, 42`
- retention times: `0, 1000, 10000 s`
- `10` fresh instances × `3` MC
- `--recalibrate_scale --scale_d2d`
- base seed: `20260520`

Outputs:

- raw:
  `thesis/results/drift_aware_sam/drift_aware_protection_seed456_10x3_20260514_003908.tsv`
- summary:
  `thesis/results/drift_aware_sam/drift_aware_protection_seed456_10x3_summary_20260514_003908.tsv`
- log:
  `logs/local_gpu_drift_aware_protection_seed456_10x3_20260514_003908.log`

## Result summary

- `fresh_all_analog`
  - `0s`: `63.2940±0.8503%`
  - `1000s`: `61.2480±0.8760%`
  - `10000s`: `61.2450±0.7773%`
- `freeze_top30_d2d`
  - `0s`: `65.3847±0.4609%`
  - `1000s`: `63.3120±0.3977%`
  - `10000s`: `63.1883±0.3545%`
- `freeze_top42_d2d`
  - `0s`: `66.6080±0.1360%`
  - `1000s`: `64.5563±0.1391%`
  - `10000s`: `64.4913±0.1469%`

## Delta vs fresh-all baseline

- `top30`
  - `0s`: `+2.0907 pp`
  - `1000s`: `+2.0640 pp`
  - `10000s`: `+1.9433 pp`
- `top42`
  - `0s`: `+3.3140 pp`
  - `1000s`: `+3.3083 pp`
  - `10000s`: `+3.2463 pp`

## Interpretation

This agrees with the seed789 direction and does so on a stronger checkpoint family.

The result matters for two reasons:

1. the gain persists after the checkpoint baseline moves upward by about `5 pp`;
2. the gain remains retention-time stable, not just a `0s` artifact.

So the local retention lane now has two checkpoints pointing the same way:

- a matched seed789 comparison where drift-aware ranking beats the older D2D-sensitivity ranking while leaving `fresh_all_analog` unchanged;
- a seed456 confirmation where the same ranking produces a clear `top30/top42` uplift above the fresh-all baseline at `0/1000/10000 s`.

## Verdict

Positive provisional confirmation.

The drift-aware ranking should now be treated as the preferred local retention/protection heuristic. The next method-level step is no longer "see whether this idea works at all," but "decide whether to stop at ranking or invest in drift-aware training/optimization."
