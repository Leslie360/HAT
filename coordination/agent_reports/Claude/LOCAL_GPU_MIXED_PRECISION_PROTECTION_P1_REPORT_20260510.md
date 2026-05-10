# Local GPU Mixed-Precision Protection P1 Report — 20260510

## Evidence grade

- `pilot/provisional`: this is a subset upper-bound design probe, not claim-bearing validation.
- No training was run; checkpoint and datasets were read-only.
- `freeze_topK_d2d` keeps the top-K sensitive layers at checkpoint D2D while resampling all other analog layers.
- `noiseless_topK_hp_upper` resamples all layers, then makes top-K layers noiseless and 256-state as an optimistic protected/digital upper bound.

## Protocol

- Checkpoint: `/home/qiaosir/projects/compute_vit/checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- Sensitivity ranking input: `/home/qiaosir/projects/compute_vit/thesis/results/mixed_precision/layer_sensitivity_full42_summary_20260510.tsv`
- Subset: 2048 CIFAR-10 test images; seeds: [20260510, 20260511, 20260512]; batch size: 256.
- Standard analog config: sigma_d2d=0.1, sigma_c2c=0.05, n_states=16.
- Protected high-precision upper-bound n_states: 256.

## GPU preflight

```text
Sun May 10 17:02:26 2026
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 595.58.04              Driver Version: 596.21         CUDA Version: 13.2     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 5070 Ti     On  |   00000000:01:00.0  On |                  N/A |
|  0%   50C    P8             19W /  300W |     351MiB /  16303MiB |      2%      Default |
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

## Summary

| Strategy | Kind | K | Mean acc (%) | Std | Δ vs source (pp) | Gain vs fresh (pp) |
|---|---|---:|---:|---:|---:|---:|
| `source_checkpoint_d2d` | source | 0 | 92.5781 | 0.5098 | 0.0000 | 83.6914 |
| `fresh_all_analog` | fresh | 0 | 8.8867 | 0.0000 | -83.6914 | 0.0000 |
| `freeze_top1_d2d` | freeze | 1 | 9.2936 | 0.6221 | -83.2845 | 0.4069 |
| `freeze_top2_d2d` | freeze | 2 | 9.7656 | 1.1262 | -82.8125 | 0.8789 |
| `freeze_top5_d2d` | freeze | 5 | 10.0911 | 0.9034 | -82.4870 | 1.2044 |
| `freeze_top10_d2d` | freeze | 10 | 26.2207 | 3.6159 | -66.3574 | 17.3340 |
| `freeze_top13_d2d` | freeze | 13 | 39.3392 | 6.1613 | -53.2389 | 30.4525 |
| `noiseless_top10_hp_upper` | noiseless_hp | 10 | 8.8867 | 0.0000 | -83.6914 | 0.0000 |
| `noiseless_top13_hp_upper` | noiseless_hp | 13 | 8.8867 | 0.0000 | -83.6914 | 0.0000 |

## Outputs

- Rows: `/home/qiaosir/projects/compute_vit/thesis/results/mixed_precision/protection_map_pilot_p1_20260510.tsv`
- Summary: `/home/qiaosir/projects/compute_vit/thesis/results/mixed_precision/protection_map_pilot_p1_summary_20260510.tsv`
- Figure: `/home/qiaosir/projects/compute_vit/thesis/figures/mixed_precision/fig_protection_map_pilot_p1_20260510.png`

## Interpretation

- Best non-source strategy in this pilot: `freeze_top13_d2d` at 39.3392% mean accuracy.
- Treat any rescue pattern as a candidate-selection signal only; promote only after full-test or fresh-instance rerun.

## GPU postcheck

```text
Sun May 10 17:05:09 2026
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
```

## Runtime

- Elapsed seconds excluding setup: 128.08.
