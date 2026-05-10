# Remote 107 GitHub Pull Review — 2026-04-30

## Scope

Remote GitHub was fetched from `git@github.com:Leslie360/HAT.git` on local machine.

Inspected branch:

- `origin/remote-exploration`
- HEAD: `4fc0ebecf1c5ae1e11bcf5771cde72af84e19c77`
- Commit title: `update deliverable with Phase 3 seed 123/456 results`

I did **not** run `git pull` into the active local branch because the local worktree has substantial uncommitted paper/R11D changes and local commits. Inspection was done in an isolated worktree:

- `/tmp/hat_remote_exploration_107`

## Merge Safety Verdict

Do not merge `origin/remote-exploration` into local main/current branch as-is.

Reasons:

- Remote branch differs from `origin/main` by 819 files: 739 added, 70 deleted, 6 modified, plus renames.
- It deletes local coordination/R11D/KV files under `report_md/_gpt`, `paper2`, and `paper2_aihwkit_baseline` if merged naively.
- It adds large checkpoint files under `checkpoints/` (~153 MB total in inspected worktree).
- It is best treated as a remote deliverable snapshot, not a source-of-truth branch for local paper-1.

Safe use pattern:

- Read/copy selected `deliverable/` files only.
- Do not pull/merge into the active local working branch.
- If importing, use a new namespace such as `remote107_deliverable/` or cherry-pick only report/code files after review.

## What 107 Added

Main deliverable tree:

- `deliverable/README.md`
- `deliverable/code/analog_kv_cache.py`
- `deliverable/code/p3_hat_train.py`
- `deliverable/code/p3_hat_eval.py`
- `deliverable/pipeline/pipeline_runner.py`
- `deliverable/pipeline/pipeline_health.sh`
- `deliverable/results_v2/*.json` — 49 v2 result JSON files
- `deliverable/p0_p3_archive/*.json` — archived pre-v2 / P0-P3 data
- root `RESULTS_SUMMARY.md`

Latest commit claims:

- Phase 3 seed 123/456 training results added.
- `RESULTS_SUMMARY.md` seed ablation table updated.
- Old `results/` reorganized into `results_v2/` and `p0_p3_archive/`.

## Current v2 Numeric Snapshot From GitHub

Remote `RESULTS_SUMMARY.md` reports:

### Generalization Eval

| Checkpoint | Clean | D2D=0.01 | D2D=0.02 | D2D=0.03 | D2D=0.04 | D2D=0.05 |
|---|---:|---:|---:|---:|---:|---:|
| D2D=0.02 train | 20.85 | 22.65 | 26.39 | 32.24 | 42.27 | 61.39 |
| D2D=0.04 train | 22.37 | 24.70 | 27.96 | 32.30 | 38.89 | 49.72 |

C2C=0.01 train: clean 19.24; C2C=0.005/0.01/0.015/0.02 = 19.78 / 21.24 / 23.49 / 26.66.

Combined train: clean 20.79; D2D=0.04 eval 47.64; C2C=0.02 eval 26.97.

### Selective Layer

| Config | last1 | last2 | last4 | all24 |
|---|---:|---:|---:|---:|
| D2D=0.02 | 18.28 | 18.83 | 20.11 | 25.49 |
| C2C=0.01 | 18.14 | 18.51 | 19.45 | 21.21 |
| Combined | — | 18.67 | — | 26.81 |

Trend remains: selective terminal-layer HAT is substantially better than all-layer HAT for PPL.

### Seed Table In GitHub

| Config | seed42 | seed123 | seed456 |
|---|---:|---:|---:|
| D2D=0.02 | 25.49 | 25.62 | 25.62 |
| D2D=0.04 | 35.93 | 35.84 | 35.84 |
| C2C=0.01 | 21.21 | 21.37 | 21.09 |
| Combined | 26.81 | 26.00 | 26.28 |

This is reproducible as a training-seed sanity check, but it is **not yet sufficient** as a D2D device-instance robustness check. See issue R107-GH-1 below.

## Critical Review Findings

### R107-GH-1 — D2D seed ablation is not true D2D instance ablation

In `deliverable/code/p3_hat_train.py`, CLI `--seed` is set at lines 359 and 366-367, but D2D buffers are generated with a layer-fixed seed:

```python
with torch.random.fork_rng():
    torch.manual_seed(0xD2D + layer_idx)
```

This makes D2D offset pattern independent of `--seed`. Therefore:

- seed123 and seed456 can be identical or near-identical for D2D-only runs.
- The table proves deterministic pipeline reproducibility, not cross-device D2D robustness.
- Generalization sweeps scale the same fixed D2D pattern rather than evaluating multiple fresh D2D instances.

Required fix:

- Add explicit `--d2d-seed` / `--device-instance-seed`.
- Generate D2D buffers with a deterministic function of `(d2d_seed, layer_idx, tensor_kind)`.
- Store both `train_seed` and `d2d_seed` in every JSON.
- For robustness claims, run fixed train checkpoint against multiple fresh `d2d_seed` values.

Minimum rerun after fix:

| Purpose | Train config | Eval config |
|---|---|---|
| D2D instance stability | all-layer D2D=0.02, 500 steps, train_seed=42 | eval d2d_seed={42,123,456,789,1001} at D2D=0.02/0.04/0.05 |
| High-noise robustness | all-layer D2D=0.04, 500 steps, train_seed=42 | same eval d2d_seed set |
| Selective route stability | last1 and last2, D2D=0.02, 500 steps | same eval d2d_seed set |

### R107-GH-2 — selective checkpoint eval requires layer-mask persistence

`p3_hat_eval.py` defaults `--analog_layers=None`, which means all layers are patched at eval time. If a selective checkpoint is evaluated later without passing the same `--analog_layers`, the eval will not match training scope.

Required fix:

- Save `analog_layers` into checkpoint metadata or a sidecar `hat_config.json`.
- `p3_hat_eval.py` should auto-load this metadata unless explicitly overridden.
- Result JSON should include `train_analog_layers` and `eval_analog_layers` separately.

### R107-GH-3 — deliverable is not portable yet

Hardcoded paths exist in:

- `deliverable/code/p3_hat_train.py`
- `deliverable/code/p3_hat_eval.py`
- `deliverable/pipeline/pipeline_runner.py`
- `deliverable/pipeline/pipeline_health.sh`

Examples include `/home/lisq753/projects/HAT/HAT`, `/home/lisq753/miniconda3/envs/LLM/bin/python`, and fixed proxy settings.

Required fix:

- Convert hardcoded paths to CLI args or environment variables.
- Add a `REPRODUCE_107.md` with exact environment variables.
- Keep remote-specific launch scripts separate from portable core code.

### R107-GH-4 — v2 numbers should be provisional until latest noise bug rerun is confirmed

GitHub v2 summary says the corrected implementation shifts PPL by +2 to +4 compared with v1. User also reported that Remote 107 has found a noise-algorithm bug and is rerunning. Therefore:

- Treat current GitHub v2 numbers as the latest available snapshot, not paper-locked canonical numbers.
- Lock only trend-level conclusions until 107 confirms the branch includes the final noise fix and rerun.

## Current Architectural Read

The 107 route remains promising, but the narrative should be stated carefully:

- Strongest current signal: HAT can recover PPL substantially under analog KV noise.
- Strongest deployment path: selective terminal-layer KV + HAT, because last1/last2 are near clean PPL and much better than all24.
- High-D2D training appears to improve high-D2D eval robustness, but true fresh-device evidence still needs `d2d_seed` rerun.
- C2C conclusions are less affected by D2D seed policy because C2C is re-sampled every forward.

## Reply To Remote 107

Recommended message:

```text
GitHub branch received and inspected. Do not change remote pipeline direction yet, but please fix the D2D seed semantics before making any seed/fresh-instance claim.

Current issue: --seed controls training RNG, but D2D buffers are generated with torch.manual_seed(0xD2D + layer_idx), so D2D seed123/456 are not independent device instances. This explains why D2D seed123 and seed456 are identical/near-identical. Please add --d2d-seed / --device-instance-seed, record train_seed and d2d_seed separately in JSON, and rerun a small corrected matrix first:

1. Train/checkpoint sanity: all-layer D2D=0.02 and D2D=0.04, 500 steps, train_seed=42.
2. Fresh D2D eval: each checkpoint evaluated at d2d_seed={42,123,456,789,1001}, eval D2D={0.02,0.04,0.05}.
3. Selective route: last1 and last2 D2D=0.02, 500 steps, same fresh D2D eval.
4. For selective checkpoints, persist/load analog_layers in eval; do not rely on manual CLI memory.
5. Return exact commit SHA, diffstat, formulas/code snippets for D2D/C2C/quantization, and updated JSON.

Current v2 trend is useful, but numbers remain provisional until this seed/device-instance fix and the latest noise-bug rerun are confirmed.
```
