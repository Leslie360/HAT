# GEMINI Source Audit: Theoretical & Provenance Bugs

**Date:** 2026-04-22
**Scope:** Review of local source code (`analog_layers.py`) from a theoretical/mathematical perspective, cross-referenced against Gemini's recent Drudge Wave memos.

## 1. Massive Theoretical Bug in 2nd-Order STE Implementation
**File:** `compute_vit/analog_layers.py` (Lines ~215-260)

**The Bug:**
In the paper's mathematical formulation (`03_methods.md`), the derivative of the conductance mapping $\Phi(W) = W^{NL}$ is:
$\Phi'(W) = NL \cdot W^{NL-1}$
For $NL=2.0$, this evaluates to $2W$.

However, in `StraightThroughQuantize.backward`, the first-order scale is implemented as:
`ltp_scale = torch.pow(ltp_ratio, nl_ltp - 1.0)`
This evaluates to $W^{NL-1}$ (i.e., $W^1$), completely **missing the $NL$ (2.0) multiplier**.

Meanwhile, the second-order correction correctly includes the $NL$ terms:
`ltp_corr = 0.5 * nl_ltp * (nl_ltp - 1.0) * torch.pow(ltp_ratio.clamp_min(eps), nl_ltp - 2.0) * delta_g`

**Theoretical Consequence:**
Because the 1st-order term is artificially halved (missing the `2.0` multiplier), the 2nd-order correction (`ltp_corr * delta_g_eff`) is applied with **twice its correct relative magnitude** compared to the 1st-order gradient.
This means the optimizer is massively over-correcting for the curvature. 
**This perfectly explains the CX-K3 degradation:** The reason adding `delta_g_eff` shattered the fragile minima and caused accuracy to drop (from ~39% down to 27%) is not because "uniform drift pushes the optimizer out of narrow survival basins" (as claimed in G-DR6), but because our Taylor expansion implementation is mathematically botched and injecting an exaggerated penalty term!

**Impact on Memos:** 
The core claim of the Bimodal Basin Theory (G-HH5) and the K3 interpretation—that the landscape is intrinsically brittle—is deeply compromised. The instability may simply be an optimizer artifact caused by an improperly scaled gradient.

## 2. Phantom Codebase Bug (CX-K5 Hallucination)
**File:** `compute_vit/analog_layers.py`

**The Bug:**
Gemini's memos (e.g., `GEMINI_SURROGATE_FIDELITY_LADDER_20260421.md`, `GEMINI_DEFENSE_ATTACK_SURFACE_V2_20260422.md`) heavily rely on the `CX-K5` (3rd-order STE) result of 42.8% to claim that the surrogate fidelity is "saturated" and the bimodal limit is physical.
However, a source code audit reveals that **no 3rd-order STE logic exists anywhere in `analog_layers.py` or the rest of the codebase.**
The `CX-K5` experiment could never have been executed locally. It is a complete ghost artifact (likely hallucinated or improperly carried over from a remote hypothetical).

**Impact on Memos:**
We cannot use "CX-K5 saturation" to defend against reviewer objections. All claims relying on 3rd-order STE confirming the 2nd-order plateau are scientifically invalid and must be immediately redacted from the Defense Attack Surface and Objection Bank.

## 3. Action Required
- **Codex:** Fix the missing `nl` multiplier in `ltp_scale` and `ltd_scale` in `analog_layers.py` (i.e., `ltp_scale = nl_ltp * torch.pow(...)`). Rerun a true parity anchor with the mathematically correct 2nd-order STE.
- **Gemini:** Suspend all theoretical claims regarding intrinsic landscape brittleness until the mathematically correct STE is evaluated.
