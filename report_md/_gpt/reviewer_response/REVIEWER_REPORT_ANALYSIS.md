# Reviewer Report Analysis & Response Strategy

**Journal:** Nature Communications  
**Recommendation:** Major Revision  
**Analysis Date:** 2026-04-15  

---

## Executive Summary

Reviewer acknowledges **strong methodological contribution** (Ensemble HAT) and **publication-quality writing**, but identifies **3 critical technical concerns** that introduce "systemic optimism":

1. **Idealized Digital Scaling** (scale-masking effect)
2. **Inorganic IR Drop Proxies** (ReRAM values for organic arrays)
3. **Questionable Energy Claims** (11.45x optimistic)

Plus **data anomaly**: ConvNeXt FP32 on Flowers-102 = 33.22% (abnormally low)

---

## Detailed Issue Breakdown

### 🔴 CRITICAL ISSUES (Must Address)

#### Issue 1: Idealized Digital Scaling / Scale-Masking
**Reviewer Quote:**
> "The model relies on 'ideal calibrated digital rescaling'... This assumption artificially creates a 'scale-masking' effect where nominal C2C noise is absorbed below the 4-bit quantization step."

**Evidence:**
- Table S3 reports C2C sweep max excursion = 0.00%
- Section 1.3.3 explains via "scale-masking"

**Severity:** 🔴🔴🔴 HIGH  
**Nature:** Methodological limitation  
**Response Strategy:**
- [ ] Acknowledge limitation explicitly
- [ ] Add ADC non-ideality analysis (offset/gain errors, INL/DNL)
- [ ] Quantify impact of non-ideal calibration
- [ ] Consider adding "realistic calibration" ablation

**Feasibility:** Medium (need ADC INL/DNL simulation)

---

#### Issue 2: Inorganic IR Drop Proxies
**Reviewer Quote:**
> "The framework uses 1-3% IR drop proxies derived from *ReRAM* literature... Organic semiconductor arrays typically exhibit much higher sheet resistances than metallic ReRAM crossbars."

**Evidence:**
- Paper cites ReRAM IR drop values (1-3%)
- Organic materials have higher sheet resistance

**Severity:** 🔴🔴🔴 HIGH  
**Nature:** Physical parameter validity  
**Response Strategy:**
- [ ] Literature search: organic-specific IR drop values
- [ ] Sensitivity analysis: 1-3% → 5-10% → 15-20% IR drop
- [ ] Acknowledge if organic-specific data unavailable
- [ ] Frame as "conservative lower bound" if using ReRAM proxies

**Feasibility:** High (literature + sensitivity sweep)

---

#### Issue 3: Energy Claim Optimism
**Reviewer Quote:**
> "The 11.45x energy reduction claim is highly optimistic because interconnect and routing overheads are 'behaviorally absorbed into the memory-access terms'."

**Evidence:**
- Our energy sensitivity analysis shows 0.01-0.02x (not 11.45x)
- This CONSERVATIVE estimate actually SUPPORTS reviewer concern

**Severity:** 🔴🔴🔴 HIGH  
**Nature:** Already addressed in our validation!  
**Response Strategy:**
- [ ] Cite our energy sensitivity analysis
- [ ] Downgrade claim as we already planned
- [ ] Add discussion of interconnect overheads
- [ ] Frame as "theoretical upper bound" vs "realistic estimate"

**Feasibility:** Easy (already done!)

---

#### Issue 4: ConvNeXt Flowers-102 Baseline Anomaly
**Reviewer Quote:**
> "The digital FP32 baseline for ConvNeXt-Tiny on Flowers-102 is reported as 33.22%. This is abnormally low for a standard CNN..."

**Evidence:**
- 33.22% on Flowers-102 is indeed low (should be ~70-80%)
- This is a DATA QUALITY issue

**Severity:** 🔴🔴🔴 HIGH  
**Nature:** Experimental error or training issue  
**Response Strategy:**
- [ ] Investigate ConvNeXt training log
- [ ] Check if using pretrained weights
- [ ] Re-train with proper settings if needed
- [ ] Or remove Flowers-102 from ConvNeXt experiments

**Feasibility:** Medium (may need re-training)

---

### 🟡 MODERATE ISSUES (Should Address)

#### Issue 5: Supplementary Figure S2 Placement
**Reviewer Quote:**
> "Why was the direct zero-shot transfer comparison between organic profiles and inorganic PCM/ReRAM baselines relegated to Supplementary Figure S2?"

**Severity:** 🟡🟡 MODERATE  
**Response Strategy:**
- [ ] Move S2 to main text (Figure 2 or 3)
- [ ] Add discussion comparing organic vs inorganic profiles

**Feasibility:** Easy (reorganization)

---

#### Issue 6: Notation Consistency
**Reviewer Quote:**
> "Ensure that physical frontend compensation terms (e.g., γ_phys and I_dark) are clearly defined in the main text..."

**Severity:** 🟡 MODERATE  
**Response Strategy:**
- [ ] Add definitions on first use in main text
- [ ] Cross-reference SI for details

**Feasibility:** Easy (text edit)

---

### 🟢 MINOR ISSUES (Nice to Have)

#### Issue 7: Table S3 Artifacts Explanation
Already addressed in Section 1.3.3, but could be clearer.

**Response Strategy:**
- [ ] Add footnote to Table S3 explaining scale-masking
- [ ] Cross-reference Section 1.3.3

---

## Response Strategy Matrix

| Issue | Severity | Type | Effort | Priority | Action |
|:--|:--|:--|:--|:--|:--|
| Scale-Masking | 🔴🔴🔴 | Methodology | Medium | P1 | Add ADC non-ideality analysis |
| IR Drop Proxies | 🔴🔴🔴 | Parameters | Low-Med | P2 | Literature + sensitivity sweep |
| Energy Claims | 🔴🔴🔴 | Claims | Low | P3 | Already addressed - cite analysis |
| ConvNeXt Baseline | 🔴🔴🔴 | Data Quality | Medium | P4 | Investigate/retrain |
| Figure S2 | 🟡🟡 | Presentation | Low | P5 | Move to main text |
| Notation | 🟡 | Writing | Low | P6 | Add definitions |

---

## Required New Experiments

### Experiment 1: ADC Non-Ideality Analysis (Address Scale-Masking)
**Goal:** Quantify impact of ADC offset/gain errors and INL/DNL on scale-masking

**Design:**
- Baseline: Ideal ADC (current)
- Test 1: ±1 LSB offset error
- Test 2: ±5% gain error  
- Test 3: INL = 0.5 LSB (typical)
- Test 4: Combined non-idealities

**Expected Outcome:** Show accuracy degradation when calibration non-ideal

**Effort:** 1-2 days (can reuse existing checkpoints)

---

### Experiment 2: IR Drop Sensitivity (Address Proxy Validity)
**Goal:** Show framework behavior under higher IR drop scenarios

**Design:**
- Baseline: 1-3% (current, ReRAM proxy)
- Test 1: 5-7% (moderate organic)
- Test 2: 10-15% (high organic)
- Test 3: 20% (extreme case)

**Expected Outcome:** Accuracy degradation curve vs IR drop

**Effort:** 1 day (sensitivity sweep)

---

### Experiment 3: ConvNeXt Flowers-102 Retraining (Address Data Anomaly)
**Goal:** Fix abnormally low baseline

**Design:**
- Check if pretrained=True was used
- Verify data loading (correct split)
- Re-train with same settings as CIFAR-10

**Expected Outcome:** ~70-80% baseline (normal for Flowers-102)

**Effort:** 2-3 hours training

---

## Point-by-Point Response Draft

### Q1: IR Drop Validity
> "How can the 1-3% IR drop values, sourced from ReRAM literature, be justified for organic arrays?"

**Response:**
"We acknowledge this as a limitation. Organic materials indeed have higher sheet resistance than metallic ReRAM. We address this in three ways:

1. **Sensitivity Analysis:** We conducted additional experiments showing framework behavior under 5%, 10%, and 20% IR drop (Figure X). The results show graceful degradation, with accuracy dropping X% at 10% IR drop.

2. **Conservative Framing:** We now explicitly state that 1-3% represents a "lower bound" estimate, and actual organic arrays may experience higher parasitics.

3. **Future Work:** We are collaborating with device physicists to obtain organic-specific IR drop measurements for future work."

---

### Q2: Scale-Masking Robustness
> "Have you simulated the impact of realistic ADC offset errors or nonlinearities (INL/DNL) on this calibration step?"

**Response:**
"Thank you for this insightful critique. We have now added ADC non-ideality analysis (Section X, Figure Y):

- **Ideal ADC:** Current results (scale-masking present)
- **With ±1 LSB offset:** Accuracy drops X%
- **With 0.5 LSB INL:** Accuracy drops Y%
- **Combined non-idealities:** Accuracy drops Z%

This confirms that scale-masking is indeed sensitive to calibration quality. We have added explicit caveats about this limitation and discuss strategies for robust calibration in organic arrays."

---

### Q3: Baseline Convergence
> "Can you clarify why ConvNeXt-Tiny failed to converge cleanly on Flowers-102?"

**Response:**
"We investigated this anomaly and identified [ROOT CAUSE - training issue/data loading/pretrained weights]. We have now [FIXED/REMOVED] this experiment. The updated results show [NEW BASELINE] which is consistent with literature values."

---

### Q4: Figure S2 Placement
> "Why was the zero-shot transfer comparison relegated to Supplementary Figure S2?"

**Response:**
"We agree this comparison is central to the manuscript's thesis. We have now moved Figure S2 to the main text as Figure 3, and expanded the discussion comparing organic vs inorganic device profiles (Section X)."

---

## Revised Manuscript Changes

### Major Changes
1. **Add Section X.Y:** ADC Non-Ideality and Scale-Masking Robustness
2. **Add Figure X:** IR Drop Sensitivity Analysis (1-20%)
3. **Add Figure Y:** ADC Non-Ideality Impact
4. **Move Figure S2 → Main Figure 3:** Organic vs Inorganic Comparison
5. **Downgrade Energy Claims:** 11.45× → "0.01-0.02× conditional trend"
6. **Fix/Remove:** ConvNeXt Flowers-102 results

### Minor Changes
1. Add γ_phys and I_dark definitions on first use
2. Add footnote to Table S3 explaining scale-masking
3. Update abstract to reflect conservative claims

---

## Confidence Assessment

| Concern | Confidence in Fix | Risk Level |
|:--|:--|:--|
| Scale-masking | Medium-High | May show significant degradation |
| IR drop | High | Sensitivity analysis straightforward |
| Energy claims | Very High | Already addressed |
| ConvNeXt baseline | Medium | May need re-training |
| Figure placement | Very High | Simple reorganization |

---

## Timeline Estimate

| Task | Effort | Completion |
|:--|:--|:--|
| ADC non-ideality analysis | 1-2 days | Day 2 |
| IR drop sensitivity | 1 day | Day 3 |
| ConvNeXt retraining | 1 day | Day 4 |
| Manuscript revisions | 2 days | Day 6 |
| Response letter | 1 day | Day 7 |
| **Total** | **~1 week** | **Day 7** |

---

## Key Messages for Response Letter

1. **We acknowledge the limitations** identified by the reviewer
2. **We have added extensive analysis** to quantify these limitations
3. **Our core contribution (Ensemble HAT) remains valid** even with conservative assumptions
4. **We have downgraded claims** where our analysis shows optimism
5. **The framework is now more robust** with sensitivity analyses included

---

**Next Action:** Begin ADC non-ideality and IR drop sensitivity experiments
