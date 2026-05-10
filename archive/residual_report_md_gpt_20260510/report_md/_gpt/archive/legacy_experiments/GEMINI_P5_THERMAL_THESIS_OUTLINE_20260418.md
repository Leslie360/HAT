# GEMINI P5 THESIS CHAPTER OUTLINE: TEMPERATURE DEPENDENCE

**Reread of canonical state:** This design relies on the state summarized in `GEMINI_CONTEXT_REREAD_20260418.md` and the future-work gap P5 identified in the Claude paper review.

## 1. Background & Motivation
Organic optoelectronic devices rely on hopping transport and exciton dissociation mechanisms that are fundamentally driven by thermal activation. Unlike traditional Si CMOS, where temperature variations induce relatively modest mobility drifts, organic arrays exhibit exponential or strong power-law temperature dependencies in their carrier mobilities, dark currents, and photoresponses \citep{[TBD_Organic_Thermal_Transport], [TBD_OPECT_Temp_Sensitivity]}. Addressing this thermal sensitivity (P5) is critical for edge-vision applications where environmental conditions fluctuate. This chapter models the temperature coefficients of $\gamma_{\text{phys}}$, $I_{\text{dark}}$, and $\sigma_{\text{D2D}}$ to evaluate the thermal robustness of the proposed framework.

## 2. Profile-Interface Extension
The framework's JSON device profile schema will be extended to explicitly support thermal states.
- **New Parameter:** `"T_op"` (Operating Temperature in Kelvin, default `300`).
- **Coefficient Table:**
  - `"T_coeff_gamma": -0.005` (e.g., $\gamma$ drifts by $-0.005$ per K)
  - `"E_activation_Idark": 0.3` (Activation energy in eV for Arrhenius $I_{\text{dark}}$ scaling)
  - `"T_coeff_sigma_D2D": 0.001` (Thermal noise inflation)

**Backward Compatibility:** If `"T_op"` is omitted or set to $300\text{K}$, the thermal modifiers evaluate to $1.0$, flawlessly reproducing the canonical NC paper results.

## 3. Worked-Example Experiment
**Setup:** Evaluate the Tiny-ViT V4 (CIFAR-10) Ensemble HAT checkpoint across a temperature sweep: $T \in \{250\text{K}, 275\text{K}, 300\text{K}, 325\text{K}, 350\text{K}\}$.
**Expected Observations:**
- At $300\text{K}$: Recovers the canonical $\sim 86.4\%$ accuracy.
- At $350\text{K}$ (Hot Edge): $I_{\text{dark}}$ increases exponentially, drastically reducing the dynamic range and inflating shot noise variance. $\sigma_{\text{D2D}}$ also increases. Expected accuracy collapse to $< 50\%$ unless specific thermal-aware training (TAT) is employed.
- At $250\text{K}$ (Cold Edge): $I_{\text{dark}}$ drops, but $\gamma_{\text{phys}}$ may shift further from the ideal $1.0$, creating a mismatch with the $300\text{K}$-calibrated inverse-gamma frontend. Expected accuracy degradation to $\sim 75\%$.

## 4. Cross-Link to P1/P2 (IR Drop)
Thermal effects do not operate in isolation. The interconnect wire resistance $R_w$ (modeled in P1) has a positive temperature coefficient (PTC). As $T$ increases, $R_w$ increases, simultaneously worsening the spatial IR drop. This chapter will explicitly note that the thermal pass updates $R_w(T)$, tightly coupling the P5 and P1/P2 evaluations in the simulator.

## 5. Cost
- **Implementation (Wall-clock):** 1-2 days (straightforward scalar modulations).
- **Execution (GPU-hours):** ~15 GPU-hours (pure inference sweeps across $T$ using existing V4 checkpoints).
