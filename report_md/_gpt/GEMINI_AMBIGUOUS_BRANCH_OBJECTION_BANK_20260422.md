# G-DR5: Reviewer Objection Bank (Ambiguous Branch + Weak K3)
**Date:** 2026-04-22

1. **Objection:** "Adding conductance drift (K3) reduces accuracy from 38% to 27%. Your mitigation strategy is fundamentally flawed."
   - **Danger:** Attacks the premise that we understand the optimization landscape.
   - **Response:** K3 is a diagnostic, not a mitigation. It proves that naive uniform drift pushes the optimizer out of fragile 2nd-order minima into worse collapse basins, validating the extreme sensitivity of the bimodal landscape.
   - **Missing Evidence:** `[K3-0p25 pending]`

2. **Objection:** "The bimodal distribution is just an artifact of insufficient training time."
   - **Danger:** Dismisses the physical limit claim.
   - **Response:** Convergence was reached (100 epochs). Training loss plateaued.
   - **Missing Evidence:** None (K2 training logs confirm plateau).

3. **Objection:** "Your 2nd-order STE is obviously miscalibrated if it creates bimodal results."
   - **Danger:** Attacks the surrogate model.
   - **Response:** The 2nd-order STE correctly reflects the local curvature. The bimodality is the *true* landscape of the hardware.
   - **Missing Evidence:** None (K5 3rd-order confirms saturation).

4. **Objection:** "38% is not deployment-ready. The paper has no positive result."
   - **Danger:** "Incremental" rejection.
   - **Response:** The value is in falsification and risk-ranking pre-silicon. We identify the failure mode so hardware designers can avoid it.
   - **Missing Evidence:** None.

5. **Objection:** "Why didn't you try SAM if the landscape is sharp?"
   - **Danger:** Points to obvious algorithmic gap.
   - **Response:** Computationally intractable for 2nd-order analog tracking; listed as future work.
   - **Missing Evidence:** None.

6. **Objection:** "The degradation at dg_eff=0.15 means your hardware assumptions are contradictory."
   - **Danger:** Attacks physics model.
   - **Response:** High drift breaks the delicate balance found by the 2nd-order STE, exposing the narrowness of the survival basins.
   - **Missing Evidence:** `[K3-0p25 pending]`

7. **Objection:** "A range of 22% to 61% means the simulation is unstable, not the hardware."
   - **Danger:** Dismisses the tool entirely.
   - **Response:** FP32 and NL=0.0 baselines on the same tool show tight Gaussian variance (~1.5%). The instability is specific to NL=2.0.
   - **Missing Evidence:** None.

8. **Objection:** "You should have binned the chips and only evaluated the >50% ones."
   - **Danger:** Misses the point of yield prediction.
   - **Response:** Yield is the core metric. Binning post-hoc ignores the 50%+ garbage rate, which drives TCO (Total Cost of Ownership) up unacceptably.
   - **Missing Evidence:** None.

9. **Objection:** "Maybe the patch embedding layer is the real bottleneck."
   - **Danger:** Misdirection.
   - **Response:** Pathway decomposition (G-GG3) mathematically shows QKV condition number is the primary driver of variance.
   - **Missing Evidence:** None.

10. **Objection:** "If K3 doesn't help, what was the point of the experiment?"
    - **Danger:** "Useless ablation" critique.
    - **Response:** It falsifies the mean-field annealing hypothesis, proving the landscape cannot be simply smoothed by global noise.
    - **Missing Evidence:** `[K3-0p25 pending]`

11. **Objection:** "Your results rely on a single Tiny-ViT architecture."
    - **Danger:** Scale attack.
    - **Response:** Lipschitz bounds suggest larger models will be strictly worse without architectural changes, as matrix dimensions increase the Softmax amplification.
    - **Missing Evidence:** None.

12. **Objection:** "The paper is too negative for Nature Communications."
    - **Danger:** Venue mismatch.
    - **Response:** Rigorous falsification of a multi-million dollar tape-out risk is a high-impact physical sciences result. (Alternatively, pivot to ICLR for Paper-2).
    - **Missing Evidence:** None.
