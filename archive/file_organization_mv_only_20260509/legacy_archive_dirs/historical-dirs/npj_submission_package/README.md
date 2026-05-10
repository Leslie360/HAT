# npj Computational Materials Submission Package

> **Target Venue**: npj Computational Materials (Nature Portfolio)  
> **Submission Type**: Article  
> **Scope**: Methodology / Simulation Framework  
> **Date**: 2026-04-13

---

## Venue Rationale

### Why npj Computational Materials?

| Factor | NC | npj Comp Mat | Advantage |
|:-------|:---|:-------------|:----------|
| Acceptance Probability | ~60% (Major Revision) | ~80% (Minor Revision) | ✅ Higher confidence |
| Hardware Validation Bar | High | Moderate | ✅ Fits simulation focus |
| Methodology Welcome | Yes | Explicitly | ✅ Better scope fit |
| Review Cycle | 3-4 months | 2-3 months | ✅ Faster |
| Impact Factor | ~16 | ~9-10 | Trade-off |
| Materials Audience | Yes | Primary | ✅ Better disciplinary fit |

### Strategic Positioning

**From**: "ML Systems contribution with materials application"
**To**: "Materials simulation methodology with ML implementation"

Key narrative shift:
- Foreground: Materials-to-system bridge, device physics sensitivity
- Background: Algorithm novelty (Ensemble HAT as enabling method)

---

## Directory Structure

```
npj_submission_package/
├── manuscript/              # Main LaTeX source
│   ├── main.tex
│   ├── sections/
│   └── refs.bib
├── supplementary/           # Supplementary Information
│   ├── supplementary.tex
│   ├── tables/
│   └── figures/
├── figures/                 # High-res figure files
│   ├── fig1_concept.png
│   ├── fig2_framework.png
│   └── ...
├── source_data/            # Source data tables (Excel/CSV)
│   ├── fig1_source_data.xlsx
│   └── ...
├── cover_letter/           # Cover letter and appeals
│   ├── cover_letter.tex
│   └── editorial_appeal.md
└── response_to_reviewers/  # Revision response templates
    ├── anticipated_R1.md
    └── anticipated_R2.md
```

---

## Checklist

### Pre-Submission [P0]
- [ ] Reposition contribution emphasis (materials-first)
- [ ] Expand device physics discussion
- [ ] Add comparison to materials simulation tools
- [ ] Verify all figures meet npj resolution requirements
- [ ] Prepare source data tables

### Submission [P1]
- [ ] Compile manuscript (no page limit for npj)
- [ ] Compile supplementary
- [ ] Generate cover letter
- [ ] Upload to Nature Portfolio submission system
- [ ] Suggest reviewers (3-5 names)

### Post-Submission [P2]
- [ ] Monitor status
- [ ] Prepare revision materials (if Minor Revision)
- [ ] Integrate measured data when available

---

## Key Document Adjustments

### 1. Title Options

| Option | Title |
|:-------|:------|
| A | Profile-Driven Behavioral Simulation for Organic Optoelectronic Compute-in-Memory: A Materials-to-System Methodology |
| B | Bridging Organic Device Characteristics and Edge Vision Deployment: A Simulation Framework for Optoelectronic CIM |
| C | Materials-Aware Simulation of Vision Transformer Deployment on Organic Optoelectronic Arrays |

**Recommended**: Option A (explicit methodology positioning)

### 2. Abstract Adjustments

**Add**: 
- "materials characterization" angle
- "computational materials science" scope
- Explicit simulation-only declaration

**Reduce**:
- ML algorithm novelty emphasis
- Ensemble HAT as primary contribution

### 3. Key Contribution Reordering

**For NC**:
1. Ensemble HAT algorithm
2. Profile-driven framework
3. ADC cliff insight
4. Case study

**For npj**:
1. Materials-to-system simulation methodology
2. Profile-driven interface for device characterization
3. Sensitivity analysis of device parameters
4. Ensemble HAT as deployment solution

---

## Comparison to Other Tools

Must add to Related Work:

| Tool | Target Devices | Organic Support | Our Differentiation |
|:-----|:---------------|:----------------|:--------------------|
| AIHWKIT | RRAM, PCM | ❌ | Organic-specific physics |
| NeuroSim | RRAM, SRAM | ❌ | Photoresponse frontend |
| CrossSim | Memristors | ❌ | Transformer deployment |
| MemTorch | Memristors | ❌ | Profile substitution |
| **Our Framework** | **Organic optoelectronic** | ✅ | Unified workflow |

---

## Anticipated Reviewer Profile

### Likely Backgrounds
1. **Computational materials scientist** (50%)
   - Cares about: Device physics accuracy, parameter sensitivity
   - Risk: Proxy parameter skepticism
   - Defense: Parameter Risk Matrix

2. **Organic electronics experimentalist** (30%)
   - Cares about: Real device relevance, validation path
   - Risk: "Where are the measured devices?"
   - Defense: Future measured-data integration path

3. **AI/ML systems** (20%)
   - Cares about: Algorithm novelty, benchmarks
   - Risk: CIFAR-scale insufficient
   - Defense: Framework contribution, not SOTA chasing

---

## Timeline

| Phase | Task | Deadline |
|:------|:-----|:---------|
| **Week 1** | Reposition manuscript for npj | 2026-04-20 |
| **Week 1** | Add materials-focused content | 2026-04-20 |
| **Week 2** | Final compile and source data prep | 2026-04-27 |
| **Week 2** | Submit to npj | 2026-04-30 |
| **Month 2-3** | Await decision | - |
| **Month 3+** | Minor Revision (if accepted) | - |
| **Ongoing** | Integrate measured data | When available |

---

## Success Metrics

**Acceptance Criteria**:
- [ ] Editorial pre-screening pass
- [ ] 2/3 reviewers recommend Minor Revision or better
- [ ] No "fundamental scope mismatch" comments

**Impact Goals**:
- [ ] Citations from materials characterization papers
- [ ] Adoption by organic electronics groups
- [ ] Future measured-device collaboration

---

**Status**: Package initialized, awaiting manuscript repositioning.
