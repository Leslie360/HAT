# compute_vit archive index

Date: 2026-05-10
Scope: `/home/qiaosir/projects/compute_vit/archive/`

This directory is an isolated historical area. Active work should not depend on files here unless an index explicitly says so.

## Rules

- Do not delete archive payloads without explicit user approval.
- Do not use archive as an active work area.
- Keep restore scripts under `reorg_20260509/restore/` when a move is reversible.
- Broken symlinks inside archived submission bundles are historical artifacts unless an active path references them.
- New active data, JSON, plot scripts, LaTeX assets, and checkpoints should be indexed in their active locations before any archive move.

## Top-level directories

| Directory | Status | Contents | Keep/delete guidance |
|:--|:--|:--|:--|
| `cleanup_candidates_20260509/` | quarantine | Candidate stale bundles, old drafts, test renderings, unreviewed material | Keep until reviewed against current paper/thesis assets |
| `file_organization_mv_only_20260509/` | local historical bulk archive | Large mv-only cleanup archive, old build outputs, legacy logs, old reports, old release/source artifacts | Keep; this is the largest rollback source |
| `final_tiny_residuals_20260510/` | restorable residual archive | Tiny leftover logs/report files from final cleanup | Keep with manifest |
| `reorg_20260509/` | active archive control area | Restore scripts, legacy root docs, report-md residuals | Keep; primary restore/control area |
| `residual_logs_gpt_20260510/` | restorable residual archive | Old `_gpt` logs | Keep with manifest |
| `residual_report_md_gpt_20260510/` | restorable residual archive | Old report_md `_gpt` payloads | Keep with manifest; old agent Markdown belongs here or similar archive areas |
| `stale_markdown_202604_review_20260510/` | restorable stale Markdown archive | Old 2026-04 reviewer-response package, old Kimi thesis template survey, old data-release README | Keep with manifest; not active |
| `round_p_rescinded/` | historical archive | Rescinded Round-P material | Keep; has `INDEX.md` |
| `scripts/` | historical script archive | Older archived scripts | Keep unless superseded by indexed restore archive |

## Removed empty directories

Removed on 2026-05-10 because they contained no files:

- `pre_fix_memos/`
- `file_organization_git_mv_20260509/`

## Known archive-only symlink issue

As of 2026-05-10, broken symlinks remain inside:

`file_organization_mv_only_20260509/outputs_archive/outputs/submission_bundle_20260417/`

These point to old submission-bundle material and are not active workspace links. Active symlink health should be checked outside `archive/`.

## Restore scripts

Primary restore scripts live in:

`reorg_20260509/restore/`

Notable current scripts:

- `ROOT_PYTHON_MIGRATION_20260510_RESTORE.sh`
- `ROOT_NONCODE_MIGRATION_20260510_RESTORE.sh`
- `STALE_202604_MARKDOWN_REVIEW_20260510_RESTORE.sh`
- `ROOT_DOCS_CLEANUP_20260510_RESTORE.sh`
- `RESIDUAL_REPORT_MD_GPT_20260510_RESTORE.sh`
- `RESIDUAL_SCRIPTS_20260510_RESTORE.sh`
- `RESIDUAL_LOGS_GPT_20260510_RESTORE.sh`
- `FINAL_TINY_RESIDUALS_20260510_RESTORE.sh`
- `LATEX_MANUSCRIPT_REORG_20260510_RESTORE.sh`
- `LATEX_UNUSED_FIGURES_20260510_RESTORE.sh`
- `R3_REPORTS_COORDINATION_RESTORE.sh`
- `R4_PAPER1_RELEASE_PROVENANCE_RESTORE.sh`
- `TOOLS_VALIDATION_PLOTTING_RESTORE.sh`

## Current cleanup status

- Archive top-level documentation exists: this file.
- Ambiguous empty archive directory `file_organization_git_mv_20260509/` has been removed.
- Empty `pre_fix_memos/` has been removed.
- Active `compute_vit/` root remains clean: root Markdown is limited to `README.md`, `PROJECT_INDEX.md`, and `WORKSPACE_LAYOUT.md`.
