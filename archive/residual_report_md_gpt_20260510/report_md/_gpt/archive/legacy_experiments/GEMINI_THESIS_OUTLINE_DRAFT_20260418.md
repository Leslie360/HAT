# GEMINI THESIS OUTLINE DRAFT — 2026-04-18

**Reread of canonical state:** I have re-read `THESIS_VS_PAPER_SCOPE_20260418.md` and confirmed the explicit 3-tier partitioning. The thesis is a superset of the NC paper (which is locked to 14 pages main + 21 pages supp). Thesis material aggressively integrates all supplementary ablations, extended datasets (SVHN, TinyImageNet), measured-device profile pipelines, code architecture, reproducibility plans, and future-work physical mappings (P1, P2, P5) that the NC paper compresses or leaves out.

## Chapter 1 — Introduction & Motivation
**Scope:** Introduces the physical scaling limits of digital edge-vision and the promise of organic optoelectronic compute-in-memory (CIM) arrays.
**NC Overlap:** Expands upon NC §1.
**Thesis-Only:** Deep discussion on why the thesis adopts a "behavioral-simulation first" framework instead of immediately fabricating a full array. Detailed motivation on the gap between materials-level characterization and system-level performance.

## Chapter 2 — Background & Related Work
**Scope:** A comprehensive literature review of organic optoelectronics, OECTs, OPECTs, and existing analog-AI simulators (AIHWKIT, CrossSim).
**NC Overlap:** Extends NC §2 (which is heavily space-constrained).
**Thesis-Only:** Exhaustive coverage of competing hardware-aware training (HAT) algorithms. Detailed comparative taxonomy of simulator feature-sets, justifying why existing tools like CrossSim are insufficient for organic-specific sublinear photoresponses.

## Chapter 3 — The compute_vit Framework
**Scope:** The full mathematical and software architecture of the `compute_vit` simulator.
**NC Overlap:** Incorporates NC §3 and the extended methods from the NC Supplementary (e.g., weight-to-conductance pipeline, analytical energy model, Sobol sensitivity).
**Thesis-Only:** Full framework architecture diagrams, API module designs, the profile JSON schema definition, and the automated fitting pipeline for measured-device raw data (the `数据_博士/` pipeline). Justification for the hybrid analog-digital mapping policy.

## Chapter 4 — Profile-Driven Edge Vision
**Scope:** Evaluates foundational models (Tiny-ViT) and CNNs (ResNet, ConvNeXt) under standardized analog deployments.
**NC Overlap:** Extracts the baseline, quantization, retention, and iso-accuracy contour map results from NC §5.
**Thesis-Only:** Exhaustive ablation data, expanded 5-seed statistical standardization results across all configurations, and cross-dataset robustness (including SVHN and Tiny-ImageNet evaluations from E2/E2b).

## Chapter 5 — Hardware-Aware Training & Noise Resilience
**Scope:** Focuses entirely on recovering from analog variation. Introduces Ensemble HAT and non-linear (NL) write mitigation.
**NC Overlap:** Contains the Ensemble HAT formulation and fresh-instance transferability from NC §5.
**Thesis-Only:** Extensive ablation on Ensemble HAT (spatial correlation, resampling frequency). A deep dive into the NL mitigation queue (MLP-only surrogate design vs. QKV collapse), detailing exactly how attention geometry breaks under severe asymmetric non-linearity.

## Chapter 6 — Toward Circuit-Aware Simulation
**Scope:** Elevates the physical models from isolated parameter proxies to interacting, spatially aware circuit approximations.
**NC Overlap:** None (NC relies on 1% placeholders for spatial phenomena).
**Thesis-Only:** Fully integrates spatial IR drop (P1), sneak-path currents (P2), thermal dependencies (P5), and the synergistic $\gamma \times \text{NL}$ interaction sweep (E6). Replaces the simple abstract model with a complex, co-optimized physical front-end.

## Chapter 7 — Reproducibility, Datasets, & Open-Source Release
**Scope:** Discusses the engineering rigor behind the research.
**NC Overlap:** None.
**Thesis-Only:** Details the reproducibility package (the 5-step plan from `REPRODUCIBILITY_PACKAGE_PLAN_20260418.md`), the checkpoint tiering strategy (A/B/C), unit-test coverage, and the decision boundary for open-sourcing the simulator vs. keeping measured-device raw data private.

## Chapter 8 — Conclusion & Future Work
**Scope:** Summarizes the thesis contributions and charts the next steps for organic CIM.
**NC Overlap:** Expands upon NC §7 and §6 Limitations.
**Thesis-Only:** Broader reflections on whether organic optoelectronics will successfully cross the "6-bit ADC cliff" in physical tape-outs, and future directions extending into pulse-level dynamic simulators.