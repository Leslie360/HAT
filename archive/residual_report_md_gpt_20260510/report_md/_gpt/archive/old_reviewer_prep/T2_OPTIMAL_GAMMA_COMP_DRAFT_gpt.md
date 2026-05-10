# T2 Draft: Optimal Compensation Exponent

## Target Insertion Point
Supplementary Information, as a new note under the frontend-compensation section.

## Core Derivation

### Problem Setup

Given a normalized input pixel $X \in [0,1]$, physical photoresponse exponent $\gamma_{\text{phys}}$, and compensation exponent $\gamma_c$, the pipeline is:

1. Compensation: $P_{\text{in}} = X^{\gamma_c}$
2. Physical transduction + shot noise: $I_{\text{photo}} = \alpha P_{\text{in}}^{\gamma_{\text{phys}}} + I_{\text{dark}} + \varepsilon_{\text{shot}}$
3. Ideal linearization target (what the neural network expects): $I_{\text{ideal}} = \alpha X + I_{\text{dark}}$

The physical inverse sets $\gamma_c = 1/\gamma_{\text{phys}}$, which exactly cancels the nonlinearity in the noiseless case:
$$I_{\text{photo}}^{(\text{no noise})} = \alpha (X^{1/\gamma_{\text{phys}}})^{\gamma_{\text{phys}}} = \alpha X$$

### Noise-Induced Deviation

With shot noise $\varepsilon_{\text{shot}}$ where $\text{Var}[\varepsilon_{\text{shot}}] = \sigma^2 I_{\text{photo}}$, the compensated signal is:
$$I_{\text{photo}} = \alpha X^{\gamma_c \gamma_{\text{phys}}} + I_{\text{dark}} + \varepsilon_{\text{shot}}$$

Define the effective signal deviation from ideal:
$$\Delta(X; \gamma_c) = I_{\text{photo}} - I_{\text{ideal}} = \alpha \left(X^{\gamma_c \gamma_{\text{phys}}} - X\right) + \varepsilon_{\text{shot}}$$

### Mean-Squared Error Objective

The optimal compensation exponent minimizes the expected squared deviation across the input distribution $p(X)$:
$$\gamma_c^* = \arg\min_{\gamma_c} \mathbb{E}_X\left[\text{MSE}(X; \gamma_c)\right]$$

where
$$\text{MSE}(X; \gamma_c) = \underbrace{\alpha^2 \left(X^{\gamma_c \gamma_{\text{phys}}} - X\right)^2}_{\text{signal nonlinearity residual}} + \underbrace{\sigma^2 \left(\alpha X^{\gamma_c \gamma_{\text{phys}}} + I_{\text{dark}}\right)}_{\text{shot-noise variance}}$$

### Key Insight

The physical inverse $\gamma_c = 1/\gamma_{\text{phys}}$ zeroes the **signal nonlinearity residual** but does not minimize the total MSE when shot noise is present. The noise term depends on $\gamma_c$ through $X^{\gamma_c \gamma_{\text{phys}}}$.

For $\gamma_{\text{phys}} > 1$:
- Physical inverse ($\gamma_c = 1/\gamma_{\text{phys}} < 1$): signal is perfectly linearized, but noise variance is $\sigma^2(\alpha X + I_{\text{dark}})$ — moderate.
- More aggressive compensation ($\gamma_c < 1/\gamma_{\text{phys}}$): over-linearizes bright regions, amplifying noise.
- Less aggressive compensation ($\gamma_c > 1/\gamma_{\text{phys}}$): leaves residual nonlinearity but reduces noise in bright regions.

### Closed-Form Approximation (Uniform $X \sim \mathcal{U}[0,1]$)

For uniform input and small dark current ($I_{\text{dark}} \approx 0$), the expected MSE is:
$$\mathcal{L}(\gamma_c) = \alpha^2 \int_0^1 \left(X^{\gamma_c \gamma_{\text{phys}}} - X\right)^2 dX + \sigma^2 \alpha \int_0^1 X^{\gamma_c \gamma_{\text{phys}}} dX$$

Evaluating the integrals:
$$\mathcal{L}(\gamma_c) = \alpha^2 \left[\frac{1}{2\gamma_c\gamma_{\text{phys}} + 1} - \frac{2}{\gamma_c\gamma_{\text{phys}} + 2} + \frac{1}{3}\right] + \frac{\sigma^2 \alpha}{\gamma_c\gamma_{\text{phys}} + 1}$$

Setting $\beta = \gamma_c \gamma_{\text{phys}}$ and differentiating:
$$\frac{d\mathcal{L}}{d\beta} = \alpha^2 \left[-\frac{2}{(2\beta+1)^2} + \frac{2}{(\beta+2)^2}\right] - \frac{\sigma^2 \alpha}{(\beta+1)^2}$$

At $\beta = 1$ (physical inverse):
$$\left.\frac{d\mathcal{L}}{d\beta}\right|_{\beta=1} = \alpha^2 \left[-\frac{2}{9} + \frac{2}{9}\right] - \frac{\sigma^2 \alpha}{4} = -\frac{\sigma^2 \alpha}{4} < 0$$

**Result**: The derivative is negative at $\beta = 1$, meaning the MSE can be reduced by increasing $\beta$ (i.e., using $\gamma_c > 1/\gamma_{\text{phys}}$). The optimal compensation is **less aggressive** than the physical inverse when shot noise dominates.

### Physical Interpretation

When shot noise is significant, the optimal strategy trades a small amount of residual nonlinearity for reduced noise variance in bright regions. The deviation from physical inverse is small for typical parameters but becomes measurable at high $\sigma^2 / \alpha$ ratios.

### Connection to Learnable Compensation (E3)

The learnable-compensation experiment (E3) tests whether end-to-end task loss optimization discovers this theoretical deviation. If the learned $\gamma_c$ deviates from $1/\gamma_{\text{phys}}$ in the direction predicted by the MSE analysis, it confirms that the task-optimal trade-off differs from the physical-linearization optimum.

## LaTeX Insertion Block

```latex
\subsubsection{Optimal Compensation Exponent}
\label{note:optimal-gamma}

The physical inverse $\gamma_c = 1/\gamma_{\text{phys}}$ exactly linearizes the photoresponse in the noiseless limit, but it is not necessarily optimal when shot noise is present. We derive the mean-squared-error-optimal compensation exponent for a uniform input distribution.

The effective signal deviation from the ideal linear response $I_{\text{ideal}} = \alpha X + I_{\text{dark}}$ is
\begin{equation}
    \Delta(X; \gamma_c) = \alpha \left(X^{\gamma_c \gamma_{\text{phys}}} - X\right) + \varepsilon_{\text{shot}},
\end{equation}
with $\text{Var}[\varepsilon_{\text{shot}}] = \sigma^2 (\alpha X^{\gamma_c \gamma_{\text{phys}}} + I_{\text{dark}})$. The expected MSE is
\begin{equation}
    \mathcal{L}(\gamma_c) = \alpha^2 \int_0^1 \!\left(X^{\gamma_c \gamma_{\text{phys}}} - X\right)^2 dX + \sigma^2 \int_0^1 \!\left(\alpha X^{\gamma_c \gamma_{\text{phys}}} + I_{\text{dark}}\right) dX.
\end{equation}

Setting $\beta = \gamma_c \gamma_{\text{phys}}$ and evaluating the integrals gives
\begin{equation}
    \mathcal{L}(\beta) = \alpha^2\!\left[\frac{1}{2\beta+1} - \frac{2}{\beta+2} + \frac{1}{3}\right] + \sigma^2\!\left[\frac{\alpha}{\beta+1} + I_{\text{dark}}\right].
\end{equation}

Differentiating at $\beta = 1$ (the physical inverse):
\begin{equation}
    \left.\frac{d\mathcal{L}}{d\beta}\right|_{\beta=1} = -\frac{\sigma^2 \alpha}{4} < 0 \quad (\text{for } I_{\text{dark}} \approx 0).
\end{equation}

Because the derivative is negative, the MSE can be reduced by increasing $\beta$; i.e., the optimal compensation exponent is **milder** than the physical inverse when shot noise is present. The deviation is small for typical device parameters ($\sigma^2 \ll \alpha$), which explains why the physical inverse remains an excellent practical approximation. The learnable-compensation experiment (E3) tests whether task-level optimization recovers this theoretically predicted deviation.
```
