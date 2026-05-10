# Local GPU Mixed-Precision Protection Full-Test Report — 20260510

## Evidence grade

- `full-test/provisional`: full CIFAR-10 test split, but still a protection-map inference probe rather than final fresh-instance protocol.
- No training was run; checkpoint and datasets were read-only.
- `freeze_topK_d2d` keeps the top-K full42-sensitive layers at checkpoint D2D while resampling every other analog layer to a fresh D2D instance.
- `freeze_top42_d2d` is a positive control equivalent to preserving all checkpoint D2D buffers.

## Protocol

- Checkpoint: `/home/qiaosir/projects/compute_vit/checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- Sensitivity ranking input: `/home/qiaosir/projects/compute_vit/thesis/results/mixed_precision/layer_sensitivity_full42_summary_20260510.tsv`
- Test split: 10000 CIFAR-10 images; seeds: [20260510, 20260511, 20260512]; batch size: 256.
- Standard analog config: sigma_d2d=0.1, sigma_c2c=0.05, n_states=16.

## GPU preflight

```text
Sun May 10 17:13:48 2026
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 595.58.04              Driver Version: 596.21         CUDA Version: 13.2     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 5070 Ti     On  |   00000000:01:00.0  On |                  N/A |
|  0%   47C    P8             19W /  300W |     348MiB /  16303MiB |      2%      Default |
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
| `source_checkpoint_d2d` | source | 0 | 91.9600 | 0.1970 | 0.0000 | 81.9600 |
| `fresh_all_analog` | fresh | 0 | 10.0000 | 0.0000 | -81.9600 | 0.0000 |
| `freeze_top10_d2d` | freeze | 10 | 22.4400 | 3.7435 | -69.5200 | 12.4400 |
| `freeze_top13_d2d` | freeze | 13 | 34.8100 | 3.0940 | -57.1500 | 24.8100 |
| `freeze_top20_d2d` | freeze | 20 | 65.9267 | 2.8793 | -26.0333 | 55.9267 |
| `freeze_top30_d2d` | freeze | 30 | 86.0633 | 0.2290 | -5.8967 | 76.0633 |
| `freeze_top42_d2d` | freeze | 42 | 91.9600 | 0.1970 | 0.0000 | 81.9600 |

## Outputs

- Rows: `/home/qiaosir/projects/compute_vit/thesis/results/mixed_precision/protection_map_fulltest_p1_20260510.tsv`
- Summary: `/home/qiaosir/projects/compute_vit/thesis/results/mixed_precision/protection_map_fulltest_p1_summary_20260510.tsv`
- Figure: `/home/qiaosir/projects/compute_vit/thesis/figures/mixed_precision/fig_protection_map_fulltest_p1_20260510.png`

## Interpretation

- Best non-source strategy in this validation: `freeze_top42_d2d` at 91.9600% mean accuracy.
- The rescue curve should be interpreted as a localization diagnostic: partial D2D preservation helps, but deployment-grade robustness still requires distribution-level training or much broader protection.
- Promote to claim-bearing only after a true fresh-instance protocol that samples multiple held-out arrays per strategy.

## GPU postcheck

```text
Sun May 10 17:21:52 2026
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 595.58.04              Driver Version: 596.21         CUDA Version: 13.2     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 5070 Ti     On  |   00000000:01:00.0  On |                  N/A |
|  0%   44C    P8             19W /  300W |     347MiB /  16303MiB |      1%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
```

## Runtime

- Elapsed seconds excluding setup: 469.37.
