# G-GG4: Why the First-Order Surrogate May Be Insufficient — A Training-Dynamics Position Memo

**Date:** 2026-04-20  
**Author:** Gemini Phase α — Round P2  
**Scope:** Pure theory; training-dynamics analysis and roadmap. No unreported experimental digits.  
**Sources:** `chapter_3_hat_taxonomy.tex`, `chapter_4_failure_modes.tex`, `chapter_5_mitigation.tex`, `nl_gradient_distortion_gpt.json`, `nl_sweep_consolidated_20260417.json`, `joint_mlp_linear_ensemble_hat_full_fresh.json`, `fresh_instance_eval.json`

---

## 1. Position Statement

This memo argues that the first-order nonlinear-write (NL) surrogate, while computationally efficient and sufficient for moderate device non-ideality ($NL \lesssim 1.2$), is **fundamentally inadequate** for training Vision Transformers under severe write nonlinearity ($NL \ge 2.0$). The inadequacy is not a matter of approximation error in a single layer; it is a **training-dynamics pathology** in which the surrogate mismatch compounds across depth, drives the optimizer toward instance-specific attractors, and precludes deployment-grade generalization. The evidence is the convergence of three independent mitigations to the same $\sim 30\%$ fresh-instance ceiling (`chapter_5_mitigation.tex`, Table~`tab:three-mitigation-ceiling`).

The memo is organized as follows. \S2 contrasts ideal fabrication-aware training with surrogate-based training. \S3 analyzes surrogate-error accumulation in deep networks. \S4 discusses why the attention pathway is disproportionately affected. \S5 presents a roadmap of alternative approaches. \S6 summarizes.

---

## 2. Ideal Fabrication-Aware Training vs. Surrogate-Based Training

### 2.1 The ideal

In an ideal world, the training loop would back-propagate through the *actual physical programming sequence*. Let $\mathcal{P}(w; \xi)$ denote the pulse-level programming protocol that maps a target weight $w$ to an effective conductance $G_{\text{eff}}$, where $\xi$ captures all physical state variables (trap occupancy, ion concentration, temperature, history). The ideal training objective is

$$
\theta^\star = \arg\min_\theta \; \mathbb{E}_{M \sim p(M)} \left[ \frac{1}{N} \sum_{n=1}^N \ell\bigl( f(x_n; \theta, \mathcal{P}(\theta; \xi), M), y_n \bigr) \right].
$$

The gradient $\nabla_\theta \mathcal{L}$ would be computed by unrolling the programming protocol $\mathcal{P}$ and differentiating through the physical dynamics. This is **fabrication-aware training** in the strict sense: the optimizer senses exactly the distortion that the deployed weights will experience.

### 2.2 The surrogate compromise

The first-order surrogate replaces $\mathcal{P}$ with a deterministic function $\Phi(G) = |G|^{NL}$ and differentiates via STE:

$$
\nabla_\theta^{\text{surrogate}} \mathcal{L} = \nabla_{\hat{G}} \mathcal{L} \cdot \Phi'(G) \cdot \frac{\partial G}{\partial \theta}.
$$

The compromise has three dimensions:

1. **Functional mismatch:** $\Phi$ is a power law; real organic devices exhibit sub-threshold turn-on, dead zones, and history-dependent hysteresis. The power law is a behavioral fit, not a physical model.
2. **Gradient mismatch:** The STE uses $\Phi'$ instead of the true Jacobian of $\mathcal{P}$. For $NL=2.0$, $\Phi'(G) = 2|G|$; the true Jacobian may involve discontinuous switching thresholds that are nowhere differentiable.
3. **Stochastic mismatch:** The surrogate ignores the variance of $\mathcal{P}$. Real programming is a stochastic process: the same target weight programmed twice yields two different conductances. The surrogate uses only the mean trajectory.

### 2.3 The honesty gap

The canonical V4 checkpoint trained under $NL=1.0$ with Ensemble HAT reaches $86.37 \pm 1.54\%$ fresh-instance accuracy (`fresh_instance_eval.json`). This is the **honest baseline**: the surrogate is exact ($\Phi' = 1$), so the only distortion is D2D mismatch and C2C noise, both of which are faithfully sampled by the resampling protocol. Under $NL=2.0$, the honest baseline would be the accuracy achieved by a model trained with the *true* programming Jacobian. We do not have this number, but the structural-limit hypothesis (G-GG1) predicts that it would still be low because the physical nonlinearity itself deforms the attention geometry. The surrogate is insufficient, but it may not be the *only* insufficiency.

---

## 3. Surrogate-Error Accumulation in Deep Networks

### 3.1 Layer-wise error propagation

Let $L$ be the number of analog-mapped layers (42 in Tiny-ViT V4). Let $\delta_\ell$ be the surrogate-error vector at layer $\ell$, defined as the difference between the true physical gradient and the STE gradient:

$$
\delta_\ell = \nabla_{W_\ell}^{\text{true}} \mathcal{L} - \nabla_{W_\ell}^{\text{surrogate}} \mathcal{L}.
$$

For the first-order NL surrogate, $\delta_\ell$ has a deterministic component (the curvature error $\Phi'' \neq 0$) and a stochastic component (the variance of the physical write process). The magnitude of $\delta_\ell$ depends on the conductance distribution at layer $\ell$, which in turn depends on the training history.

Consider the gradient back-propagation chain. The error in layer $\ell$ contributes to the error in layer $\ell-1$ via the Jacobian of the forward map:

$$
\delta_{\ell-1} \approx J_{\ell-1}^T \, \delta_\ell + \underbrace{\left( \nabla_{W_{\ell-1}}^{\text{true}} \mathcal{L} - J_{\ell-1}^T \, \nabla_{W_\ell}^{\text{true}} \mathcal{L} \right)}_{\text{local surrogate error at } \ell-1},
$$

where $J_{\ell-1} = \partial z_\ell / \partial z_{\ell-1}$ is the layer Jacobian. The total error at the input layer is a sum of weighted local errors:

$$
\delta_1 = \sum_{\ell=1}^{L} \left( \prod_{k=1}^{\ell-1} J_k^T \right) \delta_\ell^{\text{local}}.
$$

This is a **geometric series** in the Jacobian products. If the spectral norm $\|J_k\|_2 > 1$ for any layer, the error from downstream layers is amplified exponentially. Vision Transformers with residual connections are designed to keep $\|J_k\|_2 \approx 1$ in the ideal case, but the NL surrogate introduces *state-dependent* Jacobian norms that can exceed 1 for large conductances.

### 3.2 The depth-scaling law for surrogate bias

Assume each local surrogate error has mean $\mu_\delta$ and covariance $\Sigma_\delta$. Under the simplifying assumption that Jacobians are identity-like (true near initialization for residual networks), the total bias at the input layer scales as

$$
\|\mathbb{E}[\delta_1]\|_2 \lesssim L \, \|\mu_\delta\|_2.
$$

For Tiny-ViT with $L = 42$ analog modules, a $2\%$ per-layer gradient bias compounds to an $84\%$ total bias at the earliest layers. This is a **linear depth scaling** of surrogate error. The actual scaling may be worse if attention layers amplify certain frequency modes (as suggested by the low-rank bias in G-GG1, Pillar I).

The gradient-distortion diagnostic (`nl_gradient_distortion_gpt.json`) provides empirical support. When $NL=2.0$ is applied globally, the affected-parameter gradient cosine is $0.816$ and the norm ratio is $0.676$ relative to the $NL=1.0$ baseline. This means the surrogate gradient is not merely noisy; it is **systematically rotated and scaled** by $\arccos(0.816) \approx 35^\circ$ and compressed by $32\%$. Over 42 layers, a $35^\circ$ rotation per layer does not compose linearly (rotations are non-commutative), but the qualitative implication is clear: the optimizer is descending a gradient field that points in a direction substantially different from the true physical gradient.

### 3.3 Instance-specific attractors

The most severe consequence of surrogate-error accumulation is not merely slow convergence or suboptimal local minima; it is **instance-specific attractor formation**. Under fixed-mask training, the D2D field $M_0$ is fixed, and the surrogate error $\delta_\ell$ is correlated with $M_0$ because the conductance distribution $G_\ell$ adapts to $M_0$ during training. The optimizer therefore descends toward a minimum that is *compatible with the specific spatial signature of $M_0$ and the specific bias of the surrogate*.

When the D2D field changes to $M'$ at deployment, the conductance distribution is different, the surrogate error is different, and the learned weights are no longer near a minimum of the new loss landscape. The model does not merely "see noise"; it has been trained to inhabit a basin that exists only for $M_0$. This is the mechanism behind the $10.00\%$ fixed-mask collapse under D2D mismatch alone, and it is exacerbated under severe NL because the surrogate error is state-dependent and therefore *more tightly coupled* to the D2D pattern.

Ensemble HAT mitigates this for $NL=1.0$ by averaging over D2D instances, but it fails for $NL=2.0$ because the surrogate error is not a zero-mean random variable that averages away; it is a **deterministic, structured bias** that is reproduced (with different spatial patterns) on every fresh instance. The CX-J1 result—$30.53 \pm 7.07\%$ fresh-instance accuracy despite epoch-level resampling—confirms that the bias does not average out (`joint_mlp_linear_ensemble_hat_full_fresh.json`).

---

## 4. Why Attention Pathways Amplify the Insufficiency

The analysis in \S3 applies to any deep network. However, the empirical ceiling is specific to transformers: a pure MLP-Mixer or a deeply nonlinear CNN might tolerate $NL=2.0$ with ensemble resampling (this is CX-J1d in G-GG1). The transformer attention pathway amplifies surrogate insufficiency for three reasons:

1. **Bilinear gradient coupling:** The gradient of the loss with respect to $W_Q$ depends on $W_K$ and vice versa. If the surrogate introduces a bias in $\nabla_{W_Q} \mathcal{L}$, that bias propagates into the update of $W_K$ in the *same* step via the interaction term in the Hessian. The attention parameters are not updated independently; they are coupled through a non-diagonal Fisher information matrix.
2. **Softmax information bottleneck:** The softmax operator collapses the gradient for low-probability tokens to near zero. If the surrogate bias causes the optimizer to learn an attention map that is "too sharp" (i.e., attends to only one or two tokens), the gradient for all other tokens vanishes, and the corresponding weights freeze. This creates a **dead-head** phenomenon analogous to dead ReLUs, but in the attention space.
3. **Residual-stream nonlinearity:** The transformer residual stream $X_{\ell+1} = X_\ell + \text{Attn}(\text{LN}(X_\ell)) + \text{MLP}(\text{LN}(X_\ell + \text{Attn}(\dots)))$ means that the attention output is added directly to the token embeddings. A distorted attention output therefore corrupts the *entire* representation, not just a single feature map. In a CNN, a distorted convolutional kernel affects only the local receptive field; in a transformer, a distorted attention weight affects the global token geometry.

---

## 5. Alternative Roadmap

If the first-order surrogate is insufficient, what are the alternatives? We propose three research directions, ordered by increasing physical fidelity and computational cost.

### 5.1 Direction A: Higher-order behavioral surrogates

As developed in G-GG2, a second-order Taylor-corrected STE or a third-order cumulant expansion can capture curvature and variance without abandoning the differentiable programming framework. The computational cost is modest ($\sim 1.1\times$–$1.5\times$ backward overhead). The key experiment is CX-J1d: if a second-order surrogate breaks the $\sim 30\%$ ceiling, the first-order insufficiency is confirmed and the path forward is surrogate refinement.

**Pros:** Minimal code change; preserves the existing PyTorch training stack.  
**Cons:** Still a behavioral approximation; may fail if the true write response is non-smooth.

### 5.2 Direction B: Iterative programming model

Instead of approximating the write nonlinearity with a closed-form surrogate, explicitly model the programming sequence as an unrolled optimization. Let the target weight vector be $\mathbf{w} \in \mathbb{R}^m$. The programming protocol consists of $T$ write-verify pulses:

```
for t = 1 to T:
    apply pulse vector p_t
    read conductance g_t
    compute error e_t = w_target - s * g_t
    update p_{t+1} = p_t + eta * e_t
```

This is a **closed-loop controller** that can be unrolled and differentiated through the read operations. The backward pass computes $\partial \mathcal{L} / \partial \mathbf{w}_{\text{target}}$ by back-propagating through the unrolled loop, treating each pulse as a layer in a recurrent network.

**Pros:** Physically faithful; captures device history and write-verify dynamics.  
**Cons:** High simulation cost ($T \sim 10$–$100$ pulses per weight update); requires a device model that is differentiable or approximated via neural ODE.

### 5.3 Direction C: Mixed digital-analog training

The most radical alternative is to **remove the attention pathway from the analog domain entirely**. The structural-limit hypothesis (G-GG1) predicts that the attention pathway is the bottleneck. If attention weights are kept in digital FP16/FP32 memory and only the MLP weights are mapped to analog arrays, the severe-NL regime may become tolerable. This is not a training modification but an **architectural partition**:

- Digital: QKV projection, attention score computation, softmax, output projection.
- Analog: MLP fc1, MLP fc2, patch embedding.

The energy and area cost of digital attention is higher than analog attention, but the accuracy cost of analog attention under severe NL may be unacceptable. The trade-off can be quantified by the **energy-accuracy Pareto frontier**.

**Pros:** Bypasses the structural barrier entirely; leverages the observation that MLP-only linearization works.  
**Cons:** Increases digital memory bandwidth; may violate the CIM energy-reduction target ($11.45\times$ in the manuscript).

### 5.4 Selection criteria

The choice among Directions A–C should be guided by the CX-J1b/c/d results:

- If CX-J1d (attention-free architecture) escapes the ceiling, choose **Direction C** with high confidence.
- If CX-J1d fails but CX-J1d-2 (second-order STE) succeeds, choose **Direction A**.
- If both fail, choose **Direction B** as the only physically faithful path remaining.

---

## 6. Summary

The first-order NL surrogate is insufficient for severe nonlinearity because its gradient mismatch compounds linearly (or worse) across the 42 analog modules of Tiny-ViT, drives the optimizer toward instance-specific attractors, and cannot be averaged away by distributional training. The attention pathway amplifies this insufficiency due to bilinear coupling, softmax information bottlenecks, and global residual-stream corruption. Three alternative directions are proposed: higher-order surrogates (cost: $1.5\times$ compute), iterative programming models (cost: $10\times$–$100\times$ compute), and mixed digital-analog training (cost: increased digital area). The CX-J1b/c/d protocol provides a decision tree for selecting among them.
