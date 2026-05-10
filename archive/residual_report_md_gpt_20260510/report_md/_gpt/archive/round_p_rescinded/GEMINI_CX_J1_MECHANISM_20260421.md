# Mechanism Commentary: Why Attention Dominates the CX-J1 Failure Mode

## 1. Parameter-Budget Argument

In Tiny-ViT-5M the analog-mapped attention pathway (QKV + projection) holds **1.57 M** parameters (33 % of analog, 29 % of total), whereas the MLP blocks hold **3.14 M** parameters (66 % of analog, 58 % of total).  The MLP is twice as large, yet linearizing it alone yields fresh-instance accuracy of 32.12 %—statistically indistinguishable from the joint MLP-linear + Ensemble HAT result of 30.53 %.  Because removing non-linearity from the larger block produces no benefit, the bottleneck is not a raw capacity shortage.  The attention pathway dominates failure despite its smaller footprint, indicating that the softmax-normalized dot-product is the rate-limiting factor.

## 2. Gradient-Flow Argument

Under NL = 2.0 effective conductance follows $g_{\text{eff}} \propto g^{\text{NL}}$, compressing MAC output dynamic range.  Attention pre-softmax logits are
$$
z = \frac{QK^{\top}}{\sqrt{d_k}}, \qquad Q = XW_Q,\; K = XW_K,
$$
where $W_Q$ and $W_K$ reside on nonlinear crossbars.  The effective dot-product becomes a distorted bilinear form.  Softmax $\sigma(z)_i = e^{z_i}/\sum_j e^{z_j}$ is exponentially sensitive to input scale: compressed dynamic range either drives uniform attention (entropy collapse) or, combined with device variance, creates sporadic sharp peaks (attention collapse).  MLP activations pass through GELU, which is monotonic and locally linear; perturbations propagate without softmax's winner-take-all amplification.  The same NL-induced distortion therefore has a qualitatively more severe impact on attention scores than on MLP activations.

## 3. Information-Theoretic Sketch *(heuristic)*

Attention computes $\text{Attn}(X) = \text{softmax}(QK^{\top})V$.  Because softmax maps $\mathbb{R}^{L\times L} \to \Delta^{L-1}$, ADC quantization noise is coupled across the sequence dimension via the partition-function denominator.  Under severe NL the signal swing of $QK^{\top}$ collapses into fewer ADC bins, degrading SQNR.  We heuristically conjecture that attention loses more mutual information per ADC bit than the MLP: in the MLP, quantization errors remain neuron-local, whereas in attention an error in one logit perturbs the entire probability simplex.  When $QK^{\top}$ collapses, the attention distribution approaches uniform entropy $H \approx \log L$, but task-relevant token-selection information is destroyed.

## 4. D2D-Sensitivity Argument *(heuristic)*

Device-to-device mismatch introduces fixed conductance offsets $\delta g$.  In the MLP, $\Delta y = x \cdot \delta W$ is linear in the weight error and partially absorbed by batch normalization.  In attention, offsets in $W_Q$ and $W_K$ alter pre-softmax logits; the softmax Jacobian $J_{ij} = \sigma_i(\delta_{ij} - \sigma_j)$ couples all outputs, so a small systematic offset can shift the entire attention pattern.  We heuristically expect attention weights to be $2\times$–$5\times$ more sensitive to D2D mismatch than MLP weights: softmax amplifies conductance variations into discrete attention-pattern switches, including near-one-hot collapse.  The MLP lacks this competitive normalization, so its outputs remain robust to multiplicative weight errors.

## 5. Testable Prediction: CX-J1b (QKV-Only Linearization)

CX-J1b linearizes only the QKV transformations ($\text{NL}_{\text{LTP}} = 1.0$) while keeping the attention projection and all MLP layers at NL = 2.0.  If fresh-instance accuracy remains near the $\sim$30 % ceiling, the QKV arrays themselves are **not** the bottleneck.  Because QKV layers are already linear operations, idealizing their MAC arrays only removes conductance non-linearity from the query-key-value computation; the residual softmax, output projection, and their interaction remain exposed to severe NL.  A negative result therefore localizes the barrier to the attention block as a *functional unit*—specifically the softmax-normalized dot-product and its projection—rather than to any single sub-component.  Conversely, success would narrow the barrier to the QKV arrays alone, implying that projection and softmax are sufficiently robust.
