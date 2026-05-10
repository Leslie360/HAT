# DS Phase P6 Hostile Experiment Audit

**Date:** 2026-05-09
**Auditor:** DS (per Codex Superphase P6 dispatch)
**Subject:** Kimi Phase P6 — Tracks A-H hostile audit

---

## Verdict: CONDITIONAL PASS ⚠️

No scientific fraud, no Paper-1 contamination, no overclaiming. **But**: 6-bit manuscript values are stale after seed123 rerun. Minor non-blocking finding.

---

## Track-by-Track Audit

### Track A — Evidence Gap Ledger — ✅ PASS

| Check | Result |
|-------|--------|
| 9 claims mapped | ✅ All covered (1-9) |
| Gap identification | ✅ 3 gaps: 6-bit seed123, 105 seed789, 107 corrected-noise |
| Status labels honest | ✅ "Complete" / "Weak" / "Missing" correctly applied |
| Classifications correct | ✅ paper1-main-locked / supplement-candidate / work2-kv-cache / future-only |

**Note**: Track A was written BEFORE seed123 rerun completed. The ledger correctly notes "rerun in progress" for claim 5. Does not affect final verdict.

### Track B — 6-bit seed123 Gap Closure — ✅ PASS (independently verified)

| Check | My Verification | Result |
|-------|-----------------|--------|
| Rerun completed | training_history.json: best=68.51% | ✅ |
| Fresh eval | fresh_eval.json: mean=68.49%, 10×5 MC, enable_during_test=true | ✅ |
| Drift eval | drift_eval.json: 0s=68.44, 1h=68.53, 1d=68.58 | ✅ |
| training_history.json saved | Present (3746s total) | ✅ |
| CSV updated | n_source_best→4, fresh_mean→68.44, drift_drop→0.04pp | ✅ |
| PCM guard | **ALL 22 CHECKS PASS** (verified by running script) | ✅ |
| Artifacts copied to canonical_json | drift_eval.json, fresh_eval.json, training_history.json present | ✅ |

### Track C — Local GPU Queue — ✅ PASS

| Check | Result |
|-------|--------|
| GPU status | ✅ Idle before launch (346 MiB / 16GB) |
| Safety | ✅ Sequential, early stop configured (patience=10), kill criteria documented |
| Logging | ✅ Log tee'd to `logs/_gpt/p6_6bit_seed123_source_rerun_20260509.log` |
| Post-run steps | ✅ Fresh eval → drift eval → canonical copy → PCM guard |
| Skipped jobs justified | ✅ Existing evals current; no safe thesis script found; Work-2 remote-blocked |

### Track D — Statistical Completion Pack — ✅ PASS

| Check | Result |
|-------|--------|
| SEM and 95% CI | ✅ Computed for all key values |
| Cohen's d | ✅ Effect sizes: 374 (4-bit collapse vs HAT), 32 (PCM4 vs HAT), 7.2 (4-bit drift), 1.9 (8-bit vs 6-bit) |
| Robustness matrix | ✅ Strong / Moderate / Underpowered correctly labeled |
| Soften recommendations | ✅ 6-bit variance, 105 seed789 gap, 107 corrected-noise — all correctly flagged |
| Defense Q&A | ✅ Honest: "3 seeds enough? Yes for low-variance, marginal for 6-bit but that's the point" |

### Track E — Remote 105 Closure — ✅ PASS

| Check | Result |
|-------|--------|
| Seed789 acquired | ✅ 3/3 seeds complete for DeiT and ViT |
| Proportional vs digital | DeiT: +1.77pp (3/3 seeds) ✅ |
| Outlier documented | ViT seed456 digital+5.75pt — protocol audit confirms no violation ✅ |
| Classification | DeiT→paper1-supplement-candidate, ViT→defense-support ✅ |

### Track F — Remote 107 Closure — ✅ PASS

| Check | Result |
|-------|--------|
| Task list exists | ✅ Self-contained with kill criteria |
| Corrected-noise data ingested | ✅ P0B/K107-A/B/C/EPSC/scale complete |
| Canonical baseline locked | ✅ 22.18 PPL (old 15.68 deprecated) |
| Selective-layer route | ✅ last1 viable (19.45 PPL), all-layer abandoned (37.13) |
| Classification | ✅ Work-2 only. No Paper-1 contamination. |

### Track G — Repo Hygiene — ✅ PASS

| Check | Result |
|-------|--------|
| .kimi_draft* deletions | ✅ 37 files deleted. **0 remaining** (independently verified) |
| .gitignore proposal | ✅ Covers .claude/, tarballs, temp files, logs |
| Commit sequence | ✅ 4-phase conservative plan, no push without approval |
| No destructive actions | ✅ Verified |

### Track H — Final Experiment Completeness — ✅ PASS

| Check | Result |
|-------|--------|
| Submission-ready | ✅ YES — correctly assessed |
| Scientific defense | ✅ YES — with moderate/high-risk positions labeled |
| Future/Work-2 | ✅ Mostly yes — data acquired |
| What's worth doing | ✅ Prioritized list (DS audit → repo commit → supplement drafting) |
| What's not worth doing | ✅ 5-bit, all-layer KV, extra seeds — all correctly killed |
| No overclaiming | ✅ "High variance is the story, not a bug" is defensible |

---

## ⚠️ Finding: Stale 6-bit Values in Manuscript After seed123 Rerun

The seed123 rerun completed successfully (best=68.51%, fresh=68.49%), and the CSV was updated. However, the .tex files still reference **pre-rerun** 6-bit values:

| Location | Current (stale) | Should be (from CSV) | Impact |
|----------|----------------|---------------------|--------|
| `05_results.tex:61` | 68.55% / 0.07~pp | 68.44% / 0.04~pp | Negligible — both "drift-flat" |
| `05_results.tex:82` | 68.55% | 68.44% | Negligible |
| `00_abstract.tex:3` | 68.55% | 68.44% | Negligible — text says `<0.1~pp` which covers both |
| `07_conclusion.tex:7` | 68.55% | 68.44% | Negligible |
| `supplementary.tex (caption)` | "Four-seed fresh mean: 68.55%" / "drift drop of 0.07~pp" | 68.44% / 0.04~pp | Minor — caption stale |
| `supplementary.tex (seed123 row)` | `\notrun{}` / fresh=68.93% / drift_drop=-0.05pp | best=68.51% / fresh=68.49% / drift 1d=68.58% / Δ=+0.14pp | **Moderate** — seed123 row shows "not run" and uses interrupted-run values |

**Severity: LOW** — All stale values tell the same story (6-bit = lowest mean, high variance, drift-flat). No claim inflation, no narrative change. But the supplementary seed123 row is factually incorrect (shows `\notrun{}` and uses the interrupted-run fresh=68.93% which differs from the completed rerun 68.49%).

**Recommendation**: Update the stale .tex values in a batch cleanup before the next PDF rebuild.

---

## Summary

| Track | Verdict |
|-------|---------|
| A — Evidence gap ledger | ✅ PASS |
| B — 6-bit seed123 gap closure | ✅ PASS (gap closed, PCM guard verified) |
| C — Local GPU queue | ✅ PASS |
| D — Statistical completion | ✅ PASS |
| E — Remote 105 closure | ✅ PASS |
| F — Remote 107 closure | ✅ PASS |
| G — Repo hygiene | ✅ PASS (37 draft files deleted) |
| H — Completeness verdict | ✅ PASS (no overclaiming) |

**Overall**: CONDITIONAL PASS. No scientific drift, no Paper-1 contamination, no claim inflation. The 6-bit seed123 gap is closed. One minor finding: supplementary seed123 row needs updating from interrupted-run values to completed-rerun values.

Ready for Mimo audit and Codex final acceptance.

---

*Report by DS. Independent verification performed 2026-05-09 against CSV, PCM guard output, canonical JSON artifacts, file system, and grep scans.*
