# Codex T5 Weight Distribution Review

**Date:** 2026-04-23 18:28 CST
**Owner:** Codex
**Status:** T5 completed, but citation boundary narrowed.

## Executive Verdict

The original T5 output exists and is useful, but it should not be described as immediately manuscript-usable post-fix evidence without qualification. Its default comparison is old `standard V4` vs old `_ensemble V4`, not `standard V4` vs the post-fix R1 clean anchor.

I therefore ran an additional post-fix-aligned CPU analysis comparing `standard V4` against `R1 clean anchor`.

## Artifacts

### Original T5

- JSON: `report_md/_gpt/json_gpt/weight_distribution_comparison.json`
- Plots: `report_md/_gpt/weight_distribution/`
- Comparison: `checkpoints/V4_hybrid_standard_noise_hat_best.pt` vs `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt`

### Added R1-Aligned T5

- JSON: `report_md/_gpt/json_gpt/weight_distribution_r1_vs_standard.json`
- Plots: `report_md/_gpt/weight_distribution_r1_vs_standard/`
- Comparison: `checkpoints/V4_hybrid_standard_noise_hat_best.pt` vs `checkpoints/_gpt/r1_clean_anchor/V4_hybrid_standard_noise_hat_r1_clean_anchor_first_order_best.pt`

## Original T5 Summary: Standard vs Old Ensemble

| Metric | Value |
|---|---:|
| Shared weight tensors | `68` |
| Standard global weight std | `0.09668` |
| Ensemble global weight std | `0.05205` |
| Top JS-divergence layer | `stages.3.blocks.1.mlp.fc2.weight` (`0.25737`) |
| Largest spectral-norm delta | `stages.3.blocks.1.local_conv.conv.weight` (`-10.49695`) |

Interpretation: the old ensemble checkpoint is much narrower globally than the standard checkpoint. This is useful mechanistic context, but it inherits old-checkpoint provenance limits.

## R1-Aligned Summary: Standard vs R1

| Metric | Value |
|---|---:|
| Shared weight tensors | `68` |
| Standard global weight std | `0.09668` |
| R1 global weight std | `0.07440` |
| Top JS-divergence layer | `stages.2.downsample.conv2.conv.weight` (`0.09659`) |
| Largest spectral-norm delta | `stages.3.blocks.1.attn.qkv.weight` (`+10.73379`) |

Interpretation: R1 is narrower than the standard checkpoint globally, but not as narrow as the old ensemble checkpoint. The largest spectral-norm increases concentrate in attention QKV layers, which may help explain why source accuracy recovers while fresh-instance transfer remains weak.

## Citation Boundary

Safe to say now:

> A post-fix R1-aligned weight-distribution audit shows that the clean first-order anchor has a narrower global weight distribution than the standard V4 checkpoint (`std 0.0744` vs `0.0967`), while attention QKV layers show large spectral-norm increases. This is consistent with source recovery accompanied by fragile cross-instance behavior, but it is diagnostic rather than a standalone causal proof.

Do not say yet:

- Do not say T5 proves the mechanism of R1's fresh-instance failure.
- Do not cite old ensemble-vs-standard T5 as post-fix canonical evidence.
- Do not claim the old ensemble checkpoint is rehabilitated by this analysis.

## Next Step

After R2 completes, rerun the same comparison for R2 vs R1 and R2 vs standard. That will show whether corrected SO2 changes the attention/QKV spectral pattern or only shifts source accuracy.
