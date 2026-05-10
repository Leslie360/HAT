# compute_vit Ideal Layout Plan

Date: 2026-05-10
Scope: `/home/qiaosir/projects/compute_vit`

## Goal

Make `compute_vit/` a clean long-term workbench where the three deliverables are obvious, active files are small and current, and every data/figure/table/checkpoint can be traced to source.

The three product lanes are:

1. **Paper1** — nearly complete: main manuscript, supplement/appendix, cover letter, final submission bundle, source data, provenance.
2. **Paper2 / 107 KV-cache** — Work-2 selective KV-cache and AIHWKit/PCM baseline work.
3. **Degree thesis** — thesis text, template, reused Paper1 assets, and thesis-only figures/tables.

## Ideal top-level directory tree

```text
compute_vit/
├── README.md
├── PROJECT_INDEX.md
├── WORKSPACE_LAYOUT.md
├── LICENSE
├── .gitignore
├── environment.yml
├── requirements.txt
├── requirements-optional.txt
│
├── src/                         # importable Python package, not experiment clutter
├── cli/                         # thin user-facing wrappers for train/eval commands
├── configs/                     # reusable configs only
│
├── paper1/                      # Paper1 deliverable lane
├── paper2_107/                  # Paper2 / 107 KV-cache deliverable lane
├── thesis/                      # degree thesis deliverable lane
│
├── shared/                      # shared non-paper-specific assets
├── data_local/                  # local datasets and large raw data, not blindly committed
├── checkpoints/                 # protected model weights, indexed not moved casually
├── tools/                       # reusable plotting/validation/latex/data tools
├── experiments/                 # exploratory runs and scratch experiment manifests
├── coordination/                # current agent coordination only
├── logs/                        # timestamped logs
├── tests/                       # tests
├── notebooks/                   # notebooks
└── archive/                     # isolated old/backup/deprecated material
```

## Ideal product lanes

### `paper1/`

```text
paper1/
├── manuscript/
│   ├── main.tex
│   ├── supplementary.tex
│   ├── cover_letter.tex
│   ├── sections/
│   ├── supplementary/
│   ├── figures/                 # active figures used by current TeX closure
│   ├── tables/                  # active standalone table assets if any
│   └── source_data/             # active CSV/JSON source data used by figures/tables
├── release/
│   ├── paper1_submission_bundle_YYYYMMDD_final/
│   ├── paper1_submission_bundle_YYYYMMDD_final.tar.gz
│   └── SHA256SUMS.txt
├── provenance/
│   ├── paper1_active_provenance_index_YYYYMMDD.tsv
│   ├── source_data_manifests/
│   ├── figure_manifests/
│   ├── deprecated_figures/
│   ├── orphan_figures/
│   └── old_protocol_json/
├── reports/
│   ├── current/                 # only current acceptance/freeze reports
│   ├── audits/
│   └── archive/                 # old P6/P7/P8 internal reports after freeze
└── README.md
```

Rules:

- Keep Paper1 main/supplement/letter together.
- Active source data must sit near the manuscript or be indexed from there.
- Deprecated figures and old JSON are not deleted; they go to `paper1/provenance/` or `archive/` with manifests.
- Final release is frozen and SHA-verifiable.
- `paper/latex_gpt` can remain as a compatibility symlink during transition, but the ideal active home is `paper1/manuscript/`.

### `paper2_107/`

```text
paper2_107/
├── manuscript/                  # future Paper2 source when ready
├── kv_cache/
│   ├── src/
│   ├── configs/
│   ├── results/
│   ├── figures/
│   ├── source_data/
│   └── reports/
├── aihwkit_pcm/
│   ├── src/
│   ├── configs/
│   ├── results/
│   ├── figures/
│   └── reports/
├── remote_107/
│   ├── tasklists/
│   ├── returned_results/
│   └── ingestion_notes/
└── README.md
```

Rules:

- 107 selective KV-cache is Paper2/Work-2, not Paper1 evidence.
- Remote 107 tasks and returned results must be findable from `paper2_107/remote_107/`.
- AIHWKit/PCM baseline results stay separate from Paper1 source data unless explicitly copied into a future Paper2 source-data package.
- Invalid/contaminated runs stay marked but should be isolated under `paper2_107/.../deprecated/` or archive.

### `thesis/`

```text
thesis/
├── manuscript/
│   ├── cn/
│   ├── en/
│   └── xjtu_template/
├── assets/
│   ├── figures_active/
│   ├── figures_reused_from_paper1/
│   ├── figures_thesis_only/
│   └── tables/
├── source_data/
│   ├── from_paper1/
│   ├── thesis_only/
│   └── manifests/
├── notes/
│   ├── current/
│   └── archive/
└── README.md
```

Rules:

- Thesis may reuse Paper1 figures/data, but the reuse must be indexed.
- Thesis-only material should not pollute Paper1 release paths.
- Old Kimi/Misc thesis template surveys belong in archive, not active thesis source.

## Ideal code layout

### `src/`

```text
src/compute_vit/
├── analog_layers.py
├── analog_layers_ensemble.py
├── inference_analysis_utils.py
├── amp_utils.py
├── device_profile_utils.py
├── tinyvit_hybrid_utils.py
├── report_asset_paths.py
├── model_profiling.py
├── physical_noise_pipeline.py
├── hybrid_calibration.py
└── hybrid_runtime_compiler.py
```

Rules:

- This should become the importable package.
- Current root imports are fragile; migrate one library family at a time.
- Do not move these without updating imports and running tests.

### `cli/`

```text
cli/
├── train_tinyvit.py
├── train_tinyvit_ensemble.py
├── train_convnext.py
├── train_resnet18.py
├── eval_fresh_instances.py
├── eval_fresh_instances_postfix.py
├── eval_imagenet_analog.py
├── eval_literature_profile.py
├── eval_measured_profile.py
└── eval_resnet18_checkpoints.py
```

Rules:

- Root may keep thin compatibility wrappers during migration.
- Long-term root should not store full train/eval implementation files.
- Every CLI entry should have a `--help` check and documented expected inputs/outputs.

## Data, JSON, and checkpoint layout

### `data_local/`

```text
data_local/
├── datasets/
├── raw_device_data/
├── derived_profiles/
├── local_checkpoints/
└── README.md
```

Rules:

- Large datasets/raw data stay local-first.
- Do not commit large payloads blindly.
- Every derived JSON profile should point to source raw data or literature.

### `device_profiles/`

Keep this active if small and canonical:

```text
device_profiles/
├── literature_profiles_gpt.json
├── synthetic_profiles_gpt.json
├── example_measured_device_profile_gpt.json
└── README.md
```

Rules:

- Add a README/index explaining source, parameters, and intended use.
- Move `auto_fitted_profile.json` here only after grep/reference check.

### `checkpoints/`

```text
checkpoints/
├── INDEX_YYYYMMDD.md
├── paper1_canonical/
├── paper1_experimental/
├── paper2_107/
├── deprecated_or_invalid/
└── local_scratch/
```

Rules:

- Current checkpoint payloads are protected.
- Do not move/delete weights without explicit approval.
- First produce a size/provenance report, then migrate by group.
- Invalid/contaminated checkpoints should be visibly separated and indexed.

## Tools layout

```text
tools/
├── plotting/
├── validation/
├── latex/
├── data_extract/
├── maintenance/
└── README.md
```

Rules:

- Plot scripts must declare input data and output figures.
- Validation scripts must declare which claim/artifact they validate.
- One-off scripts go to `experiments/scripts/` or `archive/old_scripts/` after use.

## Coordination and Markdown policy

```text
coordination/
├── active/
│   ├── AGENT_SYNC_gpt.md
│   ├── CLAUDE_TASK_gpt.md
│   └── broadcast.md -> ../../../BROADCAST.md
├── dispatches/
├── audits/
├── agent_reports/
├── remote_tasks/
└── README.md
```

Rules:

- Only current coordination belongs here.
- Old agent Markdown goes to `archive/` with manifest/restore script.
- Paper-specific reports should live in the matching product lane, not a generic dump.

## Archive policy

```text
archive/
├── README.md
├── reorg_YYYYMMDD/
│   ├── restore/
│   └── manifests/
├── old_agent_markdown/
├── old_scripts/
├── old_reports/
├── deprecated_figures/
├── deprecated_source_data/
└── bulk_mv_snapshots/
```

Rules:

- Archive is not active work space.
- Every bulk move gets a manifest and restore script.
- Broken symlinks inside old archives can remain only if documented as archive-only.
- Do not delete archive payloads without explicit approval.

## Migration phases

### Phase 0 — Freeze current safety state

- Keep current Paper1 release untouched.
- Keep checkpoint/data payloads untouched.
- Maintain broadcast and restore scripts.

### Phase 1 — Documentation and indexes

- Finish top-level indexes: `WORKSPACE_LAYOUT.md`, `archive/README.md`, product-lane provenance TSVs.
- Add `tools/README.md`, `coordination/README.md`, `device_profiles/README.md`.
- Add Paper2/107 and thesis lane READMEs.

### Phase 2 — Active/old Markdown separation

- Keep only recent/current Markdown in active paths.
- Move old agent reports and old reviewer-response packages into archive with manifests.
- Keep Paper1/Paper2/thesis reports grouped by lane.

### Phase 3 — Data and source-data organization

- Index all active CSV/JSON/TSV by product lane.
- Separate active, backup, deprecated, invalid source data.
- Keep manifests for figure/table inputs.

### Phase 4 — Figure and LaTeX asset cleanup

- Paper1 active figures stay with current TeX closure.
- Unused/backup/deprecated figures stay in asset archive with manifest.
- Thesis reused figures are indexed, not copied randomly.

### Phase 5 — Root code migration

- Create `src/compute_vit/` package.
- Move import-sensitive libraries one family at a time.
- Add root compatibility wrappers or `cli/` wrappers.
- Run tests and `--help` checks after every group.

### Phase 6 — Checkpoint/data payload migration

- Only after explicit approval.
- Produce size/provenance report first.
- Move weights by product lane, preserving indexes and avoiding GPU/training disruption.

## Non-goals

- Do not delete large data/checkpoints during cleanup.
- Do not move root Python implementation files without package/wrapper migration.
- Do not mix Paper2/107 evidence into Paper1 release paths.
- Do not put old agent Markdown beside current work.

## Immediate next actions

1. Add `tools/README.md`, `coordination/README.md`, `device_profiles/README.md`, and lane READMEs. **Status: started/completed for current active directories on 2026-05-10.**
2. Keep `src/`, `cli`, and `configs/` as the active package/wrapper/config layout; root implementation Python has been migrated.
3. Add Paper2/107 and thesis lane READMEs explaining active paths and reused assets.
4. Continue runtime validation in a torch-enabled environment; do not run training as a cleanup check.
