# compute_vit Project Layout v2

Date: 2026-05-09
Scope: `/home/qiaosir/projects/compute_vit`
Purpose: Make every file explainable by location, lifecycle, and project role.

## 1. Design principles

1. Root directory is an index, not a storage dump.
2. Paper-1 submission, Work-2 research, thesis writing, local data, and coordination are separated.
3. Final submission artifacts stay easy to find and SHA-verifiable.
4. Large datasets/checkpoints/raw hardware data stay local-first and should not be committed blindly.
5. Historical material is preserved under archive with restore commands, not deleted.
6. Every report or artifact should be traceable to a phase, owner, and purpose.

## 2. Target root layout

```text
compute_vit/
├── README.md
├── WORKSPACE_LAYOUT.md
├── PROJECT_INDEX.md
├── .gitignore
│
├── paper1/
├── work2/
├── thesis/
├── data_local/
├── experiments/
├── coordination/
├── tools/
├── tests/
├── logs/
└── archive/
```

## 3. Directory responsibilities

### `paper1/`

Paper-1 / Nature Electronics submission lane only.

```text
paper1/
├── manuscript/
├── figures/
├── source_data/
├── release/
├── provenance/
└── reports/
```

Rules:

- Manuscript source/PDFs go under `paper1/manuscript/`.
- Final uploadable bundle goes under `paper1/release/`.
- Provenance archive goes under `paper1/provenance/`.
- P6/P7/P8 reports and audits go under `paper1/reports/`.
- Work-2/107 claims do not enter Paper-1 reports except as future-work notes.

### `work2/`

Work-2 research, including 107 analog KV-cache and follow-on AIHWKit PCM experiments.

```text
work2/
├── kv_cache/
├── aihwkit_pcm/
├── scripts/
├── results/
├── figures/
└── reports/
```

Rules:

- 107 results stay Work-2 only.
- Work-2 scripts/logs/checkpoints are not mixed with Paper-1 release artifacts.
- Large checkpoints may be linked from `data_local/checkpoints/` instead of committed.

### `thesis/`

PhD thesis writing lane.

```text
thesis/
├── en/
├── cn/
├── xjtu_template/
└── assets/
```

Rules:

- English thesis goes to `thesis/en/`.
- Chinese thesis goes to `thesis/cn/`.
- XJTU template goes to `thesis/xjtu_template/`.
- Thesis can reuse Paper-1 values only from canonical Paper-1 source data.

### `data_local/`

Large local-only data and checkpoints.

```text
data_local/
├── datasets/
├── checkpoints/
├── raw_device_data/
└── derived_profiles/
```

Rules:

- Default: do not commit large raw data/checkpoints.
- Keep index/manifests in Git if needed; keep payload local.
- Raw device data should be cited through extracted/derived profiles, not directly as Paper-1 model numbers.

### `experiments/`

Non-final experiment execution area.

```text
experiments/
├── configs/
├── scripts/
├── logs/
├── scratch/
└── manifests/
```

Rules:

- New exploratory jobs write here first.
- Outputs become Paper-1 canonical only after audit and migration into `paper1/source_data/`.

### `coordination/`

Agent and phase coordination.

```text
coordination/
├── active/
├── dispatches/
├── audits/
├── agent_reports/
└── remote_tasks/
```

Rules:

- `active/` contains `broadcast.md`, `AGENT_SYNC_gpt.md`, `CLAUDE_TASK_gpt.md` or compatibility links.
- Dispatches are grouped by phase.
- Audits are grouped by DS/Mimo/Codex/Claude.
- Agent reports are grouped by Kimi/Gemini/Codex/Claude.

### `tools/`

Reusable scripts.

```text
tools/
├── validation/
├── plotting/
├── latex/
├── data_extract/
└── maintenance/
```

Rules:

- One-off scripts belong in `archive/old_scripts/` or `experiments/scripts/`.
- Stable validation scripts belong in `tools/validation/`.

### `archive/`

Historical and restorable material.

```text
archive/
├── cleanup/
├── old_reports/
├── old_scripts/
├── old_build_outputs/
├── superseded_releases/
├── raw_imports/
└── restore/
```

Rules:

- Archive can be large and may stay local-only.
- Every bulk move should have a restore script.
- Do not use archive as an active work area.

## 4. Current compatibility paths

Until full migration is complete:

| Current path | Meaning | Target |
|---|---|---|
| `paper/latex_gpt/` | active Paper-1 manuscript | `paper1/manuscript/` |
| `release_artifacts/paper1_submission_bundle_20260509_final*` | final Paper-1 release | `paper1/release/` |
| `release_artifacts/paper1_provenance_archive_20260509*` | Paper-1 provenance | `paper1/provenance/` |
| `report_md/_gpt/` | coordination/report hub | `coordination/` + `paper1/reports/` |
| `paper2/` | Work-2 KV-cache | `work2/kv_cache/` |
| `paper2_aihwkit_baseline/` | Work-2 AIHWKit/PCM | `work2/aihwkit_pcm/` |
| `thesis/en/ (compat: paper/thesis/)` | English thesis | `thesis/en/` |
| `thesis/cn/ (compat: paper/thesis_cn/)` | Chinese thesis | `thesis/cn/` |
| `data/` | datasets | `data_local/datasets/` |
| `checkpoints/` | checkpoints | `data_local/checkpoints/` |
| `数据_博士/` | raw device data | `data_local/raw_device_data/` |

## 5. Migration phases

### R1: Non-invasive foundation

- Create target directories.
- Generate inventory.
- Write mapping and restore plan.
- Do not move active code paths yet.

### R2: Low-risk archive migration

- Move old reports, old build outputs, old release candidates, old scripts.
- Keep active Paper-1 and Work-2 paths intact.

### R3: Coordination split

- Move reports into `coordination/` and `paper1/reports/`.
- Preserve compatibility index or symlinks if needed.

### R4: Core path migration

- Move `paper/latex_gpt/` to `paper1/manuscript/`.
- Move `paper2/` and `paper2_aihwkit_baseline/` into `work2/`.
- Move thesis directories into `thesis/`.
- Move datasets/checkpoints/raw device data into `data_local/` or keep as local symlinks.

### R5: Verification

- Rebuild PDFs.
- Re-run bundle SHA.
- Re-run PCM guard.
- Grep stale values.
- Update documentation.

## 6. Inventory files

- `report_md/_gpt/FILE_PURPOSE_INVENTORY_20260509.tsv`
- `report_md/_gpt/FILE_PURPOSE_INVENTORY_SUMMARY_20260509.md`

These are the current machine-readable maps of every file's first-pass purpose classification.


## Projects-root note

The real workspace root is `/home/qiaosir/projects`. This document applies to the `compute_vit/` subproject only. See `/home/qiaosir/projects/PROJECTS_ROOT_LAYOUT_20260509.md` for workspace-level organization.
