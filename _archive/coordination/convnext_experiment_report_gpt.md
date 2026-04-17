# A2.2: ConvNeXt-Tiny Full Pipeline Validation on CIFAR-10

## Experiment Matrix Results

| Exp | Config | Quant | C2C | D2D | Training | Best Acc | MC Mean±Std |
|:---:|:-------|:-----:|:---:|:---:|:--------:|:-------:|:-----------:|
| C2 | C2_4bit_no_noise | 16L | 0.0 | 0.0 | Standard | 90.69% | 90.69±0.00% |
| C3 | C3_4bit_noise_standard | 16L | 0.05 | 0.1 | Standard | 70.48% | 69.58±0.55% |

## Key Comparisons

| Comparison | Δ Accuracy | Interpretation |
|:-----------|:----------:|:---------------|
| C2→C3 | -20.21% | Noise degradation |
