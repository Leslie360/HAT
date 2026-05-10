# Claude MV-Only File Organization Report

Date: 2026-05-09
Executor: Claude
Scope: `/home/qiaosir/projects/compute_vit`
Policy: **mv only, no deletion**
Status: COMPLETE for full cleanup pass

## 1. Rule compliance

- No deletion was performed in this file-organization pass.
- All moved files/directories were moved under `archive/file_organization_mv_only_20260509/`.
- Restore commands were appended to `archive/file_organization_mv_only_20260509/restore/RESTORE_COMMANDS.sh`.
- Final submission bundle, active Paper-1 PDFs, active Paper-1 source, canonical current source data, checkpoints, datasets, and 105/107 review clones were preserved.
- Raw device data was moved, not deleted: `数据_博士/` is now under `archive/file_organization_mv_only_20260509/raw_device_data/数据_博士`.

## 2. Archive root

`archive/file_organization_mv_only_20260509/`

Subdirectories:

| Subdir | Purpose |
|---|---|
| `release_superseded/` | superseded release candidates and old reviewer bundle |
| `release_auxiliary/` | older source-data/Zenodo auxiliary packages |
| `build_outputs/` | nested LaTeX `.aux/.log/.out/.toc/.fls/.fdb_latexmk/.blg` build outputs |
| `top_level_build_outputs/` | top-level LaTeX build residues |
| `top_level_cache_and_ide/` | `.pytest_cache`, `.vscode` |
| `top_level_logs/` | top-level old GPU logs |
| `top_level_strays/` | one-off strays and moved legacy `_archive` wrapper |
| `legacy_archive_dirs/` | old `_archive` contents |
| `legacy_logs/` | old historical log directories |
| `old_reports/pre_p6_reports/` | older 202604 / R11D / Gemini / pre-P6 report files |
| `old_reports/p1_p5_phase_reports/` | P1-P5 / P3-P5 phase reports moved out of active `_gpt` view |
| `old_reports/p6_auxiliary_tasklists/` | superseded P6 auxiliary remote tasklists |
| `report_scratch_json/` | scratch JSON/report sidecars from `_gpt` |
| `paper2_old_scripts/` | old Work-2/R11D run/watch/test scripts |
| `paper2_logs_and_figures/` | Work-2 logs and figures |
| `paper2_auxiliary_source/` | non-current auxiliary Work-2 scripts/source helpers |
| `render_and_merge_scripts/` | one-off render/merged-figure helper scripts |
| `raw_device_data/` | raw device data formerly at `数据_博士/` |
| `local_tooling/` | local `.claude/` directory |
| `restore/` | restore script |

## 3. Logs

| Action | Log |
|---|---|
| First mv-only organization pass | `logs/file_organization_mv_only_20260509_224800.log` |
| LaTeX build-output move | `logs/file_organization_build_outputs_mv_20260509_224849.log` |
| Old report move | `logs/file_organization_old_reports_mv_20260509_224916.log` |
| P1-P5 phase report move | `logs/file_organization_phase_reports_mv_20260509_224958.log` |
| paper2 old-script move | `logs/file_organization_paper2_scripts_mv_20260509_225018.log` |
| Top-level clutter move | `logs/file_organization_top_level_mv_20260509_225347.log` |
| Report scratch move | `logs/file_organization_report_scratch_mv_20260509_225434.log` |
| paper2 logs/figures move | `logs/file_organization_paper2_logs_figures_mv_20260509_225502.log` |
| paper2 remaining logs/scripts move | `logs/file_organization_paper2_remaining_mv_20260509_225517.log` |
| paper2 auxiliary source move | `logs/file_organization_paper2_aux_mv_20260509_225548.log` |
| Raw device data move | `logs/file_organization_raw_device_data_mv_20260509_225632.log` |
| Final stray move | `logs/file_organization_final_strays_mv_20260509_225702.log` |
| Legacy logs move | `logs/file_organization_legacy_logs_mv_20260509_225735.log` |
| Legacy archive move | `logs/file_organization_legacy_archive_mv_20260509_225751.log` |
| Legacy coordination move | `logs/file_organization_legacy_coordination_mv_20260509_230209.log` |
| Render/merge scripts move | `logs/file_organization_render_scripts_mv_20260509_230238.log` |
| Local Claude tooling move | `logs/file_organization_claude_local_mv_20260509_230248.log` |

## 4. Final counts

| Metric | Value |
|---|---:|
| Files under mv-only archive | 4,514 |
| Restore script lines | 498 |
| Remaining untracked items | 77 |
| Git status entries | 844 |

The `git status` entry count increased because many tracked build outputs and historical files now appear as deleted from their old paths after `mv`. They are not destroyed; every moved item has a restore command.

## 5. Critical files verified still present

| Artifact | Status |
|---|---|
| `paper/latex_gpt/main.pdf` | OK |
| `paper/latex_gpt/supplementary_main.pdf` | OK |
| `paper/latex_gpt/cover_letter.pdf` | OK |
| `paper1/release/paper1_submission_bundle_20260509_final/` | OK |
| `paper1/release/paper1_submission_bundle_20260509_final.tar.gz` | OK |
| `paper1/provenance/paper1_provenance_archive_20260509/` | OK |
| `paper1/provenance/paper1_provenance_archive_20260509.tar.gz` | OK |
| `report_md/_gpt/KIMI_P8_TRACK_J_FINAL_USER_HANDOFF_MAP_20260509.md` | OK |
| `report_md/_gpt/CLAUDE_P8_SELF_AUDIT_20260509.md` | OK |
| `scripts/_gpt/check_local_pcm_precision_ladder.py` | OK |
| `report_md/_gpt/AGENT_SYNC_gpt.md` | OK |
| `report_md/_gpt/CLAUDE_TASK_gpt.md` | OK |
| `/home/qiaosir/projects/remote_reviews/105/` | Not touched |
| `/home/qiaosir/projects/remote_reviews/107/` | Not touched |

Final tarball SHA remains:

`32959fac881ad1659d2da0a4ebeba30846dac72986e032dc411ea6e916c6f4a4  paper1/release/paper1_submission_bundle_20260509_final.tar.gz`

Bundle SHA check remains PASS.

## 6. Remaining active/untracked items by design

| Remaining item | Reason kept active |
|---|---|
| `archive/cleanup_candidates_20260509/` | P8 cleanup quarantine; kept visible for audit |
| `archive/file_organization_mv_only_20260509/` | this restore-capable cleanup archive |
| `broadcast.md` | active coordination broadcast |
| `paper/latex_gpt/sections/08_availability.tex` | active Paper-1 source file |
| `paper/latex_gpt/source_data/canonical_json/manifest_canonical_json_20260509.*` | current canonical manifest |
| `paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed456/`, `pcm_6bit_seed457/` | current corrected canonical data |
| `paper/latex_gpt/source_data/canonical_json/deprecated_20260501_old_protocol/` | provenance archive for old protocol |
| `paper/latex_gpt/supplementary/figS5_proxy_sensitivity_tikz.tex` | active supplement source |
| `thesis/cn/ (compat: paper/thesis_cn/)*`, `thesis/en/ (compat: paper/thesis/)XJTU-thesis/` | thesis work, not Paper-1 submission scope |
| `paper1/release/paper1_submission_bundle_20260509_final*` | final submission bundle |
| `paper1/provenance/paper1_provenance_archive_20260509*` | final provenance archive |
| `report_md/_gpt/KIMI_P6/P7/P8*`, P6/P7 acceptance/audits, P8 task files | active audit trail |

## 7. Restore

Full restore:

```bash
bash archive/file_organization_mv_only_20260509/restore/RESTORE_COMMANDS.sh
```

Selective restore: copy one line from the restore script for the specific file/directory.

## 8. Commit caution

Do not stage the archive blindly. If committing, use a conservative staging list:

- active Paper-1 source/bundle/P6-P8 reports if desired;
- exclude `archive/file_organization_mv_only_20260509/` unless the repository intentionally tracks cleanup archives;
- exclude raw checkpoints/datasets;
- decide separately whether thesis files belong in the same commit.

## 9. Verdict

Full mv-only organization pass complete. No deletion performed. Final submission artifacts remain intact and verified. The top-level workspace is now reduced to active code/source, final artifacts, logs, reports, checkpoints/data, and the restore-capable archive.
