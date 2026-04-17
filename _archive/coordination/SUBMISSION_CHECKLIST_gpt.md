# Nature Communications Submission Checklist

> **Paper:** Hardware-Aware Simulation of Organic Optoelectronic CIM Inference  
> **Status:** Pre-submission preparation  
> **Date:** 2026-04-11  
> **Prepared by:** Kimi

---

## 📋 NC Submission Requirements

### Manuscript Files

| Item | Status | File/Location | Notes |
|:-----|:------:|:--------------|:------|
| Main manuscript | ✅ | `main.pdf` (15 pages) | Including all sections |
| Supplementary Information | ✅ | `supplementary_main.pdf` (10 pages) | Figures, tables, methods |
| Cover letter | ✅ | `cover_letter.pdf` (2 pages) | Needs final author names |
| Response to reviewers | ⏸️ | N/A | Only if resubmission |

### Required Sections (NC Format)

| Section | Status | Location | Verification |
|:--------|:------:|:---------|:-------------|
| **Title** | ✅ | `main.tex` line 25-26 | Concise, informative |
| **Abstract** | ✅ | `sections/00_abstract.tex` | <200 words, structured |
| **Keywords** | ✅ | `main.tex` after abstract | 6-8 keywords added |
| **Introduction** | ✅ | `sections/01_introduction.tex` | Context + 4 questions |
| **Results** | ✅ | `sections/05_results.tex` | 8 subsections |
| **Discussion** | ✅ | `sections/06_discussion.tex` | 7 subsections |
| **Methods** | ✅ | `sections/03_methodology.tex` + Supplementary | Detailed in supp |
| **Data Availability** | ✅ | `sections/07_conclusion.tex` | Added |
| **Code Availability** | ✅ | `sections/07_conclusion.tex` | GitHub link |
| **Competing Interests** | ✅ | `sections/07_conclusion.tex` | Declaration |
| **Author Contributions** | ✅ | `sections/07_conclusion.tex` | CRediT style |
| **Acknowledgements** | ⏸️ | Optional | Add if needed |
| **References** | ✅ | `refs_gpt.bib` (47 entries) | All with DOIs |

### Figures & Tables

| Item | Status | Format | Resolution |
|:-----|:------:|:-------|:-----------|
| Fig 1: System Architecture | ✅ | PDF | Vector |
| Fig 2: Weight Mapping | ✅ | PDF | Vector |
| Fig 3: Accuracy Comparison | ✅ | PDF | Vector |
| Fig 4: HAT Recovery | ✅ | PDF | Vector |
| Fig 5: Energy Breakdown | ✅ | PDF | Vector |
| Supplementary Figures | ✅ | PDF | Vector |
| Table 1: FP32 Baselines | ✅ | LaTeX | Text |
| Table 2: Result Summary | ✅ | LaTeX | Text |

---

## 🔍 Pre-Submission Verification

### Content Check

- [x] **Abstract numbers match text** — Verified: 86.37±1.54%, 97.37±0.05%, 27.72±0.82%, 273.94 µJ
- [x] **No placeholder citations** — Verified: 0 "and others" / "et al." placeholders
- [x] **Cross-refs valid** — Verified: All Fig/Table refs resolve
- [x] **Bibliography complete** — 47 entries, all with DOIs
- [x] **No stale "2026" narrative** — Verified: Fixed to 2025 Early Access
- [x] **Energy claim qualified** — "upper-bound" appears in abstract, results, discussion

### Technical Claims Audit

| Claim | Evidence | Status |
|:------|:---------|:------|
| Ensemble HAT 10% → 86.37±1.54% | Table 2, §5.8 | ✅ Locked |
| Proportional noise 97.37±0.05% | §5.8 | ✅ Locked |
| NL=2.0 collapse 27.72±0.82% | §5.8 | ✅ Locked |
| Energy 273.94 µJ, 11.45x | §5.10 | ✅ Locked with routing sensitivity |
| AIHWKIT 90.08±0.21% | Supplementary §S4 | ✅ Locked |
| V4 fresh-instance 10.00% | §5.4 | ✅ Locked |

### LaTeX Technical

- [x] **Compiles clean** — 0 errors, 0 undefined refs after 2 passes
- [x] **Figures embed** — All PDFs properly included
- [x] **Font embedding** — Type 1/CID TrueType only
- [x] **Page limit** — 15 pages main (NC limit: ~13-14 ideal, but 15 acceptable)
- [ ] **Final PDF check** — Open in Adobe Reader, verify links work

---

## 📊 Reviewer Coverage Summary

| Category | Issues | Status |
|:---------|:------:|:-------|
| Tier 1 (4+ reviewers) | 6 | ✅ All resolved |
| Tier 2 (2-3 reviewers) | 22 | ✅ All resolved |
| Tier 3 (single reviewer) | 8 | ⏸️ 6 pending experiments, 2 acknowledged |
| **Total** | **109** | **101 addressed (92.7%)** |

### Remaining 8 Issues (Defensible)

| # | Issue | Defense Strategy |
|:--|:------|:-----------------|
| 5 | Activation function coverage | "Focus on core operators; beyond scope" |
| 15 | Differential asymmetry | ⏸️ **Gemini working on experiment** |
| 16 | Digital operator split ablation | Covered by hybrid mapping justification |
| 45 | Missing ablation studies | Partially covered; new experiments costly |
| 49 | Optical linearization | Low priority; frontend compensation addressed |
| 53 | NL vs COMSOL | "Device physics beyond behavioral simulation" |
| 59 | Physical non-ideality | ⏸️ **EXP-B after #15** |
| 62 | Proportional + NL coupled | "Complex interaction for future work" |

**Post-experiment coverage:** 103/109 (94.5%)

---

## 🎯 Submission Strategy

### Strengths to Emphasize

1. **Profile-driven framework** — Unique substitution interface
2. **Ensemble HAT** — Novel solution to fresh-instance overfitting
3. **Comprehensive evaluation** — 3 datasets, 3 architectures, 6 physical regimes
4. **Open source** — Full code release upon acceptance
5. **Cross-disciplinary** — Bridges materials science and ML systems

### Potential Reviewer Concerns & Responses

| Concern | Preemptive Response |
|:--------|:--------------------|
| "Why simulation, not fabrication?" | §1: Speed, parameter sweep, cross-paper comparison |
| "11.45x energy seems high" | §5.10: Explicit non-routed disclaimer + routing sensitivity |
| "ADC <0.1% suspicious" | Fig 5 caption: Array-level amortization explanation |
| "Organic devices too slow for ViT" | §3.1: Only static ops analog, attention remains digital |
| "Limited to CIFAR-scale" | §6.7: Framework extensible to larger datasets |
| "8 issues not covered" | §6.6: All acknowledged as deliberate scope boundaries |

---

## 📁 File Organization for Submission

### Main Package
```
submission/
├── manuscript.pdf          # main.pdf renamed
├── supplementary.pdf       # supplementary_main.pdf renamed
├── cover_letter.pdf        # cover_letter.pdf
├── response_to_reviewers/  # if applicable
└── source_files/           # if requested
    ├── main.tex
    ├── *.tex sections
    ├── refs_gpt.bib
    └── figures/
```

### Online Submission Portal

**Nature Communications:**
- Website: https://www.nature.com/ncomms/
- Submission system: https://mts-ncomms.nature.com/cgi-bin/main.plex
- Article type: "Article"
- Category: "Electrical and electronic engineering" or "Materials science"

**Required metadata:**
- [ ] Corresponding author email
- [ ] All author affiliations
- [ ] ORCID IDs (recommended)
- [ ] Funding information
- [ ] Competing interests (none declared)
- [ ] Data availability statement (already in paper)
- [ ] Code availability (already in paper)

---

## ⏰ Timeline

| Task | Owner | Deadline | Status |
|:-----|:------|:---------|:-------|
| EXP-A completion | Gemini | +2 hours | 🔄 In progress |
| EXP-B completion | Gemini | +4 hours | ⏸️ Pending |
| Banana image generation | Banana | +1 hour | 🔄 In progress |
| §6.6 text update | Kimi | After EXP-A | ⏸️ Ready |
| Final PDF verification | Kimi | +5 hours | ⏸️ Pending |
| Author approval | All | +6 hours | ⏸️ Pending |
| **Submission** | - | **+8 hours** | **🎯 Target** |

---

## ✅ Final Sign-Off Checklist

Before clicking "Submit":

- [ ] All authors have reviewed and approved the manuscript
- [ ] All figures display correctly in PDF
- [ ] All links (DOIs, URLs) are clickable and valid
- [ ] No identifying information in anonymized version (if required)
- [ ] Supplementary materials compile and match references
- [ ] Cover letter includes all required elements
- [ ] Response to reviewers prepared (if resubmission)
- [ ] Backup of all source files created

---

*Prepared: 2026-04-11*  
*Last updated: 2026-04-11 23:20*  
*Status: Awaiting experimental results*
