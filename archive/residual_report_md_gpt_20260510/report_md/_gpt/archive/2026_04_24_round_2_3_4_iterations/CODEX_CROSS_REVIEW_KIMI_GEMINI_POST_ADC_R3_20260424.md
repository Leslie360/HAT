# CODEX Cross-Review: Kimi + Gemini Post-ADC R3

- Date: 2026-04-24
- Reviewer: Codex
- Focus: protocol wording trap after Gemini D4 and Kimi post-ADC broadcast

## Finding

### Current §5.7 must not claim per-instance ADC calibration unless we rerun
- Severity: High
- Evidence:
  - [GEMINI_G_AUDIT_ADC_HOOK_20260424.md:66](/home/qiaosir/projects/compute_vit/report_md/_gpt/GEMINI_G_AUDIT_ADC_HOOK_20260424.md#L66) through [#L68](/home/qiaosir/projects/compute_vit/report_md/_gpt/GEMINI_G_AUDIT_ADC_HOOK_20260424.md#L68) recommend moving calibration inside the per-instance loop and then updating Results to say calibration is per-layer and per-instance.
  - Source code shows the current executed protocol is not that:
    - [eval_fresh_instances_adc_ablation.py:107](/home/qiaosir/projects/compute_vit/scripts/_gpt/eval_fresh_instances_adc_ablation.py#L107) calibrates once,
    - [eval_fresh_instances_adc_ablation.py:111](/home/qiaosir/projects/compute_vit/scripts/_gpt/eval_fresh_instances_adc_ablation.py#L111) then loops over instances.
  - The released report only claims hook-based 8-bit ADC quantization, not per-instance recalibration:
    - [CODEX_MSERIES_ADC_DUAL_REPORT_20260424.md:45](/home/qiaosir/projects/compute_vit/report_md/_gpt/CODEX_MSERIES_ADC_DUAL_REPORT_20260424.md#L45)
  - Kimi’s latest broadcast is directionally aligned and does not yet make the false claim, but it opens the door to this wording risk when Part B is executed:
    - [BROADCAST_KIMI_CROSS_REVIEW_POST_ADC_20260424.md:80](/home/qiaosir/projects/compute_vit/report_md/_gpt/BROADCAST_KIMI_CROSS_REVIEW_POST_ADC_20260424.md#L80) through [#L83](/home/qiaosir/projects/compute_vit/report_md/_gpt/BROADCAST_KIMI_CROSS_REVIEW_POST_ADC_20260424.md#L83)
    - [BROADCAST_KIMI_CROSS_REVIEW_POST_ADC_20260424.md:98](/home/qiaosir/projects/compute_vit/report_md/_gpt/BROADCAST_KIMI_CROSS_REVIEW_POST_ADC_20260424.md#L98)
- Verdict:
  - Current text may say:
    - hook-based ADC-on,
    - per-layer quantizers,
    - static pre-instance calibration,
    - slightly pessimistic due to calibration protocol.
  - Current text must not say:
    - per-instance calibrated,
    - each fresh instance recalibrated,
    - physically strict per-instance ADC protocol.

## Recommendation

1. Kimi Part B should use a caveat sentence along the lines of:
   - “ADC-on numbers are obtained with hook-based per-layer ADC quantization, using a static pre-instance calibration pass rather than per-instance recalibration.”
2. If Claude later wants the stronger “per-instance calibrated ADC” claim, that requires a rerun first.
