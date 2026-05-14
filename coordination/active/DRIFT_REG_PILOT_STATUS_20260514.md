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

## Active Pilot

Detached session:

- `tmux` session: `drift_reg_pilot_seed123_20260514`

Active log:

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

## Current Readout

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

## Ranking-Difference Diagnostic

The rebuilt ranking already exists:

- `thesis/results/drift_aware_sam/drift_aware_ranking_driftreg_seed123_1000s_20260514_092715.tsv`

Important detail:

- top-`30` overlap with the old seed123 drift-aware ranking: `30/30`
- top-`42` overlap with the old seed123 drift-aware ranking: `42/42`

So this pilot does **not** currently change the protected-set membership. If the downstream retention/protection summary improves, the gain is coming from the checkpoint itself rather than from a different top-`K` layer set.

## Decision Criteria

This pilot is a success only if both conditions hold:

1. source-domain cost is small:
   - ideally `<= 1 pp` below the original seed123 source-domain level
2. retention/protection improves on the old seed123 drift-aware baseline:
   - especially `top30` and `top42` at `1000s` / `10000s`

If source-domain drops materially while retention does not improve, this lane should be treated as a negative pilot and the next step should be:

- try smaller `drift_reg_weight`, or
- move to a mixed objective that regularizes only late-stage analog layers

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
