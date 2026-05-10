# DS Workspace Organization Review

**Date:** 2026-05-09
**Reviewer:** DS

## Verdict: GOOD FOUNDATION, 3 ACTIONABLE ISSUES

The file reorganization (by whichever agent) significantly improved the project structure. Root-level noise eliminated, coordination files logically organized, remote reviews consolidated. However, 3 issues need attention.

---

## What Was Done Well ✅

1. **Root-level cleanup** — Old REMOTE tasklists, AGENT_INTERCOM_HUB, GPU_SCHEDULE, gpu_watcher.sh, output.md all moved to archive. Root is now much cleaner.
2. **Coordination structure** — `coordination/` with active/, agent_reports/, remote_tasks/, audits/, dispatches/ is a logical, discoverable layout.
3. **Remote reviews consolidated** — `remote_reviews/` with 105/107 + README + INDEX is clean.
4. **Rollback exists** — `RESTORE_COMMANDS.sh` in archive/file_organization_mv_only_20260509/restore/ provides recovery path.

---

## Issues Found ⚠️

### Issue 1: Two Divergent BROADCAST.md Files

| File | Lines | Status |
|------|-------|--------|
| `/home/qiaosir/projects/BROADCAST.md` | 6279 | ✅ Most recent, has P6/P7 broadcasts |
| `compute_vit/coordination/active/broadcast.md` | 3974 | ❌ Missing ~2300 lines of history |
| `compute_vit/broadcast.md` | symlink | ❌ Points to the outdated copy |

**Impact**: Anyone reading `compute_vit/broadcast.md` (the symlink) sees an incomplete broadcast log. The symlink should point to the root BROADCAST.md, or the root copy should be synced into coordination/active/.

**Fix**: Replace the symlink to point to `/home/qiaosir/projects/BROADCAST.md`, or cp the root version over the coordination copy.

### Issue 2: Archive Has No INDEX / README

`compute_vit/archive/` has 7 subdirectories:
- `cleanup_candidates_20260509/` (quarantined old drafts, files)
- `file_organization_mv_only_20260509/` (git-mv reorg backup)
- `file_organization_git_mv_20260509/` (git mv variant)
- `reorg_20260509/`, `pre_fix_memos/`, `round_p_rescinded/`, `scripts/`

No README explains what each subdirectory contains or whether they can be safely deleted.

**Fix**: Add `archive/README.md` describing each subdirectory's purpose and safe-to-delete status.

### Issue 3: Archive Naming Ambiguity

Two directory names differ only by `git_mv` vs `mv_only`:
- `file_organization_git_mv_20260509/`
- `file_organization_mv_only_20260509/`

Future readers won't know which one was actually applied or which has the authoritative restore script.

**Fix**: Add a `_ACTIVE` suffix or a symlink `archive/_LATEST -> file_organization_mv_only_20260509` so it's clear which reorg is current. Or consolidate into one directory.

---

## Severity

| Issue | Severity | Fix Time |
|-------|----------|----------|
| 1. Divergent BROADCAST.md | **Medium** — affects all agent coordination | < 1 min |
| 2. Archive no README | **Low** — confusing but not breaking | < 5 min |
| 3. Archive naming | **Low** — cosmetic | < 1 min |

---

*DS review. 2026-05-09.*
