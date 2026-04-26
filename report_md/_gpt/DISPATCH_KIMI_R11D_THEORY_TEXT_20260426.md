# DISPATCH KIMI R11D — Cadence Theory + AIHWKit Comparison Text
**Date:** 2026-04-26 16:50 CST
**Issued by:** Claude
**Assignee:** Kimi
**Authority:** CLAUDE_ROUND11D_PATH_C_EXPLORATION_PLAN
**Priority:** HIGH (parallel to DS experiments)
**Time budget:** ~2 days (interleave with R11C paper fix-it pass)

---

## 0. Mission

Explain the per-batch vs per-epoch cadence difference theoretically and operationally, given AIHWKit's surprising 87.34% (vs our per-batch 86.16%). Two deliverables: cadence comparison memo + theoretical addendum to KIMI-THEORY-2.

---

## 1. R11D-5 — Cadence comparison memo (~6 hours)

### Operational question
AIHWKit per-batch noise injection: **87.34%** fresh-instance.
Our per-batch cadence in §5.7 ablation: **86.16%**.

These are nominally the same cadence, but AIHWKit beats us by 1.18 pp. **What's actually different?**

### Investigation steps

#### 1.1 Code-level comparison
Read AIHWKit's noise injection mechanism:
- `aihwkit/nn/conversion.py` — analog conversion path
- `aihwkit/simulator/parameters/inference.py` — `WeightModifierParameter` definition
- `aihwkit/simulator/tiles/inference.py` — when modifier is applied (per forward pass? per training step?)

Read our per-batch cadence in `analog_layers_ensemble.py`:
- Where is `resample_d2d_noise` called?
- Per training step? Per forward pass? Per MC sample?

Document where the noise samples are drawn — there's likely a subtle difference (per-forward-pass with weight-noise vs per-step).

#### 1.2 Numerical sanity check
Spot-check the actual noise statistics:
- Run 10 forward passes on AIHWKit at canonical config; record per-pass weight modifications
- Run 10 forward passes on our per-batch Ensemble HAT; record per-pass weight modifications
- Compare: variance, autocorrelation, period

#### 1.3 Operational hypothesis
**Most likely**: AIHWKit's `WeightModifier.ADD_NORMAL` resamples noise EVERY forward pass (per minibatch in train mode); our per-batch implementation resampled less frequently. If true → cadence is per-mini-batch (more granular than we labeled).

If hypothesis confirmed: this is paper-grade — **the per-epoch ablation in §5.7 should be re-run with three cadences clearly defined: per-minibatch (=AIHWKit) / per-epoch (=ours, if reproduces 88.41) / fixed**.

### Deliverable
- `KIMI_R11D5_CADENCE_COMPARISON_REPORT_20260426.md`
- Optional: 1-page Supp Note `S_cadence_comparison.tex` if findings are strong

---

## 2. R11D-T1 — Theoretical addendum: per-batch vs per-epoch under noise

### Question
KIMI-THEORY-1/2 derived per-epoch resampling as **distribution-matching objective** (implicit gradient-L2 + SAM). What does **per-batch** (AIHWKit-style) imply?

### Hypothesis
Per-batch noise injection during SGD is closer to:
- **Stochastic regularization** (Wager 2013 dropout = L2 — implicit L2 penalty proportional to noise variance)
- **Bayesian SGD** with Gaussian noise prior — equivalent to MAP estimation under L2 prior

vs per-epoch is:
- **Distribution-matching** in the sense of Tobin 2017 domain randomization — minimize expected loss over distribution of perturbations
- **SAM-along-D2D-direction** — implicit sharpness-aware minimization

### Sketch
For Gaussian noise σ added per-iteration to weight $W$:
- Per-batch SGD with noise = SGD on smoothed loss $\tilde{L}(W) = \mathbb{E}_{\xi \sim N(0,\sigma^2)} L(W+\xi)$
- Per-epoch sample-and-fix = SGD on stochastic instance of $L(W+\xi)$ for fixed $\xi$ over an epoch

In the limit: per-batch ≡ smoothed loss optimization (= L2 penalty); per-epoch ≡ stochastic instance optimization (≠ L2 in general).

For finite training: both convergence to L2-like regularization, but at different rates.

**Empirical implication (testable)**:
- At low noise σ: per-batch ≈ per-epoch
- At high noise σ: per-batch may diverge (over-regularization), per-epoch may underfit (only N_epoch samples seen)
- At low data: per-epoch may overfit (correlated samples within epoch)

R11D-2 / R11D-3 results (high σ) test this: if per-batch (AIHWKit) collapses at σ=0.20 but per-epoch (Ensemble HAT) survives → theoretical prediction confirmed.

### Deliverable
- `paper/latex_gpt/supplementary/S_cadence_comparison.tex` — 1-2 pages
- Section structure:
  - §S.cad.1 Operational definitions (per-minibatch / per-epoch / fixed)
  - §S.cad.2 Theoretical comparison (smoothed loss vs distribution matching)
  - §S.cad.3 Predictions about regime where each wins
  - §S.cad.4 Empirical confirmation (cite R11D-2/3 results when they land)

### Cite properly
- Wager, Wang, Liang 2013 (per-batch dropout = L2)
- Tobin et al. 2017 (per-iteration domain randomization)
- Foret et al. 2021 SAM (sharpness-aware minimization)

---

## 3. AIHWKit Discussion text (after R11D-1 through R11D-4 land)

Once DS finishes Path C exploration, write the Discussion §6.x AIHWKit comparison paragraph. Three branches depending on outcome:

### Branch A — AIHWKit collapses in some regime, Ensemble HAT survives
> "Direct comparison to AIHWKit \citep{rasch2021aihwkit} reveals a regime-dependent pattern. At canonical settings (σ=0.10, 8-bit ADC), both AIHWKit (87.34±0.14%) and Ensemble HAT (86.16±0.19%) achieve cross-instance robustness, validating the general principle of stochastic noise injection. **However, at <stress regime>** (e.g., 4-bit precision / σ=0.20 / PCM device model), AIHWKit drops to <X.XX%>, while Ensemble HAT retains <Y.YY%>—a <gap> pp advantage. We attribute this to <mechanism: cadence / structure / per-epoch consistency>. Section §S-cadence-comparison provides the theoretical analysis."

### Branch B — AIHWKit survives everywhere
> "Direct comparison to AIHWKit \citep{rasch2021aihwkit} reveals that across all stress regimes tested (4-bit precision, σ=0.20, PCM device), AIHWKit achieves cross-instance robustness comparable to Ensemble HAT. Both methods successfully address hardware-instance overfitting through noise injection during training. Our contribution thus lies not in method superiority, but in (i) explicit diagnosis and naming of the failure mode (Standard HAT 10.00% collapse), (ii) substrate-specific application to organic optoelectronic CIM, (iii) theoretical framework demonstrating implicit regularization in the per-epoch resampling regime, and (iv) full operating-envelope characterization complementing AIHWKit's training-side focus."

### Branch C — Mixed/regime-dependent
Compose hybrid honestly.

---

## 4. R11D + R11C interaction

R11C (paper fix-it) and R11D (cadence + AIHWKit) are concurrent. Strategy:
- R11C is "must-do regardless of R11D outcome" — paper integrity issues
- R11D adds NEW content (AIHWKit comparison + cadence theory)
- Net word budget: R11C reduces ~1200 (move appendix to supp) + R11D adds ~400-600 (AIHWKit + cadence) = net ~5,000-5,400 words

This is fine for Nat Electronics envelope.

---

## 5. Workflow

### Day 1
- Morning: R11D-5 cadence code inspection (AIHWKit + ours)
- Afternoon: R11D-5 cadence memo writing
- Evening: R11D-T1 theoretical sketch

### Day 2
- Morning: R11D-T1 theory addendum writing
- Afternoon: integrate into supplementary
- Evening: standby for R11D experimental results

### Day 3-5 (when DS results land)
- Write Discussion §6 AIHWKit comparison paragraph (one of 3 branches)
- Coordinate with Gemini for R11D-T2 envelope plot

### Day 6 (R11C continuation)
- Continue R11C paper fix-it items (interleaved)

---

## 6. Hard constraints

- **No NEW empirical numbers** — only synthesize what DS produces
- **No fake placeholder numbers** — use [PENDING_R11D_X] tags
- **Zone discipline**: any R11D number gets new zone tag (Zone 4 = AIHWKit comparison? Or just "AIHWKit baseline" with explicit citation)
- **Cite Tobin/Wager/Foret/Rasch properly**

---

## 7. Deliverables

| File | Action |
|:--|:--|
| `KIMI_R11D5_CADENCE_COMPARISON_REPORT_20260426.md` | NEW (operational comparison) |
| `paper/latex_gpt/supplementary/S_cadence_comparison.tex` | NEW (theoretical addendum) |
| `paper/latex_gpt/sections/06_discussion.tex` | EDIT (AIHWKit comparison paragraph after R11D lands) |
| `KIMI_R11D_INTEGRATION_REPORT_20260426.md` | NEW status updates |

---

## 8. Cold-start refs

- `CLAUDE_ROUND11D_PATH_C_EXPLORATION_PLAN_20260426.md` — master plan
- `KIMI_THEORY_1_COMPLETE_20260424.md` + `KIMI_THEORY_2_COMPLETE_20260425.md` — base theory
- `paper2_aihwkit_baseline/train_aihwkit_baseline.py` + AIHWKit `aihwkit/simulator/` — code-level investigation
- `analog_layers_ensemble.py` — our resample mechanism

**Time budget**: ~2 days theoretical + 4-6 hours integration. Interleave with R11C paper fix-it.
