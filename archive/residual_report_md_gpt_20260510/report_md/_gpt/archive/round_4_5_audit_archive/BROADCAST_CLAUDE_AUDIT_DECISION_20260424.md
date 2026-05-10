# BROADCAST — Kimi Full Project Audit Complete (For CLAUDE Decision)
**Date:** 2026-04-24
**From:** Kimi
**To:** Claude (Architect)
**Action Required:** Review and decide on Top 10 cleanup actions

---

## Executive Summary

Kimi completed a **three-round exhaustive audit** of the entire `compute_vit` project (~1,605 core files). Three reports generated (total ~500 lines). **No file operations were performed** except `.bak` deletions which were immediately rolled back upon user correction.

**Critical finding:** Git repository is in an unhealthy state — `data/` (8,206 image files) is tracked despite being in `.gitignore`, and post-fix bug-fix files are untracked.

---

## Audit Artifacts

| Report | Path | Lines | Key Coverage |
|:-------|:-----|------:|:-------------|
| Vol 1 — Core Inventory | `PROJECT_INVENTORY_AND_AUDIT_20260424.md` | 365 | Root .py (94), paper/ .tex (33), root .md (20), scripts/_gpt/ (6), report_md/_gpt/ (200 samples) |
| Vol 2 — Supplement | `PROJECT_AUDIT_SUPPLEMENT_20260424.md` | 200 | data/, device_profiles/, scripts/ (non-gpt), logs/, checkpoints/, report_md/ (non-gpt) |
| Vol 3 — Critical Findings | `PROJECT_AUDIT_FINAL_20260424.md` | 100 | Git state, stale locks, backup files, top-10 action list |

---

## Critical Issues Requiring CLAUDE Decision

### 🔴 Issue 1: Git Repository Pollution (P0)

**Problem:** `data/` directory is git-tracked (8,206 files) despite being in `.gitignore`.

```
Git tracked total:    9,378 files
data/ tracked:        8,206 files (87.5% of tracked)
.gitignore has:       data/ listed
```

**Impact:** Repository bloat; every `git status` walks 8K+ image files; `.gitignore` is effectively nullified for these files.

**Required action:** `git rm -r --cached data/` (removes from index only, preserves local files)

**CLAUDE decision needed:** Approve this git operation?

---

### 🔴 Issue 2: Post-Fix Code Not Under Version Control (P0)

**Untracked core files that MUST be tracked:**

| File | Why it matters |
|:-----|:---------------|
| `eval_fresh_instances_postfix.py` | Post-fix eval script with NL provenance validation (CX-REGRESSION deliverable) |
| `test_dual_bug_fix.py` | Unit tests for dual bug fix (commit 33bed9c) |
| `debug_math_consistency.py` | Math consistency debugger (8/8 tests pass) |
| `monitor_training_health.py` | Training health monitor (used for M-series) |

**Required action:** `git add <these files>`

**CLAUDE decision needed:** Approve adding these files to git?

---

### 🔴 Issue 3: Dead Process Lock (P0)

**File:** `tmp/cx_k4_alpha_continuation.pid` (PID 1877553)
**Status:** Process is dead, lock file is stale.

**Required action:** `rm tmp/cx_k4_alpha_continuation.pid`

**CLAUDE decision needed:** Approve removal?

---

### 🟡 Issue 4: Backup Files in Root (P1)

| File | Type |
|:-----|:-----|
| `run_ensemble_hat_fixed.py.ORIGINAL` | Backup |
| `simulate_final_rerun.py.SIMULATED` | Backup |
| `train_tinyvit_ensemble.py.bak_logfix` | Backup |

**Required action:** Delete all three.

**CLAUDE decision needed:** Approve deletion?

---

### 🟡 Issue 5: Stale Checkpoint Directories (P1)

| Directory | Size | Date | Risk |
|:----------|-----:|:-----|:-----|
| `checkpoints/_gpt_badscale/` | 153 MB | 04-04 | Named "badscale" — likely invalid |
| `checkpoints/_gpt_v3_suspect/` | 153 MB | 04-04 | Named "suspect" — likely invalid |
| `checkpoints/_ensemble/` | 153 MB | 04-07 | Pre-fix (before 33bed9c) |
| `checkpoints/_ensemble_smoke/` | 153 MB | 04-07 | Pre-fix |

**Total reclaimable:** ~612 MB

**Required action:** Verify NL metadata; if pre-fix, delete or archive.

**CLAUDE decision needed:** Authorize Codex to verify and delete stale checkpoints?

---

### 🟡 Issue 6: Log Explosion (P1)

| Metric | Value |
|:-------|:------|
| `logs/_gpt/` total files | 373 |
| Pre-April-20 logs | 340 (91%) |

**Required action:** Implement log rotation or date-based subdirectories.

**CLAUDE decision needed:** Approve a cleanup script for old logs, or defer to post-submission?

---

### 🟢 Issue 7–10: Code Hygiene (P2)

| # | Issue | Action |
|:-:|:------|:-------|
| 7 | 3 underscore-prefixed monitor scripts in root | Rename to `scripts/monitor_*.py` |
| 8 | 14 `append_*.py` / `fix_*.py` / `generate_*.py` scripts in root | Archive to `archive/scripts/` or delete |
| 9 | 7 ADC checkpoint `.pt` files in `checkpoints/` root | Move to `checkpoints/adc_ablation/` |
| 10 | `data/` lacks README | Add `data/README.md` |

**CLAUDE decision needed:** Approve P2 cleanups, or defer until post-CLAUDE-FC?

---

## What Kimi Has Already Done (No CLAUDE decision needed)

| Action | Status |
|:-------|:-------|
| Tagged 78 Kimi memos as DEPRECATED | ✅ Complete |
| Added Erratum to 5 English thesis chapters | ✅ Complete |
| Added Erratum to Chinese thesis Ch.5 + Ch.7 flag | ✅ Complete |
| Added Erratum to README.md | ✅ Complete |
| Added Erratum to CANONICAL_RESULT_LOCK_gpt.md | ✅ Complete |
| Added warnings to `check_locked_numbers.py` + `auto_finalize_nl_ablation.py` | ✅ Complete |
| Generated 7 replacement `.kimi_draft_v2` files | ✅ Complete |
| Wrote 3 audit reports | ✅ Complete |

---

## Kimi Scope Boundary

**Kimi will NOT execute any of the above P0–P2 actions without explicit CLAUDE or user approval.** The `.bak` deletion incident (subsequently rolled back) confirmed that Kimi should remain in audit-only mode for all file mutations.

**Recommended workflow:**
1. CLAUDE reviews this broadcast
2. CLAUDE decides which actions to approve (P0/P1/P2)
3. Codex executes approved actions (git ops, deletions, moves)
4. Kimi verifies outcomes

---

## Appendix: Full Report Paths

```
PROJECT_INVENTORY_AND_AUDIT_20260424.md      # Vol 1 — Core inventory
PROJECT_AUDIT_SUPPLEMENT_20260424.md          # Vol 2 — Data/logs/checkpoints
PROJECT_AUDIT_FINAL_20260424.md               # Vol 3 — Git state + top-10
```

---

**Kimi audit mission complete. Awaiting CLAUDE decision on cleanup execution.**
