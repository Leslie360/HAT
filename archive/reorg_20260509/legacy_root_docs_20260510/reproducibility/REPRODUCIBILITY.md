# Reproducibility Notes — Nature Communications Submission

**Repository root:** `compute_vit/` (this directory)  
**Paper:** "Profile-Driven Behavioral Simulation of Organic Optoelectronic Compute-in-Memory for Edge Vision"  
**Contact:** [corresponding author email]

---

## 1. What this repository contains

- `paper/latex_gpt/` — LaTeX source for main manuscript (15 pp), supplementary information (21 pp), and cover letter (2 pp).
- `scripts/` — Training and evaluation scripts for Tiny-ViT-5M, ConvNeXt-Tiny, and ResNet-18.
- `analog_layers.py` — Mixed analog–digital layer implementations with noise injection, ADC quantization, and energy profiling.
- `report_md/_gpt/json_gpt/` — Fitted device-profile JSONs (Zhang2025 OPECT, Vincze2025 standard, and measured-device summaries).
- `checkpoints/` — Trained model checkpoints (see `CHECKPOINT_INVENTORY_20260418.md` for tiered release plan).

## 2. What is *not* in this repository

- **Public datasets** (CIFAR-10/100, Flowers-102, ImageNet) — downloaded automatically by `torchvision` on first use or via `download_data.sh`.
- **Raw doctoral measurement exports** (`数据_博士/`) — fitted profiles derived from these measurements are included; raw exports are available from the corresponding author upon reasonable request.
- **Full 25 GB checkpoint archive** — only the Tier-A load-bearing subset (~1.5 GB) is deposited on Zenodo with DOI; remaining checkpoints are available upon request.
- **CrossSim vendored snapshot** (`cross-sim/`) — reviewers should use the upstream public repository.

## 3. Environment

```bash
conda env create -f environment.yml
conda activate LLM
```

Key versions: Python 3.11, PyTorch ≥2.1, CUDA 12.1.

## 4. Quick sanity check

```bash
python scripts/_gpt/check_locked_numbers.py
```

Expected: `16/16 passed`. This script re-reads every JSON cited in the manuscript and asserts numerical consistency.

## 5. Reproducing main results

| Result | Script / Command | Checkpoint needed |
|:--|:--|:--|
| V4 canonical HAT 87.95% | `python train_tinyvit.py --config configs/tinyvit_v4_standard_noise.json` | `checkpoints/V4_hybrid_standard_noise_hat_best.pt` |
| Ensemble HAT 86.37±1.54% | `python train_tinyvit_ensemble.py --config configs/tinyvit_v4_ensemble.json` | generated during training |
| OPECT zero-shot 88.53±0.08% | `python eval_measured_profile.py --profile report_md/_gpt/json_gpt/doctor_measured_profiles.json` | Ensemble HAT ckpt |
| Inverse-gamma +5.8 pp | `python run_a23_experiments.py --gamma_phys 2.0` | V6 physical-frontend ckpt |
| NL=2.0 global 27.72% | `python train_tinyvit.py --config configs/tinyvit_v4_nl2.json` | generated during training |

See `CHECKPOINT_INVENTORY_20260418.md` for the full list of pre-trained checkpoints and their provenance.

## 6. Data availability

All datasets used are publicly available:
- CIFAR-10/100: https://www.cs.toronto.edu/~kriz/cifar.html
- Flowers-102: https://www.robots.ox.ac.uk/~vgg/data/flowers/102/
- ImageNet ILSVRC2012: https://image-net.org/ (user must supply)

## 7. Code availability

The complete simulation framework, training scripts, and evaluation pipelines are available at [Zenodo DOI to be inserted at submission].

---

*Last updated: 2026-04-18*
