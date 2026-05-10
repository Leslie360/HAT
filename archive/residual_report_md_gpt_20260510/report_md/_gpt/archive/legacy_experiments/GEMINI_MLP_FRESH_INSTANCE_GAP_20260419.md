# GEMINI MLP FRESH-INSTANCE GAP ANALYSIS — 2026-04-19

**Reread of canonical state:**
I have re-read `NL_LANE_RESULTS_20260418.md` and synthesized it with the `GEMINI_CONTEXT_REREAD_20260418_v2.md` observations regarding the fresh-instance transfer gap in MLP-linearized models.

## 1. Quantitative Performance: Source-Domain vs. Fresh-Instance

The following table summarizes the test accuracy for Tiny-ViT V4 under severe write nonlinearity (NL=2.0) across the four ablation lanes.

| Lane | Source-Domain (Best %) | Fresh-Instance Mean (%) | Transfer Gap (pp) | Status |
|:---|:---:|:---:|:---:|:---:|
| **MLP-only Linear** | **87.79** | **32.12 ± 7.72** | **-55.67** | Strong Source Rescue, Transfer Failure |
| **QKV-only Linear** | 18.72 | 10.01 ± 0.10 | -8.71 | Structural Collapse |
| **All-linear** | 87.49 | [Pending] | N/A | Expected ~MLP-only |
| **Severe NL Baseline** | 27.72 | 10.00 | -17.72 | Baseline Collapse |
| *Ref: Ensemble HAT* | *91.13 (V4)* | *86.33 ± 1.61* | *-4.80* | Robust Baseline (Ideal NL=1.0) |

## 2. Mechanistic Hypothesis: Why MLP-Linear is Fresh-Instance Fragile

The catastrophic -55.67 pp gap for the MLP-only lane indicates that the linearized weights are **overfitting to the specific D2D mismatch map** used during training.

**The Interaction Mechanism:**
1. **NL-Aware Training (Standard HAT):** In a severe NL=2.0 regime, the gradient is scaled by $\propto |G|^{NL-1}$. This introduces a static, nonlinear transformation of the update step.
2. **Linearization as "Zero-Masking" the Distortion:** By linearizing the MLP path, we effectively remove this gradient distortion for that specific layer group.
3. **D2D Map Entanglement:** Standard HAT (fixed D2D) allows the network to learn a weight distribution that specifically cancels out the spatial variation of the hardware instance.
4. **The Collision:** When nonlinearity is removed *without* activating Ensemble HAT (D2D resampling), the network exploits the high-precision linear updates to fit the D2D map even more aggressively than it would under the "noisy" nonlinear updates. The linearized layers act as a high-capacity sink for hardware-specific overfitting.

In short: **Linearization restores the gradient's SNR, which standard HAT uses to fit the noise, not the data.**

## 3. Disclosing the Option-B Boundary

To maintain the integrity of the Option B decision (keeping NL mitigation as a supplementary ablation) while being transparent, the following phrasing is recommended for Section 6/Cover Letter:

> "While targeted linearization of the MLP analog path successfully restores source-domain performance under severe write nonlinearity (+60 pp improvement), this recovery is largely contingent on the specific hardware instance encountered during training. The resulting fresh-instance transfer accuracy (32.1%) remains significantly below the Ensemble HAT baseline (86.4%), suggesting that software-side linear compensation does not natively confer the same mismatch-invariance as stochastic hardware-aware training. This reinforces our decision to treat NL mitigation as a mechanistic diagnostic tool rather than a standalone architectural contribution."

## 4. Recommended Next Experiment (Thesis-Only): MLP-Linear + Ensemble HAT

**Goal:** Determine if the fresh-instance gap can be closed by combining algorithmic linearization with multi-instance training.

**Protocol:**
- **Lane:** `MLP-only` + `Ensemble HAT`.
- **Config:** Standard Ensemble HAT (resample mismatch map every epoch) but with the MLP-linearization hook active.
- **Hypothesis:** This combination will raise the fresh-instance mean to **>80%**. By forcing the network to generalize across hardware instances (Ensemble HAT) while providing clean gradients in the most sensitive dense layers (MLP linearization), we should achieve the "best of both worlds" — high accuracy that is also hardware-portable.
- **Metric:** Evaluate transferability to 10 fresh D2D instances.
- **Importance:** This transition moves the thesis narrative from "Identifying a bottleneck" (NC Paper) to "Solving for hardware-agnostic deployment" (Thesis).
