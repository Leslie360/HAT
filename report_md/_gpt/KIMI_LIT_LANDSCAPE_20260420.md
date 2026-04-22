# Literature Landscape Review — Organic Optoelectronic CIM for Vision Transformers

**Date:** 2026-04-20  
**Scope:** 2023–2026 high-impact papers in organic neuromorphic devices, CIM-ViT accelerators, noise-aware training, and adjacent edge-AI topics.  
**Manuscript:** `compute_vit/paper/latex_gpt/` (Introduction + Related Work analyzed).  
**Existing ref count:** ~35 active citations in `refs_gpt.bib`.

---

## 1. Executive Summary

The manuscript sits at the intersection of **organic optoelectronic devices**, **compute-in-memory (CIM) simulation**, and **hardware-aware training (HAT) for Vision Transformers**. After surveying 2023–2026 literature in Nature/Science family, IEDM/ISSCC, and top ML venues, four high-value gaps emerge:

1. **Missing top-journal organic-neuron papers.** The manuscript cites organic *synapses* (Guo 2024, Xu 2025, Zhang 2025 OPECT) but omits 2024–2025 *Nature Electronics* / *Nature Communications* work on organic electrochemical *neurons* and integrated wearable OECT platforms that would strengthen the "device-to-system" motivation.
2. **No 2024–2025 IEDM/ISSCC CIM-ViT tapeouts cited.** The related-work discussion of hybrid CIM mapping (Sec. 2.3) cites Hemlet (arXiv 2025) and HARDSEA (ASP-DAC 2024) but lacks recent IEDM chips that explicitly demonstrate RRAM/FeFET transfer learning on ViT backbones—exactly the benchmark regime of this work.
3. **Under-cited adjacent training-robustness literature.** The Ensemble HAT idea (Sec. 2.1) is novel, but the manuscript does not position it against the 2024–2025 explosion of "analog foundation model" and hardware-aware quantization work for memristive inference.
4. **Missing a unifying survey anchor.** A recent `Nature` / `Nature Electronics` perspective on the memristor industry or neuromorphic intermediate representation would provide a strong upstream citation for the introduction.

---

## 2. Papers by Thematic Area

### (a) Organic RRAM / Organic Optoelectronic Device Physics

| # | Citation Key Suggestion | Paper | 1-Sentence Relevance | Verdict | Section to Strengthen |
|---|------------------------|-------|----------------------|---------|----------------------|
| 1 | `liu2024wearable` | D. Liu *et al.*, "A wearable in-sensor computing platform based on stretchable organic electrochemical transistors," **Nature Electronics**, 7, 1176–1185, 2024. | First integrated wearable OECT array with >50 % stretchability and coin-sized readout, demonstrating that organic optoelectronic edge inference is leaving the bench. | **CITE** | Intro, Sec 2.2 (organic devices) |
| 2 | `beller2024organicneurons` | P. Beller *et al.*, "Unravelling the Operation of Organic Artificial Neurons for Neuromorphic Bioelectronics," **Nature Communications**, 15, 5350, 2024. | Systematic physical analysis of organic artificial neuron operation, bridging the device-physics gap that the manuscript flags as under-explored. | **CITE** | Sec 2.2 |
| 3 | `ji2025singleoectneuron` | J. Ji *et al.*, "Single-transistor organic electrochemical neurons," **Nature Communications**, 16, 4334, 2025. | Demonstrates a single-OECT neuron comparable in size to biological neurons; directly supports the manuscript’s claim that organic devices are approaching deployment-relevant density. | **CITE** | Intro, Sec 2.2 |
| 4 | `harikesh2025singleoeneuron` | P. C. Harikesh *et al.*, "Single organic electrochemical neuron capable of anticoincidence detection," **Science Advances**, 11, eadv3194, 2025. | Extends organic neurons to nonlinear XOR-classification tasks, reinforcing the argument that organic hardware can support expressive network backbones. | **CONSIDER** | Sec 2.2 (optional) |
| 5 | `harikesh2024oeneurons` | P. C. Harikesh *et al.*, "Organic electrochemical neurons for neuromorphic perception," **Nature Electronics**, 7, 525–536, 2024. | Invited perspective explicitly calling for system-level benchmarking of organic neuromorphic hardware—mirrors the manuscript’s stated motivation. | **CITE** | Intro |
| 6 | `zhou2025biomimetic` | Q. Zhou *et al.*, "Biomimetic fibrous semiconducting micromesh via tuning phase separation for high-performance stretchable optoelectronic synapses," **Nature Communications**, 16, 2025. | High-performance stretchable optoelectronic synapse with fibrous architecture; adds to the photoresponse/retention parameter landscape the manuscript profiles. | **CONSIDER** | Sec 2.2 |
| 7 | `yan2024lateral` | C. Yan *et al.*, "Lateral intercalation-assisted ionic transport towards high-performance organic electrochemical transistor," **Nature Communications**, 15, 10118, 2024. | Reports high-performance OECTs with engineered ionic transport; provides updated conductance-window and switching-energy benchmarks. | **THESIS_ONLY** | — |
| 8 | `laswick2024antiambipolar` | Z. Laswick *et al.*, "Tunable anti-ambipolar vertical bilayer organic electrochemical transistor enable neuromorphic retinal pathway," **Nature Communications**, 15, 6309, 2024. | Biorealistic retinal-pathway emulation with anti-ambipolar OECTs; adjacent to the manuscript’s optoelectronic front-end theme but more biomorphic than CIM-oriented. | **CONSIDER** | Sec 2.2 (if space) |
| 9 | `aguirre2024hardwareann` | F. Aguirre *et al.*, "Hardware implementation of memristor-based artificial neural networks," **Nature Communications**, 15, 1974, 2024. | Large-scale experimental memristor ANN demonstration in a top journal; useful as a comparator to show that organic CIM is still behind inorganic array scale. | **CITE** | Intro (gap framing) |
| 10 | `lanza2025memristor` | M. Lanza *et al.*, "The growing memristor industry," **Nature**, 640, 613–622, 2025. | High-profile survey arguing memristive technologies are entering commercial viability; provides industry context that makes organic-specific simulation work timely. | **CITE** | Intro |

#### Gap Analysis — Organic Devices
The manuscript already cites Guo 2024, Xu 2025, Zhang 2025 OPECT, Cui 2025, and Fuller 2020. What is *missing* is the **organic neuron** side of the synapse+neuron stack and the **wearable/system-integration** narrative. Liu 2024 (*Nature Electronics*) and Harikesh 2024 (*Nature Electronics* perspective) are the two most glaring omissions: a reviewer familiar with the 2024 organic-neuromorphic landscape would expect at least one of them.

---

### (b) Analog CIM for Vision Transformers / Transformers

| # | Citation Key Suggestion | Paper | 1-Sentence Relevance | Verdict | Section to Strengthen |
|---|------------------------|-------|----------------------|---------|----------------------|
| 11 | `ando2025transfer` | T. Ando *et al.*, "Transfer Learning on Edge Using 14nm CMOS-compatible ReRAM Array and Analog In-memory Training Algorithm," **IEDM**, 2024 (invited; extended 2025). | IBM-led 14 nm ReRAM AIMC chip demonstrating Tiki-Taka training and ViT-based transfer learning from CIFAR-10 to CIFAR-100; directly overlaps the manuscript’s task regime and hybrid analog–digital claim. | **CITE** | Sec 2.3 (CIM frameworks) |
| 12 | `qiu2025m3dattention` | R. Qiu *et al.*, "Monolithic 3D Integration of MoS2 eDRAM and RRAM for Analog In-Memory Attention Computing," **IEDM**, 2025. | Experimental monolithic 3D chip accelerating Transformer attention with TaOx RRAM + MoS2 eDRAM; 500× speed-up over GPU. Sets the hardware bar the manuscript’s simulation targets. | **CITE** | Intro, Sec 2.3 |
| 13 | `yan2025learningaware` | L. Yan *et al.*, "An 8Mb Learning-Aware RRAM Compute-in-Memory Accelerator for Embodied Self-Supervised Learning," **IEDM**, 2025. | PKU 40 nm 8 Mb RRAM CIM chip with lifetime-aware programming; demonstrates that RRAM CIM is now at the embodied-AI edge, reinforcing the manuscript’s focus on edge vision. | **CITE** | Intro |
| 14 | `mia2026trilinear` | M. Z. A. Mia *et al.*, "Trilinear Compute-in-Memory Architecture for Energy-Efficient Transformer Acceleration," arXiv:2604.07628, 2026 (ASPLOS-track). | DG-FeFET-based trilinear CIM that executes full attention in-memory without NVM reprogramming; the most architecturally ambitious recent CIM-Transformer proposal. | **CITE** | Sec 2.3 |
| 15 | `shi2025fe-gc` | M. Shi *et al.*, "Monolithic 3D Integrated HZO-based 2TnF Ferroelectric Gain Cell for Parallel Read CIM Accelerating Attention," **IEDM**, 2025. | Tsinghua Fe-GC with quasi-destructive read for KV-cache; 13× improvement over planar DRAM. Complements the manuscript’s discussion of ADC-resolution bottlenecks. | **CONSIDER** | Sec 2.3 |
| 16 | `wang2025micsim` | C. Wang *et al.*, "MICSim: A Modular Simulator for Mixed-Signal Compute-in-Memory based AI Accelerator," **ASPDAC**, 2025. | Modular simulator used in Hemlet for heterogeneous CIM evaluation; provides a simulator-comparison point alongside DNN+NeuroSim and CrossSim. | **CONSIDER** | Sec 2.3 |
| 17 | `tu2025tensorcim` | F. Tu *et al.*, "TensorCIM: A 28nm 3.7 nJ/Gather and 8.3 TFLOPS/W FP32 Digital-CIM Tensor Processor," **ISSCC**, 2023; **JSSC**, 60(2), 734–747, 2025. | Digital-CIM tensor processor for beyond-NN acceleration; cited in Hemlet but not in the manuscript. Useful to distinguish analog-CIM (manuscript focus) from digital-CIM alternatives. | **THESIS_ONLY** | — |
| 18 | `attar2025rram` | Attar team, "Attar: RRAM-based in-memory attention accelerator with software-hardware co-optimization," **Science China Information Sciences**, 2025. | RRAM attention accelerator with SW-HW co-optimization for Transformer; fills the gap between Bettayeb 2024 (memristor attention) and Hemlet/HARDSEA. | **CONSIDER** | Sec 2.3 |

#### Gap Analysis — CIM-ViT
The manuscript’s Sec 2.3 currently cites Hemlet (arXiv 2025), HARDSEA (ASP-DAC 2024), Bettayeb 2024, and the quantization trio (Liu 2021, Li 2022, Lin 2023). The **biggest omission** is the absence of any **IEDM/ISSCC tapeout** from 2024–2025 that explicitly maps ViT or transfer learning to RRAM/FeFET silicon. Ando 2024/2025 (IBM) is the most directly comparable because it tackles ViT-based transfer learning on real ReRAM hardware—precisely the regime the manuscript simulates. Qiu 2025 (IEDM) and Yan 2025 (IEDM) provide additional silicon evidence that CIM-Transformer is no longer purely architectural speculation.

---

### (c) Noise-Aware / Hardware-Aware Training Surveys & Methods

| # | Citation Key Suggestion | Paper | 1-Sentence Relevance | Verdict | Section to Strengthen |
|---|------------------------|-------|----------------------|---------|----------------------|
| 19 | `analogfm2025` | "Analog Foundation Models," arXiv:2505.09663, 2025 (NeurIPS-track). | First systematic effort to make LLMs robust to AIMC noise via hardware-aware training with per-channel Gaussian noise injection; directly analogous to the manuscript’s Ensemble HAT but at LLM scale. | **CITE** | Sec 2.1 (HAT & robustness) |
| 20 | `diware2024hwq` | S. Diware *et al.*, "Hardware-Aware Quantization for Accurate Memristor-Based Neural Networks," **ICCAD**, 2024. | Aligns conductance-variation errors to lower-order output bits via bit-precision tuning; a complementary quantization-centric view to the manuscript’s noise-injection HAT. | **CONSIDER** | Sec 2.1 |
| 21 | `nagal2025qatsurvey` | Nagel *et al.* / collective, "Quantization-Aware Training: A Comprehensive Survey," **OpenReview**, 2025. | Comprehensive QAT survey (2020–2025) covering ViT-specific quantization; useful as a survey anchor for the low-bit ViT paragraph in Sec 2.3. | **CONSIDER** | Sec 2.3 |
| 22 | `joshi2020accurate` | V. Joshi *et al.*, "Accurate Deep Neural Network Inference Using Computational Phase-Change Memory," **Nature Communications**, 11, 2473, 2020. | **Already cited** in the manuscript; remains the canonical HAT-for-CIM reference. No action needed. | — | — |

#### Gap Analysis — HAT
The manuscript’s Sec 2.1 does a good job distinguishing standard HAT (fixed D2D mask) from Ensemble HAT (epoch-resampling). However, it does not cite any **2024–2025 follow-up work** on analog robustness training. The *Analog Foundation Models* paper (2025) is the clearest missing piece: it trains billion-parameter models with AIMC noise injection, showing that the community has moved beyond small-perceptron HAT. Citing it would frame Ensemble HAT as part of a broader trend while highlighting its unique contribution (structured spatial-instance resampling rather than i.i.d. weight noise).

---

### (d) Nature / Science Family — Adjacent Scope (Edge AI, Neuromorphic, Organic Computing)

| # | Citation Key Suggestion | Paper | 1-Sentence Relevance | Verdict | Section to Strengthen |
|---|------------------------|-------|----------------------|---------|----------------------|
| 23 | `pedersen2024nir` | J. E. Pedersen *et al.*, "Neuromorphic intermediate representation: A unified instruction set for interoperable brain-inspired computing," **Nature Communications**, 15, 8122, 2024. | Proposes a hardware-agnostic neuromorphic IR; supports the manuscript’s argument that organic CIM needs profile-driven, simulator-interoperable evaluation frameworks. | **CITE** | Intro |
| 24 | `sun2024memchip` | B. Sun *et al.*, "Memristor-based artificial chips," **ACS Nano**, 18(1), 14–27, 2024. | High-impact review on memristor chip integration; useful upstream citation for the CIM-acceleration paragraph in the introduction. | **THESIS_ONLY** | — |
| 25 | `choi20252dneuro` | Y. Choi *et al.*, "Advanced AI computing enabled by 2D material-based neuromorphic devices," **npj Unconventional Computing**, 2, 8, 2025. | 2D-material neuromorphic survey in Nature family; adjacent to organic electronics but distinct technology stack. | **THESIS_ONLY** | — |
| 26 | `xiao2024neurochip` | Y. Xiao *et al.*, "Recent Progress in Neuromorphic Computing from Memristive Devices to Neuromorphic Chips," **Adv. Devices & Instrum.**, 0044, 2024. | Broad survey covering device-to-chip pipeline; good for thesis background, less urgent for this manuscript. | **THESIS_ONLY** | — |
| 27 | `bellec2020eprop` | G. Bellec *et al.*, "A solution to the learning dilemma for recurrent networks of spiking neurons: e-prop," **Nature Communications**, 11, 3625, 2020. | Landmark local-learning rule for spiking networks; only relevant if the manuscript wishes to discuss on-chip learning alternatives to backprop-HAT. | **IRRELEVANT** | — |
| 28 | `cui2025multimode` | D. Cui *et al.*, "Fully integrated multi-mode optoelectronic memristor array for diversified in-sensor computing," **Nature Nanotechnology**, 2025. | **Already cited**; no action needed. | — | — |

---

## 3. High-Priority Action List (Reviewer-Visible)

These are the papers most likely to be flagged by a reviewer as "obvious missing citations."

### Must-Add Before Submission (CITE verdict)

1. **`liu2024wearable`** — *Nature Electronics* wearable OECT platform. Strengthens the introduction’s claim that organic optoelectronics are becoming deployment-relevant. Add to Intro paragraph 1 or Sec 2.2.
2. **`harikesh2024oeneurons`** — *Nature Electronics* perspective on organic neurons for neuromorphic perception. Explicitly calls for system-level benchmarking; perfectly aligns with the manuscript’s motivation. Add to Intro.
3. **`beller2024organicneurons`** — *Nature Communications* organic-neuron physics. Supports the device-physics gap argument in Sec 2.2.
4. **`ji2025singleoectneuron`** — *Nature Communications* single-transistor organic neuron. Shows device scaling; add to Sec 2.2.
5. **`ando2025transfer`** — IBM IEDM ReRAM AIMC with ViT transfer learning. The closest silicon precedent to the manuscript’s simulated task regime. Essential for Sec 2.3.
6. **`qiu2025m3dattention`** — IEDM monolithic 3D attention accelerator. Demonstrates that Transformer-CIM is now at the tapeout level; add to Intro/Sec 2.3.
7. **`yan2025learningaware`** — IEDM 8 Mb RRAM embodied-SSL chip. Reinforces edge-AI relevance; add to Intro.
8. **`mia2026trilinear`** — DG-FeFET trilinear CIM for full attention-in-memory. The most architecturally advanced recent CIM-Transformer work; add to Sec 2.3.
9. **`analogfm2025`** — Analog Foundation Models. Positions Ensemble HAT within the 2025 landscape of noise-aware training at scale; add to Sec 2.1.
10. **`lanza2025memristor`** — *Nature* perspective on memristor industry growth. High-impact upstream citation for the introduction’s CIM motivation.
11. **`aguirre2024hardwareann`** — *Nature Communications* large-scale memristor ANN. Provides inorganic comparator for the organic gap analysis.
12. **`pedersen2024nir`** — *Nature Communications* neuromorphic IR. Supports the framework/profile-driven methodology narrative.

### Consider if Space Permits (CONSIDER verdict)

- `harikesh2025singleoeneuron` (Science Advances) — organic neuron XOR.
- `zhou2025biomimetic` (Nature Communications) — stretchable optoelectronic synapse.
- `laswick2024antiambipolar` (Nature Communications) — retinal-pathway OECT.
- `shi2025fe-gc` (IEDM) — Fe-GC KV-cache.
- `wang2025micsim` (ASPDAC) — modular CIM simulator.
- `attar2025rram` (Science China) — RRAM attention accelerator.
- `diware2024hwq` (ICCAD) — hardware-aware quantization for memristors.
- `nagal2025qatsurvey` (OpenReview) — QAT survey.

---

## 4. Deeper Commentary on Selected Papers

### 4.1 Ando *et al.*, IBM IEDM 2024/2025 — ViT on 14 nm ReRAM

**Why it matters:** This is the first published ReRAM silicon demonstration that explicitly includes *Vision Transformer transfer learning* (CIFAR-10 → CIFAR-100) on a 14 nm CMOS-compatible AIMC array. The authors implement Tiki-Taka v2, c-TTv2, and AGAD training algorithms to tolerate device asymmetry and variability, and they report <1 % accuracy degradation versus digital baselines under hybrid analog–digital implementations up to 20 % noise.

**Reviewer expectation:** A reviewer at a circuits/devices venue will know this paper. If the manuscript claims to be the first framework linking organic-device profiles to ViT accuracy without citing the closest inorganic silicon precedent, it risks a "insufficient related work" flag.

**Where to place:** Sec 2.3, in the paragraph discussing hybrid analog–digital mapping for ViT. Sentence suggestion: *"Recent silicon demonstrations have pushed AIMC transfer learning to ViT backbones on 14 nm ReRAM arrays, validating the hybrid analog–digital partitioning adopted here \citep{ando2025transfer}."*

### 4.2 Liu *et al.*, Nature Electronics 2024 — Wearable OECT Platform

**Why it matters:** Unlike device-level papers that report single-device conductance states, Liu demonstrates a *fully integrated* wearable in-sensor computing platform: stretchable OECT arrays + miniaturized readout + gesture-recognition demo at ~90 % accuracy. It is the strongest 2024 evidence that organic optoelectronic CIM is moving toward body-worn edge deployment.

**Reviewer expectation:** *Nature Electronics* is the top venue for organic electronics. A reviewer will expect this paper to be cited in any 2025–2026 manuscript discussing organic optoelectronic edge AI.

**Where to place:** Introduction paragraph 1 or Sec 2.2. Sentence suggestion: *"Integrated wearable platforms based on stretchable OECT arrays have already demonstrated on-body in-sensor classification \citep{liu2024wearable}, yet the system-level accuracy limits of modern vision backbones on such substrates remain unquantified."*

### 4.3 Analog Foundation Models, 2025

**Why it matters:** This paper trains Phi-3-mini and Llama-3.2-1B with per-channel additive Gaussian noise injection to survive PCM/ReRAM AIMC deployment. It is the largest-scale demonstration to date of hardware-aware training for emerging memory, evaluated on GLUE, GSM8K, MMLU, etc. The manuscript’s Ensemble HAT operates in the same conceptual space (noise injection + robustness) but for structured D2D mismatch rather than i.i.d. weight noise.

**Strategic value:** Citing it frames Ensemble HAT as complementary: *"While recent work has scaled hardware-aware noise injection to billion-parameter LLMs \citep{analogfm2025}, those models treat noise as i.i.d. per-channel perturbation; Ensemble HAT instead targets the spatially structured, instance-fixed D2D mismatch that defines analog crossbar deployment."*

### 4.4 Qiu *et al.*, IEDM 2025 — Monolithic 3D MoS2 + RRAM Attention

**Why it matters:** Vertical integration of MoS2 eDRAM (dynamic KV cache) and TaOx RRAM (static weights) specifically for Transformer attention. Hardware-calibrated simulations show 500× GPU speed-up. This is the strongest recent evidence that the "hybrid static+dynamic memory" strategy the manuscript adopts (analog crossbar for weights, digital for attention) is being pursued at the 3D-integration level.

---

## 5. Low-Priority / Thesis-Only Papers

These are solid papers but either overlap heavily with existing citations or sit too far from the manuscript’s core contributions.

- `yan2024lateral`, `sun2024memchip`, `choi20252dneuro`, `xiao2024neurochip` — good for thesis literature review, not essential for this manuscript.
- `tu2025tensorcim` — excellent digital-CIM work, but the manuscript is analog-CIM focused.
- `bellec2020eprop` — spiking-network local learning; outside the ANN/ViT scope.

---

## 6. Final Gap Checklist

| Gap | Risk if omitted | Recommended fix |
|-----|-----------------|-----------------|
| No 2024–2025 *Nature Electronics* organic neuron/neuromorphic perception citation | Reviewer: "You claim organic devices are promising but miss the top 2024–2025 papers." | Add `liu2024wearable`, `harikesh2024oeneurons`, `beller2024organicneurons`, `ji2025singleoectneuron` |
| No IEDM/ISSCC ViT-on-CIM silicon cited | Reviewer: "Hemlet and HARDSEA are architectural proposals; where is the silicon?" | Add `ando2025transfer`, `qiu2025m3dattention`, `yan2025learningaware` |
| No 2025 analog-robustness training at scale cited | Reviewer: "How does Ensemble HAT relate to recent LLM analog-training work?" | Add `analogfm2025` |
| Missing *Nature* / *Nature Communications* upstream anchor | Reviewer: "Introduction lacks a high-impact survey citation." | Add `lanza2025memristor`, `pedersen2024nir`, `aguirre2024hardwareann` |

---

## 7. BibTeX Sketches (Ready for `refs_gpt.bib`)

```bibtex
@article{liu2024wearable,
  author  = {Dingyao Liu and Xinyu Tian and Jing Bai and Shaocong Wang and Shilei Dai and Yan Wang and Zhongrui Wang and Shiming Zhang},
  title   = {A Wearable In-Sensor Computing Platform Based on Stretchable Organic Electrochemical Transistors},
  journal = {Nature Electronics},
  volume  = {7},
  pages   = {1176--1185},
  year    = {2024},
  doi     = {10.1038/s41928-024-01250-9}
}

@article{beller2024organicneurons,
  author  = {P. Beller and J. Pyrni Tardés and I. Cuculloch and others},
  title   = {Unravelling the Operation of Organic Artificial Neurons for Neuromorphic Bioelectronics},
  journal = {Nature Communications},
  volume  = {15},
  pages   = {5350},
  year    = {2024},
  doi     = {10.1038/s41467-024-48496-w}
}

@article{ji2025singleoectneuron,
  author  = {J. Ji and D. Gao and H.-Y. Wu and M. Xiong and others},
  title   = {Single-Transistor Organic Electrochemical Neurons},
  journal = {Nature Communications},
  volume  = {16},
  pages   = {4334},
  year    = {2025},
  doi     = {10.1038/s41467-025-59587-4}
}

@article{harikesh2024oeneurons,
  author  = {P. C. Harikesh and C.-Y. Yang and D. Tu and others},
  title   = {Organic Electrochemical Neurons for Neuromorphic Perception},
  journal = {Nature Electronics},
  volume  = {7},
  pages   = {525--536},
  year    = {2024},
  doi     = {10.1038/s41928-024-01251-8}
}

@inproceedings{ando2025transfer,
  author    = {Takashi Ando and Omobayode Fagbohungbe and Kenichi Imakita and others},
  title     = {Transfer Learning on Edge Using 14nm {CMOS}-compatible {ReRAM} Array and Analog In-memory Training Algorithm},
  booktitle = {IEEE International Electron Devices Meeting (IEDM)},
  year      = {2024},
  note      = {Invited}
}

@inproceedings{qiu2025m3dattention,
  author    = {Rui Qiu and Guoyun Gao and Zhiyuan Du and others},
  title     = {Monolithic 3D Integration of {MoS2} {eDRAM} and {RRAM} for Analog In-Memory Attention Computing},
  booktitle = {IEEE International Electron Devices Meeting (IEDM)},
  year      = {2025}
}

@inproceedings{yan2025learningaware,
  author    = {Longhao Yan and Zhe Zhan and Zelun Pan and others},
  title     = {An 8Mb Learning-Aware {RRAM} Compute-in-Memory Accelerator for Embodied Self-Supervised Learning},
  booktitle = {IEEE International Electron Devices Meeting (IEDM)},
  year      = {2025}
}

@misc{mia2026trilinear,
  author       = {Md Zesun Ahmed Mia and Jiahui Duan and Kai Ni and Abhronil Sengupta},
  title        = {Trilinear Compute-in-Memory Architecture for Energy-Efficient Transformer Acceleration},
  year         = {2026},
  eprint       = {2604.07628},
  archivePrefix= {arXiv}
}

@misc{analogfm2025,
  title         = {Analog Foundation Models},
  year          = {2025},
  eprint        = {2505.09663},
  archivePrefix = {arXiv}
}

@article{lanza2025memristor,
  author  = {Mario Lanza and others},
  title   = {The Growing Memristor Industry},
  journal = {Nature},
  volume  = {640},
  pages   = {613--622},
  year    = {2025},
  doi     = {10.1038/s41586-025-08733-5}
}

@article{aguirre2024hardwareann,
  author  = {F. Aguirre and others},
  title   = {Hardware Implementation of Memristor-Based Artificial Neural Networks},
  journal = {Nature Communications},
  volume  = {15},
  pages   = {1974},
  year    = {2024},
  doi     = {10.1038/s41467-024-45670-9}
}

@article{pedersen2024nir,
  author  = {J. E. Pedersen and others},
  title   = {Neuromorphic Intermediate Representation: A Unified Instruction Set for Interoperable Brain-Inspired Computing},
  journal = {Nature Communications},
  volume  = {15},
  pages   = {8122},
  year    = {2024},
  doi     = {10.1038/s41467-024-52259-9}
}
```

---

*End of review. Do NOT modify manuscript source or `refs_gpt.bib` yet — delegate to K-U8.*
