# ImageNet Zero-Shot Analog Deployment Results (GPT)

- Validation directory: `data/tiny-imagenet-200/val`
- Evaluated samples: `1000`

| Condition | Hybrid | Noise | Accuracy | Checkpoint |
|:----------|:------:|:-----:|:---------|:-----------|
| digital_fp32_pretrained | no | off | 0.00 +/- 0.00% (1 runs) | `timm pretrained` |
| hybrid_quant_only | yes | off | 0.00 +/- 0.00% (1 runs) | `timm pretrained` |
| hybrid_standard_noise | yes | on | 0.00 +/- 0.00% (10 runs) | `timm pretrained` |

## Notes

- `digital_fp32_pretrained` is the reference timm-pretrained Tiny-ViT baseline on ImageNet-1k.
- `hybrid_quant_only` measures zero-shot analog deployment with quantization and scale recovery but no device noise.
- `hybrid_standard_noise` adds standard organic noise (5% C2C, 10% D2D) without ImageNet HAT training.
- `hybrid_hat_checkpoint` is included only when a compatible 1000-class HAT checkpoint is provided.
- Optional `--device-profile-json` lets the same ImageNet path reuse in-house measured device parameters.

