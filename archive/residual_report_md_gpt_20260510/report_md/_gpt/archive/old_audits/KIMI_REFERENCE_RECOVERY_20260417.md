# Kimi Reference Recovery — 2026-04-17

Scope: verify or recover canonical metadata for the papers most likely to be challenged in review, and flag formatting inconsistencies in `refs_gpt.bib`.

---

## Verified / Corrected Entries

| Bib key | Full title | Authors | Venue | Year | Vol/Issue/Pages | DOI | URL |
|:--------|:-----------|:--------|:------|:----:|:----------------|:----|:----|
| `peng2020dnnneurosim` | DNN+NeuroSim V2.0: An End-to-End Benchmarking Framework for Compute-in-Memory Accelerators for On-Chip Training | Xiaochen Peng, Shanshi Huang, Hongwu Jiang, Anni Lu, Shimeng Yu | IEEE TCAD | **2021** | 40(11):2306–2319 | 10.1109/TCAD.2020.3043731 | https://doi.org/10.1109/TCAD.2020.3043731 |
| `rasch2021aihwkit` | A Flexible and Fast PyTorch Toolkit for Simulating Training and Inference on Analog Crossbar Arrays | Malte J. Rasch, Diego Moreda, Tayfun Gokmen, Manuel Le Gallo, Fabio Carta, Cindy Goldberg, Kaoutar El Maghraoui, Abu Sebastian, Vijay Narayanan | IEEE ICRC (arXiv:2104.02184) | 2021 | — | 10.48550/arXiv.2104.02184 | https://doi.org/10.48550/arXiv.2104.02184 |
| `crosssim2026` | CrossSim: Sandia's simulator for analog AI accelerators | Sandia National Laboratories (tech report) | SAND Report | **2024** | — | 10.2172/2585829 | https://doi.org/10.2172/2585829 |
| `lammie2022memtorch` | MemTorch: An open-source simulation framework for memristive deep learning systems | Corey Lammie, Wei Xiang, Bernabé Linares-Barranco, Mostafa Rahimi Azghadi | Neurocomputing | 2022 | 485:124–133 | 10.1016/j.neucom.2022.02.043 | https://doi.org/10.1016/j.neucom.2022.02.043 |
| `tobin2017domain` | Domain Randomization for Transferring Deep Neural Networks from Simulation to the Real World | Josh Tobin, Rachel Fong, Alex Ray, Jonas Schneider, Wojciech Zaremba, Pieter Abbeel | IROS | 2017 | pp. 23–30 | **10.1109/IROS.2017.8202133** | https://doi.org/10.1109/IROS.2017.8202133 |
| `joshi2020accurate` | Accurate Deep Neural Network Inference Using Computational Phase-Change Memory | Vinay Joshi, Manuel Le Gallo, Simon Haefeli, Irem Boybat, S. R. Nandakumar, Christophe Piveteau, Martino Dazzi, Bipin Rajendran, Abu Sebastian, Evangelos Eleftheriou | Nature Communications | 2020 | 11:2473 | **10.1038/s41467-020-16108-9** | https://doi.org/10.1038/s41467-020-16108-9 |
| `choi2019pact` | PACT: Parameterized Clipping Activation for Quantized Neural Networks | Jungwook Choi, Zhuo Wang, Swagath Venkataramani, Pierce I-Jen Chuang, Vijayalakshmi Srinivasan, Kailash Gopalakrishnan | ICML 2018 / arXiv:1805.06085 | **2018** | — | 10.48550/arXiv.1805.06085 | http://arxiv.org/abs/1805.06085 |
| `bengio2013estimating` | Estimating or Propagating Gradients Through Stochastic Neurons for Conditional Computation | Yoshua Bengio, Nicholas Léonard, Aaron Courville | arXiv:1308.3432 | 2013 | — | — | http://arxiv.org/abs/1308.3432 |
| `xu2025emerging` | Emerging Artificial Synaptic Devices Based on Organic Semiconductors: Molecular Design, Structure and Applications | Yunchao Xu, Yuan He, Dongyong Shan, Biao Zeng, Qian-Xi Ni | ACS Applied Materials & Interfaces | 2025 | — | 10.1021/acsami.4c17455 | https://doi.org/10.1021/acsami.4c17455 |
| `guo2024organic` | An Organic Optoelectronic Synapse with Multilevel Memory Enabled by Gate Modulation | Haotian Guo, Jing Guo, Yujing Wang, Hezhen Wang, Simin Cheng, Zehao Wang, Qian Miao, Xiaomin Xu | ACS Applied Materials & Interfaces | 2024 | — | 10.1021/acsami.3c19624 | https://doi.org/10.1021/acsami.3c19624 |
| `zhang2026opect` | Near-infrared organic photoelectrochemical synaptic transistors by photolithography for neuromorphic visual systems | Xu Liu, Shilei Dai, Yiyang Jin, Junyao Zhang, Ziyi Guo, Tongrui Sun, Li Li, Pu Guo, Huaiyu Gao, Haixia Liang | Nature Communications | **2025** | 17:197 | 10.1038/s41467-025-66891-6 | https://doi.org/10.1038/s41467-025-66891-6 |
| `vincze2026dualplasticity` | Simultaneous Dual-Plasticity Organic Synaptic Transistor for Neuromorphic Computing | Tomas Vincze, Michal Hanic, Martin Berki, Martin Weis | Advanced Electronic Materials | **2025** | 11(1):2500515 | 10.1002/aelm.202500515 | https://doi.org/10.1002/aelm.202500515 |

---

## Per-Paper Notes (Relevance + Placement)

**`peng2020dnnneurosim`**
- *Why it matters*: Positions the manuscript within the established CIM simulator lineage (NeuroSim).
- *Where it is cited*: Introduction and Related Work, used to acknowledge prior inorganic benchmarking frameworks.

**`rasch2021aihwkit`**
- *Why it matters*: AIHWKIT is the closest industrial/academic analog-training toolkit; the manuscript uses it for a shared-regime sanity check (ResNet-18/CIFAR-10, 4-bit).
- *Where it is cited*: Introduction, Discussion (§6.6), and Supplementary (inorganic-comparison section).

**`crosssim2026`**
- *Why it matters*: CrossSim is the other mature simulator against which the framework is directly compared in the revised manuscript.
- *Where it is cited*: Introduction, Related Work, Discussion (joint-calibration comparison).

**`lammie2022memtorch`**
- *Why it matters*: MemTorch represents the PyTorch-embedded memristive-simulation thread that precedes the present organic-specific stack.
- *Where it is cited*: Introduction / Related Work.

**`tobin2017domain`**
- *Why it matters*: Provides the conceptual anchor for domain-randomization / sim-to-real framing that reviewers may compare against Ensemble HAT.
- *Where it is cited*: Introduction and Related Work.

**`joshi2020accurate`**
- *Why it matters*: Canonical hardware-aware training (HAT) reference for PCM/CIM; the manuscript explicitly contrasts standard HAT with Ensemble HAT.
- *Where it is cited*: Introduction, Related Work, and Discussion.

**`choi2019pact`**
- *Why it matters*: Quantization-aware training baseline that anchors the HAT discussion.
- *Where it is cited*: Introduction and Related Work.

**`bengio2013estimating`**
- *Why it matters*: Straight-through estimator (STE) lineage; underlies the quantization and analog-surrogate backward pass in the methodology.
- *Where it is cited*: Related Work / methodology context (implicit in HAT formulation).

**`xu2025emerging`**
- *Why it matters*: Recent comprehensive review of organic synaptic devices; strengthens the introductory motivation.
- *Where it is cited*: Introduction, Related Work.

**`guo2024organic`**
- *Why it matters*: Specific recent organic optoelectronic synapse demonstration with multilevel memory.
- *Where it is cited*: Introduction, Related Work.

**`zhang2026opect`**
- *Why it matters*: The 2025 OPECT case-study anchor; the manuscript reports zero-shot transfer to a profile calibrated from this paper.
- *Where it is cited*: Introduction, Results (§5.7 case study), Discussion, and Supplementary parameter-provenance tables.

**`vincze2026dualplasticity`**
- *Why it matters*: Source of the canonical retention / dual-plasticity parameters used in the organic profile.
- *Where it is cited*: Introduction, Results, Discussion, and Supplementary (Vincze parameter extraction section).

---

## Likely Weak or Placeholder References

1. **`wang2025oectarray`** — Author list is truncated to `Wang, Shuai and others`. Venue metadata exists (J. Mater. Chem. C, DOI 10.1039/D4TC02839B), but the incomplete author string is not publication-grade. If retained, it should be expanded or downgraded to a parenthetical mention rather than a formal numbered citation.
2. **`liu2025optoelectronic`** — Same issue: `Liu, L. and Li, Z. and Zheng, Y. and others` is a placeholder. The actual paper has a longer author list.
3. **`olizaman2023dmm`** — Journal field currently reads `NSF Public Access Repository`, which is not a standard bibliographic venue. The entry is actually an arXiv preprint (arXiv:2201.09342, DOI 10.48550/arXiv.2201.09342). It should be reformatted as an arXiv/misc entry with a coherent title: *Reliability Improvement in RRAM-based DNN for Edge Computing*.
4. **`kim2025hemlet`** — Listed as an arXiv preprint without a URL or DOI in the current bib. It is fine as a forward-looking accelerator reference, but the lack of a direct URL/DOI makes it slightly fragile for review.

---

## Likely Duplicate / Inconsistent Entries

1. **Bib-key vs. year mismatch (`choi2019pact`)** — The bib key says 2019, but the work is ICML 2018 / arXiv 2018. This inconsistency can confuse automated bib processing and should be reconciled (prefer key `choi2018pact`).
2. **Bib-key vs. year mismatch (`peng2020dnnneurosim`)** — The bib key says 2020, but the IEEE TCAD publication year is 2021. This is a common legacy mismatch from preprint-to-journal lag, but it is technically inconsistent.
3. **Bib-key vs. year mismatch (`crosssim2026`, `zhang2026opect`, `vincze2026dualplasticity`)** — All three use a 2026 bib key while the actual publication years are 2024, 2025, and 2025 respectively. These keys were likely written when the papers were anticipated as 2026 publications, but they have since appeared earlier. The keys should be updated to `crosssim2024`, `zhang2025opect`, and `vincze2025dualplasticity` (or the manuscript should accept the mismatch if the keys are already frozen in the LaTeX source).
4. **No DOI for `joshi2020accurate` and `tobin2017domain`** — Both have well-known DOIs that are currently missing from `refs_gpt.bib` (see table above for exact values).

---

## Actionable Fixes for `refs_gpt.bib`

- **Add DOI** to `joshi2020accurate`: `doi = {10.1038/s41467-020-16108-9}`
- **Add DOI** to `tobin2017domain`: `doi = {10.1109/IROS.2017.8202133}`
- **Add DOI/URL** to `kim2025hemlet`: `eprint = {2511.15397}`, `archivePrefix = {arXiv}`, `url = {https://arxiv.org/abs/2511.15397}`
- **Reformat** `olizaman2023dmm` from `@article` to `@misc` or `@online`, fix title, and replace journal with `archivePrefix = {arXiv}`.
- **Expand or deprioritize** `wang2025oectarray` and `liu2025optoelectronic` author lists if they are to remain formal citations.
- **Decide** whether to rename bib keys (`choi2019pact`→`choi2018pact`, `crosssim2026`→`crosssim2024`, etc.) or to document the mismatch in a supplementary note. Renaming is cleaner but requires a global find-replace across the `.tex` source.
