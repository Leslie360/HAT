# Claude Takeover Cleanup Audit

Date: 2026-05-10
Scope: `/home/qiaosir/projects/compute_vit`
Policy: current filesystem is authoritative; no deletion; no commit; no push.

## 1. Active filesystem status

| Check | Result |
|---|---|
| Active broken symlinks in `/home/qiaosir/projects` | 0 |
| Active broken symlinks in `compute_vit` | 0 |
| Archive-only broken symlinks | Historical only; left unchanged |
| Paper-1 final bundle SHA | `32959fac881ad1659d2da0a4ebeba30846dac72986e032dc411ea6e916c6f4a4` |
| PCM precision-ladder guard | PASS via old and new tool paths |

## 2. Takeover action performed

The previous broken active workspace symlink:

```text
experiments/outputs/compute_vit -> ../../compute_vit/outputs
```

was moved into:

```text
archive/projects_root_cleanup_20260509/broken_symlinks/
```

and replaced with:

```text
experiments/outputs/compute_vit/README.md
```

Restore script:

```text
compute_vit/archive/reorg_20260509/restore/PROJECTS_EXPERIMENTS_OUTPUTS_LINK_RESTORE.sh
```

## 3. `compute_vit` git status interpretation

`compute_vit` currently shows many tracked deletions because prior cleanup moved old/historical paths into archives or canonical locations without staging the rename groups.

Approximate deleted tracked-path classes from `git status --porcelain=v1 -z`:

| Class | Count | Interpretation |
|---|---:|---|
| legacy archive moved to new archive | 323 | Old `_archive`, BFG reports, `outputs`, and similar history moved under `archive/file_organization_mv_only_20260509/` |
| old `report_md/_gpt` moved/missing from legacy location | 198 | Current active sync/report entrypoints moved into `coordination/active` or `paper1/reports` |
| release artifacts moved/archived | 97 | Final Paper-1 release/provenance promoted to `paper1/`; older artifacts archived |
| raw doctor data moved/archived | 32 | `数据_博士` historical/raw data moved into archive during mv-only cleanup |
| thesis files now exist under canonical thesis tree | 24 | `paper/thesis*` paths replaced by compatibility symlinks; canonical files under `thesis/en` and `thesis/cn` |
| Kimi draft / build residue paths absent from canonical tree | 27 | Draft/build residue paths intentionally excluded from active thesis/manuscript tree |
| Paper source-data old manifests/evals | 5 | Superseded canonical JSON artifacts moved or replaced |
| paper2 AIHWKit run scripts | 10 | Old run scripts moved/archived; active Work-2 migration not finalized |

## 4. Do not do blindly

Do not run:

```bash
git add -A
```

unless the user explicitly wants to commit the entire reorganization. The safe path is to stage by reviewed groups:

1. projects-root docs and README/NAVIGATION updates
2. `remote_reviews` symlinks and docs
3. `compute_vit/coordination/active` plus compatibility symlinks
4. `compute_vit/tools/{validation,plotting}` plus compatibility symlinks
5. `compute_vit/thesis` plus thesis compatibility symlinks
6. restore scripts paired with each move group
7. archive moves only after reviewing size and intent

## 5. Recommended next step

Stop structural moves here unless a specific target is named. The workspace is navigable and active broken symlinks are resolved. The remaining work is a Git decision: either preserve this reorganization through carefully staged commits, or restore selected move groups using the recorded restore scripts.
