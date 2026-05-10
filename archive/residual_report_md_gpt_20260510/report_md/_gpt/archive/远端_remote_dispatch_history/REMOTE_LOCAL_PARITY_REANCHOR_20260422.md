# Local Parity Re-Anchor (2026-04-22)

This note records the first local parity re-anchor after **both** of the following fixes landed:

1. config-sharing bug in `convert_to_hybrid()`
2. missing `nl` multiplier in the `LTP` first-order backward scale

## Probe set
All runs used:
- warm-start: `checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- `epochs=1`
- `batch_size=64`
- `num_workers=0`
- `dataset=cifar10`
- global severe-NL: `--nl-ltp 2.0 --nl-ltd -2.0`

## Results

| tag | group | SO2 | delta_g_eff | train_acc | test_acc |
|:--|:--|:--:|:--:|--:|--:|
| `j1d_historical_auto` | mlp | Y | `-1.0` (auto) | 82.88% | 46.75% |
| `j1d_literal_zero` | mlp | Y | `0.0` (literal) | 82.47% | 57.00% |
| `mlp_noso2_fixed` | mlp | N | none | 82.34% | 55.65% |
| `all_so2_auto` | all | Y | `-1.0` (auto) | 88.33% | 83.34% |

## Interpretation
1. The historical local `81.86%` MLP-protected anchor is no longer reproducible under corrected code.
2. The remote `~27%` collapse is also no longer the whole story under corrected code.
3. Under corrected local code, mixed-NL at epoch 0 currently lands in the **46–57%** range, depending on the exact SO2 / `delta_g_eff` setting.
4. `group=all` remains healthy (`83.34%`), which is directionally consistent with the remote parity-dissection result.

## Consequence
The old parity argument must be reclassified:
- pre-fix `27%`, `58%`, and `81%` anchor values are all contaminated by one or both source-level bugs
- future mixed-NL interpretation must start from this corrected local re-anchor, not from the historical local J1d number
