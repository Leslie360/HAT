# DISPATCH KIMI-PAPER-SYNC — Root paper/ ↔ compute_vit/paper/ Housekeeping
**Date:** 2026-04-24 22:30 CST
**Issued by:** Claude
**Assignee:** Kimi (can delegate grep/copy ops to Codex if preferred)
**Priority:** LOW
**Time budget:** ~30 min

---

## 1. Objective

Reconcile any divergence between `/home/qiaosir/projects/paper/` (root level) and `/home/qiaosir/projects/compute_vit/paper/` (project level). The project-level directory is authoritative; the root-level is a legacy/convenience mirror.

---

## 2. Tasks

### 2.1 Audit

- `diff -r /home/qiaosir/projects/paper/ /home/qiaosir/projects/compute_vit/paper/ | head -50`
- Identify:
  - Files present in one but not the other
  - Files present in both but content-diverged
  - Last-modified timestamp comparison

### 2.2 Classify divergence

For each divergent file:
- **Project-level newer**: delete root-level copy (root is stale)
- **Root-level newer**: investigate — may be user-edited, flag to Claude before overwrite
- **Present only at one level**: determine canonical location

### 2.3 Reconcile

- Default: mirror `compute_vit/paper/` → `paper/` (one-way, project→root)
- If user-edited root file found: **STOP, flag to Claude**, do not overwrite
- Any deletions: confirm with user before executing

### 2.4 Canonicalize

Decide one source-of-truth location going forward:
- Recommendation: `compute_vit/paper/` (where all LaTeX, figures, drafts live)
- Root `paper/` becomes a symlink to `compute_vit/paper/` if that's cleanly possible

### 2.5 Deliverable

`KIMI_PAPER_SYNC_REPORT_20260424.md`:
- Divergence map (file-level)
- Reconciliation actions taken
- Symlink decision (if applicable)
- Any user-flagged items requiring attention

---

## 3. Constraints

- **No overwrites of user-edited files** without explicit Claude approval
- **No git operations** beyond what's needed for the sync (no new commits, no push)
- **Dry run first**: list all intended actions before executing

---

## 4. Success criteria

- Single source of truth for manuscript files
- Clean diff after sync (or documented remaining divergences)
- Pre-submission housekeeping one less thing to worry about
