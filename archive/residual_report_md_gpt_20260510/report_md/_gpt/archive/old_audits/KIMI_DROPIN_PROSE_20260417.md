# Drop-in Prose Blocks for Manuscript and Reviewer Response

**Date:** 2026-04-17
**Constraint:** Conservative, citation-aware, no invented methods, no fake certainty. These blocks are designed to survive hostile review.

---

## Block 1 — Introduction paragraph (simulator gap)

> Mature inorganic simulators have established effective workflows for benchmarking resistive CIM. DNN+NeuroSim connected device models to peripheral-circuit costs and network accuracy \citep{peng2020dnnneurosim}, MemTorch embedded memristive non-idealities into PyTorch for end-to-end evaluation \citep{lammie2022memtorch}, AIHWKIT exposed analog training and inference in a practical software stack \citep{rasch2021aihwkit}, and CrossSim provides GPU-accelerated crossbar simulation with parasitic resistance, ADC, drift, and lookup-table-based training models \citep{crosssim2026}. These frameworks remain anchored mainly to inorganic resistive memories; they do not natively capture the coupled photoresponse, retention, and write nonlinearity that define organic optoelectronic inference. A complementary simulator tailored to organic device profiles—and to the mixed-signal deployment of modern vision transformers—is therefore needed to bridge the materials-to-system gap.

*Where to paste:* Replace or extend the existing Introduction paragraph that currently covers the same simulators (around lines 11–13 of `01_introduction.tex`).

---

## Block 2 — Related-work paragraph (Ensemble HAT positioning)

> Hardware-aware training mitigates analog non-idealities by injecting device noise into the forward path during optimization \citep{joshi2020accurate}. Standard HAT keeps one fixed D2D realization throughout training, which we show causes the model to overfit a particular hardware instance \citep{rasch2021aihwkit}. Although related in spirit to quantization-aware training \citep{choi2019pact} and to domain randomization in sim-to-real transfer \citep{tobin2017domain}, HAT for CIM faces an additional difficulty: device-to-device mismatch is spatially structured and fixed per instance, unlike independent thermal noise or global rendering parameters. Ensemble HAT resamples the spatial mismatch map at each training epoch, improving zero-shot transfer to unseen arrays from chance level ($10.00\%$) to $86.37 \pm 1.54\%$.

*Where to paste:* `02_related_work.tex`, subsection "Hardware-Aware Training and Robustness" (currently lines 5–8).

---

## Block 3 — Contribution bullets (Nature-style, 3 bullets)

> **Three concrete contributions are made.**
> (1) A profile-driven first-order behavioral workflow for organic optoelectronic CIM that maps literature-derived device characteristics to task-level vision accuracy while retaining a common mixed-signal deployment model across CNN and ViT backbones.
> (2) Identification of the dominant deployment constraints in this regime: a two-stage ADC–D2D hierarchy quantified by Sobol analysis, together with a fresh-instance transfer failure mode showing that standard HAT overfits one fixed mismatch realization and that epoch-level resampling of spatial D2D maps mitigates this collapse.
> (3) Bounded system-level evidence for two frequently qualitative concerns: zero-shot transfer to a literature-anchored OPECT profile, and localization of the present $NL=2.0$ surrogate failure primarily to the MLP analog path rather than to the entire transformer.

*Where to paste:* End of Introduction (currently `01_introduction.tex` lines 19–23). This block can replace the existing contribution paragraph with only minor numerical adjustments.

---

## Block 4 — Response to reviewers: "Why no MI-HAT / SDR-HAT comparison?"

> We are not aware of a prior open-source baseline that implements exactly the same epoch-level resampling of full spatial D2D mismatch maps. The closest available analog-training toolkit, AIHWKIT, supports only i.i.d. noise injection, which our ablation shows is insufficient for fresh-instance transfer \citep{rasch2021aihwkit}. Variation-aware training methods in the literature (e.g., Zhu et al., DATE 2020; Liu et al., DAC 2015) model device variability statistically, but they typically sample parameters per weight or per layer rather than resampling complete spatial instance maps. The labels "MI-HAT" and "SDR-HAT" do not correspond to known citable methods in the analog-CIM literature. Because no external apples-to-apples baseline exists, we rely on internal controls—fixed-mask standard HAT, per-batch i.i.d. perturbation, and per-epoch structured D2D resampling—to isolate the causal contribution of the mismatch-map exposure schedule.

*Where to paste:* `REVIEWER_RESPONSE_DRAFT_gpt.md` or any point-by-point response addressing Major Comment #3 / innovation validation.

---

## Block 5 — Response to reviewers: "Simulation-only without fabricated-array validation"

> The study is intentionally behavioral and simulation-only. Array-level parasitics (IR drop, sneak paths), thermal effects, and pulse-faithful programming dynamics are not modeled explicitly; the energy parameters are analytical placeholders rather than measured circuit values. The framework is therefore presented as a materials-to-system decision aid for ranking deployment risks under plausible parameter ranges, not as a chip-predictive emulator for a specific fabricated array. Where possible, we anchor the device profiles to reported literature values and provide sensitivity sweeps (e.g., $\pm$50\% retention-parameter variation, 1--15\% D2D mismatch) to bound the conclusions. Measured organic-array data will be necessary to refine these bounds in future work.

*Where to paste:* `REVIEWER_RESPONSE_DRAFT_gpt.md` under questions about physical validation / experimental verification, or in the Discussion limitations section.

---

## Block 6 — Response to reviewers: "Why are the CrossSim / AIHWKIT shared-regime checks still meaningful?"

> The CrossSim and AIHWKIT comparisons are used only as shared-regime sanity checks to verify numerical consistency between the present simulator and mature inorganic toolkits under one matched configuration. Under matched 4-bit / noise assumptions on ResNet-18/CIFAR-10, the AIHWKIT baseline reaches $90.08 \pm 0.21\%$ versus our $86.57\%$, and the CrossSim clean baseline reaches $83.70\%$ versus our $86.20\%$ (1\,000-sample subset). These results confirm that our inference pipeline produces numerically reasonable outcomes in a regime where independent simulators are well validated. They do **not** claim physical validation for organic-specific behaviors (retention, photoresponse, nonlinear write), nor do they assert superiority over mature inorganic simulators on digital benchmarks. The comparisons are therefore methodological consistency checks, not competitive benchmarking claims.

*Where to paste:* `REVIEWER_RESPONSE_DRAFT_gpt.md` under any question about external simulator comparisons, or in the Discussion (`06_discussion.tex`) where CrossSim/AIHWKIT is mentioned.

---

*End of drop-in prose blocks.*
