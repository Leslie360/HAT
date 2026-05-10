# GEMINI NL MITIGATION THESIS CHAPTER — 2026-04-18

**Reread of canonical state:** Building upon `NL_LANE_RESULTS_20260418.md` and `CLAUDE_A_DECISION_FINAL_20260418.md`, the NL mitigation story is locked as a supplementary ablation in the NC paper but warrants a full, deep-dive chapter in the thesis.

## 1. Chapter Scope: The Mechanistic Story of NL=2.0 Mitigation
This chapter explores why standard hardware-aware training (HAT) collapses under severe asymmetric write non-linearity (NL=2.0, yielding 27.72%) and how targeted linear compensations reveal architectural vulnerabilities.
- **MLP Path Recovery (87.79%):** Linearizing only the MLP analog layers recovers performance to within ~4 pp of the idealized NL=1.0 upper bound. The MLP channel-mixing path is dense but structurally robust; it can absorb the gradient scaling distortions introduced by the STE backward surrogate without catastrophic geometric collapse.
- **QKV Path Collapse (18.72%):** The attention mechanism relies on softmax exponentiation, which amplifies small relative distortions in the query/key projections. Severe NL disrupts the angular geometry of these projections, leading to attention map fragmentation. Linearizing QKV alone fails to rescue the network, proving the attention path is structurally hypersensitive to asymmetric updates.
- **All-Linear Upper Bound (87.49%):** Linearizing all analog layers performs similarly to MLP-only, confirming that the MLP nonlinearity is the dominant failure site holding back the baseline recipe.

## 2. Extended Experiments (Thesis-Only)
Since the NC paper limits this to a single supplementary table, the thesis will expand the investigation:
1. **NL Severity Sweep:** Evaluate $NL \in \{1.2, 1.5, 1.7, 2.0, 2.5\}$ across the MLP-only and QKV-only lanes to plot the exact divergence point where attention geometry irrevocably shatters.
2. **MLP-Linearization Granularity:** Ablate the MLP block further—linearize `fc1` (expansion) vs. `fc2` (projection) independently to see if proximity to the GELU activation function dictates the severity of the gradient distortion.
3. **Attention-Rescue Strategies:** Since QKV must remain analog in a fully deployed array, explore algorithmic rescues such as gradient clipping, structured noise injection during the forward pass to regularize the attention maps, or lower-rank QKV projection constraints.

## 3. Tie-Back to Circuit-Aware Integration (G-J)
The NL=2.0 mitigation interacts directly with the spatial IR drop and thermal dependencies (P1/P2/P5).
- **IR Drop Interaction:** Severe spatial IR drop lowers the effective write voltage $V_{\text{eff}}(i,j)$ for cells far from the driver. This voltage drop shifts the devices into different, often more severe, regions of their nonlinear conductance update curves. A joint $\text{IR} \times \text{NL}$ sweep will evaluate if devices at the array edges suffer accelerated gradient distortions.

## 4. Estimated Cost
- **Wall-clock time:** 1.5 to 2 weeks for code modification and analysis.
- **GPU-hours:** ~100 GPU-hours for the fine-grained NL severity sweep and sub-layer ablations.
