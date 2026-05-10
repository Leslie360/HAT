<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# K4R Canonical Branch A Result — Interpretation Framework

## Experiment Configuration
| Parameter | Value |
|:----------|:------|
| Branch | A (`ab56c2d`) |
| Group | `all` (uniform-NL) |
| NL_LTP | 1.0 |
| NL_LTD | -1.0 |
| Second-order α | 0.25 |
| δg_eff | auto (σ_d2d + σ_c2c) |
| Training epochs | 100 |
| Train best acc | [FILL] |
| Train best epoch | [FILL] |

## Fresh-Instance Eval Results
| Metric | Value |
|:-------|:------|
| Cross-instance mean | [FILL] |
| Cross-instance std | [FILL] |
| Min instance mean | [FILL] |
| Max instance mean | [FILL] |
| Range (max-min) | [FILL] |

## Branch A Compliance Checklist
- [ ] Result produced on `ab56c2d` or later
- [ ] First-order STE: no `nl` multiplier (`(...)^(NL-1)`)
- [ ] Second-order sign: negative (`-0.5`)
- [ ] Eval uses same `group=all` uniform-NL as training
- [ ] δg_eff auto-filled from module noise config

## Comparison with Pre-Branch-A Baseline
| | Pre-Branch-A `[INVALID]` | K4R (Branch A) |
|:--|:-------------------------|:---------------|
| Fresh-instance mean | 86.37% [INVALID] | [FILL] |
| Fresh-instance std | 1.54% [INVALID] | [FILL] |

## Interpretation Guide (auto-fill based on result)

### Scenario A: Cross-instance mean ≥ 85%
**Verdict**: Branch A canonical achieves parity with pre-Branch-A nominal threshold.
**Implication**: Sign-corrected second-order brake does not degrade transfer.
**Next steps**: Sweep α ∈ {0.1, 0.5, 1.0} to characterize sensitivity.

### Scenario B: 80% ≤ Cross-instance mean < 85%
**Verdict**: Within ~5 pp of nominal threshold.
**Implication**: Brake may be slightly too strong or ensemble size insufficient.
**Next steps**: Tune α down; consider joint MLP-linear + Ensemble HAT.

### Scenario C: Cross-instance mean < 80%
**Verdict**: Significant degradation relative to nominal threshold.
**Implication**: Second-order brake materially harms transfer; first-order only may be preferable for deployment.
**Next steps**: Ablation without second-order; revisit physical derivation.

## Open Questions
1. Does K4R same-instance accuracy differ from V4?
2. Is the variance budget widened relative to pre-Branch-A?
3. Does `group=mlp` diagnostic show different NL sensitivity?

## Archive
- JSON: `report_md/_gpt/json_gpt/cx_k4r_fresh_eval.json`
- Report: `report_md/_gpt/KIMI_K4R_FRESH_EVAL_REPORT.md`
- Log: `logs/_gpt/cx_k4r_fresh_eval_*.log`
