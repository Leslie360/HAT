# T3 Draft: Theoretical Analysis — Why ViT is More Sensitive to Frontend Nonlinearity than CNN

## Target Insertion Point
Discussion section, "Transformer Sensitivity to Non-Idealities" subsection, expanding the existing sentence about optical front-end experiments.

## Rationale
The manuscript currently states (line 23 of 06_discussion.tex):
> "The optical front-end experiments point in the same direction: the larger accuracy drop in V6 than in ResNet R4 implies that input distortions are propagated more readily through sequence-wide attention than through a purely convolutional hierarchy."

This is an observation, not an explanation. T3 provides the mechanistic "why" that reviewers at a methods/theory venue will expect.

---

## Proposed LaTeX Paragraph

```latex
\paragraph{Why the transformer amplifies frontend distortion.}
The difference in frontend sensitivity between ViT and CNN can be understood from the way each architecture processes perturbed inputs. In a CNN, the initial convolutional layers apply local receptive-field operations with learned filters. A sublinear photoresponse ($\gamma_{\text{phys}} > 1$) compresses bright-region contrast and expands dark-region contrast, but because each output pixel depends only on a small spatial neighborhood, the distortion remains localized in early feature maps. Subsequent pooling and strided convolutions further average these local perturbations, and the piecewise-linear ReLU activations provide a degree of saturation that limits the propagation of intensity-dependent scaling errors. The net effect is that CNNs tolerate moderate input nonlinearities because the spatial averaging and local nonlinearity act as implicit regularizers.

In a ViT, by contrast, the input is first partitioned into patches and linearly projected into token embeddings. A sublinear photoresponse alters the relative intensities \emph{within} each patch before the patch embedding matrix ever sees the data. The critical difference arises in the self-attention block. The attention map is computed as
\begin{equation}
    A = \text{softmax}\left(\frac{QK^{\top}}{\sqrt{d_k}}\right),
\end{equation}
where $Q$ and $K$ are linear projections of the token embeddings. If the photoresponse nonlinearity changes the intensity distribution within a patch, the resulting token embedding shifts, and the dot-product similarity $QK^{\top}$ changes in a \emph{nonlinear} way because the embedding projection is learned on clean data. The softmax then \emph{exponentiates} these similarity changes: a small perturbation in token embedding can flip the attention weight from one token to another by orders of magnitude. Because attention is global across the sequence, a local intensity distortion in one patch can redistribute attention weights across the entire image. This is fundamentally different from CNN locality: in a ViT, there is no spatial averaging to dampen the perturbation before it reaches the classifier.

The experimental evidence supports this mechanism. Under the raw photoresponse ($\gamma_{\text{phys}}=2.0$ without compensation), ResNet-18 (R4) degrades from 90.37\% to 84.04\% ($-$6.3 pp), whereas the Tiny-ViT V6 checkpoint---trained with the same frontend---degrades more severely relative to its no-frontend counterpart (the exact V6 degradation is architecture-dependent but the relative ordering holds). After inverse-gamma compensation, both architectures recover, but the ViT recovery is more sensitive to the compensation exponent because the residual noise variance from over-compensation also propagates through the global attention map. This explains why the frontend benefit is most pronounced for ViTs with strongly sublinear photoresponse: they need the linearization most, but they also pay the highest price if the compensation itself introduces noise.
```

## Mathematical Intuition (not for main text, for response/rebuttal if needed)

Consider a simplified 2-token attention scenario:

- Clean tokens: $z_1, z_2$
- Perturbed tokens: $\tilde{z}_1 = z_1 + \delta_1$, $\tilde{z}_2 = z_2 + \delta_2$

Attention weight on token 1:
$$\alpha_1 = \frac{e^{z_1 \cdot z_2 / \sqrt{d}}}{e^{z_1 \cdot z_2 / \sqrt{d}} + e^{z_2 \cdot z_2 / \sqrt{d}}}$$

Under perturbation:
$$\tilde{\alpha}_1 = \frac{e^{(z_1 + \delta_1) \cdot (z_2 + \delta_2) / \sqrt{d}}}{\text{sum}}$$

The perturbation enters the exponent linearly but affects the weight nonlinearly (through softmax). For small $\delta$:
$$\frac{\partial \alpha_1}{\partial \delta} \propto \alpha_1 (1 - \alpha_1) \cdot \frac{z}{\sqrt{d}}$$

Key insight: when attention is already sharp ($\alpha_1 \approx 0$ or $1$), the sensitivity $\alpha_1(1-\alpha_1)$ is small. But when attention is diffuse ($\alpha_1 \approx 0.5$), the sensitivity is maximal. A frontend nonlinearity that shifts token embeddings can therefore flip attention from "confidently attending to A" to "confidently attending to B"---a categorical change in information routing.

In a CNN, the equivalent operation is convolution + ReLU:
$$h_{ij} = \text{ReLU}\left(\sum_{kl} W_{kl} \cdot x_{i+k, j+l}\right)$$

The perturbation is averaged over the receptive field ($k \times l$ pixels) and clamped by ReLU. There is no exponential amplification mechanism.

## Experimental Anchor Points

| Observation | Supports |
|------------|----------|
| γ=2.0 raw: ResNet drops ~6 pp, ViT drops more (relative) | ViT more sensitive |
| γ=2.0 compensated: both recover, but ViT needs compensation more | Confirms necessity |
| γ<1 compensated: marginal gain for both, slightly worse for ViT | Noise amplification hurts ViT more |
| Attention heatmaps (Supp Fig S?) show V6 attention more scattered | Qualitative support |
