# G-DR6: Defense Attack Surface v2
**Date:** 2026-04-22

1. **"Why does your K2 data show a bimodal distribution instead of a Gaussian curve?"**
   - *Short answer:* The Softmax Lipschitz constant shatters the loss landscape.
   - *Longer answer:* Severe asymmetric NL creates deep, narrow ravines. The 2nd-order STE allows the optimizer to find these fragile minima, but fresh D2D noise causes stochastic survival or collapse.
   - *Depends on K3-0p25:* no.

2. **"Why did K3's drift sweep fail to improve the mean accuracy significantly?"**
   - *Short answer:* Global drift destroys fragile local minima.
   - *Longer answer:* The mean-field annealing hypothesis assumed drift would convexify the space. Instead, it pushes the optimizer out of narrow survival basins into broader collapse basins.
   - *Depends on K3-0p25:* yes.

3. **"Is the 38.95% mean from K2 a hard physical limit?"**
   - *Short answer:* It's a stochastic yield limit.
   - *Longer answer:* Optimal weights exist (some instances hit >50%), but the optimization trajectory cannot reliably converge on them due to landscape fragmentation.
   - *Depends on K3-0p25:* no.

4. **"If the surrogate fidelity ladder saturated, why did K3 fail?"**
   - *Short answer:* K3 tests trajectory, not surrogate fidelity.
   - *Longer answer:* Modeling the curvature perfectly (2nd-order) doesn't change the fact that uniform drift (K3) physically breaks the found minimum.
   - *Depends on K3-0p25:* yes.

5. **"Could lower learning rates have settled into the >50% basins more reliably?"**
   - *Short answer:* No, due to D2D resampling.
   - *Longer answer:* Ensemble HAT resamples the D2D mask every epoch. A low learning rate fails to adapt to the new mask, causing catastrophic forgetting.
   - *Depends on K3-0p25:* no.

6. **"Why shouldn't industry just use digital attention and ignore this?"**
   - *Short answer:* They should.
   - *Longer answer:* Our framework explicitly proves that Hybrid CIM (Digital Attention + Analog MLP) is strictly necessary under severe NL.
   - *Depends on K3-0p25:* no.

7. **"Is the 22% lower bound of the bimodal distribution random chance?"**
   - *Short answer:* Yes, near 10% chance level.
   - *Longer answer:* The collapse basin destroys the attention map's ability to mix tokens, reducing the ViT to a severely impaired bag-of-patches classifier.
   - *Depends on K3-0p25:* no.

8. **"What if the device asymmetry (NL_LTP vs NL_LTD) was reversed?"**
   - *Short answer:* The Lipschitz bound remains identically broken.
   - *Longer answer:* The magnitude of the distortion, not the sign, drives the exponential variance amplification through the Softmax.
   - *Depends on K3-0p25:* no.

9. **"Why stop K3 at delta_g_eff=0.25?"**
   - *Short answer:* Beyond 0.25 is physically unrealistic.
   - *Longer answer:* Shifting 25% of the dynamic range per update means the device acts more like a random number generator than functional memory.
   - *Depends on K3-0p25:* yes.

10. **"Why include Tier-2 spatial mitigations (IR drop) if the baseline is simulation?"**
    - *Short answer:* To prove orthogonality.
    - *Longer answer:* IR drop is an additive spatial error. The Softmax collapse is a multiplicative error. We prove they are distinct failure modes.
    - *Depends on K3-0p25:* no.

11. **"Why does Chapter 5 frame K2 as a falsification if some instances survive?"**
    - *Short answer:* It falsifies deterministic yield.
    - *Longer answer:* Hardware demands >99% yield. A bimodal distribution with significant collapse fundamentally falsifies commercial viability.
    - *Depends on K3-0p25:* no.

12. **"Could post-training calibration fix the scale mismatch?"**
    - *Short answer:* No, D2D is instance-specific.
    - *Longer answer:* You cannot calibrate a global PTQ factor for an array where the error pattern changes stochastically on every fresh chip.
    - *Depends on K3-0p25:* no.

13. **"Do your limits apply to perfectly linear arrays (NL=1.0)?"**
    - *Short answer:* No.
    - *Longer answer:* Our positive control (Ensemble HAT at NL=1.0) achieves >86%. The structural limit requires the *interaction* of Softmax and Severe NL.
    - *Depends on K3-0p25:* no.

14. **"Does this theory hold for NLP Transformers like LLaMA?"**
    - *Short answer:* The Softmax mechanism holds, but input stats differ.
    - *Longer answer:* Vision patches have different covariance structures than text embeddings. The exact onset of the bimodal basin might shift, but the Lipschitz bound applies.
    - *Depends on K3-0p25:* no.

15. **"What is the single biggest takeaway?"**
    - *Short answer:* Analog attention is stochastically unstable.
    - *Longer answer:* First-order models hide yield collapse. High-fidelity simulation proves analog attention is a dead end without architectural linearization.
    - *Depends on K3-0p25:* no.
