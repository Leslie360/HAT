<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Kimi Canonical Survivors — Post Dual-Bug Scrub

**Date:** 2026-04-23
**Rule:** Only results proven unaffected by the two `analog_layers.py` bugs are listed. No speculation. No forward-looking claims.

---

## Valid Results (Safe to Cite Right Now)

| Result | Value | Why It Survives |
|:-------|:------|:----------------|
| **V4 same-instance (train best)** | 91.13% | Checkpoint metadata: `nl_ltp=1.0`, `nl_ltd=-1.0`, `use_second_order_ste=False`. NL=1 makes both bugs no-ops. |
| **V4 same-instance MC eval** | ~91.3% | Same checkpoint as above. Eval path is forward-only; backward bugs irrelevant. |
| **V4 scale-masking (V2 → standard)** | ~97.39% | Forward-only eval on valid V4 checkpoint. No backward pass. |
| **V4 retention curve** | 91.63% → 79% | Forward-only eval on valid V4 checkpoint. Measures inference-time drift, not training gradients. |
| **V4 severe-NL inference-only** | 27.72% | Forward-only eval on valid V4 checkpoint. No training involved. |
| **Digital FP32 baselines** | (various) | No analog STE code path. Completely independent of `analog_layers.py`. |

---

## Explicitly Invalidated (Do Not Cite)

| Result | Status |
|:-------|:-------|
| K4R same-instance (91.62%) | **INVALID** — trained with branch swap + extraneous `nl` multiplier |
| K4R fresh-instance (34.99%) | **INVALID** — evaluates contaminated checkpoint |
| P1-C | **STOPPED / CONTAMINATED** |
| P1-C2 | **STOPPED / CONTAMINATED** |
| All pre-Branch-A K-series (K1–K5, J1d, K2, K4 α sweep, etc.) | **INVALID** — pre-`ab56c2d`, bugs present when NL ≠ 1 or second-order active |
| Ensemble HAT (86.37±1.54%) | **INVALID** — pre-`ab56c2d`, NL=2 active, wrong signs, bugs present |
| NL-HAT retraining (27.37%, 27.72±0.82%) | **INVALID** — pre-`ab56c2d` |
| MLP-linearized (32.12%) | **INVALID** — pre-`ab56c2d` |
| All-linear (32.60±9.18%) | **INVALID** — pre-`ab56c2d` |
| OPECT transfer (88.53%) | **INVALID** — checkpoint provenance ties to pre-fix code |
| Proportional-noise HAT (97.37±0.05%) | **INVALID** — provenance unclear; hold until post-fix audit |

---

## Boundary Condition

V4 survives **only because NL=1 makes the entire STE backward path an identity**. Any claim that generalizes V4 behavior to `NL != 1` is **not supported** by valid evidence at this time.

There is currently **no valid fresh-instance result for any experiment with `NL != 1` or second-order STE active**.

---

*End of survivors list. No new experiments proposed. No theory appended.*
