# Drift-Regularized Pilot Status

Date: 2026-05-14 09:35 CST
Owner: Codex
Branch: `codex-exchange-20260511`

## Objective

Move the local drift-aware retention lane from a ranking heuristic into a method lane by adding a small retention-drift regularizer to the TinyViT Ensemble HAT trainer.

This pilot is intentionally narrow:

- checkpoint family: `cifar100_seed123`
- base experiment: `V4_hybrid_standard_noise_hat`
- initialization: warm-start from the existing seed123 V4 best checkpoint
- goal: test whether a light drift-aware regularizer can improve downstream retention/protection without immediately collapsing source-domain accuracy

## Implementation State

Code landed in:

- `src/compute_vit/train_tinyvit_ensemble.py`
- `scripts/run_cifar100_drift_regularized_pilot_seed123_20260514.sh`

New CLI flags:

- `--drift-reg-weight`
- `--drift-reg-time`
- `--drift-reg-state-dependent`

Current penalty form:

- mean absolute effective-weight drift power across analog layers
- measured after retention at the requested time
- evaluated before sampled D2D/C2C noise injection

## Important Correction

The first draft used a relative drift ratio:

- `drift_power / base_power`

Under state-independent retention this became effectively constant, because all conductances shrink by the same factor. Logs exposed the issue directly:

- `drift_penalty=0.160000` at every epoch

That first long run was invalid as a method test and was stopped.

The current form instead uses:

- `mean((retained_effective - base_effective)^2)`

This is not constant and does provide gradient information.

## Smoke Validation

1-epoch warm-start smoke passed after the fix:

- `test_acc=62.58%`
- `drift_penalty=0.570607`

This only validates that the penalty is live and training still runs.

## Pilot Run

Run log:

- `logs/cifar100_drift_regularized_pilot_seed123_20260514_092715.log`

Current save dir:

- `checkpoints/_drift_aware/cifar100_seed123_regw5e-3_t1000`

Current hyperparameters:

- warm-start from `checkpoints/_ensemble/cifar100_seed123/V4_hybrid_standard_noise_hat_best.pt`
- `epochs=12`
- `early_stop_patience=6`
- `lr=1e-4`
- `drift_reg_weight=0.005`
- `drift_reg_time=1000`
- `drift_reg_state_dependent=False`

Post-train chain in the launcher:

1. source eval
2. drift-vector profile
3. rebuilt drift-aware ranking
4. full retention/protection `10x3`

## Final Readout

Training phase finished with early stop:

- best checkpoint epoch: `5`
- best test accuracy during train: `67.49%`

Source eval (3 runs) completed:

- file:
  `thesis/results/drift_aware_sam/drift_reg_pilot_eval_seed123_20260514_092715.json`
- mean source accuracy:
  `67.13%`
- run-to-run std:
  `0.07 pp`

Practical interpretation:

- relative to the original seed123 train best `67.75%`, the source-domain cost is about `-0.62 pp`
- that is small enough that the pilot remains worth finishing through the retention/protection stage
- note:
  this first eval JSON was produced before the eval-path metadata fix landed, so the
  `drift_regularizer_*` fields inside that file are stale. A metadata-corrected eval
  plus a matched baseline source eval are queued in the postprocess watcher and should
  be treated as the final source-domain comparison artifacts.

Matched source-domain comparison after postprocess:

- baseline seed123 source eval:
  `67.1533%`
- drift-regularized checkpoint source eval:
  `67.1400%`
- delta:
  `-0.0133 pp`

So the source-domain cost is effectively zero at the matched eval level.

## Ranking-Difference Diagnostic

The rebuilt ranking already exists:

- `thesis/results/drift_aware_sam/drift_aware_ranking_driftreg_seed123_1000s_20260514_092715.tsv`

Important detail:

- top-`30` overlap with the old seed123 drift-aware ranking: `30/30`
- top-`42` overlap with the old seed123 drift-aware ranking: `42/42`

So this pilot does **not** change the protected-set membership. Any downstream gain would have to come from the checkpoint itself rather than from a different top-`K` layer set.

## Retention/Protection Outcome

Final summary:

- `thesis/results/drift_aware_sam/drift_aware_retention_driftreg_seed123_10x3_summary_20260514_092715.tsv`

Compared with the old seed123 drift-aware baseline:

- `fresh_all_analog`
  - `+0.0996 / +0.1140 / +0.0483 pp` at `0 / 1000 / 10000 s`
- `freeze_top30_d2d`
  - `-0.2856 / -0.0810 / -0.0347 pp`
- `freeze_top42_d2d`
  - `-0.3090 / -0.0896 / -0.2147 pp`

Lift-relative deltas versus `fresh_all_analog`:

- `top30`: `-0.3852 / -0.1950 / -0.0830 pp`
- `top42`: `-0.4086 / -0.2036 / -0.2630 pp`

Interpretation:

- the checkpoint became marginally better on `fresh_all_analog`,
- but the protected strategies did not improve,
- so the pilot fails the actual retention/protection objective.

## Decision Criteria

This pilot was a success only if both conditions held:

1. source-domain cost is small:
   - ideally `<= 1 pp` below the original seed123 source-domain level
2. retention/protection improves on the old seed123 drift-aware baseline:
   - especially `top30` and `top42` at `1000s` / `10000s`

Outcome:

- source-domain stayed essentially unchanged,
- retention/protection did not improve,
- therefore this is a **negative pilot**.

## Stage-3 Filtered Follow-Up

A second pilot was run immediately after the global one:

- regularizer filter:
  `stages.3`
- tag:
  `regw5e-3_t1000_stage3`

Matched source-domain comparison:

- baseline:
  `67.3633%`
- stage3-filtered candidate:
  `67.1533%`
- delta:
  `-0.2100 pp`

Retention/protection comparison vs original seed123 drift-aware baseline:

- `fresh_all_analog`
  - `+0.6643 / +0.8313 / +0.7026 pp`
- `freeze_top30_d2d`
  - `-0.1456 / +0.0724 / +0.0867 pp`
- `freeze_top42_d2d`
  - `-0.0810 / +0.1530 / -0.0084 pp`

But lift-relative deltas are still all negative:

- `top30`
  - `-0.8099 / -0.7589 / -0.6159 pp`
- `top42`
  - `-0.7453 / -0.6783 / -0.7110 pp`

Interpretation:

- stage3 filtering is numerically better than the global regularizer,
- but still fails the real objective because it lifts `fresh_all_analog` even more than the protected strategies.

## Current Next Step

Do not keep tuning the same state-independent setup by tiny increments.

The next meaningful variant should change one of these assumptions:

1. state-dependent retention regularizer + matched state-dependent eval lane
2. top-risk-subset-weighted regularizer
3. explicit late-MLP / top-`K` ranking-aware objective

## State-Dependent Follow-Up

A third pilot was run with a matched state-dependent train/eval lane:

- tag:
  `regw5e-3_t1000_state_dep`
- filter:
  `stages.3`
- regularizer:
  state-dependent
- eval lane:
  state-dependent retention enabled

Matched source-domain comparison:

- baseline:
  `67.2467%`
- candidate:
  `67.0433%`
- delta:
  `-0.2033 pp`

Absolute retention deltas vs original seed123 baseline:

- `fresh_all_analog`
  - `-1.3904 / -1.5173 / -1.5597 pp`
- `freeze_top30_d2d`
  - `-0.6553 / -0.4450 / -0.4943 pp`
- `freeze_top42_d2d`
  - `-0.2597 / +0.0044 / -0.1657 pp`

Lift-relative deltas versus `fresh_all_analog`:

- `top30`
  - `+0.7351 / +1.0723 / +1.0654 pp`
- `top42`
  - `+1.1307 / +1.5217 / +1.3940 pp`

Interpretation:

- this is the first pilot that improves protection lift,
- but it does so by lowering the fresh-all checkpoint floor.

Current best reading:

- the state-dependent lane is mechanistically real,
- but it is not yet an absolute deployment improvement.

## Updated Next Step

The next rational variant is:

1. keep the state-dependent setup,
2. reduce `drift_reg_weight`, and/or
3. regularize only the most retention-sensitive late layers within `stages.3`

The target is now explicit:

- preserve the lift gain,
- recover the `fresh_all_analog` floor.

## Fourth Pilot In Flight

A fourth pilot is now running with exactly one variable changed relative to the
third pilot:

- state-dependent retention regularizer
- `stages.3` filter
- `drift_reg_weight = 0.002`
- tag:
  `regw2e-3_t1000_state_dep`

Current background sessions:

- `tmux` session: `drift_reg_pilot_state_dep_w2_20260514`
- watcher: `drift_reg_post_state_dep_w2_20260514`

Early readout:

- epoch `0/12`: `test_acc=67.18%`
- epoch `1/12`: `test_acc=66.82%`

This run is intentionally not interpreted yet; wait for the matched source eval
and full retention/protection summary before judging whether the lower weight
recovers the `fresh_all_analog` floor without losing the positive lift effect.

## Fourth Pilot Outcome

The low-weight state-dependent pilot finished with:

- tag:
  `regw2e-3_t1000_state_dep`
- matched source eval delta:
  `-0.0400 pp`

Absolute retention deltas vs original seed123 baseline:

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

- lowering the state-dependent regularizer weight recovers the absolute floor,
- but it eliminates the positive lift effect that made the higher-weight state-dependent run interesting.

Matched source-domain comparison:

- baseline:
  `67.3367%`
- candidate:
  `67.2967%`
- delta:
  `-0.0400 pp`

## Current Best Reading

Across four pilots:

1. global state-independent: negative
2. stage3-filtered state-independent: negative
3. stage3-filtered state-dependent (`0.005`): mixed but mechanistically real
4. stage3-filtered state-dependent (`0.002`): source preserved, lift lost

So the best current conclusion is:

- state-dependent regularization is the first lane that truly changes the retention/protection mechanism,
- but the current scalar penalty still does not yield a good Pareto point between `fresh_all_analog` and protection lift.

## Current Next Step

Do not open another scalar-weight sweep immediately.

The next useful variant should change the objective structure:

1. top-risk-subset-weighted state-dependent regularizer
2. late-MLP-output-weighted state-dependent regularizer
3. protected-set-stability-oriented objective

## First Readout Checklist

When the active pilot finishes, check these files first:

1. training summary:
   - `thesis/results/drift_aware_sam/drift_reg_pilot_train_seed123_<stamp>.json`
2. source eval:
   - `thesis/results/drift_aware_sam/drift_reg_pilot_eval_seed123_<stamp>.json`
3. rebuilt ranking:
   - `thesis/results/drift_aware_sam/drift_aware_ranking_driftreg_seed123_1000s_<stamp>.tsv`
4. retention/protection summary:
   - `thesis/results/drift_aware_sam/drift_aware_retention_driftreg_seed123_10x3_summary_<stamp>.tsv`

Compare against:

- original seed123 train best:
  - `67.75%`
- original seed123 drift-aware retention/protection summary:
  - `thesis/results/drift_aware_sam/drift_aware_protection_seed123_10x3_summary_20260514_011900.tsv`
