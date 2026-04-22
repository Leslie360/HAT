# G-GG9: Conference-Venue Fit v2 — Submission Strategy and 12-Month Roadmap

**Date:** 2026-04-20  
**Author:** Gemini Phase β — Round P2  
**Scope:** Target-venue analysis for Paper-2 and follow-on work. Fit scores are qualitative judgments based on review criteria, editorial scope, and recent proceedings trends. No specific reviewer identities are inferred.  
**Sources:** `GEMINI_STRUCTURAL_LIMIT_FORMAL_20260420.md` (G-GG1), `GEMINI_HIGHER_ORDER_NL_DESIGN_20260420.md` (G-GG2), `GEMINI_PAPER2_ARCH_MEMO_20260420.md` (G-GG5), `GEMINI_PAPER2_EXP_DESIGN_20260420.md` (G-GG6), Paper-2 skeleton (`paper/paper2/draft_v0/SKELETON.md`), Paper-1 (`paper/latex_gpt/main.tex` and `sections/06_discussion.tex`).

---

## 1. Venue-by-Venue Analysis

### 1.1 NeurIPS (Neural Information Processing Systems)

**Scope:** Premier venue for machine learning theory, algorithms, and applications. Increasingly receptive to ML-for-systems and hardware-aware training, though the core audience remains algorithmically oriented.

**Fit for Paper-2:** ★★★★☆ (4/5)

- **Alignment:** The structural-limit hypothesis is a *learning-theory claim* about generalization under structured perturbation (D2D mismatch maps). The falsification methodology and pre-registration align with NeurIPS's growing emphasis on rigorous empirical science and reproducibility.
- **Tension:** The experimental substrate (analog CIM simulation) is niche. Reviewers without hardware backgrounds may question whether the `~30%` ceiling is an ML phenomenon or a simulator artifact. The paper must foreground the theoretical mechanism (Pillar I–III, G-GG1) and relegate device physics to Methods.
- **Recommended track:** Main conference ( archival paper). Avoid workshops unless the paper is rejected from the main track and resubmitted to a hardware-aware ML workshop (e.g., ML for Systems, MLSys co-located workshops).
- **Competition intensity:** Extreme. Acceptance rate ~25% in recent years. Theory papers face stiff competition from pure optimization and statistical learning theory. The applied-ML-for-hardware angle is less crowded but requires exceptional clarity about ML novelty.
- **Deadline prediction:** Abstract deadline typically mid-May; full paper late May. For the 2026 cycle, anticipate **abstract: ~May 11, 2026; full paper: ~May 18, 2026** (based on 2025 calendar: abstract May 9, full May 15). Verify on `neurips.cc`.

**Verdict:** Strong fit if the narrative is framed as "generalization theory for structured parameter-space perturbations" rather than "device simulation." Title should mention "Transformers" and "generalization barrier," not "organic RRAM."

---

### 1.2 MLSys (Conference on Machine Learning and Systems)

**Scope:** Systems-oriented ML venue spanning hardware, compilers, distributed training, and inference optimization. Reviewers are hybrid ML/systems researchers.

**Fit for Paper-2:** ★★★★☆ (4/5)

- **Alignment:** MLSys explicitly solicits work on "ML accelerators" and "efficient training and inference." The compute-ViT framework is a systems contribution: a simulator that ranks hardware-induced failure modes. The structural-limit claim adds theoretical rigor to a systems paper.
- **Tension:** MLSys prioritizes empirical speedups, energy measurements, and deployable artifacts. Paper-2 is theory-first and simulation-only; it lacks silicon measurements or throughput benchmarks. The paper must argue that *bounding accuracy limits* is a systems contribution comparable to speeding up training.
- **Recommended track:** Main conference. The MLSys dual-track (Fall and Spring) offers two opportunities per year; the Spring track is typically less competitive.
- **Competition intensity:** High but lower than NeurIPS. Acceptance rate ~20–25%. Systems papers with strong artifacts (open-source code, reproducibility packages) are favored.
- **Deadline prediction:** Spring cycle abstract ~January, full paper ~February. Fall cycle abstract ~July, full paper ~August. For Paper-2, the **Fall 2026 cycle (~July 2026)** is realistic if writing begins immediately after CX-J1b/c/d results.

**Verdict:** Strong fit if the paper emphasizes the simulator framework, open-source artifact, and deployment-envelope characterization. Weaker if framed purely as theory.

---

### 1.3 DATE (Design, Automation and Test in Europe)

**Scope:** Leading European venue for electronic design automation, test, and embedded systems. Strong analog/mixed-signal and hardware-software co-design communities.

**Fit for Paper-2:** ★★★☆☆ (3/5)

- **Alignment:** DATE has a dedicated track on "Machine Learning for EDA and Test" and a long-standing analog/mixed-signal design community. The CIM simulation framework and mixed digital-analog partition study (E5, G-GG6) fit naturally.
- **Tension:** DATE reviewers expect concrete design automation contributions—tools, algorithms, or silicon demonstrations. A theory-first paper about training-dynamics limits may be seen as too abstract unless tightly coupled to a design-flow implication (e.g., "this limit tells you not to map attention to analog in your next tapeout").
- **Recommended track:** Special session on "AI Hardware and Emerging Technologies" or regular track "Design Methods and Tools."
- **Competition intensity:** Moderate. Acceptance rate ~25–30% for regular papers. Special sessions are by invitation and have higher visibility.
- **Deadline prediction:** Typically **mid-September** (e.g., Sept 15, 2025 for DATE 2026). For DATE 2027, anticipate **~September 14, 2026**.

**Verdict:** Moderate fit. Best suited for a **companion paper** that emphasizes the mixed-partition energy-accuracy Pareto and design-automation workflow, rather than the core structural-limit theory. Consider DATE for a **Paper-3** submission (Year 2, G-GG7).

---

### 1.4 ISSCC (IEEE International Solid-State Circuits Conference)

**Scope:** The premier venue for circuit and system design. Papers report measured silicon results; simulation-only work is extremely rare and faces skepticism.

**Fit for Paper-2:** ★★☆☆☆ (2/5)

- **Alignment:** ISSCC has an "Emerging Technologies" forum and a "Machine Learning Processors" session. Organic CIM arrays have appeared in ISSCC demonstrator sessions.
- **Tension:** Paper-2 is simulation-only and theory-first. ISSCC reviewers prioritize measured energy, area, and speed metrics. A behavioral simulator without silicon validation is unlikely to survive peer review in the main technical program.
- **Recommended track:** **Demo or Forum session only**, not the archival technical program. The compute-ViT framework could be demonstrated as a design-space exploration tool alongside a fabricated organic array.
- **Competition intensity:** Extreme for main program (~20% acceptance). Forum/demo sessions are less selective but non-archival.
- **Deadline prediction:** Typically **early September** (e.g., Sept 3, 2025 for ISSCC 2026). For ISSCC 2027, anticipate **~September 2, 2026**.

**Verdict:** Weak fit for Paper-2 as a standalone archival submission. Strong fit for **Paper-4** (Year 3, G-GG7) if hardware-in-the-loop validation produces measured array data. Consider a non-archival demo at ISSCC 2027 only if partnered with a fabrication group.

---

### 1.5 ASP-DAC (Asia and South Pacific Design Automation Conference)

**Scope:** Major Asia-Pacific venue for design automation and embedded systems. Similar to DATE in scope but with stronger presence from East Asian semiconductor industries.

**Fit for Paper-2:** ★★★☆☆ (3/5)

- **Alignment:** ASP-DAC has a "System Design and Application" track and an increasing number of ML-for-hardware papers. The mixed-partition and surrogate-design aspects fit.
- **Tension:** Same as DATE: theory-first papers must be anchored in a design-flow or tool contribution. The ASP-DAC audience is more industry-oriented than DATE; reviewers may question the commercial relevance of a CIFAR-10 study.
- **Recommended track:** "System Design and Application" or special session on "AI Chip Design."
- **Competition intensity:** Moderate. Acceptance rate ~30%.
- **Deadline prediction:** Typically **early July** (e.g., July 5, 2025 for ASP-DAC 2026). For ASP-DAC 2027, anticipate **~July 3, 2026**.

**Verdict:** Moderate fit. A viable fallback if DATE rejects a companion paper. The shorter review cycle (relative to DATE) makes it attractive for rapid dissemination of Year 2 results.

---

### 1.6 Nature Electronics

**Scope:** High-impact, broad-audience journal spanning electronic materials, devices, circuits, and systems. Emphasizes interdisciplinary significance and societal impact.

**Fit for Paper-2:** ★★★★★ (5/5)

- **Alignment:** Nature Electronics publishes papers that bridge materials/device advances with system-level implications. The structural-limit narrative—"organic CIM promises efficiency but faces a structural barrier in transformer attention"—is precisely the kind of interdisciplinary story the journal seeks. The negative-result framing (preventing wasted fabrication) aligns with sustainability and responsible research narratives.
- **Tension:** The journal expects conceptual novelty accessible to non-specialists. The mathematical machinery (Pillar I–III) must be distilled into intuitive physical arguments without losing rigor. The Methods section must be extensive enough for replication.
- **Recommended format:** Full Article (not Brief Communication). The scope justifies 6,000–8,000 words.
- **Competition intensity:** Extreme. Acceptance rate < 10%. Editorial pre-screening is rigorous; a strong cover letter emphasizing interdisciplinary impact is essential.
- **Deadline prediction:** **Rolling submission**; no fixed deadline. Target submission for **June 2026** to allow time for editorial feedback and potential revision before the end of the grant year.

**Verdict:** Excellent fit. Nature Electronics should be the **primary target** for Paper-2. The theory-first stance, interdisciplinary scope, and falsification methodology are distinctive features that differentiate the paper from incremental device demonstrations.

---

## 2. Comparative Venue Matrix

| Venue | Fit score | Primary audience | Best for | Deadline (predicted) | Competition | Archival? |
|---|---|---|---|---|---|---|
| **Nature Electronics** | ★★★★★ | Interdisciplinary (materials, devices, systems) | Paper-2 core theory | Rolling (target June 2026) | Extreme | Yes |
| **NeurIPS** | ★★★★☆ | ML theory and algorithms | Generalization theory claim | ~May 18, 2026 | Extreme | Yes |
| **MLSys** | ★★★★☆ | ML systems and hardware | Simulator framework artifact | ~July/Aug 2026 (Fall) | High | Yes |
| **DATE** | ★★★☆☆ | EDA and mixed-signal design | Mixed-partition design flow | ~Sept 14, 2026 | Moderate | Yes |
| **ASP-DAC** | ★★★☆☆ | EDA and embedded systems | Fallback for DATE companion | ~July 3, 2026 | Moderate | Yes |
| **ISSCC** | ★★☆☆☆ | Circuit design and silicon | Paper-4 hardware validation | ~Sept 2, 2026 | Extreme | Yes (main); No (forum) |

---

## 3. Twelve-Month Submission Roadmap

The roadmap assumes Paper-2 is the immediate priority, with follow-on papers scheduled according to the three-year grant plan (G-GG7).

### Quarter 2 2026 (April–June)
- **April:** Finalize CX-J1b/c/d results. Lock all numbers.
- **May:** Submit **Paper-2 to NeurIPS 2026** (~May 18 deadline). This is the "fast" track for ML recognition. Simultaneously prepare the Nature Electronics version with expanded Methods and interdisciplinary framing.
- **June:** Submit **Paper-2 to Nature Electronics** (rolling). If NeurIPS accepts, the Nature Electronics submission becomes a significantly expanded version with supplementary device physics. If NeurIPS rejects, the Nature Electronics submission carries the full weight.

### Quarter 3 2026 (July–September)
- **July:** Prepare **MLSys Fall 2026** submission if NeurIPS rejects and the paper needs a systems-oriented venue. Alternatively, prepare an **ASP-DAC 2027** companion paper focusing on the mixed digital-analog partition energy model.
- **August:** If E3/E4 (second-order STE) yields positive results, prepare a **rapid-communication brief** for arXiv and submission to a methods venue (e.g., ICLR 2027 workshop).
- **September:** No major deadline. Use this month for **revision and resubmission** if Q2 submissions receive revise-and-resubmit decisions.

### Quarter 4 2026 (October–December)
- **October:** Prepare **DATE 2027** submission (deadline ~Sept 2026 has passed; target DATE 2027 if not already submitted). Alternatively, prepare a **special-session proposal** for DATE 2027 on "Analog CIM for Transformers: Limits and Opportunities." Special sessions require organizer commitment but guarantee visibility.
- **November:** Begin drafting **Paper-3** (surrogate remedies / attention-free architectures, Year 2 deliverable). Target ICLR 2027 or MLSys Spring 2027.
- **December:** Winter break; minimal submission activity. Conduct internal review of Paper-3 draft.

### Quarter 1 2027 (January–March)
- **January:** Submit **Paper-3 to ICLR 2027** (~late September 2026 deadline has passed; adjust to ICLR 2028 or MLSys Spring 2027). *Correction:* ICLR deadline is typically October. If missed, pivot to **MLSys Spring 2027** (~January deadline).
- **February:** If hardware-in-the-loop validation (Year 3) is ahead of schedule, prepare **ISSCC 2028 Forum abstract** (~Sept 2027 deadline). This is early planning for silicon demonstration.
- **March:** Evaluate acceptance outcomes from Q2 2026 submissions. Plan revision strategy for any pending resubmissions.

---

## 4. Track-Specific Positioning Advice

### For Nature Electronics
- **Title template:** "Structural limits of analog compute-in-memory for vision transformers" or "Why severe write nonlinearity breaks transformer attention on analog arrays."
- **Cover letter emphasis:** (1) Sustainability angle—negative results prevent wasted fabrication. (2) Interdisciplinary bridge—connects organic device physics to learning theory. (3) Actionable guidelines—`NL < 1.5` threshold, 6-bit ADC minimum.
- **Visual summary:** A single figure showing the three converging ceilings + the structural hypothesis schematic (Pillar I–III as icons).

### For NeurIPS
- **Title template:** "A structural generalization barrier for transformers under structured parameter perturbations" or "Falsifying natural mitigations for severe nonlinearity in analog neural networks."
- **Abstract emphasis:** Generalization theory, falsification methodology, pre-registered predictions. Minimize device physics jargon.
- **Supplementary material:** Include full CX-J1b/c/d protocol, statistical power analysis, and open-source code.

### For MLSys
- **Title template:** "compute-ViT v2: Bounding the accuracy envelope of analog-mapped vision transformers" or "Profile-driven simulation and structural limit diagnosis for organic CIM."
- **Artifact emphasis:** Code repository, reproducibility checklist, Docker container, and pre-trained checkpoint manifest. Artifact evaluation score is critical.

### For DATE / ASP-DAC
- **Title template:** "Design-rule extraction for mixed digital-analog vision-transformer accelerators under severe device nonlinearity"
- **Emphasis:** Mixed-partition Pareto, energy model (even if placeholder), and design-automation workflow. The structural-limit theory becomes a "design constraint" rather than the core contribution.

---

## 5. Contingency Planning

| Scenario | Response |
|---|---|
| **NeurIPS rejects Paper-2** | Pivot to MLSys Fall 2026 or ICLR 2027. The structural-limit theory is venue-agnostic; only framing needs adjustment. |
| **Nature Electronics rejects after review** | Consider **Nature Communications** (lower barrier, still high impact) or **IEEE TED** (device-oriented audience, strong fit for hardware validation story). |
| **CX-J1d-2 breaks ceiling before NeurIPS deadline** | Revise Paper-2 to emphasize the **surrogate breakthrough** narrative (R-B, G-GG5) while retaining the structural-limit framework as "what we learned before breaking it." This is a stronger paper, not a weaker one. |
| **CX-J1d-2 fails, but E5 (mixed dig/ana) succeeds** | Add E5 results to Paper-2 Discussion. The paper becomes: "Structural limit exists for full-analog attention, but mixed partition escapes it." This is still a limit theorem with an engineering escape clause. |
| **All top-tier ML venues reject** | Target **IEEE TNANO** special issue on neuromorphic computing or **Frontiers in Neuroscience** (lower impact but guaranteed archival status and receptive audience). |

---

## 6. Summary

**Nature Electronics** is the highest-fitness venue for Paper-2, offering interdisciplinary prestige, rolling submission, and alignment with the theory-first, sustainability-conscious narrative. **NeurIPS** is the highest-risk, highest-reward ML venue; it should be pursued in parallel for rapid recognition. **MLSys** is the optimal systems fallback. **DATE/ASP-DAC** are suited for companion papers emphasizing design-automation and mixed-signal partitioning. **ISSCC** is deferred to Paper-4 (hardware validation). The 12-month roadmap sequences submissions to maximize acceptance probability while preserving strategic flexibility.
