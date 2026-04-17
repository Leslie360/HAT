# KX52: Submission Timing Decision Triggers v2

> **Date**: 2026-04-13  
> **Status**: COMPLETED  
> **Scope**: Practical timing memo for long-horizon project (no pre-decided path)

---

## Decision Framework

Three timing options, each with explicit value/cost trade-offs. No "correct" answer—depends on user priorities.

---

## Option 1: Submit Current Simulation-First Paper Now

### What New Value is Gained
- **Timeliness**: Establishes priority on methodology contribution
- **Feedback**: Obtains peer review input for potential revision
- **Milestone**: Formal progress marker for PhD timeline/funding

### What Schedule Cost is Paid
- **Risk**: Major Revision likely at NC (~8/10 reviewers); Minor Revision likely at npj/AIS
- **Revision work**: 2-4 months of response preparation if Major Revision
- **Opportunity cost**: Cannot incorporate measured data into initial submission

### What Would Actually Change in Manuscript
- **Current state**: Already defensible (KX41/KX43 defense packs ready)
- **Additions**: Evidence-grounded Parameter Risk Matrix (KX50)
- **No changes**: Locked numbers remain; no new experiments required

### Trigger Condition
- User prioritizes **timeline over measured-data integration**
- User accepts **Major Revision risk** at NC, OR
- User prefers **npj/AIS path** for higher acceptance confidence

---

## Option 2: Wait for 1-2 Optional Supplementary Experiments

### What New Value is Gained
- **Defensive strength**: per-forward i.i.d. baseline distinguishes Ensemble HAT
- **Causal clarity**: pure-digital ADC sweep separates organic-CIM from ViT-quantization effects
- **Reviewer ammunition**: "We have already addressed this concern experimentally"

### What Schedule Cost is Paid
- **Delay**: 1-2 weeks for experiments (if GPU available)
- **Risk**: Experiments may not show expected results; requires interpretation
- **Scope creep**: May lead to "just one more experiment" trap

### What Would Actually Change in Manuscript
- **Supplementary additions**:
  - Table: per-forward vs per-epoch D2D comparison
  - Figure: pure-digital ADC sweep (4/6/8-bit)
- **Text updates**:
  - Ensemble HAT section strengthened with quantitative baseline
  - ADC cliff claim qualified with digital-comparison context
- **No changes to**: Locked numbers; main conclusions

### Trigger Condition
- **GPU time available** AND
- User prioritizes **reviewer-defense strength** over speed, AND
- User wants to **preempt Major Revision** at NC

---

## Option 3: Wait for First In-House Measured Raw Tables

### What New Value is Gained
- **Validation**: Measured-device case study transforms "simulation" to "calibrated framework"
- **Acceptance boost**: Likely shifts NC from Major to Minor Revision
- **Impact**: Measured-data papers generally cited more than pure simulation

### What Schedule Cost is Paid
- **Uncertainty**: Arrival time of measured data unknown (weeks to months)
- **Delay**: Submission postponed until data arrives + analysis time
- **Risk**: May be scooped; measured-data validation may not align with predictions

### What Would Actually Change in Manuscript
- **New section**: "Measured-Device Validation" (or integrated into Case Study)
- **Updated claims**: "Calibrated against measured X" vs "Literature-derived proxy"
- **Parameter updates**: Replace proxy estimates with fitted values (if different)
- **Supplementary additions**:
  - Parameter extraction methodology from raw data
  - Comparison: literature-proxy vs. measured-profile predictions

### Trigger Condition
- User prioritizes **validation strength** over speed, AND
- Measured data expected **within 2 months**, AND
- User is willing to risk **delay for potential acceptance boost**

---

## Decision Matrix

| User Priority | Recommended Option | Venue | Expected Outcome |
|:--------------|:-------------------|:------|:-----------------|
| Speed (submit ASAP) | Option 1 | npj or AIS | Minor Revision → Acceptance |
| Impact (maximize IF) | Option 1 or 3 | NC | Major Revision (Opt 1) or Minor Revision (Opt 3) |
| Confidence (>80% accept) | Option 1 | npj | Minor Revision → Acceptance |
| Defense (preempt reviewer attacks) | Option 2 | NC | Strengthens against Major Revision |
| Validation (measured-data closure) | Option 3 | NC | Best paper; timeline uncertain |

---

## Hybrid Strategy (Recommended)

**Parallel track preparation**:

```
Week 1-2: Finalize manuscript with KX50 evidence-grounded Parameter Risk Matrix
          └─► Ready for Option 1 (submit anytime)

Week 2-3: Run GM-E1/E2 optional experiments (if GPU free)
          └─► Strengthens Option 1 if successful

Month 1+:  Await measured data
          └─► If arrives: integrate and prefer NC (Option 3)
          └─► If delayed: submit with optional experiments (Option 2)
          └─► If urgent need: submit current version (Option 1)
```

**Decision triggers**:
- **Measured data arrives** → Integrate; submit to NC
- **2 months pass, no data** → Submit with optional experiments to NC or current version to npj
- **Funding/PhD deadline pressure** → Submit current version to npj (highest acceptance confidence)

---

## Key Principle

**No single path is locked.** The project maintains readiness for:
- Immediate submission (Option 1)
- Optional-experiment strengthening (Option 2)
- Measured-data validation (Option 3)

Codex compiles and patches; user decides timing based on priorities and external constraints (data arrival, deadlines, GPU availability).

---

## Next Actions by Role

| Role | Action | Timing |
|:-----|:-------|:-------|
| **Kimi** | Prepare defense packs for all three options | Done (KX41, KX43, KX50) |
| **Gemini** | Execute optional experiments if GPU available | If Option 2 selected |
| **Codex** | Compile submission-ready package for all venues | On user trigger |
| **User** | Decide timing priority; request measured data from PhD students | Immediate |
