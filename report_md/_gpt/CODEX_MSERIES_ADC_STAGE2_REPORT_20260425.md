# CODEX M-Series ADC Stage-2 Per-Instance Calibration Report

## 1. Provenance

- Eval commit: `33bed9cbb8ade7676d71074490ad45e68347950e`
- Eval-stack code SHA256: `2a07ed71a70f9c8c6f5b7856acfb426f89bac786287795935867ebdf07bdc4ad`
- Dirty worktree at eval time: `True`
- CUDA device: `NVIDIA GeForce RTX 5070 Ti`
- PyTorch: `2.10.0+cu128`
- Protocol: `10` fresh instances x `5` MC eval runs per checkpoint
- ADC setting: `8-bit`, `adc_dnl_sigma=0.5`, `adc_calibration_batches=2`
- Stage-2 calibration: `adc_calibration_scope=per_instance`, `adc_calibration_noise=current_d2d_with_c2c_disabled`
- NL setting: `NL_LTP=2.0`, `NL_LTD=-2.0`; noise mode matched each checkpoint provenance.
- Provenance guard: `allow_eval_nl_override=false` and `eval_provenance_mismatches=[]` for every JSON used here.
- CSV output: `report_md/_gpt/csv_gpt/mseries_adc_stage2_report.csv`

## 2. Stage-1 vs Stage-2 Comparison

| Run | Config | Seed | Fresh ADC-off | Fresh ADC-on static cal (Stage 1) | Fresh ADC-on per-instance cal (Stage 2) | Δ Stage2−Stage1 | Δ Stage2−Off | JSONs |
|:--|:--|--:|--:|--:|--:|--:|--:|:--|
| CX-M1 | V3 Standard | 123 | 82.03 ± 0.94 | 81.87 ± 0.98 | 81.89 ± 1.02 | 0.02 | -0.14 | `report_md/_gpt/json_gpt/cx_m1_fresh_eval.json`<br>`report_md/_gpt/json_gpt/cx_m1_adc_fresh_eval.json`<br>`report_md/_gpt/json_gpt/cx_m1_adc_perinstance_fresh_eval.json` |
| CX-M2 | V4 Ensemble | 123 | 80.45 ± 0.58 | 80.39 ± 0.60 | 80.37 ± 0.59 | -0.02 | -0.08 | `report_md/_gpt/json_gpt/cx_m2_fresh_eval.json`<br>`report_md/_gpt/json_gpt/cx_m2_adc_fresh_eval.json`<br>`report_md/_gpt/json_gpt/cx_m2_adc_perinstance_fresh_eval.json` |
| CX-M3 | V4 Proportional | 123 | 80.71 ± 0.14 | 80.65 ± 0.15 | 80.64 ± 0.13 | -0.01 | -0.07 | `report_md/_gpt/json_gpt/cx_m3_fresh_eval.json`<br>`report_md/_gpt/json_gpt/cx_m3_adc_fresh_eval.json`<br>`report_md/_gpt/json_gpt/cx_m3_adc_perinstance_fresh_eval.json` |
| CX-M4 | V4 Proportional | 456 | 80.75 ± 0.43 | 80.66 ± 0.41 | 80.67 ± 0.41 | 0.01 | -0.08 | `report_md/_gpt/json_gpt/cx_m4_fresh_eval.json`<br>`report_md/_gpt/json_gpt/cx_m4_adc_fresh_eval.json`<br>`report_md/_gpt/json_gpt/cx_m4_adc_perinstance_fresh_eval.json` |
| CX-M5 | V3 Standard | 456 | 80.47 ± 0.09 | 80.37 ± 0.11 | 80.37 ± 0.08 | -0.00 | -0.09 | `report_md/_gpt/json_gpt/cx_m5_fresh_eval.json`<br>`report_md/_gpt/json_gpt/cx_m5_adc_fresh_eval.json`<br>`report_md/_gpt/json_gpt/cx_m5_adc_perinstance_fresh_eval.json` |
| CX-M6 | V4 Ensemble | 456 | 81.18 ± 1.68 | 81.04 ± 1.76 | 81.04 ± 1.73 | -0.00 | -0.14 | `report_md/_gpt/json_gpt/cx_m6_fresh_eval.json`<br>`report_md/_gpt/json_gpt/cx_m6_adc_fresh_eval.json`<br>`report_md/_gpt/json_gpt/cx_m6_adc_perinstance_fresh_eval.json` |

## 3. Aggregate By HAT Type

| HAT Type | Stage-2 per-instance ADC-on | Stage-1 static ADC-on | Δ Stage2−Stage1 |
|:--|--:|--:|--:|
| Standard | 81.13 ± 1.07 | 81.12 ± 1.06 | 0.01 |
| Ensemble | 80.71 ± 0.47 | 80.72 ± 0.46 | -0.01 |
| Proportional | 80.66 ± 0.02 | 80.66 ± 0.01 | 0.00 |

## 4. Escalation Verdict

- Mean Δ Stage2−Stage1 across all six M-series runs: `0.0002` pp; run-to-run std: `0.0124` pp.
- Claude threshold verdict: **NO ESCALATION: Stage-2 recovery is effectively zero and below Claude's expected +0.2 to +0.8 pp window; the static-calibration caveat did not materially bias the current M-series ADC numbers.**
- Interpretation scope: these remain hook-based ADC quantization measurements with per-instance range recalibration on each fresh noisy hardware realization; they validate that static calibration was not a material confounder under the current hook protocol, but they still use the current post-module-output hook implementation.

## 5. Paper-Safe Statement For Kimi

> Severe-NL fresh-instance accuracy under the current hook-based 8-bit ADC quantization protocol, with per-instance recalibration on each noisy hardware realization, sits at [81.13±1.07%] for Standard HAT, [80.71±0.47%] for Ensemble HAT, and [80.66±0.02%] for Proportional HAT, across two seeds per configuration. This is a +0.00 pp change relative to the static-calibration protocol reported in the initial dual report, indicating no material static-calibration bias under the current hook implementation.
