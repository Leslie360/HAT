# G-GG8: Industrial Partnership Brief v2 — Technology Translation and IP Strategy

**Date:** 2026-04-20  
**Author:** Gemini Phase β — Round P2  
**Scope:** Positioning memo for semiconductor and optoelectronic enterprise engagement. No specific company names; domain-level partner typology only. Theory-first stance preserved: technology claims are bounded by surrogate-class assumptions.  
**Sources:** `GEMINI_STRUCTURAL_LIMIT_FORMAL_20260420.md` (G-GG1), `GEMINI_HIGHER_ORDER_NL_DESIGN_20260420.md` (G-GG2), `GEMINI_PAPER2_ARCH_MEMO_20260420.md` (G-GG5), `GEMINI_PAPER2_EXP_DESIGN_20260420.md` (G-GG6), `GEMINI_GRANT_V3_20260420.md` (G-GG7), Paper-1 Discussion (`paper/latex_gpt/sections/06_discussion.tex`), and thesis chapter outlines.

---

## 1. Executive Summary for Industry Partners

Analog compute-in-memory (CIM) with organic optoelectronic devices promises orders-of-magnitude energy efficiency for edge vision, but a critical translation gap remains: device-level demonstrations do not guarantee system-level accuracy. Our compute-ViT framework closes this gap by mapping literature-derived device parameters to task-level vision accuracy before fabrication commitment.

**The key message for partners:** We have identified a structural generalization barrier that arises when severe write nonlinearity (`NL ≥ 2.0`) interacts with Vision Transformer attention pathways under standard training recipes. This barrier is **not a materials impossibility**—it is a boundary condition. We provide three actionable responses:

1. **Device engineering:** Push write nonlinearity below `NL ≈ 1.5` for analog-mapped attention blocks.
2. **Algorithm engineering:** Adopt higher-order training surrogates (second-order STE) if `NL` cannot be reduced.
3. **Architecture engineering:** Migrate attention computations to digital SRAM while keeping MLP and patch-embedding layers in analog arrays.

Each response has quantifiable accuracy, energy, and area trade-offs. This brief provides the decision framework.

---

## 2. Technology Maturity Assessment (TRL Scale)

### 2.1 Current TRL by component

| Component | TRL | Evidence | Gap to next level |
|---|---|---|---|
| **Organic optoelectronic device physics** | 3–4 | Demonstrated multilevel conductance tuning, retention, and photoresponse in discrete devices and small arrays (`guo2024organic`, `zhang2025opect`, `vincze2025dualplasticity`). | Array-level statistical characterization (>`1 kbit`) with matched simulator calibration. |
| **Behavioral simulation framework (compute-ViT)** | 3 | Profile-driven accuracy evaluation for ResNet-18, ConvNeXt-Tiny, and Tiny-ViT-5M on CIFAR-10/100. Cross-validated against CrossSim (`run_framework_comparison.py`). | Integration with SPICE-level compact models for parasitic-aware prediction. |
| **Hardware-aware training (Ensemble HAT)** | 3 | Simulation-only validation. Recovers `86.37 ± 1.54%` fresh-instance accuracy under moderate NL (`NL = 1.0`). | Hardware-in-the-loop validation on measured arrays. |
| **Higher-order surrogate (second-order STE)** | 2 | Mathematical design complete (G-GG2); implementation path defined. No experimental validation yet. | CX-J1d-2 execution and fresh-instance evaluation. |
| **Mixed digital-analog partition** | 2 | Conceptual design and energy model (placeholder constants). No layout or silicon demonstration. | Floor-planning and energy annotation with real parasitic extraction. |
| **Inverse-gamma front-end compensation** | 3 | Simulation-validated on CIFAR-10 (`+5.8` pp at `γ_phys = 2.0`). | CMOS readout circuit integration and noise-amplification characterization. |

### 2.2 Aggregate TRL judgment

The overall technology readiness is **TRL 3** (analytical and experimental critical function and/or characteristic proof of concept). The simulation framework has matured to the point where it can rank design choices and bound operating envelopes, but it has not been validated against fabricated organic CIM chips executing end-to-end ViT inference. The path to TRL 4 (component and/or breadboard validation in a laboratory environment) requires hardware-in-the-loop correlation; the path to TRL 5 (component and/or breadboard validation in a relevant environment) requires a fabricated array with integrated readout and digital peripheral logic.

**Partner implication:** Engagements at this stage are **co-development partnerships**, not technology licensing. The value proposition is risk reduction: our simulator prevents partners from committing to device recipes or array geometries that are predicted to fail at the system level.

---

## 3. Value Proposition by Partner Type

### 3.1 Type A: Organic semiconductor / device foundries
- **Pain point:** Device papers report conductance windows and switching ratios, but foundries lack feedback on which parameters matter for neural-network accuracy.
- **Our offer:** A calibrated accuracy-to-parameter sensitivity map. For example: reducing `NL` from `2.0` to `1.5` is predicted to have a larger accuracy impact than reducing `σ_D2D` from `10%` to `5%` in the attention pathway. This prioritizes process-development investment.
- **Collaboration mode:** Joint characterization campaigns. We provide simulation predictions; the foundry provides measured conductance distributions. Discrepancies drive surrogate refinement.

### 3.2 Type B: Analog / mixed-signal IC design houses
- **Pain point:** CIM macros are designed for CNNs (regular convolutions, ReLU); ViT attention requires high-precision matrix-vector products and dynamic softmax normalization, which analog arrays struggle to implement efficiently.
- **Our offer:** A partitioning guideline: which layers should be analog, which digital, and at what ADC precision. Our analysis shows that 6-bit ADC is the minimum viable precision for transformer deployment; below this, accuracy collapses regardless of conductance control.
- **Collaboration mode:** Co-design of mixed-signal floor plans. We provide accuracy constraints as design specifications; the design house provides energy/area estimates.

### 3.3 Type C: Edge-AI system integrators (automotive, robotics, wearables)
- **Pain point:** System integrators need accuracy guarantees under environmental variation (temperature, aging, batch-to-batch device variation).
- **Our offer:** Distributional training protocols (Ensemble HAT) that bake deployment variation into the training objective, yielding accuracy bounds rather than point estimates. Fresh-instance evaluation provides a statistical guarantee across hardware batches.
- **Collaboration mode:** Requirements-flow translation. The integrator specifies target accuracy (`> 85%` on CIFAR-10) and environmental stress range; we map this to device-parameter bounds.

### 3.4 Type D: EDA and simulation software vendors
- **Pain point:** Existing CIM simulators (CrossSim, AIHWKIT) do not natively support spatially structured D2D mismatch maps or organic-device-specific profiles.
- **Our offer:** A device-profile interface specification and reference implementations for severe-NL surrogates. Integration into commercial simulation workflows.
- **Collaboration mode:** API co-development or open-source plugin architecture.

---

## 4. Intellectual Property Strategy

### 4.1 Background IP
The compute-ViT framework, Ensemble HAT protocol, and inverse-gamma preprocessor were developed in the context of an academic thesis. Depending on host-institution policy, these may be subject to **automatic institutional ownership** or **student retention** of copyright. The following actions are recommended before any partnership negotiation:

1. **Clarify ownership:** File an invention disclosure with the technology transfer office (TTO) for:
   - Ensemble HAT (per-epoch D2D resampling protocol)
   - Group-wise heterogeneous surrogate training
   - Inverse-gamma front-end compensation for sublinear photoresponse
   - Second-order Taylor-corrected STE (if experimental validation succeeds)

2. **Open-source defensive publication:** The core simulation framework is already documented in open repositories. This creates **prior art** that prevents third parties from patenting the basic protocol, while preserving freedom to file on specific implementations.

### 4.2 Foreground IP — patentable inventions
The following inventions have provisional patent potential, contingent on experimental validation:

| Invention | Status | Patentability assessment | Suggested filing timeline |
|---|---|---|---|
| **Second-order STE for analog CIM training** | Mathematical design complete; awaiting CX-J1d-2 validation | High. Novel gradient-correction method specific to nonlinear conductance programming. Clear industrial utility. | Within 6 months of positive CX-J1d-2 result. |
| **Mixed digital-analog ViT partition with accuracy-guaranteed boundary** | Conceptual; energy model is placeholder | Medium. The partitioning idea is not novel per se, but the *accuracy-boundary condition* (`NL < 1.5` for analog attention) derived from systematic falsification may be patentable as a design rule. | After E5 (mixed dig/ana) execution and energy annotation. |
| **Group-wise heterogeneous NL surrogate selector** | Implemented in `run_tinyvit_groupwise_nl_comp.py` | Low. A software-implemented training heuristic may struggle to meet subject-matter eligibility in some jurisdictions (US Alice Corp restrictions). Better protected by copyright and trade secret. | Do not patent; maintain as open-source with BSD license. |
| **Hardware-instance overfitting detection metric** | Conceptual: a diagnostic that flags when a checkpoint has overfit to a specific D2D realization | Medium. A method for quality control of neural-network deployment on analog hardware. | After fresh-instance protocol standardization. |

### 4.3 Licensing model recommendations
- **Framework code (compute-ViT):** Release under permissive license (MIT or BSD-3). This maximizes adoption and citation, creating network effects that benefit downstream licensing.
- **Device profiles:** Release under Creative Commons BY-SA. Encourages community contribution while requiring attribution.
- **Patented training methods (second-order STE, mixed partition):** Offer **non-exclusive royalty-bearing licenses** to foundries and design houses. Retain academic use rights.
- **Consulting and bespoke simulation:** For partners requiring custom profiles or integration support, offer **fee-for-service consulting** rather than exclusive IP licenses. This preserves flexibility and avoids lock-in.

### 4.4 Freedom-to-operate (FTO) risks
- **IBM AIHWKIT:** Check whether Ensemble HAT or second-order STE implementations infringe on any IBM patents covering "analog training tiles" or "stochastic pulse updates." Preliminary assessment: no direct overlap, as AIHWKIT focuses on inference-time drift and closed-loop programming, not epoch-level D2D resampling or curvature-corrected gradients.
- **CrossSim:** No FTO concern; CrossSim is open-source and our framework is cross-validated against it, not derived from it.
- **Samsung / SK hynix CIM patents:** Major memory manufacturers hold broad CIM patents. A formal FTO search is recommended before any hardware tapeout.

---

## 5. Partnership Roadmap (12-Month Horizon)

### Months 1–3: Internal preparation
- File invention disclosures with TTO.
- Draft non-confidential technical brief (this memo, sanitized).
- Prepare one-page capability statements for each partner type (A–D).
- Update open-source repository with clean documentation and reproducibility checklist.

### Months 4–6: Outreach and discovery
- **Target Type A:** Approach 2–3 organic-device research groups at conferences (MRS, EMRS, SPIE Photonics West). Goal: identify one group with measured `NL ≥ 1.5` data willing to share for simulation calibration.
- **Target Type B:** Approach mixed-signal design groups at DATE or ISSCC. Goal: gather feedback on 6-bit ADC cliff and mixed-partition energy estimates.
- **Target Type C:** Approach edge-AI product managers at embedded-vision summits. Goal: validate accuracy requirements and environmental stress ranges.

### Months 7–9: Pilot collaboration
- Execute one **joint characterization pilot** with a Type A partner: measured D2D map → simulator calibration → accuracy prediction → discrepancy analysis.
- Execute one **co-design study** with a Type B partner: mixed-partition floor plan + parasitic-aware energy estimate.

### Months 10–12: Agreement structuring
- Negotiate **MTA (Material Transfer Agreement)** for measured data if not already in place.
- Negotiate **MTA / NDA / Collaboration Agreement** for joint IP. Default to non-exclusive terms.
- Prepare **Phase 2 proposal** (grant or internal R&D funding) contingent on pilot results.

---

## 6. Risk Factors for Partners

| Risk | Severity | Mitigation for partner |
|---|---|---|
| Simulation predictions do not match silicon | High | We explicitly scope predictions as "risk ranking" rather than "chip-accurate emulation." Hardware-in-the-loop validation is a funded objective (G-GG7, Year 3). |
| Negative results discourage device investment | Medium | We frame structural limits as **boundary conditions**, not impossibility proofs. The `NL < 1.5` guideline tells engineers where to aim, not to abandon the field. |
| Open-source code dilutes competitive advantage | Low | The core value is not the code but the **calibrated device profiles and design rules**. These require partnership-specific measurements and are not fully replicable from public repositories. |
| Academic timeline misalignment with product roadmap | Medium | Pilot engagements are scoped to 3–6 months with clear go/no-go milestones. No long-term exclusivity is requested at TRL 3. |

---

## 7. Summary

The compute-ViT framework is at TRL 3, ready for co-development partnerships rather than technology licensing. The primary value proposition for industrial partners is **risk reduction**: bounding the accuracy impact of device non-idealities before expensive fabrication commitments. The IP strategy balances open-source dissemination (for adoption and citation) with selective patenting of validated training methods and design rules. A 12-month partnership roadmap prioritizes organic-device foundries (Type A) and mixed-signal design houses (Type B) for pilot engagements, with the goal of hardware-in-the-loop validation by Year 3. Specific company names are withheld pending bilateral non-disclosure discussions.
