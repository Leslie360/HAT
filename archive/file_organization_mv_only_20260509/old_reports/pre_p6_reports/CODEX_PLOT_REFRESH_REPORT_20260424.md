# CODEX Plot Refresh Report

- Date: 2026-04-24
- Scope: post-fix severe-NL figure refresh from CX-M1..M6 JSON files.
- No experiments were run by this plotting script.

## Outputs

- `paper/figures/fig5_hat_recovery.png` and `.pdf`
- `paper/figures/figS3_ensemble_hat.png` and `.pdf`
- `paper/figures/fig_postfix_severe_nl.png` and `.pdf`
- `paper/figures/figS_cross_host_parity.png` and `.pdf`

## Source Data

- `report_md/_gpt/json_gpt/cx_m1_fresh_eval.json`
- `report_md/_gpt/json_gpt/cx_m2_fresh_eval.json`
- `report_md/_gpt/json_gpt/cx_m3_fresh_eval.json`
- `report_md/_gpt/json_gpt/cx_m4_fresh_eval.json`
- `report_md/_gpt/json_gpt/cx_m5_fresh_eval.json`
- `report_md/_gpt/json_gpt/cx_m6_fresh_eval.json`

Remote rows used only where dispatch supplied fresh values:
- R-M1 Standard seed 123: 83.64 +/- 0.10
- R-M2 Proportional seed 123: 84.80 +/- 0.08
- R-M2 Proportional seed 222: 84.79 +/- 0.07

## Notes

- Existing `fig5_hat_recovery` and `figS3_ensemble_hat` were backed up under `paper/figures/deprecated_20260424/` before overwrite.
- `fig_postfix_severe_nl` now includes an ADC-off vs ADC-on subplot; 6-bit bars are spot-checks for Standard and Proportional only.
- Bug-immune canonical Ensemble HAT value `86.37 +/- 1.54` is retained as a reference bar.
- The severe-NL structural-limit figure remains quarantined.
- Captions should state that error bars are 1 standard deviation across seeds unless otherwise noted.
