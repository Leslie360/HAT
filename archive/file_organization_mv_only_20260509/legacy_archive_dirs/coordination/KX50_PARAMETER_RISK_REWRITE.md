# KX50: Evidence-Grounded Parameter-Risk Rewrite

> **Date**: 2026-04-13  
> **Status**: COMPLETED  
> **Scope**: Replace star-rated matrix with evidence-grounded version using only manuscript-sourced facts

---

## Data Sources

All quantities below are derived from:
- `paper/latex_gpt/supplementary.tex` (Tables S2, S3, sensitivity data)
- `paper/latex_gpt/main.tex` (locked numbers)
- `report_md/_gpt/AGENT_SYNC_gpt.md` (Codex-confirmed blocks)

**No invented values. All placeholders explicitly labeled.**

---

## Evidence-Grounded Parameter Table

### Table SX: Parameter Provenance and Evidence Status

| Parameter | Source Literature | Manuscript Value | Evidence Status | What Manuscript Actually Shows |
|:----------|:------------------|:-----------------|:----------------|:-------------------------------|
| **τ₁ (fast retention)** | Vincze 2025 | 140 ms | **Measured-derived** | Vincze Fig. 2a dual-exponential fit; manuscript Section S1.3.1 |
| **τ₂ (slow retention)** | Vincze 2025 | 610 ms | **Measured-derived** | Same as above |
| **A₀ (amplitude ratio)** | Vincze 2025 | 0.6 | **Measured-derived** | Same as above |
| **G_max/G_min (canonical)** | Conservative | 10:1 | **Assumption** | Manuscript Section S1.3; "scalable OPECT regime" |
| **G_max/G_min (Zhang)** | Zhang 2025 | 47.3:1 | **Literature-extracted** | Zhang Fig. 3h max/min current levels |
| **n_states (canonical)** | Assumption | 16 (4-bit) | **Assumption** | "General low-precision target" |
| **n_states (Zhang)** | Zhang 2025 | 34 | **Literature-counted** | Zhang Fig. 3h & Supp.Fig. 8 distinguishable levels |
| **σ_C2C (canonical)** | Conservative | 5% | **Assumption** | Manuscript Section S1.3 |
| **σ_C2C (Zhang)** | Zhang 2025 | 2% | **Proxy estimate** | "8-cycle repeatability (Supp.Fig.15)" |
| **σ_D2D (canonical)** | Conservative | 10% | **Assumption** | Manuscript Section S1.3 |
| **σ_D2D (Zhang)** | Zhang 2025 | 3% | **Proxy estimate** | "~1% Vth spread" conductance-domain conversion |
| **NL (canonical LTP)** | Symmetric default | 1.0 | **Assumption** | "Symmetric writes" |
| **NL (canonical LTD)** | Symmetric default | -1.0 | **Assumption** | "Symmetric writes" |
| **NL (stress test)** | Physical estimate | ±2.0 | **Literature-informed** | Vincze indicates moderate nonlinearity; NL=2.0 is severe stress |

---

## Evidence-Grounded Sensitivity Matrix

### Table SY: Sensitivity Sweep Results (From Manuscript Table S3)

| D2D \ C2C | 1% | 2% (Nominal) | 5% | 8% |
|:----------|:---|:-------------|:---|:---|
| **2%** | 88.57% | 88.57% | 88.57% | 88.57% |
| **3% (Nominal)** | 88.53% | 88.53% | 88.53% | 88.53% |
| **5%** | 88.33% | 88.33% | 88.33% | 88.33% |
| **10%** | 87.30% | 87.30% | 87.30% | 87.30% |
| **15%** | 84.59% | 84.59% | 84.59% | 84.59% |

**Source**: `supplementary.tex` Table S3 (lines 89-104)

**What manuscript actually proves**:
- C2C variation 1-8% produces **0.00 pp** accuracy change at fixed D2D
- D2D variation 3%-15% produces **3.94 pp** degradation (88.53% → 84.59%)
- Conclusion: D2D dominates C2C in Ensemble HAT regime (manuscript-grounded)

---

## Evidence-Grounded Robustness Assessment

### What Manuscript Actually Tests

| Claim | Manuscript Evidence | Confidence |
|:------|:--------------------|:-----------|
| C2C invariance (scale-masking) | Table S3: 0.00 pp across 1-8% C2C | **High** (tested) |
| D2D dominance | Table S3: 88.53% → 84.59% as D2D increases | **High** (tested) |
| Ensemble HAT recovery | Main text: 10.00% → 86.37% (10 fresh instances) | **High** (tested) |
| 6-bit ADC cliff | Main text/Fig S1: ~27% at 4-bit, >80% at 6-bit | **High** (tested) |
| NL=2.0 unrecovered | Main text: 27.72% under gradient-scaling | **Moderate** (single point) |
| Retention uniformity | Table S8: <0.1 pp diff uniform vs state-dependent | **Moderate** (Ensemble-HAT-only test) |

### What Manuscript Does NOT Test (Explicitly Labeled)

| Quantity | Status | Required for Claim |
|:---------|:-------|:-------------------|
| τ₁, τ₂ sensitivity sweep | **Not yet bounded** | Cannot claim retention-robustness beyond Vincze values |
| NL scan (1.0, 1.5, 1.8, 2.0, 2.5) | **Not yet bounded** | Cannot claim "threshold" shape; only "unrecovered at 2.0" |
| ImageNet-scale validation | **Not performed** | Cannot claim generalization beyond CIFAR/Flowers |
| Per-forward i.i.d. D2D baseline | **Not performed** | Cannot quantitatively distinguish Ensemble HAT from i.i.d. |
| Pure-digital ADC sweep | **Not performed** | Cannot claim cliff is organic-CIM-specific vs ViT-quantization |

---

## LaTeX-Ready Parameter Risk Text

See separate file `KX50_LATEX_INSERT.tex` for ready-to-merge LaTeX code.

Key principles for insertion:
1. Use `\textbf{Measured-derived}` etc. for evidence status
2. Reference Table S3 for sensitivity bounds
3. Use `\textit{not yet bounded}` for untested parameters
4. Never claim universal robustness beyond tested ranges

---

## Comparison: Old vs. New Approach

| Aspect | Old (KX41) | New (KX50) |
|:-------|:-----------|:-----------|
| Robustness stars | Invented (5-star) | Removed; replaced with evidence status |
| Physical ranges | Estimated | Labeled "not yet bounded" if not in manuscript |
| Confidence claims | Implied high | Explicitly scoped to tested ranges |
| Value to Codex | Template structure | Evidence-grounded content |

---

## Summary

This rewrite provides:
1. **Strict evidence grounding**: All values from manuscript source files
2. **Explicit uncertainty labeling**: "Not yet bounded" clearly marked
3. **Defensible claims**: Only what manuscript actually tests
4. **No invented robustness stars**: Replaced with evidence status categories

**Ready for Codex review.**
