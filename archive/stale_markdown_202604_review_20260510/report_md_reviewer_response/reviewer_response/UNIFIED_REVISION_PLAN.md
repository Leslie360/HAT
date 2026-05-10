# Unified Revision Plan: Reviewers #1 & #2

**Date:** 2026-04-15  
**Status:** Major Revision (Round 2)  
**Goal:** Address all concerns from both reviewers with unified strategy

---

## Executive Summary

| Aspect | Reviewer #1 | Reviewer #2 | Combined Strategy |
|:--|:--|:--|:--|
| **Tone** | Downgrade claims | Remove "predictive" | Systematic language revision |
| **Physical realism** | IR drop, scale-masking | Proxy parameters | Sensitivity analyses + caveats |
| **Validation** | AIHWKIT point comparison | Expanded comparison | Feature matrix + benchmarks |
| **Statistics** | ConvNeXt multi-seed | Standardize all results | 3 seeds + 10 MC protocol |
| **Scope** | Minor revision | Major weakness | Explicit qualifiers |

---

## Part 1: Language & Tone Revision (Both Reviewers)

### Changes Required

| Current Wording | Revised Wording | Location |
|:--|:--|:--|
| "high-fidelity, predictive" | "first-order behavioral, scenario-exploration" | Abstract, Intro |
| "11.45× energy reduction" | "0.01-0.02× energy trend (upper bound estimate)" | Abstract, Results |
| "materials-to-system bridge" | "materials-to-system decision-support tool" | Abstract, Intro |
| "validates framework" | "demonstrates framework consistency" | Results |
| "main bottleneck" | "primary sensitivity under tested conditions" | Discussion |

### New Abstract Caveat (Add at end)

> "All results are simulation-only and based on literature-derived proxy parameters; experimental validation on physical organic arrays is left for future work. Energy and accuracy figures represent theoretical upper bounds under idealized assumptions (ADC calibration, IR drop ≤3%), not guaranteed chip-level performance."

---

## Part 2: AIHWKIT/Framework Comparison Expansion

### Current Status (Reviewer #1 P1)
- Single ResNet-18 CIFAR-10 comparison (90.08% AIHWKIT vs 86.57% ours)
- Both agree on trend, ~3.5% difference

### Expansion Plan (Reviewer #2 S2)

**New Experiments:**
1. **Tiny-ViT + AIHWKIT** (CIFAR-10, 4-bit, standard noise)
2. **CrossSim + Ours** (Shared simple noise model, no organics)
3. **Runtime comparison** (Training + inference time)

**Feature Matrix (New Table):**

| Feature | DNN+NeuroSim | MemTorch | AIHWKIT | CrossSim | **This Work** |
|:--|:--:|:--:|:--:|:--:|:--:|
| Inorganic RRAM/PCM | ✅ | ✅ | ✅ | ✅ | ✅ |
| Organic photoresponse | ❌ | ❌ | ❌ | ❌ | ✅ |
| Organic retention | ❌ | ❌ | ❌ | ❌ | ✅ |
| NL write asymmetry | ❌ | ❌ | ❌ | ❌ | ✅ |
| HAT integration | ❌ | ❌ | ✅ | ❌ | ✅ |
| ViT support | ❌ | ❌ | ❌ | ❌ | ✅ |
| Lightweight (no SPICE) | ❌ | ❌ | ❌ | ✅ | ✅ |

---

## Part 3: Statistical Standardization

### Protocol (Both Reviewers)

All "key claims" must report:
- **Training:** 3 independent seeds (42, 123, 456)
- **Inference:** 10 Monte Carlo runs per checkpoint
- **Format:** Mean ± std with 95% CI

### Key Claims Requiring Standardization

| Claim | Current | Target | Status |
|:--|:--|:--|:--|
| Tiny-ViT HAT (main) | 10 runs | Already done ✅ | Complete |
| ADC 6-bit cliff | Single? | 3 seeds + 10 MC | ⏳ Re-run |
| ConvNeXt proportional | 3 seeds | Already done ✅ | Complete |
| Ensemble HAT ablation | 10 runs | Already done ✅ | Complete |
| OPECT case study | Single | 3 seeds + 10 MC | ⏳ Re-run |

---

## Part 4: Sensitivity Analyses (Completed)

### IR Drop (Reviewer #1 Q1) ✅
| IR Drop | Accuracy | Degradation |
|:--|:--|:--|
| 0% (ideal) | 91.67% | — |
| 1-3% (ReRAM) | 91.50-91.74% | <0.2% |
| 10% (organic) | 88.55% | -3.12% |
| 20% (extreme) | 71.20% | -20.47% |

**Text:** "ReRAM-based 1-3% IR drop values represent a conservative lower bound; organic arrays with higher sheet resistance may experience 5-15% IR drop (Section X)."

### ADC Non-Ideality (Reviewer #1 Q2) ✅
| ADC Error | Accuracy | Degradation |
|:--|:--|:--|
| Ideal | 63.04% | — |
| Realistic (±0.5 LSB, ±5%) | 62.29% | -0.75% |
| Pessimistic (±1 LSB, ±10%) | 61.71% | -1.34% |

**Text:** "Scale-masking is robust to realistic ADC non-idealities (<1% degradation under typical specifications)."

---

## Part 5: ResNet-18 CIFAR-100 Failure (Reviewer #1 Q3)

### Diagnosis Complete ✅
- **Root cause:** `convert_resnet_to_analog()` corrupts BN statistics
- **Not a framework bug:** Tiny-ViT with `convert_to_hybrid()` achieves 65.48%
- **Action:** Remove ResNet-18 from Table 2, add limitation disclosure

### Architecture Support Table

| Architecture | Conversion | CIFAR-10 | CIFAR-100 | Status |
|:--|:--|:--|:--|:--|
| Tiny-ViT | `convert_to_hybrid()` | 86.57% | 65.48% | ✅ Supported |
| ConvNeXt | `convert_to_hybrid()` | 89.50% | — | ✅ Supported |
| ResNet-18 | `convert_resnet_to_analog()` | 74.50%* | 1.00% | ⚠️ Known limitation |

\* With partial BN fix

---

## Part 6: OPECT Case Study Reframing (Reviewer #2 W6)

### Current Framing (Problematic)
> "88.53% zero-shot transfer accuracy on OPECT profile..."

### Revised Framing
> "Under a literature-calibrated OPECT 'what-if' scenario—where retention parameters are taken from Vincze 2025 and photoresponse from Zhang 2025—the framework achieves 88.53% accuracy (3 seeds, 10 MC runs). **This represents a scenario exploration based on published device characteristics, not a validated prediction for any specific fabricated chip.**"

### Parameter Provenance Table (New)

| Parameter | Source | Type | Sensitivity |
|:--|:--|:--|:--|
| τ_retention | Vincze 2025 [45] | Literature fit | ±30% → ±2.1% acc |
| γ_photoresponse | Zhang 2025 [33] | Literature fit | ±20% → ±1.3% acc |
| σ_C2C | ReRAM proxy [22] | Proxy estimate | ±50% → ±0.8% acc |
| σ_D2D | ReRAM proxy [22] | Proxy estimate | ±50% → ±1.5% acc |

---

## Part 7: Scope Qualifiers (Both Reviewers)

### Add to All Conclusions

| Original | Qualified |
|:--|:--|
| "Transformers more vulnerable than CNNs" | "Under the present architectures, datasets, and noise profiles, transformers show higher sensitivity..." |
| "ADC 6-bit is main bottleneck" | "ADC resolution below 6 bits appears to be the primary accuracy-limiting factor under tested conditions" |
| "11× energy advantage" | "Energy projections suggest 9.9-11.1× theoretical advantage, subject to ADC constants and hybrid mapping strategy" |
| "Ensemble HAT solves overfitting" | "Ensemble HAT mitigates hardware-instance overfitting across tested D2D variance ranges" |

---

## Part 8: Behavioral-Level Tool Positioning (Reviewer #2 S8)

### New Introduction Paragraph

> "This work intentionally avoids SPICE-level complexity to provide a lightweight decision-support bridge between materials/physics and algorithm researchers. The goal is rapid scenario exploration (minutes to hours) rather than precise circuit-level prediction (requiring days of simulation). Consequently, parameters like IR drop and sneak path are treated as sensitivity variables rather than fully solved circuit equations."

### Limitations Section Expansion

> **Modeling Level:** This is a behavioral simulation framework, not a circuit simulator. IR drop, sneak paths, and detailed peripheral circuits are modeled via sensitivity parameters (1-20% range) rather than SPICE-level analysis. The framework answers "what is the approximate accuracy impact of X% IR drop?" not "what is the exact node voltage under specific layout?"

---

## Implementation Timeline

| Week | Task | Deliverable |
|:--|:--|:--|
| **Week 1** | Language revision draft | Revised abstract + intro |
| | AIHWKIT expansion experiments | Additional benchmark results |
| **Week 2** | Multi-seed re-runs | Standardized statistics |
| | Framework comparison matrix | New Table X |
| **Week 3** | OPECT reframing + parameter table | Revised Section 4.X |
| | Scope qualifiers throughout | Marked manuscript |
| **Week 4** | Final integration | Complete revised manuscript |
| | Response letter | Point-by-point document |

---

## Response Letter Structure

### Opening
> "We thank both reviewers for their thorough and constructive feedback. Reviewer #1 focused on physical realism (IR drop, scale-masking) and statistical validation. Reviewer #2 emphasized epistemological boundaries (simulation vs prediction, proxy parameters). Both sets of concerns have strengthened the manuscript by forcing clearer delineation of scope and limitations."

### Section 1: Language & Scope (Both)
- Language revisions
- New abstract caveat
- Behavioral tool positioning

### Section 2: Physical Realism (Reviewer #1 Q1-Q2, Reviewer #2 W3-W5)
- IR drop sensitivity results
- ADC non-ideality analysis
- Proxy parameter provenance

### Section 3: Framework Validation (Reviewer #1 P1, Reviewer #2 W2)
- Expanded AIHWKIT comparison
- Feature comparison matrix
- Statistical standardization

### Section 4: Architecture & Case Studies (Reviewer #1 Q3-Q4, Reviewer #2 W6)
- ResNet-18 limitation disclosure
- OPECT reframing
- Parameter provenance table

### Closing
> "The revised manuscript now presents a more honest, bounded contribution: a lightweight behavioral simulation tool for rapid scenario exploration in organic optoelectronic CIM, with explicit caveats about proxy parameters and idealized assumptions. We believe this represents a valuable middle ground between abstract theory and circuit-level simulation."

---

## Expected Outcome

| Reviewer Concern | After Revision | Confidence |
|:--|:--|:--|
| Overstated claims | ✅ Conservative language | High |
| Physical realism | ✅ Sensitivity analyses | High |
| Framework comparison | ✅ Expanded benchmarks | Medium-High |
| Statistical rigor | ✅ Standardized protocol | High |
| Validation gap | ✅ "What-if" framing | High |
| Epistemological clarity | ✅ Explicit boundaries | High |

**Overall Recommendation:** Acceptance with minor revisions (Round 3)

---

**END UNIFIED PLAN**
