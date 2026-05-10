# A2.2 / Task 21: ConvNeXt-Tiny Validation on cifar100

## Experiment Matrix Results

| Exp | Config | Quant | C2C | D2D | Training | Best Acc | MC Mean±Std |
|:---:|:-------|:-----:|:---:|:---:|:--------:|:-------:|:-----------:|
| C1 | C1_FP32_baseline | FP32 | 0.0 | 0.0 | Standard | 64.12% | 64.12±0.00% |
| C3 | C3_4bit_noise_standard | 16L | 0.05 | 0.1 | Standard | 23.86% | 23.65±0.25% |
| C4 | C4_4bit_noise_HAT | 16L | 0.05 | 0.1 | HAT | 60.54% | 60.15±0.11% |

## Key Comparisons

| Comparison | Δ Accuracy | Interpretation |
|:-----------|:----------:|:---------------|
| C1→C3 | -40.26% | Noise degradation vs FP32 baseline |
| C1→C4 | -3.58% | HAT recovery vs FP32 baseline |
| C3→C4 | +36.68% | HAT recovery vs noisy standard training |
