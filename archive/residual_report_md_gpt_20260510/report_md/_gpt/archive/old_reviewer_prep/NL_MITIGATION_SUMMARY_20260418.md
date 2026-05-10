# NL Mitigation Summary

| Condition | Exists | Best / Mean acc (%) | Best epoch | Source |
|:--|:--:|--:|--:|:--|
| Severe NL baseline | yes | 27.716 |  | `v4_nl2_hat_eval_results_gpt.json` |
| MLP-only linear compensation | yes | 87.79 | 73 | `v4_nl2_mlp_linear_comp_train_results_gpt.json` |
| QKV-only linear compensation | yes | 18.72 | 2 | `v4_nl2_qkv_linear_comp_train_results_gpt.json` |
| All-analog linear compensation | yes | 87.49 | 59 | `v4_nl2_all_linear_comp_train_results_gpt.json` |

## Gradient diagnostic anchors

- MLP affected-grad cosine: `0.8150389939546585`
- MLP affected-grad norm ratio: `0.6712781248246112`
- QKV affected-grad cosine: `None`
- QKV affected-grad norm ratio: `None`
- All-analog affected-grad cosine: `None`
- All-analog affected-grad norm ratio: `None`

Interpretation: compare the finished mitigation runs against the severe NL baseline and the gradient-localization evidence before promoting any result into the manuscript.
