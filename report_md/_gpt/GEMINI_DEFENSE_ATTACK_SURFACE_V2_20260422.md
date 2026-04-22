# G-DR6: Defense Attack Surface v2 (K2/K3 Context)
**Date:** 2026-04-22

1. **"Why did K3's drift sweep degrade performance instead of improving it?"**
   - *Short:* The mean-field annealing hypothesis was wrong.
   - *Long:* Uniform drift pushes the optimizer out of narrow survival basins into broader collapse basins. The 2nd-order minima are extremely fragile.
   - *Depends on K3-0p25:* Yes.

2. **"Is the 38.95% mean from K2 a physical ceiling or an optimization artifact?"**
   - *Short:* It's a stochastic physical ceiling.
   - *Long:* The variance proves the optimal weights exist, but the landscape shatters the optimizer's ability to reliably find them.
   - *Depends on K3-0p25:* No.

3. **"If the surrogate fidelity ladder saturated at 2nd order, why does K3 fail?"**
   - *Short:* K3 tests trajectory shifts, not surrogate fidelity.
   - *Long:* We accurately model the local curvature, but the global drift (dg_eff) breaks the fragile minima found.
   - *Depends on K3-0p25:* Yes.

4. **"Aren't you just overfitting to a specific 2nd-order Taylor expansion?"**
   - *Short:* No, CX-K5 (3rd-order) shows identical results.
   - *Long:* Adding the cubic term didn't change the bimodal mean (~42.8%). The surrogate is saturated; the landscape is the reality.
   - *Depends on K3-0p25:* No.

5. **"Why shouldn't industry just use digital attention and ignore this?"**
   - *Short:* They should. That's our conclusion.
   - *Long:* Our Paper-2 explicitly advocates for Hybrid CIM (Digital Attention + Analog MLP) precisely because of these structural limits.
   - *Depends on K3-0p25:* No.

6. **"Could lower learning rates have settled into the >50% basins more reliably?"**
   - *Short:* Unlikely, due to D2D resampling.
   - *Long:* Ensemble HAT resamples the D2D mask every epoch. A low learning rate would fail to adapt to the new mask, causing catastrophic forgetting, not better settling.
   - *Depends on K3-0p25:* No.

7. **"Is the 22% lower bound of the bimodal distribution just random chance?"**
   - *Short:* Yes, 10-class classification chance is 10%. 22% is near-chance with slight residual feature recognition.
   - *Long:* The collapse basin destroys the attention map's ability to mix tokens, effectively reducing the ViT to a bag-of-patches linear classifier.
   - *Depends on K3-0p25:* No.

8. **"What if the device asymmetry (NL_LTP vs NL_LTD) was reversed?"**
   - *Short:* The condition number of the Softmax remains the same.
   - *Long:* The magnitude of the distortion matters more than the sign for breaking the Softmax Lipschitz bound.
   - *Depends on K3-0p25:* No.

9. **"Why did you stop K3 at dg_eff=0.25?"**
   - *Short:* Beyond 0.25, the analog device behaves more like a random number generator than a memory cell.
   - *Long:* It represents 25% of the total dynamic range shifting per update, which is physically unrealistic for functional memory.
   - *Depends on K3-0p25:* Yes.

10. **"If your framework is a 'simulation baseline', why did you add Tier-2 physical mitigations (IR drop)?"**
    - *Short:* To prove the bimodal collapse is independent of spatial effects.
    - *Long:* IR drop is an additive spatial error. The Softmax collapse is a multiplicative error. Tier-2 proves they are orthogonal problems.
    - *Depends on K3-0p25:* No.

11. **"Why does your Chinese thesis Chapter 5 frame K2 as a 'falsification' if some instances survive?"**
    - *Short:* It falsifies deterministic deployment.
    - *Long:* Hardware requires >99% yield. A bimodal distribution with 50% collapse is a falsification of the architecture's commercial viability.
    - *Depends on K3-0p25:* No.

12. **"Could post-training quantization (PTQ) calibration fix the scale mismatch?"**
    - *Short:* No, D2D is instance-specific.
    - *Long:* You cannot calibrate a global PTQ scale factor for an array where the error pattern changes on every fresh chip.
    - *Depends on K3-0p25:* No.

13. **"If I build a perfect linear analog array (NL=1.0), do your limits apply?"**
    - *Short:* No.
    - *Long:* Our positive control (Ensemble HAT at NL=1.0) achieves >86% fresh-instance accuracy. The structural limit is specifically the *interaction* of Softmax and Severe NL.
    - *Depends on K3-0p25:* No.

14. **"Does your theory hold for NLP Transformers (e.g., BERT, LLaMA)?"**
    - *Short:* The Softmax math holds, but the input statistics differ.
    - *Long:* Vision patches have different covariance structures than text embeddings. While the Lipschitz bound applies, the exact onset of the bimodal basin might shift.
    - *Depends on K3-0p25:* No.

15. **"Ultimately, what is the single biggest takeaway from your thesis?"**
    - *Short:* Analog attention is a dead end without architectural linearization.
    - *Long:* First-order models hide the yield collapse. High-fidelity simulation proves that Softmax attention on organic RRAM is stochastically unstable, necessitating Hybrid CIM architectures.
    - *Depends on K3-0p25:* No.
