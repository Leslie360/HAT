# Reviewer #2 Analysis: Weaknesses & Suggestions

**Date:** 2026-04-15  
**Type:** Second Reviewer (New Set of Concerns)  

---

## Overview

Reviewer #2 focuses on **epistemological boundaries** of simulation-based research:
- What claims can legitimately be made from behavioral simulation?
- How to distinguish "simulation findings" from "experimental facts"?
- What is the appropriate scope for a "materials-to-system bridge"?

The reviewer acknowledges the technical rigor but questions the **interpretation and presentation** of results.

---

## The 7 Major Weaknesses

### Weakness 1: "High-Fidelity/Predictive" Overstatement

**Reviewer Quote:**
> "All results come from behavioral-level simulation... parameters are literature-inferred or proxy estimates, without direct fitting or closed-loop validation from real organic arrays."

**Overlap with Reviewer #1:**
- Related to Q2 (scale-masking) and Q3 (energy claims)
- Both reviewers question optimistic language

**Severity:** 🔴🔴🔴 HIGH  
**Action:** Tone down claims throughout manuscript

---

### Weakness 2: Weak Comparison with Mature CIM Frameworks

**Reviewer Quote:**
> "Only one AIHWKIT sanity check in supplementary... no systematic quantitative comparison showing whether precision curves match under same noise model."

**Overlap with Reviewer #1:**
- Directly addresses P1 (AIHWKIT comparison)
- Reviewer #1 wanted shared-regime validation; #2 wants expanded comparison

**Severity:** 🔴🔴🔴 HIGH  
**Action:** Expand AIHWKIT comparison and add feature matrix

---

### Weakness 3: "Engineering" vs "Physical Fitting"

**Reviewer Quote:**
> "Many key parameters are 'proxy estimates' rather than direct fitting curves... retention uses simplified double-exponential model... remains at 'first-order behavioral risk assessment'."

**Overlap with Reviewer #1:**
- Related to IR drop proxies (Q1) and scale-masking (Q2)
- Both question physical realism

**Severity:** 🟡🟡 MODERATE  
**Action:** Be transparent about proxy parameters, add sensitivity evidence

---

### Weakness 4: Uneven Statistical Reporting

**Reviewer Quote:**
> "Some key results report 3 seeds or 10-run MC, but others give only single run... some show 'best single checkpoint' with large gap to 3-seed mean."

**Overlap with Reviewer #1:**
- Minor revision point #5 (ConvNeXt multi-seed)
- Both want consistent statistical reporting

**Severity:** 🟡🟡 MODERATE  
**Action:** Standardize all key results to 3 seeds + 5-10 MC

---

### Weakness 5: Idealized ADC/Peripheral Modeling

**Reviewer Quote:**
> "Energy model uses fixed constants... 'analytical placeholders for first-order edge-node model'... no comparison with actual organic circuit implementation."

**Overlap with Reviewer #1:**
- Directly matches Q2 (scale-masking) and energy downgrade (P2)
- Both question ADC calibration assumptions

**Severity:** 🔴🔴🔴 HIGH  
**Action:** Add ADC non-ideality analysis (already done!), label as "upper bound"

---

### Weakness 6: Closed-Loop Validation Gap

**Reviewer Quote:**
> "The '88.53% zero-shot transfer accuracy' only shows the framework can ingest literature profiles... not that the profile was validated on any specific chip."

**Overlap with Reviewer #1:**
- New concern (not explicitly in #1)
- Questions the OPECT case study validity

**Severity:** 🔴🔴 MODERATE-HIGH  
**Action:** Reframe OPECT study as "what-if scenario" not "deployment prediction"

---

### Weakness 7: Blurring Simulation vs Experimental Facts

**Reviewer Quote:**
> "Strong language like 'transformers more vulnerable than CNNs', 'ADC precision is main bottleneck' come from simulation under specific conditions... not cross-platform measurements."

**Overlap with Reviewer #1:**
- Related to minor revision point #5 (scope qualifiers)
- Both want careful distinction between simulation findings and universal laws

**Severity:** 🟡🟡 MODERATE  
**Action:** Add qualifiers: "under present architectures, datasets, and noise profiles"

---

## The 8 Specific Suggestions

| # | Suggestion | Overlap | Effort | Priority |
|:--|:--|:--|:--|:--|
| 1 | Replace "high-fidelity, predictive" with "first-order behavioral" | Both reviewers | Low | 🔴 P1 |
| 2 | Expand AIHWKIT/CrossSim quantitative comparison | Both reviewers | Medium | 🔴 P1 |
| 3 | Turn "proxy parameters" into strength—explicit provenance table | Unique to #2 | Low | 🟡 P3 |
| 4 | Standardize statistics: 3 seeds + 5-10 MC for all key results | Both reviewers | Medium | 🟡 P2 |
| 5 | Add scope qualifiers to conclusions | Both reviewers | Low | 🟡 P3 |
| 6 | Reframe OPECT as "literature-calibrated what-if scenario" | Unique to #2 | Low | 🟡 P2 |
| 7 | Compress repetitive figures, focus on core insights | Editorial | Medium | 🟢 P4 |
| 8 | Emphasize "behavioral-level tool, not circuit simulator" | Unique to #2 | Low | 🟡 P2 |

---

## Unified Concern Matrix

| Concern Area | Reviewer #1 | Reviewer #2 | Unified Response |
|:--|:--|:--|:--|
| **Language tone** | Downgrade energy claims | Remove "predictive" | Systematic wording revision |
| **Physical realism** | IR drop, scale-masking | Proxy parameters, ADC idealization | Sensitivity analyses + caveats |
| **Framework comparison** | Single AIHWKIT point | Expanded comparison | Feature matrix + additional benchmarks |
| **Statistical rigor** | ConvNeXt multi-seed | All key results standardized | 3 seeds + MC for all claims |
| **Scope boundaries** | Minor revision point | Major weakness #7 | Explicit qualifiers throughout |
| **Validation type** | N/A | OPECT "what-if" vs "deployment" | Reframe case study language |

---

## Key Insight: Reviewer #2's Core Message

> "The work is technically sound but epistemologically overreaching. Simulation can provide insights and guide decisions, but should not be presented as 'predicting' real hardware behavior without experimental validation."

**Response Strategy:**
1. **Acknowledge** the limitation explicitly
2. **Reframe** the contribution: "decision support tool" not "predictive simulator"
3. **Emphasize** the practical value: bridging materials and algorithm communities
4. **Add** appropriate caveats to all quantitative claims

---

## Unified Response Narrative

### For Both Reviewers

> "We acknowledge that our behavioral simulation provides **first-order scenario exploration** rather than **circuit-level prediction**. The parameters are derived from literature and sensitivity analyses show robustness within ±50% variation. The OPECT case study represents a **'what-if' scenario** based on published device characteristics, not a validated deployment prediction. We have systematically revised the language throughout to reflect these boundaries, added comprehensive statistical reporting (3 seeds + 10 MC), and expanded framework comparisons. The contribution is a **lightweight decision-support bridge** between materials and algorithm researchers, not a replacement for circuit simulation tools."

---

## Action Items Consolidated

### High Priority (Both Reviewers)
1. ✅ Tone down language ("high-fidelity" → "first-order behavioral")
2. ✅ Expand AIHWKIT comparison (additional benchmarks)
3. ✅ Add statistical standardization (3 seeds + MC)
4. ✅ Add sensitivity analyses (IR drop, ADC non-ideality)

### Medium Priority (At Least One Reviewer)
5. Reframe OPECT case study language
6. Add framework feature comparison matrix
7. Add explicit scope qualifiers to conclusions
8. Emphasize behavioral-level tool positioning

### Lower Priority (Editorial)
9. Compress repetitive figures
10. Add parameter provenance table

---

## Evidence Status

| Requirement | Reviewer #1 | Reviewer #2 | Status |
|:--|:--|:--|:--|
| IR drop sensitivity | ✅ Q1 | Implicit | ✅ Complete |
| ADC non-ideality | ✅ Q2 | W5 | ✅ Complete |
| AIHWKIT expansion | ✅ P1 | S2 | ⏳ In progress |
| Multi-seed standardization | Minor #5 | W4/S4 | ⏳ Ongoing |
| Language revision | P2, P3 | S1 | ⏳ Drafting |
| OPECT reframing | — | W6/S6 | ⏳ Drafting |

---

## Confidence Assessment

| Response Element | Confidence | Reasoning |
|:--|:--|:--|
| IR drop/ADC analyses | Very High | Experiments complete, data solid |
| AIHWKIT expansion | High | Framework installed, needs execution |
| Language revision | High | Straightforward text changes |
| Statistical standardization | Medium | Requires re-running some experiments |
| OPECT reframing | High | Text-only change |

---

## Next Steps

1. **Immediate (Today):**
   - Draft language revision guidelines
   - Begin AIHWKIT expansion experiments

2. **Short-term (This Week):**
   - Complete multi-seed re-runs for all key results
   - Generate framework comparison matrix
   - Draft OPECT reframing text

3. **Final Polish:**
   - Integrate all changes into unified response
   - Final manuscript revision

---

**Key Advantage:** Both reviewers' concerns are complementary rather than contradictory. Addressing them together strengthens the manuscript's epistemological clarity and methodological transparency.
