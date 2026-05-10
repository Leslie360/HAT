# Next-Grant Proposal Outline: From Behavioral Simulation to Physical Tape-Out in Organic Optoelectronic CIM

**Date:** 2026-04-20 | **Duration:** 36 months | **Building from:** NC submission + PhD thesis

---

## 1. Program Title

**Closing the Simulation-to-Silicon Gap for Organic Optoelectronic CIM: Joint Training and Physical Realism**

---

## 2. Specific Aims

### Aim 1 — Joint Training → Hardware-in-the-Loop (Years 1–2)

The NC paper showed Ensemble HAT recovers fresh-instance accuracy from 10 % to 86.37 % in simulation. This aim closes the loop by porting the forward-pass noise model onto an FPGA emulation board and re-training Tiny-ViT / ConvNeXt surrogates with real analog-macro latencies and ADC quantization per layer. By Month 18 we will have a hardware-in-the-loop (HIL) trainer replaying measured device profiles through the FPGA while back-propagation stays digital, validating whether the 6-bit ADC cliff and Ensemble HAT schedule survive physical clocking.

### Aim 2 — Language-Model CIM Scaling (Years 1–3)

Current experiments are vision-only (CIFAR-10/100, Tiny-ImageNet). This aim extends compute_vit to language-model inference on tiled CIM macros, targeting TinyLLaMA-1.1B and Phi-2-sized models. We will profile attention-layer sensitivity to retention drift and IR-drop under sequences of 512–4,096 tokens, and develop a precision-routing scheduler allocating higher bit-widths to Q/K projections and aggressive quantization to MLP down-projections. Target: <3 % perplexity degradation at 4-bit effective precision relative to FP32.

### Aim 3 — Full Physical-Realism Pipeline (Years 2–3)

The NC paper uses isolated parameter proxies (1 % placeholders for spatial effects). This aim replaces them with coupled physical models: spatial IR-drop (P1), sneak-path currents (P2), and thermal-dependent retention (P5) solved self-consistently per tile. A compact thermal model (64 × 64 finite-difference grid) feeds temperature maps back into conductance drift equations, validated against measured wafer data. By Month 30 the pipeline produces iso-accuracy contours in (temperature, retention time, supply-voltage) space, yielding direct design rules for fabricators.

---

## 3. Milestones

### Aim 1 Milestones

| Milestone | Target | Deliverable |
|-----------|--------|-------------|
| M1.1 | Month 6 | FPGA noise-injection kernel validated against compute_vit baseline; bit-exact agreement ≥99 % on ResNet-18 CIFAR-10. |
| M1.2 | Month 12 | End-to-end HIL trainer operational; Ensemble HAT ported; fresh-instance recovery ≥80 % on Tiny-ViT. |
| M1.3 | Month 18 | Correlated-D2D spatial mask loaded from measured wafer maps; MLP-linear joint training baseline established; 1 conference submission. |

### Aim 2 Milestones

| Milestone | Target | Deliverable |
|-----------|--------|-------------|
| M2.1 | Month 12 | compute_vit extended to LLM layers; attention-sensitivity profiling complete; 512-seq baseline perplexity locked. |
| M2.2 | Month 24 | Precision-routing scheduler implemented; 4-bit effective precision target met on TinyLLaMA-1.1B Wikitext-2. |
| M2.3 | Month 30 | Retention-drift stress test under 1K-token generation; adaptive refresh policy designed; 1 journal submission. |

### Aim 3 Milestones

| Milestone | Target | Deliverable |
|-----------|--------|-------------|
| M3.1 | Month 18 | Coupled IR-drop + sneak-path SPICE netlist validated against analytical proxies; discrepancy <2 % on 128 × 128 tile. |
| M3.2 | Month 24 | Thermal-retention co-simulation operational; temperature-dependent γ × NL interaction sweep reproduced. |
| M3.3 | Month 30 | Full pipeline benchmarked on Tiny-ViT and LLM tile maps; iso-accuracy design rules delivered to fabrication partner. |

---

## 4. Personnel

| Role | FTE | Responsibility |
|------|-----|----------------|
| PhD Student (continuing) | 1.0 | HIL integration (Aim 1); LLM extension (Aim 2); thesis completion (Month 36). |
| Postdoc — Analog Devices | 0.75 | Thermal/retention model development (Aim 3); wafer-level measurement campaigns; SPICE validation. |
| Collaborator — Chip Fabrication | 0.25 (in-kind) | Organic array tape-out; measured profile delivery; design-rule feedback. |
| PI / Advisor | 0.25 | Strategic direction; collaborator coordination; grant administration. |

---

## 5. Collaborators

- **Organic device fabrication:** [Placeholder — OECT/OPECT array process development, wafer map characterization, retention-time datasets.]
- **FPGA emulation & digital front-end:** [Placeholder — Xilinx/Alveo board loan, PCIe driver stack, DMA forward-pass integration.]
- **Foundry access & packaging:** [Placeholder — MPW shuttle for 130 nm or 65 nm CMOS back-end; monolithic integration of organic layer.]

---

## 6. Budget Tiers

| Tier | Amount | Scope |
|------|--------|-------|
| **Lean** | **$300K** | 1 PhD student (3 yr); GPU upgrade (2× A6000 Ada); travel ($6K/yr); cloud credits ($10K/yr). |
| **Moderate** | **$600K** | Above + 1 postdoc (2 yr); FPGA board (ZCU102 + mezzanine, ~$15K); expanded travel ($12K/yr); summer intern. |
| **Full** | **$1.2M** | Above + fabrication run costs (MPW + organic deposition, ~$350K); FPGA cluster (4× Alveo U55C, ~$80K); foundry liaison; 2 workshops. |

---

## 7. Risk Mitigation

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| **Aim 1 fails:** FPGA HIL does not reach ≥80 % recovery due to clock-domain noise or DRAM bandwidth limits. | Medium | **Fallback 1A:** Theory-only paper on memory-bandwidth lower bounds for analog HIL training. **Fallback 1B (Route R-C):** Replace FPGA with AWS F1 HLS instances, preserving analog-macro fidelity without hardware risk. |
| **Aim 2 fails:** LLM attention layers collapse under 4-bit quantization. | Low–Medium | Reduce scope to encoder-only models or 256-token contexts; pivot to "Attention Sensitivity Taxonomy for Analog CIM." |
| **Aim 3 fails:** Thermal model diverges >5 % from measured data. | Medium | Revert to lookup-table interpolation from measured wafer maps; publish dataset paper. |
| **Fabrication delay:** Wafer delivery slips beyond Month 24. | Medium | Maintain simulation-only trajectory using literature profiles; all M3 milestones achievable with synthetic profiles. |

---

## 8. Expected Outcomes

1. **Peer-reviewed papers:** 2 — (i) HIL training for organic CIM (conference, e.g., ISSCC/CICC or NeurIPS MLSys); (ii) LLM scaling and physical-realism pipeline (journal, e.g., *Nature Electronics* or *IEEE TCAS-I*).
2. **Open-source release:** compute_vit v2.0 — public repository with HIL FPGA kernels, thermal-retention co-simulation, LLM tiling scheduler, and reproducible 5-seed benchmarks (Zenodo deposit).
3. **Thesis completion:** 1 PhD dissertation defending the integrated program by Month 36.
4. **Secondary artifacts:** 1 design-rule brief delivered to the fabrication partner; 1 workshop/tutorial at a major EDA or ML conference.

---

*End of proposal outline.*
