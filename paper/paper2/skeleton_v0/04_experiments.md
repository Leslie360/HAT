# §4 Experimental Design

This section describes the six core experiments that constitute the CX-J diagnostic protocol. All experiments are designed to be executable within the existing compute-ViT PyTorch stack; no new simulators, model families, or dataset requirements are introduced. Each experiment is accompanied by a pre-registered prediction derived from the structural-limit hypothesis. The experiments form a **falsification lattice**: if the hypothesis is correct, E1–E4 should converge on the $\sim 30\%$ ceiling, E5 should escape to deployment-grade accuracy, and E6 should reveal rank collapse. If any experiment violates its prediction, the hypothesis is refined in a direction specified in advance.

## 4.1 Experiment E1: CX-J1b — QKV-Only Linearization + Ensemble HAT

**Research question.** Is the $\sim 30\%$ fresh-instance ceiling localized to the QKV projection specifically, or to the attention pathway as a whole? If QKV-only linearization breaks the ceiling, the structural bottleneck is the QKV-to-output-projection interaction.

**Method.** Using the group-wise selector, the `.attn.qkv` layers are designated as the protected group and receive the linear surrogate ($\text{NL}_{\text{LTP}}=1.0$, $\text{NL}_{\text{LTD}}=-1.0$). All other analog layers (`.attn.proj`, `.mlp.fc1`, `.mlp.fc2`, `patch_embed.*`) retain the severe-NL surrogate ($\text{NL}=2.0$). Training follows the ensemble HAT recipe: per-epoch D2D resampling, $100$ epochs, AdamW with cosine annealing, cold start from the ImageNet-pretrained Tiny-ViT-5M checkpoint. Evaluation uses the canonical fresh-instance protocol ($10$ instances × $5$ MC passes).

**Pre-registered prediction.** Under the attention-pathway-dominance hypothesis, QKV-only linearization is predicted to stay near the $\sim 30\%$ ceiling. Linearizing QKV in isolation creates a decoupled optimization: QKV receives clean gradients while the attention output projection receives distorted gradients. The optimizer adapts $W_{V}$ and $W_{O}$ to a distortion that $W_{Q}$ and $W_{K}$ do not sense, tearing the attention mechanism between incompatible objectives. Adding ensemble HAT resampling does not fix this decoupling because the problem is gradient inconsistency, not D2D memorization.

**Falsification criterion.** If fresh-instance accuracy exceeds $50\%$, the attention-pathway-dominance hypothesis is weakened. The adaptation is that the QKV–output-projection interaction is less fragile than predicted, and the ceiling must be attributed to a different mechanism (e.g., multi-head correlation disruption or scale-recovery mismatch in the MLP path).

## 4.2 Experiment E2: CX-J1c — Output-Projection-Only Linearization + Ensemble HAT

**Research question.** Symmetric to E1: is the bottleneck the attention output projection (`.attn.proj`) rather than QKV? If output-projection-only linearization breaks the ceiling, the barrier is the inverse of value aggregation.

**Method.** The `.attn.proj` layers are designated as the protected group ($\text{NL}=1.0$); QKV, MLP, and patch-embedding layers retain $\text{NL}=2.0$. All other training and evaluation settings are identical to E1.

**Pre-registered prediction.** Under the attention-pathway-dominance hypothesis, CX-J1c is also predicted to stay near $\sim 30\%$. The reasoning is symmetric: if QKV is distorted, the attention scores are computed from corrupted queries and keys, and linearizing the output projection cannot restore the corrupted score geometry. The softmax has already re-ranked the tokens based on the distorted $QK^{\top}$ product; no linear correction in the value aggregation stage can invert that re-ranking.

**Falsification criterion.** If fresh-instance accuracy exceeds $50\%$, the hypothesis is weakened and the bottleneck shifts to the output projection. The research priority would then become output-projection-specific mitigations (e.g., lower-rank output matrices or structured sparsity).

**Unified falsification criterion for E1–E2.** The structural hypothesis is supported if and only if

$$
\text{FreshAcc(E1)} \approx \text{FreshAcc(E2)} \approx \text{FreshAcc(CX-J1\ joint)} \approx 30\%.
$$

If either E1 or E2 breaks the ceiling while the other does not, the hypothesis must be refined into a sub-path hypothesis identifying which specific matrix ($W_{Q}$, $W_{K}$, $W_{V}$, or $W_{O}$) is the bottleneck.

## 4.3 Experiment E3: CX-J1d-2 — Second-Order STE in Attention Blocks

**Research question.** Is the $\sim 30\%$ ceiling a first-order artifact (truncated Taylor expansion of the write dynamics) or a deeper structural property of the attention pathway? If the second-order Taylor-corrected STE breaks the ceiling, the barrier is surrogate-dependent, not architecture-dependent.

**Method.** All analog layers operate at $\text{NL}=2.0$ globally. In the backward hooks of `AnalogLinear` and `AnalogConv2d`, the first-order STE is replaced by the second-order STE:

$$
\text{grad}_{\text{input}} = \text{grad}_{\text{output}} \cdot \bigl( \Phi'(G) + \tfrac{1}{2}\Phi''(G)\,\Delta g_{\text{eff}} \bigr),
$$

where $\Phi'(G)=\text{NL}\,|G|^{\text{NL}-1}$ and $\Phi''(G)=\text{NL}(\text{NL}-1)\,|G|^{\text{NL}-2}$. The effective perturbation $\Delta g_{\text{eff}}$ is set to $\sigma_{\text{d2d}}(G_{\max}-G_{\min})+\sigma_{\text{c2c}}|G|$, auto-populated from the experiment config. The second-order correction is applied only to attention blocks (QKV + proj); MLP blocks remain on first-order STE to isolate the attention-pathway effect. A clamp $\min(|G|, 10^{-4})$ prevents divergence at $G\approx 0$. Training follows the ensemble HAT recipe.

**Pre-registered prediction.** Under the structural-limit hypothesis, the second-order correction is predicted not to exceed $50\%$ fresh-instance accuracy. The barrier arises from the interaction between the attention pathway's bilinear $QK^{\top}$ geometry and the state-dependent conductance mapping, not merely from gradient-approximation error. Even a perfect gradient would still face the rank-collapse and scale-recovery-mismatch mechanisms. Under the first-order-insufficiency hypothesis, the second-order correction should show a measurable lift ($>10$ percentage points) relative to the first-order baseline.

**Falsification criterion.** If fresh-instance accuracy exceeds $50\%$, the structural-limit hypothesis is falsified in its strong form, and the barrier is reclassified as a surrogate-truncation artifact.

## 4.4 Experiment E4: CX-J1d-3 — Cumulant Expansion (Third-Order) in Attention Blocks

**Research question.** Does propagating variance sensitivity (second cumulant) and skewness sensitivity (third cumulant) into the backward pass further improve generalization? This tests whether stochastic programming dynamics, not just deterministic curvature, are responsible for the ceiling.

**Method.** All analog layers operate at $\text{NL}=2.0$ globally. The cumulant-corrected STE is applied to attention blocks only:

$$
\frac{\partial \mathcal{L}}{\partial G} = \frac{\partial \mathcal{L}}{\partial \hat{G}}\,\mu_{1}'(G) + \tfrac{1}{2}\frac{\partial^{2}\mathcal{L}}{\partial \hat{G}^{2}}\,\mu_{2}'(G) + \tfrac{1}{6}\frac{\partial^{3}\mathcal{L}}{\partial \hat{G}^{3}}\,\mu_{3}(G).
$$

The second derivative of the loss is obtained via PyTorch double-backward (`create_graph=True`). Activation checkpointing for analog linear layers is enabled if out-of-memory errors occur. Training follows the ensemble HAT recipe.

**Pre-registered prediction.** If the barrier is purely deterministic gradient-approximation error, the cumulant expansion should show incremental improvement over the second-order STE. If the barrier is structural, the cumulant expansion will not escape the $\sim 30\%$ ceiling. The structural-limit hypothesis predicts no significant lift beyond E3.

**Falsification criterion.** Fresh-instance accuracy $>50\%$ would indicate that stochastic higher-moment propagation is sufficient to break the barrier.

## 4.5 Experiment E5: Mixed Digital–Analog Partition (Attention Digital, MLP Analog)

**Research question.** If the attention pathway is indeed the structural bottleneck under severe NL, can we bypass the barrier entirely by keeping attention weights in digital memory while mapping only the MLP and patch-embedding layers to analog arrays? This tests the most radical architectural implication of the structural-limit hypothesis.

**Method.** During model conversion, layers matching `"attn.qkv"`, `"attn.proj"`, and `"attn"` generally are skipped and remain standard `nn.Linear` / `nn.Conv2d` in FP16/FP32. The analog scope is restricted to `patch_embed.*`, `.mlp.fc1`, and `.mlp.fc2`. All analog layers operate at $\text{NL}=2.0$; digital layers are ideal. Training follows the ensemble HAT recipe.

**Pre-registered prediction.** If the structural-limit hypothesis is correct, this partition is predicted to restore deployment-grade accuracy ($>80\%$ fresh-instance) because the bottleneck pathway is removed from the analog domain. The cost is increased digital memory bandwidth and area.

**Falsification criterion.** If accuracy remains near $\sim 30\%$, the hypothesis is falsified: either the MLP path is also severely affected under global $\text{NL}=2.0$ (contradicting the pathway-decomposition analysis), or the patch-embedding layer is the hidden bottleneck.

## 4.6 Experiment E6: Rank-Collapse Diagnostic (Training-Time SVD Trajectory)

**Research question.** Does severe NL induce rank collapse in Q/K projections, as predicted by Pillar I of the structural-limit hypothesis? This is a pure diagnostic with no mitigation intent; it provides mechanistic evidence.

**Method.** Two training runs are executed under identical conditions except NL regime:
- Baseline: $\text{NL}=1.0$ globally, ensemble HAT.
- Severe: $\text{NL}=2.0$ globally, ensemble HAT.

Every $10$ epochs, the effective rank of $W_{Q}$ and $W_{K}$ is computed for each transformer stage:

$$
r_{\text{eff}} = \text{number of singular values} > 0.01 \times \sigma_{\max}.
$$

The sum $r_{Q}+r_{K}$ per layer is logged. For Tiny-ViT, the QKV weight tensor is sliced appropriately to isolate $W_{Q}$ and $W_{K}$.

**Pre-registered prediction.** Under Pillar I, we predict

$$
r_{Q}(\text{NL}=2.0) + r_{K}(\text{NL}=2.0) < r_{Q}(\text{NL}=1.0) + r_{K}(\text{NL}=1.0),
$$

specifically a rank deficit of at least $25\%$ relative to the $\text{NL}=1.0$ baseline (Condition F1). If no rank deficit is observed, Pillar I is falsified.

## 4.7 Experiment Summary and Falsification Lattice

| ID | Experiment | Protected / Modified | NL (protected) | NL (exposed) | STE order | Predicted fresh-instance | Falsifies if |
|:---|:---|:---|:---|:---|:---|:---|:---|
| E1 | CX-J1b | QKV only | $1.0$ | $2.0$ | 1st | $\sim 30\%$ | $>50\%$ |
| E2 | CX-J1c | Attn proj only | $1.0$ | $2.0$ | 1st | $\sim 30\%$ | $>50\%$ |
| E3 | CX-J1d-2 | Attn blocks | — | $2.0$ | 2nd (attn) | $\sim 30\%$ (structural) or $>40\%$ (surrogate) | $>50\%$ |
| E4 | CX-J1d-3 | Attn blocks | — | $2.0$ | 3rd (cumulant) | $\sim 30\%$ or slight lift | $>50\%$ |
| E5 | Mixed dig/ana | Attention digital | N/A (digital) | $2.0$ (MLP/emb) | 1st | $>80\%$ | $<50\%$ |
| E6 | Rank diagnostic | None | $1.0$ vs. $2.0$ | — | — | Rank deficit $\ge 25\%$ | No deficit |

## 4.8 Compute Budget and Scheduling

| Experiment | GPU-hours (RTX 4090) | Wall time | Dependencies |
|:---|:---|:---|:---|
| E1 (CX-J1b) | $\sim 6$ | $1$ day | None |
| E2 (CX-J1c) | $\sim 6$ | $1$ day | None |
| E3 (CX-J1d-2) | $\sim 7$ | $1$ day | Minor `analog_layers.py` patch |
| E4 (CX-J1d-3) | $\sim 9$ | $1$ day | E3 patch + double-backward |
| E5 (Mixed dig/ana) | $\sim 6$ | $1$ day | `convert_to_hybrid` exclusion logic |
| E6 (Rank diagnostic) | $\sim 6$ | $1$ day | SVD callback |
| **Total** | **$\sim 40$** | **$1$ week (parallelizable)** | — |

All six experiments can execute in parallel on a $4$-GPU node. The critical path is the code patches for E3/E4/E5, which require at most $2$ hours of development each.

## 4.9 Fallbacks and Risk Mitigation

| Risk | Mitigation |
|:---|:---|
| E3/E4 code patch introduces bugs | Run the $\text{NL}=1.0$ baseline through the patched hook; verify identical accuracy to unpatched run. |
| E5 digital attention exceeds GPU memory | Reduce batch size to $32$; use gradient accumulation. Accuracy trend is the metric, not absolute throughput. |
| E6 SVD too slow on CPU | Run SVD asynchronously in a background process every $10$ epochs; skip if training is paused. |
| Fresh-instance variance too high ($\sigma>12$ pp) | Increase to $n=15$ instances; recompute SEM and Cohen's $d$. |
| Any experiment yields ambiguous result (e.g., $42\%$) | Report the number honestly; discuss whether it supports a weak structural limit or a partial surrogate improvement. Do not force interpretation. |
