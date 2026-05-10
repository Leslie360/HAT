# Claude Structured Reorganization Execution Report

Date: 2026-05-10
Scope: `/home/qiaosir/projects` and `/home/qiaosir/projects/compute_vit`
Policy: reversible organization; no deletion; no commit; no push.

## 1. Executive status

The interrupted structured reorganization step has been verified and closed.

| Area | Status |
|---|---|
| Active coordination migration | PASS |
| Validation/plotting tools migration | PASS |
| Thesis tree migration | PASS |
| Legacy compatibility symlinks | PASS |
| Paper-1 final bundle SHA | PASS |
| PCM precision-ladder guard via old and new paths | PASS |

## 2. Canonical locations after reorganization

### Workspace root

`/home/qiaosir/projects` is the workspace root. `compute_vit/` is the main project, while `remote_reviews/105` and `remote_reviews/107` are sibling review clones.

### Active coordination

Canonical active coordination files are now:

```text
compute_vit/coordination/active/AGENT_SYNC_gpt.md
compute_vit/coordination/active/CLAUDE_TASK_gpt.md
compute_vit/coordination/active/broadcast.md
```

Compatibility symlinks remain valid:

```text
compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md -> ../../coordination/active/AGENT_SYNC_gpt.md
compute_vit/report_md/_gpt/CLAUDE_TASK_gpt.md -> ../../coordination/active/CLAUDE_TASK_gpt.md
compute_vit/broadcast.md -> coordination/active/broadcast.md
```

### Validation and plotting tools

Canonical tool locations are now:

```text
compute_vit/tools/validation/check_local_pcm_precision_ladder.py
compute_vit/tools/plotting/plot_paper1_decision_map.py
compute_vit/tools/plotting/plot_paper1_spine.py
```

Compatibility symlinks remain valid:

```text
compute_vit/scripts/_gpt/check_local_pcm_precision_ladder.py -> ../../tools/validation/check_local_pcm_precision_ladder.py
compute_vit/scripts/_gpt/plot_paper1_decision_map.py -> ../../tools/plotting/plot_paper1_decision_map.py
compute_vit/scripts/_gpt/plot_paper1_spine.py -> ../../tools/plotting/plot_paper1_spine.py
```

### Thesis tree

Canonical thesis locations are now:

```text
compute_vit/thesis/en
compute_vit/thesis/cn
compute_vit/thesis/xjtu_template
```

Compatibility symlinks remain valid:

```text
compute_vit/paper/thesis -> ../thesis/en
compute_vit/paper/thesis_cn -> ../thesis/cn
compute_vit/thesis/en/XJTU-thesis -> ../xjtu_template
```

## 3. Verification evidence

### Paper-1 final bundle

```text
32959fac881ad1659d2da0a4ebeba30846dac72986e032dc411ea6e916c6f4a4  compute_vit/paper1/release/paper1_submission_bundle_20260509_final.tar.gz
```

### PCM guard

The precision-ladder guard passed through both the compatibility symlink and canonical tools path:

```text
python scripts/_gpt/check_local_pcm_precision_ladder.py  # PASS
python tools/validation/check_local_pcm_precision_ladder.py  # PASS
```

Verification log:

```text
compute_vit/logs/reorg_102_pcm_guard_verify_20260510_000223.log
```

### Restore scripts present

```text
compute_vit/archive/reorg_20260509/restore/ACTIVE_COORDINATION_RESTORE.sh
compute_vit/archive/reorg_20260509/restore/TOOLS_VALIDATION_PLOTTING_RESTORE.sh
compute_vit/archive/reorg_20260509/restore/THESIS_MIGRATION_RESTORE.sh
compute_vit/archive/reorg_20260509/restore/R3_REPORTS_COORDINATION_RESTORE.sh
compute_vit/archive/reorg_20260509/restore/R3_REPORT_MD_RESIDUALS_RESTORE.sh
compute_vit/archive/reorg_20260509/restore/R4_PAPER1_RELEASE_PROVENANCE_RESTORE.sh
compute_vit/archive/reorg_20260509/restore/PROJECTS_ROOT_REMOTE_REVIEWS_RESTORE.sh
compute_vit/archive/reorg_20260509/restore/PROJECTS_ROOT_REPORT_MD_RESTORE.sh
compute_vit/archive/reorg_20260509/restore/PROJECTS_ROOT_DOCS_RESTORE.sh
compute_vit/archive/reorg_20260509/restore/PROJECTS_ROOT_LAYOUT_DOCS_RESTORE.sh
compute_vit/archive/reorg_20260509/restore/PROJECTS_ROOT_TOP_LEVEL_CLUTTER_RESTORE.sh
```

## 4. Explicit non-actions

The following were intentionally not done:

- No files were deleted.
- No commit was created.
- No push was made.
- `compute_vit/paper/latex_gpt/` was not moved because it still has high hardcoded-path risk.
- No GPU jobs were launched.

## 5. Remaining caveat

The workspace has many uncommitted changes and symlinked/moved paths from the broader cleanup. Do not stage with `git add -A` blindly. If preserving the reorganization in Git, stage by reviewed path groups and keep restore scripts with the moves they reverse.

## 6. Safe next actions

1. Review this report with the projects-wide management report:
   - `docs/PROJECTS_WIDE_FILE_MANAGEMENT_REPORT_20260509.md`
2. Decide whether to keep the reorganization in Git or restore selected moves.
3. If keeping it, stage explicitly by group: projects-root docs, remote review symlinks, compute_vit coordination, tools, thesis, and restore scripts.
