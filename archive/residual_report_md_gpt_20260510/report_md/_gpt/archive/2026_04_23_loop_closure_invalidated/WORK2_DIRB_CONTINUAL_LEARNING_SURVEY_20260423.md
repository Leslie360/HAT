# Direction B Survey: Continual Learning / Incremental Learning on Organic CIM

**Date:** 2026-04-23
**Scope:** Literature sweep (2021–2026) for Master's thesis Work 2
**Relation to Work 1:** Work 1 studies inference-only simulation of organic optoelectronic CIM. Organic devices are rewritable (no hard filament breakdown typical of oxide RRAM), opening a path to on-device learning. Direction B asks whether this rewritability can support continual learning (CL) on the same physical array.

---

## 1. Motivation: Why Organic CIM for Continual Learning?

Continual learning (CL) requires a synaptic substrate that can be updated repeatedly without catastrophic loss of previous knowledge. Conventional oxide-RRAM-based CIM faces a fundamental tension:
- **Endurance limitation:** Filamentary RRAM wears out after 10⁶–10¹² cycles; aggressive on-chip training accelerates stuck-at-fault failures [[Mehonic 2023]](https://vlsijournal.com).
- **Asymmetric updates:** Non-linear, device-dependent potentiation/depression curves make gradient-based consolidation difficult [[Rasch 2024]](https://www.nature.com/articles/s41467-024-51221-z.pdf).

Organic optoelectronic synapses offer a qualitatively different trade-off:
- **Rewritable by design:** Switching relies on electrochemical doping, charge trapping, or photogating rather than filament formation/destruction, enabling gentler write-erase cycling [[Chen 2023]](http://www.ijemnet.com/article/pdf/preview/10.1088/2631-7990/ad9bff.pdf)[[Hwang 2025]](https://pubs.rsc.org/zh-tw/content/articlepdf/2025/tc/d5tc00997a).
- **Optical programmability:** Light can be used to modulate conductance non-destructively, offering an extra degree of freedom for weight consolidation (e.g., global "annealing" pulses to preserve important weights).
- **Bio-compatibility:** Organic devices naturally mimic synaptic metaplasticity (plasticity of plasticity), a biological mechanism thought to prevent forgetting [[D'Agostino 2023]](https://arxiv.org/abs/2306.12142).

If organic CIM can be shown to support CL with lower forgetting than digital baselines (or with lower energy/memory overhead), it becomes a unique hardware platform for edge AI that adapts to new tasks without cloud retraining.

---

## 2. SOTA Landscape

### 2.1 Continual Learning Algorithms (Software)
Three families dominate:
- **Regularization:** EWC (Kirkpatrick et al., 2017) penalizes changes to weights deemed important for past tasks via Fisher information. Scalable but assumes high-precision weight importance storage.
- **Replay:** iCaRL, GEM store exemplars or gradients in a buffer. Effective but memory-heavy—problematic for edge devices.
- **Architecture / Masking:** HAT, Progressive Networks allocate sub-networks per task. Task-identification at inference is required.

Recent surveys [[De Lange 2022]](https://ualberta.scholaris.ca/server/api/core/bitstreams/5189eddf-a288-4f8b-9216-0e311ec4a3f9/content)[[Mishra 2023]](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2023.1149410/pdf?isPublishedV2=false) emphasize that most CL work ignores hardware constraints.

### 2.2 Neuromorphic / Hardware CL
- **Metaplasticity on memristors:** D'Agostino et al. (2023) implemented synaptic metaplasticity on a 16 kbit HfO₂ crossbar (130 nm CMOS). A two-layer perceptron achieved 97% (MNIST) → 86% (Fashion-MNIST) sequential accuracy, matching software baselines and demonstrating immunity to catastrophic forgetting despite analog device imperfections. Multi-level memristor cells provided a **15× memory reduction** over binary networks.
- **Probabilistic metaplasticity:** Karia et al. (2024) proposed modulating the *probability* (not magnitude) of weight updates in low-precision memristor weights, eliminating auxiliary high-precision memory. Achieved **≈67% lower memory overhead** and **≈60× lower update energy** vs. auxiliary-memory solutions.
- **Edge continual training:** Liu et al. (2024, IEDM) demonstrated "Edge Continual Training and Inference with RRAM-Gain Cell Memory Integrated on Si CMOS," showing that RRAM can be updated in-situ for task-incremental scenarios at the edge.
- **On-chip few-shot learning:** Pallo et al. (2025, VLSI Symposium) validated few-shot on-chip training on a ReRAM CIM platform using MAML, achieving high accuracy after only **5 conductance-update iterations** on Omniglot.

### 2.3 Organic Synapse Cycling & Reliability
- **Endurance:** Organic memristors based on reduced GO or polymer composites typically show 10²–10⁴ switching cycles—orders of magnitude below oxide RRAM [[Duke thesis]](https://dukespace.lib.duke.edu/server/api/core/bitstreams/ad650796-0625-4065-a4c9-6f51c08f62d9/content). However, some printed organic devices maintained stable ON/OFF ratios (>10⁵) over 10⁴ cycles without degradation.
- **Electrical erasability:** Hwang et al. (2025) introduced metal-nanoparticle-engineered organic synaptic transistors achieving **30 distinct potentiation/depression states** with efficient electrical erase, overcoming the write-once-read-many limitation of conventional charge-trapping OSTs.
- **Photon modulation:** Chen et al. (2023, *Nature Photonics*) demonstrated an organic optoelectronic synapse based on photon-modulated electrochemical doping, enabling bidirectional conductance tuning with light. This suggests the possibility of **non-destructive, optically-mediated consolidation** (e.g., illuminating a subset of devices to freeze weights).

### 2.4 In-Memory Training on Resistive Arrays
- IBM Research demonstrated "Fast and robust analog in-memory deep neural network training" on PCM/RRAM arrays, co-optimizing device programming and algorithms to tolerate noise [[Rasch 2024]](https://www.nature.com/articles/s41467-024-51221-z.pdf).
- Tsinghua's fully integrated memristor chip (Science 2023) performed edge learning with sparsity and quantization, proving that real-world device variability need not preclude on-chip adaptation.

---

## 3. Research Gap

| Dimension | Existing Work | What's Missing |
|-----------|--------------|----------------|
| **Material** | Oxide RRAM / PCM dominates hardware CL demos | No experimental or simulation study of CL on *organic optoelectronic* CIM |
| **Algorithm–Device Co-Design** | Metaplasticity tested on HfO₂; probabilistic updates on generic memristors | No CL rule tailored to organic synapse physics (electrochemical doping, optical reset, large hysteresis) |
| **Endurance–Forgetting Trade-off** | Organic endurance is low, but CL algorithms assume near-infinite updates | No quantification of how *finite organic cycling budget* constrains task sequence length or learning rate |
| **Optical Degree of Freedom** | Optoelectronic synapses exist as standalone devices | No system-level proposal using *light* for weight consolidation (e.g., global EWC-style "freezing" via illumination patterns) |
| **Simulator** | CrossSim / AIHWKIT support inference + static training | No simulator models *task-incremental* updates with organic device cycling degradation |

**Core gap:** There is no prior work that combines continual learning algorithms with organic optoelectronic CIM arrays—either in experiment or in high-fidelity simulation. This is a blank space the thesis can fill.

---

## 4. Feasibility Assessment

| Factor | Assessment | Risk Level |
|--------|-----------|------------|
| **Simulation feasibility** | Work 1 already uses CrossSim + custom organic device models. Extending to CL requires adding weight-update non-idealities (cycling drift, retention) and a CL loss. **Doable within 3–4 months.** | Low |
| **Algorithmic maturity** | EWC, metaplasticity, and replay are well understood. Adapting them to analog noise has precedent (D'Agostino 2023). | Low |
| **Device model availability** | Organic optoelectronic models in CrossSim exist from Work 1, but cycling/aging models may need fitting from literature data. | Medium |
| **Experimental validation** | If the student has device access, a small 4×4 or 16×16 array could demonstrate 2-task CL. If not, simulation-only is acceptable for a Master's. | Medium |
| **Endurance ceiling** | Organic devices with ~10³–10⁴ cycles may limit sequence length. However, CL with EWC or replay requires fewer updates per task than full retraining. | Medium |

**Overall:** Direction B is **highly feasible** as a simulation-first contribution, with a possible small-scale experimental follow-up.

---

## 5. Preliminary Experiment Design

### 5.1 Simulation Track (Primary)
1. **Baseline:** Train a 2-layer MLP on MNIST → Fashion-MNIST sequentially using standard SGD in CrossSim with organic device models.
2. **CL baselines:** Implement EWC and tiny-exemplar replay on the same network.
3. **Organic-aware CL:** Design a metaplasticity rule where "importance" weights are stored via optical bias (simulated as a secondary programmable conductance) rather than digital auxiliary memory.
4. **Ablation:** Vary cycling endurance (10²–10⁵ cycles) and write noise to find the "forgetting vs. endurance" Pareto front.

### 5.2 Experimental Track (Stretch Goal)
1. Fabricate or access a small organic optoelectronic crossbar (from Work 1 collaborator).
2. Program Task A weights, measure accuracy.
3. Apply Task B updates with EWC-style constraints (e.g., limiting weight change via light-induced bias).
4. Report backward transfer (Task A accuracy after Task B).

### 5.3 Metrics
- Average accuracy over task sequence
- Backward transfer (forgetting measure)
- Energy per update (analog vs. digital reference)
- Effective endurance consumed per task

---

## 6. Key Citations

| # | Citation | Year | Venue | Key Finding / Relevance |
|---|----------|------|-------|------------------------|
| 1 | Mishra, R. & Suri, M. "A survey and perspective on neuromorphic continual learning systems." | 2023 | *Front. Neurosci.* | Identifies hardware considerations and gaps for NCL; roadmap for CL on neuromorphic substrates. |
| 2 | D'Agostino, S. et al. "Synaptic metaplasticity with multi-level memristive devices." | 2023 | arXiv / IEDM | First hardware demonstration of metaplasticity on HfO₂ crossbar; 97→86% sequential MNIST/F-MNIST. |
| 3 | Karia, V., Soures, N. & Kudithipudi, D. "Probabilistic metaplasticity for continual learning with memristors in spiking networks." | 2024 | arXiv | Modulates update *probability* instead of magnitude; 67% lower memory, 60× lower update energy. |
| 4 | Kirkpatrick, J. et al. "Overcoming catastrophic forgetting in neural networks." | 2017 | *PNAS* | EWC foundational paper; regularizes important weights via Fisher information. |
| 5 | Rasch, M. et al. "Fast and robust analog in-memory deep neural network training." | 2024 | *Nat. Commun.* | Co-design of device programming and training for RRAM/PCM arrays; tolerates analog noise. |
| 6 | Zhang, W. et al. "Edge learning using a fully integrated neuro-inspired memristor chip." | 2023 | *Science* | Full memristor chip for on-chip edge learning; shows viability of in-situ updates. |
| 7 | Liu, S. et al. "Edge continual training and inference with RRAM-Gain cell memory integrated on Si CMOS." | 2024 | *IEDM* | Demonstrates task-incremental training on RRAM at the edge. |
| 8 | Chen, K. et al. "Organic optoelectronic synapse based on photon-modulated electrochemical doping." | 2023 | *Nat. Photonics* | Organic synapse with bidirectional optical tuning; enables non-destructive weight modulation. |
| 9 | Hwang, Y. et al. "Electrically erasable multi-level charge trapping memory … for organic synaptic transistors." | 2025 | *J. Mater. Chem. C* | 30 distinct analog states with electrical erase; overcomes WORM limitation in organic OSTs. |
| 10 | De Lange, M. et al. "A continual learning survey: Defying forgetting in classification tasks." | 2022 | *IEEE TPAMI* | Comprehensive CL taxonomy and benchmarks; essential for metric and protocol selection. |
| 11 | Sebastian, A. et al. "Memory devices and applications for in-memory computing." | 2020 | *Nat. Nanotechnol.* | Foundational review of memristor requirements for CIM; endurance/retention targets. |
| 12 | Pallo, M. et al. "On chip customized learning on resistive memory technology for secure edge AI." | 2025 | *VLSI Symp.* | Few-shot on-chip training on ReRAM CIM with MAML; only 5 programming iterations needed. |
| 13 | Wen, T.-H. et al. "Fusion of memristor and digital compute-in-memory processing for energy-efficient edge computing." | 2024 | *Science* | Hybrid memristor+digital CIM chip; shows path for mixed-signal CL accelerators. |
| 14 | Lee, Y. et al. "Organic electronic synapses with low energy consumption." | 2021 | *Joule* | Reviews organic synapse operating principles and energy efficiency. |

---

## 7. Bottom Line

**Direction B is scientifically well-motivated and technically feasible.** The combination of organic rewritability and continual learning has not been explored in the literature. The student can leverage the existing CrossSim organic device pipeline from Work 1, add a CL algorithm layer (EWC or metaplasticity), and produce a novel simulation contribution quantifying how organic device endurance and optical programmability affect catastrophic forgetting. If device access is available, even a small 2-task demonstration would be a first.
