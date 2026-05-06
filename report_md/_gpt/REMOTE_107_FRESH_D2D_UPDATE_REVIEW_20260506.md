# Remote 107 Fresh-D2D Update Review

Date: 2026-05-06
Reviewer: Codex
Remote branch: `origin/107-clean`
Remote HEAD after fetch: `37df860 D2D seed ablation + fresh-D2D cross-instance results (auto)`
Prior reviewed commit: `aca7dd5`
Local action: fetched and inspected only; no merge into local paper branch.

## 1. Executive Verdict

Remote 107 has now closed the main missing Work-2 KV-cache question from the previous audit: selective terminal-layer HAT was evaluated across fresh D2D device seeds.

Scientific route verdict:

- Strong positive for selective terminal-layer analog KV-cache plus HAT.
- Last-layer-only (`analog_layers=[23]`) is substantially more robust than all-layer analog KV under fresh D2D.
- Fresh-D2D variance is very small for last1/last2, which supports a real cross-device robustness story rather than same-device memorization.
- Do not merge `107-clean` into local Paper-1 branch. Keep it as a standalone Work-2 deliverable branch.

Canonical-status verdict:

- Numeric trend is usable for route planning.
- Exact PPL values are still `PROVISIONAL` for paper use because JSON outputs do not include the full required metadata packet (`git_commit`, `script`, `mode`, `model`, dataset split, command line, separate train/eval D2D seed fields).
- Request one small metadata/summary cleanup from 107 before locking these as canonical.

## 2. New GitHub Update

New commits after `aca7dd5`:

1. `b0ecb4d` - fixes selective checkpoint naming in `pipeline_fresh_d2d.py`.
2. `37df860` - adds fresh-D2D cross-instance results and selective last1/last2 training JSONs.

Changed payload:

- `pipeline_fresh_d2d.py`
- `results/d2d_seed_ablation/.pipeline_fresh_d2d_state.json`
- 30 selective fresh-D2D eval JSONs:
  - last1: 3 eval D2D levels x 5 eval D2D seeds
  - last2: 3 eval D2D levels x 5 eval D2D seeds
- 2 selective training JSONs:
  - `hat_d2d002_500_freshd2d_last1_seed42.json`
  - `hat_d2d002_500_freshd2d_last2_seed42.json`

Pipeline completion state:

- completed tasks: 62/62
- started: `2026-05-06 09:45:16`
- finished: `2026-05-06 09:57:32`

Syntax verification on archived branch:

```text
python -m py_compile deliverable/code/p3_hat_train.py deliverable/code/p3_hat_eval.py pipeline_d2d_seed.py pipeline_fresh_d2d.py pipeline_runner.py pipeline_next.py
PY_COMPILE_OK
```

## 3. Aggregated Fresh-D2D Results

### 3.1 All-layer reference, fixed training D2D seed 42

| checkpoint | eval D2D | n eval seeds | mean PPL | std | min | max |
|---|---:|---:|---:|---:|---:|---:|
| all-layer train D2D=0.02 | 0.02 | 5 | 26.05 | 0.53 | 25.17 | 26.50 |
| all-layer train D2D=0.02 | 0.04 | 5 | 44.34 | 2.65 | 40.08 | 46.74 |
| all-layer train D2D=0.02 | 0.05 | 5 | 66.84 | 5.91 | 57.65 | 73.06 |
| all-layer train D2D=0.04 | 0.02 | 5 | 27.97 | 0.40 | 27.34 | 28.45 |
| all-layer train D2D=0.04 | 0.04 | 5 | 38.35 | 1.68 | 35.58 | 40.11 |
| all-layer train D2D=0.04 | 0.05 | 5 | 47.98 | 3.13 | 42.78 | 51.13 |

Interpretation:

- Training at higher D2D buys high-D2D robustness.
- D2D=0.04 training is worse at eval D2D=0.02, but much better at eval D2D=0.04/0.05.
- This closes the earlier qualitative trend under explicit fresh D2D seed override for all-layer checkpoints.

### 3.2 Selective terminal-layer fresh-D2D

| checkpoint | analog layers | eval D2D | n eval seeds | mean PPL | std | min | max |
|---|---|---:|---:|---:|---:|---:|---:|
| last1 train D2D=0.02 | `[23]` | 0.02 | 5 | 18.42 | 0.02 | 18.40 | 18.45 |
| last1 train D2D=0.02 | `[23]` | 0.04 | 5 | 18.55 | 0.03 | 18.52 | 18.58 |
| last1 train D2D=0.02 | `[23]` | 0.05 | 5 | 18.60 | 0.03 | 18.56 | 18.63 |
| last2 train D2D=0.02 | `[22,23]` | 0.02 | 5 | 18.71 | 0.02 | 18.69 | 18.74 |
| last2 train D2D=0.02 | `[22,23]` | 0.04 | 5 | 19.07 | 0.04 | 19.03 | 19.13 |
| last2 train D2D=0.02 | `[22,23]` | 0.05 | 5 | 19.21 | 0.04 | 19.17 | 19.26 |

Interpretation:

- Last1 is the best deployment route in this batch.
- Last1 barely degrades from eval D2D=0.02 to 0.05: mean PPL `18.42 -> 18.60`.
- Last2 is also robust but consistently worse than last1.
- Both selective routes are dramatically better than all-layer fresh-D2D at the same eval noise.

## 4. Route Decision

Current Work-2 priority should be:

1. Primary route: selective terminal-layer analog KV-cache, starting with last1.
2. Secondary route: last2 if reviewers demand more capacity/coverage than last1.
3. All-layer analog KV: use as stress-test/control, not deployment route.
4. Higher-D2D training: useful for all-layer robustness but apparently unnecessary for last1 under this tested range.

This is a clean pivot away from all-layer KV as the paper-facing deployment claim.

## 5. Remaining Metadata Gaps

The result JSONs are numerically useful but not fully canonical. Example eval JSON keys:

```text
['analog_layers', 'checkpoint_dir', 'd2d_seed', 'n_states', 'ppl', 'retention_step_time', 'sigma_c2c', 'sigma_d2d']
```

Missing relative to the requested return template:

- `git_commit`
- `script`
- `mode`
- `model`
- `dataset_eval`
- `train_seed`
- `train_d2d_seed`
- `eval_d2d_seed` as a separate explicit field
- exact `command`

This does not invalidate the trend because filenames, branch commit, pipeline state, and JSON values are consistent. It does prevent direct paper-locking without a small summary/metadata cleanup.

## 6. Required Reply To Remote 107

```text
107 update received and audited at origin/107-clean commit 37df860.

Good:
- pipeline_fresh_d2d.py naming fix is correct.
- The 62-task fresh-D2D pipeline completed.
- Selective last1/last2 fresh-D2D evals are now present: 30 JSONs.
- Py-compile passed on the clean branch archive.

Main result:
- last1 analog KV ([23]) is the strongest route:
  eval D2D=0.02 -> 18.42 +/- 0.02 PPL
  eval D2D=0.04 -> 18.55 +/- 0.03 PPL
  eval D2D=0.05 -> 18.60 +/- 0.03 PPL
- last2 ([22,23]) is also robust but worse:
  eval D2D=0.02 -> 18.71 +/- 0.02 PPL
  eval D2D=0.04 -> 19.07 +/- 0.04 PPL
  eval D2D=0.05 -> 19.21 +/- 0.04 PPL
- all-layer remains a stress/control path, not the deployment route.

Route decision:
Proceed with selective terminal-layer KV-cache + HAT as Work-2 primary route. Last1 is the current best deployment candidate.

Still needed before canonical paper use:
Please add a small RESULTS_SUMMARY_FRESH_D2D.md at branch root or coordination/ with:
1. branch + full commit SHA,
2. py_compile output,
3. exact train/eval commands or the launcher command,
4. environment packet,
5. training checkpoint table,
6. aggregated fresh-D2D table for all-layer/last1/last2,
7. explicit statement that `d2d_seed` in eval JSON means eval_d2d_seed override,
8. note that train_d2d_seed=42 for these checkpoints.

For future JSONs, please include git_commit, script, mode, model, dataset_eval, train_seed, train_d2d_seed, eval_d2d_seed, analog_layers, command. Current numbers are strong but metadata-provisional.
```

## 7. Local Integration

Do not merge `107-clean` into `paper1-release-20260501`.

Recommended local handling:

- Keep `107-clean` as a standalone GitHub communication/deliverable branch.
- Consume it via reports and small JSON summaries only.
- Do not entangle with Paper-1 submission files.
- If later archiving locally, import into a namespaced folder such as `remote107_clean_deliverable/`, not repository root.

