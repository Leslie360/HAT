# Bibliography Hardening — Exact Replacement Blocks

**Date:** 2026-04-17
**Scope:** Publication-grade replacement metadata and drop-in BibTeX blocks for the weakest live entries in `refs_gpt.bib`.

---

## 1. `wang2025oectarray`

### Current problem
- Author list is truncated to `Wang, Shuai and others`.
- The actual title in the bib (`High-Density, Ultraflexible Organic Electrochemical Transistor Array with Vertically Stacked Electrodes`) does **not** match the canonical paper title.

### Verified canonical metadata
| Field | Value |
|:------|:------|
| **Title** | High-density, ultraflexible organic electrochemical transistor array for brain activity mapping |
| **Authors** | Wei Xu, Yanlan Zhu, Xiaolin Zhou, Haoyue Guo, Jingxin Wang, Ruiqi Zhu, Zhengwei Hu, Wei Ma, Xing Ma, Xiaojian Li, Xiaomin Xu |
| **Journal** | Journal of Materials Chemistry C |
| **Year** | 2025 |
| **DOI** | 10.1039/D4TC02839B |
| **URL** | https://doi.org/10.1039/D4TC02839B |

### Drop-in BibTeX block
```bibtex
@article{wang2025oectarray,
  author  = {Wei Xu and Yanlan Zhu and Xiaolin Zhou and Haoyue Guo and Jingxin Wang and Ruiqi Zhu and Zhengwei Hu and Wei Ma and Xing Ma and Xiaojian Li and Xiaomin Xu},
  title   = {High-density, Ultraflexible Organic Electrochemical Transistor Array for Brain Activity Mapping},
  journal = {Journal of Materials Chemistry C},
  year    = {2025},
  doi     = {10.1039/D4TC02839B},
  url     = {https://doi.org/10.1039/D4TC02839B}
}
```

### Citation-use guidance
**Keep** as a recent organic-array demonstration, but ensure the manuscript text cites it for high-density OECT arrays / flexible substrates rather than for the incorrect "vertically stacked electrodes" framing.

---

## 2. `liu2025optoelectronic`

### Current problem
- Author list is a placeholder (`Liu, L. and Li, Z. and Zheng, Y. and others`).
- The full author list and exact article identifier were missing.

### Verified canonical metadata
| Field | Value |
|:------|:------|
| **Title** | Reconfigurable optoelectronic memristive architecture based on doped nanowire array for in-memory parallel perception and computation |
| **Authors** | Lingchen Liu, Zhexin Li, Yiqiang Zheng, Linlin Li, Bowen Zhong, Yongchao Yu, Zheng Lou, Lili Wang |
| **Journal** | National Science Review |
| **Year** | 2025 |
| **Volume / Issue** | 12 / 11 |
| **Pages / Article No.** | nwaf386 |
| **DOI** | 10.1093/nsr/nwaf386 |
| **URL** | https://doi.org/10.1093/nsr/nwaf386 |

### Drop-in BibTeX block
```bibtex
@article{liu2025optoelectronic,
  author  = {Lingchen Liu and Zhexin Li and Yiqiang Zheng and Linlin Li and Bowen Zhong and Yongchao Yu and Zheng Lou and Lili Wang},
  title   = {Reconfigurable Optoelectronic Memristive Architecture Based on Doped Nanowire Array for In-Memory Parallel Perception and Computation},
  journal = {National Science Review},
  year    = {2025},
  volume  = {12},
  number  = {11},
  pages   = {nwaf386},
  doi     = {10.1093/nsr/nwaf386},
  url     = {https://doi.org/10.1093/nsr/nwaf386}
}
```

### Citation-use guidance
**Keep** as a strong 2025 optoelectronic-memory-array reference. It supports the manuscript’s claim that recent array demonstrations now reach system-level integration.

---

## 3. `kim2025hemlet`

### Current problem
- Listed only as an arXiv preprint with no URL or DOI.

### Verified canonical metadata
| Field | Value |
|:------|:------|
| **Title** | Hemlet: A Heterogeneous Compute-in-Memory Chiplet Architecture for Vision Transformers with Group-Level Parallelism |
| **Authors** | Cong Wang, Zexin Fu, Jiayi Huang, Shanshi Huang |
| **Year** | 2025 |
| **eprint** | 2511.15397 |
| **archivePrefix** | arXiv |
| **URL** | https://arxiv.org/abs/2511.15397 |

### Drop-in BibTeX block
```bibtex
@misc{kim2025hemlet,
  author       = {Cong Wang and Zexin Fu and Jiayi Huang and Shanshi Huang},
  title        = {{Hemlet}: A Heterogeneous Compute-in-Memory Chiplet Architecture for Vision Transformers with Group-Level Parallelism},
  year         = {2025},
  eprint       = {2511.15397},
  archivePrefix= {arXiv},
  url          = {https://arxiv.org/abs/2511.15397}
}
```

### Citation-use guidance
**Keep** as a forward-looking ViT-on-CIM accelerator reference. The lack of a journal DOI is acceptable for a recent preprint, provided the manuscript does not overstate its peer-review status.

---

## 4. `olizaman2023dmm`

### Current problem
- The bib entry is formatted as an `@article` with `journal = {NSF Public Access Repository}`, which is not a standard bibliographic venue.
- The actual publication is an **IEEE ISCAS 2022 conference paper**, not a repository preprint.

### Verified canonical metadata
| Field | Value |
|:------|:------|
| **Title** | Reliability Improvement in RRAM-based DNN for Edge Computing |
| **Authors** | Md Oli-Uz-Zaman, Sajjad A. Khan, Geng Yuan, Ying Wang, Zhonghui Liao, Jiajun Fu, Caiwen Ding, Jingtong Wang |
| **Booktitle** | IEEE International Symposium on Circuits and Systems (ISCAS) |
| **Year** | 2022 |
| **Pages** | 581--585 |
| **Location** | Austin, TX, USA |

### Drop-in BibTeX block
```bibtex
@inproceedings{olizaman2022dmm,
  author    = {Md Oli-Uz-Zaman and Sajjad A. Khan and Geng Yuan and Ying Wang and Zhonghui Liao and Jiajun Fu and Caiwen Ding and Jingtong Wang},
  title     = {Reliability Improvement in {RRAM}-based {DNN} for Edge Computing},
  booktitle = {IEEE International Symposium on Circuits and Systems ({ISCAS})},
  year      = {2022},
  pages     = {581--585},
  address   = {Austin, TX, USA},
  organization = {IEEE}
}
```
*Note:* The original bib key said `2023`; the conference took place in 2022, so the key has been updated to `olizaman2022dmm`.

### Citation-use guidance
**Keep** if the manuscript needs a citation for RRAM reliability / differential-mapping at the edge, but move it to the **inorganic/related-work** cluster. If it is not actively cited in the main text, consider removing it to keep the bibliography lean.

---

## 5. `bettayeb2024memristorattention`

### Current problem
- The paper is currently cited in the manuscript to justify keeping attention operations digital, but **Bettayeb et al. actually argues the opposite**: it proposes an *analog memristor accelerator for transformer self-attention*. This creates a logical contradiction if cited as direct support for the manuscript's claim.

### Verified canonical metadata
| Field | Value |
|:------|:------|
| **Title** | Efficient memristor accelerator for transformer self-attention functionality |
| **Authors** | Meriem Bettayeb, Yasmin Halawani, Muhammad Umair Khan, Hani Saleh, Baker Mohammad |
| **Journal** | Scientific Reports |
| **Year** | 2024 |
| **Volume / Issue / Pages** | 14 / 1 / 24173 |
| **DOI** | 10.1038/s41598-024-75021-z |
| **URL** | https://doi.org/10.1038/s41598-024-75021-z |

### Drop-in BibTeX block
```bibtex
@article{bettayeb2024memristorattention,
  author  = {Meriem Bettayeb and Yasmin Halawani and Muhammad Umair Khan and Hani Saleh and Baker Mohammad},
  title   = {Efficient Memristor Accelerator for Transformer Self-Attention Functionality},
  journal = {Scientific Reports},
  year    = {2024},
  volume  = {14},
  number  = {1},
  pages   = {24173},
  doi     = {10.1038/s41598-024-75021-z},
  url     = {https://doi.org/10.1038/s41598-024-75021-z}
}
```

### Citation-use guidance
**Do not delete blindly.** Instead, **reframe** the citation to acknowledge a competing view. Safe sentence:

> "Recent heterogeneous CIM accelerators for Vision Transformers typically keep attention scores, softmax normalization, and dynamic interactions digital because of precision requirements and irregular access patterns (Kim 2025; Lin 2024), although analog memristor accelerators for self-attention have also been explored (Bettayeb 2024)."

This turns a contradictory citation into a balanced literature acknowledgment and avoids the appearance of selective omission.

---

## Summary of key changes

| Bib key | Action | New state |
|:--------|:-------|:----------|
| `wang2025oectarray` | Replace title + expand authors | Correct J. Mater. Chem. C entry |
| `liu2025optoelectronic` | Replace placeholder authors with full list | Correct NSR entry with DOI |
| `kim2025hemlet` | Add arXiv URL / eprint | Proper `@misc` preprint entry |
| `olizaman2023dmm` | Reformat from fake journal to IEEE ISCAS 2022 | Correct `@inproceedings` entry; key updated to 2022 |
| `bettayeb2024memristorattention` | Keep bib, but reframe sentence in manuscript | Acknowledge competing view rather than direct support |
