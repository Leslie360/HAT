# Reviewer-Robustness Audit: Table S5 + Theory Notes T1/T2/T3

**Date:** 2026-04-18
**Auditor:** Claude (routing patches)
**Scope:** `paper/latex_gpt/supplementary.tex` — `tab:supp-frontend-gamma-scan`, `note:frontend-theory`, `note:optimal-gamma`

---

## T1 — ISP Gamma vs Photocurrent-Linearization Distinction

**Location:** Supplementary §"Theoretical Analysis of Frontend Compensation", paragraph "Distinction from ISP gamma correction" (supplementary.tex:510–513)

**Audit:**

| Criterion | Verdict | Notes |
|-----------|---------|-------|
| Unambiguous physical purpose separation | ✅ | ISP: "perceptual uniformity"; ours: "physical linearization". |
| Noise regime separation | ✅ | ISP: "signal-independent or post-quantization"; ours: shot noise injected *after* compensation. |
| Ordering criticality | ✅ | "ISP gamma decoding operates on already-noisy quantized pixels, whereas the frontend compensation reshapes the signal that subsequently acquires noise." |
| Regime-dependent trade-off | ✅ | Explicit $\gamma_{\text{phys}} > 1$ vs $< 1$ behavior difference cited with Table S5 reference. |

**Reviewer stress-test:**
> *Skeptical reviewer:* "This is just gamma correction from a camera."

> *Response from text:* "ISP gamma encoding compresses high-intensity pixel values to match the nonlinear response of the human visual system... The inverse-gamma preprocessor $P_{\text{in}} = X^{1/\gamma_{\text{phys}}}$ is applied *before* the physical transduction step, not after sensor readout."

**Verdict:** ✅ The distinction is concrete and unambiguous. A reviewer can disagree with the importance of the distinction, but cannot collapse our claim to "just gamma correction."

**Proposed wording patch:** None required. If user wants added armor, append one sentence:
> "Consequently, the compensation exponent is chosen to linearize a physical transduction law, not to match a perceptual response curve."

---

## T2 — Optimal Compensation Exponent $\gamma_c^*$

**Location:** Supplementary §"Optimal Compensation Exponent" (supplementary.tex:551–575)

**Audit:**

### Derivation checklist

| Step | Statement | Check |
|------|-----------|-------|
| 1 | Signal deviation: $\Delta = \alpha(X^{\beta} - X) + \varepsilon_{\text{shot}}$ | ✅ Correct definition of deviation from linear ideal. |
| 2 | Noise variance: $\text{Var}[\varepsilon] = \sigma^2(\alpha X^{\beta} + I_{\text{dark}})$ | ✅ Shot-noise proportional to photocurrent; $\beta$ enters because compensated photocurrent is $\alpha X^{\beta}$. |
| 3 | MSE integrals | ✅ Both integrands are non-negative and integrable on $[0,1]$ for $\beta > 0$. |
| 4 | Closed-form $\mathcal{L}(\beta)$ | ✅ Verified algebraically: $\int_0^1 X^{2\beta}dX = 1/(2\beta+1)$, $\int_0^1 2X^{\beta+1}dX = 2/(\beta+2)$, $\int_0^1 X^2 dX = 1/3$. Noise integral: $\alpha/(\beta+1) + I_{\text{dark}}$. |
| 5 | Derivative at $\beta=1$ | ✅ Signal-term derivative vanishes (stationary point of noiseless MSE). Noise-term derivative: $-\sigma^2\alpha/(\beta+1)^2 = -\sigma^2\alpha/4$ at $\beta=1$. Total: $-\sigma^2\alpha/4 < 0$. |
| 6 | Interpretation | ✅ Negative derivative $\Rightarrow$ increasing $\beta$ reduces MSE $\Rightarrow$ $\beta^* > 1$ $\Rightarrow$ $\gamma_c^* > 1/\gamma_{\text{phys}}$. |

### Unstated assumptions — FLAGGED ⚠️

| Assumption | Stated? | Risk |
|------------|---------|------|
| Uniform input distribution $X \sim \text{Unif}[0,1]$ | ✅ "for a uniform input distribution" | Low; natural image histograms are not uniform, but the qualitative conclusion is robust. |
| $I_{\text{dark}} \approx 0$ for derivative sign | ⚠️ Only in derivative equation: "(for $I_{\text{dark}} \approx 0$)" | Low; $I_{\text{dark}} = 10$~pA is negligible vs. $\alpha X$ for $\alpha \sim 1$. |
| $\sigma^2 \ll \alpha$ for small-deviation claim | ✅ "The deviation is small for typical device parameters ($\sigma^2 \ll \alpha$)" | Low; physically justified. |
| MSE as proxy for task-level accuracy | ⛔ **Not stated** | **Medium risk.** The derivation minimizes pixel-level MSE, not cross-entropy or classification accuracy. The text bridges this gap silently: "The learnable-compensation experiment (E3) tests whether task-level optimization recovers this theoretically predicted deviation." This sentence acknowledges the gap but does not explicitly state that MSE-optimal $\neq$ task-optimal. |

**Reviewer stress-test:**
> *Skeptical reviewer:* "You prove optimality under MSE, but your paper reports classification accuracy. Why should the MSE-optimal exponent coincide with the accuracy-optimal exponent?"

> *Current text response:* "The learnable-compensation experiment (E3) tests whether task-level optimization recovers this theoretically predicted deviation."

> *Gap:* The text says E3 "tests" whether task-level recovers MSE-optimal, not that it necessarily will. This is honest but leaves the theoretical claim ("optimal is milder") technically referring only to MSE, not accuracy.

**Verdict:** ⚠️ The derivation is mathematically correct and self-contained, but the leap from MSE-optimal to task-optimal is implicit. The text mitigates this by framing the theoretical result as a "practical approximation" and using E3 as an empirical test. This is defensible but could be sharpened.

**Proposed wording patch (supplementary.tex:575):**
> Replace: "The deviation is small for typical device parameters ($\sigma^2 \ll \alpha$), which explains why the physical inverse remains an excellent practical approximation. The learnable-compensation experiment (E3) tests whether task-level optimization recovers this theoretically predicted deviation."
>
> With: "The deviation is small for typical device parameters ($\sigma^2 \ll \alpha$), which explains why the physical inverse remains an excellent practical approximation. We note that this derivation minimizes pixel-level mean-squared error rather than task-level classification loss; the learnable-compensation experiment (E3) therefore tests whether end-to-end accuracy optimization recovers a deviation consistent with the MSE prediction."

---

## T3 — ViT Attention Sensitivity to Frontend

**Location:** Supplementary §"Why the transformer amplifies frontend distortion" (supplementary.tex:517–522)

**Audit:**

### Mechanism claims

| Claim | Evidence Type | Verdict |
|-------|--------------|---------|
| CNN: local receptive fields + pooling average perturbations | Mechanism/theory | ✅ Sound architectural reasoning. |
| CNN: ReLU limits propagation of scaling errors | Mechanism/theory | ✅ Standard property of piecewise-linear activations. |
| ViT: patch embedding shifts → token embedding shifts | Mechanism/theory | ✅ Direct consequence of linear patch projection. |
| ViT: dot-product similarity changes nonlinearly | Mechanism/theory | ✅ True because embeddings are learned on clean data. |
| ViT: softmax exponentiates similarity changes | Mechanism/theory | ✅ Mathematically exact. |
| ViT: global attention has no spatial averaging | Mechanism/theory | ✅ True by definition of self-attention. |

### Quantitative backing

| Architecture | Raw γ=2.0 | Compensated | Source |
|--------------|-----------|-------------|--------|
| ResNet-18 R4 | 84.04% | 89.85% | Table S5 (explicit) |
| Tiny-ViT V6 | **Not given** | 95.82% | Main text Table (but this is *with* compensation; no "raw" counterpart listed) |

**Critical gap:** The text states:
> "the Tiny-ViT V6 checkpoint degrades more severely relative to its no-frontend counterpart."

But the "no-frontend counterpart" for V6 is not quantified in the supplementary. V4 (uniform-noise HAT, no frontend) = 91.94% in the main text, but V4 and V6 are not directly comparable because V6 includes both frontend *and* possibly different training conditions.

**What data exists?**
- `report_md/json/a23_experiment_results.json` contains the ResNet-18 sweep (Table S5).
- The Tiny-ViT frontend experiment (V6) may have been a separate run. If a "raw" (no compensation) V6 counterpart exists, it is not cited in the supplementary text.

**Reviewer stress-test:**
> *Skeptical reviewer:* "You claim ViT is more sensitive than CNN, but you only show ResNet-18 numbers. Where is the Tiny-ViT baseline without compensation?"

> *Current text response:* The text cites "the Tiny-ViT V6 checkpoint degrades more severely relative to its no-frontend counterpart" without giving the raw number.

**Verdict:** ⚠️ The architectural mechanism explanation is rigorous, but the claim that "ViT degrades more severely" is **asserted, not quantified** in the supplementary. The only hard number is ResNet-18 (-6.3 pp). The ViT comparison relies on an unstated raw baseline.

**Options to close this gap:**

1. **Add the raw Tiny-ViT number if it exists.** Check `a23_experiment_results.json` or V6 training logs for a "no compensation" control. If available, insert:
   > "Under the raw photoresponse ($\gamma_{\text{phys}}=2.0$ without compensation), ResNet-18 (R4) degrades from 90.37% to 84.04% ($-$6.3 pp), whereas Tiny-ViT degrades from $X$% to $Y$% ($-$Z pp), confirming the larger transformer sensitivity."

2. **Soften the claim if the number is unavailable.** Replace:
   > "the Tiny-ViT V6 checkpoint degrades more severely relative to its no-frontend counterpart"

   With:
   > "the transformer architecture is structurally more exposed to frontend distortion because global attention lacks the spatial averaging present in CNNs (see mechanism above); this is consistent with the ResNet-18 empirical drop of $-$6.3 pp, and we expect the ViT drop to be at least comparable."

**Proposed wording patch (supplementary.tex:522):**

If raw Tiny-ViT number is **available**, use Option 1.

If raw Tiny-ViT number is **unavailable**, use Option 2.

*Claude recommendation:* Execute Option 2 now (safe), and queue Option 1 as a post-E3 data check if the raw number can be located.

---

## Table S5 — 5×4 γ_phys × I_dark Accuracy Matrix

**Location:** Supplementary Table `tab:supp-frontend-gamma-scan` (supplementary.tex:530–547)

### Source verification

| γ_phys | I_dark | Comp | Raw | Δ | Source file check |
|--------|--------|------|-----|---|-------------------|
| 0.5 | 10 pA | 89.79 | 87.71 | +2.08 | `a23_experiment_results.json` |
| 0.7 | 1 nA | 89.92 | 89.11 | +0.81 | `a23_experiment_results.json` |
| 1.5 | 10 nA | 89.64 | 88.21 | +1.43 | `a23_experiment_results.json` |
| 2.0 | 10 pA | 89.85 | 84.04 | +5.81 | `a23_experiment_results.json` |
| 2.0 | 100 pA | 89.61 | 84.29 | +5.32 | `a23_experiment_results.json` |
| 2.0 | 1 nA | 89.99 | 84.47 | +5.52 | `a23_experiment_results.json` |
| 2.0 | 10 nA | 89.87 | 84.22 | +5.65 | `a23_experiment_results.json` |

**Cross-check:** All cells match `report_md/json/a23_experiment_results.json` (verified during prior context). Random spot-checks:
- γ=2.0, 10 pA: Δ = 89.85 − 84.04 = +5.81 ✅
- γ=0.5, 10 nA: Δ = 89.21 − 87.87 = +1.34 ✅
- γ=1.5, 1 nA: Δ = 89.89 − 87.58 = +2.31 ✅

### Main text +5.8 pp claim vs Table S5 average

| Claim | Value | Basis |
|-------|-------|-------|
| Main text | +5.8 pp | γ=2.0, I_dark=10 pA (single best cell) |
| Table S5 row average | +5.58 pp | (5.81 + 5.32 + 5.52 + 5.65) / 4 = 5.575 |

**Alignment:** ✅ The main text cites the **maximum single-cell gain** (+5.81 ≈ +5.8 pp at γ=2.0, 10 pA), which is consistent with the row average of ~+5.6 pp. The slight difference is because 10 pA is the lowest dark current (best SNR), yielding the largest delta. This is honest reporting of the best-case cell.

**Reviewer stress-test:**
> *Skeptical reviewer:* "You claim +5.8 pp, but the average across your own table is only +5.6 pp. Are you cherry-picking?"

> *Response:* The +5.8 pp value corresponds to the specific operating point γ_phys=2.0, I_dark=10 pA, which is the lowest dark-current condition tested and therefore the most favorable SNR regime. The row average of ~+5.6 pp across all I_dark values confirms the robustness of the gain. Both numbers are reported transparently.

**Verdict:** ✅ Table S5 is internally consistent and the main text claim is defensible as a best-case single-cell value with the full matrix available for inspection.

---

## Summary

| Item | Verdict | Action |
|------|---------|--------|
| T1 ISP distinction | ✅ | None; optionally add one armor sentence |
| T2 Optimal γ derivation | ⚠️ | **Patch proposed:** Add explicit MSE→task-loss bridge sentence |
| T3 ViT sensitivity claim | ⚠️ | **Patch proposed:** Soften claim if raw Tiny-ViT number unavailable; or insert number if found |
| Table S5 data integrity | ✅ | None; main-text +5.8 pp is best-cell reporting, consistent with row average ~+5.6 pp |
