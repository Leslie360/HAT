# R10C: OPECT Distribution vs. Canonical Gaussian Prior — Zero-Shot Transfer Defense

**Date:** 2026-04-25  
**Task:** R10C (Claude Round-10 dispatch)  
**Analyst:** Kimi Code CLI  
**Sources:** `literature_profiles_gpt.json`, `literature_profile_zhang2025_provenance_gpt.md`

---

## 1. Available OPECT Statistics Summary

Profile under analysis: **"Organic OPECT Zhang2025 Literature-Fitted"**

| Parameter | Value | Status | Evidence |
|:--|--:|:--|:--|
| `sigma_d2d` | **0.03** (3 %) | Proxy estimate | V_th spread across 80 devices (Fig. 3b/c): dark mean = −1.50 V, std = 0.01 V (~0.67 %); light mean = −1.37 V, std = 0.02 V (~1.46 %). Value is a conservative conductance-domain uplift from threshold-voltage statistics, **not** a direct conductance histogram. |
| `sigma_c2c` | **0.02** (2 %) | Proxy estimate | Supplementary Fig. 15 (8-cycle LTP/LTD repeatability) and Fig. 3g (three reproducible curves). No explicit conductance-domain sigma reported; 0.02 is a transparent proxy. |
| Distribution shape | **Unknown / unreported** | Missing | No direct conductance-domain D2D histogram has been identified in the main paper or current extraction package. The simulator uses a Gaussian prior; whether the true OPECT distribution is Gaussian, log-normal, skewed, or multimodal cannot be determined from the available literature. |
| `G_max / G_min` | 47.3 | Direct-normalized | Abstract / Results / Fig. 3h / Supplementary Fig. 8 |
| `n_states` | 34 | Direct-conservative | Explicitly reported as "34 distinguishable conductance states" |

**Key bibliographic anchor:** Zhang et al., *Nature Communications* 17, 197 (2026), doi:10.1038/s41467-025-66891-6.

---

## 2. Comparison to Canonical Gaussian Prior

The framework’s canonical training prior ("Organic OPECT Standard") is:

| Parameter | Canonical prior | OPECT (Zhang2025) | Ratio |
|:--|--:|--:|--:|
| `sigma_d2d` | **0.10** (10 %) | 0.03 (3 %) | **3.3× lower** |
| `sigma_c2c` | **0.05** (5 %) | 0.02 (2 %) | **2.5× lower** |
| Distribution shape | Gaussian (by construction) | Unknown | — |

**Interpretation:** The OPECT literature profile occupies a **parameter-shifted regime** relative to the canonical training prior. The simulator is trained with a Gaussian noise model whose spread is substantially wider than the proxy-estimated OPECT spread. This is a **distribution-parameter mismatch** (different variance) rather than a **distribution-shape mismatch** (e.g., Gaussian vs. log-normal), because the shape of the true OPECT distribution is simply not reported.

### Why this matters for the zero-shot transfer claim

A strong "zero-shot transfer" or "mismatch-distribution-shape invariance" claim would require evidence that the framework generalizes across *different distribution families* (e.g., trained on Gaussian, tested on uniform or empirical histogram). The OPECT case study does **not** provide that evidence, because:

1. We do not know the true OPECT distribution shape.
2. The OPECT proxy estimates are *lower-variance* versions of the same broad Gaussian-like regime the simulator already sees during training.
3. The 88.53 ± 0.08 % accuracy result therefore demonstrates **profile-substitution robustness under a parameter-shifted regime** — a valid but weaker claim than shape invariance.

---

## 3. Honest Assessment: What Can and Cannot Be Claimed

### ✅ Safe claims

- The framework successfully ingests a literature-derived OPECT profile with transparent proxy estimates.
- The simulator achieves **88.53 ± 0.08 %** accuracy on CIFAR-10 using the OPECT profile, comparable to or within variance of the canonical prior result.
- This demonstrates **profile-substitution robustness**: swapping device parameters (G_max, n_states, sigma_d2d, sigma_c2c) without retraining the stochastic regularization ensemble does not degrade accuracy.
- The OPECT D2D variability (~3 % proxy) is lower than the canonical training prior (10 %), showing the framework tolerates a **lower-bound shift** in mismatch variance.

### ❌ Unsafe claims

- "The framework generalizes to the true OPECT empirical distribution." (We do not have the true distribution.)
- "The framework is invariant to mismatch-distribution shape." (No shape information is available; the test uses the same Gaussian sampler with different variance.)
- "All OPECT parameters are directly measured." (sigma_d2d and sigma_c2c are proxy estimates; retention and nonlinearity parameters are withheld.)
- "This single case study fully validates the framework." (It is one literature bridge; full validation requires hardware-calibrated data.)

### ⚠️ Nuanced claims (require explicit qualification)

- "Zero-shot transfer to OPECT" — acceptable only if qualified as **"literature-profile zero-shot transfer"** or **"parameter-substitution zero-shot transfer"**, explicitly distinguishing it from hardware-calibrated zero-shot transfer.

---

## 4. Recommended Paper-Safe Paragraph for §5.8 (OPECT Case Study)

> The OPECT D2D variability (σ≈3%, proxy-estimated from V_th spread across 80 devices) is lower than our canonical training prior (σ=10%), and the conductance-domain distribution shape is not directly reported in the source literature. The 88.53±0.08% accuracy therefore demonstrates profile-substitution robustness under a parameter-shifted regime rather than mismatch-distribution-shape invariance, the latter pending hardware-calibrated data.

**Rationale for this wording:**
- "σ≈3%, proxy-estimated" — transparently flags the estimate nature.
- "not directly reported" — honest about missing data.
- "profile-substitution robustness under a parameter-shifted regime" — precise, defensible claim.
- "rather than mismatch-distribution-shape invariance" — explicitly closes the door on the stronger but unsupported claim.
- "pending hardware-calibrated data" — signals future work and invites reviewers to accept the honest framing.

---

## 5. Supplementary LaTeX Note

A short supplementary note (`S_opect_distribution.tex`) has been generated for the paper’s supplementary materials, providing the same analysis in academic LaTeX form with a parameter comparison table and explicit caveats.

---

## 6. Outcome Classification

**Outcome C** — *Honest framing required.*

> OPECT conductance-domain distribution data unavailable in paper SI; the analysis must be presented as parameter-shift profile-substitution robustness, not as distribution-shape invariance.

This outcome is the most scientifically defensible position given the evidence currently in hand. If future digitization of Supplementary Fig. 15 or a direct conductance-uniformity histogram becomes available, the classification can be revisited.
