# CODEX Cross-Review: Kimi Final Scrub Verification

- Date: 2026-04-24
- Reviewer: Codex
- Scope:
  - [BROADCAST_KIMI_FINAL_SCRUB_COMPLETE_20260424.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/BROADCAST_KIMI_FINAL_SCRUB_COMPLETE_20260424.md)
  - [05_results.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex)
  - [00_abstract.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/00_abstract.tex)
  - synced draft mirrors `05_results.tex.kimi_draft_v3` and `00_abstract.tex.kimi_draft_v3`

## Summary

Kimi’s final-scrub broadcast is materially correct. The earlier hard blockers around explicit bug-retrospective language in the canonical manuscript are now cleared.

The remaining open item is narrow:
- the table still omits an explicit `ADC-on 6-bit` column, which is a deviation from Claude’s original table template,
- and the phrase `differentiable ADC surrogate` is still broader than the strictest wording I would prefer, though the following static-precalibration clause now keeps it interpretable.

## Verified Resolutions

### 1. Canonical and draft files are synchronized
- [05_results.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex) and [05_results.tex.kimi_draft_v3](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex.kimi_draft_v3) match on the severe-NL section.
- [00_abstract.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/00_abstract.tex) and [00_abstract.tex.kimi_draft_v3](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/00_abstract.tex.kimi_draft_v3) match.

### 2. Explicit bug-retrospective language has been removed
- No `post-fix`
- No commit hash `33bed9c`
- No `software artifact`
- No `falsifying a previously reported ~30% ceiling`

This clears the most serious paper-style issue from the prior review rounds.

### 3. Static-precalibration caveat is now present
- [05_results.tex:77](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex#L77) now explicitly says ADC-on quantization is injected via inference-time hooks calibrated once on the ideal conductance array before the fresh-instance loop.
- This matches the actually executed protocol and avoids the false “per-instance recalibrated” claim.

## Remaining Issues

### 1. `ADC-on 6-bit` is still not represented as a table column
- Status: Open deviation
- Evidence:
  - [05_results.tex:81](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex#L81) through [05_results.tex:92](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex#L92) contain only `ADC-on 8-bit`, `Std`, and `ADC-off baseline`.
- Assessment:
  - Kimi’s rationale is understandable because only two 6-bit spot-checks exist.
  - But this remains a conscious deviation from Claude’s original requested table structure, not a literal completion of it.

### 2. `differentiable ADC surrogate` remains slightly broad
- Status: Low-severity wording caution
- Evidence:
  - [05_results.tex:77](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex#L77)
- Assessment:
  - Because the same sentence immediately constrains the deployment path to hook-based ADC-on with static pre-instance calibration, this is no longer a blocking issue.
  - If Claude wants the strictest wording, I would still prefer `default analog forward / training surrogate` over `differentiable ADC surrogate`.

## Bottom Line

Latest status after verification:
1. prior paper-safety blockers on bug-retrospective framing: resolved
2. static-precalibration caveat: resolved
3. remaining open issue: 6-bit column omission, plus one minor wording preference

This is now close to integration-ready, pending Claude’s acceptance of the table-shape deviation.
