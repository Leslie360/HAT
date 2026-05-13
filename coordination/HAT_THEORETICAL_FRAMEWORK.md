# HAT Theoretical Framework: PAC-Bayes, Implicit Regularization, and Flat Minima

> Date: 2026-05-13  
> Branch: `107-clean`  
> Status: Draft — mathematical derivations for Paper 2 theoretical section

---

## 1. Problem Setup

We formalize Hardware-Aware Training (HAT) for analog KV cache in LLMs as follows.

### 1.1 Notation

| Symbol | Meaning |
|---|---|
| $w \in \mathbb{R}^d$ | Network weights (frozen after HAT training) |
| $x$ | Input token sequence |
| $K(x), V(x)$ | Key/value states produced by clean digital forward pass |
| $\tilde{K}(x), \tilde{V}(x)$ | Analog-noise-corrupted KV states |
| $\mathcal{L}(w; x)$ | Per-sample loss (negative log-likelihood) |
| $\hat{\mathcal{L}}_S(w)$ | Empirical loss on training set $S$ of size $n$ |
| $\mathcal{L}_\mathcal{D}(w)$ | Population loss under data distribution $\mathcal{D}$ |
| $\sigma_\text{c2c}, \sigma_\text{d2d}$ | Cycle-to-cycle and device-to-device noise stddev |

### 1.2 Analog KV Noise Model

During HAT training, the KV cache of the target layer(s) is replaced by analog memory. Each read injects:

$$
\tilde{K} = K + \underbrace{\epsilon_\text{d2d}}_{\text{fixed per-cell}} + \underbrace{\epsilon_\text{c2c}}_{\text{random per-read}}, \qquad \epsilon_\text{d2d} \sim \mathcal{N}(0, \sigma_\text{d2d}^2 I), \quad \epsilon_\text{c2c} \sim \mathcal{N}(0, \sigma_\text{c2c}^2 I)
$$

The forward pass therefore computes a **stochastic loss**:

$$
\tilde{\mathcal{L}}(w; x) = \mathcal{L}(w; x, \tilde{K}, \tilde{V})
$$

HAT minimizes the **expected noisy loss**:

$$
\min_w \; \mathbb{E}_{\epsilon_\text{c2c}, \epsilon_\text{d2d}} \big[ \tilde{\mathcal{L}}(w; x) \big]
$$

Because the noise is injected only into the KV cache (not into the weight matrices), the randomness is **conditional on the data path**, not on the weights themselves. This makes the analysis slightly different from standard weight-noise regularization, but the same Taylor-expansion tools apply.

> **Implementation note.** The actual codebase injects noise in the *conductance domain* (differential pair of memristor crossbars) with per-head dynamic scaling. After the forward mapping $K \to G \to \tilde{G} \to \tilde{K}$, the effective noise variance in KV space is proportional to $\text{scale}^2$, where $\text{scale}$ is the per-head max-norm of the clean KV tensor. Thus the real noise is **heteroscedastic** (signal-dependent). The additive isotropic model above is an *idealization* that captures the dominant first-order behavior and makes the analysis tractable. All derivations below should be understood as applying to this idealized model; the qualitative conclusions (flatness-seeking, Hessian trace penalty) carry over to the full conductance-domain implementation.

---

## 2. PAC-Bayesian Generalization Bound

### 2.1 Standard PAC-Bayes (McAllester 1999; Dziugaite & Roy 2017)

For any prior $P$ over weights (independent of training data) and any posterior $Q$ over weights (which may depend on $S$), with probability at least $1-\delta$ over the draw of $S$:

$$
\mathbb{E}_{w \sim Q}\big[\mathcal{L}_\mathcal{D}(w)\big] \;\le\; \mathbb{E}_{w \sim Q}\big[\hat{\mathcal{L}}_S(w)\big] \;+\; \sqrt{\frac{\mathrm{KL}(Q \| P) + \ln \frac{2\sqrt{n}}{\delta}}{2n}}
$$

### 2.2 How HAT Satisfies the Flat-Minimum Condition

The tightness of the bound depends on $\mathrm{KL}(Q \| P)$. If $Q$ is concentrated in a **small neighborhood** where the loss is approximately flat, then $\mathrm{KL}(Q \| P)$ is small and the bound is tight.

**HAT enforces exactly this.** By training with KV noise, the optimizer is forced to find weights $w^*$ such that:

$$
\mathcal{L}(w^*; x, K + \delta K, V + \delta V) \approx \mathcal{L}(w^*; x, K, V)
$$

for typical perturbations $\delta K, \delta V$ induced by $\sigma_\text{c2c}, \sigma_\text{d2d}$. In other words, $w^*$ lives in a **flat basin** of the loss landscape with respect to KV perturbations.

### 2.3 From Data-Path Noise to Weight-Posterior Flatness

Consider the deterministic digital network with weights $w$ and a **linear approximation** of the attention output with respect to KV perturbations:

$$
o(w; x, \tilde{K}, \tilde{V}) = o(w; x, K, V) + J_K \cdot \delta K + J_V \cdot \delta V + O(\|\delta\|^2)
$$

where $J_K = \frac{\partial o}{\partial K}$ and $J_V = \frac{\partial o}{\partial V}$ are the Jacobians of the attention output w.r.t. KV states. If HAT training succeeds, it must have learned weights for which $J_K$ and $J_V$ are **small in operator norm** — otherwise the perturbation would propagate and explode.

This means HAT is implicitly solving:

$$
\min_w \; \hat{\mathcal{L}}_S(w) \;+\; \lambda \big( \|J_K(w)\|_F^2 + \|J_V(w)\|_F^2 \big)
$$

which is precisely a **Jacobian regularization** objective. Small Jacobians imply flat loss landscape along the KV directions. 

> **Note:** The step from "KV-direction flatness" to "weight-direction flatness" is an *intuitive argument*, not a strict equivalence. Weight perturbations $\delta w$ affect the loss through $\delta K = \frac{\partial K}{\partial w}\delta w$, and HAT only directly penalizes $\frac{\partial \mathcal{L}}{\partial K}$. In practice, the coupling between weight and KV Hessians through the network layers means minimizing one tends to reduce the other (see also the SAM discussion in §4).

Therefore, a posterior $Q$ concentrated around $w^*$ will have:
- Small empirical loss (by construction)
- Small KL divergence (because the neighborhood is flat, so $Q$ need not be broad)
- Tight PAC-Bayes bound

**Interpretation:** HAT finds a weight configuration that is robust to KV perturbations; this robustness translates into a flat minimum; the flat minimum yields a tight PAC-Bayes generalization bound; therefore HAT generalizes well.

---

## 3. Noise Injection as Implicit Regularization

### 3.1 Taylor Expansion of Noisy Loss

Write the noisy KV states as $\tilde{K} = K + \epsilon$ where $\epsilon \sim \mathcal{N}(0, \sigma^2 I)$ (we combine C2C and D2D for simplicity). Expand the loss to second order:

$$
\tilde{\mathcal{L}}(w; x) = \mathcal{L}(w; x) + \nabla_{K,V}\mathcal{L}^\top \epsilon + \frac{1}{2} \epsilon^\top H_{K,V} \epsilon + O(\|\epsilon\|^3)
$$

where $H_{K,V} = \nabla^2_{K,V} \mathcal{L}$ is the Hessian w.r.t. KV states.

> **Validity of the expansion.** The actual forward function includes clamping (`clamp(-R, R)`), STE quantization, and per-head scale normalization, all of which introduce non-smooth or non-differentiable points. The expansion above is therefore a *simplified local approximation* that is valid away from clamping boundaries and treats quantization as a small perturbation. The Hessian $H_{K,V}$ in this context is the Hessian of the *smooth idealized* loss, not the true piecewise-constant Hessian of the STE-quantized network. Nevertheless, the leading-order correction $\frac{\sigma^2}{2}\mathrm{tr}(H)$ correctly captures the qualitative behavior: noise-averaging penalizes high curvature.

### 3.2 Expectation over Noise

Taking expectation over $\epsilon$:

$$
\mathbb{E}_\epsilon[\tilde{\mathcal{L}}] = \mathcal{L} + \underbrace{\frac{\sigma^2}{2} \mathrm{tr}(H_{K,V})}_{\text{Hessian-trace penalty}} + O(\sigma^4)
$$

The first-order term vanishes because $\mathbb{E}[\epsilon]=0$. The dominant correction is proportional to the **trace of the KV Hessian**.

Minimizing $\mathbb{E}_\epsilon[\tilde{\mathcal{L}}]$ therefore **penalizes large curvature** in the KV directions. This is a strong regularizer: it forces the network to avoid regions where small KV perturbations cause large loss changes.

### 3.3 Connection to Jacobian Norm (Variance / Gradient Stability)

Using the chain rule on the first-order term (before expectation):

$$
\nabla_{K,V}\mathcal{L} = \underbrace{\frac{\partial o}{\partial (K,V)}}_{J_{K,V}} \cdot \underbrace{\frac{\partial \mathcal{L}}{\partial o}}_{\nabla_o \mathcal{L}}
$$

Although the first-order term vanishes in expectation, it contributes to the **variance** of the noisy loss:

$$
\mathrm{Var}_\epsilon\big[ \tilde{\mathcal{L}} \big] \;=\; \mathbb{E}_\epsilon\big[ (\nabla_{K,V}\mathcal{L}^\top \epsilon)^2 \big] + O(\sigma^4) \;=\; \sigma^2 \|\nabla_{K,V}\mathcal{L}\|^2 + O(\sigma^4) \;=\; \sigma^2 \|J_{K,V}^\top \nabla_o \mathcal{L}\|^2 + O(\sigma^4)
$$

During SGD, the stochastic gradient w.r.t. weights is $\nabla_w \tilde{\mathcal{L}} = \nabla_w \mathcal{L} + \nabla_w(\nabla_{K,V}\mathcal{L}^\top \epsilon) + \dots$. The variance of this stochastic gradient therefore contains a term proportional to $\|J_{K,V}^\top \nabla_o \mathcal{L}\|^2$. Thus HAT training not only minimizes the expected loss, but also **suppresses gradient variance** through the KV cache. Small Jacobians mean:
- More stable optimization (low gradient noise)
- More robust inference (KV perturbations do not amplify through the network)

### 3.4 Why HAT Improves Clean Digital Performance

The implicit regularizers above do not depend on the analog hardware being present at inference time. They act on the **weight matrices** during training. Therefore, even when the analog patch is removed (digital inference), the weights still enjoy:
- Small KV Jacobians → stable representations
- Small KV Hessian trace → flat minimum
- Tight PAC-Bayes bound → good generalization

This explains the experimental observation that HAT-trained checkpoints achieve **better clean-digital PPL than the original pretrained model** (e.g., 410M: 22.18 → 18.75 after 500-step HAT).

---

## 4. Connection to SAM (Sharpness-Aware Minimization)

SAM (Foret et al., ICLR 2021) solves:

$$
\min_w \max_{\|\epsilon\|_2 \le \rho} \mathcal{L}(w + \epsilon)
$$

HAT solves (in expectation):

$$
\min_w \mathbb{E}_{\epsilon \sim \mathcal{N}(0, \sigma^2)} \big[ \mathcal{L}(w; x, K+\epsilon, V+\epsilon) \big]
$$

**Key difference:** SAM perturbs **weights** adversarially; HAT perturbs **activations (KV cache)** stochastically.

**Key similarity:** Both biases toward flat minima. SAM does so by explicitly minimizing the worst-case loss in a weight ball. HAT does so by minimizing the average loss over KV noise realizations. In a locally quadratic approximation:

- SAM penalizes the **largest eigenvalue** of the weight Hessian (sharpness)
- HAT penalizes the **trace of the KV Hessian** (average curvature)

Both are flatness-seeking objectives. Because the weight Hessian and the KV Hessian are coupled through the network's layers, minimizing one tends to reduce the other. Thus HAT can be viewed as a **stochastic, activation-space analog of SAM** that is naturally compatible with memristor inference.

### 4.1 SAM vs HAT: Computational Cost

| Method | Forward passes per step | Perturbation target | Inference compatibility |
|---|---|---|---|
| SAM | 2× (w and w+ε) | Weights | Requires digital weights |
| HAT | 1× | KV activations | Runs on analog hardware |

HAT is cheaper per step (no double forward) and produces weights that can be deployed directly on analog accelerators without conversion.

---

## 5. Interpretation of Experimental Results

### 5.1 Scale Trend (410M → 1B → 2.8B → 6.9B)

As model width $h$ increases, the KV Jacobian $J_{K,V} \in \mathbb{R}^{h \times h}$ is effectively averaged over more dimensions. Under random initialization, the operator norm scales roughly as $O(1/\sqrt{h})$, and HAT training further suppresses it. This yields the *heuristic* scaling:

$$
\text{Analog noise overhead} \propto \|J_{K,V}\|^2 \cdot \sigma^2 \sim O(1/h)
$$

**Larger models tolerate more noise** — consistent with the observed monotonic trend (410M +0.42 PPL → 2.8B +0.10 PPL at D2D=0.02). We note this is a post-hoc intuition rather than a rigorous bound for pretrained networks.

### 5.2 Retention Noise

In addition to C2C and D2D noise, the analog memristor array exhibits **retention decay**: stored conductance values drift over time following a double-exponential profile

$$
G(t) = G_\min + (G(0) - G_\min) \cdot \bigl(A_1 e^{-t/\tau_1} + A_2 e^{-t/\tau_2} + A_0\bigr)
$$

where $A_0$ is the persistent fraction and $\tau_1, \tau_2$ are short- and long-term time constants. In the KV cache, earlier tokens (stored longer) experience stronger decay than recent tokens. This introduces a **structured, time-dependent perturbation** that is qualitatively different from the isotropic Gaussian model above. The Taylor expansion still applies locally, but the effective "noise" is now correlated across sequence positions and asymmetric in time. Our experiments (R1-RET) show that retention noise up to realistic levels ($\sim 1\%$ drift) has minimal impact on PPL, because HAT training already learns weights that are robust to slow conductance drift.

### 5.4 Adaptive Schedules

A fixed noise level throughout training applies the same regularization strength at all times. But:
- Early training: weights are far from optimum; large noise helps escape sharp regions
- Late training: weights are near optimum; small noise allows fine-tuning without disturbing convergence

The **cosine schedule** implements exactly this intuition:

$$
\sigma_\text{c2c}(t) = \sigma_0 \cdot \Bigl(0.1 + 0.45 \bigl(1 + \cos(\pi t / T)\bigr)\Bigr)
$$

which is large at $t=0$ (exploration, $\sigma_\text{c2c}=\sigma_0$) and small at $t=T$ (exploitation, $\sigma_\text{c2c}=0.1\sigma_0$). The 10\% floor prevents the regularizer from vanishing completely, which we found empirically stabilizes late-stage fine-tuning. This is analogous to learning-rate scheduling, but acting on the **regularization strength** instead of the step size.

### 5.5 Layer-Wise Schedule

Deeper layers have larger KV caches (same dimension but more tokens attended to), so analog noise at deeper layers contributes more to the trace penalty. The layer-wise schedule linearly increases noise with depth:

$$
\sigma_\text{c2c}^{(\ell)} = \sigma_0 \cdot \Bigl(0.5 + \frac{\ell}{L - 1}\Bigr)
$$

For a model with $L$ layers (indexed $0,\dots,L-1$), this gives a range of $[0.5\sigma_0,\, 1.5\sigma_0]$, concentrating regularization where the analog area savings are largest (last layers). This matches the experimental finding that last1 selective KV is optimal.

The **reverse layer-wise** schedule flips the depth dependence:

$$
\sigma_\text{c2c}^{(\ell)} = \sigma_0 \cdot \Bigl(1.5 - \frac{\ell}{2(L - 1)}\Bigr)
$$

which assigns *more* noise to early layers and less to late layers. Our experiments show this performs worse than standard layer-wise (410M reverse = 21.30 vs. layer-wise = 18.36), confirming that regularizing late layers is more effective.

---

## 6. Open Questions for Future Work

1. **Non-Gaussian noise:** Real RRAM/PCM/FeFET noise is non-Gaussian (log-normal, asymmetric). How does the implicit regularizer change under non-Gaussian perturbations?
2. **Multi-layer analog:** Our analysis treats each layer independently. What is the cross-layer coupling of KV Jacobians when multiple layers are analogized?
3. **Dynamical systems view:** Can we bound the Lyapunov exponent of the attention recurrence under KV noise, guaranteeing stable long-horizon generation?
4. **PAC-Bayes with data-dependent priors:** Dziugaite & Roy (2018) show that using the SGD trajectory as a prior can yield non-vacuous bounds for deep nets. Can we instantiate this with HAT's noise trajectory?

---

## 7. References

All citations below are real and verified; see `coordination/literature_citations_paper2.md` for full bibliographic details.

1. **McAllester (1999)** — PAC-Bayesian theorems. *Machine Learning.*
2. **Dziugaite & Roy (2017)** — Non-vacuous generalization bounds for deep nets via PAC-Bayes optimization.
3. **Dziugaite & Roy (2018)** — Data-dependent PAC-Bayes priors via differential privacy. *NeurIPS.*
4. **Hochreiter & Schmidhuber (1997)** — Flat Minima. *Neural Computation.*
5. **Keskar et al. (2017)** — On large-batch training and sharp minima.
6. **Foret et al. (2021)** — Sharpness-Aware Minimization. *ICLR.*
7. **Camuto et al. (2020)** — Explicit regularisation in Gaussian noise injections. *NeurIPS.*
8. **Lim et al. (2021)** — Noisy Recurrent Neural Networks: hidden-state noise penalizes Jacobians. *NeurIPS.*
9. **Dhifallah & Lu (2021)** — Inherent regularization effects of noise injection.
10. **Baek et al. (2024)** — Why is SAM robust to label noise?

---

*Document status: Draft — core derivations complete. Pending: numerical sanity checks against 410M loss curves, and cross-reference with exact experimental configs.*
