# Device Comparison Results (GPT)

- Generated: `2026-04-07 15:06:51`
- Models: `tinyvit`
- Tiny-ViT experiment: `V4`
- ConvNeXt experiment: `C4`
- Eval runs per profile: `10`
- Profile source: `report_md/_gpt/json_gpt/measured_sample_profile.json`

## Current Invocation

| Model | Device Profile | Accuracy | Source |
|:------|:---------------|:---------|:-------|
| tinyvit | Measured Sample Profile (Suboptimal) | 10.00 +/- 0.00% (10 runs) | simulated_data_case_study |

## Notes

- This sweep measures zero-shot hardware transferability from organic-HAT checkpoints.
- Each profile applies a freshly resampled D2D instance after updating device parameters; results therefore reflect transfer to a new hardware instance, not reuse of the checkpoint's stored mismatch map.
- It does not claim device-specific optimal performance for RRAM or PCM because no device-specific HAT fine-tuning is performed.
- Loaded profiles: `Measured Sample Profile (Suboptimal)`
- Total merged rows: `11`

