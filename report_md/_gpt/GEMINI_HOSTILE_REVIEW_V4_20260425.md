# G-HH13: Hostile Review v4 (Branch C Focus)
**Date:** 2026-04-25
**Scope:** Phase γ

## R1 (The Optimizer): "Use SAM."
*Critique:* "The bimodal distribution just means you are falling into sharp minima. This is a known problem in deep learning. Just use Sharpness-Aware Minimization (SAM) and the problem goes away. This isn't a hardware limit."
*Defense:* SAM requires computing the gradient of the gradient, doubling the backward pass cost. For 10M+ parameters with 2nd-order analog tracking, this is currently computationally intractable. Furthermore, standard SAM assumes isotropic noise, whereas analog D2D is highly asymmetric and weight-dependent.

## R2 (The Hardware Purist): "Missing Sneak Paths."
*Critique:* "You claim landscape fragmentation, but you didn't model crossbar sneak paths or spatial IR drops in the J1d runs."
*Defense:* Sneak paths and IR drops are spatially correlated and additive (as shown in our CX-J4 ablation). They shift the mean loss but do not inherently shatter the local landscape geometry. The bimodality is driven by the multiplicative nature of QKV attention under stochastic D2D noise, independent of IR drop.

## R3 (The Skeptic): "39% is still terrible."
*Critique:* "Whether it's 30% or 39%, the accuracy is unusable. The paper is incremental."
*Defense:* The contribution is falsification and yield risk-ranking. Identifying *why* it fails (bimodal landscape fragmentation vs absolute structural wall) dictates whether the community should fix the algorithm (SAM) or abandon the architecture entirely.
