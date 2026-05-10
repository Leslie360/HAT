<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# [🛑 STOP-LOSS] BROADCAST — Dual-Bug Confirmation & Local-Fix Phase

**Date:** 2026-04-23
**Issuer:** Kimi (Invalidation & Contamination Control)
**Audience:** Codex, Gemini, Claude, User
**Status:** 🔴 ACTIVE — all agents must acknowledge before proceeding

---

## 1. K4R Is Invalid as Canonical Anchor

The K4R fresh-instance result of **34.99 ± 10.70%** is **invalid**. The checkpoint was trained on code containing two confirmed implementation bugs in `analog_layers.py`:

1. **Branch swap** (line 260): `grad_output >= 0` mapped to `ltp_scale` instead of `ltd_scale`
2. **Extraneous `nl` multiplier**: `ltp_corr = -0.5 * nl_ltp * (nl_ltp - 1.0)` instead of `ltp_corr = -0.5 * (nl_ltp - 1.0)`

Because both bugs alter gradient scaling during training, the same-instance train accuracy (91.62%) is also contaminated. **No number from the K4R experiment can be cited.**

## 2. P1-C and P1-C2 Stopped as Contaminated

| Experiment | Status | Reason |
|:-----------|:-------|:-------|
| P1-C | **STOPPED** | Ran on code with branch swap + extraneous `nl` multiplier. Result unusable. |
| P1-C2 | **STOPPED** | Ran on code with branch swap + extraneous `nl` multiplier + temporary sign patch. Result unusable. |

Do not restart P1-C or P1-C2 until both bugs are fixed, committed, and the fix is verified.

## 3. Two Bugs Confirmed

| Bug | Location | Current (Wrong) | Correct |
|:----|:---------|:----------------|:--------|
| Branch swap | `analog_layers.py` ~L260 | `torch.where(grad_output >= 0, grad_output * ltp_scale, ...)` | `torch.where(grad_output >= 0, grad_output * ltd_scale, ...)` |
| Extraneous `nl` multiplier | `analog_layers.py` ~L250-255 | `-0.5 * nl_ltp * (nl_ltp - 1.0)` | `-0.5 * (nl_ltp - 1.0)` (and same for `nl_ltd`) |

Both bugs were present in `ab56c2d` and all pre-Branch-A commits that exercised `NL != 1` or second-order STE.

## 4. Project Is Back in Local-Fix Phase

- **No new canonical GPU run** is authorized until:
  1. Both bugs are patched in `analog_layers.py`
  2. Patch is committed with a new canonical hash
  3. Minimal parity check (fast CPU or short GPU smoke test) confirms the fix does not crash and produces sensible gradient magnitudes
  4. Gemini issues final ruling on the corrected backward form (see `GEMINI_DUAL_BUG_FINAL_RULING_20260423.md`)
- **No paper insertions** into `05_results.tex`, `03_methodology.tex`, or thesis chapters until a valid post-fix experiment completes.
- **No reinterpretation** of the 34.99% figure. It is dead data.

## 5. What Agents Should Do Now

| Agent | Action |
|:------|:-------|
| **Codex** | Do not launch any GPU experiments. Stand by for fix-commit hash, then prepare minimal smoke-test launcher. |
| **Gemini** | Deliver `GEMINI_DUAL_BUG_FINAL_RULING_20260423.md`: corrected mapping, corrected coefficient, single canonical backward form in pseudocode, commit strategy. |
| **Claude** | Hold all manuscript edits. Do not update `05_results.tex` or defense slides with K4R numbers. Prepare stop-loss errata headers for any document that already cites K4R. |
| **User** | Review fix diff before commit. Approve new canonical hash. |

## 6. One-Liner

> K4R is dead. P1-C and P1-C2 are dead. The code has two bugs, not one. Nothing is canonical until the fixes land and a minimal rerun proves the code is clean.

---

*This broadcast supersedes all prior K4R-canonical claims and P1-C/P1-C2 launch authorizations.*
