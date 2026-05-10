# Fresh-Instance Cadence Control

- Generated: `2026-04-18T13:00:16.087887`
- Protocol: `10 fresh D2D instances x 5 MC evaluations per instance on CIFAR-10 Tiny-ViT V4 checkpoints`

| Training mode | Train best acc (%) | Fresh-instance mean (%) | Cross-instance std (%) |
|:--|--:|--:|--:|
| fixed | 91.94 | 10.00 | 0.00 |
| epoch | 91.13 | 86.33 | 1.61 |
| batch | 90.30 | 89.48 | 0.36 |

## Interpretation

- `fixed` measures the paper-locked standard HAT checkpoint under fresh D2D instances.
- `epoch` measures the paper-locked Ensemble HAT checkpoint under the same protocol.
- `batch` is the new per-batch resampling control trained under the same V4 recipe and evaluated under the same fresh-instance protocol.
