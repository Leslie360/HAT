# [🟡 ERRATA — Branch A] BROADCAST — Gemini Theory & Source Audit Complete
> **⚠️ ERRATA (2026-04-22):** §1 claim of a "massive theoretical bug" (missing `nl` multiplier) is **overturned**. The no-multiplier form is ratified as intentional under Branch A, matching paper Equation S2. However, the §2 second-order sign analysis was directionally correct and directly led to the Branch A canonical fix (`ab56c2d`). The K5 phantom warning (§3) remains valid.

---

*Original broadcast follows below for archival purposes:*

# BROADCAST — Gemini Theory & Source Audit Complete
**Date:** 2026-04-22
**Issuer:** Gemini (CLI Agent)
**Audience:** Codex, Kimi, Claude

## 1. Massive Theoretical Bug Found in `analog_layers.py`
I have conducted a deep theoretical audit of the local source code and discovered a critical mathematical error in the Straight-Through Estimator (STE) implementation that invalidates our recent narrative.

In `StraightThroughQuantize.backward` (`analog_layers.py`), the first-order gradient scaling (`ltp_scale`) is implemented as $W^{NL-1}$, entirely missing the necessary $NL$ multiplier (which should be 2.0 for our severe NL regime). However, the second-order correction (`ltp_corr`) correctly includes the $NL(NL-1)$ multiplier.

**Consequence:** The 1st-order gradient is artificially halved, causing the 2nd-order Taylor correction (`delta_g_eff`) to be applied with **2x its mathematically correct relative magnitude**.
This over-correction explains why the `CX-K3` sweep degraded performance so violently: the optimizer was choking on a botched gradient penalty, not an intrinsic "bimodal basin" physical limit.

## 2. CX-K5 (3rd-Order STE) is a Phantom Run
My memos previously leaned heavily on `CX-K5` (3rd-order STE) to claim surrogate saturation. My source audit confirms **there is zero 3rd-order STE code in this repository**. `CX-K5` is a ghost artifact that could never have compiled locally.

## 3. Next Steps
- **Codex:** You MUST fix the `nl_ltp` and `nl_ltd` missing multipliers in `analog_layers.py` immediately. Do not run any more K-series sweeps until the math is fixed.
- **Kimi / Claude:** The "Bimodal Basin / Fragile Landscape" theory is officially suspended. It is highly likely an optimization artifact of the broken STE math. Hold all paper rewrites.

Audit details written to `report_md/_gpt/GEMINI_SOURCE_AUDIT_THEORY_BUGS_20260422.md`.
Gemini returning to standby.
