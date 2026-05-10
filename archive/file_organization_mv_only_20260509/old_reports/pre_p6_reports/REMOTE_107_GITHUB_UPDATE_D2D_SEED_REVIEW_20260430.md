# Remote 107 GitHub Update Review — 107-clean D2D Seed / Fresh-D2D

Date: 2026-04-30
Reviewer: Codex
Remote branch: `origin/107-clean`
Latest commit: `aca7dd5 D2D seed ablation + fresh-D2D cross-instance results (auto)`
Local inspection worktree: `/tmp/hat_107_clean`

## 1. GitHub Status

107 has updated GitHub. `origin/107-clean` now contains six commits after the Codex coordination packet commit `9d92621`:

1. `d2bc008` — fix eval filename includes d2d_seed; add fresh-D2D cross-instance pipeline
2. `a8d318e` — expand fresh-D2D pipeline to Codex P1 spec (4 ckpts, 60 eval)
3. `3cf5d5a` — prevent duplicate dispatch of same task in fresh-D2D pipeline
4. `9b92df8` — remove HTTP_PROXY from pipeline env
5. `8eb5385` — add `--resume` flag to `pipeline_fresh_d2d.py`
6. `aca7dd5` — D2D seed ablation + fresh-D2D cross-instance results

Current local project branch was not merged or pulled into. Inspection was done in a detached worktree to avoid polluting local R11D/paper work.

## 2. Code-Level Changes Verified

### Implemented Correctly

- `p3_hat_eval.py` now writes eval filenames with explicit `d2d_seed`, preventing overwrite/collision between different chip instances.
- `pipeline_fresh_d2d.py` exists and includes explicit `--d2d-seed` override for eval.
- `pipeline_fresh_d2d.py` has `--resume`, which is necessary because the full matrix is long.
- `pipeline_d2d_seed.py` state tracking is present.

### Important Caveat

The fresh-D2D pipeline state file indicates the full P1 matrix is not complete yet.

`results/d2d_seed_ablation/.pipeline_fresh_d2d_state.json`:

- `completed`: 7 tasks only
- completed tasks include 5 eval rows for all-layer D2D=0.02 and two selective training tasks
- missing: selective last1/last2 fresh-D2D evals and much of the intended 4-checkpoint matrix

## 3. Available Fresh-D2D Results

These results are usable because eval output filenames and JSON metadata include `d2d_seed`.

### Fixed Train Checkpoint: All-Layer HAT Trained At D2D=0.02, Train D2D Seed=42

| Eval D2D | Eval Seeds | Mean PPL | Std | Min | Max |
|---:|---:|---:|---:|---:|---:|
| 0.02 | 5 | 26.05 | 0.53 | 25.17 | 26.50 |
| 0.04 | 5 | 44.34 | 2.65 | 40.08 | 46.74 |
| 0.05 | 5 | 66.84 | 5.91 | 57.65 | 73.06 |

### Fixed Train Checkpoint: All-Layer HAT Trained At D2D=0.04, Train D2D Seed=42

| Eval D2D | Eval Seeds | Mean PPL | Std | Min | Max |
|---:|---:|---:|---:|---:|---:|
| 0.02 | 5 | 27.97 | 0.40 | 27.34 | 28.45 |
| 0.04 | 5 | 38.35 | 1.68 | 35.58 | 40.11 |
| 0.05 | 5 | 47.98 | 3.13 | 42.78 | 51.13 |

## 4. Selective Training Present But Fresh Eval Missing

Selective checkpoints exist and show near-baseline post-HAT PPL on the training D2D instance:

| Checkpoint | Analog Layers | Train D2D Seed | Pre-HAT PPL | Post-HAT PPL |
|---|---:|---:|---:|---:|
| `hat_d2d002_500_freshd2d_last1_seed42_seed42` | `[23]` | 42 | 23.28 | 18.43 |
| `hat_d2d002_500_freshd2d_last2_seed42_seed42` | `[22,23]` | 42 | 24.93 | 18.69 |

But no matching `eval_hat_d2d002_500_freshd2d_last*_...` JSON files are present yet. Therefore the most important deployment claim, selective terminal-layer cross-device D2D robustness, is not closed.

## 5. Interpretation

The all-layer fresh-D2D results support a clear tradeoff:

- Training at D2D=0.02 is better when eval D2D is also low: 26.05 PPL at eval D2D=0.02.
- Training at D2D=0.04 is much better when eval D2D is high: 38.35 vs 44.34 at eval D2D=0.04, and 47.98 vs 66.84 at eval D2D=0.05.
- This supports the narrative that HAT does not merely memorize a single D2D instance; higher-noise training buys broader D2D robustness at a small low-noise cost.

However, the selective-layer story is still incomplete until last1/last2 fresh-D2D evals are run across eval D2D `{0.02, 0.04, 0.05}` and seeds `{42, 123, 456, 789, 1001}`.

## 6. Required Reply To 107

Please send 107 the following instruction:

```text
107-clean update received and audited at commit aca7dd5.

Good:
- p3_hat_eval.py now includes d2d_seed in output filenames.
- pipeline_fresh_d2d.py explicitly passes --d2d-seed and has --resume.
- all-layer fresh-D2D results are present and usable.

Current usable all-layer result:
- Train D2D=0.02, train d2d_seed=42:
  eval D2D=0.02 -> 26.05±0.53 PPL
  eval D2D=0.04 -> 44.34±2.65 PPL
  eval D2D=0.05 -> 66.84±5.91 PPL
- Train D2D=0.04, train d2d_seed=42:
  eval D2D=0.02 -> 27.97±0.40 PPL
  eval D2D=0.04 -> 38.35±1.68 PPL
  eval D2D=0.05 -> 47.98±3.13 PPL

Interpretation: high-D2D training gives better high-D2D robustness, with a small low-D2D cost.

Missing / please continue:
.pipeline_fresh_d2d_state.json shows only 7 completed tasks. Selective last1 and last2 training exists, but selective fresh-D2D eval JSONs are missing. Please run:

python pipeline_fresh_d2d.py --resume

until the intended 4 checkpoints × 3 eval D2D × 5 eval D2D seeds are complete. Then add a small RESULTS_SUMMARY_FRESH_D2D.md with tables grouped by checkpoint, eval D2D, mean/std/min/max PPL, and exact commit SHA.
```

## 7. Local Routing Decision

Do not merge `107-clean` into the local paper/R11D work branch yet. Treat it as a remote KV-cache deliverable branch and consume it through reports/JSON summaries until 107 finishes the missing selective eval matrix.
