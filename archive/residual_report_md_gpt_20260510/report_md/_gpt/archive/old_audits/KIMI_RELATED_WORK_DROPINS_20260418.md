# Related-Work Drop-In Paragraphs — 2026-04-18

**Style:** Publication-ready, conservative, citation-aware. No invented methods.

---

## 1. Intro Simulator Paragraph (Replacement for current §1 Paragraph 3)

**Target location:** `sections/01_introduction.tex`, paragraph following HAT discussion.

**Current text:**
> System-level CIM simulators for inorganic memories---DNN+NeuroSim [peng2020dnnneurosim], MemTorch [lammie2022memtorch], AIHWKIT [rasch2021aihwkit], and CrossSim [crosssim2026]---do not directly capture the coupled photoresponse, retention, and write nonlinearity that define organic optoelectronic inference.

**Status:** Already compressed and accurate. No drop-in needed unless user wants expansion. If expansion is desired:

> System-level CIM simulators established effective workflows for inorganic resistive memories. DNN+NeuroSim connected hierarchical device models to peripheral-circuit costs and network accuracy [peng2020dnnneurosim]; MemTorch embedded memristive non-idealities into PyTorch for end-to-end evaluation [lammie2022memtorch]; AIHWKIT exposed analog HAT and inference simulation in a practical mixed-signal stack [rasch2021aihwkit]; and CrossSim provides a GPU-accelerated crossbar-accuracy workflow with parasitic resistance, ADC, drift, and lookup-table-based training [crosssim2026]. These frameworks remain anchored mainly to inorganic resistive memories, and they do not directly capture the coupled photoresponse, retention, and write nonlinearity that define organic optoelectronic inference.

---

## 2. Related-Work HAT Paragraph (Replacement for §2.1 opening)

**Target location:** `sections/02_related_work.tex`, §2.1 first paragraph.

**Current text:**
> Hardware-aware training (HAT) mitigates analog non-idealities by injecting hardware perturbations into the forward path during optimization [joshi2020accurate]. Although related in spirit to quantization-aware training [choi2019pact] and to domain randomization in sim-to-real transfer [tobin2017domain], HAT for CIM faces an additional difficulty: device-to-device (D2D) mismatch is spatially structured and fixed for a given hardware instance. It is therefore different from independent thermal or sampling noise. Standard HAT usually keeps one random D2D mask fixed throughout training. Section 5.4 shows that this choice causes the model to fit a particular hardware instance rather than the deployment distribution. Ensemble HAT resamples the static D2D mask at each training epoch, improving zero-shot transfer to fresh hardware instances.

**Status:** Already reviewer-safe. The paragraph correctly:
- Credits Joshi et al. for PCM HAT precedent.
- Draws conceptual analogy to QAT and domain randomization without conflating them.
- States the D2D-specific difficulty clearly.
- Introduces Ensemble HAT as our response.

**No replacement needed.**

---

## 3. Related-Work Organic-Array Paragraph (Replacement for §2.2)

**Target location:** `sections/02_related_work.tex`, §2.2.

**Current text:**
> Organic synaptic and memristive devices have been widely explored as flexible, low-power candidates for neuromorphic hardware... [paragraph continues]

**Proposed tightening (more compact, same citations):**

> Organic synaptic and memristive devices offer optical sensitivity, multilevel conductance tuning, and flexible-substrate compatibility for neuromorphic hardware [xu2025emerging,photonics2025organicreview]. Recent demonstrations include multilevel memory [guo2024organic,jung2024organicfilaments], long retention tails [zeng2023organicmemristor], and integrated optoelectronic arrays [gebregiorgis2023organiccim,zhang2026opect,zhang2025mooptoelectronic,cui2025multimode]. Array-level studies are beginning to treat active-matrix addressing, spatial optical response, and crosstalk as system constraints rather than purely materials observations [visionarch2023crosstalk,amspa2024insensor,jang2023insensor]. Nevertheless, most network demonstrations remain device-centric or limited to small benchmarks; variability and transfer across fabricated instances are rarely evaluated quantitatively at the task level [alibart2016physical].

**Value:** Removes the redundant "Taken together, this literature provides plausible ranges..." sentence (already said in Introduction), tightening by ~2 lines.

---

## 4. Hybrid-Mapping / ViT Paragraph (Replacement for §2.3 closing)

**Target location:** `sections/02_related_work.tex`, §2.3 last paragraph.

**Current text:**
> Unlike prior ViT-on-PIM studies, we explicitly model photoresponse, profile substitution, and joint variability, retention, ADC resolution, and front-end distortion within one workflow. This focus is also consistent with recent low-bit ViT quantization studies, which repeatedly identify attention logits, softmax-adjacent computations, and activation scaling as especially sensitive under aggressive precision reduction [liu2021ptqvit,li2022qvit,lin2023vitptq]. Post-training quantization studies likewise note that attention remains difficult below 6 bits unless specialized approximations are introduced [lin2023vitptq]. By extending established simulator practice to organic optoelectronic domains, we aim to provide a deployment-facing framework that links reported device characteristics to CIFAR-scale transformer benchmarks.

**Status:** Already strong. Minor polish:

> Unlike prior ViT-on-PIM studies, we jointly model photoresponse, profile substitution, variability, retention, ADC resolution, and front-end distortion within one workflow. This focus converges with low-bit ViT quantization findings that attention-adjacent computations remain especially sensitive below 6 bits [liu2021ptqvit,li2022qvit,lin2023vitptq]. Extending established simulator practice to organic optoelectronic domains, the present framework links reported device characteristics to CIFAR-scale transformer benchmarks through a replaceable profile interface.

**Value:** Tighter; removes redundant "Post-training quantization studies likewise note..." sentence.

---

## 5. Discussion Sentence on CrossSim / AIHWKIT Complementarity

**Target location:** `sections/06_discussion.tex`, §Outlook (or new sentence in Limitations).

**Drop-in:**

> A preliminary cross-framework comparison against CrossSim shows consistent baseline inference under clean conditions (86.2\% ours vs.\ 83.7\% CrossSim on a 1\,000-sample subset at 8-bit ADC), but the accuracy gap widens substantially under noise injection (81.6\% vs.\ 67.2\% at $\sigma=5\%$), highlighting the sensitivity of accuracy predictions to the specific noise-to-conductance mapping. Because the two toolchains use different internal approximations for mapping device assumptions to effective conductances, this discrepancy should be read as a joint-calibration problem rather than as evidence that one simulator is categorically correct.

**Status:** Already present in §Outlook. No change needed.

---

## Summary of Recommended Edits

| § | Action | Effort | Priority |
|---|--------|--------|----------|
| §2.2 Organic devices | Replace with tightened paragraph | 1-line swap | Medium |
| §2.3 Closing | Replace with tighter version | 3-line swap | Medium |
| §1 Simulator | Keep current compressed form | None | — |
| §2.1 HAT | Keep current | None | — |
| §6 Outlook CrossSim | Keep current | None | — |
