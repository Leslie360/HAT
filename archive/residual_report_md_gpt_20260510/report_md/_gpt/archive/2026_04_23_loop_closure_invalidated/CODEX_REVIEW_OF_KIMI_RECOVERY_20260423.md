# Codex Review of Kimi Recovery Work

**Date:** 2026-04-23 17:52 CST
**Reviewer:** Codex
**Scope:** Review Kimi's 2026-04-23 recovery/control-plane documents after the dual-bug invalidation and after R1 clean rerun completion.

## Executive Verdict

Kimi's latest recovery-control work is mostly correct and should be used as the current process baseline. It correctly invalidates K4R/P1-C/P1-C2 and requires a clean `group=all`, first-order-only full rerun with `10x5` fresh-instance evaluation before any new canonical claims.

However, several older Kimi K4R/Branch-A documents remain on disk and still frame K4R as canonical or pending-canonical. Those files are now stale and must not be used for manuscript text, reviewer replies, or experiment routing.

## Accepted Kimi Outputs

| File | Review status | Reason |
|---|---:|---|
| `KIMI_RECOVERY_MASTER_STATUS_20260423.md` | ACCEPT with update needed | Correctly freezes contaminated runs and defines the next minimal rerun. Needs a new addendum because R1 has now completed. |
| `KIMI_MINIMAL_RERUN_REQUIREMENTS_20260423.md` | ACCEPT | Correct artifact gate: full training log, train JSON, and `10x5` fresh eval JSON. R1 now satisfies this gate. |
| `KIMI_DUAL_BUG_INVALIDATION_MATRIX_20260423.md` | ACCEPT | Correctly classifies K4R, P1-C, P1-C2, old K/J severe-NL runs, and stale K4R documents as invalid or historical. |
| `KIMI_CANONICAL_SURVIVORS_20260423.md` | ACCEPT, conservative | Safe citation boundary. It may be stricter than eventually necessary, but strict is appropriate until R1/R2 land cleanly. |
| `KIMI_DOC_PATCH_PRIORITY_20260423.md` | ACCEPT with wording update | Patch ordering is right. Replace "after local code fix" with "after fixed/tested working tree and clean provenance record" unless a clean commit is used. |
| `KIMI_PUBLIC_STATUS_WORDING_20260423.md` | ACCEPT with wording update | The public wording is directionally right, but "atomic fix" should not imply a clean committed release if the tree is dirty. |
| `KIMI_DISPATCH_20260423_T1_ENERGY_AUDIT.md` | ACCEPT | Correctly demotes the energy result to audit instead of treating the contradictory output as usable. |

## Superseded / Do Not Use

The following Kimi files are historical only or invalid under Kimi's own later matrix. They must not be cited as current truth:

- `KIMI_K4R_FRESH_EVAL_REPORT.md`
- `KIMI_K4R_RESULTS_CONDITIONAL_DRAFT_20260423.md`
- `KIMI_K4R_RESULT_TEMPLATE_20260423.md`
- `KIMI_K4R_COMPLETION_BROADCAST_TEMPLATE_20260423.md`
- `KIMI_K4R_INTERIM_ANALYSIS_20260423.md`
- `KIMI_K4R_LIVE_PROGRESS.md`
- `KIMI_BRANCH_A_QUICK_REFERENCE_20260423.md`
- `KIMI_PRE_SUBMISSION_CHECKLIST_20260423.md`
- `KIMI_CODEX_BROADCAST_20260423.md`
- `KIMI_INDEX_20260423.md`
- `KIMI_EXPERIMENT_QUEUE_POST_K4R_20260423.md`

Reason: these were written before final dual-bug recovery closure and still assume `ab56c2d`/K4R/Branch-A semantics as canonical or pending-canonical.

## Current Evidence After Review

### Code/Test Status

- Current git HEAD: `33bed9c`.
- Working tree is dirty, so do not describe the current state as a clean release commit.
- Kimi's claim that `test_dual_bug_fix.py` passes was verified directly: all 5 script-level tests passed.
- Codex unit test suite also passed earlier: `test_groupwise_nl_wrapper.py`, 7 tests.

### R1 Clean Anchor Status

R1 has completed and satisfies Kimi's minimal rerun gate.

| Metric | Value |
|---|---:|
| Train best same-instance test accuracy | `91.50%` |
| Best epoch | `96` |
| Final test accuracy | `90.72%` |
| Fresh protocol | `10 instances x 5 eval runs` |
| Fresh mean | `34.5612%` |
| Fresh std | `8.7878%` |
| Fresh min instance mean | `22.986%` |
| Fresh max instance mean | `49.614%` |

Artifacts:

- Train log: `logs/_gpt/r1_clean_anchor_train_20260423_131610.log`
- Train JSON: `report_md/_gpt/json_gpt/r1_clean_anchor_train.json`
- Fresh JSON: `report_md/_gpt/json_gpt/r1_clean_anchor_fresh_eval.json`
- Checkpoint: `checkpoints/_gpt/r1_clean_anchor/V4_hybrid_standard_noise_hat_r1_clean_anchor_first_order_best.pt`

Interpretation: R1 is a valid clean first-order anchor candidate, not yet a manuscript result. It shows strong source recovery but weak cross-instance transfer relative to the old invalid 86% narrative and relative to remote domain-randomization directions.

### Broadcast Drift That Must Be Corrected

- `AGENT_SYNC_gpt.md` contains a 14:10 block stating T1 complete with `~2.86x` and T2 failed. Local evidence conflicts with this: T1 raw output from `run_energy_sensitivity.py` remains contradictory and needs audit; T2 has a completed AIHWKIT shared-regime JSON.
- T2 current JSON reports digital subset `95.55%`, AIHWKIT analog mean `90.43 +- 0.51%`, delta `-5.12 pp`, CPU-only subset benchmark.
- Any document claiming T1 is settled should be blocked until `KIMI_T1_ENERGY_AUDIT_20260423.md` exists and is reviewed.

## Required Next Actions For Kimi

1. Create an R1 landing review: accept/reject R1 as the first clean anchor candidate using Kimi's own minimal rerun requirements.
2. Add superseded headers or a deprecation index for the stale K4R files listed above.
3. Resolve the T1 energy contradiction before any energy/speedup number is reused.
4. Update public wording to avoid claiming a clean atomic release while the worktree remains dirty.
5. Keep paper/thesis insertion frozen until R1 is reviewed and R2/SO2 comparison is either run or explicitly deferred.

## Codex Position

Kimi's latest recovery logic is usable. The main risk is not Kimi's reasoning; it is stale-document contamination from Kimi's older K4R packet and broadcast drift in shared ledgers. The safe route is to treat Kimi's 12:08-12:25 recovery documents as the active policy, treat earlier K4R documents as historical, and route all new claims through R1/R2 post-fix artifacts.
