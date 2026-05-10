# Fresh-Instance Cadence Control

- Generated: `2026-04-17T21:09:55.614438`
- Protocol: `1 fresh D2D instances x 1 MC evaluations per instance on CIFAR-10 Tiny-ViT V4 checkpoints`

| Training mode | Train best acc (%) | Fresh-instance mean (%) | Cross-instance std (%) |
|:--|--:|--:|--:|
| fixed | 91.94 | 10.00 | 0.00 |
| epoch | 91.13 | 87.45 | 0.00 |
| batch | 65.87 | 66.17 | 0.00 |

## Interpretation

- `fixed` measures the paper-locked standard HAT checkpoint under fresh D2D instances.
- `epoch` measures the paper-locked Ensemble HAT checkpoint under the same protocol.
- `batch` is the new per-batch resampling control trained under the same V4 recipe and evaluated under the same fresh-instance protocol.
