# CLAUDE DEEP CLEANUP EXECUTION REPORT
**Date:** 2026-04-25 11:50 CST
**From:** Claude (Chief Architect)
**Authority:** User directive "你来做一次深层次的项目整理清理" + Kimi 3-vol audit (`BROADCAST_CLAUDE_AUDIT_DECISION_20260424.md`) + Kimi cleanup proposal (`BROADCAST_CLAUDE_CLEANUP_UPDATE_20260425.md`)
**Status:** Physical cleanup COMPLETE; git operations PREPARED but DEFERRED to user

---

## 0. Decision: Option B+ (Conservative + safe extensions)

Per user authorization for "deep cleanup" + Kimi's recommendation to defer git ops:
- **Executed**: All non-git physical cleanup (deletions, relocations, archives, README creation)
- **Deferred to user**: All git index mutations (`git rm --cached`, `git add`, commits)
- **Protected**: Canonical assets (`checkpoints/_ensemble/`, paper baselines, manuscript files)

---

## 1. EXECUTED — Physical cleanup

### 1A. Safe deletions (low-risk, named-explicit-stale)

| Target | Reason |
|:--|:--|
| `tmp/cx_k4_alpha_continuation.pid` | Dead PID lock (PID 1877553), process gone |
| `run_ensemble_hat_fixed.py.ORIGINAL` | Backup, root clutter |
| `simulate_final_rerun.py.SIMULATED` | Backup, root clutter |
| `train_tinyvit_ensemble.py.bak_logfix` | Backup, root clutter |
| `.codex` (empty file) | Zero-byte agent artifact |
| 3× `__pycache__/` dirs | Auto-regenerable Python bytecode |

### 1B. Stale checkpoint dirs (459 MB reclaimed)

| Dir | Size | Reason | Action |
|:--|--:|:--|:--|
| `checkpoints/_gpt_badscale/` | 153 MB | Filename explicit "badscale" | DELETED |
| `checkpoints/_gpt_v3_suspect/` | 153 MB | Filename explicit "suspect" | DELETED |
| `checkpoints/_ensemble_smoke/` | 153 MB | Smoke test (04-07, pre-fix) | DELETED |
| **`checkpoints/_ensemble/`** | 153 MB | **Canonical V4 Ensemble HAT — source of 86.37% / OPECT 88.53% / AR(1) zone-3A** | **PROTECTED — NOT deleted** |

`_ensemble/` is referenced by `eval_fresh_instances.py`, `scripts/_gpt/eval_spatially_correlated_d2d.py`, `scripts/_gpt/eval_heavy_tailed_d2d.py`, `scripts/_gpt/retention_comparison_gpt.py`, `ablation_ensemble_hat_vs_iid.py` — verified pre-deletion via grep. **Deleting it would corrupt the entire zone-3A evidence chain.**

### 1C. File relocations (no deletion, organization only)

| Source | Destination | Count |
|:--|:--|--:|
| Root `BROADCAST_*.md` + `PROJECT_AUDIT_*.md` + `COMPILE_PRECHECK.md` | `report_md/_gpt/round_4_5_audit_archive/` | 15 |
| Root `append_*.py` + `fix_*.py` + `generate_*.py` | `archive/scripts/` | 24 |
| Root `_rapid_monitor.py` | `scripts/` | 1 |
| `logs/_gpt/*.log` (>5 days old) | `logs/_gpt/archive_pre_20260420/` | 200 |

### 1D. False-start corrected

I initially relocated `checkpoints/C1..C8.pt` and `R1..R6.pt` (paper baselines) to a misnamed subdir thinking they were ADC ablations. Verified via grep that they ARE referenced by `scripts/_gpt/run_c4_*.sh`, `multi_seed_train_gpt.py`, etc. **Restored to original location.**

### 1E. Documentation added

- `data/README.md` — directory purpose + reproducibility note + git policy reminder

---

## 2. DEFERRED — Git operations (user approval needed)

These are all reversible but mutate the git index, so I'm preparing commands and asking user to authorize before execution.

### 2A. P0-#1: Untrack `data/` (8206 files)

**Command:**
```bash
git rm -r --cached data/
git commit -m "chore: untrack data/ per .gitignore (preserves local files)"
```

**Effect:** Removes 8206 image files from index; preserves on disk; `.gitignore` finally takes effect.

**Risk:** Low. Reversible via `git checkout HEAD -- data/`. Affects all clones (they'll lose the tracked images on next pull).

**My recommendation:** APPROVE. Cleans up `git status` performance and respects `.gitignore`.

### 2B. P0-#2: Track post-fix code

**Command:**
```bash
git add eval_fresh_instances_postfix.py test_dual_bug_fix.py test_groupwise_nl_wrapper.py test_adc_perinstance_calibration.py debug_math_consistency.py
git commit -m "feat: add post-fix verification suite + eval scripts to version control"
```

**Effect:** Adds 5 critical post-fix files to tracked set. These are referenced in our test discipline (commit 9cdbe77 verification).

**Risk:** Verify no secrets/credentials. Spot-checked: pure code, no secrets.

**My recommendation:** APPROVE.

### 2C. Tracked-but-deleted reconciliation

`git status` shows ~150 files marked `D ...` (tracked but physically deleted, mostly old `docs/`, `generate_*.py`, etc., from prior cleanup waves). To finalize:

```bash
git add -u
git commit -m "chore: stage prior physical deletions in git index"
```

**Risk:** Medium. This commits all deletions in one go. Inspection recommended via `git status -s | head -100`.

**My recommendation:** APPROVE after user spot-checks the list.

---

## 3. NOT executed — defer to Round-7 polish

Per Kimi's "P2 — Code Hygiene (Low Risk, Can Defer to Round-7)" classification:

| Item | Why deferred |
|:--|:--|
| Update import paths after `_rapid_monitor.py` move | No active imports break |
| `data/` extended docs | README placeholder is enough for now |
| `tmp/bak_cleanup_20260425/` final disposition | Per Kimi A2 ruling: keep until Round-7 freeze |
| `.bak`, `.ORIGINAL` discipline going forward | Add to `.gitignore` later |

---

## 4. State diff

### Before
- Root dir: 173 files (cluttered)
- Root .py: ~124 (mix of canonical + scratch + monitor + generate)
- Root broadcasts: 12 files (inconsistent w/ report_md/_gpt/ pattern)
- `checkpoints/`: ~6.4 GB total (lots of stale)
- `logs/_gpt/`: 348 active logs (most >5 days old)
- `git status --porcelain`: 526 entries

### After
- Root dir: 149 files (down 14%)
- Root .py: 100 (down ~20%, only canonical + active)
- Root broadcasts: 0 (all in `report_md/_gpt/round_4_5_audit_archive/`)
- `checkpoints/`: ~5.95 GB (459 MB reclaimed; canonical preserved)
- `logs/_gpt/`: 148 active + 200 archived
- `git status --porcelain`: 595 entries (more entries because deletions/moves now visible; resolves with §2C commit)

---

## 5. Protections applied

These were explicitly NOT touched despite being old/large:

| Asset | Reason |
|:--|:--|
| `checkpoints/_ensemble/V4_*.pt` | Canonical 86.37% / 88.53% / AR(1) source — Zone 3A evidence chain |
| `checkpoints/{C,R,V}{1..8}_*.pt` | Paper baselines, referenced by 10+ scripts |
| `checkpoints/_gpt/postfix_m_series/` | M1-M6 severe-NL Stage-2 source |
| `paper/` (entire) | Manuscript canonical |
| `paper_orchestra_input/` | Submission packet |
| `release_artifacts/source_data_v1/` | Zenodo bundle |
| `report_md/_gpt/` (entire) | Coordination ledger |
| `tmp/bak_cleanup_20260425/` | Stage-1 backups (audit trail per Kimi A2) |
| `device_profiles/` | Literature-calibrated device priors |
| `outputs/remote_github_handoff_*` | Remote dispatch base |

---

## 6. Outstanding decisions for user

1. **Approve git ops in §2A (untrack data/)?** Recommended yes.
2. **Approve git ops in §2B (track post-fix code)?** Recommended yes.
3. **Approve git ops in §2C (stage prior deletions)?** Recommended yes after spot-check.
4. **Do all three as one commit, or three separate commits?** Recommend three separate (cleaner history).

I will NOT execute any git operation until user signals. Reply "git approve" + (1/2/3 or all) to fire.

---

## 7. New doctrine (for forward continuity)

- **`.bak`/`.ORIGINAL`/`.SIMULATED` files**: must live in `tmp/` not root. Add to `.gitignore` later.
- **Root broadcasts**: always under `report_md/_gpt/`, never project root.
- **Generate/append/fix scripts**: `archive/scripts/` if one-shot, `scripts/_gpt/` if reusable.
- **Stale checkpoints**: explicit naming (`_badscale`, `_suspect`, `_smoke`) → safe to delete.
- **Canonical checkpoints**: NEVER delete `_ensemble/`, `postfix_m_series/`, paper baselines without grep-first verification.
- **Logs >5 days**: archive subdir, don't delete (audit trail).
- **`__pycache__/`**: free to delete (regenerable).

---

## 8. Sprint compatibility

This cleanup does NOT interfere with Round-7 proactive sprint (`BROADCAST_ROUND7_PROACTIVE_SPRINT_20260425.md`):
- Phase 1 Kimi theory deepening — operates on `paper/latex_gpt/supplementary/` (untouched)
- Phase 2 Codex empirical analyses — operates on `checkpoints/_ensemble/` + `checkpoints/_gpt/postfix_m_series/` (BOTH PROTECTED)
- Phase 3 Kimi writing polish — operates on `paper/latex_gpt/sections/` (untouched)
- Phase 4 Kimi defense + tooling — operates on `report_md/_gpt/` (untouched)

Cleanup runs in parallel without conflicts.

---

## 9. One-line

Deep cleanup executed: 459 MB checkpoints reclaimed (canonical preserved), 200 logs archived, 24 scripts + 12 broadcasts relocated, 6 backup/cache files deleted; git operations prepared but deferred for user authorization; manuscript + canonical evidence chain untouched.
