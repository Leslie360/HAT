# Local GPU Mixed-Precision P0 Report — 20260510

## Evidence grade

- `pilot/provisional`: 512-image CIFAR-10 test-subset probe over the top 10 static-ranked analog layers, not a final claim-bearing result.
- No training was run; checkpoints and datasets were read-only.

## Exact command

```bash
LOG="/home/qiaosir/projects/compute_vit/logs/local_gpu_mixed_precision_sensitivity_20260510_161122_20260510.log"; PYTHONPATH="/home/qiaosir/projects/compute_vit/src/compute_vit" /home/qiaosir/miniconda3/envs/aihwkit/bin/python - <<'PY' 2>&1 | tee "$LOG"
```

- Log: `/home/qiaosir/projects/compute_vit/logs/local_gpu_mixed_precision_sensitivity_20260510_161122_20260510.log`

## GPU preflight

```text
Sun May 10 16:11:24 2026
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 595.58.04              Driver Version: 596.21         CUDA Version: 13.2     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 5070 Ti     On  |   00000000:01:00.0  On |                  N/A |
|  0%   53C    P8             20W /  300W |     351MiB /  16303MiB |      2%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A             520      G   /Xwayland                             N/A      |
+-----------------------------------------------------------------------------------------+
```

## Method correction

- The first attempted probe disabled or globally resampled D2D and failed the checkpoint reproduction gate.
- This report uses the checkpoint D2D buffers as baseline because the V4 checkpoint reproduces 91.92% through the official eval path only under its learned/loaded analog state.
- Perturbation is one target layer D2D resample at a time, with all other analog layers restored to checkpoint D2D and baseline V4 noise settings.

## Inputs

- Checkpoint: `/home/qiaosir/projects/compute_vit/checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- Checkpoint metadata: epoch=99, best_epoch=99, best_acc=91.94, dataset=cifar10, num_classes=None
- Dataset: `cifar10` test subset, n=512, deterministic seed=20260510.
- Baseline per seed: checkpoint D2D buffers, sigma_d2d=0.1, sigma_c2c=0.05.
- Perturbation: one target layer D2D buffer resampled at sigma_d2d=0.1; C2C seed matched; seeds=[20260510, 20260511, 20260512].

## Baseline reproduction gate

| Seed | Baseline loss | Baseline acc (%) |
|---:|---:|---:|
| 20260510 | 0.338983 | 93.7500 |
| 20260511 | 0.364759 | 92.7734 |
| 20260512 | 0.472269 | 91.2109 |

- Mean baseline subset accuracy: 92.5781%.

## Outputs

- Layer inventory: `/home/qiaosir/projects/compute_vit/thesis/results/mixed_precision/layer_inventory_20260510.tsv`
- Static priority rank: `/home/qiaosir/projects/compute_vit/thesis/results/mixed_precision/layer_static_rank_20260510.tsv`
- Sensitivity rows: `/home/qiaosir/projects/compute_vit/thesis/results/mixed_precision/layer_sensitivity_20260510.tsv`
- Sensitivity summary: `/home/qiaosir/projects/compute_vit/thesis/results/mixed_precision/layer_sensitivity_summary_20260510.tsv`
- Figure: `/home/qiaosir/projects/compute_vit/thesis/figures/mixed_precision/fig_layer_sensitivity_20260510.png`

## Pilot sensitivity ranking

| Rank | Layer | Role | Stage | Mean acc drop (pp) | Mean loss delta | Static rank |
|---:|---|---|---|---:|---:|---:|
| 1 | `stages.3.blocks.0.mlp.fc2` | mlp_fc2 | stage_3 | 83.5938 ± 1.2807 | 8.046876 | 3 |
| 2 | `stages.3.blocks.0.mlp.fc1` | mlp_fc1 | stage_3 | 2.3438 ± 0.5167 | 0.085344 | 1 |
| 3 | `stages.2.blocks.2.mlp.fc1` | mlp_fc1 | stage_2 | 1.1068 ± 0.8807 | 0.052785 | 9 |
| 4 | `stages.2.blocks.0.mlp.fc1` | mlp_fc1 | stage_2 | 1.0417 ± 0.1128 | 0.034313 | 7 |
| 5 | `stages.2.blocks.3.mlp.fc1` | mlp_fc1 | stage_2 | 0.8464 ± 0.2983 | 0.022558 | 10 |
| 6 | `stages.2.blocks.1.mlp.fc1` | mlp_fc1 | stage_2 | 0.2604 ± 0.4066 | 0.040582 | 8 |
| 7 | `stages.3.blocks.0.attn.qkv` | attention_qkv | stage_3 | 0.0651 ± 0.9230 | -0.012254 | 5 |
| 8 | `stages.3.blocks.1.mlp.fc2` | mlp_fc2 | stage_3 | 0.0651 ± 0.1128 | -0.030324 | 4 |
| 9 | `stages.3.blocks.1.mlp.fc1` | mlp_fc1 | stage_3 | 0.0000 ± 0.5167 | 0.002723 | 2 |
| 10 | `stages.3.blocks.1.attn.qkv` | attention_qkv | stage_3 | -0.0651 ± 0.4915 | -0.002457 | 6 |

## Recommended next P1 maps

- Treat the highest positive-drop layers in this pilot as initial 8-bit/digital candidates only after a larger rerun confirms the ordering.
- Immediate next map to test: protect the top 10 static-ranked layers, then compare against a top-positive-drop-only map from this pilot.
- Do not promote this probe to thesis claim-bearing status until it is rerun across all 42 analog layers and a larger validation subset/full test split.

## GPU postcheck

```text
Sun May 10 16:12:19 2026
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 595.58.04              Driver Version: 596.21         CUDA Version: 13.2     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 5070 Ti     On  |   00000000:01:00.0  On |                  N/A |
|  0%   55C    P8             20W /  300W |     341MiB /  16303MiB |      1%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A             520      G   /Xwayland                             N/A      |
+-----------------------------------------------------------------------------------------+
```

## Remaining risks

- Only top 10 static-ranked layers were perturbed; lower-ranked layers may still be sensitive.
- The 512-image subset can exaggerate or hide small accuracy deltas.
- Single-layer D2D resampling isolates layer sensitivity but does not yet validate complete mixed-precision maps.
