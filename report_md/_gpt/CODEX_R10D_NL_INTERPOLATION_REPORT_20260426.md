# Codex R10D NL Interpolation Report

Date: 2026-04-26  
Owner: Codex  
Status: COMPLETE

## Executive Verdict

R10D is complete for NL = 1.2, 1.5, and 1.8 using canonical Ensemble HAT training with seed 123 and uniform noise. The intermediate-NL curve is not monotone in source-domain best accuracy but shows a clear fresh-instance degradation as NL approaches 2.0.

| NL | Source Best | Best Epoch | Fresh Mean +/- Std | Fresh Range |
|---:|---:|---:|---:|---:|
| 1.2 | 83.12% | 13 | 83.03 +/- 0.22% | 82.73--83.36% |
| 1.5 | 82.81% | 29 | 82.63 +/- 0.10% | 82.46--82.76% |
| 1.8 | 82.77% | 41 | 80.31 +/- 0.40% | 79.75--81.06% |

Interpretation:

- Mildly elevated NL (`1.2`, `1.5`) remains source/fresh stable around 82.6--83.0%.
- NL `1.8` still trains to 82.77% source but loses about 2.3 pp in fresh-instance mean versus NL `1.2`.
- The transition toward severe NL is gradual up to 1.8 in this fixed seed/protocol, not a sudden collapse; the severe `NL=2.0` story remains governed by the revised M-series evidence, not by this interpolation alone.

## Artifacts

- Summary JSON: `report_md/_gpt/json_gpt/r10d_nl_interpolation_summary.json`
- NL 1.2 fresh JSON: `report_md/_gpt/json_gpt/r10d_nl1.2_fresh_eval.json`
- NL 1.5 fresh JSON: `report_md/_gpt/json_gpt/r10d_nl1.5_fresh_eval.json`
- NL 1.8 fresh JSON: `report_md/_gpt/json_gpt/r10d_nl1.8_fresh_eval.json`
- Train logs: `logs/_gpt/r10d_nl1.2.log`, `logs/_gpt/r10d_nl1.5.log`, `logs/_gpt/r10d_nl1.8.log`

## GPU Status

No `train_tinyvit_ensemble.py`, `eval_fresh_instances_postfix.py`, or R10D launcher process remains active after completion.
