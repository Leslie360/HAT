# CODEX Cross-Review: Kimi + Gemini Post-ADC R2

- Date: 2026-04-24
- Reviewer: Codex
- Delta over prior review: Gemini D4 hook-audit is now delivered; Kimi manuscript-side `05_results` still has not been updated.

## Findings

### 1. Kimi Part B remains the active document-side blocker
- Severity: High
- Evidence:
  - [05_results.tex.kimi_draft_v3:103](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex.kimi_draft_v3#L103) still says ADC-on columns are pending.
  - [05_results.tex.kimi_draft_v3:105](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex.kimi_draft_v3#L105) through [05_results.tex.kimi_draft_v3:114](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex.kimi_draft_v3#L114) remain ADC-off only.
  - File mtime is still earlier than both the dual-report trigger and Gemini D4 delivery.
- Verdict:
  - Kimi is now unblocked and says Part B is executing, but the manuscript-side file is not updated yet. This remains the main blocker.

### 2. Gemini D4 is delivered, and its main protocol finding is confirmed by the code
- Severity: Medium
- Evidence:
  - [GEMINI_G_AUDIT_ADC_HOOK_20260424.md:45](/home/qiaosir/projects/compute_vit/report_md/_gpt/GEMINI_G_AUDIT_ADC_HOOK_20260424.md#L45) through [#L49](/home/qiaosir/projects/compute_vit/report_md/_gpt/GEMINI_G_AUDIT_ADC_HOOK_20260424.md#L49) flag that calibration is done once before the fresh-instance loop.
  - [eval_fresh_instances_adc_ablation.py:107](/home/qiaosir/projects/compute_vit/scripts/_gpt/eval_fresh_instances_adc_ablation.py#L107) calibrates `output_ranges` once.
  - [eval_fresh_instances_adc_ablation.py:111](/home/qiaosir/projects/compute_vit/scripts/_gpt/eval_fresh_instances_adc_ablation.py#L111) only then enters the instance loop.
  - [inference_analysis_utils.py:551](/home/qiaosir/projects/compute_vit/inference_analysis_utils.py#L551) shows calibration itself is performed with `noise_enabled=False`, i.e. on the ideal/noise-free array state.
- Verdict:
  - Gemini’s D4 finding is correct. The current ADC-on numbers are hook-valid, but they are not per-instance-recalibrated ADC numbers.

### 3. The projected `+0.2` to `+0.8` pp recovery is still speculative
- Severity: Medium
- Evidence:
  - [GEMINI_G_AUDIT_ADC_HOOK_20260424.md:68](/home/qiaosir/projects/compute_vit/report_md/_gpt/GEMINI_G_AUDIT_ADC_HOOK_20260424.md#L68) gives an expected shift estimate without a rerun.
  - Kimi’s latest broadcast repeats the same idea as an optional polish pass, but no new measurement exists yet.
- Verdict:
  - This is a hypothesis only. It should not be promoted into manuscript text, captions, or summary claims unless we actually rerun.

## Clean Passes

### 1. The previous “missing D4 file” blocker is closed
- Gemini has now delivered [GEMINI_G_AUDIT_ADC_HOOK_20260424.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/GEMINI_G_AUDIT_ADC_HOOK_20260424.md).
- The remaining issue is claim scoping, not missing work.

### 2. Gemini has aligned on the remaining blocker
- Latest AGENT_SYNC broadcast says Kimi Part B is the gap and rescinds the earlier premature approval.
- That alignment reduces coordination risk.

## Recommendations

1. Kimi should finish Part B using the current dual report, with one explicit caveat:
   - current ADC-on numbers are hook-based deployment estimates under static pre-instance calibration.
2. No one should cite the speculative `+0.2` to `+0.8` pp recovery as evidence.
3. With GPU intentionally idle, the honest path is documentation, not rerun:
   - integrate current numbers,
   - note the calibration limitation,
   - leave per-instance recalibration as a later polish pass.
