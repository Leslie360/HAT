 # A2.2: ConvNeXt-Tiny Full Pipeline Validation on CIFAR-10

## Experiment Matrix Results

| Exp | Config | Quant | C2C | D2D | Training | Best Acc | MC Mean±Std |
|:---:|:-------|:-----:|:---:|:---:|:--------:|:-------:|:-----------:|
| C1 | C1_FP32_baseline | FP32 | 0.0 | 0.0 | Standard | 90.74% | 90.74±0.00% |
| C2 | C2_4bit_no_noise | 16L | 0.0 | 0.0 | Standard | 90.69% | 90.69±0.00% |
| C3 | C3_4bit_noise_standard | 16L | 0.05 | 0.1 | Standard | 70.48% | 69.58±0.55% |
| C4 | C4_4bit_noise_HAT | 16L | 0.05 | 0.1 | HAT | 89.91% | 89.71±0.17% |
| C5 | C5_4bit_pessimistic_HAT | 16L | 0.1 | 0.2 | HAT | 88.13% | 87.68±0.14% |
| C6 | C6_6bit_noise_HAT | 64L | 0.05 | 0.1 | HAT | 89.62% | 89.48±0.14% |
| C7 | C7_4bit_HAT_ADC4 (ADC 4-bit) | 16L | 0.05 | 0.1 | HAT | 89.19% | 89.03±0.14% |
| C8 | C8_4bit_HAT_ADC6 (ADC 6-bit) | 16L | 0.05 | 0.1 | HAT | 89.13% | 88.88±0.14% |

## Key Comparisons

| Comparison | Δ Accuracy | Interpretation |
|:-----------|:----------:|:---------------|
| C1→C2 | -0.05% | Pure quantization loss |
| C1→C3 | -20.26% | Noise degradation vs FP32 baseline |
| C1→C4 | -0.83% | HAT recovery vs FP32 baseline |
| C2→C3 | -20.21% | Noise degradation vs quantized no-noise |
| C3→C4 | +19.43% | HAT recovery vs noisy standard training |
| C4→C5 | -1.78% | Pessimistic scenario |
| C4→C6 | -0.29% | Bit-width sensitivity (6-bit) |
| C4→C7 | -0.72% | ADC 4-bit extreme |
| C4→C8 | -0.78% | ADC 6-bit moderate |

## Figures

![ConvNeXt Accuracy Comparison](images_gpt/convnext_accuracy_comparison_gpt.png)

## C9: Retention Decay Experiment

Checkpoint provenance:

- Path: `checkpoints/C4_4bit_noise_HAT_best.pt`
- Source experiment: `C4_4bit_noise_HAT`
- Saved epoch: 197
- Best accuracy: 89.91%
- Planned epochs for source run: 200

Using the specified HAT-trained checkpoint, measuring accuracy after weight drift.

| Time (s) | Accuracy (MC 20 runs) |
|:--------:|:-------------------:|
| 0 | 89.66±0.15% |
| 1 | 86.07±0.17% |
| 10 | 84.30±0.18% |
| 100 | 84.23±0.19% |
| 1000 | 84.33±0.25% |
| 10000 | 84.28±0.19% |

Observation: retention clearly drops from `0s` to `10s`, then enters a narrow `~84.2%~84.3%` plateau. The `1000s` point is slightly above `100s`, but the difference is smaller than the MC uncertainty, so this should be interpreted as sampling noise rather than true recovery.

![ConvNeXt Retention Curve](images_gpt/convnext_retention_curve_gpt.png)
