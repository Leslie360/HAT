# DISPATCH KIMI-THEORY-1 — Ensemble HAT Formal Derivation
**Date:** 2026-04-24
**Issued by:** Claude
**Assignee:** Kimi
**Priority:** HIGHEST (this is the main methodological upgrade)
**Depends on:** NARRATIVE_PIVOT_20260424.md (master spec)
**Time budget:** unconstrained — depth > speed, PhD-graduation-gated submission means months of buffer

---

## 1. Objective

Upgrade Ensemble HAT from "a training trick that worked" to "a principled distribution-matching objective with implicit regularization equivalence". Produce a 3-4 page Supplementary Note + a compressed ~8-sentence Methods paragraph that the paper body can cite as justification.

This is the single most important non-experimental contribution we can add. Reviewers at Nat Electronics ask "why does resampling work" — we need a formal answer, not "empirically it helped".

---

## 2. Derivation skeleton (your task to flesh out)

### 2.1 Define both objectives formally

**Standard HAT (fixed-mask):**
$$
\mathcal{L}_{\text{Std}}(W; M_0) = \mathbb{E}_{\xi_{\text{C2C}}, (x,y)\sim\mathcal{D}}\Big[\ell\big(f(x;\, W \odot (1 + M_0) + \xi_{\text{C2C}}),\, y\big)\Big]
$$
where $M_0 \in \mathbb{R}^{d}$ is a **fixed** per-device fractional mismatch map sampled once at the start of training from $\mathcal{D}_{\text{D2D}}$.

**Ensemble HAT (distribution-matching):**
$$
\mathcal{L}_{\text{Ens}}(W) = \mathbb{E}_{M \sim \mathcal{D}_{\text{D2D}},\, \xi_{\text{C2C}},\, (x,y)\sim\mathcal{D}}\Big[\ell\big(f(x;\, W \odot (1 + M) + \xi_{\text{C2C}}),\, y\big)\Big]
$$
where $M$ is resampled **per training epoch** (or equivalent schedule).

The epoch-level resampling vs per-batch-resampling distinction is empirically important (see Results §5.7 — 88.41% epoch vs 86.16% per-batch). Speculate on why epoch is the load-bearing scale: epoch-level mismatch gives the optimizer enough consistent signal within an epoch to fit that instance, then the instance changes, enforcing a "learn-to-adapt" regime rather than noise-averaging. Compare to domain randomization in robotics (Tobin 2017).

### 2.2 First-order Taylor expansion

Assume $M$ has zero mean and covariance $\Sigma_M$ (for uncorrelated D2D, $\Sigma_M = \sigma_{\text{D2D}}^2 I$). Expand $f$ around $W$:

$$
f(x; W \odot (1 + M)) \approx f(x; W) + \sum_i M_i W_i \frac{\partial f}{\partial W_i}(x; W) + \mathcal{O}(\|M\|^2)
$$

Expected loss to second order in $M$:

$$
\mathbb{E}_M[\ell] \approx \ell(f(x;W), y) + \frac{1}{2}\mathbb{E}_M\Big[\sum_{i,j} M_i M_j W_i W_j \frac{\partial \ell}{\partial f_i}\frac{\partial \ell}{\partial f_j}\cdot (\text{second-order terms})\Big]
$$

For Gaussian $M$ with diagonal covariance $\sigma_{\text{D2D}}^2 I$:

$$
\mathcal{L}_{\text{Ens}}(W) \approx \mathcal{L}_0(W) + \frac{\sigma_{\text{D2D}}^2}{2} \sum_i W_i^2 \mathbb{E}_{(x,y)}\Big[\Big(\frac{\partial \ell}{\partial W_i}\Big)^2\Big] + \text{(cross terms)}
$$

**This is the key result.** Ensemble HAT ≈ Standard cross-entropy + a weighted gradient-squared penalty — an **implicit regularizer on the sensitivity of the loss to each weight**, weighted by $W_i^2 \sigma_{\text{D2D}}^2$.

### 2.3 Compare to Wager 2013 dropout = L2

Wager, Wang, Liang (NeurIPS 2013) showed Gaussian input dropout with rate $p$ on linear models induces L2 regularization with coefficient $\lambda = p/(1-p)$. Our result is the **multiplicative-weight-noise analog** of that: instead of $p/(1-p)$ we have $\sigma_{\text{D2D}}^2$ as the regularization strength; instead of L2 on $W$ we have a gradient-L2 (a Fisher-like penalty, structurally related to elastic weight consolidation but arising from hardware physics).

### 2.4 Why this explains generalization across D2D instances

The implicit regularizer penalizes weights whose gradient magnitudes are sensitive to small multiplicative perturbations. The optimizer pushes toward flat regions of the loss landscape **in the $M$-direction**. A fresh D2D instance $M_{\text{new}}$ drawn from the same distribution lands in one of those flat regions with high probability. Hence transferability.

Standard HAT, in contrast, fits one specific $M_0$: the trained weights land at a local minimum of $\ell(W \odot (1+M_0))$, which is **not** guaranteed to be a minimum of $\ell(W \odot (1+M'))$ for different $M'$. Hence fresh-instance collapse.

### 2.5 Extension to spatially correlated D2D

When $M$ has AR(1) structure with correlation $\rho$, the covariance $\Sigma_M$ is no longer diagonal. The implicit regularizer becomes:
$$
\frac{1}{2} \sum_{i,j} W_i W_j (\Sigma_M)_{ij} \mathbb{E}\Big[\frac{\partial \ell}{\partial W_i}\frac{\partial \ell}{\partial W_j}\Big]
$$
— a **Fisher-matrix-weighted penalty anisotropic along spatial correlation directions**. Predicts that correlation degrades Ensemble HAT effectiveness, consistent with Supp Note S2 numerical result (ρ=0.3 → –1.76pp, ρ=0.5 → –4.20pp).

### 2.6 Bridge to heavy-tailed distributions

If measured D2D (pending PhD data) turns out heavy-tailed (kurtosis > 3), the second-order expansion breaks down earlier. Briefly note this as a limitation and point to potential higher-order correction using moments of the measured distribution directly. Don't derive — just flag as future work.

---

## 3. Deliverables

### 3.1 Supplementary Note S-Theory (3-4 pages)

Structure:
1. **Setup** (0.5 page): fixed-mask vs distribution-matching HAT formalism, per-epoch resampling discipline.
2. **First-order Taylor analysis** (1 page): derive the implicit regularization equivalence for Gaussian D2D.
3. **Comparison to dropout-as-L2 (Wager 2013)** (0.5 page): cite properly, explain structural analogy.
4. **Mechanistic explanation of fresh-instance generalization** (0.5 page): flat-region-in-M-direction argument.
5. **Extension to spatially correlated D2D** (0.5 page): AR(1) case, ties to Supp Note S2.
6. **Limitations: heavy-tailed regime** (0.5 page): flag for measured-D2D pass.

File path: `paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex`

### 3.2 Methods paragraph (~8 sentences, ~150 words)

Drop-in replacement for current Methods paragraph that defines Eq 8-style Ensemble HAT objective. Must:
- State Eq.~\ref{eq:hat-ensemble} in its distribution-matching form.
- Reference the Supp Note S-Theory for full derivation.
- State the implicit-regularization interpretation in one sentence.
- Note that this explains empirical transferability without needing additional hyperparameters.

File path: output as `paper/latex_gpt/sections/03_methodology_ensemble_hat_v2.tex.kimi_draft` (Kimi drafts, Claude integrates later).

### 3.3 Discussion paragraph (~4 sentences)

Insert into Discussion §6.1 (Principal Accuracy Bottlenecks) where Ensemble HAT is first discussed. State that Ensemble HAT's empirical effectiveness is now theoretically grounded, cite Supp Note S-Theory, and connect to the softer "flat-region-in-M-direction" intuition.

File path: `paper/latex_gpt/sections/06_discussion_ensemble_hat_paragraph.tex.kimi_draft`

---

## 4. Constraints and discipline

- **Cite properly**: Wager, Wang, Liang 2013 NeurIPS dropout=L2. Tobin 2017 domain randomization. EWC paper (Kirkpatrick 2017) for Fisher-penalty analog. Any analog CIM mismatch-aware training paper you find (Rasch 2023 IBM AIHWKit if relevant).
- **Do not claim novelty for the Taylor-expansion technique** — only for the application to hardware-mismatch-aware training with per-epoch resampling.
- **Keep math honest**: if the expansion fails at 2nd order or higher, say so. Don't handwave cross-terms.
- **No mention of bug-fix in theory note**. This is pure methodology. Bug discipline is in Supp Note S-Verification (separate dispatch).
- **No numeric results claimed from theory alone** — all quantitative support stays in Results section. The theory is mechanistic interpretation, not predictive model.
- **Length discipline**: Supp Note 3-4 pages firm. Methods paragraph ~150 words. Discussion paragraph ~4 sentences. Over-length is worse than under-length here.

---

## 5. Delivery protocol

1. Write to the three file paths in §3.
2. Append a status block to `AGENT_SYNC_gpt.md` when draft v0 ready.
3. Flag to Claude via `KIMI_THEORY_1_COMPLETE_<date>.md` summary file.
4. Claude will integrate + optionally ask Gemini for independent math check.

---

## 6. Success criteria

- Reviewer at Nat Electronics reading §3.2 Methods paragraph has a one-sentence answer to "why does Ensemble HAT work" that cites a formal derivation.
- Derivation chain Taylor → Gaussian → gradient-L2 is reproducible by any ML theorist in 1 hour.
- Wager 2013 analogy makes the contribution legible within existing implicit-regularization literature.
- Limitations (heavy-tails, higher-order terms) honestly stated.

**No time budget.** Do it right, not fast.
