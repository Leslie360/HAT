# G-HH22: Theoretical Quantization Floor for Attention Softmax
**Date:** 2026-04-23
**Scope:** Work 2 (LLM KV-Cache Mapping)

## 1. Top-K Rank Preservation in Attention

In LLM decoding, the exact absolute values of the attention matrix $A = \text{softmax}\left(\frac{Q K^T}{\sqrt{d}}\right)$ are less critical than the **relative ranking** of the top-$k$ attended tokens. If the device noise $\sigma_{dev}$ and quantization noise $\sigma_Q$ cause a non-relevant token to overtake a critical token (a rank-flip), the generated perplexity will degrade exponentially.

Let $S_i$ be the true pre-softmax logit for the $i$-th token. Assume token 1 is the ground-truth top token, and token 2 is the runner-up. Let the gap be $\delta = S_1 - S_2 > 0$.

When mapping $K$ and $V$ to analog states, the logit $S_i$ is corrupted by an additive error $e_i$, forming $\tilde{S}_i = S_i + e_i$.
A catastrophic rank-flip occurs if $\tilde{S}_2 > \tilde{S}_1$, which implies:
$$ e_2 - e_1 > \delta $$

## 2. Noise Propagation and Variance
The error $e_i$ arises from the dot product of the query vector $q$ and the noisy key vector $\tilde{k}_i$:
$$ \tilde{k}_i = \text{Quantize}_{N}(k_i) + \mathcal{N}(0, \sigma_{dev}^2 I) $$
The quantization error for $N$ states is uniformly distributed with variance $\sigma_Q^2 = \frac{\Delta^2}{12}$, where $\Delta = \frac{k_{max} - k_{min}}{N-1}$.

The total error variance per weight is $\sigma_W^2 = \sigma_Q^2 + \sigma_{dev}^2$.
Assuming query elements $q_j$ are independent with variance $\sigma_q^2$, the variance of the logit error $e_i$ (a sum over $d$ dimensions) is:
$$ \text{Var}(e_i) = \sigma_{logit}^2 = d \cdot \sigma_q^2 \cdot \left( \frac{(k_{max}-k_{min})^2}{12(N-1)^2} + \sigma_{dev}^2 \right) $$

## 3. Deriving the Theoretical Floor for N
The difference $e_2 - e_1$ has variance $2\sigma_{logit}^2$. Assuming the errors are roughly Gaussian (by the Central Limit Theorem for large $d$):
$$ e_2 - e_1 \sim \mathcal{N}(0, 2\sigma_{logit}^2) $$
The probability of a rank-flip is:
$$ \mathbb{P}(e_2 - e_1 > \delta) = Q\left( \frac{\delta}{\sqrt{2}\sigma_{logit}} \right) < \epsilon_{flip} $$
Where $Q(x)$ is the standard Gaussian tail probability. Let $\gamma = Q^{-1}(\epsilon_{flip})$. We require:
$$ \sigma_{logit} < \frac{\delta}{\sqrt{2}\gamma} $$

Substituting the expression for $\sigma_{logit}^2$:
$$ d \cdot \sigma_q^2 \cdot \left( \frac{(k_{max}-k_{min})^2}{12(N-1)^2} + \sigma_{dev}^2 \right) < \frac{\delta^2}{2\gamma^2} $$

Solving for $N$:
$$ \frac{(k_{max}-k_{min})^2}{12(N-1)^2} < \frac{\delta^2}{2\gamma^2 d \sigma_q^2} - \sigma_{dev}^2 $$
$$ N > 1 + \frac{k_{max}-k_{min}}{\sqrt{12 \left( \frac{\delta^2}{2\gamma^2 d \sigma_q^2} - \sigma_{dev}^2 \right)}} $$

## 4. Conclusion and Number-Agnostic Projection
This inequality establishes the **fundamental floor on analog-state count $N$**.
Crucially, it reveals a hard physical limit: if the device noise $\sigma_{dev}$ exceeds $\frac{\delta}{\sqrt{2d}\gamma\sigma_q}$, the denominator becomes imaginary, meaning **no amount of quantization precision (even $N \to \infty$) can save the attention ranking**.

Until `CX-L1` provides the empirical values for the expected attention gap $\delta$, query variance $\sigma_q^2$, and dimension $d$ for TinyLlama-1.1B, the exact numerical value of $N$ remains agnostic. However, based on typical LLM logit distributions, we hypothesize $N_{floor}$ will lie in the range of $4 \le N \le 6$ (2 to 2.5-bit equivalent).
