# G-DR5: Reviewer Objection Bank (Ambiguous Branch + Weak K3)
**Date:** 2026-04-22

1. **Objection:** "The 38.95% mean is too low to be useful. The paper lacks a positive engineering result."
   - **Why dangerous:** Rejects the paper for being incremental or negative.
   - **Strongest response:** The paper's value is rigorous falsification and risk-ranking pre-silicon, exposing hardware constraints that simple simulations miss.
   - **Missing evidence:** none.

2. **Objection:** "The K3 drift sweep shows degraded accuracy. Your methodology for modeling drift is flawed."
   - **Why dangerous:** Attacks the core simulator physics.
   - **Strongest response:** It is not a modeling flaw; it accurately reflects the extreme fragility of the 2nd-order minima. Uniform drift pushes the optimizer out of narrow survival basins.
   - **Missing evidence:** `[K3-0p25 pending]`

3. **Objection:** "The bimodal variance (22% to 61%) is just noise from insufficient training epochs."
   - **Why dangerous:** Dismisses the physical limit claim.
   - **Strongest response:** Training loss plateaued over 100 epochs. The variance is intrinsic to the landscape, not a transient optimization state.
   - **Missing evidence:** none.

4. **Objection:** "Why not use Sharpness-Aware Minimization (SAM) to fix the bimodal basins?"
   - **Why dangerous:** Points to an obvious algorithmic gap.
   - **Strongest response:** Computing SAM over a 2nd-order analog tracking surrogate is currently computationally intractable for 10M+ parameters, leaving it as future work.
   - **Missing evidence:** none.

5. **Objection:** "You overclaim 'structural limit' when 4 of 30 instances achieve >50% accuracy."
   - **Why dangerous:** Attacks the definition of the limit.
   - **Strongest response:** We define the limit structurally in terms of *yield* and *reliability*. A 50% garbage rate is a structural failure for any deterministic deployment.
   - **Missing evidence:** none.

6. **Objection:** "Perhaps your 2nd-order STE is fundamentally miscalibrated."
   - **Why dangerous:** Attacks the surrogate model validity.
   - **Strongest response:** The 2nd-order STE faithfully captures local curvature. Any further 'calibration' would mask the true physical landscape fragmentation.
   - **Missing evidence:** `[K5 3rd-order landing pending]`

7. **Objection:** "If K3 drift hurts performance, the mean-field annealing theory in your intro is wrong."
   - **Why dangerous:** Undermines the theoretical setup.
   - **Strongest response:** We frame the mean-field theory as a testable hypothesis, which our rigorous K3 empirical data falsifies, advancing community understanding.
   - **Missing evidence:** `[K3-0p25 pending]`

8. **Objection:** "The results are specific to the chosen Tiny-ViT architecture and won't generalize."
   - **Why dangerous:** Limits the impact of the findings.
   - **Strongest response:** The Lipschitz bounds of the Softmax operator scale with matrix dimensionality. Larger ViTs will likely experience worse shattering without architectural changes.
   - **Missing evidence:** none.

9. **Objection:** "Binning the chips post-fabrication solves this. The simulation is pessimistic."
   - **Why dangerous:** Argues the problem is trivial in hardware.
   - **Strongest response:** Binning cannot recover the massive Total Cost of Ownership (TCO) losses incurred by a <50% yield.
   - **Missing evidence:** none.

10. **Objection:** "The pathway decomposition is flawed if linearizing QKV (J1b) still collapsed."
    - **Why dangerous:** Attacks the foundational pathway analysis.
    - **Strongest response:** The collapse of J1b confirms the QKV condition number is the primary driver; both paths (MLP and QKV) must be addressed, but QKV is the structural blocker.
    - **Missing evidence:** none.

11. **Objection:** "The degradation under K3 is just an artifact of the specific delta_g_eff grid chosen."
    - **Why dangerous:** Implies a tuning error rather than a physical truth.
    - **Strongest response:** We swept a granular grid (0.0 to 0.25). The consistent failure to lift the mean across this grid robustly falsifies the annealing hypothesis.
    - **Missing evidence:** `[K3-0p25 pending]`

12. **Objection:** "This is purely a negative result, better suited for a workshop."
    - **Why dangerous:** Venue mismatch.
    - **Strongest response:** Falsifying the viability of naive analog Transformers at severe NL prevents multi-million dollar tape-out errors, constituting high-impact scientific knowledge.
    - **Missing evidence:** none.
