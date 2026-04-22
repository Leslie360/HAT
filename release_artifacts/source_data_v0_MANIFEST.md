# Source Data v0 Manifest — 2026-04-18

This is a scaffold bundle for editorial/reviewer source-data requests. It is not yet the final public release package.

## Included files

### Figure 4 release table
- `report_md/_gpt/data_releases/fig4_source_data.csv`
- `report_md/_gpt/data_releases/fig4_source_data_README.md`

### Locked-number JSON snapshots
- `report_md/_gpt/json_gpt/fresh_instance_eval.json`
- `report_md/_gpt/json_gpt/literature_profile_eval.json`
- `report_md/_gpt/json_gpt/v4_ensemble_results_gpt.json`
- `report_md/_gpt/json_gpt/v4_nl2_hat_eval_results_gpt.json`
- `report_md/_gpt/iso_accuracy_contour_data.json`
- `report_md/_gpt/sobol_sensitivity.json`

### NL ablation CSV exports
- `report_md/_gpt/data_releases/nl_lane_source_domain_20260418.csv`
- `report_md/_gpt/data_releases/nl_lane_fresh_instance_20260418.csv`

## Purpose

- make Fig. 4 source-data requestable immediately
- bundle the locked quantitative JSONs most likely to be cited in review
- expose the severe-NL ablation table in CSV form without waiting for final public archiving

## Deliberate exclusions

- no private raw measured-device trees
- no `数据_博士/`
- no full checkpoint bundle
- no internal logs archive
