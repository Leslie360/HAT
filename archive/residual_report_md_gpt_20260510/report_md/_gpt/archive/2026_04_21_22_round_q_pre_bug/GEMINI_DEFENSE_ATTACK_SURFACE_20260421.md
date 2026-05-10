# G-HH4: Defense Attack Surface
**Date:** 2026-04-21
**Scope:** Phase α (G-HH4)

This document anticipates the 15 most rigorous and hostile questions a PhD defense committee might ask regarding the current state of the Compute-ViT framework, specifically focusing on the vulnerabilities introduced by the severe-NL diagnostic loop. It provides evidence-backed response paths using *only* data currently on disk.

---

## Group 1: The "Broken Simulator" Angle
**1. "If all your mitigations collapse at NL=2.0, how do we know your PyTorch analog simulation layer doesn't just have a numerical overflow bug?"**
*Response Path:* Point to the `all-linear` (CX-AB) baseline. It achieves ~32.60% accuracy, avoiding the 10.00% chance-level collapse. Furthermore, our models achieve >86% accuracy at NL=1.0 and >97% without noise. A numerical bug would corrupt all forward passes, not just the non-linear mappings.

**2. "Is NL=2.0 a physically realistic parameter, or did you just inject so much noise that any neural network would mathematically fail?"**
*Response Path:* NL=2.0 represents a severe, but physically grounded, non-ideality typical of early-stage organic memristors (e.g., strong asymmetry in LTP/LTD updates). Cite `docs/PHYSICS_STACK.md` and the organic optoelectronic literature profiles we fitted against. It is an edge-case stress test, not random noise.

## Group 2: The Bimodal Basin (Branch C) Attacks
**3. "You claim a 'bimodal basin' at ~38.95% mean accuracy. Isn't this just evidence of insufficient hyperparameter tuning or a bad learning rate schedule?"**
*Response Path:* We executed a rigorous stability extension (CX-K2, N=30 seeds) holding hyperparameters constant. The resulting per-instance distribution was strictly bimodal (ranges from 22.03% to 61.69%). If it were a global learning rate failure, the distribution would be uniform or unimodally poor, not fractured into distinct survival vs. collapse basins.

**4. "If higher-order Taylor surrogates (CX-K2) recover some instances to >50%, doesn't that invalidate your claim in Chapter 5 that the limit is structural to the attention mechanism?"**
*Response Path:* It refines it. The structural limit of attention is that its Lipschitz constant drastically amplifies the *variance* of the analog mapping. The higher-order surrogate proves that the optimal weights exist, but the bimodal distribution proves that reaching them reliably is structurally hindered by the attention landscape.

**5. "Did you test adding a third-order Taylor term? Maybe second-order just isn't enough."**
*Response Path:* Yes (CX-K5). Adding the third-order term saturated the recovery at ~42.8%. The instability is intrinsic to the severe NL landscape, not an artifact of truncation error in the surrogate.

## Group 3: The CrossSim Comparison
**6. "Your baseline inference matches CrossSim, but under noise, your framework drops 14.43 percentage points faster than CrossSim. Why should we trust your noise injection over Sandia's established tool?"**
*Response Path:* CrossSim's default noise injection primarily models additive Gaussian read noise. Our framework rigorously models conductance-dependent, state-aware non-idealities (asymmetric LTP/LTD). The divergence under noise is exactly the intended contribution of this thesis: proving that naive noise models underestimate the damage caused by physical programming asymmetry.

## Group 4: Device Physics & Scale
**7. "How can you justify evaluating spatial IR drop (CX-J4) when you lack an actual layout or routing design for the organic array?"**
*Response Path:* We explicitly state our spatial IR drop model is a minimal-effort circuit-aware layer geometry (16x16 vs 32x32), acting as a preliminary stress test. By showing 16x16 maintains 85% accuracy while 32x32 drops to 81%, we provide a boundary condition that informs future physical layout constraints, without overclaiming we've solved the full routing problem.

**8. "Does the temperature drift stress-test (CX-J3) account for non-uniform thermal hotspots on the chip, or just a uniform global temperature shift?"**
*Response Path:* CX-J3 models Arrhenius-form conductance drift across a global -20C to 85C range. While it does not model localized hotspots, it successfully validates that the rank-ordering of weights is preserved under uniform thermal scaling, isolating one major variable before moving to complex spatial thermal maps.

**9. "You cite a 1-month retention extrapolation (CX-J6) plateauing at 78.5%. Isn't 1 month far too short for edge deployment?"**
*Response Path:* The 1-month benchmark is an accelerated aging protocol designed to expose the short-term state relaxation typical of organic memristors. The plateau at 78.5% is crucial because it demonstrates the degradation is bounded, providing a predictable floor for system-level calibration, rather than a continuous slide to 10% chance.

**10. "If the ADC floor is 6-bits (CX-J7), but standard digital architectures are moving to 4-bit or lower, isn't CIM fundamentally uncompetitive for this architecture?"**
*Response Path:* The 6-bit cliff (85% acc) vs 5-bit (79% acc) is precisely the risk-ranking value our framework provides. It proves that to be competitive, analog arrays must guarantee 6-bit precision, guiding hardware engineers on the exact specification they must meet to match digital performance.

## Group 5: The Methodology & Claims
**11. "Your thesis relies heavily on 'Ensemble HAT'. How is this different from simple data augmentation with random noise?"**
*Response Path:* Simple data augmentation adds noise to the activations or inputs. Ensemble HAT resamples the specific, hardware-derived D2D mismatch mask *at every epoch*, directly exposing the optimizer to the expected hardware deployment distribution of the physical weights themselves.

**12. "You only test Tiny-ViT (5M parameters). Can you guarantee these limits won't just vanish with a larger ViT-B model?"**
*Response Path:* We cannot guarantee it, which is exactly why we documented scaling as an 'Open Problem' (G-HH16). However, the Lipschitz amplification mechanism we formalized in G-HH5 suggests that without architectural changes (like pre-LN or Linear Attention), simply increasing depth may compound the variance, making the bimodality worse.

**13. "If the bimodal basin means 50% of your chips are 'silicon garbage', why should any funding agency give you a grant to continue?"**
*Response Path:* Because identifying the 50% failure rate *before* spending $10M on a tape-out is exactly what simulation tools are for. The next grant (G-HH11) focuses on convexifying these basins via HA-SAM and Linearized Attention Primitives to rescue that 50% yield.

**14. "You claim the MLP path is the bottleneck, but linearizing QKV only (CX-J1b) collapsed to 26.54%. Doesn't this contradict your own pathway decomposition?"**
*Response Path:* No, it confirms it. The QKV path has an exponentially higher condition number due to the Softmax. If QKV is unprotected (or only partially protected), it shatters the landscape. We found that *both* paths must be addressed, but the attention mechanism is the structural limit that prevents first-order recovery.

**15. "Why did you switch your thesis language to Simplified Chinese mid-project? Doesn't this limit your audience?"**
*Response Path:* The core scientific results (Paper-1, Paper-2, code releases) remain entirely in English for the global community. The thesis language pivot adheres to the specific formatting and submission regulations of the degree-granting institution, ensuring administrative compliance without compromising scientific dissemination.
