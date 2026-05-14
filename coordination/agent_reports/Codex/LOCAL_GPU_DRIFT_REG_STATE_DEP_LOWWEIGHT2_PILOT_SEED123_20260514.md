# Local GPU Drift-Regularized State-Dependent Very-Low-Weight Pilot — Seed123

Date: 2026-05-14 15:10 CST
Owner: Codex
Evidence grade: provisional

## Goal

Test whether reducing the state-dependent regularizer weight further, from `0.005`
 to `0.002`, can retain the protection-lift gain while recovering more of the
absolute checkpoint floor.

## Configuration

Training:

- warm-start checkpoint:
  `checkpoints/_ensemble/cifar100_seed123/V4_hybrid_standard_noise_hat_best.pt`
- tag:
  `regw2e-3_t1000_state_dep`
- `drift_reg_weight = 0.002`
- `drift_reg_time = 1000 s`
- `drift_reg_state_dependent = True`
- `drift_reg_include_substrings = stages.3`

Checkpoint:

- `checkpoints/_drift_aware/cifar100_seed123_regw2e-3_t1000_state_dep/V4_hybrid_standard_noise_hat_best.pt`

## Source-Domain Comparison

Matched 3-run source eval:

- baseline:
  `67.3367%`
- candidate:
  `67.2967%`
- delta:
  `-0.0400 pp`

Interpretation:

- source-domain cost is almost zero
- this run preserves the checkpoint slightly better than the `0.005` state-dependent run

## Retention/Protection Comparison vs Original Seed123 Baseline

Summary:

- `thesis/results/drift_aware_sam/drift_aware_retention_driftreg_seed123_10x3_summary_regw2e-3_t1000_state_dep_20260514_141535.tsv`

Absolute deltas:

- `fresh_all_analog`
  - `+0.6486 / +0.7073 / +0.6266 pp`
- `freeze_top30_d2d`
  - `-0.2776 / -0.0733 / -0.0903 pp`
- `freeze_top42_d2d`
  - `-0.0637 / +0.1134 / -0.0534 pp`

Lift-relative deltas versus `fresh_all_analog`:

- `top30`
  - `-0.9262 / -0.7806 / -0.7169 pp`
- `top42`
  - `-0.7123 / -0.5939 / -0.6800 pp`

Interpretation:

- lowering the weight further clearly recovers the absolute floor
- but the positive lift effect disappears completely

## Comparison vs the `0.005` State-Dependent Pilot

The `0.005` pilot had:

- slightly worse source/fresh-all floor
- but strongly positive lift deltas:
  - `top30`: `+0.7351 / +1.0723 / +1.0654 pp`
  - `top42`: `+1.1307 / +1.5217 / +1.3940 pp`

This `0.002` pilot has:

- better floor
- but negative lift deltas everywhere

So the lower weight does not improve the Pareto point; it moves back toward the
state-independent behavior.

## Verdict

Negative for the main objective.

This closes the scalar-weight tuning question tightly enough for now:

- high state-dependent weight (`0.005`) gives mechanism but hurts floor
- lower state-dependent weight (`0.002`) restores floor but loses mechanism

## Next Step

Do not continue another scalar weight sweep immediately.

The next useful move must change objective structure:

1. top-risk-subset-weighted state-dependent regularizer
2. late-MLP-output-weighted state-dependent regularizer
3. direct protected-set-stability objective
