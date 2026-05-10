# A2.2 / Task 21: ConvNeXt-Tiny Validation on cifar10

## Experiment Matrix Results

| Exp | Config | Quant | C2C | D2D | Training | Best Acc | MC Mean±Std |
|:---:|:-------|:-----:|:---:|:---:|:--------:|:-------:|:-----------:|
| C4 | C4_4bit_noise_HAT | 16L | 0.05 | 0.1 | HAT | 91.98% | 91.91±0.08% |

## Key Comparisons

| Comparison | Δ Accuracy | Interpretation |
|:-----------|:----------:|:---------------|

## C9: Retention Decay Experiment

Checkpoint provenance:

- Path: `checkpoints/C4_4bit_noise_HAT_best.pt`
- Source experiment: `C4_4bit_noise_HAT`
- Saved epoch: 197
- Best accuracy: 89.91%
- Planned epochs for source run: 200

Using the specified HAT-trained checkpoint, measuring accuracy after weight drift.

| Time (s) | Accuracy (MC 1 runs) |
|:--------:|:-------------------:|
| 0 | 89.58±0.00% |
| 1 | 85.78±0.00% |
