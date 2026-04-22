# §3 Methods

## 3.1 Simulation Framework and Architecture

All experiments are executed inside the compute-ViT framework, a PyTorch-based behavioral simulator that maps vision-transformer weights to differential conductance pairs and injects device non-idealities during training. We use Tiny-ViT V4 (approximately $5\,\text{M}$ parameters) as the backbone, trained from an ImageNet-pretrained initialization on CIFAR-10 for $100$ epochs with AdamW ($\text{lr}=5\times 10^{-4}$, weight decay $0.05$), cosine annealing, and batch size $64$. The analog-mapping rules convert each linear and convolutional layer to differential conductance arrays with six-bit ADC readout, baseline D2D mismatch variance $\sigma^{2}_{\text{D2D}}=(5\%)^{2}$, and C2C variability drawn from a Gaussian distribution. These settings mirror the canonical protocol established in prior work.

## 3.2 First-Order Nonlinear-Write Surrogate

Let $G$ denote the target differential conductance before programming, and let $\hat{G}$ denote the effective conductance after the analog write. The first-order surrogate models the write nonlinearity as a deterministic power law:

$$
\hat{G} = \begin{cases}
+\,|G|^{\text{NL}} & \text{(LTP)}, \\[4pt]
-\,|G|^{\text{NL}} & \text{(LTD)},
\end{cases}
\qquad \text{NL} \ge 1.
$$

During hardware-aware training, the forward pass uses $\hat{G}$, but the backward pass applies a straight-through estimator (STE) with a state-dependent scaling factor:

$$
\frac{\partial \hat{G}}{\partial G}\bigg|_{\text{STE}} = \text{NL} \, |G|^{\text{NL}-1} \, \text{sign}(G).
$$

For $\text{NL}=1.0$ this reduces to the identity. For $\text{NL}=2.0$ the scaling becomes $2|G|\,\text{sign}(G)=2G$, which amplifies the gradient magnitude for large conductances and suppresses it near zero. The asymmetry between LTP and LTD branches is encoded by distinct parameters $\text{NL}_{\text{LTP}}$ and $\text{NL}_{\text{LTD}}$; for severe nonlinearity we set $|\text{NL}_{\text{LTD}}|=\text{NL}_{\text{LTP}}=2.0$.

The analog array stores conductances, not weights. The recovered weight is $\hat{W}_{ij}=s_{\ell}\,G_{\text{eff},ij}$, where $s_{\ell}=w_{\max}/(G_{\max}-G_{\min})$. Under D2D mismatch field $M$ and C2C noise $\varepsilon$,

$$
G_{\text{eff}} = \hat{G}(G) \odot (1+M) + \varepsilon.
$$

The scale factor $s_{\ell}$ is learned implicitly because the STE back-propagates through $s_{\ell}$ as if it were a constant gain.

## 3.3 The Structural-Limit Hypothesis

> **Hypothesis (Attention-Pathway Dominance under Severe NL).**  
> Under the first-order $\text{NL}=2.0$ surrogate, the QKV and output-projection gradients acquire a state-dependent asymmetry that couples the learned spatial filters to the particular D2D pattern experienced during training. When the D2D pattern changes at deployment, the attention geometry—which is the core representational engine of the transformer—ceases to function. The MLP path, even when perfectly linearized, cannot compensate for a broken attention mechanism. Consequently, no training-objective modification within the first-order surrogate family can raise fresh-instance accuracy above a structural ceiling near $30\%$.

The hypothesis rests on three theoretical pillars derived from the interaction between the surrogate and the attention forward map.

### 3.3.1 Pillar I: Rank Collapse in Q/K Projections

Under the STE, the gradient of the loss with respect to the QKV weights receives a multiplicative factor $\text{NL}\,|G|^{\text{NL}-1}$ that depends on the instantaneous conductance magnitude. For $\text{NL}=2.0$,

$$
\frac{\partial \mathcal{L}}{\partial W_{Q}} = X^{\top} \left( \frac{\partial \mathcal{L}}{\partial Q} \right) \odot \left( 2 \, |G_{Q}| \, \text{sign}(G_{Q}) \right) s_{\ell}.
$$

Because $|G_{Q}|$ is spatially structured by the D2D field $M$, the effective learning rate for each element of $W_{Q}$ becomes position-dependent. Over many epochs, the optimizer adapts $W_{Q}$ to this modulation, effectively pre-distorting the query matrix so that the product $XW_{Q}$ compensates for the known spatial signature of $M$. The critical issue is that the query-key inner product $QK^{\top}$ is bilinear in the weights. If $W_{Q}$ and $W_{K}$ are each adapted to a different spatial distortion (because their conductance arrays have independent D2D realizations), the compensation does not transfer. The softmax operator is highly sensitive to the relative magnitudes of the inner products; a small shift in $W_{Q}$ or $W_{K}$ can re-rank the attention scores and destroy token-to-token correspondence.

**Mathematical prediction.** If we measure the effective rank of $W_{Q}$ and $W_{K}$ during training under $\text{NL}=2.0$, we predict

$$
\text{rank}(W_{Q}) + \text{rank}(W_{K}) < \text{rank}(W_{Q}^{\text{NL}=1.0}) + \text{rank}(W_{K}^{\text{NL}=1.0}),
$$

because the state-dependent gradient scaling biases the matrices toward the dominant singular vectors associated with large-conductance regions of the D2D map. This rank collapse reduces the expressive capacity of the attention mechanism and makes the geometry fragile to D2D perturbation.

### 3.3.2 Pillar II: Exponential Amplification of Surrogate Bias

The softmax operator is an exponential max-entropizer:

$$
\sigma(S)_{ij} = \frac{e^{S_{ij}}}{\sum_{k} e^{S_{ik}}}, \qquad S_{ij} = \frac{q_{i}\cdot k_{j}}{\sqrt{d_{h}}}.
$$

A small perturbation $\Delta S$ to the score matrix induces a relative change in the attention weights that scales as

$$
\frac{\Delta \sigma}{\sigma} \approx \Delta S \cdot (1-\sigma).
$$

Near the decision boundary of the softmax (where multiple tokens compete for attention), the sensitivity approaches $O(1)$. Now consider that $\Delta S$ is not random noise but a systematic bias induced by the NL surrogate. Because the Q and K weights are programmed with asymmetric LTP/LTD scaling, the inner product $QK^{\top}$ acquires a deterministic skew. The softmax exponentiates this skew. Even if the mean error in $S$ is small, the exponential nonlinearity can re-rank the attention map, causing tokens that should attend to each other to become orthogonal in the attention landscape. The attention pathway is therefore structurally coupled to the NL surrogate: the surrogate does not merely add noise; it reshapes the geometry of the token-interaction manifold in a way that is not invertible by linear compensation in the MLP path.

### 3.3.3 Pillar III: Instance-Specific Scale-Recovery Mismatch

Under $\text{NL}=2.0$, the mean effective conductance is $\mathbb{E}_{G}[\hat{G}]=\mathbb{E}_{G}[G^{2}]=\text{Var}(G)+\mathbb{E}[G]^{2}$, which depends on the second moment of the conductance distribution. The D2D field $M$ changes both the mean and the variance of $G_{\text{eff}}$ across the array. The learned scale factor $s_{\ell}$ therefore calibrates to the training-time second moment under $M_{0}$. At deployment, the second moment under $M'\neq M_{0}$ differs, and the scale recovery introduces a systematic gain mismatch that is invisible to source-domain accuracy (because the model trained on $M_{0}$ has already adapted to the miscalibrated $s_{\ell}$) but fatal to fresh-instance transfer.

In the MLP path, this mismatch is less severe because the MLP operates pointwise on tokens. A global scale error in $W_{\text{fc1}}$ can be partially absorbed by the downstream $W_{\text{fc2}}$ and by the LayerNorm that follows. In the attention path, the scale error enters before the softmax, where it is exponentiated and re-normalized globally across tokens. The error propagation is multiplicative and non-local in attention, but additive and local in MLP.

## 3.4 Falsifiable Conditions

A hypothesis is scientifically useful only if it can be falsified. We propose three concrete mathematical conditions; if any is violated, the structural-limit hypothesis must be revised.

**Condition F1 (Rank-collapse threshold).** Let $r_{Q}=\text{rank}(W_{Q})$ and $r_{K}=\text{rank}(W_{K})$ measured by the number of singular values above $0.01\times\sigma_{\max}$. Under $\text{NL}=2.0$ with fixed-mask training, we predict $r_{Q}+r_{K}\le 1.5\,d_{h}$ (i.e., at least $25\%$ rank deficit relative to the $\text{NL}=1.0$ baseline, where $r_{Q}\approx r_{K}\approx d_{h}$). If $r_{Q}+r_{K}>1.8\,d_{h}$, Pillar I is falsified.

**Condition F2 (Attention-map relative entropy bound).** Let $A^{(\text{NL}=1.0)}$ and $A^{(\text{NL}=2.0)}$ be the attention maps for the same input batch under ideal and severe-NL checkpoints. Define the per-token KL divergence $D_{\text{KL}}(A^{(1.0)}_{i}\,\|\,A^{(2.0)}_{i})$. We predict $\mathbb{E}_{i}[D_{\text{KL}}]>1.0$ nat for at least one transformer stage. If the KL divergence is $<0.1$ nat for all stages, Pillar II is falsified.

**Condition F3 (Fresh-instance ceiling invariance).** If a model trained with a second-order NL surrogate under joint MLP-linear + ensemble HAT achieves fresh-instance accuracy $>50\%$, the structural-limit hypothesis is falsified in its strong form, because a higher-fidelity surrogate would have broken the ceiling. If the ceiling persists at $\sim 30\%$ even with second-order correction, the hypothesis is strengthened and the barrier is attributed to the attention-pathway architecture itself.

## 3.5 Block-Heterogeneous Surrogate Taxonomy

To isolate the structural bottleneck, we define five training lanes within the first-order surrogate family:

1. **Standard HAT (fixed mask, $\text{NL}=2.0$ everywhere).** Baseline with a single D2D realization held constant throughout training.
2. **MLP-only linearization.** Attention layers (QKV + projection) remain at $\text{NL}=2.0$; MLP layers ($\text{fc1}$, $\text{fc2}$) are linearized to $\text{NL}=1.0$.
3. **All-linear.** All analog layers are linearized to $\text{NL}=1.0$, establishing an architectural upper bound on first-order recovery.
4. **Joint MLP-linear + Ensemble HAT.** Lane 2 combined with per-epoch D2D resampling and warm-start from the canonical $\text{NL}=1.0$ checkpoint.
5. **Canonical Ensemble HAT ($\text{NL}=1.0$ everywhere).** Positive control validating that the protocol itself is operational.

The group-wise selector is implemented via a naming-based filter over the Tiny-ViT module tree. Protected groups receive the linear surrogate; exposed groups retain the severe-NL surrogate. This taxonomy tests the MLP-dominance hypothesis: if the bottleneck were concentrated in the MLP blocks, Lane 2 should recover fresh-instance accuracy comparable to the positive control.

## 3.6 Second-Order Surrogate Extension (Falsification Probe)

To test whether the barrier is a first-order truncation artifact, we derive a second-order Taylor-corrected STE. Expanding the effective conductance to second order around the nominal conductance:

$$
\hat{G}(G+\Delta G) \approx \hat{G}(G) + \Phi'(G)\,\Delta G + \tfrac{1}{2}\Phi''(G)\,(\Delta G)^{2},
$$

where $\Phi(G)=|G|^{\text{NL}}$ and the derivatives are

$$
\Phi'(G) = \text{NL}\,|G|^{\text{NL}-1}\,\text{sign}(G), \qquad
\Phi''(G) = \text{NL}(\text{NL}-1)\,|G|^{\text{NL}-2}.
$$

The second-order STE replaces the first-order gradient with

$$
\frac{\partial \hat{G}}{\partial G}\bigg|_{\text{STE-2}} = \Phi'(G) + \tfrac{1}{2}\Phi''(G)\,\Delta g_{\text{eff}},
$$

where $\Delta g_{\text{eff}}$ is the effective perturbation amplitude, approximated as $\sigma_{\text{d2d}}(G_{\max}-G_{\min})+\sigma_{\text{c2c}}|G|$. For $\text{NL}=2.0$, $\Phi''(G)=2$, a constant, making the correction cheap to evaluate. The backward-pass overhead is approximately $1.1\times$ versus first-order.

We also specify a third-order cumulant expansion:

$$
\frac{\partial \mathcal{L}}{\partial G} = \frac{\partial \mathcal{L}}{\partial \hat{G}}\,\mu_{1}'(G) + \tfrac{1}{2}\frac{\partial^{2}\mathcal{L}}{\partial \hat{G}^{2}}\,\mu_{2}'(G) + \tfrac{1}{6}\frac{\partial^{3}\mathcal{L}}{\partial \hat{G}^{3}}\,\mu_{3}(G),
$$

where the second derivative of the loss is obtained via PyTorch double-backward. Memory cost is approximately $1.5\times$, feasible on $24\,\text{GB}$ VRAM with batch size $64$.

These higher-order extensions are applied selectively to attention blocks (QKV + projection) while keeping MLP blocks on first-order STE, isolating the attention-pathway effect. They are framed as falsification probes (CX-J1d) rather than claimed breakthroughs: if they break the ceiling, the barrier is surrogate-dependent; if they do not, the barrier is structural.

## 3.7 Ensemble HAT Protocol

Ensemble HAT resamples the full spatial D2D mismatch map $M\sim\mathcal{N}(0,\sigma^{2}_{\text{D2D}})$ at the beginning of every training epoch. This exposes the optimizer to the deployment distribution rather than a single instance, preventing hardware-instance overfitting. The protocol uses block-stationary resampling (one map per layer type) and AdamW with cosine annealing. Under moderate nonlinearity ($\text{NL}=1.0$), ensemble HAT recovers strong fresh-instance accuracy, validating that the protocol is operational when the surrogate remains locally valid.

## 3.8 Fresh-Instance Evaluation Protocol

The primary generalization metric is fresh-instance accuracy: after training concludes, the checkpoint is evaluated on $n=10$ independent unseen D2D realizations ("arrays"), with $5$ Monte Carlo forward passes per instance. The primary metric is the mean accuracy across the $10$ per-instance means; uncertainty is reported as the standard deviation across the $10$ per-instance means. Secondary metrics include source-domain (in-distribution) accuracy and per-instance variance. This protocol distinguishes same-instance overfitting from genuine distributional generalization.

## 3.9 Statistical Treatment

All fresh-instance comparisons use Welch's two-sample t-test (two-tailed, $\alpha=0.05$) with Cohen's $d$ as effect size. The ceiling-convergence claim requires not merely overlapping confidence intervals but also a small effect size ($d<0.3$) between the three severe-NL lanes. Sample size $n=10$ is sufficient to detect a $7$ percentage-point difference at observed $\sigma\approx 7$–$9$ pp with power $1-\beta=0.80$. One-sample t-tests against chance ($10\%$ on CIFAR-10) confirm whether severe-NL lanes remain above random guessing.

## 3.10 Code and Data Availability

All experiments are implemented in PyTorch within the compute-ViT repository. Device profiles, hyperparameter tables, checkpoint naming conventions, and locked random seeds are provided in Supplementary Note 1. Raw evaluation logs (JSON) for all completed experiments are archived with SHA-256 checksums.
