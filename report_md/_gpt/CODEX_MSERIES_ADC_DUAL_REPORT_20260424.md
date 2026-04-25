# CODEX M-Series ADC Dual Report

## 1. Provenance

- Eval commit: `33bed9cbb8ade7676d71074490ad45e68347950e`
- Eval-stack code SHA256: `d287dc4422a5b5bee810381731dfb43fdf51e2a275ea50a0b32ab630864f9642`
- Dirty worktree at eval time: `True`
- CUDA device: `NVIDIA GeForce RTX 5070 Ti`
- PyTorch: `2.10.0+cu128`
- Protocol: `10` fresh instances x `5` MC eval runs per checkpoint
- NL setting: `NL_LTP=2.0`, `NL_LTD=-2.0`
- Provenance guard: `allow_eval_nl_override=false` and `eval_provenance_mismatches=[]` for every ADC-off, ADC-on 8-bit, and ADC-on 6-bit JSON used here.
- CSV output: `report_md/_gpt/csv_gpt/mseries_adc_dual_report.csv`

## 2. Main Dual-Column Table

| Run | Config | Seed | Train Best | Fresh ADC-off | Fresh ADC-on 8-bit | Fresh ADC-on 6-bit | Δ8-bit vs off | Δ6-bit vs off | JSONs |
|:--|:--|--:|--:|--:|--:|--:|--:|--:|:--|
| CX-M1 | V3 Standard | 123 | 82.89 | 82.03 ± 0.94 | 81.87 ± 0.98 | 79.01 ± 1.80 | -0.16 | -3.02 | `report_md/_gpt/json_gpt/cx_m1_fresh_eval.json`<br>`report_md/_gpt/json_gpt/cx_m1_adc_fresh_eval.json`<br>`report_md/_gpt/json_gpt/cx_m1_adc6_fresh_eval.json` |
| CX-M2 | V4 Ensemble | 123 | 80.97 | 80.45 ± 0.58 | 80.39 ± 0.60 | — | -0.07 | — | `report_md/_gpt/json_gpt/cx_m2_fresh_eval.json`<br>`report_md/_gpt/json_gpt/cx_m2_adc_fresh_eval.json` |
| CX-M3 | V4 Proportional | 123 | 80.88 | 80.71 ± 0.14 | 80.65 ± 0.15 | 78.10 ± 0.77 | -0.06 | -2.61 | `report_md/_gpt/json_gpt/cx_m3_fresh_eval.json`<br>`report_md/_gpt/json_gpt/cx_m3_adc_fresh_eval.json`<br>`report_md/_gpt/json_gpt/cx_m3_adc6_fresh_eval.json` |
| CX-M4 | V4 Proportional | 456 | 81.39 | 80.75 ± 0.43 | 80.66 ± 0.41 | — | -0.09 | — | `report_md/_gpt/json_gpt/cx_m4_fresh_eval.json`<br>`report_md/_gpt/json_gpt/cx_m4_adc_fresh_eval.json` |
| CX-M5 | V3 Standard | 456 | 80.69 | 80.47 ± 0.09 | 80.37 ± 0.11 | — | -0.09 | — | `report_md/_gpt/json_gpt/cx_m5_fresh_eval.json`<br>`report_md/_gpt/json_gpt/cx_m5_adc_fresh_eval.json` |
| CX-M6 | V4 Ensemble | 456 | 81.87 | 81.18 ± 1.68 | 81.04 ± 1.76 | — | -0.14 | — | `report_md/_gpt/json_gpt/cx_m6_fresh_eval.json`<br>`report_md/_gpt/json_gpt/cx_m6_adc_fresh_eval.json` |

## 3. Aggregate By HAT Type

| HAT Type | ADC-on 8-bit headline | ADC-off surrogate baseline | Δ8-bit vs off |
|:--|--:|--:|--:|
| Standard | 81.12 ± 1.06 | 81.25 ± 1.10 | -0.13 |
| Ensemble | 80.72 ± 0.46 | 80.82 ± 0.52 | -0.10 |
| Proportional | 80.66 ± 0.01 | 80.73 ± 0.03 | -0.08 |

ADC-on 8-bit is the deployment headline. ADC-off remains in the table as the training-surrogate reference only.

## 4. ADC Impact Analysis

- Mean ΔADC-8bit across all six runs: `-0.1021` pp; run-to-run std: `0.0393` pp.
- Mean ΔADC-6bit across available spot-checks (M1, M3): `-2.8144` pp; run-to-run std: `0.2896` pp.
- 8-bit impact is small and uniform across HAT types: Standard `-0.13` pp, Ensemble `-0.10` pp, Proportional `-0.08` pp at the two-seed aggregate level.
- 6-bit was intentionally run as a spot-check on representative Standard and Proportional checkpoints only; it shows a materially larger cliff than 8-bit and should not be conflated with the paper headline.

## 5. Paper-Safe Statement

> Severe-NL fresh-instance deployment accuracy, evaluated with hook-based 8-bit ADC quantization, sits at [81.12±1.06%] for Standard HAT, [80.72±0.46%] for Ensemble HAT, and [80.66±0.01%] for Proportional HAT, across two seeds per configuration. ADC-off training-surrogate baselines differ by approximately [0.10] pp on average, consistent with the 6-bit ADC cliff analysis (Section~\ref{subsec:iso-accuracy}).

Additional note: 6-bit results are available only for `CX-M1` and `CX-M3` in this batch (`79.01 ± 1.80%` and `78.10 ± 0.77%`, respectively), which is why the headline remains 8-bit deployment fidelity rather than 6-bit stress testing.
