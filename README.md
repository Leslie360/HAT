# Profile-Driven Simulation for Organic Optoelectronic CIM

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Citation Count](https://img.shields.io/badge/citations-0-blue)]()

> Profile-driven simulation framework for training Vision Transformers on organic optoelectronic compute-in-memory arrays.

---

## Key Results

| Result | Value | Notes |
|:---|:---|:---|
| **Ensemble HAT** | **86.37 ± 1.54%** | Tiny-ViT-5M on CIFAR-10 with epoch-level D2D resampling |
| Severe-NL ceiling | 30.53% | Accuracy collapse under extreme photoresponse nonlinearity |
| Correlated D2D | — | Spatially correlated device-to-device variation degrades ensemble margins |
| Retention drift | — | Time-dependent photoresponse decay shifts analog weights |

See [`CHECKPOINT_INVENTORY_20260418.md`](CHECKPOINT_INVENTORY_20260418.md) for model weights and provenance.

---

## Quick Start

```bash
# 1. Install dependencies
conda env create -f environment.yml && conda activate LLM

# 2. Run a sanity check
python scripts/_gpt/check_locked_numbers.py   # Expected: 16/16 passed

# 3. Reproduce the Ensemble HAT result
python train_tinyvit_ensemble.py --config configs/tinyvit_v4_ensemble.json
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
├── analog_layers.py               # Mixed analog–digital layer library
├── analog_layers_ensemble.py      # Ensemble HAT extensions
├── physical_noise_pipeline.py     # Frontend photoresponse + shot noise
├── inference_analysis_utils.py    # Evaluation and profiling utilities
├── device_profile_utils.py        # Profile loading and validation
├── train_tinyvit.py               # Tiny-ViT training script
├── train_tinyvit_ensemble.py      # Ensemble HAT training
├── train_convnext.py              # ConvNeXt-Tiny training
├── train_resnet18.py              # ResNet-18 training
├── eval_measured_profile.py       # Zero-shot literature profile evaluation
├── run_a23_experiments.py         # Inverse-gamma frontend sweep
├── device_profiles/               # Literature-calibrated device profiles
├── checkpoints/                   # Pre-trained model weights
├── scripts/                       # Experiment orchestration
├── report_md/                     # Result manifests and JSON profiles
├── paper/                         # Manuscript source
├── data/                          # Datasets (auto-downloaded)
├── requirements.txt               # pip dependencies
├── environment.yml                # Conda environment
└── REPRODUCIBILITY.md             # Detailed reproducibility notes
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

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on bug reports, feature requests, and pull requests.

---

## Acknowledgements

This work was supported in part by the NVIDIA Academic Partnership Award (Apamayo).

---

*Last updated: 2026-04-18*
