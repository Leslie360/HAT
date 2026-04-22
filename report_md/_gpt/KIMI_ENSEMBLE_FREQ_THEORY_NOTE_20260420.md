# Ensemble-Frequency Effective-Width Theory

**Context:** Thesis Chapter 3, §4 (cadence ablation).  
**Status:** Heuristic / conjectural.

---

## 1. Ensemble frequency

Define the ensemble frequency $f$ as the inverse of the mean correlation time between adjacent device draws from the mismatch distribution $p(M)$:

$$
f = \frac{1}{\tau_{\text{corr}}} \quad [\text{draws per epoch}].
$$

For the canonical Tiny-ViT recipe (CIFAR-10, batch size 64, $\sim$782 batches/epoch):

- **Fixed-mask HAT:** $f \to 0$ (one draw, held forever);
- **Ensemble HAT (per-epoch):** $f \approx 1\ \text{epoch}^{-1}$;
- **Per-batch resampling:** $f \approx 7.8 \times 10^{2}\ \text{epoch}^{-1}$.

Lower $f$ means adjacent mini-batches share the same device instance $M$ for longer, so their forward paths and gradients are highly correlated.

## 2. Heuristic AR(1) model and effective width

Treat the sequence of exposed device instances as an AR(1)-like process in the training-time index. Let $\rho_{\text{corr}}(f)$ denote the effective autocorrelation between adjacent mini-batches under cadence $f$. When $f$ is small the same instance persists across many batches, so $\rho_{\text{corr}} \to 1$; when $f$ is large instances refresh rapidly and $\rho_{\text{corr}} \to 0$.

The characteristic correlation length—the number of batches spanned by one correlated block—is heuristically

$$
\xi(f) \;\propto\; \frac{1}{1 - \rho_{\text{corr}}(f)}.
$$

We identify this block size with the **effective ensemble width** $N_{\text{eff}}(f)$. It measures how many batches are statistically redundant because they share the same structured instance. The number of independent adaptation episodes is therefore inversely proportional to $N_{\text{eff}}(f)$.

## 3. Plateau location from the 50-epoch ablation

The exploratory 50-epoch scan reports held-out accuracies:

- **Per-epoch (Ensemble HAT):** 88.41\%
- **Fixed-mask control:** 87.18\%
- **Per-batch control:** 86.16\%

Accuracy rises when $N_{\text{eff}}(f)$ is large enough to allow many batches of descent under a stable instance—fixed mask provides only one episode, so it underfits the distributional breadth. But when $N_{\text{eff}}(f)$ becomes too small—i.e., when the block size shrinks below the time the optimizer needs to adapt—the trajectory never settles into a basin compatible with any single structured instance. The per-batch result ($86.16\%$) signals this collapse.

The plateau therefore sits at the **per-epoch cadence**, $f^{*} \approx 1\ \text{epoch}^{-1}$, where the block size $\xi \approx B$ matches one full epoch. At this saturation point the number of independent episodes reaches $N_{\text{episodes}}^{*} \approx E = 50$; additional draws within an epoch do not expand the explored distributional support.

## 4. Comparison to dropout and SWA

**Dropout** samples a random subnetwork every forward pass. Its frequency is maximal ($f \to \infty$ in our notation), but the ensemble is over architectural masks in function space, not over device realizations, and there is no block-stationary phase for the analog forward path to stabilize.

**Stochastic Weight Averaging (SWA)** collects weights along a single trajectory and averages them post hoc. It operates in weight space with per-update frequency, seeking a flat minimum. Ensemble HAT, by contrast, forces the *same* weight vector to survive many distinct structured instances. The essential difference is that **ensemble frequency controls the temporal correlation structure of the training surrogate**, not the network architecture or a weight-space average.

## 5. Testable prediction

If the saturation picture is correct, doubling the ensemble size beyond $N_{\text{eff}}^{*}$ should yield diminishing returns. Concretely, extending per-epoch training from 50 to 100 epochs (doubling the number of independent draws from 50 to 100) should improve held-out accuracy by **less than 0.1 percentage points**, because the additional device instances are statistically redundant once the full D2D distribution has already been covered.
