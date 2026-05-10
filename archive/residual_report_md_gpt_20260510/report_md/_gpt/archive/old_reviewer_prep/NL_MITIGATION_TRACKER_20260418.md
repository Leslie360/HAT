# NL Mitigation Tracker — 2026-04-18

## Objective

Stress-test the current manuscript claim that severe nonlinear write
(`NL=2.0`) is a recovery bottleneck under the present gradient-scaling recipe,
and determine whether the failure is global or path-localized.

## Locked baseline

- Canonical severe point: `NL=2.0`
- Paper-locked anchor: `27.72 ± 0.82%`
- Mechanistic diagnostic already landed:
  - dominant backward-surrogate distortion localized to the `MLP` analog path
  - `QKV` and other attention-side analog blocks did not show the same gradient distortion signature

## Finished training controls

| Condition | Best acc (%) | Best epoch | Final acc (%) | Artifact |
|:--|--:|--:|--:|:--|
| Severe NL baseline | 27.72 | n/a | n/a | `report_md/_gpt/json_gpt/v4_nl2_hat_eval_results_gpt.json` |
| MLP-only linear compensation | 87.79 | 73 | 86.22 | `report_md/_gpt/json_gpt/v4_nl2_mlp_linear_comp_train_results_gpt.json` |
| QKV-only linear compensation | 18.72 | 2 | 10.15 | `report_md/_gpt/json_gpt/v4_nl2_qkv_linear_comp_train_results_gpt.json` |
| All-analog linear compensation | 87.49 | 59 | 84.81 | `report_md/_gpt/json_gpt/v4_nl2_all_linear_comp_train_results_gpt.json` |

## Current readout

- `MLP-only` recovers almost the entire severe-NL gap.
- `QKV-only` collapses, so the mitigation is **not** explained by protecting attention-side projections alone.
- `All-analog` does not materially outperform `MLP-only`, which strengthens the claim that the present failure is concentrated in the `MLP` path rather than uniformly distributed across all analog blocks.

## Fresh-instance controls already completed

| Training mode | Train best acc (%) | Fresh-instance mean (%) | Cross-instance std (%) | Artifact |
|:--|--:|--:|--:|:--|
| fixed | 91.94 | 10.00 | 0.00 | `report_md/_gpt/json_gpt/fresh_instance_cadence_control.json` |
| epoch | 91.13 | 86.33 | 1.61 | same |
| batch | 90.30 | 89.48 | 0.36 | same |

## Fresh-instance transfer checks

| Condition | Train best acc (%) | Fresh-instance mean (%) | Cross-instance std (%) | Status |
|:--|--:|--:|--:|:--|
| `MLP-only` linear compensation | 87.79 | 32.12 | 7.72 | complete |
| `QKV-only` linear compensation | 18.72 | 10.01 | 0.10 | complete |
| `all-linear` compensation | 87.49 | 32.60 | 9.18 | complete |

Interpretation at this stage:

- `MLP-only` is a strong **source-domain** rescue but not a strong **fresh-instance** rescue.
- `QKV-only` remains collapsed under both source-domain and fresh-instance evaluation.
- `all-linear` improves source-domain accuracy but still reaches only `32.60 ± 9.18%` under fresh-instance transfer, so broader linearization does not convert the severe-NL ablation into a deployment-grade mitigation.

## Immediate editorial implication

- The main manuscript should continue to frame severe-NL as a **baseline-recipe bottleneck**, not as a fundamental device limit.
- The strongest compact supplementary story is now:
  - severe baseline
  - `MLP-only` rescue
  - `QKV-only` collapse
  - `all-linear` upper-bound control
- The fresh-instance picture is now complete enough to support supplementary-only placement:
  none of the severe-NL linearization lanes reproduce canonical Ensemble-HAT transfer.
