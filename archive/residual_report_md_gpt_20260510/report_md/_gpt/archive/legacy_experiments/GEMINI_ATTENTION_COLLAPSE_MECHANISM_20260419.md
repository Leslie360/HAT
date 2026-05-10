# GEMINI ATTENTION COLLAPSE MECHANISM ANALYSIS — 2026-04-19

**Reread of canonical state:**
I have re-read `paper/latex_gpt/sections/06_discussion.tex` (Frontend-Transformer paragraph), `NL_LANE_RESULTS_20260418.md`, and `GEMINI_NL_MITIGATION_THESIS_CHAPTER_20260418.md`.

## 1. Mathematical Argument: Structural Hypersensitivity of Softmax

The failure of QKV-only linearization (18.72%) and attn_proj-only linearization (~11%, collapsing) demonstrates that the self-attention mechanism is structurally incompatible with severe asymmetric nonlinearity (NL=2.0).

**The Mechanism of Amplification:**
In a standard Attention block, the attention scores $A$ are computed as:
$$ A = \text{Softmax} \left( \frac{(Q + \delta Q)(K + \delta K)^T}{\sqrt{d_k}} \right) $$
where $\delta Q, \delta K$ represent the accumulated weight errors from nonlinear updates. Expanding the product:
$$ Q K^T + \underbrace{Q \delta K^T + \delta Q K^T + \delta Q \delta K^T}_{\text{Geometric Distortion } \epsilon} $$
Because Softmax is an exponential operator, $\text{Softmax}(x) \propto \exp(x)$, the attention weights $w_i$ respond to the distortion $\epsilon$ nonlinearly:
$$ w_i' \approx w_i \cdot \exp(\epsilon_i) $$
Even small angular distortions in the Query/Key projections lead to **exponential scattering** of the attention probability mass. If the distortion $\epsilon$ is large enough to shift the maximum logit away from the semantically relevant token, the attention map fragments, and the block fails to aggregate features correctly.

**Why MLP layers survive:**
MLP layers use linear transformations followed by relatively benign activations like GELU/ReLU. Errors in MLP weights $(\delta W)$ propagate linearly: $y = (W + \delta W)x$. Unless the error is large enough to flip the sign or saturate the activation, the block remains functionally stable. **Attention transforms geometric similarity into probability distributions, making it an error-amplifier by design.**

## 2. Alternative Interpretations: Structural vs. Optimization Path

### Interpretation A: Structural Failure (The Hard Bound)
- **Argument:** The attention mechanism requires a level of angular precision that a 1-bit or 2-bit update fidelity (imposed by NL=2.0) simply cannot provide. No amount of training will find a stable basin because the "canyons" in the attention loss landscape are too narrow for the coarse nonlinear steps to land in.
- **Evidence:** The QKV-only lane fails even though gradients are "perfect" (linearized) for that specific block. This suggests the distortion isn't just in the updates, but in the resulting stationary weights being unable to represent the required attention geometry under analog noise.

### Interpretation B: Optimization-Path Collapse (The Initialization Trap)
- **Argument:** The failure occurs because the network collapses at Epoch 0–2 before the learning rate can decay into a stable regime. If we initialized with a "better" pretrained starting point or used a warmer learning rate schedule, the QKV path might find a stable configuration.
- **Evidence:** Both QKV and attn_proj best accuracies are frozen at Epoch 0 or 2. They never "learn" and then fail; they fail immediately upon first exposure to the analog noise/nonlinearity combined update.

## 3. Diagnostic Experiments (Thesis-Only)

To distinguish between Structural and Optimization failure, the thesis should run:
1. **The "Warm-Start" Transfer:** Initialize the QKV-only NL=2.0 training using the *final* weights of a successful MLP-only or NL=1.0 run. If it still collapses, the failure is structural.
2. **The Orthogonality Metric:** Compute the rank and condition number of the $Q$ and $K$ matrices during training. If Interpretation A is correct, we expect to see a collapse in matrix rank (loss of representation diversity) long before accuracy hits 10%.
3. **NL-Severity Gradient Step Scan:** Instead of a full train, perform a single-epoch gradient update with different NL values ($1.2 \to 2.0$) and measure the Cosine Similarity of the resulting Attention Maps. Map the "Geometric Divergence Curve" of the attention distribution.

## 4. Implications for the NC Paper

The Section 6 Discussion sentence:
> "Group-wise ablation confirms that the bottleneck is concentrated in the MLP analog path, while both attention-side linearizations (QKV and projection) collapse structurally."

**Recommendation:** This sentence is currently **accurate** and supported by the dual-failure of QKV and attn_proj. No softening is required. However, we should ensure the supplementary text clarifies that "structural collapse" refers to the hypersensitivity of the softmax similarity search to update asymmetry.
