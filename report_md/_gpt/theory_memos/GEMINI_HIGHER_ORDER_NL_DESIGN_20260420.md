# G-GG2: Higher-Order Nonlinear-Write Surrogate Design

**Date:** 2026-04-20  
**Author:** Gemini Phase α — Round P2  
**Scope:** Pure theory; proposed mathematical forms and implementation paths. No unreported experimental digits.  
**Sources:** `chapter_5_mitigation.tex`, `run_tinyvit_groupwise_nl_comp.py`, `nl_mitigation_summary_20260418.json`, `nl_gradient_distortion_gpt.json`, `joint_mlp_linear_ensemble_hat_full_fresh.json`

---

## 1. The Limitations of the First-Order Surrogate

The current hardware-aware training (HAT) framework models nonlinear write as a deterministic power-law mapping of the target conductance $G$ to the effective conductance $\hat{G}$:

$$
\hat{G} = \Phi(G) = \text{sign}(G) \, |G|^{NL},
$$

with a straight-through estimator (STE) for the backward pass:

$$
\frac{\partial \hat{G}}{\partial G}\bigg|_{\text{STE}} = \Phi'(G) = NL \, |G|^{NL-1}.
$$

For $NL = 1.0$, $\Phi$ is the identity and the STE is exact. For $NL = 2.0$, the STE is a first-order approximation that ignores curvature. The limitation is not merely that $\Phi''(G) \neq 0$; it is that the **higher-order derivatives encode physical information about the write process** that the first-order surrogate discards.

Specifically, the first-order surrogate makes three implicit assumptions that break down under severe nonlinearity:

1. **Local linearity:** The STE assumes that the gradient of the loss with respect to $G$ is well-approximated by scaling the ideal gradient by $\Phi'(G)$. This is valid only when the loss landscape is locally linear over the scale of the nonlinearity.
2. **Symmetry preservation:** The STE treats LTP and LTD as mirror-symmetric branches because the magnitude scaling $|G|^{NL-1}$ is the same for both polarities. Real organic devices exhibit *asymmetric* LTP/LTD curvature (different exponents, different threshold voltages, different ion-migration dynamics).
3. **Determinism:** The surrogate ignores cycle-to-cycle (C2C) variance in the write nonlinearity itself, treating $NL$ as a fixed scalar rather than a stochastic process $NL(G, \xi)$ where $\xi$ is a per-pulse noise source.

The empirical cost of these approximations is visible in the fresh-instance ceiling: joint MLP-linear + Ensemble HAT (CX-J1) reaches $91.36\%$ source-domain accuracy but only $30.53 \pm 7.07\%$ fresh-instance (`joint_mlp_linear_ensemble_hat_full_fresh.json`). The source-domain rescue is excellent because the optimizer can exploit the deterministic bias of the first-order surrogate; the fresh-instance collapse occurs because that bias is instance-specific and non-transferable.

---

## 2. A Second-Order Surrogate: Taylor-Corrected STE

### 2.1 Mathematical form

Let the true write function be $\Phi(G)$, now treated as a smooth nonlinear map with at least two continuous derivatives. Instead of the first-order STE, we propose a **Taylor-corrected STE** that propagates a second-order correction to the gradient:

$$
\frac{\partial \hat{G}}{\partial G}\bigg|_{\text{STE-2}} = \Phi'(G) + \frac{1}{2} \, \Phi''(G) \, \Delta G_{\text{eff}},
$$

where $\Delta G_{\text{eff}}$ is an effective perturbation scale that captures the typical curvature-sensing distance. In the context of crossbar programming, a natural choice is

$$
\Delta G_{\text{eff}} = \sigma_{\text{D2D}} \, (G_{\max} - G_{\min}) + \sigma_{\text{C2C}} \, |G|,
$$

i.e., the sum of the device-to-device spread and the state-dependent cycle-to-cycle noise. The second-order STE then becomes

$$
\boxed{
\frac{\partial \hat{G}}{\partial G}\bigg|_{\text{STE-2}} = NL \, |G|^{NL-1} + \frac{1}{2} \, NL(NL-1) \, |G|^{NL-2} \, \Delta G_{\text{eff}} \, \text{sign}(G)
}
$$

for $G \neq 0$, with a regularized limit at $G = 0$.

### 2.2 Interpretation

The first term is the original STE. The second term is a **curvature correction** that accounts for the fact that the gradient of the loss is evaluated over a neighborhood of $G$, not at a single point. When $NL = 2.0$, the correction simplifies to $\Delta G_{\text{eff}}$, a constant offset independent of $G$. This means the second-order surrogate adds a *state-independent bias* to the gradient scaling that is proportional to the noise floor. Intuitively, it tells the optimizer: "Because the write is curved, a small change in the target conductance produces a non-linearly amplified change in the effective conductance, and you must account for the width of the noise cloud."

### 2.3 Asymmetric branch extension

Real organic synaptic transistors often exhibit stronger nonlinearity in one polarity. Let $NL_{\text{LTP}}$ and $NL_{\text{LTD}}$ be the exponents for the two branches, and let $\kappa = NL_{\text{LTP}} - |NL_{\text{LTD}}|$ be the asymmetry. The second-order surrogate generalizes to

$$
\frac{\partial \hat{G}}{\partial G}\bigg|_{\text{STE-2, asym}} = 
\begin{cases}
NL_{\text{LTP}} |G|^{NL_{\text{LTP}}-1} + \frac{1}{2} NL_{\text{LTP}}(NL_{\text{LTP}}-1) |G|^{NL_{\text{LTP}}-2} \Delta G_{\text{eff}} & G > 0, \\[6pt]
|NL_{\text{LTD}}| |G|^{|NL_{\text{LTD}}|-1} + \frac{1}{2} |NL_{\text{LTD}}|(|NL_{\text{LTD}}|-1) |G|^{|NL_{\text{LTD}}|-2} \Delta G_{\text{eff}} & G < 0.
\end{cases}
$$

The asymmetry $\kappa$ now enters both the first- and second-order terms, and the optimizer can sense the differential curvature between potentiation and depression. This is physically motivated: organic electrochemical devices often exhibit faster ion insertion (LTP) than extraction (LTD), leading to not only different exponents but different *second derivatives*.

---

## 3. Higher-Order Surrogate: Stochastic Programming Model

### 3.1 Beyond deterministic power laws

The power-law model $\Phi(G) = |G|^{NL}$ is a behavioral fit, not a physical law. A more faithful surrogate can be derived from a **stochastic programming model** that treats each weight update as a pulse sequence. Let $N_p$ be the number of programming pulses, and let each pulse induce a conductance increment $\Delta g_k$ drawn from a state-dependent distribution:

$$
\Delta g_k \sim p\bigl(\Delta g \,|\, g_{k-1}, V_p, t_p\bigr),
$$

where $V_p$ and $t_p$ are the pulse voltage and duration. The cumulative conductance after $N_p$ pulses is

$$
g_{N_p} = g_0 + \sum_{k=1}^{N_p} \Delta g_k.
$$

The first-order surrogate approximates the *mean* trajectory $E[g_{N_p}]$ by a power law. A higher-order surrogate should approximate the *variance* and *skewness* of the terminal conductance distribution.

### 3.2 Cumulant expansion

Expand the terminal conductance distribution in cumulants:

$$
\mathbb{E}\left[ \hat{G} \right] = \mu_1(G), \quad \text{Var}\left[ \hat{G} \right] = \mu_2(G), \quad \text{Skew}\left[ \hat{G} \right] = \mu_3(G).
$$

The forward pass uses the mean $\mu_1(G)$. The backward pass uses a **cumulant-corrected STE**:

$$
\frac{\partial \mathcal{L}}{\partial G} = \frac{\partial \mathcal{L}}{\partial \hat{G}} \cdot \mu_1'(G) + \frac{1}{2} \frac{\partial^2 \mathcal{L}}{\partial \hat{G}^2} \cdot \mu_2'(G) + \frac{1}{6} \frac{\partial^3 \mathcal{L}}{\partial \hat{G}^3} \cdot \mu_3(G).
$$

This is a **stochastic generalization of the STE** that propagates not only the first derivative but also the sensitivity of the loss to variance and skewness. For a cross-entropy loss, $\partial^2 \mathcal{L} / \partial \hat{G}^2$ is related to the Fisher information, so the second term acts as an **information-regularizing** gradient that discourages conductance states with high programming variance.

---

## 4. Computational Cost and Implementation Path

### 4.1 Cost analysis

The first-order STE requires one additional multiplication per weight during backpropagation: $\nabla_G \mathcal{L} = \nabla_{\hat{G}} \mathcal{L} \times \Phi'(G)$. The second-order STE requires:

1. One multiplication for $\Phi'(G)$.
2. One multiplication and one addition for $\frac{1}{2}\Phi''(G)\Delta G_{\text{eff}}$.
3. One additional multiply-add to combine the terms.

The per-weight FLOP increase is approximately $2\times$ during the backward pass. For Tiny-ViT V4, which has $\sim 5.8 \times 10^6$ parameters of which $\sim 4.2 \times 10^6$ are analog-mapped, the backward-pass overhead is negligible compared to the forward-pass cost of the attention mechanism ($O(n^2 d)$ per layer).

The cumulant expansion (third-order) requires computing $\partial^2 \mathcal{L} / \partial \hat{G}^2$, which is a Hessian-vector product. This can be obtained via **double backward** in PyTorch:

```python
grad_hat = torch.autograd.grad(loss, hat_G, create_graph=True)[0]
grad_G_first = grad_hat * phi_prime(G)
grad_G_second = 0.5 * grad_hat * phi_double_prime(G) * delta_G_eff
# For cumulant term, need second derivative of loss:
hessian_term = torch.autograd.grad(grad_hat.sum(), hat_G, retain_graph=True)[0]
```

The double-backward increases memory by $\sim 1.5\times$ because the computation graph must be retained through the first backward pass. For a 100-epoch training run with batch size 64 on CIFAR-10, this is feasible on a single consumer GPU (24 GB VRAM).

### 4.2 Integration into `train_tinyvit_ensemble.py`

The existing group-wise NL wrapper (`run_tinyvit_groupwise_nl_comp.py`) sets `module.config.NL_LTP` and `module.config.NL_LTD` per analog module. To accommodate the second-order surrogate, we propose the following minimal extension:

1. **Add configuration fields** to the analog layer config:
   - `use_second_order_ste: bool = False`
   - `delta_g_eff: float = sigma_d2d + sigma_c2c` (auto-populated from the experiment config)
   - `use_cumulant_ste: bool = False`

2. **Modify the backward hook** in `AnalogLinear` / `AnalogConv2d`:
   ```python
   if config.use_second_order_ste:
       phi_prime = config.NL_LTP * torch.abs(g) ** (config.NL_LTP - 1)
       phi_double_prime = config.NL_LTP * (config.NL_LTP - 1) * torch.abs(g) ** (config.NL_LTP - 2)
       correction = 0.5 * phi_double_prime * config.delta_g_eff
       grad_input = grad_output * (phi_prime + correction)
   else:
       grad_input = grad_output * phi_prime
   ```

3. **Preserve the group-wise override mechanism** from `run_tinyvit_groupwise_nl_comp.py`. The `make_groupwise_setter` function can be extended to propagate `use_second_order_ste` to protected and unprotected groups independently, enabling experiments such as "second-order STE in attention, first-order in MLP."

### 4.3 Activation check-pointing for memory

If the cumulant expansion (third-order) is enabled, the double-backward memory cost can be mitigated by **activation checkpointing** the analog layers. Because the analog layers are linear projections (no intra-layer nonlinearity), checkpointing them adds only the cost of one extra forward pass per layer during backpropagation, not the quadratic cost of attention checkpointing.

---

## 5. Experimental Design to Inform CX-J1d

### 5.1 CX-J1d: Second-order STE under joint MLP-linear + Ensemble HAT

The structural-limit hypothesis (G-GG1) predicts that the $\sim 30\%$ fresh-instance ceiling is a property of the first-order surrogate interacting with the attention pathway. CX-J1d should test whether a higher-order surrogate breaks this ceiling.

**Protocol:**

| Lane | MLP NL | Attention NL | D2D cadence | STE order | Purpose |
|---|---|---|---|---|---|
| CX-J1d-1 | 1.0 | 2.0 | Epoch | First-order | Replicate CX-J1 baseline |
| CX-J1d-2 | 1.0 | 2.0 | Epoch | Second-order | Test curvature correction |
| CX-J1d-3 | 1.0 | 2.0 | Epoch | Cumulant (3rd) | Test variance sensitivity |
| CX-J1d-4 | 1.0 | 1.5 | Epoch | Second-order | Test moderate-NL benefit |

**Predictions:**
- If the structural-limit hypothesis is correct, CX-J1d-2 and CX-J1d-3 will not exceed $50\%$ fresh-instance accuracy, because the barrier is architectural (attention-pathway dominance), not merely a gradient-approximation error.
- If the barrier is *only* a gradient-approximation error, CX-J1d-2 should show a measurable lift ($> 10$ pp) in fresh-instance mean relative to CX-J1d-1.
- CX-J1d-4 provides a sanity check: at $NL = 1.5$, the second-order correction should be smaller (because $\Phi'' \propto NL(NL-1)$ vanishes at $NL=1$), so the gap between first- and second-order should shrink.

### 5.2 Diagnostic gradients to log

For each training step, log the following quantities in `wandb` or a JSON stream:

1. **Layer-wise effective gradient scaling:** $\langle \Phi'(G) \rangle$ and $\langle \Phi''(G) \Delta G_{\text{eff}} \rangle$ per analog module.
2. **Attention-map KL divergence:** $D_{\text{KL}}(A^{(t)} \,\|\, A^{(t-1)})$ between consecutive epochs, averaged over a fixed validation batch. A collapsing KL indicates attention-map instability.
3. **Q/K rank trajectory:** Effective rank of $W_Q$ and $W_K$ per layer, computed via SVD on a CPU callback every 10 epochs.
4. **Fresh-instance variance:** After training, evaluate on 10 fresh D2D instances with 5 MC runs each, as in the canonical protocol.

### 5.3 Compute budget estimate

- CX-J1d-1: 100 epochs $\times$ 64 batch $\times$ CIFAR-10 $\approx$ 6 hours on RTX 4090.
- CX-J1d-2: Same wall time; backward pass is $\sim 1.1\times$ slower due to the extra multiply-add.
- CX-J1d-3: $\sim 1.5\times$ slower due to double-backward; $\sim$ 9 hours.
- Total for four lanes: $\sim$ 30 GPU-hours, well within a single-node budget.

---

## 6. Risk Assessment and Fallbacks

**Risk 1: Numerical instability at $G \approx 0$.**  
The term $|G|^{NL-2}$ diverges for $NL < 2$ as $G \to 0$. Mitigation: clip $|G|$ to $\epsilon = 10^{-4}$ before evaluating the second derivative.

**Risk 2: The second-order correction is too small to matter.**  
For $NL = 2.0$ and typical conductances $|G| \sim 0.5$ (normalized), $\Phi'(G) = 1.0$ and $\Phi''(G) = 2.0$. With $\Delta G_{\text{eff}} \sim 0.1$, the correction is $0.1$, i.e., $10\%$ of the first-order term. This is small but not negligible; it may accumulate over depth.

**Risk 3: The true physical nonlinearity is not smooth.**  
If the write response is piecewise-linear or has a dead zone, the Taylor expansion is invalid. Fallback: replace the Taylor correction with a **lookup-table STE** that interpolates $\Phi'(G)$ and $\Phi''(G)$ from a pre-characterized grid. This trades differentiability for physical fidelity and can be made differentiable via soft interpolation.

---

## 7. Summary

The first-order NL surrogate is a local linearization that discards curvature, asymmetry, and stochasticity. We have designed a second-order Taylor-corrected STE and a third-order cumulant expansion that reintroduce these effects at modest computational cost ($\sim 1.1\times$ and $\sim 1.5\times$ backward overhead, respectively). The implementation path requires only minor extensions to the existing `AnalogLinear`/`AnalogConv2d` backward hooks and the group-wise override mechanism in `run_tinyvit_groupwise_nl_comp.py`. The proposed CX-J1d experiment directly tests whether the $\sim 30\%$ fresh-instance ceiling is a first-order artifact or a deeper structural property of the attention pathway.
