# Figure 4 Source Data README

## Files

- `fig4_source_data.csv`

## Figure target

This table is the source-data scaffold for main-text **Figure 4** (`fig4_accuracy_comparison`), included from:
- `paper/latex_gpt/sections/05_results.tex:17`

## Schema

Columns:
- `experiment_id`: experiment code used in the repository (`C1/C3/C4`, `V1/V3/V4`)
- `architecture`: plotted model family
- `dataset`: `cifar10`, `cifar100`, or `flowers102`
- `condition`: `FP32`, `Standard-noise`, or `HAT`
- `MC_seed`: blank for this release scaffold because the plotted figure uses summary bars rather than per-seed dots
- `accuracy`: plotted bar height
- `error_bar`: plotted uncertainty bar where available; blank means deterministic or point-estimate bar
- `source_metric`: metric field used to generate the plotted bar (`mc_mean_acc` or `best_test_acc`)
- `source_file`: repository artifact from which the value was read
- `provenance_note`: short note explaining the row role

## Interpretation

This CSV stores the **plotted bar-level values**, not the full raw training histories.

- For ConvNeXt rows, the plotting code prefers `mc_mean_acc` and `mc_std_acc` when present.
- For Tiny-ViT rows, the currently plotted bars come from `best_test_acc` summaries because those JSONs do not expose a uniform Monte Carlo summary field for every dataset/condition pair.
- Blank `error_bar` values therefore do **not** mean zero uncertainty; they mean the currently plotted Figure 4 bar is represented as a deterministic or point-estimate summary in the locked artifact.

## Row count

- total rows: 18
- expected design: 2 architectures × 3 datasets × 3 conditions = 18 rows

## Primary source artifacts

- `report_md/_gpt/json_gpt/convnext_full_results_gpt.json`
- `report_md/_gpt/json_gpt/convnext_cifar100_c134_results_gpt.json`
- `report_md/_gpt/json_gpt/convnext_flowers102_c134_results_gpt.json`
- `report_md/_gpt/json_gpt/tinyvit_v1_results_gpt.json`
- `report_md/_gpt/json_gpt/tinyvit_v2v7_results_gpt.json`
- `report_md/_gpt/json_gpt/tinyvit_cifar100_v134_results_gpt.json`
- `report_md/_gpt/json_gpt/tinyvit_flowers102_v134_results_gpt.json`

## Generation note

This file was generated as a submission-facing source-data scaffold for editorial/reviewer request handling. It is intentionally conservative: it preserves the exact plotted bar values used by the locked Figure 4 generator rather than attempting to reconstruct unlogged per-seed distributions.
