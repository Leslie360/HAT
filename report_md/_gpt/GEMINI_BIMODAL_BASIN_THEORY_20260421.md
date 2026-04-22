# G-HH5: Bimodal Basin Theory
**Date:** 2026-04-21
**Scope:** Phase β

## Formal Claim
Under fresh-instance D2D sampling, severe non-ideality (NL=2.0) combined with a higher-order surrogate exposes a strictly bimodal basin structure in the loss landscape of the Transformer.

## Derivation & Condition
Let $J(\theta)$ be the loss function. The analog mapping injects instance-specific noise $W' = W + \Delta W$. Under standard first-order analysis, if $\Delta W \sim \mathcal{N}(0, \sigma^2)$, the expected loss shifts smoothly: $\mathbb{E}[J] \approx J(\theta) + \frac{1}{2} \sigma^2 \text{Tr}(H)$.

However, severe asymmetric NL breaks the Gaussian assumption. Crucially, the Softmax attention matrix $A = \text{softmax}(QK^T/\sqrt{d})$ has a local Lipschitz constant $L_A$ that scales exponentially with the variance of the pre-softmax logits. 
When the perturbation exceeds the linear regime ($||\Delta W|| \cdot L_A > 1$), the gradient scaling approximation collapses. The optimizer using a 2nd-order STE can "see" the local curvature during training, but the physical landscape itself is deeply fragmented. 

**Conclusion:** The optimization space is not a single wide minimum, but a shattered landscape of narrow, deep ravines (collapse to <30%) and flat plateaus (survival at >50%). Thus, the fresh-instance accuracy is not Gaussian-distributed around the ~39% mean, but bimodal.
