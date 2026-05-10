# compute_vit Project Reorganization Plan

Date: 2026-05-09
Scope: `/home/qiaosir/projects/compute_vit`
Goal: Convert the repository from phase/history accumulation into a clean, purpose-indexed workspace.

## 1. Current state

The workspace has already had a mv-only cleanup pass. No files were deleted. The current archive root is:

`archive/file_organization_mv_only_20260509/`

Restore script:

`archive/file_organization_mv_only_20260509/restore/RESTORE_COMMANDS.sh`

Final Paper-1 submission bundle remains verified:

`32959fac881ad1659d2da0a4ebeba30846dac72986e032dc411ea6e916c6f4a4  paper1/release/paper1_submission_bundle_20260509_final.tar.gz`

## 2. Immediate problem

The workspace is visually cleaner, but Git status is not clean because tracked historical/build files were moved by filesystem `mv`; Git sees old paths as deleted and the archive as untracked. This is expected and recoverable, but it means the next step must be deliberate.

## 3. Desired target

Use `WORKSPACE_LAYOUT_V2_20260509.md` as the target layout:

```text
paper1/
work2/
thesis/
data_local/
experiments/
coordination/
tools/
tests/
logs/
archive/
```

## 4. Recommended next execution phases

### R1 — Foundation, no core moves

Status: mostly complete.

Actions:

- Keep final Paper-1 bundle in current location for submission safety.
- Keep `paper/latex_gpt/` active until after submission or Codex acceptance.
- Use file inventory as the source of truth.

Deliverables:

- `WORKSPACE_LAYOUT_V2_20260509.md`
- `ROOT_REORG_PLAN_20260509.md`
- `FILE_PURPOSE_INVENTORY_20260509.tsv`

### R2 — Normalize archive structure

Move current cleanup archives into clearer names:

```text
archive/cleanup/20260509_p8_candidates/
archive/cleanup/20260509_mv_only_workspace/
archive/cleanup/restore/
```

Keep this local unless user wants archive committed.

### R3 — Split reports by role

Target mapping:

```text
report_md/_gpt/KIMI_P6* -> paper1/reports/P6/KIMI/
report_md/_gpt/KIMI_P7* -> paper1/reports/P7/KIMI/
report_md/_gpt/KIMI_P8* -> paper1/reports/P8/KIMI/
report_md/_gpt/DS_PHASE_P6* -> paper1/reports/P6/audits/DS/
report_md/_gpt/MIMO_PHASE_P6* -> paper1/reports/P6/audits/MIMO/
report_md/_gpt/CODEX_PHASE_P6* -> paper1/reports/P6/acceptance/
report_md/_gpt/DISPATCH_SUPERPHASE_P6* -> coordination/dispatches/P6/
report_md/_gpt/REMOTE_105_PHASE_P8* -> coordination/remote_tasks/105/
report_md/_gpt/REMOTE_107_PHASE_P8* -> coordination/remote_tasks/107/
```

Keep compatibility index in `report_md/_gpt/INDEX_CURRENT.md` if needed.

### R4 — Paper-1 migration

Only after acceptance/submission safety check:

```text
paper/latex_gpt/ -> paper1/manuscript/
paper/figures/ -> paper1/figures/legacy_main_figures/
paper1/release/paper1_submission_bundle_20260509_final* -> paper1/release/
paper1/provenance/paper1_provenance_archive_20260509* -> paper1/provenance/
```

Required verification:

- rebuild PDFs;
- verify tarball SHA;
- update any scripts that assume `paper/latex_gpt`;
- grep stale values.

### R5 — Work-2 migration

```text
paper2/ -> work2/kv_cache/
paper2_aihwkit_baseline/ -> work2/aihwkit_pcm/
```

For large local payloads:

```text
paper2_aihwkit_baseline/checkpoints/ -> data_local/checkpoints/work2_aihwkit/
paper2_aihwkit_baseline/data/ -> data_local/datasets/work2_aihwkit/
```

Use symlinks or config updates if scripts hard-code old paths.

### R6 — Thesis migration

```text
thesis/en/ (compat: paper/thesis/) -> thesis/en/
thesis/cn/ (compat: paper/thesis_cn/) -> thesis/cn/
thesis/en/ (compat: paper/thesis/)XJTU-thesis/ -> thesis/xjtu_template/
```

Required check:

- grep thesis for stale Paper-1 values: `68.55`, `0.07`, `86.37 ± 0.19`.

### R7 — Tool migration

```text
scripts/_gpt/check_local_pcm_precision_ladder.py -> tools/validation/
scripts/_gpt/plot_paper1_*.py -> tools/plotting/
scripts/oneshot_root/ -> experiments/scripts/oneshot/
```

## 5. Git strategy options

### Option A — Archive is local-only

Restore tracked moved paths before commit, then commit only active Paper-1/P8 changes.

Pros: clean commit, avoids large archive.
Cons: visual clutter returns unless `.gitignore` or local archive policy handles it.

### Option B — Commit the reorganization

Stage moved old paths and archive paths together so Git records deletions/additions/renames.

Pros: repository becomes clean for everyone.
Cons: large commit; archive may bloat repo.

### Option C — Hybrid recommended

- Commit active Paper-1/P8 files.
- Keep `archive/file_organization_mv_only_20260509/` local-only.
- Later create a smaller curated archive commit with only indexes/manifests, not raw payloads.

## 6. Current recommendation

Before Paper-1 submission, choose Option C:

1. Do not commit the bulk archive yet.
2. Use final tarball for submission.
3. Keep mv-only archive local and restorable.
4. After submission, do R3/R4/R5 as a proper branch-level reorganization.

## 7. Safety checks before any future move

- `sha256sum paper1/release/paper1_submission_bundle_20260509_final.tar.gz`
- `sha256sum -c paper1/release/paper1_submission_bundle_20260509_final/SHA256SUMS.txt`
- `python scripts/_gpt/check_local_pcm_precision_ladder.py`
- stale-value grep for `68.55`, `0.07 pp`, stale 6-bit `\notrun`, stale `86.37 ± 0.19` aggregate.


## Projects-root note

The real workspace root is `/home/qiaosir/projects`. This document applies to the `compute_vit/` subproject only. See `/home/qiaosir/projects/PROJECTS_ROOT_LAYOUT_20260509.md` for workspace-level organization.
