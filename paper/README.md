# paper/ compatibility shell

This directory is no longer the canonical Paper1 manuscript home.

## Current role

| Path | Role |
|:--|:--|
| `latex_gpt` | Symlink to `../manuscripts/paper1/src`, which now resolves to `../paper1/manuscript`, for old build/script compatibility. |
| `thesis` | Symlink to `../thesis/en`. |
| `thesis_cn` | Symlink to `../thesis/cn`. |
| `figures/` | Compatibility symlink pool pointing to `../paper1/provenance/asset_archive/legacy_parallel_paper_figures/`. |
| `*.py` helpers | Compatibility symlinks to moved plotting helpers under `../tools/plotting/`. |
| reference lock `*.md` | Compatibility symlinks to `../paper1/provenance/reference_locks/`. |

## Canonical locations

- Editable Paper1 source: `../paper1/manuscript/`
- Compatibility Paper1 source: `../manuscripts/paper1/src/`
- Frozen Paper1 release: `../paper1/release/`
- Paper1 provenance/reports: `../paper1/provenance/`, `../paper1/reports/`
- Paper1 reference locks: `../paper1/provenance/reference_locks/`
- Directory role map: `../PAPER_DIRECTORY_MAP_20260510.md`
- Legacy `paper/paper2/` drafts archived to `../archive/reorg_20260509/paper2_legacy_drafts_20260510/paper/paper2/`.

## Rules

- Do not add new active assets here.
- Prefer canonical paths in new docs/scripts.
- Keep compatibility symlinks until all old references have been retired.
