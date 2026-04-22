# ADC Precision Floor Theory v2

## 1. Problem Formalization

In an analog CIM accelerator, the query–key product $S = QK^T \in \mathbb{R}^{N \times N}$ is produced as a continuous distribution. An $b$-bit ADC maps each entry $s_{ij}$ to $\hat{s}_{ij}$ with step $\Delta = R / 2^b$, where $R$ is the full-scale range. The information loss is the mutual information $I(S; \hat{S})$, bounded above by $b$ bits per sample. When $I(S; \hat{S})$ falls below the entropy required to distinguish the $N$ attention scores feeding into softmax, the attention mechanism collapses.

## 2. Variance Argument

Assume $Q, K \in \mathbb{R}^{N \times d_k}$ have independent, zero-mean, unit-variance entries. Each dot-product is
$$
s_{ij} = \sum_{k=1}^{d_k} q_{ik} k_{jk}.
$$
By the CLT, $s_{ij} \approx \mathcal{N}(0, d_k)$. Scaled dot-product attention divides by $\sqrt{d_k}$, giving
$$
\sigma_{QK}^2 = 1, \qquad \sigma_{QK} = 1.
$$
With a typical dynamic range $R \approx 6\sigma_{QK} = 6$ (covering $\pm 3\sigma$), the quantization step is
$$
\Delta = \frac{6}{2^b}.
$$
The naive critical precision where $\Delta \approx \sigma_{QK}$ gives $b \approx \log_2 6 \approx 2.6$, which is far too low because it ignores softmax discrimination.

## 3. The 6-Bit Cliff Explanation

Softmax is sensitive to *relative* differences. Define the effective resolution as levels per standard deviation:
$$
N_\sigma = \frac{\sigma_{QK}}{\Delta} = \frac{2^b}{6}.
$$
For $b = 6$, $N_\sigma \approx 10.7$. Below 6 bits, $N_\sigma < 10$, and the softmax tail—where a few large scores dominate—collapses into the same bin as mid-range scores. Empirically, preserving a sparse attention distribution with peak-to-mean ratio $> 2$ requires $\approx 10$ effective levels. This creates the observed accuracy cliff at $b \approx 6$.

*Heuristic gap:* The exact threshold depends on the token distribution and is derived here from phenomenological accuracy curves.

## 4. Information-Theoretic Bound

Let $\alpha = \text{softmax}(S)$ and $\hat{\alpha} = \text{softmax}(\hat{S})$. Correct classification requires
$$
I(\alpha; \hat{\alpha}) \geq H(\text{class}) - \epsilon.
$$
Rate-distortion gives a lower bound on the required rate $R$ for MSE distortion $D$:
$$
R(D) \geq \frac{1}{2} \log_2 \frac{\sigma_{QK}^2}{D}.
$$
Setting $D = \Delta^2 / 12$ (uniform quantization noise) and requiring $R(D) \geq b_{\min}$:
$$
b_{\min} \geq \frac{1}{2} \log_2 \left( \frac{12 \sigma_{QK}^2}{R^2} \cdot 2^{2b} \right).
$$
For $R = 6\sigma_{QK}$, this reduces to a consistency check: if the RHS exceeds $b$, the ADC is information-limited. The bound is tight only with dynamic per-channel scaling.

*Rigorous gap:* We conflate scalar quantization of $S$ with vector quantization of $\alpha$; a full treatment requires vector rate-distortion on the softmax simplex.

## 5. Extension to Different $d_k$

With $\sqrt{d_k}$ scaling, $\sigma_{QK} = 1$ is independent of $d_k$. However, hardware noise is often absolute (in volts), not relative. The pre-scaling dot-product magnitude grows as $\sqrt{d_k}$, so effective SNR improves with larger $d_k$:
- **$d_k = 32$:** Analog noise is a larger relative perturbation. Estimated $b_{\min} \approx 7$.
- **$d_k = 128$:** More averaging suppresses outliers; attention becomes more uniform. Estimated $b_{\min} \approx 6$.

A refined heuristic replaces fixed $R$ with $R \propto \sqrt{d_k}$:
$$
b_{\min}(d_k) \approx 6 + \frac{1}{2}\log_2\left(\frac{64}{d_k}\right).
$$

## 6. Validation Plan

1. **Controlled sweep:** Fix D2D variation and nonlinearity at measured levels; sweep $b \in \{4,5,6,7,8\}$ on CIFAR-10/100 with a small ViT.
2. **Cliff localization:** Fit $\text{Acc}(b) = A + (B-A)/(1 + e^{-k(b-b_0)})$ and extract $b_0$ as the empirical floor.
3. **MI proxy:** Compute $H(\alpha)$ and $H(\hat{\alpha})$ from calibration batches; verify that $\Delta I = I(\text{input}; \alpha) - I(\text{input}; \hat{\alpha})$ correlates with accuracy degradation.
4. **$d_k$ ablation:** Repeat for $d_k \in \{32,64,128\}$ at fixed capacity; check whether the cliff shifts according to the scaling law in §5.
