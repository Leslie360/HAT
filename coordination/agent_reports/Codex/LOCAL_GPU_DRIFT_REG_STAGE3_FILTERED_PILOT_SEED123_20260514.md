# Local GPU Drift-Regularized Stage-3 Filtered Pilot — Seed123

Date: 2026-05-14 11:00 CST
Owner: Codex
Evidence grade: provisional

## Goal

Follow up the negative global drift-regularized pilot with a narrower regularizer:

- keep the same state-independent retention evaluation protocol,
- regularize only late-stage analog layers whose names contain `stages.3`,
- test whether concentrated late-layer pressure improves retention/protection more than the global regularizer.

## Configuration

Training:

- warm-start checkpoint:
  `checkpoints/_ensemble/cifar100_seed123/V4_hybrid_standard_noise_hat_best.pt`
- tag:
  `regw5e-3_t1000_stage3`
- `drift_reg_weight = 0.005`
- `drift_reg_time = 1000 s`
- `drift_reg_state_dependent = False`
- `drift_reg_include_substrings = stages.3`

Checkpoint:

- `checkpoints/_drift_aware/cifar100_seed123_regw5e-3_t1000_stage3/V4_hybrid_standard_noise_hat_best.pt`

## Source-Domain Comparison

Matched 3-run source eval:

- baseline:
  `67.3633%`
- stage3-filtered candidate:
  `67.1533%`
- delta:
  `-0.2100 pp`

Interpretation:

- source-domain cost remains small
- this pilot still preserves the checkpoint reasonably well

## Retention/Protection Comparison vs Original Seed123 Drift-Aware Baseline

Summary:

- `thesis/results/drift_aware_sam/drift_aware_retention_driftreg_seed123_10x3_summary_regw5e-3_t1000_stage3_20260514_101736.tsv`

Absolute deltas:

- `fresh_all_analog`
  - `0s`: `+0.6643 pp`
  - `1000s`: `+0.8313 pp`
  - `10000s`: `+0.7026 pp`
- `freeze_top30_d2d`
  - `0s`: `-0.1456 pp`
  - `1000s`: `+0.0724 pp`
  - `10000s`: `+0.0867 pp`
- `freeze_top42_d2d`
  - `0s`: `-0.0810 pp`
  - `1000s`: `+0.1530 pp`
  - `10000s`: `-0.0084 pp`

Lift-relative deltas versus `fresh_all_analog`:

- `top30`
  - `0s`: `-0.8099 pp`
  - `1000s`: `-0.7589 pp`
  - `10000s`: `-0.6159 pp`
- `top42`
  - `0s`: `-0.7453 pp`
  - `1000s`: `-0.6783 pp`
  - `10000s`: `-0.7110 pp`

Interpretation:

- unlike the global pilot, this stage3-filtered version does raise the protected strategies at some time points in absolute terms
- but it raises `fresh_all_analog` even more
- therefore the protection advantage actually gets worse

## Comparison vs Global Pilot

Compared with the first global regularizer:

- stage3-filtered is numerically better on almost every absolute accuracy row
- but still not good enough to improve the protection lift that matters

So the stage3 filter is a better direction than the global regularizer, but it is still a negative pilot under the current success criterion.

## Ranking Diagnostic

Top-set overlap with the original seed123 drift-aware ranking:

- top-`10`: `9/10`
- top-`30`: `30/30`
- top-`42`: `42/42`

Interpretation:

- the filter changes ordering slightly inside the top tail,
- but not enough to change the actual top-`30` / top-`42` membership

## Verdict

Negative pilot, but directionally better than the global regularizer.

## Next Step

Do not keep tuning the same state-independent ranking-preserving setup by tiny increments.

The next meaningful variant should change one of these assumptions:

1. **state-dependent retention regularizer + state-dependent eval lane**
2. **regularizer tied directly to top-`K` protected layers or late MLP outputs**
3. **ranking-aware objective that penalizes drift on the current top-risk subset more strongly than on the rest**
