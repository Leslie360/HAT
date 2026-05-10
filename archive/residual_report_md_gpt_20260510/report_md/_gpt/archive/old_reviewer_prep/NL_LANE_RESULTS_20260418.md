# NL Lane Results — 2026-04-18

## Scope

This memo freezes the current severe-`NL=2.0` mitigation lanes for Tiny-ViT `V4`
under the present gradient-scaling recipe. It is intended to support the
Claude-side placement decision about what belongs in the main paper, what
belongs in the supplement, and what should stay rebuttal-only.

## Source-domain training lanes

| Lane | Status | Best acc (%) | Best epoch | Final acc (%) | Checkpoint | Log | Interpretation |
|:--|:--|--:|--:|--:|:--|:--|:--|
| Severe NL baseline | complete | 27.72 | n/a | n/a | `report_md/_gpt/json_gpt/v4_nl2_hat_eval_results_gpt.json` | manuscript-locked eval artifact | Paper-locked anchor for the current severe-NL claim. |
| MLP-only linear compensation | complete | 87.79 | 73 | 86.22 | `checkpoints/_gpt/nl_mitigation/v4_nl2_mlp_linear_comp/V4_hybrid_standard_noise_hat_nl2_mlp_linear_comp_best.pt` | `logs/_gpt/train_tinyvit_v4_nl2_mlp_linear_comp_TESTDEBUG.log` | Strong rescue. This is the key positive result. |
| QKV-only linear compensation | complete | 18.72 | 2 | 10.15 | `checkpoints/_gpt/nl_mitigation/v4_nl2_qkv_linear_comp/V4_hybrid_standard_noise_hat_nl2_qkv_linear_comp_best.pt` | `logs/_gpt/train_tinyvit_v4_nl2_qkv_linear_comp_20260418_130728_queue_qkv.log` | Collapse. This is the negative control against a generic “attention-side” explanation. |
| All-linear compensation | complete | 87.49 | 59 | 84.81 | `checkpoints/_gpt/nl_mitigation/v4_nl2_all_linear_comp/V4_hybrid_standard_noise_hat_nl2_all_linear_comp_best.pt` | `logs/_gpt/train_tinyvit_v4_nl2_all_linear_comp_20260418_144254_queue_all.log` | Upper-bound control. It does not materially outperform MLP-only. |
| Attn-proj-only linear compensation | stopped @ ep 54 (timeout) | 18.86 | 0 | ~10.25 | `checkpoints/_gpt/nl_mitigation/v4_nl2_attn_proj_linear_comp/V4_hybrid_standard_noise_hat_nl2_attn_proj_linear_comp_best.pt` | `logs/_gpt/train_tinyvit_v4_nl2_attn_proj_linear_comp_20260418_1700.log` | Collapse. Mirrors QKV-only pattern; confirms entire attention side is structurally required. |

## Canonical fresh-instance transfer baseline

| Condition | Train best acc (%) | Fresh-instance mean (%) | Cross-instance std (%) | Artifact |
|:--|--:|--:|--:|:--|
| fixed | 91.94 | 10.00 | 0.00 | `report_md/_gpt/json_gpt/fresh_instance_cadence_control.json` |
| epoch | 91.13 | 86.33 | 1.61 | same |
| batch | 90.30 | 89.48 | 0.36 | same |

## Severe-NL fresh-instance checks

| Lane | Train best acc (%) | Fresh-instance mean (%) | Cross-instance std (%) | Status |
|:--|--:|--:|--:|:--|
| `MLP-only` linear compensation | 87.79 | 32.12 | 7.72 | complete |
| `QKV-only` linear compensation | 18.72 | 10.01 | 0.10 | complete |
| `all-linear` compensation | 87.49 | 32.60 | 9.18 | complete |

## Current mechanistic readout

- `MLP-only` recovers from the severe-NL anchor (`27.72%`) to `87.79%`.
- `QKV-only` fails (`18.72%` best, `10.15%` final), which argues against a
  generic attention-side explanation.
- `All-linear` reaches `87.49%`, essentially matching `MLP-only` rather than
  materially exceeding it.
- `MLP-only` does **not** inherit the canonical Ensemble-HAT transfer behavior:
  its fresh-instance mean is only `32.12 ± 7.72%`.
- `QKV-only` remains collapsed under fresh-instance transfer as well
  (`10.01 ± 0.10%`).
- `all-linear` also fails to restore deployment-grade transfer
  (`32.60 ± 9.18%`), despite its strong source-domain accuracy.
- This pattern is consistent with the earlier gradient-distortion diagnostic:
  the present severe-NL failure is localized primarily to the `MLP` analog path.

## Immediate editorial implication

- The severe-NL statement in the main manuscript should remain framed as a
  **baseline-recipe bottleneck**, not as a fundamental device limit.
- The strongest compact supplementary story is now:
  `baseline severe NL` vs `MLP-only rescue` vs `QKV-only collapse` vs `all-linear upper bound`.
- Because both `MLP-only` and `all-linear` gains are largely source-domain and
  not strong fresh-instance results, the mitigation story is better kept in the
  supplement than promoted to a new main-text contribution.
