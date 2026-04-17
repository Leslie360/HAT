# Attention Visualization Results (GPT)

- Target layer: `stages.3.blocks.0.attn`
- Main figure: `paper/figures/fig_attention_maps.png`
- Difference figure: `paper/figures/fig_attention_differences.png`

| Sample idx | Label | V1 pred | V3 pred | V4 pred | V6 pred |
|-----------:|:------|:--------|:--------|:--------|:--------|
| 0 | cat | cat | truck | cat | cat |
| 23 | truck | truck | truck | truck | cat |
| 37 | automobile | truck | truck | truck | dog |

## Notes

- Default paper samples use fixed CIFAR-10 indices `[0, 23, 37]` for reproducibility.
- Heatmaps are generated from head-averaged attention after softmax.
- The default aggregation averages over all query tokens to highlight globally attended spatial regions.
- Difference panels use absolute deviation relative to the V1 digital baseline.

