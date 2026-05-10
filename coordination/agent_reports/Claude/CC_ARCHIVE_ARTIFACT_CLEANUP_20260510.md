# Archive and Non-Active Artifact Cleanup Report — 2026-05-10

## Scope

User requested broader cleanup of old Markdown, PDFs, and images. This pass removed only archived/deprecated/generated artifacts and preserved active deliverables.

Preserved:

- `paper1/manuscript/`
- `paper1/release/paper1_submission_bundle_20260509_final/`
- `thesis/cn/`
- `thesis/en/`
- `paper2/results/` audit outputs
- `data/`, checkpoints, datasets
- `remote_reviews/`

## Deleted groups

### 1. Archive Markdown/PDF/image junk

Deleted all `*.md`, `*.pdf`, `*.png`, `*.jpg`, `*.jpeg`, `*.svg` under `archive/`, except `archive/README.md`.

- Initial candidate count: 2454 files.
- Initial candidate bytes: 448,445,282 bytes.
- Follow-up safe-path cleanup removed the 5 path-with-space/unicode leftovers.
- Result: 0 matching archive junk files remain outside `archive/README.md`.

Logs:

- `logs/archive_junk_cleanup_20260510_154758_20260510.log`
- `logs/archive_junk_cleanup_20260510_154758_20260510.paths`

### 2. Non-active report/provenance/template generated artifacts

Deleted 197 non-active PDF/image files from:

- `report_md/images/`
- root-level PDF/image files directly under `report_md/`
- `paper1/provenance/asset_archive/unused_figures_candidates/`
- `paper1/provenance/asset_archive/legacy_parallel_paper_figures/`
- `paper1/provenance/paper1_provenance_archive_20260509/orphan_figures/`
- `paper1/provenance/paper1_provenance_archive_20260509/deprecated_20260424/`
- generated XJTU template PDFs under `thesis/xjtu_template/Build/` and `thesis/xjtu_template/main.pdf`

Deleted bytes: 170,668,561 bytes.

Logs:

- `logs/nonactive_artifact_cleanup_20260510_154921_20260510.log`
- `logs/nonactive_artifact_cleanup_20260510_154921_20260510.paths`

## Remaining large files are intentionally retained

The largest remaining PDFs/images are active or protected:

- Paper1 active/release PDFs and figures.
- CN/EN thesis PDFs.
- Paper2 107 audit figures.
- dataset images under `data/flowers-102/`.

## Notes

- No training was run.
- No push was performed.
- This cleanup intentionally produces many git deletions because the old archive/provenance artifacts were tracked.
- If a specific archived asset is needed later, recover from git history or the path logs above.
