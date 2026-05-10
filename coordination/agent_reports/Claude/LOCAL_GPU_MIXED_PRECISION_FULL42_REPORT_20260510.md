# Local GPU Mixed-Precision Full-42 Report — 20260510

## Evidence grade

- `pilot/provisional`: full 42 analog layers were probed on a 512-image CIFAR-10 test subset, not a final claim-bearing validation.
- No training was run; checkpoint and dataset payloads were read-only.

## Method

- Baseline keeps checkpoint-loaded D2D buffers and V4 noise settings.
- Perturbation resamples one target layer D2D buffer at a time; all other analog layers are restored to checkpoint D2D.
- Seeds: [20260510, 20260511, 20260512]; sigma_d2d=0.1; sigma_c2c=0.05; subset_size=512.

## GPU preflight

```text
Sun May 10 16:30:03 2026
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 595.58.04              Driver Version: 596.21         CUDA Version: 13.2     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 5070 Ti     On  |   00000000:01:00.0  On |                  N/A |
|  0%   52C    P8             20W /  300W |     345MiB /  16303MiB |      2%      Default |
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

## Inputs and outputs

- Checkpoint: `/home/qiaosir/projects/compute_vit/checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- Checkpoint metadata: epoch=99, best_epoch=99, best_acc=91.94, dataset=cifar10
- Sensitivity rows: `/home/qiaosir/projects/compute_vit/thesis/results/mixed_precision/layer_sensitivity_full42_20260510.tsv`
- Sensitivity summary: `/home/qiaosir/projects/compute_vit/thesis/results/mixed_precision/layer_sensitivity_full42_summary_20260510.tsv`
- Figure: `/home/qiaosir/projects/compute_vit/thesis/figures/mixed_precision/fig_layer_sensitivity_full42_20260510.png`

## Baseline reproduction gate

| Seed | Baseline loss | Baseline acc (%) |
|---:|---:|---:|
| 20260510 | 0.338983 | 93.7500 |
| 20260511 | 0.364759 | 92.7734 |
| 20260512 | 0.472269 | 91.2109 |

- Mean baseline subset accuracy: 92.5781%.

## Top 15 sensitivity ranking

| Rank | Layer | Role | Stage | Mean acc drop (pp) | Mean loss delta | Arrays |
|---:|---|---|---|---:|---:|---:|
| 1 | `stages.3.blocks.0.mlp.fc2` | mlp_fc2 | stage_3 | 83.5938 ± 1.2807 | 8.046876 | 60 |
| 2 | `stages.1.blocks.1.mlp.fc2` | mlp_fc2 | stage_1 | 26.2370 ± 14.3290 | 1.865661 | 8 |
| 3 | `stages.2.blocks.5.mlp.fc2` | mlp_fc2 | stage_2 | 9.1146 ± 5.0417 | 0.516524 | 20 |
| 4 | `stages.2.blocks.4.mlp.fc1` | mlp_fc1 | stage_2 | 7.9427 ± 1.3295 | 0.330807 | 20 |
| 5 | `stages.2.blocks.2.mlp.fc2` | mlp_fc2 | stage_2 | 3.1250 ± 0.5167 | 0.154214 | 20 |
| 6 | `stages.3.blocks.0.mlp.fc1` | mlp_fc1 | stage_3 | 2.3438 ± 0.5167 | 0.085344 | 60 |
| 7 | `stages.1.blocks.1.mlp.fc1` | mlp_fc1 | stage_1 | 1.6276 ± 0.4066 | 0.080184 | 8 |
| 8 | `stages.1.blocks.0.mlp.fc1` | mlp_fc1 | stage_1 | 1.4974 ± 0.2255 | 0.085573 | 8 |
| 9 | `stages.2.blocks.2.mlp.fc1` | mlp_fc1 | stage_2 | 1.1068 ± 0.8807 | 0.052785 | 20 |
| 10 | `stages.2.blocks.0.mlp.fc2` | mlp_fc2 | stage_2 | 1.0417 ± 0.4066 | 0.069203 | 20 |
| 11 | `stages.2.blocks.1.mlp.fc2` | mlp_fc2 | stage_2 | 1.0417 ± 0.1128 | 0.047063 | 20 |
| 12 | `stages.2.blocks.0.mlp.fc1` | mlp_fc1 | stage_2 | 1.0417 ± 0.1128 | 0.034313 | 20 |
| 13 | `stages.2.blocks.3.mlp.fc1` | mlp_fc1 | stage_2 | 0.8464 ± 0.2983 | 0.022558 | 20 |
| 14 | `stages.2.blocks.0.attn.qkv` | attention_qkv | stage_2 | 0.6510 ± 0.9021 | 0.060285 | 16 |
| 15 | `stages.2.blocks.3.attn.qkv` | attention_qkv | stage_2 | 0.6510 ± 0.2255 | 0.051195 | 16 |

## Recommended P1 mixed-precision candidates

- Protect top positive-drop outliers first: especially any layer with multi-point or catastrophic drop under D2D resample.
- Compare two maps next: top-10-by-full42-sensitivity protected vs top-30%-by-full42-sensitivity protected, with the rest kept at 4-bit PCM.
- Rerun on a larger subset or full test split before promoting any ranking to thesis claim-bearing evidence.

## GPU postcheck

```text
Sun May 10 16:32:54 2026
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 595.58.04              Driver Version: 596.21         CUDA Version: 13.2     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 5070 Ti     On  |   00000000:01:00.0  On |                  N/A |
|  0%   42C    P8             19W /  300W |     347MiB /  16303MiB |      1%      Default |
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

## Runtime

- Probe elapsed seconds excluding setup: 72.02.

## Remaining risks

- 512-image subset may overstate single-layer effects.
- Single-layer perturbation does not yet validate complete mixed-precision maps.
- The catastrophic sensitivity of individual layers should be confirmed on full test split before being used as a final design rule.
