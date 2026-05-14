# Local GPU Drift-Regularized State-Dependent Pilot — Seed123

Date: 2026-05-14 13:20 CST
Owner: Codex
Evidence grade: provisional

## Goal

Test whether a state-dependent retention regularizer, evaluated under a matched
state-dependent retention lane, can improve protection lift even if it changes
the absolute checkpoint quality.

## Configuration

Training:

- warm-start checkpoint:
  `checkpoints/_ensemble/cifar100_seed123/V4_hybrid_standard_noise_hat_best.pt`
- tag:
  `regw5e-3_t1000_state_dep`
- `drift_reg_weight = 0.005`
- `drift_reg_time = 1000 s`
- `drift_reg_state_dependent = True`
- `drift_reg_include_substrings = stages.3`

Checkpoint:

- `checkpoints/_drift_aware/cifar100_seed123_regw5e-3_t1000_state_dep/V4_hybrid_standard_noise_hat_best.pt`

## Source-Domain Comparison

Matched 3-run source eval:

- baseline:
  `67.2467%`
- state-dependent candidate:
  `67.0433%`
- delta:
  `-0.2033 pp`

Interpretation:

- source-domain cost remains small
- unlike the state-independent pilots, this run does not fail immediately on source accuracy

## Retention/Protection Comparison vs Original Seed123 Baseline

Summary:

- `thesis/results/drift_aware_sam/drift_aware_retention_driftreg_seed123_10x3_summary_regw5e-3_t1000_state_dep_20260514_124134.tsv`

Absolute deltas:

- `fresh_all_analog`
  - `0s`: `-1.3904 pp`
  - `1000s`: `-1.5173 pp`
  - `10000s`: `-1.5597 pp`
- `freeze_top30_d2d`
  - `0s`: `-0.6553 pp`
  - `1000s`: `-0.4450 pp`
  - `10000s`: `-0.4943 pp`
- `freeze_top42_d2d`
  - `0s`: `-0.2597 pp`
  - `1000s`: `+0.0044 pp`
  - `10000s`: `-0.1657 pp`

Lift-relative deltas versus `fresh_all_analog`:

- `top30`
  - `0s`: `+0.7351 pp`
  - `1000s`: `+1.0723 pp`
  - `10000s`: `+1.0654 pp`
- `top42`
  - `0s`: `+1.1307 pp`
  - `1000s`: `+1.5217 pp`
  - `10000s`: `+1.3940 pp`

Interpretation:

- this is the first pilot that actually improves protection lift
- but it does so by sacrificing the underlying fresh-all checkpoint quality
- in other words, the regularizer redistributes robustness rather than giving a free gain

## Ranking Diagnostic

Overlap with the original seed123 drift-aware ranking:

- top-`10`: `9/10`
- top-`30`: `30/30`
- top-`42`: `42/42`

Interpretation:

- the protected-set membership still does not change
- the improvement comes from the checkpoint dynamics, not from a different top-`K` set

## Verdict

Mixed but scientifically useful pilot.

Compared with the two state-independent pilots:

- global regularizer: negative
- stage3-filtered regularizer: negative but slightly better
- state-dependent stage3-filtered regularizer: first pilot with clearly positive lift deltas, but paid for by a lower `fresh_all_analog` floor

This means the state-dependent lane is the first one that looks mechanistically real, but it is not yet deployment-improving in absolute terms.

## Next Step

The right next variant is not another broad sweep. It should target the tradeoff directly:

1. lower `drift_reg_weight` under the same state-dependent setup, or
2. regularize only the most retention-sensitive late layers inside `stages.3`

The objective is now clear:

- keep the positive lift effect,
- recover the `fresh_all_analog` floor.
