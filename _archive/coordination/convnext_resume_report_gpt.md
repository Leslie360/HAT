# A2.2: ConvNeXt-Tiny Full Pipeline Validation on CIFAR-10

## Experiment Matrix Results

| Exp | Config | Quant | C2C | D2D | Training | Best Acc | MC Mean±Std |
|:---:|:-------|:-----:|:---:|:---:|:--------:|:-------:|:-----------:|
| C5 | C5_4bit_pessimistic_HAT | 16L | 0.1 | 0.2 | HAT | 88.13% | 87.68±0.14% |
| C6 | C6_6bit_noise_HAT | 64L | 0.05 | 0.1 | HAT | 89.62% | 89.48±0.14% |
| C7 | C7_4bit_HAT_ADC4 (ADC 4-bit) | 16L | 0.05 | 0.1 | HAT | 89.19% | 89.03±0.14% |
| C8 | C8_4bit_HAT_ADC6 (ADC 6-bit) | 16L | 0.05 | 0.1 | HAT | 89.13% | 88.88±0.14% |

## Key Comparisons

| Comparison | Δ Accuracy | Interpretation |
|:-----------|:----------:|:---------------|
