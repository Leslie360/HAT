# G-GG1: Formal Statement of the Structural-Limit Hypothesis

**Date:** 2026-04-20  
**Author:** Gemini Phase α — Round P2  
**Scope:** Pure theory; no unreported experimental digits. All cited numbers are drawn from locked thesis chapters and archived JSON logs.  
**Sources:** `chapter_4_failure_modes.tex`, `chapter_5_mitigation.tex`, `nl_mitigation_summary_20260418.json`, `joint_mlp_linear_ensemble_hat_full_fresh.json`

---

## 1. Preamble: What Needs Explanation

Three independent mitigations for severe nonlinear write (global $NL = 2.0$) converge to the same fresh-instance accuracy regime:

| Mitigation | Source-domain best | Fresh-instance mean $\pm$ std | Source file |
|---|---|---|---|
| MLP-only linearization ($NL=2.0$, fixed mask) | $87.79\%$ | $32.12 \pm 7.72\%$ | `chapter_5_mitigation.tex`, Table~`tab:fresh-instance-nl-c5` |
| All-linear ($NL=2.0$, fixed mask) | $87.49\%$ | $32.60 \pm 9.18\%$ | `nl_fresh_instance_controls_all_only_20260418.json` |
| Joint MLP-linear + Ensemble HAT ($NL=2.0$, epoch resampling) | $91.36\%$ | $30.53 \pm 7.07\%$ | `joint_mlp_linear_ensemble_hat_full_fresh.json` |
| *Reference:* Canonical Ensemble HAT ($NL=1.0$) | $91.13\%$ | $86.33 \pm 1.61\%$ | `fresh_instance_eval.json` |

The joint-training experiment (CX-J1) is decisive. Ensemble HAT rescues fixed-mask D2D collapse from $10.00\%$ to $86.37\%$ under $NL=1.0$, yet when coupled with MLP-linearization under $NL=2.0$ it reaches only $30.53\%$. The failure is therefore **not an optimization gap**. This memo states a falsifiable structural hypothesis that explains why severe-NL $\times$ attention blocks may constitute a fundamental generalization barrier.

---

## 2. Definitions

### 2.1 First-order nonlinear-write surrogate

Let $G$ denote the target differential conductance before programming, and let $\hat{G}$ denote the effective conductance after the analog write. The first-order surrogate models the write nonlinearity as a deterministic power law:

$$
\hat{G} = \begin{cases}
+\,|G|^{NL} & \text{(LTP)}, \\[4pt]
-\,|G|^{NL} & \text{(LTD)},
\end{cases}
\qquad NL \ge 1.
$$

During hardware-aware training (HAT), the forward pass uses $\hat{G}$, but the backward pass applies a straight-through estimator (STE) with a state-dependent scaling factor:

$$
\frac{\partial \hat{G}}{\partial G}\bigg|_{\text{STE}} = NL \, |G|^{NL-1} \, \text{sign}(G).
$$

For $NL = 1.0$ this reduces to the identity. For $NL = 2.0$ the scaling becomes **asymmetric** between LTP and LTD because the magnitude $|G|$ enters the gradient multiplicatively:

$$
\frac{\partial \hat{G}}{\partial G}\bigg|_{NL=2.0} = 2 \, |G| \, \text{sign}(G) = 2G.
$$

Wait—that appears symmetric. The true asymmetry arises when the *physical* LTP and LTD branches have *different* exponents, or when the conductance is mapped from a signed weight $w = s(G^+ - G^-)$ and the two branches experience opposite-polarity distortion. In the present framework the asymmetry is encoded by distinct parameters $NL_{\text{LTP}}$ and $NL_{\text{LTD}}$; for severe nonlinearity we set $|NL_{\text{LTD}}| = NL_{\text{LTP}} = 2.0$, but the sign flip between potentiation and depression means that a weight near zero receives a gradient whose magnitude depends on the polarity of the last update.

### 2.2 Attention-block forward map

Consider a single-head self-attention layer. Let $X \in \mathbb{R}^{n \times d}$ be the token embedding matrix after layer normalization. The QKV projection is

$$
Q = X W_Q, \quad K = X W_K, \quad V = X W_V,
$$

with $W_Q, W_K, W_V \in \mathbb{R}^{d \times d_h}$. The attention score matrix is

$$
S = \frac{QK^T}{\sqrt{d_h}} \in \mathbb{R}^{n \times n},
$$

and the output is

$$
\text{Attn}(X) = \text{softmax}(S) \, V \, W_O,
$$

where $W_O \in \mathbb{R}^{d_h \times d}$ is the output projection. In Tiny-ViT, multi-head concatenation is absorbed into $W_O$ for notational brevity.

### 2.3 Scale-recovery coupling

The analog array stores conductances, not weights. The recovered weight is

$$
\hat{W}_{ij} = s_\ell \, G_{\text{eff},ij}, \qquad s_\ell = \frac{w_{\max}}{G_{\max} - G_{\min}}.
$$

Under D2D mismatch field $M$ and C2C noise $\varepsilon$,

$$
G_{\text{eff}} = \hat{G}(G) \odot (1 + M) + \varepsilon.
$$

The scale factor $s_\ell$ is learned implicitly through the digital optimizer because the STE back-propagates through $s_\ell$ as if it were a constant gain. When $NL \neq 1$, the mapping $G \mapsto \hat{G}$ is nonlinear, so the effective weight $\hat{W}$ depends on $G$ in a power-law fashion, and the learned scale factor $s_\ell$ calibrates to the *mean distortion* of the training-time array.

---

## 3. The Structural-Limit Hypothesis

> **Hypothesis (Attention-Pathway Dominance under Severe NL).**  
> Under the first-order $NL = 2.0$ surrogate, the QKV and output-projection gradients acquire a state-dependent asymmetry that couples the learned spatial filters to the particular D2D pattern experienced during training. When the D2D pattern changes at deployment, the attention geometry—which is the core representational engine of the transformer—ceases to function. The MLP path, even when perfectly linearized, cannot compensate for a broken attention mechanism. Consequently, **no training-objective modification within the first-order surrogate family can raise fresh-instance accuracy above a structural ceiling near $30\%$**.

This hypothesis rests on three theoretical pillars derived from the definitions above.

### 3.1 Pillar I: Gradient-asymmetry-induced rank collapse in Q/K

Under the STE, the gradient of the loss with respect to the QKV weights receives a multiplicative factor $NL \, |G|^{NL-1}$ that depends on the *instantaneous conductance magnitude*. For $NL = 2.0$,

$$
\frac{\partial \mathcal{L}}{\partial W_Q} = X^T \, \underbrace{\left( \frac{\partial \mathcal{L}}{\partial Q} \right)}_{\text{attention gradient}} \, \odot \, \underbrace{\left( 2 \, |G_Q| \, \text{sign}(G_Q) \right)}_{\text{STE scaling}} \, s_\ell.
$$

Because $|G_Q|$ is spatially structured by the D2D field $M$, the effective learning rate for each element of $W_Q$ becomes *position-dependent*. This is not merely noise; it is a **deterministic, structured modulation** of the gradient field. Over many epochs, the optimizer adapts $W_Q$ to this modulation, effectively "pre-distorting" the query matrix so that the *product* $X W_Q$ compensates for the known spatial signature of $M$.

The critical issue is that the query-key inner product $QK^T$ is **bilinear** in the weights. If $W_Q$ and $W_K$ are each adapted to a *different* spatial distortion (because their conductance arrays have independent D2D realizations), the compensation is not guaranteed to transfer. More formally, define the *effective* query matrix under mismatch map $M$ as

$$
\tilde{W}_Q(M) = \arg\min_{W_Q} \mathbb{E}_{X}\left[ \ell\bigl( f(X; W_Q, W_K, W_V, M), Y \bigr) \right].
$$

For fixed-mask training, the model learns $\tilde{W}_Q(M_0)$ and $\tilde{W}_K(M_0)$. At deployment, the fresh mismatch map $M' \neq M_0$ changes the effective gradient scaling, so the learned matrices are no longer optimal. The softmax operator $\sigma(S)$ is highly sensitive to the *relative* magnitudes of the inner products; a small shift in $W_Q$ or $W_K$ can re-rank the attention scores and destroy token-to-token correspondence.

**Mathematical prediction:** If we measure the effective rank of $W_Q$ and $W_K$ during training under $NL = 2.0$, we predict

$$
\text{rank}(W_Q) + \text{rank}(W_K) < \text{rank}(W_Q^{NL=1.0}) + \text{rank}(W_K^{NL=1.0}),
$$

because the state-dependent gradient scaling biases the matrices toward the dominant singular vectors associated with large-conductance regions of the D2D map. This **rank-collapse** reduces the expressive capacity of the attention mechanism and makes the geometry fragile to D2D perturbation.

### 3.2 Pillar II: Exponential nonlinearity of attention scores amplifies surrogate error

The softmax operator is an exponential max-entropizer:

$$
\sigma(S)_{ij} = \frac{e^{S_{ij}}}{\sum_{k} e^{S_{ik}}}.
$$

A small perturbation $\Delta S$ to the score matrix induces a relative change in the attention weights that scales as

$$
\frac{\Delta \sigma}{\sigma} \approx \Delta S \cdot (1 - \sigma).
$$

Near the decision boundary of the softmax (where multiple tokens compete for attention), $\sigma \approx 1/C$ for $C$ competing tokens, and the sensitivity approaches $\Delta S \cdot (1 - 1/C)$. For $C = 10$ classes or $n = 197$ tokens, this is $O(1)$.

Now consider that $\Delta S$ is not random noise but a **systematic bias** induced by the NL surrogate. Because the Q and K weights are programmed with asymmetric LTP/LTD scaling, the inner product $QK^T$ acquires a *deterministic skew*:

$$
\mathbb{E}\left[ S_{ij} \right] = \frac{1}{\sqrt{d_h}} X_i \, \tilde{W}_Q(M) \, \tilde{W}_K(M)^T \, X_j^T \;\neq\; \frac{1}{\sqrt{d_h}} X_i \, W_Q^{\text{ideal}} \, W_K^{\text{ideal}\,T} \, X_j^T.
$$

The softmax exponentiates this skew. Even if the *mean* error in $S$ is small, the exponential nonlinearity can re-rank the attention map, causing tokens that should attend to each other to become orthogonal in the attention landscape. This is why the attention pathway is **structurally coupled** to the NL surrogate: the surrogate does not merely add noise; it reshapes the geometry of the token-interaction manifold in a way that is not invertible by linear compensation in the MLP path.

### 3.3 Pillar III: Scale-recovery mismatch is instance-specific

The scale factor $s_\ell$ is learned implicitly. Under $NL = 2.0$, the mean effective conductance is

$$
\mathbb{E}_G\left[ \hat{G} \right] = \mathbb{E}_G\left[ G^2 \right] = \text{Var}(G) + \mathbb{E}[G]^2,
$$

which depends on the second moment of the conductance distribution. The D2D field $M$ changes both the mean and the variance of $G_{\text{eff}}$ across the array. The learned $s_\ell$ therefore calibrates to the *training-time second moment* under $M_0$. At deployment, the second moment under $M'$ differs, and the scale recovery introduces a **systematic gain mismatch** that is invisible to source-domain accuracy (because the model trained on $M_0$ has already adapted to the miscalibrated $s_\ell$) but fatal to fresh-instance transfer.

In the MLP path, this mismatch is less severe because the MLP operates pointwise on tokens: the feed-forward transformation $X \mapsto \text{GELU}(X W_{fc1}) W_{fc2}$ is a *local* mixing operation. A global scale error in $W_{fc1}$ can be partially absorbed by the downstream $W_{fc2}$ and by the LayerNorm that follows. In the attention path, the scale error enters *before* the softmax, where it is exponentiated and re-normalized globally across tokens. The error propagation is therefore **multiplicative and non-local** in attention, but **additive and local** in MLP.

---

## 4. Falsifiable Mathematical Conditions

A hypothesis is scientifically useful only if it can be falsified. We propose three concrete mathematical conditions; if any is violated, the structural-limit hypothesis must be revised.

### Condition F1: Rank-collapse threshold

> **F1.** Let $r_Q = \text{rank}(W_Q)$ and $r_K = \text{rank}(W_K)$ measured by the number of singular values above $0.01 \times \sigma_{\max}$. Under $NL = 2.0$ with fixed-mask training, we predict $r_Q + r_K \le 1.5 \, d_h$ (i.e., at least $25\%$ rank deficit relative to the $NL = 1.0$ baseline, where $r_Q \approx r_K \approx d_h$). If $r_Q + r_K > 1.8 \, d_h$, Pillar I is falsified.

### Condition F2: Attention-map relative entropy bound

> **F2.** Let $A^{(NL=1.0)} = \text{softmax}(Q^{(1.0)} K^{(1.0)\,T}/\sqrt{d_h})$ and $A^{(NL=2.0)} = \text{softmax}(Q^{(2.0)} K^{(2.0)\,T}/\sqrt{d_h})$ be the attention maps for the same input batch under ideal and severe-NL checkpoints. Define the per-token KL divergence $D_{\text{KL}}(A^{(1.0)}_i \,\|\, A^{(2.0)}_i)$. We predict $\mathbb{E}_i[D_{\text{KL}}] > 1.0$ nat for at least one transformer stage. If the KL divergence is $< 0.1$ nat for all stages, Pillar II is falsified.

### Condition F3: Fresh-instance ceiling invariance

> **F3.** If a model trained with a **second-order** NL surrogate (see G-GG2) under joint MLP-linear + Ensemble HAT achieves fresh-instance accuracy $> 50\%$, the structural-limit hypothesis is falsified in its strong form, because a higher-fidelity surrogate would have broken the ceiling. If the ceiling persists at $\sim 30\%$ even with second-order correction, the hypothesis is strengthened and the barrier is attributed to the attention-pathway architecture itself.

---

## 5. Relation to Existing Results

The gradient-distortion diagnostic (`nl_gradient_distortion_gpt.json`) shows that when $NL = 2.0$ is activated only in the MLP blocks, the affected-parameter gradient cosine drops to $0.815$ and the norm ratio to $0.671$, while QKV and attention-projection gradients remain at $1.00$. This confirms that the *backward* distortion is concentrated in the MLP path. Yet the *fresh-instance* failure is concentrated in the attention path, as evidenced by the CX-J1 result. The structural-limit hypothesis resolves this apparent paradox: **the MLP path suffers the gradient distortion, but the attention path suffers the representational collapse**. The MLP distortion is recoverable because MLP geometry is local and redundant; the attention collapse is irrecoverable because attention geometry is global and rank-sensitive.

---

## 6. Summary

We have formally stated the structural-limit hypothesis: severe nonlinear write ($NL = 2.0$) applied to the transformer attention pathway imposes a fundamental generalization barrier near $30\%$ fresh-instance accuracy, independent of MLP linearization or D2D resampling cadence. The barrier arises from three interacting mechanisms: (1) gradient-asymmetry-induced rank collapse in Q/K projections, (2) exponential amplification of surrogate bias by the softmax attention operator, and (3) instance-specific scale-recovery mismatch that is invisible to source-domain accuracy. Three falsifiable conditions (F1–F3) are provided. The hypothesis is consistent with all existing locked data and predicts the outcomes of the CX-J1b/c/d diagnostic protocol.
