# G-GG7: Grant Proposal Outline v3 — Three-Year Research Plan

**Date:** 2026-04-20  
**Author:** Gemini Phase β — Round P2  
**Scope:** Funding roadmap for NSFC Key Programme / Horizon Europe MSCA-IF or ERC Starting Grant / NSF CISE Core Programs. Theory-first positioning; experimental claims reference locked data or pre-registered protocols only.  
**Sources:** `GEMINI_STRUCTURAL_LIMIT_FORMAL_20260420.md` (G-GG1), `GEMINI_HIGHER_ORDER_NL_DESIGN_20260420.md` (G-GG2), `GEMINI_PATHWAY_DECOMPOSITION_20260420.md` (G-GG3), `GEMINI_FIRST_ORDER_LIMIT_20260420.md` (G-GG4), `GEMINI_PAPER2_ARCH_MEMO_20260420.md` (G-GG5), Paper-1 Discussion (`paper/latex_gpt/sections/06_discussion.tex`), and thesis chapter outlines.

---

## 1. Executive Summary

The analog compute-in-memory (CIM) community has reached an inflection point: device-level demonstrations of organic optoelectronic synaptic arrays are mature, yet system-level accuracy guarantees for modern neural architectures remain elusive. Our prior work established a profile-driven behavioral framework (compute-ViT) that maps literature-derived device parameters to task-level vision accuracy, and identified a fresh-instance transfer failure mode that standard hardware-aware training (HAT) cannot mitigate under severe write nonlinearity.

This proposal asks: **What are the theoretical and algorithmic boundaries of analog CIM for Vision Transformers, and how can they be relaxed through higher-fidelity training surrogates, architectural co-design, or materials-level intervention?** We approach the question through a falsification methodology: pre-registering structural hypotheses, designing experiments capable of refuting them, and using converging negative evidence to bound the deployment envelope.

The work is organized into three thrusts:
- **Thrust I (Year 1):** Structural limits and diagnostic theory — formalizing the attention-pathway barrier under first-order surrogates.
- **Thrust II (Year 2):** Surrogate fidelity and algorithmic remedies — second-order Taylor-corrected STE, cumulant expansion, and iterative programming models.
- **Thrust III (Year 3):** Hardware-in-the-loop validation and architectural co-design — correlating simulator predictions with measured organic-array statistics and exploring attention-free hybrids.

---

## 2. Intellectual Merit and Novelty

### 2.1 Novelty relative to prior work
Existing CIM simulators (AIHWKIT, CrossSim, MemTorch) treat device noise as i.i.d. perturbation or lookup-table error. None systematically test severe nonlinearity (`NL ≥ 2.0`) against fresh-instance transfer in Vision Transformers. Our structural-limit hypothesis (G-GG1) is the first theoretical framework to explain *why* the attention pathway is disproportionately fragile, with three falsifiable mathematical conditions.

### 2.2 Broader impact
- **For device engineering:** Honest reporting of structural limits prevents wasted fabrication runs (estimated `$50k–$200k` per organic-array mask set).
- **For algorithm design:** The higher-order surrogate family (G-GG2) provides a closed-form, low-overhead training modification compatible with existing PyTorch stacks.
- **For architecture design:** The mixed digital-analog partition study (E5, G-GG6) quantifies the accuracy-cost trade-off of removing attention from analog arrays.

### 2.3 Theory-first positioning
The proposal does not seek to maximize accuracy benchmarks. It seeks to **bound what is achievable** under well-defined physical approximations. This epistemic stance is rare in the hardware-aware ML literature, which is overwhelmingly benchmark-driven.

---

## 3. Three-Year Research Plan

### Year 1 — Structural Limits and Diagnostic Theory

**Objective:** Formalize the structural-limit hypothesis, execute the CX-J1b/c/d diagnostic suite, and publish Paper-2.

**Milestones:**
- M1.1 (Q1): Complete CX-J1b/c experiments (QKV-only and output-projection-only linearization). Pre-register predictions in a public registry (e.g., OSF).
- M1.2 (Q2): Complete rank-collapse diagnostic (E6, G-GG6). Validate Pillar I of G-GG1 via SVD trajectory analysis.
- M1.3 (Q2): Submit Paper-2 to a top-tier ML or interdisciplinary venue (target: Nature Electronics or NeurIPS; see G-GG9).
- M1.4 (Q3): Extend the structural-limit framework to **spatially correlated D2D** (AR(1) separable perturbation). Paper-1 Supplementary Note showed bounded degradation at `ρ = 0.3` and `ρ = 0.5`; Year 1 will derive analytical bounds on correlation-induced rank collapse.
- M1.5 (Q4): Develop a **layer-wise information-bottleneck theory** for analog transformers. Quantify how much mutual information between tokens is preserved under NL-distorted QKV projections.

**Deliverables:**
- Paper-2 (submitted)
- Technical report on correlated-D2D bounds
- Open-source release of diagnostic logging utilities (`wandb` integration for gradient scaling, attention-map KL divergence, Q/K rank)

### Year 2 — Surrogate Fidelity and Algorithmic Remedies

**Objective:** Test whether higher-order surrogates, mixed digital-analog partitions, or architectural redesign can break the structural ceiling.

**Milestones:**
- M2.1 (Q1): Implement and evaluate second-order STE (CX-J1d-2) and cumulant expansion (CX-J1d-3). Report whether the ceiling is broken or persists.
- M2.2 (Q2): If higher-order surrogates fail, pivot to **iterative programming models** (G-GG4, §5.2): unroll a write-verify pulse sequence and differentiate through the loop. This is computationally expensive (`10×–100×` surrogate cost) but physically faithful.
- M2.3 (Q2): Evaluate **attention-free architectures** (MLP-Mixer, State Space Models such as Mamba) under the same severe-NL protocol. If these architectures tolerate `NL = 2.0`, the structural limit is specific to self-attention, not to dense linear transforms generally.
- M2.4 (Q3): Design and simulate a **mixed digital-analog Tiny-ViT partition** (E5, G-GG6) with energy annotation. Quantify the Pareto frontier of energy versus accuracy under the partition.
- M2.5 (Q4): Synthesize Year 2 results into **Paper-3**: "Beyond First-Order Surrogates: Algorithmic and Architectural Remedies for Severe Nonlinearity in Analog CIM."

**Deliverables:**
- Paper-3 (submitted)
- PyTorch extension package (`analog_layers_v2`) with second-order STE and cumulant hooks
- Energy-accuracy Pareto dataset for mixed-partition designs

### Year 3 — Hardware-in-the-Loop Validation and Co-Design

**Objective:** Correlate simulator predictions with measured organic-array data and transfer validated design rules to fabrication partners.

**Milestones:**
- M3.1 (Q1–Q2): Establish collaboration with a fabrication group (organic RRAM or OPECT array). Collect measured conductance-update curves, D2D mismatch maps, and retention trajectories.
- M3.2 (Q2): Fit **device-specific profiles** to measured data. Test zero-shot simulator transfer: does a model trained on the literature-derived DNTT profile generalize to the measured profile without retraining?
- M3.3 (Q3): Execute **hardware-in-the-loop HAT**: use measured array conductances as the forward-pass noise source during training. Compare accuracy against purely simulated training.
- M3.4 (Q3): Validate the **structural-limit boundary** on real devices. If measured `NL < 1.5`, the analog-attention pathway is viable; if measured `NL > 2.0`, the mixed-partition or attention-free designs from Year 2 become the recommended architecture.
- M3.5 (Q4): Publish **Paper-4** (venue: ISSCC, JSSC, or Nature Electronics) reporting measured validation and the final co-design guidelines.

**Deliverables:**
- Paper-4 (submitted)
- Validated device-profile library with measured data
- Final design-rule memo for fabrication partners (see G-GG8)

---

## 4. Budget Framework (Category Percentages)

No specific monetary amounts are given, as they depend on the funding scheme, host institution overhead rates, and national cost-of-living adjustments. The following category proportions are calibrated against typical Horizon Europe MSCA-IF, NSF CRII/CISE, and NSFC Key Programme awards.

| Category | Proportion | Rationale |
|---|---|---|
| **Personnel (PI + PhD/Postdoc)** | 55–60% | Primary cost. One PhD student (Years 1–3) and one postdoc (Years 2–3). PI effort: 30% academic year + 1 summer month. |
| **Equipment (GPU cluster + measurement setup)** | 15–20% | GPU node (4× A100 or equivalent) for training; semiconductor parameter analyzer or custom PCB for array characterization in Year 3. |
| **Travel and Collaboration** | 8–10% | International conference attendance (NeurIPS, DATE, ISSCC); fabrication-lab visits; invited seminar exchanges. |
| **Open Science and Dissemination** | 3–5% | Article processing charges (APC) for open-access venues; dataset hosting (Zenodo); code repository maintenance; reproducibility challenge prizes. |
| **Indirect / Overhead** | 12–18% | Host institution facilities and administration. Varies by country (UK: ~40% full economic cost; US: ~26% federally negotiated rate; China: ~5–10% management fee). |

### 4.1 Multi-scheme calibration
- **NSF CISE Core (3 years, ~$600k):** Emphasize algorithmic contributions (Thrusts I–II). Hardware validation is scoped to collaboration with an existing fabrication group (no new equipment). Budget shifts toward personnel (65%) and travel (12%).
- **Horizon Europe ERC Starting Grant (5 years, ~€1.5M):** Expand Thrust III to include full custom array design and tapeout support. Add a second PhD student and a technician. Budget shifts toward equipment (25%) and personnel (50%).
- **NSFC Key Programme (4 years, ~¥3M):** Emphasize domestic fabrication partnerships and optoelectronic device co-design. Budget shifts toward equipment (20%) and collaborative travel (10%).

---

## 5. Expected Outcomes and Impact Metrics

### 5.1 Publication targets
| Year | Target venue | Submission | Anticipated outcome |
|---|---|---|---|
| 1 | Nature Electronics or NeurIPS | Q2 | Paper-2: Structural limits |
| 2 | ICLR or MLSys | Q3 | Paper-3: Surrogate remedies |
| 2 | IEEE TED or JSSC | Q4 | Device-oriented companion |
| 3 | ISSCC or Nature Electronics | Q3 | Paper-4: Hardware validation |

### 5.2 Software and data
- **compute-viT v2.0:** Extended with second-order STE, cumulant hooks, and hardware-in-the-loop adapter.
- **Organic CIM Benchmark Suite:** Standardized train/test splits, device profiles, and evaluation protocols for CIFAR-10/100 and (if scaled) Tiny-ImageNet.
- **Diagnostic Dashboard:** Interactive visualization of attention-map KL divergence, Q/K rank trajectories, and gradient-scaling histograms.

### 5.3 Training and career development
- One PhD student trained at the intersection of ML theory, device physics, and systems architecture.
- One postdoc with a profile in hardware-aware training or neuromorphic engineering.
- Open reproducibility tutorials at major conferences (NeurIPS reproducibility workshop, DATE tutorial track).

### 5.4 Quantitative impact metrics (Year 3 retrospective)
- Citation target for Paper-2: > 50 citations (structural-limit papers in niche hardware-ML intersection typically accumulate slowly but durably).
- Open-source repository stars/downloads: > 200 GitHub stars; > 10 independent reproducibility reports.
- Hardware validation: Correlation coefficient `R² > 0.85` between simulator-predicted and measured task-level accuracy.
- Patent filings: 1–2 provisional patents on higher-order STE or mixed-partition architectures (see G-GG8).

---

## 6. Risk Assessment and Contingencies

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| CX-J1d (second-order STE) breaks ceiling unexpectedly | Medium | High — Paper-2 narrative must pivot from "limit" to "surrogate breakthrough" | Pre-register both interpretations. The paper remains valuable: it shows *how* the barrier is broken. R-A skeleton already contains this branch (G-GG5, §6.2). |
| Fabrication partner withdraws in Year 3 | Medium | High — Thrust III collapses | Maintain two parallel partnership conversations (domestic and international). Scope Year 3 to "measured data from *any* organic array source," not a specific lab. |
| MLP-Mixer / Mamba also collapses under `NL = 2.0` | Low | Medium — Implies barrier is generic to dense linear transforms, not attention-specific | Publish honestly. The result is still valuable: it bounds *all* analog-mapped deep networks, not just transformers. |
| Reviewer rejection of negative-result framing | Medium | Medium — Some venues still penalize null results | Target venues with explicit reproducibility or negative-result tracks (NeurIPS reproducibility workshop, PMLR R0-FoMo workshop, IEEE TNANO special issues). |
| GPU cluster unavailability | Low | Low | All training is feasible on single-node consumer GPUs (RTX 4090 / 24 GB). Cloud credits (AWS/Azure) are a fallback. |

---

## 7. Alignment with Funding Schemes

### 7.1 NSF CISE (US)
- **Relevant programs:** CCF (Algorithmic Foundations), SHF (Software and Hardware Foundations), TI (Trustworthy AI).
- **Fit:** Thrusts I–II align with CCF (theoretical analysis of training dynamics under perturbation) and SHF (hardware-software co-design). The theory-first stance satisfies NSF's emphasis on rigorous foundations.
- **Broader impacts:** Open-source software, reproducibility protocols, and curriculum development for hardware-aware ML courses.

### 7.2 Horizon Europe (EU)
- **Relevant programs:** ERC Starting Grant (PE6: Computer Science and Informatics), MSCA Postdoctoral Fellowships, Chips Joint Undertaking (design pillar).
- **Fit:** The deployment-envelope framing (G-GG5, §6.3) aligns with Chips JU industrial translation goals. The organic-device focus is compatible with EU Green Deal priorities (low-energy neuromorphic computing, bio-compatible materials).
- **Collaboration requirement:** Identify an EU host institution with fabrication access (e.g., IMEC, CNRS, or TU Dresden / NaMLab).

### 7.3 NSFC Key Programme (China)
- **Relevant programs:** Key Programme (重点项目) under Department of Information Sciences; Major Research Plan on "Intelligent Computing" (智能计算专项).
- **Fit:** The information-bottleneck theory (M1.5) and structural-limit formalism align with NSFC's growing emphasis on "fundamental theory of intelligent systems." The optoelectronic device focus fits the "new display and flexible electronics" strategic area.
- **Team requirement:** A domestic fabrication partner (e.g., Institute of Physics, CAS; Fudan University flexible electronics group; SJTU micro-nano fabrication facility) is essential.

---

## 8. Summary

This grant outline proposes a three-year, three-thrust research program that moves from theoretical diagnosis (Year 1) to algorithmic and architectural remedies (Year 2) to hardware validation (Year 3). The budget framework is flexible across NSF, Horizon Europe, and NSFC schemes. The epistemic stance is theory-first and falsification-oriented: we seek to bound the achievable, report negative results honestly, and use converging evidence to guide the analog-CIM community toward high-payoff investments. The expected outcomes include four peer-reviewed papers, two open-source software releases, one validated device-profile library, and design rules transferable to fabrication partners.
