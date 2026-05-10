# Fresh-Instance NL Mitigation Controls

- Generated: `2026-04-19T00:23:11.967338`
- Protocol: `10 fresh D2D instances x 5 MC evaluations per instance on CIFAR-10 Tiny-ViT V4 severe-NL mitigation checkpoints`

| Condition | Train best acc (%) | Fresh-instance mean (%) | Cross-instance std (%) |
|:--|--:|--:|--:|
| all | 87.49 | 32.60 | 9.18 |

## Interpretation

- `mlp` tests whether protecting only the MLP analog path restores cross-instance robustness under severe nonlinear write.
- `qkv` is the negative control against the MLP-localization hypothesis.
- `all` is the upper-bound control that linearizes every analog block while keeping the severe-NL global setting elsewhere in the recipe.
