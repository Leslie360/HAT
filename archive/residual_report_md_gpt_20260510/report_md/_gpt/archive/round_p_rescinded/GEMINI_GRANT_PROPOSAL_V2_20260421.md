# Structural Limits of First-Order CIM Surrogates: From Diagnostic Characterization to Next-Generation Architectures

**Date:** 2026-04-21 | **Duration:** 36 months | **Building from:** NC submission + PhD thesis

---

## 1. Program Title

**Structural Limits of First-Order CIM Surrogates: A Diagnostic-to-Design Pipeline for Organic Optoelectronic Compute-in-Memory**

---

## 2. Specific Aims

### Aim 1 — Characterize Structural Limits of First-Order CIM Surrogates (Years 1–2)

The NC paper showed Ensemble HAT recovers fresh-instance accuracy from 10 % to 86.37 %, yet left a critical question open: *why* does the surrogate still fail under correlated D2D variation? This aim treats first-order models as hypotheses to be falsified.

**Sub-aim 1a:** Systematic falsification of mitigation strategies. Reproduce and stress-test Ensemble HAT, parametric noise injection, learned affine calibration, and domain randomization under controlled (NL, γ, correlation) sweeps. Each strategy receives a falsification score: the physical severity at which accuracy collapses beyond 5 %.

**Sub-aim 1b:** Diagnostic experiments to isolate the failure mode (CX-J1b/c/d). Ablate the surrogate layer-by-layer to determine whether the bottleneck is input-referred noise amplification, rank collapse in attention projections, or temporal drift. Layer-wise Jacobian spectra and Fisher Information traces quantify where first-order approximations break.

**Sub-aim 1c:** Higher-order surrogate validation (CX-J1d). Fit second-order polynomial conductance models and compare accuracy ceilings against the linear baseline. A ceiling shift isolates NL as the dominant limit; absence implicates spatial coupling or drift.

### Aim 2 — Develop Next-Generation Surrogates and Architectures (Years 1–3)

Once the structural limit is diagnosed, this aim engineers around it.

**Sub-aim 2a:** Second- and third-order nonlinear surrogates. Extend compute_vit to polynomial conductance maps up to 3rd order, with automatic differentiation through the physical forward pass. Target: <2 % accuracy gap to behavioral SPICE on 128 × 128 tiles at 20 % NL.

**Sub-aim 2b:** Attention-free architectures for severe nonlinearity. If attention proves disproportionately sensitive to NL, adapt Mamba-style state-space and pooling-based architectures that replace Q/K/V with linear-recurrent or convolutional operators, trading modest accuracy for analog robustness.

**Sub-aim 2c:** Hybrid digital-analog attention engines. For moderate NL, design split-precision attention: analog CIM for MLP projections, digital SRAM for Q/K/V with 6-bit fixed-point MAC. A precision-routing scheduler allocates bit-width per layer from per-token sensitivity profiles.

### Aim 3 — Hardware-in-the-Loop Validation (Years 2–3)

Validate diagnosed structural limits on FPGA. The forward-pass noise model—informed by the exact nonlinearity order from Aim 1—is replayed through measured device profiles while back-propagation stays digital. By Month 30, deliver iso-accuracy contours in (nonlinearity order, temperature, retention time) space as design rules for fabricators.

---

## 3. Milestones

| Milestone | Target | Deliverable |
|-----------|--------|-------------|
| M1.1 | Month 6 | Falsification matrix for 4 strategies across (NL, γ, correlation); dataset released. |
| M1.2 | Month 12 | Diagnostic report (CX-J1b/c/d) identifying dominant failure mode; spectra published. |
| M1.3 | Month 18 | Higher-order surrogate validated; ceiling shift quantified; 1 conference submission. |
| M2.1 | Month 12 | 2nd-order surrogate in compute_vit; <2 % SPICE gap on 128 × 128 tile. |
| M2.2 | Month 24 | Attention-free architecture under 20 % NL; accuracy-per-Joule baseline locked. |
| M2.3 | Month 30 | Hybrid digital-analog engine on FPGA; scheduler operational; 1 journal submission. |
| M3.1 | Month 18 | FPGA kernel validated; ≥99 % bit-exact agreement on ResNet-18 CIFAR-10. |
| M3.2 | Month 24 | Correlated-D2D mask from wafer maps; structural-limit predictions confirmed in HIL. |
| M3.3 | Month 30 | Iso-accuracy contour map delivered to fabrication partner; design-rule brief published. |

---

## 4. Personnel

| Role | FTE | Responsibility |
|------|-----|----------------|
| PhD Student (continuing) | 1.0 | Diagnostic experiments (Aim 1); surrogate extension (Aim 2); thesis completion (Month 36). |
| Postdoc — Analog Devices | 0.75 | Higher-order fitting (Aim 1c); FPGA HIL (Aim 3); wafer-level measurement campaigns. |
| Collaborator — Fabrication | 0.25 (in-kind) | Organic tape-out; measured profile delivery; design-rule feedback. |
| PI / Advisor | 0.25 | Strategic direction; collaborator coordination; grant administration. |

---

## 5. Budget Tiers

| Tier | Amount | Scope |
|------|--------|-------|
| **Lean** | **$300K** | 1 PhD student (3 yr); GPU upgrade (2× A6000 Ada); travel ($6K/yr); cloud credits ($10K/yr). |
| **Moderate** | **$600K** | Above + 1 postdoc (2 yr); FPGA board (ZCU102 + mezzanine, ~$15K); expanded travel ($12K/yr); summer intern. |
| **Full** | **$1.2M** | Above + fabrication run (~$350K); FPGA cluster (4× Alveo U55C, ~$80K); foundry liaison; 2 workshops. |

---

## 6. Risk Mitigation

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| **Higher-order surrogate fails to break ceiling.** | Medium | Pivot to theory paper: formal proof that first-order error propagates exponentially through attention layers, establishing a fundamental analog-CIM bound. |
| **Higher-order surrogate breaks ceiling.** | Medium | Pivot to engineering paper: tape-out the validated surrogate with design-rule extraction, targeting ISSCC/CICC. |
| **Diagnostic ambiguity:** Spectra do not isolate a single failure mode. | Low–Medium | Combine Jacobian, Fisher, and activation histograms into a composite diagnostic index; publish methodology paper. |
| **Fabrication delay:** Wafer delivery slips beyond Month 24. | Medium | All M3 milestones achievable with synthetic profiles validated against literature data; HIL proceeds without tape-out. |

---

## 7. Expected Outcomes

1. **Peer-reviewed papers:** 2–3 — (i) Structural-limit falsification (NeurIPS MLSys/ICML); (ii) Next-generation surrogates (*Nature Electronics* / *IEEE JSSC*); optional (iii) Theory of first-order error propagation (COLT/ALT or *IEEE TCAS-I*).
2. **Open-source release:** compute_vit v2.0 — polynomial surrogate engine, diagnostic toolkit, attention-free benchmarks, and 5-seed falsification matrix (Zenodo deposit).
3. **Thesis completion:** 1 PhD dissertation defending the diagnostic-to-design program by Month 36.
4. **Secondary artifacts:** 1 design-rule brief for fabrication partner; 1 workshop/tutorial at a major EDA or ML conference.

---

*End of proposal outline.*
