# ConvNeXt C9 Retention Record (GPT)

Generated at `2026-04-04 17:36 +08`.

Note: no dedicated standalone tee log was preserved when `C9` was executed during the final ConvNeXt consolidation step. This report is reconstructed from the final GPT-scoped consolidated outputs so that `C9` can be referenced directly without re-reading the full package.

## Sources

- `report_md/_gpt/json_gpt/convnext_full_results_gpt.json`
- `report_md/_gpt/convnext_full_report_gpt.md`

## Checkpoint Provenance

- Path: `checkpoints/C4_4bit_noise_HAT_best.pt`
- Source experiment: `C4_4bit_noise_HAT`
- Saved epoch: `197`
- Best accuracy: `89.91%`
- Planned epochs for source run: `200`

## Results

| Time (s) | Accuracy (MC 20 runs) |
|:--------:|:---------------------:|
| 0 | 89.66+-0.15% |
| 1 | 86.07+-0.17% |
| 10 | 84.30+-0.18% |
| 100 | 84.23+-0.19% |
| 1000 | 84.33+-0.25% |
| 10000 | 84.28+-0.19% |

## Observation

Retention drops clearly from `0s` to `10s`, then settles into a narrow `~84.2%~84.3%` plateau. The `1000s` point is slightly above `100s`, but the gap is smaller than the Monte Carlo uncertainty, so it should be treated as sampling noise rather than real recovery.

## Figure

![ConvNeXt Retention Curve](images_gpt/convnext_retention_curve_gpt.png)
