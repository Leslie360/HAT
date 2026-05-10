# GEMINI J1d Branch Synthesis
**Date:** 2026-04-21
**Scope:** Phase α (G-HH1)

This memo synthesizes the theoretical and narrative implications of the three possible outcomes for the J1d diagnostic (higher-order surrogate under severe NL). It establishes what claims are scientifically sound for each branch, preventing narrative overreach.

---

## Branch A: < 35% (Structural Limit Confirmed)
*Triggered if higher-order surrogate fails to break the ceiling.*

**What can be claimed:**
- The severe-NL failure mode (~10% for standard HAT, ~30% for all mitigation strategies) is a **fundamental structural property** of mapping the Softmax-Attention block to analog crossbars under severe non-ideality.
- It is NOT an artifact of the optimizer failing to find a robust minimum (as joint training also failed).
- It is NOT an artifact of the first-order gradient scaling surrogate (as higher-order surrogates also failed).

**What cannot be claimed:**
- We cannot claim that analog Transformers are entirely impossible—only that they require explicit architectural protection or fundamental device improvements beyond current organic RRAM capabilities.

**Viable Paper-2 Route:**
- **Route R-A (Structural Limits of Attention)**: A pure theoretical and empirical deep-dive into the condition number of the Softmax and the exponential amplification of analog noise.

---

## Branch C: 35–50% (Bimodal Basin Instability)
*Triggered if partial recovery occurs, but with high variance across instances (e.g., mean ~39%, range 22-62%).*

**What can be claimed:**
- Severe NL induces a **fragmented, bimodal loss landscape**.
- The hardware does not hit a hard structural wall, but rather causes fresh instances to fall stochastically into either a "robust basin" (maintaining >50% accuracy) or a "collapsed basin" (<30% accuracy).
- First-order surrogates mask this instability by averaging out the gradients, whereas higher-order surrogates expose the landscape's true fragmentation.

**What cannot be claimed:**
- We cannot claim a clean "falsification" of analog attention. Some instances survive.
- We cannot claim we have "solved" the issue, as the variance remains unacceptably high for deterministic deployment.

**Viable Paper-2 Route:**
- **Route R-A (Modified)**: Shift focus from absolute limits to "Stochastic Basin Sensitivity in Analog Neural Networks."
- **Route R-C (Theory/Optimization)**: Focus on optimization techniques (like Sharpness-Aware Minimization) designed specifically to convexify these bimodal basins.

---

## Branch B: > 50% (Ceiling Broken / Surrogate Artifact)
*Triggered if higher-order surrogate reliably recovers performance.*

**What can be claimed:**
- The ~30% ceiling was an **artifact of the first-order training surrogate**.
- High-fidelity (second/third order) modeling of the analog device during the backward pass is strictly required to find generalizable minima under severe NL.
- Analog attention is physically viable if the training simulator accurately models higher-order device physics.

**What cannot be claimed:**
- We cannot claim structural limits of the attention mechanism itself.
- We must retract the "rigorous falsification" framing.

**Viable Paper-2 Route:**
- **Route R-B (High-Fidelity Surrogate Design)**: A methods-heavy paper proposing and validating multi-order Taylor expansion surrogates for organic memristors.
