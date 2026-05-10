# Remote 105/107 Data Acquisition Index

Date: 2026-05-07
Owner: Codex local data acquisition
Scope: data capture only. No thesis-writing judgment and no paper narrative edits.

## Stable Snapshot

Raw worktrees were located under `/tmp`, so they were copied into a stable workspace data snapshot:

- `hat_105_results`: `/home/qiaosir/projects/docs/data/remote_snapshots_20260507/hat_105_results`
- `hat_107_clean`: `/home/qiaosir/projects/docs/data/remote_snapshots_20260507/hat_107_clean`

Excluded: `.git`, `__pycache__`, and heavyweight checkpoint patterns (`*.pt`, `*.pth`).
Included: Markdown handoffs, JSON/CSV/TXT/LOG data, scripts, 107 deliverable code, and pipeline metadata.

## Git / Provenance Anchors

| Source | Snapshot path | Branch/worktree anchor | Experiment-code commit inside JSON |
|---|---|---|---|
| Remote 105 | `hat_105_results/` | detached worktree HEAD `4776925e3ddeade5f579e5fc4ef471f371e8df0f` | `fbfda71018eae5078968aa6f7faba0ae5b2d5ead` |
| Remote 107 | `hat_107_clean/` | detached worktree HEAD `37df860ba9b9cc06997163f2fdd2714c09c25243` | JSON metadata incomplete for some files; branch-level anchor is required |

## Generated Machine-Readable Tables

- `/home/qiaosir/projects/docs/data/remote_snapshots_20260507/remote105_tinyimagenet_fresh_eval.csv`
- `/home/qiaosir/projects/docs/data/remote_snapshots_20260507/remote105_noise_off.csv`
- `/home/qiaosir/projects/docs/data/remote_snapshots_20260507/remote107_kv_training_v2.csv`
- `/home/qiaosir/projects/docs/data/remote_snapshots_20260507/remote107_kv_eval_v2.csv`
- `/home/qiaosir/projects/docs/data/remote_snapshots_20260507/remote107_kv_fresh_d2d_raw.csv`
- `/home/qiaosir/projects/docs/data/remote_snapshots_20260507/remote107_kv_fresh_d2d_aggregate.csv`

## Remote 105: TinyImageNet Cross-Architecture Data

Protocol from JSON: 10 fresh instances x 5 MC runs per checkpoint. Dataset: TinyImageNet-200.

| Arch | HAT | Seed | Source best test (%) | Fresh mean (%) | Fresh std | Fresh-source (pp) | Raw |
|---|---|---:|---:|---:|---:|---:|---|
| deit_small_patch16_224 | digital | 123 | 48.22 | 48.22 | 0.00 | +0.00 | `hat_105_results/results/json/deit_small_patch16_224_digital_seed123_best_fresh_eval.json` |
| deit_small_patch16_224 | digital | 456 | 53.61 | 53.61 | 0.00 | +0.00 | `hat_105_results/results/json/deit_small_patch16_224_digital_seed456_best_fresh_eval.json` |
| deit_small_patch16_224 | ensemble | 123 | 45.26 | 40.44 | 0.43 | -4.82 | `hat_105_results/results/json/deit_small_patch16_224_ensemble_seed123_best_fresh_eval.json` |
| deit_small_patch16_224 | ensemble | 456 | 44.52 | 41.11 | 0.35 | -3.41 | `hat_105_results/results/json/deit_small_patch16_224_ensemble_seed456_best_fresh_eval.json` |
| deit_small_patch16_224 | proportional | 123 | 50.24 | 50.20 | 0.10 | -0.04 | `hat_105_results/results/json/deit_small_patch16_224_proportional_seed123_best_fresh_eval.json` |
| deit_small_patch16_224 | proportional | 456 | 54.44 | 54.19 | 0.09 | -0.25 | `hat_105_results/results/json/deit_small_patch16_224_proportional_seed456_best_fresh_eval.json` |
| deit_small_patch16_224 | standard | 123 | 40.61 | 6.38 | 0.85 | -34.23 | `hat_105_results/results/json/deit_small_patch16_224_standard_seed123_best_fresh_eval.json` |
| deit_small_patch16_224 | standard | 456 | 41.19 | 6.84 | 0.83 | -34.35 | `hat_105_results/results/json/deit_small_patch16_224_standard_seed456_best_fresh_eval.json` |
| vit_small_patch16_224 | digital | 123 | 48.83 | 48.83 | 0.00 | +0.00 | `hat_105_results/results/json/vit_small_patch16_224_digital_seed123_best_fresh_eval.json` |
| vit_small_patch16_224 | digital | 456 | 54.58 | 54.58 | 0.00 | +0.00 | `hat_105_results/results/json/vit_small_patch16_224_digital_seed456_best_fresh_eval.json` |
| vit_small_patch16_224 | ensemble | 123 | 43.64 | 40.24 | 0.36 | -3.40 | `hat_105_results/results/json/vit_small_patch16_224_ensemble_seed123_best_fresh_eval.json` |
| vit_small_patch16_224 | ensemble | 456 | 44.79 | 40.08 | 0.36 | -4.71 | `hat_105_results/results/json/vit_small_patch16_224_ensemble_seed456_best_fresh_eval.json` |
| vit_small_patch16_224 | proportional | 123 | 49.03 | 49.00 | 0.09 | -0.03 | `hat_105_results/results/json/vit_small_patch16_224_proportional_seed123_best_fresh_eval.json` |
| vit_small_patch16_224 | proportional | 456 | 54.06 | 53.90 | 0.13 | -0.16 | `hat_105_results/results/json/vit_small_patch16_224_proportional_seed456_best_fresh_eval.json` |
| vit_small_patch16_224 | standard | 123 | 39.22 | 5.22 | 0.51 | -34.00 | `hat_105_results/results/json/vit_small_patch16_224_standard_seed123_best_fresh_eval.json` |
| vit_small_patch16_224 | standard | 456 | 38.43 | 8.62 | 0.94 | -29.81 | `hat_105_results/results/json/vit_small_patch16_224_standard_seed456_best_fresh_eval.json` |

Notes:

- Seed 789 is not present in the acquired 105 JSON snapshot: `True`.
- Main current 105 value: DeiT proportional beats DeiT digital on both seeds; ViT proportional is not consistently above ViT digital.
- Standard HAT is the negative control and collapses under fresh eval.
- Raw source: `hat_105_results/results/json/*_best_fresh_eval.json`.

## Remote 105: Noise-Off Ablation

Raw file(s):

- `hat_105_results/results/json/deit_small_patch16_224_proportional_seed456_noise_off.json`

Important reported comparison from 105 handoff: `deit_proportional_seed456 noise_off=54.52`, `fresh=54.19`, `digital=53.61`.

## Remote 107: KV Cache v2 Current Results

Canonical summary file: `hat_107_clean/RESULTS_SUMMARY.md`.
Deliverable README: `hat_107_clean/deliverable/README.md`.
Current v2 baseline: digital Pythia-410m PPL = `15.68`.

Primary v2 training table lives in `remote107_kv_training_v2.csv`.
Primary v2 generalization eval table lives in `remote107_kv_eval_v2.csv`.

## Remote 107: Fresh-D2D Selective Terminal-Layer Aggregate

| Checkpoint | Scope | Eval D2D | n | Mean PPL | Std | Min | Max |
|---|---|---:|---:|---:|---:|---:|---:|
| `hat_d2d002_500_freshd2d_last1_seed42` | last1 | 0.02 | 5 | 18.42 | 0.02 | 18.40 | 18.45 |
| `hat_d2d002_500_freshd2d_last1_seed42` | last1 | 0.04 | 5 | 18.55 | 0.02 | 18.52 | 18.58 |
| `hat_d2d002_500_freshd2d_last1_seed42` | last1 | 0.05 | 5 | 18.60 | 0.03 | 18.56 | 18.63 |
| `hat_d2d002_500_freshd2d_last2_seed42` | last2 | 0.02 | 5 | 18.71 | 0.02 | 18.69 | 18.74 |
| `hat_d2d002_500_freshd2d_last2_seed42` | last2 | 0.04 | 5 | 19.07 | 0.04 | 19.03 | 19.13 |
| `hat_d2d002_500_freshd2d_last2_seed42` | last2 | 0.05 | 5 | 19.21 | 0.03 | 19.17 | 19.26 |

Interpretation for data use only:

- Last1 `[23]` is the strongest current KV route in the acquired data.
- Last2 `[22,23]` is close but consistently worse than last1.
- All-layer results are preserved as stress/control data, not the deployment-preferred data slice.
- These numbers remain metadata-provisional for formal paper use unless 107 returns full command/env/git metadata per JSON.

## Where To Pull Data For Thesis Later

| Need | Use this source first | Fallback |
|---|---|---|
| 105 TinyImageNet tables | `remote105_tinyimagenet_fresh_eval.csv` | `hat_105_results/docs/handoff/20260430_1140_data_report.md` |
| 105 provenance | `hat_105_results/config/environment.md` and JSON fields | `hat_105_results/README.md` |
| 107 headline tables | `hat_107_clean/RESULTS_SUMMARY.md` | generated CSVs in this folder |
| 107 training curves/losses | `hat_107_clean/deliverable/results_v2/hat_*.json` | `remote107_kv_training_v2.csv` for compact values |
| 107 fresh D2D | `remote107_kv_fresh_d2d_aggregate.csv` | raw JSONs under `hat_107_clean/results/d2d_seed_ablation/` |
| 107 code/math reproduction | `hat_107_clean/deliverable/code/` | root scripts in `hat_107_clean/` |

## Data-Use Warnings

- Do not cite `/tmp/...` paths; cite the stable snapshot path above.
- 105 seed 789 is missing because the server crashed before final seed completion.
- 107 v2 fixed a prior noise-algorithm bug; prefer `deliverable/results_v2` over `p0_p3_archive` for current values.
- 107 JSON metadata is incomplete in places; use branch commit + README + generated tables as provenance until a fuller remote summary arrives.
