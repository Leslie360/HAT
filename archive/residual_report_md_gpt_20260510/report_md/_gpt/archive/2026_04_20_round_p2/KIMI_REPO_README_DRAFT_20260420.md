# Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision

[![License](https://img.shields.io/badge/license-TBD-blue.svg)](LICENSE)
[![Zenodo](https://img.shields.io/badge/zenodo-DOI_TBD-blue.svg)](https://doi.org/TBD)

> **Repository:** `https://github.com/USERNAME/REPO_NAME` (placeholder — will be updated upon public release)

This repository implements a PyTorch-native behavioral simulation framework that maps literature-derived organic optoelectronic device metrics to task-level vision accuracy. It supports mixed analog–digital deployment of ResNet-18, ConvNeXt-Tiny, and Tiny-ViT-5M under realistic non-idealities including photoresponse nonlinearity, retention drift, device-to-device variability, and ADC quantization. Through a replaceable profile interface, the framework incorporates photoresponse, retention, and write nonlinearity not directly captured by inorganic simulators, serving as a simulation-based materials-to-system decision aid for identifying device characteristics that constrain edge-vision deployment.

---

## Installation

We recommend using [conda](https://docs.conda.io/) with the provided environment file:

```bash
conda env create -f environment.yml
conda activate LLM
```

Core dependencies:
- Python 3.11
- PyTorch ≥2.1
- CUDA 12.1
- torchvision, numpy, scipy, matplotlib, scikit-learn, timm

For a minimal pip-only install:

```bash
pip install -r requirements.txt
```

---

## Quick Start — Reproduce the Three Headline Numbers

| Headline Result | Value | Command |
|:---|:---|:---|
| **Ensemble HAT** (fresh-instance recovery) | **86.37 ± 1.54%** | `python train_tinyvit_ensemble.py --config configs/tinyvit_v4_ensemble.json` |
| **Standard HAT collapse** (hardware-instance overfitting) | **10.00%** | `python scripts/_gpt/eval_standard_fresh_instance_noamp.py` |
| **Correlated-D2D robustness** (ρ = 0.3) | **84.57 ± 2.39%** | `python scripts/_gpt/eval_spatially_correlated_d2d.py --correlations 0.3` |

> **Note:** Training Ensemble HAT from scratch (~1.5 h on a single GPU) reproduces the 86.37% result. The 10.00% and 84.57% results are **evaluation-only** and require the pre-trained checkpoints (see [Dataset & Checkpoint Preparation](#dataset--checkpoint-preparation)).

### Sanity check

After installing dependencies and downloading checkpoints, verify numerical consistency against the manuscript:

```bash
python scripts/_gpt/check_locked_numbers.py
```

Expected output: `16/16 passed`.

---

## Dataset & Checkpoint Preparation

### Datasets

All datasets are publicly available. CIFAR-10/100 and Flowers-102 will be downloaded automatically by `torchvision` on first use:

| Dataset | Auto-download | Notes |
|:---|:---:|:---|
| CIFAR-10 | ✅ | `torchvision.datasets.CIFAR10` |
| CIFAR-100 | ✅ | `torchvision.datasets.CIFAR100` |
| Flowers-102 | ✅ | `torchvision.datasets.Flowers102` |
| ImageNet ILSVRC2012 | ❌ | User must supply manually; see `download_data.sh` for expected directory structure |

### Pre-trained checkpoints

The Tier-A load-bearing subset of checkpoints (~1.5 GB) is required to reproduce the evaluation-only results. Checkpoints will be deposited on Zenodo with a DOI assigned at acceptance; until then, they are available upon reasonable request (see `CHECKPOINT_INVENTORY_20260418.md` for the full catalog).

Place downloaded checkpoints under:

```
checkpoints/
├── V4_hybrid_standard_noise_hat_best.pt          # Standard HAT (for 10.00% collapse eval)
├── _ensemble/V4_hybrid_standard_noise_hat_best.pt # Ensemble HAT (for 86.37% and 84.57% evals)
└── ... (see CHECKPOINT_INVENTORY_20260418.md)
```

---

## Hardware Requirements

- **GPU:** NVIDIA GPU with CUDA 12.1 support
- **VRAM:** ≥8 GB recommended (batch size 64; reduce `--batch_size` if constrained)
- **Storage:** ~5 GB for datasets + ~2 GB for Tier-A checkpoints
- **OS:** Linux (tested on Ubuntu 22.04)

The training scripts default to `cuda` if available and fall back to `cpu`. Training Tiny-ViT-5M from scratch takes approximately **1–2 hours** on a modern consumer GPU (e.g., RTX 3090 / RTX 4090) and **<30 minutes** on an A100.

---

## Repository Structure

```
.
├── analog_layers.py              # Core mixed-signal layer library
├── analog_layers_ensemble.py     # Ensemble HAT extensions
├── train_tinyvit.py              # Tiny-ViT training (V1–V8 regimes)
├── train_tinyvit_ensemble.py     # Ensemble HAT training
├── train_convnext.py             # ConvNeXt-Tiny training
├── train_resnet18.py             # ResNet-18 training
├── eval_*.py                     # Evaluation and fresh-instance transfer scripts
├── scripts/_gpt/                 # Reproducibility helpers (locked-number checks, correlated-D2D eval)
├── checkpoints/                  # Pre-trained model checkpoints
├── configs/                      # JSON experiment configurations
├── paper/latex_gpt/              # Manuscript LaTeX source
├── report_md/_gpt/json_gpt/      # Fitted device profiles and result JSONs
├── environment.yml               # Conda environment specification
├── requirements.txt              # Pip-only dependency list
└── README.md                     # This file
```

---

## Citation

If you use this code or framework in your research, please cite:

```bibtex
@article{li2026organic,
  title={Profile-Driven Behavioral Simulation of Organic Optoelectronic Compute-in-Memory for Edge Vision},
  author={Li, Songqiao and others},
  journal={Nature Communications},
  year={2026},
  publisher={Springer Nature},
  doi={TBD},
  url={TBD}
}
```

---

## License

This project is released under a permissive open-source license (MIT / Apache-2.0 / BSD — **TBD; placeholder until authors finalize**). See `LICENSE` for details.

---

## Data & Code Availability

- **Source data:** Submission-facing source-data bundles (raw experiment JSONs and summary CSVs for all figures) are staged under `release_artifacts/` and will be expanded into the final public Zenodo archive at acceptance.
- **Zenodo DOI:** `10.5281/zenodo.TBD` (placeholder — will be minted at acceptance).
- **Raw measurements:** Raw doctoral measurement exports are available from the corresponding author upon reasonable request.

---

*Last updated: 2026-04-20*
