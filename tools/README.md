# tools/

Reusable tools only. One-off or stale scripts belong in `experiments/scripts/` or `archive/`.

## Subdirectories

| Subdir | Purpose | Required provenance |
|:--|:--|:--|
| `plotting/` | Scripts that generate paper/thesis figures | Input data path and output figure path must be documented in the script or linked manifest. |
| `validation/` | Scripts that validate locked claims, source data, or release gates | State which claim/artifact is validated and where logs should be written. |
| `latex/` | LaTeX build or asset helpers | State target manuscript and output directory. |
| `data_extract/` | Data extraction/conversion helpers | State raw input, derived output, and manifest path. |
| `maintenance/` | Workspace hygiene helpers | Must be dry-run or manifest-first unless explicitly approved. |

## Current active tools

| Tool | Role | Inputs | Outputs / consumers |
|:--|:--|:--|:--|
| `plotting/plot_paper1_spine.py` | Paper1 figure/source-data plotting | `manuscripts/paper1/src/source_data/fig1_paper1_spine.csv` | Paper1 source figures/data |
| `plotting/plot_paper1_decision_map.py` | Paper1 decision-map plotting | `manuscripts/paper1/src/source_data/fig2_paper1_decision_map.csv` | Paper1 source figures/data |
| `validation/check_local_pcm_precision_ladder.py` | Validates local PCM precision ladder evidence | Paper1 canonical JSON/source data | Paper1 evidence gate |

## Rules

- Do not run GPU-heavy or training-related tools without checking GPU state and user constraints.
- Always tee command output to `logs/` with a timestamp.
- Do not move active data/figures without updating the relevant manifest.
