# Strategic Positioning v3 — Long-Horizon Field Forecast

**Date:** 2026-04-21
**Scope:** Analog CIM for edge vision, 2024–2028
**Audience:** Thesis committee, program officers, collaborators

---

## 1. 2024–2025: The Device-First Era

The present landscape is dominated by materials breakthroughs. Papers report organic optoelectronic synaptic transistors with multilevel states and 10⁴-cycle endurance, followed by a perceptron or shallow CNN on MNIST. The implicit assumption is that better devices automatically yield better systems.

**The gap:** No credible bridge links a measured LTP/LTD curve to Vision Transformer accuracy on CIFAR-100. Device engineers optimize conductance window; ML engineers optimize ImageNet top-1. The communities speak past each other because no simulation layer respects both organic photogating physics and attention dynamics. *We do not fix the device; we fix the interface.*

## 2. 2025–2026: The Simulation-First Era

This paper inaugurates the transition. compute-ViT shows that a literature-derived device profile—photoresponse nonlinearity, proportional noise, retention drift—can predict, *before tape-out*, whether a network survives on unseen hardware. The negative result matters as much as the positive: standard training reaches 75 % on a fixed noise map but collapses to 10 % on fresh instances, while epoch-level spatial resampling (Ensemble HAT) recovers 86.37 ± 1.54 %. The fabrication team learns what not to build.

**Our role is to establish simulation as a first-class citizen.** We trade SPICE fidelity for architectural throughput, claiming that this trade-off bounds deployment feasibility. We lead on fresh-instance protocols, organic-specific models, and attention sensitivity. We follow on absolute energy/area (NeuroSim, CrossSim) and transistor-level mismatch (TCAD).

## 3. 2026–2027: The Diagnostic Era

The field shifts from “does it work?” to “why does it fail?” First-order surrogates will hit a ceiling—our data suggest a structural bound near 30 % under severe nonlinearity (NL ≥ 2.0) that no training protocol currently breaks. Whether this is fundamental (softmax on power-law-distorted conductances) or artifactual (surrogate-order limitation) will define the next research wave.

**The agenda:** Higher-order polynomial conductance maps, layer-wise Jacobian spectra, and Fisher-information traces to isolate failure modes. If attention projections are the bottleneck, the community needs attention-free architectures—Mamba-style state-space or pooling-based hybrids. If spatial coupling dominates, we need correlated-D2D wafer maps and statistical field theories of mismatch. *We lead the diagnostic methodology and open-source falsification matrices; we follow the architecture community on analog-native backbone design.*

## 4. 2027–2028: The Co-Design Era

By 2028, analog CIM matures from materials novelty to systems technology. Device and ML engineers jointly optimize within a shared design envelope: the device team adjusts photoresponse gamma knowing, in real time, how each parameter moves the iso-accuracy contour in (ADC precision, nonlinearity, temperature) space. The enabling simulation framework becomes a standard design tool.

**Our role:** Deliver the deployment envelope as an open-source standard—analogous to Cacti or Darknet—where a foundry inputs a measured profile and receives a predicted accuracy curve, recommended ADC bit-width, and a flag list of layers that must stay digital. We will not build the PDK or tape out the chip. *We build the language that lets device and algorithm teams negotiate.*

## 5. Our Role in Each Era

| Era | What we do | What we do not do | Posture |
|:---|:---|:---|:---|
| **Device-first** | Translate profiles into accuracy predictions; expose the device-to-system gap. | Build better transistors; compete on endurance. | **Lead** the interface. |
| **Simulation-first** | Establish fresh-instance evaluation, organic surrogates, attention sensitivity. | Claim SPICE fidelity; claim energy-area superiority. | **Lead** the protocol; **follow** on physical fidelity. |
| **Diagnostic** | Falsify mitigations; publish structural-limit theory; release higher-order surrogates. | Invent analog-native attention from scratch; fabricate test chips. | **Lead** methodology; **follow** on architectures and HIL. |
| **Co-design** | Deliver the deployment envelope as a community standard. | Build a commercial EDA tool; run a foundry. | **Lead** the standard; **follow** on industrial integration. |

**Honest uncertainties.** The 30 % structural-limit hypothesis is heuristic, not proven; higher-order surrogates may break or confirm it. Real organic variability may exceed literature profiles, rendering our predictions optimistic. The architecture community may solve analog-ViT robustness before we finish diagnosing it. We proceed anyway, because building devices without system feedback is empirically more expensive.

---

*End of forecast.*
