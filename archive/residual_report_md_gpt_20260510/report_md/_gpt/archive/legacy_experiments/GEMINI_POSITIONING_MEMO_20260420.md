# Strategic Positioning Memo — compute-ViT in the Analog-CIM Landscape

**Date:** 2026-04-20
**Word count:** ~780
**Audience:** Thesis defense committee + Nature Communications revision reviewers

---

## 1. Incumbent Landscape (One Sentence Each)

- **CrossSim (SANDIA):** GPU-accelerated crossbar-accuracy simulator with parasitic resistance, ADC drift, and lookup-table training models; built for inorganic RRAM/PCM and does not expose organic photoresponse or epoch-level spatial D2D resampling.
- **IBM AIHWKIT:** Industrial-grade mixed-signal analog-training stack with per-batch i.i.d. noise injection and practical inference simulation; lacks structured spatial mismatch maps and fresh-instance transfer validation.
- **DeepCompute / NeuroSim family:** Device-to-system energy/area/delay estimator with calibrated circuit macros; accuracy is an output of a hierarchical spreadsheet, not an end-to-end trainable PyTorch layer.
- **MemTorch:** PyTorch-integrated memristive non-ideality wrapper for end-to-end evaluation; targets oxide memristors and does not parameterize organic optoelectronic conductance states or retention.
- **Qin et al. / generic device-model frameworks:** Provide closed-loop programming-error models and variation-aware training; scope is typically limited to single-layer perceptrons or MLPs on MNIST, not modern vision transformers at CIFAR/Flowers scale.

---

## 2. Gap Analysis: What Everyone Else Misses

- **ViT-specific attention-projection sensitivity:** No incumbent jointly models analog non-idealities *inside* the QKV/output projection paths of a Vision Transformer; they treat transformers as generic MLPs or stop at ResNet-scale CNNs.
- **Fresh-instance evaluation protocol:** Existing frameworks validate on a single fixed noise realization or i.i.d. resampling; none report accuracy on *unseen spatial D2D mismatch maps* drawn from a fabrication distribution, which is the actual deployment condition for crossbar arrays.
- **Organic-device parameterization:** Organic optoelectronic synaptic transistors (OPECT) have distinct physics—inverse-gamma photoresponse, double-exponential retention drift, state-dependent proportional noise—that inorganic simulators treat as out-of-scope.
- **Literature-to-accuracy bridge:** Incumbents require measured wafer data or PDK decks to run; compute-ViT accepts a JSON literature profile and returns an accuracy prediction without code changes, closing the loop for materials papers that lack system co-design.

---

## 3. The "Only X" Claim

> **The only open-source framework that trains Vision Transformers on device-parameterized organic analog arrays with a validated fresh-instance evaluation protocol.**

- "Only" is defensible because no public toolkit combines (a) PyTorch-native end-to-end training of Tiny-ViT/ConvNeXt, (b) organic-specific non-idealities (photoresponse + retention + proportional noise), and (c) epoch-level spatial D2D resampling with zero-shot transfer to 10 unseen hardware instances.
- Do not overclaim: we are a *behavioral* simulator, not a SPICE-level circuit solver; the "only" applies to the algorithm–device bridge, not to absolute physical fidelity.

---

## 4. Weaknesses We Must Acknowledge

- **No SPICE co-simulation:** We model array behavior at the conductance/Ohm's-law level; transient sneak-path currents, wire parasitics, and sense-amplifier offsets are abstracted into static noise terms.
- **No foundry PDK integration:** There is no GDSII tape-out path, no DRC/LVS, and no standard-cell library; the framework stops at the algorithm–accuracy boundary.
- **Silicon validation pending:** The Zhang 2025 OPECT bridge (88.53%) is a *literature-derived* calibration, not a measured-device closure; measured data from the doctoral line is still en route.
- **Limited architecture scope:** Only linear/dense operators are mapped to analog; depthwise convolutions, softmax, and LayerNorm remain digital by policy, which caps the analog acceleration fraction.
- **CrossSim comparison gap:** CrossSim underestimates our accuracy by 14.4 pp at standard noise, but we have not fully root-caused the discrepancy (likely due to differing D2D semantics); we therefore treat CrossSim as a directional cross-check, not a ground-truth oracle.

---

## 5. Positioning for NC Revision: "Why Not Just Use CrossSim?"

CrossSim is an excellent inorganic-RRAM simulator, but its noise model is parameterized through generic `programming_error` and `read_noise` scalars that collapse accuracy by 14 pp relative to our framework under the same nominal σ_C2C/σ_D2D, and it offers no organic photoresponse or retention primitives. For organic optoelectronic arrays, the relevant question is not "which simulator is faster?" but "which simulator can ingest an OPECT literature profile and predict whether attention-projections will survive the analog ceiling at 6-bit ADC?" Only compute-ViT does the latter.

---

## 6. Positioning for Thesis Defense: The 10-Year Arc

- **2015–2019 (Device era):** Organic memristors and OPECTs were demonstrated as individual synaptic devices with LTP/LTD curves; system impact was speculative.
- **2020–2023 (Simulator era):** NeuroSim, AIHWKIT, and CrossSim connected inorganic devices to network accuracy, but organic materials were excluded because their physics (photogating, ionic retention, flexible-substrate variability) did not fit the RRAM template.
- **2024–2026 (Architecture-aware era):** ViTs entered the edge-computing conversation, yet analog-CIM studies still evaluated them with CNN-centric noise assumptions or ignored attention-specific sensitivity entirely.
- **This work (Bridging era):** We show that the bottleneck is not the device alone, nor the algorithm alone, but the *interface*: how attention-projections respond to spatially structured organic mismatch, and how training must resample that structure epoch-by-epoch to avoid instance overfitting. The thesis contribution is the methodology for closing that interface—not a better transistor, but a better bridge between transistor literature and transformer deployment.

---

*End of memo.*
