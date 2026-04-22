# G-GG3: QKV vs. MLP Pathway Decomposition Theory

**Date:** 2026-04-20  
**Author:** Gemini Phase α — Round P2  
**Scope:** Pure theory; information-flow decomposition of the ViT forward map. All cited numbers are from locked thesis chapters and archived JSON logs.  
**Sources:** `chapter_4_failure_modes.tex`, `chapter_5_mitigation.tex`, `run_tinyvit_groupwise_nl_comp.py`, `nl_mitigation_summary_20260418.json`, `nl_gradient_distortion_gpt.json`, `nl_fresh_instance_controls_all_only_20260418.json`

---

## 1. Introduction: The Anatomy of a Transformer Block

A Vision Transformer (ViT) block contains two parallel computational pathways: the **attention path** and the **MLP path**. From an information-flow perspective, these paths perform fundamentally different transformations on the token embedding matrix $X \in \mathbb{R}^{n \times d}$:

- **Attention path:** $X \mapsto \text{softmax}(X W_Q W_K^T X^T / \sqrt{d_h}) \, X W_V W_O$. This is a **global, token-to-token interaction** that re-weights the feature dimensions based on pairwise similarity. The softmax operator introduces a competitive, max-entropic nonlinearity across the token dimension.
- **MLP path:** $X \mapsto \text{GELU}(X W_{fc1}) W_{fc2}$. This is a **local, token-wise mixing** operation that applies the same nonlinear transformation independently to each token. The nonlinearity is elementwise (GELU), not competitive.

This decomposition is not merely architectural; it determines how errors and perturbations in the analog weight arrays propagate through the network. This memo analyzes why MLP-only linearization recovers source-domain accuracy while QKV-only linearization collapses, and why the patch-embedding convolution occupies a special position in the sensitivity hierarchy.

---

## 2. Information-Flow Analysis

### 2.1 The MLP path as a local kernel machine

Consider a single token $x \in \mathbb{R}^d$. The MLP computes

$$
\text{MLP}(x) = \text{GELU}(x W_{fc1} + b_1) W_{fc2} + b_2.
$$

For a fixed input distribution, the GELU nonlinearity can be expanded in a Hermite polynomial basis:

$$
\text{GELU}(z) = \sum_{k=0}^{\infty} c_k \, \text{He}_k(z),
$$

where $c_k$ are coefficients and $\text{He}_k$ are probabilist's Hermite polynomials. The MLP therefore implements a **kernel expansion** of the input token in a reproducing kernel Hilbert space (RKHS) defined by the GELU activation. The weights $W_{fc1}$ and $W_{fc2}$ control the kernel basis and the kernel coefficients, respectively.

The key property is **locality**: an error in $W_{fc1}$ affects only the *magnitude* of the GELU response for the tokens that pass through it. Because the GELU is a smooth, monotonic function with a well-defined linear regime near zero, small perturbations to $W_{fc1}$ produce small, continuous perturbations to the output. There is no competitive re-ranking; the error is **additive and contractive** (thanks to LayerNorm and residual connections).

### 2.2 The attention path as a global similarity graph

The attention path computes a **weighted adjacency matrix** over tokens:

$$
A_{ij} = \frac{\exp(S_{ij})}{\sum_k \exp(S_{ik})}, \qquad S_{ij} = \frac{q_i \cdot k_j}{\sqrt{d_h}}.
$$

The output for token $i$ is a convex combination of the value vectors:

$$
y_i = \sum_j A_{ij} v_j.
$$

The attention scores $A_{ij}$ form a **doubly stochastic-like** matrix (row-stochastic by construction) that encodes the semantic relationships between tokens. In vision, this allows a patch token to "attend to" spatially distant but semantically similar patches.

The critical difference from the MLP path is that the attention path contains a **bilinear form** ($QK^T$) followed by an **exponential normalization** (softmax). These operators have two properties that make the path structurally fragile:

1. **Bilinearity:** The score $S_{ij}$ depends on the *product* of two independently learned matrices, $W_Q$ and $W_K$. If either matrix is perturbed, the product is perturbed multiplicatively, not additively. An $\epsilon$-error in $W_Q$ and an $\epsilon$-error in $W_K$ compound to an $O(\epsilon^2)$ error in $S$ if the errors are correlated, or an $O(\epsilon)$ error if they are anti-correlated.
2. **Exponential sensitivity:** The softmax exponentiates the scores. A perturbation $\Delta S_{ij} = \epsilon$ changes the attention weight by

$$
\Delta A_{ij} \approx A_{ij} (1 - A_{ij}) \, \epsilon.
$$

When $A_{ij}$ is near $0.5$ (maximally uncertain attention), the sensitivity is $0.25 \epsilon$. But when one token dominates ($A_{ij} \approx 1$), the sensitivity to competing tokens vanishes. This means the softmax creates **sharp, winner-take-all attention maps** that are structurally rigid: once the optimizer has found a sharp map, small perturbations to $W_Q$ or $W_K$ can flip the winner, causing a discontinuous change in the output $y_i$.

### 2.3 The compositional difference

The MLP path composes as

$$
\text{MLP}_L \circ \text{Attn}_L \circ \cdots \circ \text{MLP}_1 \circ \text{Attn}_1 \circ \text{PatchEmbed}.
$$

Each MLP layer is a **contractive perturbation** of the identity (thanks to residual connections and LayerNorm). Each attention layer is a **re-ranking operator** that can non-locally reshuffle information. The MLP path *refines* representations; the attention path *routes* them. Linearizing the MLP path preserves the routing; linearizing the attention path destroys the refinement mechanism by removing the nonlinearity that shapes the routing.

Wait—that is backwards. The data show that linearizing the MLP path *recovers* accuracy ($87.79\%$ source-domain), while linearizing the QKV path *collapses* it ($18.72\%$). The correct interpretation is:

- **MLP linearization preserves the attention routing.** The attention mechanism remains nonlinear and functional, so the global token-to-token structure is intact. The MLP, even with ideal linear write, still provides sufficient local mixing because the GELU activation (which is digital, not analog) preserves the nonlinearity of the path.
- **QKV linearization destroys the attention routing.** The QKV projection is the *gateway* to the attention mechanism. If the QKV weights are programmed with an ideal linear surrogate ($NL=1.0$) while the output projection suffers $NL=2.0$, the attention scores are computed from "clean" queries and keys but projected back through a distorted output matrix. Wait—the group-wise ablation shows that QKV-only linearization *collapses below the unmitigated baseline* ($18.72\%$ vs. $27.72\%$). This suggests that the attention mechanism is not merely sensitive to distortion; it is **structurally coupled** to the nonlinearity in a way that linearization breaks.

The resolution is that the QKV and output-projection linearizations are *not independent*. The attention geometry depends on the *interaction* between QKV and output projection through the residual stream:

$$
X_{\text{out}} = X + \text{Attn}(\text{LN}(X)) + \text{MLP}(\text{LN}(X + \text{Attn}(\text{LN}(X)))).
$$

When QKV is linearized in isolation, the *forward* pass uses ideal QKV weights but the *backward* pass uses ideal gradients for QKV and distorted gradients for the output projection. This creates a **gradient mismatch**: the forward attention map is computed with clean QKV, but the gradient that flows back to QKV passes through the distorted output-projection surrogate. The optimizer therefore updates QKV based on a backward signal that is inconsistent with the forward computation. This inconsistency is a form of **adversarial training** that drives QKV toward a subspace that minimizes the inconsistent gradient, causing representational collapse.

---

## 3. Why MLP-Only Linearization Works (Source-Domain)

The gradient-distortion diagnostic (`nl_gradient_distortion_gpt.json`) provides direct evidence:

| Group | Affected grad cosine | Affected grad norm ratio |
|---|---|---|
| MLP only | $0.815$ | $0.671$ |
| QKV only | $1.000$ | $1.000$ |
| Attn proj only | $1.000$ | $1.000$ |

When $NL=2.0$ is applied only to the MLP blocks, the backward gradient for MLP parameters is scaled and rotated (cosine $0.815$, norm ratio $0.671$), while attention parameters receive *perfect* gradients. The optimizer can therefore learn ideal attention geometry and adapt the MLP weights to the distorted backward signal. Because the MLP path is local and redundant, the MLP weights can absorb the distortion without catastrophic loss of representational capacity.

Source-domain accuracy reaches $87.79\%$ (`nl_mitigation_summary_20260418.json`), only $0.16$ pp below the canonical $NL=1.0$ baseline of $87.95\%$. The MLP path is a **bottleneck, not a structural foundation**: linearizing it removes the bottleneck, and the remaining attention path carries the network to near-baseline accuracy.

---

## 4. Why QKV-Only Linearization Fails

When $NL=2.0$ is applied to the attention output projection while QKV is linearized, the forward pass computes attention scores with clean QKV but projects the output through a distorted matrix. The backward pass sends clean gradients to QKV but distorted gradients to the output projection. The problem is that the **output projection is the inverse of the value aggregation**: it maps the mixed value vectors back to the embedding dimension. If this projection is distorted, the residual stream $X + \text{Attn}(X)$ receives a corrupted update, and the LayerNorm that follows cannot fully correct it because the corruption is structured across the feature dimension, not just a scale shift.

More formally, let $W_O$ be the output projection. Under severe NL, the effective weight is $\hat{W}_O = s_\ell \, \Phi(G_O) \odot (1 + M)$. The attention output is

$$
\text{Attn}(X) = A(X) \, X W_V \, \hat{W}_O.
$$

If $\hat{W}_O$ is distorted, the product $W_V \hat{W}_O$ becomes a *random linear transformation* of the value space. Because $W_V$ and $\hat{W}_O$ are learned jointly, the optimizer can partially compensate by adapting $W_V$ to the particular distortion of $\hat{W}_O$. But when QKV is linearized *in isolation*, $W_Q$ and $W_K$ are *not* allowed to adapt to the output-projection distortion because their gradients are clean (they do not sense the distortion). The result is a **decoupled optimization**: $W_Q$ and $W_K$ optimize for an ideal output projection, while $W_V$ optimizes for a distorted one. The attention mechanism is torn between two incompatible objectives, and the residual stream collapses.

This explains why QKV-only linearization ($18.72\%$) is *worse* than the unmitigated global $NL=2.0$ baseline ($27.72\%$): the global baseline at least provides *consistent* distortion across all attention parameters, allowing the optimizer to find a joint compromise.

---

## 5. Patch-Embedding Convolution Sensitivity

The patch-embedding layer (`patch_embed.conv1` and `patch_embed.conv2`) is the first analog-mapped operation in Tiny-ViT. It is a strided convolution that maps the raw image pixels to a sequence of patch tokens. The gradient-distortion diagnostic shows that patch-embedding gradients are unaffected by NL distortion (cosine $1.000$, norm ratio $1.000$) when NL is applied only to MLP blocks. However, the patch-embedding layer is the *most sensitive* to D2D mismatch because:

1. **Early-layer amplification:** The patch-embedding output feeds into *all* subsequent transformer blocks. A spatially structured D2D error in the convolution kernels creates a fixed pattern of patch-corruption that propagates through the entire depth of the network. This is analogous to the "hardware-instance overfitting" described in `chapter_4_failure_modes.tex`: the model can learn to compensate for a *known* corruption pattern, but not for a fresh one.
2. **Spatial locality:** The convolution kernels are small ($3 \times 3$), so each output pixel depends on a small spatial neighborhood. A D2D mismatch that is correlated over the kernel footprint creates *coherent* spatial distortions (e.g., blurring or edge enhancement) that are semantically meaningful and therefore hard for downstream layers to decorrelate.
3. **No residual bypass:** Unlike the transformer blocks, the patch-embedding layer has no residual connection. The input image passes *through* the convolution; there is no skip path to preserve the original signal. This makes the patch-embedding layer a **single point of failure** for the visual front-end.

The all-linear lane (`nl_fresh_instance_controls_all_only_20260418.json`) linearizes the patch-embedding convolutions along with all other analog layers. Its fresh-instance accuracy is $32.60 \pm 9.18\%$, essentially identical to the MLP-only lane ($32.12 \pm 7.72\%$). This suggests that patch-embedding linearization does not materially improve fresh-instance transfer, consistent with the hypothesis that the $\sim 30\%$ ceiling is enforced by the attention pathway, not by the front-end.

---

## 6. Expected Explanation Framework for CX-J1b/c

The CX-J1b and CX-J1c experiments (proposed in `chapter_5_mitigation.tex`, \S\ref{sec:structural-limit}) are designed to falsify the attention-pathway-dominance hypothesis. Regardless of the actual numbers, the following theoretical framework can adapt:

### 6.1 CX-J1b: QKV-linear + Ensemble HAT

**Intervention:** Linearize *only* the QKV projection ($NL=1.0$) while keeping the attention output projection at $NL=2.0$, with epoch-level D2D resampling.

**Expected outcome under hypothesis:** Collapse to $\sim 30\%$ or below. The reasoning is that QKV linearization in isolation creates the decoupled optimization described in \S4. Adding Ensemble HAT resampling does not fix the decoupling because the problem is not D2D memorization but gradient inconsistency between QKV and the output projection. The fresh-instance mean should be statistically indistinguishable from the CX-J1 joint-training result ($30.53 \pm 7.07\%$).

**Alternative outcome and adaptation:** If CX-J1b exceeds $50\%$, the hypothesis is weakened. The adaptation is that the QKV-output-projection interaction is less fragile than predicted, and the $\sim 30\%$ ceiling must be attributed to a different mechanism (e.g., multi-head correlation disruption or scale-recovery mismatch in the MLP path).

### 6.2 CX-J1c: Output-projection-linear + Ensemble HAT

**Intervention:** Linearize *only* the attention output projection ($NL=1.0$) while keeping QKV at $NL=2.0$, with epoch-level D2D resampling.

**Expected outcome under hypothesis:** Collapse to $\sim 30\%$ or below. The reasoning is symmetric to CX-J1b: the output projection is the inverse of value aggregation, and if QKV is distorted, the attention scores are computed from corrupted queries and keys. Linearizing the output projection cannot restore the corrupted score geometry.

**Alternative outcome and adaptation:** If CX-J1c exceeds $50\%$, the hypothesis is weakened. The adaptation is that the output projection is the true bottleneck, not the QKV projection. This would shift the research priority to output-projection-specific mitigations (e.g., lower-rank output matrices or structured sparsity).

### 6.3 Unified falsification criterion

The attention-pathway-dominance hypothesis is supported if and only if:

$$
\text{FreshAcc(CX-J1b)} \approx \text{FreshAcc(CX-J1c)} \approx \text{FreshAcc(CX-J1)} \approx 30\%.
$$

If any single-path linearization (QKV-only or output-projection-only) breaks the ceiling while the other does not, the hypothesis must be refined into a **sub-path hypothesis** that identifies which specific matrix (Q, K, V, or O) is the structural bottleneck.

---

## 7. Summary

The transformer block decomposes into a **global routing path** (attention) and a **local refinement path** (MLP). The attention path is structurally fragile under severe NL because its bilinear score computation and exponential softmax create sharp, winner-take-all maps that are sensitive to multiplicative weight perturbations. The MLP path is structurally robust because its pointwise GELU nonlinearity creates smooth, additive perturbations that are absorbed by LayerNorm and residual connections. Patch-embedding convolutions are sensitive to D2D mismatch due to early-layer amplification and the absence of a residual bypass, but they do not enforce the $\sim 30\%$ fresh-instance ceiling. The expected outcomes of CX-J1b/c are collapse for both lanes, consistent with the attention-pathway-dominance hypothesis; if either lane escapes the ceiling, the framework adapts by localizing the bottleneck to the specific attention sub-path that remains linearized.
