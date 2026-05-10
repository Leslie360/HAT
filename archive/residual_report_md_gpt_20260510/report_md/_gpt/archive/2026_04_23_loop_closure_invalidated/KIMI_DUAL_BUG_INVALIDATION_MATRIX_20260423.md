<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Kimi Dual-Bug Invalidation Matrix

**Date:** 2026-04-23
**Bugs confirmed:**
1. **Branch swap** (`analog_layers.py` line 260): `grad_output >= 0` mapped to `ltp_scale` instead of `ltd_scale`
2. **Extraneous `nl` multiplier** (`analog_layers.py`): `ltp_corr = -0.5 * nl_ltp * (nl_ltp - 1.0)` should be `ltp_corr = -0.5 * (nl_ltp - 1.0)`

**Scope:** Any result or document that assumes `ab56c2d` (Branch A) or pre-Branch-A code with `NL != 1` or second-order STE active is potentially contaminated.

---

## Classification Key

| Label | Meaning |
|:------|:--------|
| `invalid immediately` | Must not be cited as current truth. Underlying numbers or canonical claims are false due to the bugs. |
| `historical only` | Documents a decision or discovery step; factually records what was believed at the time, but the conclusions drawn are now known to be based on buggy code. |
| `still valid` | Unaffected by the two bugs. Safe to cite right now. |

---

## Required Audit Items

| Document / Result | Classification | Rationale |
|:------------------|:---------------|:----------|
| `BROADCAST_BRANCH_A_SCRUB_COMPLETE_20260423.md` | **historical only** | Records the Branch A ratification and K4R launch accurately as-of 2026-04-23 00:05, but the entire experimental chain (K4R, P1-C, P1-C2) was running on code with the branch-swap bug and the extraneous `nl` multiplier. The "scrub complete" claim is superseded. |
| `BROADCAST_K4R_DISASTER_COLLECTIVE_DECISION_20260423.md` | **historical only** | Documents the 34.99% fresh-instance observation and the collective decision to launch P1-C/P1-C2. The 34.99% figure is now known to be **invalid** (contaminated by both bugs), and the four hypotheses it framed are moot because the root cause was implementation error, not physics. Retain as timeline record only. |
| `BROADCAST_KIMI_BRANCH_SWAP_VERIFIED_20260423.md` | **historical only** | Factually records the verification of Bug 1. The bug claim itself is true, but the broadcast's call for "collective assessment before stopping experiments" is superseded — P1-C/P1-C2 are now stopped. |
| `KIMI_BRANCH_A_QUICK_REFERENCE_20260423.md` | **invalid immediately** | Contains active canonical claims that are false: (a) K4R listed as "🔄 Running / first canonical experiment", (b) second-order formula cites `NL * (NL-1)` (Bug 2), (c) thresholds table assumes K4R validity. Must not be used as reference until rewritten post-fix. |
| `KIMI_PRE_SUBMISSION_CHECKLIST_20260423.md` | **invalid immediately** | Assumes `ab56c2d` is canonical and lists K4R as the fresh-instance baseline to insert into `05_results.tex`. The checklist item `second-order -0.5 * nl * (nl-1)` encodes Bug 2. All paper-insertion actions are blocked until fixes land and a valid rerun completes. |
| `KIMI_K4R_RESULT_TEMPLATE_20260423.md` | **invalid immediately** | Template frames K4R as the "first canonical Branch A experiment" and provides comparison against pre-Branch-A baseline. The underlying K4R numbers are invalid. Do not fill or use. |
| `KIMI_K4R_RESULTS_CONDITIONAL_DRAFT_20260423.md` | **invalid immediately** | All three conditional drafts (A/B/C) assume K4R is a valid canonical result from `ab56c2d`. Since K4R is invalid, none of the paragraphs can be pasted into `05_results.tex`. |
| K4R train result (91.62% same-instance) | **invalid immediately** | Produced by training on `ab56c2d`, which contains both bugs. Same-instance accuracy is also contaminated because the optimizer followed wrong gradient scaling throughout training. |
| K4R fresh eval (34.99%) | **invalid immediately** | Evaluates a checkpoint trained with both bugs. The 34.99% figure cannot be attributed to "second-order brake too aggressive" because the branch swap alone could produce catastrophic transfer failure. |
| V4 provenance (`KIMI_V4_PROVENANCE_CONFIRMED_20260423.md`) | **still valid** | V4 checkpoint trained with `nl_ltp=1.0`, `nl_ltd=-1.0`, `use_second_order_ste=False`. Bug 1 (branch swap) is a no-op because both LTP and LTD scales equal 1.0 when `NL=1`. Bug 2 (extraneous `nl` multiplier) is a no-op because second-order was inactive, and even if active, `nl=1` makes `nl*(nl-1) = 0` identical to `(nl-1) = 0`. |
| All pre-Branch-A K-series (K1–K5, J1d, K2 N=30, K4 α sweep, etc.) | **invalid immediately** | All used `analog_layers.py` with `NL != 1` and/or second-order STE active. Both bugs were present in the pre-Branch-A codebase. The pre-Branch-A results were already marked invalid for wrong signs; the dual-bug discovery removes any residual ambiguity — they are unequivocally invalid. |
| P1-C (`group=all`, no SO2) | **invalid immediately** | Running on code with branch swap and extraneous `nl` multiplier. Stopped as contaminated. |
| P1-C2 (`group=all`, +0.5 signs) | **invalid immediately** | Running on code with branch swap, extraneous `nl` multiplier, and a temporary sign patch. Stopped as contaminated. |
| Ensemble HAT 86.37±1.54% | **invalid immediately** | Pre-`ab56c2d`, trained with `NL=2` active, wrong signs, and both bugs. Already invalidated; dual-bug finding confirms no rehabilitation path. |
| NL-HAT retraining (27.37%, 27.72±0.82%) | **invalid immediately** | Same reasoning as Ensemble HAT. |
| MLP-linearized (32.12%) | **invalid immediately** | Pre-`ab56c2d`, code contained both bugs. |
| All-linear (32.60±9.18%) | **invalid immediately** | Pre-`ab56c2d`, code contained both bugs. |
| OPECT transfer (88.53%) | **invalid immediately** | Checkpoint provenance ties it to pre-`ab56c2d` training. Cannot be cited until re-evaluated on a post-fix checkpoint. |
| Proportional-noise HAT (97.37±0.05%) | **invalid immediately** | Checkpoint provenance unclear; pre-`ab56c2d` origin suspected. Hold until provenance audit on post-fix code. |
| Digital FP32 baselines | **still valid** | No analog STE path; completely unaffected by `analog_layers.py` bugs. |
| V4 scale-masking (~97.4%) | **still valid** | Forward-only evaluation path; no backward pass. NL=1 default also makes any residual backward path a no-op. |
| V4 retention curve (91.6% → 79%) | **still valid** | Forward-only eval of a valid V4 checkpoint. |
| V4 severe-NL inference-only (27.72%) | **still valid** | Forward-only eval of a valid V4 checkpoint. |

---

## Cross-Reference: Documents Already Marked Historical by Prior Broadcasts

The following were tagged `[INVALID — pre-ab56c2d]` or `🚨 OVERTURNED` in `BROADCAST_BRANCH_A_SCRUB_COMPLETE_20260423.md`. They remain `historical only` / `invalid immediately` under the dual-bug ruling:

- `BROADCAST_ARBITRATION_STE_SEMANTICS_20260422.md`
- `BROADCAST_KIMI_STATUS_20260422.md` (§3 overturned)
- `CODEX_STE_MULTIPLIER_FIX_20260422.md` (rescinded)
- `CODEX_ROUTE_DECISION_20260422.md` (errata)
- All `cx_k4_*.md` and `cx_parity_*.md` pre-Branch-A experiment memos

---

## Summary Count

| Classification | Count (audited items) |
|:---------------|:----------------------|
| invalid immediately | 16 |
| historical only | 5 |
| still valid | 6 |

*End of matrix.*
