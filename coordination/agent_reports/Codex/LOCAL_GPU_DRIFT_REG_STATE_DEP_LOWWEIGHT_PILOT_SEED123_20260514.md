# Local GPU Drift-Regularized State-Dependent Low-Weight Pilot — Seed123

Date: 2026-05-14 15:00 CST
Owner: Codex
Evidence grade: provisional

## Goal

Test whether lowering the state-dependent regularizer weight can keep the positive
lift effect from the previous state-dependent pilot while recovering the
`fresh_all_analog` floor.

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
- low-weight candidate:
  `67.2967%`
- delta:
  `-0.0400 pp`

Interpretation:

- source-domain cost is almost zero
- this pilot preserves the checkpoint noticeably better than the higher-weight state-dependent run

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

- lowering the weight successfully recovers the absolute floor
- but it destroys the positive protection-lift effect seen at weight `0.005`

## Comparison vs Higher-Weight State-Dependent Pilot

Compared with `regw5e-3_t1000_state_dep`:

- source-domain is better preserved
- `fresh_all_analog` is much higher
- but the positive lift signal disappears completely

So the lower-weight pilot does not improve the tradeoff; it just moves back toward
the state-independent behavior.

## Verdict

Negative for the main objective.

This pilot shows that simply lowering the weight is not enough: the mechanism
becomes too weak to improve protected-vs-fresh lift.

## Final Method-Line Reading

Across the four pilots:

1. global, state-independent: negative
2. stage3-filtered, state-independent: negative
3. stage3-filtered, state-dependent, weight `0.005`: mixed but mechanistically real
4. stage3-filtered, state-dependent, weight `0.002`: source preserved, lift lost

The best current scientific conclusion is:

- **state-dependent regularization is the first lane that actually changes the retention/protection mechanism**
- but the current scalar penalty does not yet give a good Pareto point between source floor and protection lift

## Next Step

Do not open another broad scalar-weight sweep immediately.

The next useful variant should change objective structure, not just scale:

1. top-risk-subset-weighted state-dependent regularizer
2. explicit late-MLP-output-weighted regularizer
3. regularizer that emphasizes `top42`-style protected-set stability directly
