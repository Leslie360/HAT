# P13 AIHWKIT Full CIFAR-10 Benchmark

| Framework | Regime | Accuracy |
|:--|:--|:--|
| PyTorch digital | FP32 baseline (cuda) | `95.46%` |
| AIHWKIT | shared regime (cpu, 10 runs, quant=4, adc=8, σ_C2C=0.05, σ_D2D=0.1) | `90.08 ± 0.21%` |

| Item | Value |
|:--|:--|
| Checkpoint | `/home/qiaosir/projects/compute_vit/checkpoints/R1_FP32_baseline_best.pt` |
| Checkpoint epoch | `179` |
| Checkpoint best acc | `95.46%` |
| Effective test samples | `10000` |
| Requested test-samples arg | `0` |
| Batch size | `128` |
| Wall clock | `11358.9s` |
| Delta (analog - digital) | `-5.38%` |
