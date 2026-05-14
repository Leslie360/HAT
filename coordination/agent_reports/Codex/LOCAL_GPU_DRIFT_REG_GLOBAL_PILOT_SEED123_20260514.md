# Local GPU Drift-Regularized Global Pilot — Seed123

Date: 2026-05-14 10:12 CST
Owner: Codex
Evidence grade: provisional

## Goal

Test the first method-level extension beyond ranking-only drift awareness:

- start from the existing CIFAR-100 TinyViT V4 Ensemble HAT seed123 checkpoint,
- add a light retention-drift regularizer during warm-start fine-tuning,
- then re-run source eval, drift profiling, ranking build, and full retention/protection `10x3`.

## Configuration

Training:

- warm-start checkpoint:
  `checkpoints/_ensemble/cifar100_seed123/V4_hybrid_standard_noise_hat_best.pt`
- `lr = 1e-4`
- `epochs = 12`
- `early_stop_patience = 6`
- `drift_reg_weight = 0.005`
- `drift_reg_time = 1000 s`
- `drift_reg_state_dependent = False`
- no module filter; all analog layers regularized equally

Resulting checkpoint:

- `checkpoints/_drift_aware/cifar100_seed123_regw5e-3_t1000/V4_hybrid_standard_noise_hat_best.pt`

## Source-Domain Comparison

Matched 3-run eval on the original seed123 checkpoint:

- baseline:
  `67.1533%`

Matched 3-run eval on the drift-regularized checkpoint:

- candidate:
  `67.1400%`

Delta:

- `-0.0133 pp`

Interpretation:

- source-domain cost is essentially zero at the matched eval level
- the regularizer did not meaningfully damage the checkpoint

## Retention/Protection Comparison

Baseline summary:

- `thesis/results/drift_aware_sam/drift_aware_protection_seed123_10x3_summary_20260514_011900.tsv`

Candidate summary:

- `thesis/results/drift_aware_sam/drift_aware_retention_driftreg_seed123_10x3_summary_20260514_092715.tsv`

Absolute deltas:

- `fresh_all_analog`
  - `0s`: `+0.0996 pp`
  - `1000s`: `+0.1140 pp`
  - `10000s`: `+0.0483 pp`
- `freeze_top30_d2d`
  - `0s`: `-0.2856 pp`
  - `1000s`: `-0.0810 pp`
  - `10000s`: `-0.0347 pp`
- `freeze_top42_d2d`
  - `0s`: `-0.3090 pp`
  - `1000s`: `-0.0896 pp`
  - `10000s`: `-0.2147 pp`

Lift-relative deltas versus `fresh_all_analog`:

- `top30`
  - `0s`: `-0.3852 pp`
  - `1000s`: `-0.1950 pp`
  - `10000s`: `-0.0830 pp`
- `top42`
  - `0s`: `-0.4086 pp`
  - `1000s`: `-0.2036 pp`
  - `10000s`: `-0.2630 pp`

Interpretation:

- the checkpoint got slightly better on `fresh_all_analog`
- but the protected strategies got slightly worse
- the pilot therefore did **not** improve the retention/protection objective that actually matters

## Ranking Diagnostic

Rebuilt ranking:

- `thesis/results/drift_aware_sam/drift_aware_ranking_driftreg_seed123_1000s_20260514_092715.tsv`

Overlap with the old seed123 drift-aware ranking:

- top-`30`: `30/30`
- top-`42`: `42/42`

Interpretation:

- this global regularizer did not change protected-set membership at all
- the failure is therefore not a ranking-construction bug
- it is a method-design issue: the global state-independent regularizer is too uniform to reshape the late-layer retention bottleneck

## Verdict

Negative pilot.

This first global drift-regularized fine-tune is not worth promoting:

- source-domain is preserved,
- but retention/protection does not improve,
- and ranking membership is unchanged.

## Next Step

Do not repeat the same global state-independent regularizer.

The next rational variants are:

1. **late-stage filtered regularizer**
   - e.g. regularize only modules whose names contain `stages.3`
2. **state-dependent regularizer + matched state-dependent eval lane**
   - only if we explicitly want to move the whole evaluation protocol

The immediate low-risk follow-up is the first one, because it keeps the current state-independent retention evaluation protocol unchanged while introducing non-uniform pressure across layers.
