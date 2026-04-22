# HAT as an Implicit Regularizer

*Theory note — citable from Thesis Chapter 3 (Section 3.5, "Resampling cadence as an implicit transfer guarantee")*

---

## 1. Formal setup

Let $\mathcal{D}$ denote a random device profile drawn from the device-instance distribution $P(\mathcal{D})$. In the crossbar setting, $\mathcal{D}$ comprises the spatial D2D mismatch field $M$, the conductance bounds $(G_{\min}, G_{\max})$, and the noise law. Let $\theta \in \mathbb{R}^{d}$ be the digital network parameters. The empirical risk under a particular device instance is

$$
L(\theta; \mathcal{D}) = \frac{1}{N}\sum_{n=1}^{N} \ell\bigl(f(x_{n}; \theta, \mathcal{D}),\, y_{n}\bigr).
$$

Fixed-mask HAT minimizes $L(\theta; \mathcal{D}_{0})$ for a single draw $\mathcal{D}_{0}$ (Eq. 3.2 of the thesis). Ensemble HAT (Eq. 3.3) targets the expected risk:

$$
\theta^{\star}_{\text{ens}} = \arg\min_{\theta}\; \mathbb{E}_{\mathcal{D}\sim P(\mathcal{D})}\bigl[ L(\theta; \mathcal{D}) \bigr],
$$

which we approximate by Monte Carlo sampling.

## 2. Per-epoch resampling as Monte Carlo marginalization

During training we observe a sequence of $E$ independent draws $\{\mathcal{D}^{(1)}, \dots, \mathcal{D}^{(E)}\}$. Because one map is held constant across all mini-batches within epoch $e$, the per-epoch empirical risk is

$$
\hat{L}_{e}(\theta) = \frac{1}{N}\sum_{n=1}^{N} \ell\bigl(f(x_{n}; \theta, \mathcal{D}^{(e)}),\, y_{n}\bigr),
$$

and the full training trajectory minimizes the sample average

$$
\hat{L}_{\text{MC}}(\theta) = \frac{1}{E}\sum_{e=1}^{E} \hat{L}_{e}(\theta).
$$

By the strong law of large numbers, $\hat{L}_{\text{MC}}(\theta) \to \mathbb{E}_{\mathcal{D}}[L(\theta; \mathcal{D})]$ almost surely as $E \to \infty$. With $E = 100$, the finite-sample variance is small relative to optimization noise. Ensemble HAT therefore does not merely "add noise"; it marginalizes the objective over $P(\mathcal{D})$.

## 3. Connection to SAM: flat minima in hardware space

Sharpness-Aware Minimization (SAM) seeks parameters that sit in a flat basin of the *parameter-space* loss landscape by solving

$$
\min_{\theta} \max_{\|\epsilon\|_{2}\leq\rho} L(\theta + \epsilon; \mathcal{D}_{0}).
$$

SAM is a regularizer because flatness in parameter space implies robustness to weight perturbations. Ensemble HAT induces an analogous flatness, but in *device-instance* space. Instead of perturbing $\theta$ and keeping $\mathcal{D}$ fixed, Ensemble HAT perturbs $\mathcal{D}$ and keeps $\theta$ shared. The resulting parameters must lie in a basin that is simultaneously compatible with many structured realizations $\mathcal{D}^{(e)}$.

Is HAT "SAM in hardware space"? Structurally yes: both replace a point estimate with a neighborhood average. But SAM averages over an isotropic ball in parameter space, whereas HAT averages over the structured, spatially correlated manifold of device instances. Replacing D2D with i.i.d. noise every epoch drops fresh-instance accuracy from $86.37\%$ to $\sim 75\%$ (thesis, Section 3.4), confirming that HAT regularization is *distribution-specific*, not generic.

## 4. Connection to SWA: averaging over trajectories

Stochastic Weight Averaging (SWA) computes $\bar{\theta} = \frac{1}{K}\sum_{k} \theta^{(k)}$ over a parameter trajectory to find the center of a flat basin.

Ensemble HAT averages over a *hardware-noise* trajectory instead. The final $\theta^{\star}_{\text{ens}}$ is the fixed point of

$$
\theta^{(e+1)} = \theta^{(e)} - \eta \nabla_{\theta} \hat{L}_{e}(\theta^{(e)}),
$$

so the converged vector implicitly encodes an average over the sequence of hardware landscapes. The key difference is that SWA post-hoc averages weights that have already explored a basin, whereas HAT *drives* the optimizer into a shared basin by changing the landscape itself every epoch. HAT is a training-time regularizer; SWA is primarily inference-time stabilization.

## 5. PAC-Bayes framing

Treat $P(\mathcal{D})$ as a prior over device instances. For Ensemble HAT, the empirical risk is exactly the MC estimate $\hat{L}_{\text{MC}}(\theta)$. A standard PAC-Bayes bound takes the form

$$
\mathbb{E}_{\mathcal{D}\sim P}\bigl[ L(\theta; \mathcal{D}) \bigr] \;\leq\; \hat{L}_{\text{MC}}(\theta) + \sqrt{\frac{\mathrm{KL}(Q\,\|\,P) + \ln(2\sqrt{N}/\delta)}{2N}},
$$

where $Q$ is a posterior over hypotheses and $\delta$ is the confidence level. The *left-hand side* is exactly the quantity Ensemble HAT minimizes. By optimizing the MC surrogate, we directly minimize an upper bound on fresh-instance generalization error. Fixed-mask HAT minimizes only the first term for a single $\mathcal{D}_{0}$, leaving the bound vacuous for $P(\mathcal{D})$.

## 6. Why this matters

This perspective explains *structurally* why Ensemble HAT works. It is not a lucky empirical trick, nor merely "more noise augmentation." It is a principled Monte Carlo approximation to an expected-risk objective, and the per-epoch block-stationary schedule is the minimal cadence that lets the optimizer descend within each block while marginalizing across blocks. The learned parameters are forced into a basin flat across the hardware distribution, not just across parameter perturbations. This is why epoch-level resampling outperforms both fixed-mask training (no marginalization, instance overfitting) and per-batch resampling (too much landscape volatility). HAT is best understood not as a hardware-compatibility patch, but as a distributionally robust empirical risk minimizer whose implicit regularizer is the device-instance distribution itself.
