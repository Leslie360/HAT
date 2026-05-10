# Tiny-ViT Noise Diagnostic (GPT)

- Generated: `2026-04-05T13:29:51`
- Device: `cuda`
- Eval runs: `10`
- Target noise: `sigma_c2c=0.05`, `sigma_d2d=0.1`

## Condition Summary

| Condition | Experiment | Resample D2D | Accuracy | mean|D2D| | mean std(D2D) |
|:----------|:-----------|:-------------|:---------|------:|--------------:|
| V2_current_path | V2 | False | 97.39 +/- 0.00% | 0.000000 | 0.000000 |
| V2_resampled_d2d | V2 | True | 97.39 +/- 0.00% | 0.719626 | 0.901811 |
| V4_reference | V4 | False | 91.73 +/- 0.18% | 0.718030 | 0.899681 |

## Representative Layer Diagnostics

### V2_current_path

| Layer | Noise/weight | Noise/effective-weight | D2D std (G) | C2C std (G) | Scale factor |
|:------|-------------:|-----------------------:|------------:|------------:|------------:|
| patch_embed.conv1.conv | 0.3101 | 0.3074 | 0.000000 | 0.447384 | 0.063178 |
| stages.1.blocks.0.attn.qkv | 0.4546 | 0.4479 | 0.000000 | 0.449355 | 0.099355 |
| stages.3.blocks.1.mlp.fc2 | 0.7281 | 0.7007 | 0.000000 | 0.450132 | 0.165858 |

### V2_resampled_d2d

| Layer | Noise/weight | Noise/effective-weight | D2D std (G) | C2C std (G) | Scale factor |
|:------|-------------:|-----------------------:|------------:|------------:|------------:|
| patch_embed.conv1.conv | 0.7285 | 0.7222 | 0.959054 | 0.464455 | 0.063178 |
| stages.1.blocks.0.attn.qkv | 1.0149 | 0.9999 | 0.895455 | 0.450286 | 0.099355 |
| stages.3.blocks.1.mlp.fc2 | 1.6287 | 1.5674 | 0.900843 | 0.450071 | 0.165858 |

### V4_reference

| Layer | Noise/weight | Noise/effective-weight | D2D std (G) | C2C std (G) | Scale factor |
|:------|-------------:|-----------------------:|------------:|------------:|------------:|
| patch_embed.conv1.conv | 0.6025 | 0.5995 | 0.882724 | 0.450291 | 0.078133 |
| stages.1.blocks.0.attn.qkv | 0.9035 | 0.8922 | 0.904621 | 0.451074 | 0.099828 |
| stages.3.blocks.1.mlp.fc2 | 1.7166 | 1.6453 | 0.898736 | 0.450718 | 0.173856 |

## Notes

- `V2_current_path` mimics the pre-fix `run_noise_sweep.py` behavior: config sigmas are updated but D2D buffers are not re-sampled.
- `V2_resampled_d2d` forces D2D re-sampling after changing `sigma_d2d` and is the correctness check requested by Claude.
- `V4_reference` uses the HAT checkpoint under the same target noise setting as a reference point.
