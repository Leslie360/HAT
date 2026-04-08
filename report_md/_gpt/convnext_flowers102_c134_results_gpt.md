# A2.2 / Task 21: ConvNeXt-Tiny Validation on flowers102

## Experiment Matrix Results

| Exp | Config | Quant | C2C | D2D | Training | Best Acc | MC Mean±Std |
|:---:|:-------|:-----:|:---:|:---:|:--------:|:-------:|:-----------:|
| C1 | C1_FP32_baseline | FP32 | 0.0 | 0.0 | Standard | 33.22% | 33.22±0.00% |
| C3 | C3_4bit_noise_standard | 16L | 0.05 | 0.1 | Standard | 3.79% | 1.57±0.83% |
| C4 | C4_4bit_noise_HAT | 16L | 0.05 | 0.1 | HAT | 3.35% | 2.03±0.68% |

## Key Comparisons

| Comparison | Δ Accuracy | Interpretation |
|:-----------|:----------:|:---------------|
| C1→C3 | -29.44% | Noise degradation vs FP32 baseline |
| C1→C4 | -29.87% | HAT recovery vs FP32 baseline |
| C3→C4 | -0.44% | HAT recovery vs noisy standard training |
