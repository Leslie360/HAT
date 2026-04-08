# A2.2: ConvNeXt-Tiny Full Pipeline Validation on CIFAR-10

## Experiment Matrix Results

| Exp | Config | Quant | C2C | D2D | Training | Best Acc | MC Mean±Std |
|:---:|:-------|:-----:|:---:|:---:|:--------:|:-------:|:-----------:|
| C1 | C1_FP32_baseline | FP32 | 0.0 | 0.0 | Standard | 47.89% | 47.89±0.00% |

## Key Comparisons

| Comparison | Δ Accuracy | Interpretation |
|:-----------|:----------:|:---------------|

## C9: Retention Decay Experiment

Using C4 (HAT-trained) model, measuring accuracy after weight drift.

| Time (s) | Accuracy (MC 5 runs) |
|:--------:|:-------------------:|
| 0 | 9.91±0.23% |
| 1 | 9.99±0.24% |
| 10 | 9.91±0.17% |
| 100 | 10.08±0.17% |
| 1000 | 10.09±0.22% |
