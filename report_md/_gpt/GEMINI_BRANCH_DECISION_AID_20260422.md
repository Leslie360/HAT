# G-DR8: One-Page Branch Decision Aid
**Date:** 2026-04-22

This decision aid is for local use after `[K3-0p25 pending]` lands.

## if `0.25` lifts above K2 (> 42%)
- **scientific interpretation:** High drift acts as effective mean-field annealing, escaping collapse basins.
- **what not to claim:** Do not claim the issue is "solved", as variance remains high.
- **best next experiment:** K4 (Alpha sweep) to test annealing + weaker 2nd-order.
- **whether paper-2 route changes:** Shifts slightly to focus on annealing escape paths.

## if `0.25` roughly matches K2 (~38%)
- **scientific interpretation:** Drift is irrelevant to the landscape shattering.
- **what not to claim:** Do not claim drift is an effective mitigation or major danger.
- **best next experiment:** K5 (3rd order sanity check).
- **whether paper-2 route changes:** Route remains Stochastic Basin (focus on intrinsic limits).

## if `0.25` is worse than K2 (< 35%)
- **scientific interpretation:** Drift actively destroys fragile minima found by 2nd-order STE. The landscape is incredibly brittle.
- **what not to claim:** Do not claim mean-field theory applies. Do not claim 2nd-order STE finds robust solutions.
- **best next experiment:** Stop K-series. Brittleness is proven.
- **whether paper-2 route changes:** Route becomes Structural Limit Reinforced (extreme sensitivity to physical perturbations).
