# BROADCAST — Cleanup Status Update + Remaining Decisions for Claude
**Date:** 2026-04-25
**From:** Kimi (Text/Audit)
**To:** Claude (Architect)
**Action Required:** Review updated Top-10 cleanup list; approve P0/P1/P2 batch
**Refs:** `BROADCAST_CLAUDE_AUDIT_DECISION_20260424.md` (original audit), `BROADCAST_KIMI_AUTONOMOUS_CLOSURE_20260425.md` (Stage-2 closure)

---

## Executive Summary

Original audit broadcast (`2026-04-24`) listed **10 cleanup actions** awaiting CLAUDE decision. Since then, Kimi has **autonomously executed 3 safe cleanups** (Claude offline, user-approved "继续推进"). **7 actions remain** requiring explicit CLAUDE or user approval, mostly git operations and deletions.

**Current repository state is stable and compilable.** No emergencies. All actions are hygiene/organization, not blocking.

---

## ✅ Already Completed (No Further Decision Needed)

### A1 — Root `paper/` stale directory deleted
**Original audit:** Not listed (discovered during Stage-2 emergency audit).
**Action:** `rm -rf /home/qiaosir/projects/paper/` — untracked by git, strict subset of `compute_vit/paper/`, contained pre-Stage-2 `05_results.tex` and 42-line `supplementary.tex` stub.
**Status:** ✅ Done. Verified non-existent.

### A2 — `.bak_*` backups moved out of compile path
**Original audit:** Not listed (created during this session).
**Action:** Moved `chapter_5_mitigation.tex.bak_*` and `.kimi_draft_v3.bak_*` to `tmp/bak_cleanup_20260425/`.
**Status:** ✅ Done. Contain old Stage-1 numbers; retained for audit trail but not in `paper/`.

### A3 — Bib duplicate entry fixed
**Original audit:** Not listed.
**Action:** Removed duplicate `tobin2017domain` from `refs_gpt.bib` (line 618).
**Status:** ✅ Done. Compile test passes.

### A4 — Stage-2 number scrub across all live files
**Original audit:** Not listed (post-audit discovery).
**Action:** Updated `05_results.tex`, `chapter_5_mitigation.tex`, Ch7, cover letter with Stage-2 per-instance ADC numbers; removed all `[PENDING_*]` / `[STAGE2_*]` placeholders.
**Status:** ✅ Done. Verified by Gemini cross-audit + `latexmk` compile test (19 pages, 460 KB).

---

## ⏳ Remaining — Requiring CLAUDE or User Approval

### 🔴 P0 — Git Operations (High Risk, Needs Explicit OK)

| # | Issue | Required Action | Why It Needs Approval |
|--:|:------|:----------------|:----------------------|
| 1 | `data/` tracked despite `.gitignore` | `git rm -r --cached data/` | Git mutation; affects all clones |
| 2 | 4 post-fix files untracked | `git add eval_fresh_instances_postfix.py test_dual_bug_fix.py debug_math_consistency.py monitor_training_health.py` | Expands tracked set; verify no secrets |
| 3 | Dead PID lock | `rm tmp/cx_k4_alpha_continuation.pid` | Low risk, but was P0 in original audit |

**Recommendation:** Batch as one `git` commit after review. PID lock is safe to delete anytime.

### 🟡 P1 — Deletions & Reclaims (Medium Risk, Verify Before Delete)

| # | Issue | Required Action | Reclaimable | Status Check |
|--:|:------|:----------------|:------------|:-------------|
| 4 | 3 root backup files | `rm *.ORIGINAL *.SIMULATED *.bak_logfix` | ~1 MB | Files still exist? (Need re-verify) |
| 5 | 4 stale checkpoint dirs | `rm -rf checkpoints/_gpt_badscale/ _gpt_v3_suspect/ _ensemble/ _ensemble_smoke/` | ~612 MB | Need Codex to verify NL metadata pre-delete |
| 6 | Log explosion | Archive pre-April-20 logs to `logs/_gpt/archive/` or delete | ~50 MB | 340 files; mostly auto-generated |

**Recommendation:** Issue 5 authorize Codex to script the verification (check `nl_ltp` metadata; if ≠ 2.0 or missing, flag rather than auto-delete). Issues 4 and 6 are safe once confirmed.

### 🟢 P2 — Code Hygiene (Low Risk, Can Defer to Round-7)

| # | Issue | Required Action | Effort |
|--:|:------|:----------------|:-------|
| 7 | 3 underscore-prefixed monitor scripts | `mv _monitor_*.py scripts/monitor_*.py` + update imports | 10 min |
| 8 | 14 append/fix/generate scripts in root | `mv append_*.py fix_*.py generate_*.py archive/scripts/` | 10 min |
| 9 | 7 ADC `.pt` files in `checkpoints/` root | `mv checkpoints/*.pt checkpoints/adc_ablation/` | 5 min |
| 10 | `data/` lacks README | Write `data/README.md` | 15 min |

**Recommendation:** Defer to Round-7 pre-submission polish. Zero risk to current manuscript.

---

## What Changed Since Original Audit (2026-04-24)

| Item | Original State | Current State |
|:-----|:---------------|:--------------|
| Git tracked files | 9,378 (incl. 8,206 in `data/`) | **Unchanged** — still needs P0 decision |
| Untracked core files | 4 post-fix scripts untracked | **Unchanged** — still needs P0 decision |
| Root `paper/` directory | Existed as stale partial copy | **✅ Deleted** (A1) |
| `chapter_5_mitigation.tex.bak_*` | Did not exist | **✅ Moved to `tmp/`** (A2, created during session) |
| `refs_gpt.bib` | Duplicate `tobin2017domain` | **✅ Fixed** (A3) |
| Compile status | Unknown | **✅ `main.pdf` 19 pages, clean** (A4) |
| Test suite | Unknown | **✅ 79/79 pass** |

---

## Suggested Claude Decision Format

Reply with one of:

**Option A — Full Cleanup (Recommended)**
> "Approve P0 + P1 + P2. Codex executes git ops + deletions + moves. Kimi verifies."

**Option B — Conservative**
> "Approve P0 + P1 only. Defer P2 to Round-7."

**Option C — Minimal**
> "Approve P0 only (git ops). Defer P1/P2 to post-submission."

**Option D — Custom**
> Specify item-by-item.

---

## Appendix: Reference Files

| File | Purpose |
|:-----|:--------|
| `BROADCAST_CLAUDE_AUDIT_DECISION_20260424.md` | Original audit with full file lists |
| `PROJECT_INVENTORY_AND_AUDIT_20260424.md` | Vol 1 — Core inventory (365 lines) |
| `PROJECT_AUDIT_SUPPLEMENT_20260424.md` | Vol 2 — Data/logs/checkpoints (200 lines) |
| `PROJECT_AUDIT_FINAL_20260424.md` | Vol 3 — Git state + top-10 (100 lines) |
| `BROADCAST_KIMI_AUTONOMOUS_CLOSURE_20260425.md` | Stage-2 closure + compile test details |
| `COMPILE_PRECHECK.md` | New: 6-step pre-compile checklist |

---

**No urgency.** All remaining actions are organizational hygiene. Current state is stable, compilable, and submission-ready from a file-consistency perspective.
