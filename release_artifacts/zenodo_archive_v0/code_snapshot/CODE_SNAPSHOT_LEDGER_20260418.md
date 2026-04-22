# Code Snapshot Ledger — 2026-04-18

This ledger lists the repository files that the compiled manuscript currently depends on, together with the `.tex` line that anchors the dependency.

## Main manuscript quantitative figures

| File | Role | Manuscript cite |
|:--|:--|:--|
| `paper/plot_paper_figures.py` | Generator for `fig4_accuracy_comparison` | `paper/latex_gpt/sections/05_results.tex:17` |
| `report_md/_gpt/json_gpt/tinyvit_v1_results_gpt.json` | Fig. 4 Tiny-ViT FP32 (`V1`, CIFAR-10) | `paper/latex_gpt/sections/05_results.tex:17` |
| `report_md/_gpt/json_gpt/tinyvit_v2v7_results_gpt.json` | Fig. 4 Tiny-ViT (`V3/V4`, CIFAR-10) | `paper/latex_gpt/sections/05_results.tex:17` |
| `report_md/_gpt/json_gpt/tinyvit_cifar100_v134_results_gpt.json` | Fig. 4 Tiny-ViT (`V1/V3/V4`, CIFAR-100) | `paper/latex_gpt/sections/05_results.tex:17` |
| `report_md/_gpt/json_gpt/tinyvit_flowers102_v134_results_gpt.json` | Fig. 4 Tiny-ViT (`V1/V3/V4`, Flowers-102) | `paper/latex_gpt/sections/05_results.tex:17` |
| `report_md/_gpt/json_gpt/convnext_full_results_gpt.json` | Fig. 4 ConvNeXt (`C1/C3/C4`, CIFAR-10) | `paper/latex_gpt/sections/05_results.tex:17` |
| `report_md/_gpt/json_gpt/convnext_cifar100_c134_results_gpt.json` | Fig. 4 ConvNeXt (`C1/C3/C4`, CIFAR-100) | `paper/latex_gpt/sections/05_results.tex:17` |
| `report_md/_gpt/json_gpt/convnext_flowers102_c134_results_gpt.json` | Fig. 4 ConvNeXt (`C1/C3/C4`, Flowers-102) | `paper/latex_gpt/sections/05_results.tex:17` |
| `report_md/_gpt/iso_accuracy_contour_data.json` | Fig. 3 contour map source | `paper/latex_gpt/sections/05_results.tex:53` |
| `report_md/_gpt/json_gpt/device_comparison_results_gpt.json` | Fig. 10 zero-shot transfer source | `paper/latex_gpt/sections/05_results.tex:109` |
| `report_md/_gpt/json_gpt/fresh_instance_eval.json` | Ensemble HAT fresh-instance numbers used in Fig. `figS3_ensemble_hat` | `paper/latex_gpt/sections/05_results.tex:67` |

## Supplementary quantitative figures

| File | Role | Manuscript cite |
|:--|:--|:--|
| `paper/plot_paper_figures.py` | Generator for supplementary quantitative plots | `paper/latex_gpt/supplementary.tex:99` |
| `report_md/_gpt/json_gpt/zhang_sensitivity_sweep_10mc.json` | `fig_proxy_sensitivity_map` | `paper/latex_gpt/supplementary.tex:99` |
| `report_md/_gpt/sobol_sensitivity.json` | `fig_sobol_sensitivity` | `paper/latex_gpt/supplementary.tex:142` |
| `report_md/_gpt/json_gpt/noise_sweep_results_gpt.json` | `fig9_noise_sensitivity` | `paper/latex_gpt/supplementary.tex:223` |
| `report_md/_gpt/json_gpt/fresh_instance_eval.json` | `fig_fresh_instance_ablation` fresh-instance panel | `paper/latex_gpt/supplementary.tex:230` |
| `report_md/_gpt/ensemble_frequency_ablation.json` | `fig_fresh_instance_ablation` cadence panel | `paper/latex_gpt/supplementary.tex:230` |
| `visualize_attention.py` | `fig_attention_maps` generator | `paper/latex_gpt/supplementary.tex:237` |
| `report_md/_gpt/json/attention_maps_gpt.json` | attention-map metadata | `paper/latex_gpt/supplementary.tex:237` |
| `report_md/_gpt/json_gpt/tinyvit_v4_retention_results_gpt.json` | `fig7_retention_curve` Tiny-ViT retention source | `paper/latex_gpt/supplementary.tex:253` |
| `report_md/_gpt/json_gpt/convnext_full_results_gpt.json` | `fig7_retention_curve` ConvNeXt retention source | `paper/latex_gpt/supplementary.tex:253` |
| `report_md/json/a23_experiment_results.json` | `fig6_physical_compensation`, frontend theory, and SNR curves | `paper/latex_gpt/supplementary.tex:266` |

## NL mitigation / reviewer-facing release artifacts

| File | Role | Manuscript or release cite |
|:--|:--|:--|
| `scripts/_gpt/auto_finalize_nl_ablation.py` | finalize hook for `attn_proj-only` completion | `report_md/_gpt/BROADCAST_ASSIGNMENT_20260418F.md:46` |
| `scripts/_gpt/check_locked_numbers.py` | locked-number guard script | `report_md/_gpt/PRE_SUBMISSION_CHECKLIST.md:21` |
| `report_md/_gpt/NL_LANE_RESULTS_20260418.md` | canonical severe-NL lane summary | `report_md/_gpt/CLAUDE_A_DECISION_FINAL_20260418.md:29` |
| `report_md/_gpt/SUPP_TABLE_NL_ABLATION_SCAFFOLD.md` | Table SX.N scaffold | `report_md/_gpt/CLAUDE_A_DECISION_FINAL_20260418.md:45` |

## Scope note

This is a manuscript-facing ledger, not a complete dependency graph of the training stack. It intentionally tracks the files the paper and submission package are expected to expose or defend during review.
