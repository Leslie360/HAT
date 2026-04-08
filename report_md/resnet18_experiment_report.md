# A2.1: ResNet-18 Full Pipeline Validation on CIFAR-10

## Experiment Matrix Results

| Exp | Config | Quant | C2C | D2D | Training | Best Acc | MC Mean±Std |
|:---:|:-------|:-----:|:---:|:---:|:--------:|:-------:|:-----------:|
| R1 | R1_FP32_baseline | FP32 | 0.0 | 0.0 | Standard | 95.46% | 95.46±0.00% |
| R2 | R2_4bit_no_noise | 16L | 0.0 | 0.0 | Standard | 94.12% | 94.12±0.00% |
| R3 | R3_4bit_noise_standard | 16L | 0.05 | 0.1 | Standard | 16.48% | 17.30±0.26% |
| R4 | R4_4bit_noise_HAT | 16L | 0.05 | 0.1 | HAT | 90.37% | 89.92±0.11% |
| R5 | R5_4bit_pessimistic_HAT | 16L | 0.1 | 0.2 | HAT | 77.92% | 76.50±0.80% |
| R6 | R6_6bit_noise_HAT | 64L | 0.05 | 0.1 | HAT | 91.20% | 90.90±0.19% |

## Key Comparisons

| Comparison | Δ Accuracy | Interpretation |
|:-----------|:----------:|:---------------|
| R1→R2 | -1.34% | Pure quantization loss |
| R2→R3 | -77.64% | Noise degradation |
| R3→R4 | +73.89% | HAT recovery (core result) |
| R4→R5 | -12.45% | Pessimistic scenario survival |
| R4→R6 | +0.83% | Bit-width sensitivity |
