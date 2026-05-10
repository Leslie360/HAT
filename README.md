# Profile-Driven Simulation for Organic Optoelectronic CIM

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Citation Count](https://img.shields.io/badge/citations-0-blue)]()

> Profile-driven simulation framework for training Vision Transformers on organic optoelectronic compute-in-memory arrays.

---

## Key Results

| Result | Value | Notes |
|:---|:---|:---|
| **Ensemble HAT** | **86.16 ± 0.19%** | Tiny-ViT-5M on CIFAR-10; three training seeds with epoch-level D2D resampling |
| Severe-NL recovery | ~81% | Recovery under NL=2.0 using audited gradient-scaling recipe |
| Correlated D2D | 82.1-84.6% | Robustness against spatially correlated device variation |
| Retention drift | ~79% | Accuracy plateau after scale-recalibration recovery |

See [`WORKSPACE_LAYOUT.md`](WORKSPACE_LAYOUT.md) for the active workspace map and [`PAPER_DIRECTORY_MAP_20260510.md`](PAPER_DIRECTORY_MAP_20260510.md) for why multiple paper-related directories still exist. Old root-level protocol/checklist/reproducibility snapshots are isolated under `archive/reorg_20260509/legacy_root_docs_20260510/`.

---

## Quick Start

```bash
# 1. Install dependencies
conda env create -f environment.yml && conda activate LLM

# 2. Review the active workspace map
less WORKSPACE_LAYOUT.md

# 3. Run a small evaluation or training job from the project root
python cli/eval_fresh_instances.py --help
python cli/train_tinyvit_ensemble.py --help
```

---

## Installation

### Conda (recommended)

```bash
conda env create -f environment.yml
conda activate LLM
```

### pip

```bash
pip install -r requirements.txt
```

### GPU Requirements

- NVIDIA GPU with CUDA 12.1 support
- ≥ 8 GB VRAM for Tiny-ViT training
- ≥ 16 GB VRAM recommended for ensemble training

---

## Project Structure

```
compute_vit/
├── cli/                           # Train/eval command wrappers
├── src/compute_vit/               # Python implementation package
├── configs/                       # Stable configs
├── device_profiles/               # Literature/calibrated device profiles
├── manuscripts/                   # Compatibility links to manuscript sources
├── paper/                         # Legacy Paper1 compatibility shell
├── paper1/                        # Paper-1 manuscript, release, provenance, reports
├── paper2/                        # Paper-2 / 107 KV-cache research
├── paper2_aihwkit_baseline/       # Paper-2 AIHWKit/PCM baseline
├── thesis/                        # Degree thesis sources and template
├── coordination/                  # Active dispatches, audits, agent reports
├── tools/                         # Validation, plotting, LaTeX, maintenance tools
├── scripts/                       # Experiment orchestration
├── experiments/                   # Exploratory experiments and manifests
├── archive/                       # Isolated old files and restore scripts
├── data/                          # Datasets (auto-downloaded/local)
├── checkpoints/                   # Protected local model weights
├── requirements.txt               # pip dependencies
├── environment.yml                # Conda environment
└── WORKSPACE_LAYOUT.md            # Workspace map
```

---

## Citation

If you use this code in your research, please cite:

```bibtex
@article{li2026organic,
  title={Profile-Driven Behavioral Simulation of Organic Optoelectronic Compute-in-Memory for Edge Vision},
  author={Li, Songqiao and others},
  journal={Nature Communications},
  year={2026}
}
```

---

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

## Contributing

Issues and improvements should preserve the root layout in [`WORKSPACE_LAYOUT.md`](WORKSPACE_LAYOUT.md) and keep old or deprecated files isolated under `archive/`.

---

## Acknowledgements

This work was supported in part by the NVIDIA Academic Partnership Award (Apamayo).

---

*Last updated: 2026-05-10*
