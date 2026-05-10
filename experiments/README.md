# experiments/

Non-final experiment workspace.

## Subdirectories

| Subdir | Purpose |
|:--|:--|
| `configs/` | Exploratory or staging configs. |
| `scripts/` | Experiment scripts that are not stable reusable tools. |
| `logs/` | Experiment-specific logs when not written to root `logs/`. |
| `scratch/` | Temporary scratch outputs. |
| `manifests/` | Indexes describing experiment inputs/outputs. |

## Rules

- New exploratory jobs should start here before promotion to Paper1/Paper2/thesis lanes.
- Promote results only after writing a manifest and linking source data/scripts.
- Do not store final release artifacts here.
- Archive stale experiments with a manifest rather than leaving loose files active.
