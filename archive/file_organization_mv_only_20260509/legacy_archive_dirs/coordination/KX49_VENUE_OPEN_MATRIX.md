# KX49: Venue-Open Submission Matrix

> **Date**: 2026-04-13  
> **Status**: COMPLETED  
> **Scope**: Multi-venue strategy supporting open decision-making (not pre-locked)

---

## Strategy Principle

This matrix supports **open multi-track positioning**. No venue is "confirmed"; each represents a viable path with distinct trade-offs. The project maintains readiness for any option until explicit submission.

---

## Venue Comparison Matrix

| Venue | Fit | Main Editorial Risk | Minimum Manuscript Delta | What Measured Data Would Help | Timing |
|:-----|:---|:--------------------|:-------------------------|:------------------------------|:-------|
| **Nature Communications** | Cross-disciplinary (materials+ML+architecture); simulation framework precedent (AIHWKIT) | 8/10 0412 reviewers expect Major Revision; proxy parameter skepticism from materials side | Current version already defensible; add Parameter Risk Matrix (evidence-grounded); strengthen Ensemble HAT baseline text | Single-device measured profile for case study validation; confirmation of Zhang/Vincze parameter extraction | Submit now (Major Revision expected) or after measured data (strengthens to Minor Revision) |
| **npj Computational Materials** | Nature portfolio; explicit methodology welcome; lower hardware validation bar | Lower impact factor perception; may be seen as "downgrade" from NC ambition | Reposition contributions (materials-first); add "Computational Materials Tools" section; expand device physics discussion | Multi-state retention data; wavelength-dependent photoresponse; confirmed conductance window | Submit now (high confidence) |
| **Advanced Intelligent Systems** (Wiley) | Emerging venue; neuromorphic focus; simulation-accepting | Less prestigious; smaller readership; IF ~7 | Minor reformatting; emphasize "intelligent systems" angle | Any single measured profile would strengthen significantly | Submit now (high confidence, fast cycle) |
| **IEEE TCAD** | Top EDA venue; strong simulation tradition; tool papers welcome | Very long review cycle (6-9 months); expects formal verification; minimal materials audience | Expand methodology detail; add formal model verification; add SPICE co-simulation if available | Full parameter set with statistical validation; circuit-level correlation | Submit only if EDA credibility is priority over timeline |

---

## Decision Flowchart

```
Start
│
├─► Do you have measured data now? ──Yes──► Lead with measured case study
│   │                                         (any venue, stronger position)
│   No
│   │
├─► Is maximum impact (IF ~16) critical? ──Yes──► NC (accept Major Revision risk)
│   │
├─► Is acceptance confidence >80% required? ──Yes──► npj or AIS (Minor Revision likely)
│   │
├─► Is timeline <3 months required? ──Yes──► AIS (fastest)
│   │
└─► EDA community credibility priority? ──Yes──► IEEE TCAD (long cycle)
```

---

## Evidence-Grounded Positioning

### Current Manuscript Strengths (All Venues)
- ✅ Parameter provenance matrix (Table S2 in supplementary.tex)
- ✅ Sensitivity sweep data (Table S3: C2C 1-8%, D2D 2-15%, accuracy 88.57%-84.59%)
- ✅ C2C invariance mechanistically explained (scale-masking, Section 5.2)
- ✅ Three-seed reproducibility (Table: seeds 42/123/2026, aggregate 87.95±0.27%)
- ✅ Transparency disclosures throughout

### Current Gaps (Venue-Dependent)
| Gap | NC Risk | npj Risk | AIS Risk | TCAD Risk |
|:----|:--------|:---------|:---------|:----------|
| Measured-device closure | High | Moderate | Low | Low |
| Ensemble HAT i.i.d. baseline | Moderate | Low | Low | Moderate |
| ImageNet-scale validation | Moderate | Low | Moderate | Low |
| Formal verification | Low | Low | Low | High |

---

## Measured-Data Value by Venue

| Data Type | NC Value | npj Value | AIS Value | TCAD Value |
|:----------|:---------|:----------|:----------|:-----------|
| Single-device profile (Zhang 2025 style) | Major → Minor Revision | Strengthens methodology | High impact | Moderate |
| Multi-device statistics (σD2D, σC2C) | Definitive validation | Strong methodology | Strong | Moderate |
| Retention time constants (τ1, τ2) | Parameter validation | Core physics | Moderate | Low |
| Wavelength response (γ) | Case study depth | Organic specificity | Moderate | Low |
| Full-array programming data | Game-changing | Excellent fit | Good | Low |

---

## Recommended Parallel Preparation

### Track A: NC-Ready (Current)
- Version: Current manuscript + KX41/KX43 defense packs
- Submit: Immediate
- Expected: Major Revision
- Revision ammunition: Parameter Risk Matrix (evidence-grounded)

### Track B: npj-Optimized (2-day delta)
- Changes: Reposition contributions; add Computational Materials section
- Submit: 2 days after decision
- Expected: Minor Revision
- Measured data integration: Revision phase

### Track C: AIS-Fallback (1-day delta)
- Changes: Reformatting; systems-angle abstract
- Submit: 1 day after decision
- Expected: Minor Revision or Accept

---

## Trigger Conditions

| Trigger | Action |
|:--------|:-------|
| User decides "maximum impact" | Submit to NC (Track A) |
| User decides "high confidence" | Submit to npj (Track B) |
| Measured data arrives before submission | Integrate into case study; prefer NC or npj |
| Measured data arrives during review | Prepare as Revision material |
| 3+ months pass without decision | Consider AIS as clean-slate submission |

---

## Conclusion

This matrix maintains **strategic optionality**. The current manuscript is defensible at NC; repositioning for npj requires modest effort; AIS offers fast fallback. No venue is locked until explicit submission action.

**Recommendation**: Prepare all three tracks; decide based on user priority (impact vs. confidence) and measured-data arrival timing.
