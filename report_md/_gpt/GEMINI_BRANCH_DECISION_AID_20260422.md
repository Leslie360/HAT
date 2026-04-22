# G-DR8: One-Page Branch Decision Aid (Post K3-0.25)
**Date:** 2026-04-22

This sheet directs Kimi/Codex on how to interpret the final `CX-K3 delta_g_eff=0.25` data point once it lands.

## Scenario 1: `0.25` Lifts Above K2 (> 42%)
- **Scientific Interpretation:** High drift acts as an effective mean-field annealing mechanism, helping the optimizer escape the worst collapse basins during 2nd-order STE training.
- **What not to claim:** Do not claim it "solves" the issue, as variance will still be bimodal.
- **Best Next Exp:** K4 (Alpha sweep) to see if annealing + weaker 2nd-order is optimal.
- **Paper-2 Route:** Stochastic Basin (focus on annealing escape paths).

## Scenario 2: `0.25` Roughly Matches K2 (~38%)
- **Scientific Interpretation:** Drift is irrelevant to the structural landscape shattering. The bimodal basins are too deep for mean-field drift to bridge.
- **What not to claim:** Do not claim drift is an effective mitigation or a major danger.
- **Best Next Exp:** K5 (3rd order sanity check).
- **Paper-2 Route:** Stochastic Basin (focus on intrinsic topological limits).

## Scenario 3: `0.25` is Worse Than K2 (< 35%)  [CURRENT TREND]
- **Scientific Interpretation:** Drift actively destroys the fragile minima found by the 2nd-order STE. The landscape is incredibly brittle, and the "survival" basins found in K2 are extremely narrow.
- **What not to claim:** Do not claim mean-field theory applies here. Do not claim 2nd-order STE finds robust solutions.
- **Best Next Exp:** Stop K-series. The brittleness is proven.
- **Paper-2 Route:** Structural Limit Reinforced (focus on extreme sensitivity to physical perturbations).
