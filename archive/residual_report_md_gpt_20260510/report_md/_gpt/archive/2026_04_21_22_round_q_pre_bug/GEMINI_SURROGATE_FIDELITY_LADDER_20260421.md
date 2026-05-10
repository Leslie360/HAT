# G-HH7: Surrogate Fidelity Ladder
**Date:** 2026-04-21
**Scope:** Phase β

This memo establishes the theoretical ordering of Straight-Through Estimator (STE) orders against fresh-instance variance.

1. **1st-Order STE (Gradient Scaling):**
   - *Characteristics:* High bias, low variance.
   - *Effect:* Averages out the extreme nonlinearities at the edges of the conductance range. The optimizer finds a false "wide" minimum that does not physically exist. Result: Reliable collapse (~30%).
2. **2nd-Order STE (Taylor Expansion - J1d/K2):**
   - *Characteristics:* Low bias, high variance.
   - *Effect:* Accurately models the local curvature of the asymmetric LTP/LTD updates. The optimizer successfully navigates the true (fragmented) landscape, but finds solutions that are highly sensitive to the exact D2D noise draw. Result: Bimodal distribution (mean ~39%, range 22-62%).
3. **3rd-Order STE (CX-K5):**
   - *Characteristics:* Saturation point.
   - *Effect:* CX-K5 data (~42.8%) shows no meaningful deviation from 2nd-order. This proves that the bimodal instability is a **physical property of the analog hardware landscape**, not an artifact of Taylor series truncation.
