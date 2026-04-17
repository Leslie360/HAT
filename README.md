# Hardware-Aware Simulation of Organic Optoelectronic CIM Inference

This repository provides a profile-driven behavioral simulation framework
for organic optoelectronic compute-in-memory (CIM)
inference on edge-vision tasks.
The project connects device-profile assumptions to system-level outcomes across
CNN and Transformer backbones, with explicit support for quantization,
device-to-device and cycle-to-cycle variability, retention, ADC effects,
nonlinear-write stress, and literature-derived profile substitution.

## Architecture

The repository is organized around a hybrid analog/digital deployment model.

- `analog_layers.py`: analog linear and convolution layers, retention/noise logic, ADC, energy profiling
- `train_tinyvit.py`: Tiny-ViT train/eval entrypoint with checkpoint and Monte Carlo evaluation support
- `train_convnext.py`: ConvNeXt train/eval entrypoint with matching analog controls
- `device_profile_utils.py`: literature/measured profile loading and validation
- `run_device_comparison.py`: zero-shot transfer across device profiles
- `paper/`: manuscript assets, figures, LaTeX scaffold, and plotting scripts
- `report_md/`: generated result artifacts and internal experiment reports

## Quick Start

Create or activate the project environment first, then run the baseline or
analog experiments from the repository root.

### Minimal setup

```bash
conda create -n compute_vit python=3.11 -y
conda activate compute_vit
```

Then install the dependencies required by your workflow, including PyTorch,
TorchVision, timm, and the standard scientific Python stack used by the
training, evaluation, and plotting scripts.

### Tiny-ViT CIFAR-10 digital baseline

```bash
python train_tinyvit.py \
  --mode train \
  --experiment V1 \
  --dataset cifar10 \
  --pretrained \
  --amp \
  --epochs 100 \
  --batch-size 256 \
  --num-workers 4
```

### Tiny-ViT repeated evaluation from a checkpoint

```bash
python train_tinyvit.py \
  --mode eval \
  --experiment V4 \
  --dataset cifar10 \
  --checkpoint checkpoints/path/to/V4_4bit_noise_hat_best.pt \
  --eval-runs 10 \
  --amp
```

### ConvNeXt CIFAR-10 analog training

```bash
python train_convnext.py \
  --mode train \
  --experiment C4 \
  --dataset cifar10 \
  --amp \
  --epochs 100 \
  --batch-size 128
```

## Device Profile System

The framework is profile-driven: device assumptions can be replaced through a
JSON profile without modifying the training or evaluation code paths.

Supported profile fields include:

- conductance window: `G_min`, `G_max`, `dynamic_range`
- discrete levels: `n_states`
- variability: `sigma_c2c`, `sigma_d2d`, `noise_mode`
- retention: `A_0`, `tau_1`, `tau_2`
- plasticity surrogates: `NL_LTP`, `NL_LTD`
- optoelectronic terms: `gamma_phys`, `I_dark`, `responsivity_alpha`
- optional conductance INL lookup table: `inl_table`

Built-in and literature-derived examples live under:

- `device_profiles/`

For stable profile guidance, start with:

- `docs/DEVICE_PROFILE_GUIDE.md`

### Measured-profile evaluation

```bash
python eval_measured_profile.py \
  --profile-json report_md/_gpt/json_gpt/doctor_measured_profiles.json \
  --checkpoint-path checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt \
  --model-type tinyvit \
  --experiment V4 \
  --dataset cifar10 \
  --max-samples 1000
```

Every run now emits a user-facing bundle under:

- `outputs/measured_profile_runs/<timestamp>_<model>_<experiment>_<dataset>_<checkpoint>/`

Start with:

- `run_summary.md`: one-file human summary of what was evaluated and what the results mean
- `metrics.csv`: compact table for cross-run comparison
- `profiles_used.json`: exact machine-readable profile payload used during the run

## Documentation

Stable project-facing documentation lives under `docs/`:

- `docs/README.md`: top-level documentation index
- `docs/DEVICE_PROFILE_GUIDE.md`: profile schema, fitting expectations, and validation rules
- `docs/EXPERIMENT_REGISTRY.md`: canonical experiment IDs and reporting semantics
- `docs/PHYSICS_STACK.md`: modeled physics, first-order assumptions, and out-of-scope effects

## Experiments

The manuscript centers on three evidence layers:

- canonical cross-dataset results: CIFAR-10, CIFAR-100, Flowers-102
- fresh-instance transferability: same-instance vs fresh-instance robustness
- physical-stress extensions: proportional noise, nonlinear write, retention-aware retraining

Key scripts:

- `run_noise_sweep.py`
- `run_device_comparison.py`
- `eval_fresh_instances.py`
- `run_a23_experiments.py`

## Reproducibility

The project records execution traces and generated artifacts under
`logs/` and `report_md/`. The current standard is execution-trace
reproducibility rather than strict bitwise determinism; Monte Carlo evaluations
and checkpoint lineage are stored so that reported results remain auditable.

## Citation

If you use this repository, please cite the accompanying manuscript:

```bibtex
@article{li2026organiccim,
  title   = {Hardware-Aware Simulation of Organic Optoelectronic Compute-in-Memory Inference for Edge Vision},
  author  = {Li, Songqiao},
  journal = {Under review},
  year    = {2026}
}
```

## License

This project is released under the Apache License 2.0. See [LICENSE](LICENSE)
for the full text.
