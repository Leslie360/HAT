# Literature Freshness Audit: Ensemble HAT Novelty Claim
**Task:** R10F — Prior-art search for per-epoch D2D mask resampling (Ensemble HAT)  
**Date:** 2026-04-25  
**Auditor:** Kimi (subagent)  
**Search window:** Jan 2024 – Apr 2026 (concentrated on 2025–2026)  

---

## 1. Search Methodology

### 1.1 Search terms deployed (Google/Web search)
| Term set | Purpose |
|----------|---------|
| `"analog CIM HAT" / "hardware-aware training analog"` | Catch all recent HWA training papers |
| `"structured noise injection" memristor` | Find noise-injection training variants |
| `"device mismatch" training resampling` | Target D2D-aware training methods |
| `"analog-aware training" transformer` | Transformer-specific analog training |
| `"in-memory computing" CIM transformer noise` | Transformer-on-CIM robustness |
| `"ensemble HAT" / "epoch resampling" D2D` | Direct hit for our method |
| `"multi-instance hardware-aware training"` | Cross-instance training paradigms |
| `"variance-aware" noisy training analog` | Dynamic/noise-schedule training |
| `"layer ensemble averaging" memristive` | Specific IBM/GWU fault-tolerance scheme |
| `"sub-6-bit ADC" transformer analog CIM` | ADC-cliff prior art |
| `"Yoshioka" / "Wolters" analog CIM transformer precision` | Specific transformer-precision citations |

### 1.2 Venues scanned
- **arXiv** (cs.LG, cs.AR, eess.SP) — daily submissions via search proxy
- **NeurIPS 2025** (full proceedings, Dec 2025)
- **ICLR 2026** (accepted papers, Apr 2026)
- **ICML 2025** (accepted papers, Jul 2025)
- **Nature Electronics / Nature Communications** — last 18 months
- **IEEE TED, ISSCC, JSSC, TVLSI** — 2024–2026
- **IEDM 2025, ASP-DAC 2024/2025, ICCAD 2024**

### 1.3 Date range
Primary focus: **2025-01-01 to 2026-04-25**  
Back-stop: 2024-01-01 for foundational transformer-CIM papers.

---

## 2. Direct Prior Art: Per-Epoch D2D Mask Resampling for Analog CIM Training

**Verdict: NONE FOUND.**

After exhaustive search across the above venues and terms, **no published work** was identified that combines the following three elements of the Ensemble HAT claim:
1. **Per-epoch resampling** of device-to-device (D2D) variation masks during training;
2. **Training a single model** to be simultaneously robust across an ensemble of distinct hardware instances (i.e., cross-instance distribution matching at training time);
3. **Application to analog CIM hardware-aware training** of deep neural networks (specifically transformers).

The search specifically probed for:
- Multi-instance noise injection where each epoch draws a fresh D2D mask from a population of simulated chips.
- Ensemble-based training loops that average gradients across multiple hardware-realization samples per epoch.
- Any mention of “epoch resampling” combined with “D2D” in the analog/mixed-signal ML literature.

**Result:** Zero hits. The concept appears unreported in the peer-reviewed or pre-print literature through April 2026.

---

## 3. Close Prior Art (Structural Overlap but Distinct)

### 3.1 Rasch et al., *Nature Communications* 2023  
**Title:** "Hardware-aware training for large-scale and diverse deep learning inference workloads using in-memory computing-based accelerators"  
**Overlap:** Comprehensive HWA training with noise injection in the forward pass, systematic sensitivity analysis across CNNs/RNNs/Transformers, iso-accuracy demonstrations.  
**Distinction:** Uses a **single static noise model** per training run. No per-epoch resampling of D2D masks, no ensemble of hardware instances, no cross-instance robustness objective.  
**Action:** Already a canonical reference; ensure it is cited and distinguished.

### 3.2 Wang et al. (Heidelberg), *arXiv* Mar 2025 / ECML-PKDD 2025  
**Title:** "Variance-Aware Noisy Training: Hardening DNNs against Unstable Analog Computations"  
**Overlap:** Proposes dynamic noise schedules during training. Samples a noise standard deviation σ_var ~ N(α·σ_train, θ²) **per input image**, injecting time-varying noise that emulates temporal drift.  
**Distinction:** VANT varies noise **strength** per-sample/ per-training-phase but does **not** resample structured D2D spatial masks per epoch, nor does it train against an ensemble of distinct hardware instances. The noise is i.i.d. Gaussian on activations/weights, not a spatially-correlated D2D mask ensemble.  
**Action:** **Add citation.** Explicitly distinguish: VANT = temporal variance scheduling; Ensemble HAT = spatial D2D mask resampling across a chip population.

### 3.3 Büchel et al., *NeurIPS* 2025  
**Title:** "Analog Foundation Models"  
**Overlap:** Scalable HWA training for LLMs (Phi-3, Llama-3.2) on noisy, low-precision analog hardware. Achieves 4-bit-weight/8-bit-act baselines with analog noise.  
**Distinction:** Focuses on **quantization-aware adaptation** of pre-trained LLMs using static noise injection and distillation. No ensemble of D2D masks, no per-epoch resampling.  
**Action:** Already in `refs_gpt.bib` (`analogfm2025`). Ensure novelty paragraph contrasts with this work.

### 3.4 Yousuf et al., *Nature Communications* Feb 2025  
**Title:** "Layer ensemble averaging for fault tolerance in memristive neural networks"  
**Overlap:** Uses the word “ensemble” in the context of memristive crossbars, improves robustness to stuck-at faults.  
**Distinction:** **This is inference-time hardware redundancy**, not training-time ensemble HAT. LEA maps pre-trained weights redundantly onto multiple crossbar rows and averages output currents during inference. It requires **no retraining** and is a post-deployment fault-tolerance scheme.  
**Criticality:** HIGH — reviewers may conflate the two because of the shared term “ensemble.”  
**Action:** **Add citation.** Include a crisp distinction in the manuscript: *“Unlike Yousuf et al. [LEA], which ensembles at inference via physical redundancy, Ensemble HAT ensembles at training via per-epoch D2D mask resampling, yielding a single deployable weight set.”*

### 3.5 HaLoRA — Wu et al., *arXiv* Feb 2025  
**Title:** "HaLoRA: Hardware-aware Low-Rank Adaptation for Large Language Models Based on Hybrid Compute-in-Memory Architecture"  
**Overlap:** Hardware-aware adaptation for CIM; trains LoRA branches robust to RRAM noise.  
**Distinction:** Uses an extra loss term to minimize the gap between ideal and noisy optimization trajectories. Single-instance noise model; no D2D mask resampling.  
**Action:** **Add citation** as related work on hybrid-CIM robustness.

---

## 4. Related but Distinct Work

### 4.1 Full-stack memristor CIM training
**Yu et al., *Nature Communications* Mar 2025** — "A full-stack memristor-based computation-in-memory system with software-hardware co-development."  
Proposes Post-Deployment Training (PDT) that accounts for bit-slicing quantization errors and compiler-level weight splitting. Focuses on **software-hardware co-development** and automatic parameter search, not ensemble training.  
**Action:** Cite as recent full-stack training effort; distinguish scope.

### 4.2 On-chip analog transfer learning
**IBM IEDM 2025 (Ando et al.)** — "Transfer Learning on Edge Using 14nm CMOS-compatible ReRAM Array and Analog In-memory Training Algorithm."  
Demonstrates Tiki-Taka on-chip training with ViT-based transfer learning (CIFAR-10 → CIFAR-100). Hybrid analog-digital implementations tolerate up to 20% noise.  
**Action:** Already in `refs_gpt.bib` (`ando2025transfer`). Keep as related on-chip training reference.

### 4.3 SRAM-based ACiM simulation & hybrid inference
**Zhang et al. (ASiM), *IEEE TVLSI* 2025** — Simulation framework for SRAM-based analog CiM; explores hybrid analog-digital execution and majority voting for inference robustness.  
**Distinction:** Simulation tool + inference-time hybrid schemes, not training ensemble.  
**Action:** Cite as related simulation/benchmarking work.

### 4.4 Transformer-CIM simulation frameworks
**TransCIM (*arXiv* Apr 2026)** — End-to-end transformer evaluation on CIM; adds ADC quantization, back-gate non-uniformity.  
**CQ-CiM (*arXiv* Feb 2026)** — Hardware-aware embedding shaping for retrieval; level-dependent noise injection after compression head.  
**Action:** Both are post-training or inference-evaluation frameworks; cite for CIM-transformer ecosystem context.

### 4.5 Precision cliff for transformers on analog CIM
**Yoshioka, *ISSCC* 2024 / *JSSC* 2025** — "A 818–4094 TOPS/W Capacitor-Reconfigured CIM Macro for Unified Acceleration of CNNs and Transformers."  
- First analog CIM to achieve transformer-sufficient precision (45 dB SQNR, 31 dB CSNR in transformer mode vs. lower requirements for CNNs).  
- Explicitly demonstrates that transformers need **higher compute-SNR** than CNNs.  
**Wolters et al., *arXiv* Jun 2024** — "Memory Is All You Need: An Overview of Compute-in-Memory Architectures for Accelerating Large Language Model Inference."  
- Survey notes: *"compute-SNR values of 15–30 dB (4–6 effective bits) are sufficient for CNNs but potentially inadequate for transformers or large LLM inference."*  
**Action:** **Add both citations.** They provide independent, published support for the sub-6-bit / precision-cliff narrative that motivates Ensemble HAT.

### 4.6 Analog in-memory training theory
**Wu et al., *NeurIPS* 2025** — "Analog In-memory Training on General Non-ideal Resistive Elements: The Impact of Response Functions."  
Theoretical foundation for gradient-based training on AIMC with asymmetric response functions; proposes residual learning algorithm.  
**Action:** Cite as complementary theoretical work on analog training dynamics.

---

## 5. Conclusion: Novelty Claim Assessment

| Claim element | Status | Notes |
|---------------|--------|-------|
| **Per-epoch D2D mask resampling** | ✅ **No direct prior art found** | Searched arXiv, NeurIPS 2025, ICLR 2026, ICML 2025, Nature family, IEEE TED/ISSCC/JSSC. No published method uses per-epoch resampling of spatial D2D masks during training. |
| **Ensemble of hardware instances at training time** | ✅ **No direct prior art found** | Closest is Yousuf et al. 2025 (layer ensemble averaging), but that is **inference-time physical redundancy**, not training-time distribution matching. |
| **Cross-instance fresh-transfer benchmarking** | ⚠️ **Under-explored in literature** | Most works (Rasch 2023, Analog Foundation Models 2025) benchmark on a single noise model or average over random seeds. No standard benchmark explicitly tests “train on ensemble → deploy on unseen chip instance.” This is a **strength** of the manuscript’s empirical framing. |
| **Sub-6-bit ADC cliff for transformers** | ✅ **Supported by independent prior art** | Yoshioka 2024/2025 and Wolters 2024 explicitly state that transformers need higher CSNR/SQNR than CNNs, and that 4–6 effective bits is marginal. This **reinforces** the motivation rather than weakening it. |

### Bottom-line ruling
**The Ensemble HAT novelty claim STANDS, but requires proactive reframing in the manuscript to avoid reviewer confusion.**

Specifically:
1. **Distinguish from Layer Ensemble Averaging (Yousuf et al. 2025)** — reviewers may conflate the two because of the word “ensemble.” Add a sentence in the introduction or related work: *“We emphasize that Ensemble HAT operates at training time by resampling D2D masks per epoch, whereas Yousuf et al.’s layer ensemble averaging is an inference-time redundancy scheme that does not modify the training loop.”*
2. **Distinguish from Variance-Aware Noisy Training (Wang et al. 2025)** — VANT uses dynamic noise strength but not structured D2D spatial masks. Clarify that Ensemble HAT explicitly models spatially-correlated, instance-specific D2D variation rather than i.i.d. temporal drift.
3. **Leverage Yoshioka & Wolters** — Use their published precision-cliff observations as **motivational prior art** that makes Ensemble HAT timely and necessary.
4. **No reframing of the core claim is needed** — the method remains novel as of April 2026.

---

## 6. New Citations to Add to `refs_gpt.bib`

The following entries should be appended to `compute_vit/paper/latex_gpt/refs_gpt.bib` (and propagated to submission bundle copies). They are **not currently present** in the bib file as of the 2026-04-25 snapshot.

### 6.1 Close prior art to distinguish
```bibtex
@article{yousuf2025lea,
  author  = {Osama Yousuf and Brian D. Hoskins and Karthick Ramu and Mitchell Fream and William A. Borders and Advait Madhavan and Matthew W. Daniels and Andrew Dienstfrey and Jabez J. McClelland and Martin Lueker-Boden and Gina C. Adam},
  title   = {Layer Ensemble Averaging for Fault Tolerance in Memristive Neural Networks},
  journal = {Nature Communications},
  volume  = {16},
  number  = {1},
  pages   = {1250},
  year    = {2025},
  doi     = {10.1038/s41467-025-56319-6},
  url     = {https://doi.org/10.1038/s41467-025-56319-6},
  note    = {Inference-time redundancy; not training-time ensemble}
}

@misc{wang2025vant,
  author       = {Xiao Wang and Hendrik Borras and Bernhard Klein and Holger Froning},
  title        = {Variance-Aware Noisy Training: Hardening {DNN}s against Unstable Analog Computations},
  year         = {2025},
  eprint       = {2503.16183},
  archivePrefix= {arXiv},
  url          = {https://arxiv.org/abs/2503.16183},
  note         = {Dynamic noise schedules; no per-epoch D2D mask resampling}
}
```

### 6.2 Transformer precision / ADC cliff support
```bibtex
@inproceedings{yoshioka2024isscc,
  author    = {Kentaro Yoshioka},
  title     = {A 818--4094{TOPS/W} Capacitor-Reconfigured {CIM} Macro for Unified Acceleration of {CNN}s and Transformers},
  booktitle = {2024 {IEEE} International Solid-State Circuits Conference ({ISSCC})},
  year      = {2024},
  pages     = {574--576},
  doi       = {10.1109/ISSCC49657.2024.10454489},
  url       = {https://doi.org/10.1109/ISSCC49657.2024.10454489}
}

@article{yoshioka2025jssc,
  author  = {Kentaro Yoshioka},
  title   = {A 818--4094 {TOPS/W} Capacitor-Reconfigured Analog {CIM} for Unified Acceleration of {CNN}s and Transformers},
  journal = {IEEE Journal of Solid-State Circuits},
  volume  = {60},
  number  = {5},
  pages   = {1844--1855},
  year    = {2025},
  doi     = {10.1109/JSSC.2024.3457898},
  url     = {https://doi.org/10.1109/JSSC.2024.3457898}
}

@misc{wolters2024memory,
  author       = {Christopher Wolters and Xiaoxuan Yang and Ulf Schlichtmann and Toyotaro Suzumura},
  title        = {Memory Is All You Need: An Overview of Compute-in-Memory Architectures for Accelerating Large Language Model Inference},
  year         = {2024},
  eprint       = {2406.08413},
  archivePrefix= {arXiv},
  url          = {https://arxiv.org/abs/2406.08413}
}
```

### 6.3 Recent related work (ecosystem context)
```bibtex
@article{yu2025fullstack,
  author  = {Ruihua Yu and Ze Wang and Qi Liu and Bin Gao and Zhenqi Hao and Tao Guo and Sanchuan Ding and Junyang Zhang and Qi Qin and Dong Wu and Peng Yao and Qingtian Zhang and Jianshi Tang and He Qian and Huaqiang Wu},
  title   = {A Full-Stack Memristor-Based Computation-in-Memory System with Software-Hardware Co-Development},
  journal = {Nature Communications},
  volume  = {16},
  pages   = {2577},
  year    = {2025},
  doi     = {10.1038/s41467-025-57183-0},
  url     = {https://doi.org/10.1038/s41467-025-57183-0}
}

@misc{wu2025halora,
  author       = {Taiqiang Wu and Chenchen Ding and Wenyong Zhou and Yuxin Cheng and Xincheng Feng and Shuqi Wang and Chufan Shi and Zhengwu Liu and Ngai Wong},
  title        = {{HaLoRA}: Hardware-aware Low-Rank Adaptation for Large Language Models Based on Hybrid Compute-in-Memory Architecture},
  year         = {2025},
  eprint       = {2502.19747},
  archivePrefix= {arXiv},
  url          = {https://arxiv.org/abs/2502.19747}
}

@inproceedings{wu2025neurips_train,
  author    = {Zhaoxian Wu and Quan Xiao and Tayfun Gokmen and Omobayode Fagbohungbe and Tianyi Chen},
  title     = {Analog In-memory Training on General Non-ideal Resistive Elements: The Impact of Response Functions},
  booktitle = {Advances in Neural Information Processing Systems 38 ({NeurIPS} 2025)},
  year      = {2025},
  url       = {https://neurips.cc/virtual/2025/poster/116321}
}

@article{rasch2023ncomms,
  author  = {Malte J. Rasch and Charles Mackin and Manuel Le Gallo and An Chen and Andrea Fasoli and Frederic Odermatt and Ning Li and S. R. Nandakumar and Pritish Narayanan and Hsinyu Tsai and Geoffrey W. Burr and Abu Sebastian and Vijay Narayanan},
  title   = {Hardware-Aware Training for Large-Scale and Diverse Deep Learning Inference Workloads Using In-Memory Computing-Based Accelerators},
  journal = {Nature Communications},
  volume  = {14},
  pages   = {5282},
  year    = {2023},
  doi     = {10.1038/s41467-023-40770-4},
  url     = {https://doi.org/10.1038/s41467-023-40770-4}
}
```

---

## 7. Recommendations for Manuscript Defense

1. **Pre-empt the LEA confusion.** Add one sentence in the Introduction or Related Work that explicitly separates Ensemble HAT from Yousuf et al.’s Layer Ensemble Averaging (Nature Communications 2025). The distinction is training-time vs. inference-time.

2. **Pre-empt the VANT confusion.** Clarify that dynamic noise scheduling (Wang et al. 2025) does not address spatially-correlated D2D variation masks; it addresses temporal drift in noise magnitude.

3. **Strengthen motivation with Yoshioka & Wolters.** Cite the ISSCC 2024 / JSSC 2025 chip results and the Wolters 2024 survey to show that the transformer-precision cliff is an **externally validated problem** that makes Ensemble HAT necessary.

4. **Add the missing bib entries now.** The six citation blocks above should be appended to `refs_gpt.bib` before any camera-ready or rebuttal submission.

5. **No claim weakening required.** The core novelty of per-epoch D2D mask resampling for analog CIM training remains unchallenged by the 2025–2026 literature corpus.

---

*End of audit.*
