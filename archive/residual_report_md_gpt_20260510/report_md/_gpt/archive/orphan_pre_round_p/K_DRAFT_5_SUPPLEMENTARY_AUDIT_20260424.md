# K-DRAFT-5: Supplementary.tex Audit Report
**Date:** 2026-04-24
**Auditor:** Kimi
**File:** `paper/latex_gpt/supplementary.tex` (811 lines, 63,175 bytes)

## Executive Summary

`supplementary.tex` contains **minimal direct contamination** from the bug-contaminated severe-NL narrative. The main-text §5.x figures (structural ceiling, bimodal basin, Hartigan p=0.98, J1–K5 sweep) are **not referenced** in the supplementary material. However, one ablation table embeds pre-fix NL=2.0 baseline numbers that are bug-contaminated and must be flagged.

| Severity | Count | Action |
|:---------|:-----:|:-------|
| 🔴 **Critical** | 1 table row | Flag for post-fix re-evaluation |
| 🟡 **Moderate** | 2 fresh-transfer numbers | Qualitative conclusion holds; numeric update pending |
| 🟢 **Clean** | >95% of file | No action needed |

---

## Detailed Findings

### 🔴 Critical: Table `tab:supp-nl-ablation` row (b)

**Location:** Lines 783–784

```latex
(b)~None ($NL=2.0$ global) & $27.72\pm0.82$ & $27.72\pm0.82$ & $0.00$ \\
```

**Issue:** This is the pre-fix Standard HAT @ NL=2.0 baseline for the group-wise ablation. The value 27.72% was obtained with bug-contaminated `analog_layers.py` (branch swap + extraneous nl multiplier at commit pre-33bed9c). It serves as the reference point ($\Delta = 0.00$) against which all protected-group rows are compared.

**Impact:** All $\Delta$ values in the table (e.g., MLP-only +60.07 pp, QKV-only −9.00 pp) are computed relative to a contaminated baseline. The **qualitative ranking** (MLP protection >> attention protection) may still hold because the bug affects all NL=2.0 layers uniformly, but the **absolute numeric deltas** are unreliable.

**Recommendation:**
- **Do not delete** the table — it is a valuable ablation design.
- **Flag row (b)** with a footnote: "Pre-fix baseline; post-fix re-evaluation pending (CX-M1)."
- **Re-evaluate** the entire ablation with post-fix code after M1 lands.

---

### 🟡 Moderate: Fresh-instance transfer numbers in ablation interpretation

**Location:** Line 792 (interpretation paragraph)

```latex
... the MLP-linearized checkpoint achieves only $32.12\pm7.72$\% fresh-instance
transfer accuracy ... The all-linear upper-bound control behaves similarly
under fresh-instance transfer, reaching only $32.60\pm9.18$\% ...
```

**Issue:** These fresh-instance transfer evaluations were performed on pre-fix checkpoints (trained with NL=2.0 global, bug-contaminated STE). The transfer protocol itself (eval at NL=2.0) is correct, but the underlying checkpoint weights were trained with wrong gradients.

**Impact:** The conclusion — "linearizing every analog block still does not restore deployment-grade transfer" — is **qualitatively robust** because the all-linear control (NL=1.0 all layers) reaches 87.49% same-instance, so the fresh-instance collapse to ~32% is a genuine generalization failure, not a bug artifact. However, the exact 32.12% and 32.60% numbers are not trustworthy.

**Recommendation:**
- Flag with placeholder: "Pre-fix checkpoint; post-fix re-evaluation pending."
- The qualitative conclusion (linearization insufficient for deployment) is safe to keep.

---

### 🟢 Clean: All other content

The following sections are **bug-immune** and require no action:

| Section | Lines | Why clean |
|:--------|:------|:----------|
| ResNet-18 / Tiny-ViT CIFAR-10 baselines | 161–176 | NL=1.0 canonical; bug does not manifest |
| Front-end compensation (V6) | 529–547 | NL=1.0 canonical; photoresponse ablation |
| ADC calibration / sensitivity tables | 639, 748 | NL=1.0 canonical |
| Cross-framework sanity check (CrossSim) | 716, 795 | Uses canonical NL=1.0 checkpoint + matched noise |
| Standard HAT collapse @ NL=1.0 | 795 | 10.00±0.00% is canonical bug-immune result |
| Correlated-D2D stress test | 804 | Uses canonical Ensemble HAT checkpoint (NL=1.0) |
| SNR curves / retention / IR drop | Various | NL=1.0 or peripheral non-ideality |

**Confirmed absent from supplementary.tex:**
- No mention of "30% structural ceiling"
- No mention of "bimodal basin" or Hartigan's dip
- No J1b/J1d, K2–K5 experiment references
- No 38.95%, 41.53%, 30.53% numbers
- No proportional HAT 90.88% claim

---

## Action Table

| # | Line | Text | Status | Recommended Action |
|:-:|:-----|:-----|:------:|:-------------------|
| 1 | 783 | `$27.72\pm0.82$` (row b) | 🔴 Contaminated | Add footnote: pre-fix baseline; pending post-fix re-eval |
| 2 | 792 | `$32.12\pm7.72$\%` | 🟡 Contaminated | Add footnote: pre-fix checkpoint; pending re-eval |
| 3 | 792 | `$32.60\pm9.18$\%` | 🟡 Contaminated | Add footnote: pre-fix checkpoint; pending re-eval |
| 4 | 783–790 | Entire `tab:supp-nl-ablation` | 🟡 Mixed | Keep table; flag baseline row; re-evaluate post-fix |
| 5 | All other lines | — | 🟢 Clean | No action |

---

## Audit Method

1. Grep search for all known contaminated numbers: 30.53, 38.95, 41.53, 27.72, 90.88, Hartigan, bimodal, structural ceiling, J1b, J1d, K2–K5.
2. Contextual read of hit regions (±10 lines).
3. Manual verification of each table/checkpoint source against bug-immunity scope (§1 of broadcast).
4. Cross-reference with `json_gpt/` filenames to confirm provenance where possible.

---

## Conclusion

`supplementary.tex` is **largely clean**. The only contamination is localized to the NL=2.0 ablation table (`tab:supp-nl-ablation`) and its interpretation paragraph. Because the supplementary material does not repeat the main-text §5.x severe-NL narrative, the damage is contained. After M1 lands, the ablation should be re-run with post-fix code; until then, a footnote suffices.
