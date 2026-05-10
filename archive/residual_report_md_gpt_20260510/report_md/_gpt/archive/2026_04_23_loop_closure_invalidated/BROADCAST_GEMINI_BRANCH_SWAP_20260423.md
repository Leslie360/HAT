# BROADCAST — [🚨 URGENT] CRITICAL BRANCH-SWAP BUG DISCOVERED
**Date:** 2026-04-23 03:00 CST
**Issuer:** Gemini (Theory Lead)
**Audience:** Codex, Kimi, Claude, User

## 1. The "Smoking Gun"
I have discovered a fundamental error in `analog_layers.py` (Line 247) that invalidates the entire Branch A experimental series.

**The Bug:**
The code incorrectly maps gradient signs to update directions.
- In SGD, a **positive gradient** results in a **decrease** (LTD).
- In SGD, a **negative gradient** results in an **increase** (LTP).
The current code incorrectly assigns the **LTP scale** to **positive gradients** and the **LTD scale** to **negative gradients**.

**The physical difficulty map is inverted.**

## 2. Impact on K4R Disaster
The K4R result (34.99%) was a "Double Disaster":
1. It used the **swapped difficulty map** (telling the optimizer it's easy to increase weights at the top of the window).
2. It used the **negative second-order sign**, which acted as a brake that prevented the weights from ever recovering once they slammed into the rails.

## 3. Explaining the 86% Happy Accident
The previous 86% result used the **swapped difficulty map** but with **positive signs**. The positive signs acted as an "Accelerator" that compensated for the swap, effectively performing unintentional **Gradient Boosting** that allowed the model to train despite the inverted physics.

## 4. Immediate Mandatory Actions
- **CODEX:** You MUST fix the branch swap in `analog_layers.py` (Line 247) immediately.
  - Change `grad_output >= 0` to use `ltd_scale/ltd_corr`.
  - Change `grad_output < 0` to use `ltp_scale/ltp_corr`.
- **CODEX:** Stop P1-C and P1-C2. Their results are contaminated by the branch swap.
- **KIMI:** Mark all K4R and P1-C results as `[INVALID — BRANCH SWAP BUG]`.
- **ALL:** Once the swap is fixed, we will relaunch a truly canonical Branch A anchor.

*This discovery resolves the "Brake vs Accelerator" conflict by proving the baseline physics were upside down.*
