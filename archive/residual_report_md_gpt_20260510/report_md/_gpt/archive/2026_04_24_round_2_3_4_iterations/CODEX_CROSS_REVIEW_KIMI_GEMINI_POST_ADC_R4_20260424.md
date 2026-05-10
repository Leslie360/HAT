# CODEX Cross-Review: Kimi + Gemini Post-ADC R4

- Date: 2026-04-24
- Reviewer: Codex
- Scope: latest manuscript-side update in [05_results.tex.kimi_draft_v3](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex.kimi_draft_v3) plus consistency with [00_abstract.tex.kimi_draft_v3](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/00_abstract.tex.kimi_draft_v3)

## Findings

### 1. Kimi Part B landed only partially: the table is updated, but it still does not satisfy Claude’s required dual-report structure
- Severity: High
- Evidence:
  - [05_results.tex.kimi_draft_v3:83](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex.kimi_draft_v3#L83) through [#L92](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex.kimi_draft_v3#L92) now include `ADC-on 8-bit` and `ADC-off baseline`, but there is no `ADC-on 6-bit` column.
  - [DISPATCH_KIMI_ROUND2_20260424.md:116](/home/qiaosir/projects/compute_vit/report_md/_gpt/DISPATCH_KIMI_ROUND2_20260424.md#L116) through [#L123](/home/qiaosir/projects/compute_vit/report_md/_gpt/DISPATCH_KIMI_ROUND2_20260424.md#L123) explicitly requested a table with `ADC-off`, `ADC-on 8-bit`, and `ADC-on 6-bit`.
  - [05_results.tex.kimi_draft_v3:97](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex.kimi_draft_v3#L97) discusses the 6-bit cliff in body text, so omitting it from the table creates a structure mismatch.
- Verdict:
  - This is no longer “not started,” but it is still not the exact table Claude asked for.

### 2. §5.7 still contains banned bug-retrospective / internal-code narrative
- Severity: High
- Evidence:
  - [05_results.tex.kimi_draft_v3:76](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex.kimi_draft_v3#L76) uses the heading `Post-fix severe-NL retraining`.
  - [05_results.tex.kimi_draft_v3:77](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex.kimi_draft_v3#L77) says `post-\texttt{33bed9c} codebase`.
  - [05_results.tex.kimi_draft_v3:81](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex.kimi_draft_v3#L81) repeats `post-\texttt{33bed9c}` in the caption.
  - [05_results.tex.kimi_draft_v3:99](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex.kimi_draft_v3#L99) says the previous ceiling was a `software artifact` and names the exact implementation bugs.
  - [DISPATCH_KIMI_ROUND2_20260424.md:82](/home/qiaosir/projects/compute_vit/report_md/_gpt/DISPATCH_KIMI_ROUND2_20260424.md#L82) through [#L96](/home/qiaosir/projects/compute_vit/report_md/_gpt/DISPATCH_KIMI_ROUND2_20260424.md#L96) explicitly banned this style of wording.
- Verdict:
  - Kimi fixed the table direction, but reintroduced exactly the narrative mode Claude told it to remove.

### 3. The protocol sentence now overstates the training path and still lacks the D4 caveat
- Severity: Medium
- Evidence:
  - [05_results.tex.kimi_draft_v3:77](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex.kimi_draft_v3#L77) says `the training forward path employs a differentiable ADC surrogate`.
  - Our audited position is narrower: current training path is the default analog forward / training surrogate, while ADC quantization is injected only at inference time via hooks; the severe-NL ADC-on runs also use static pre-instance calibration, not per-instance recalibration.
  - [CODEX_MSERIES_ADC_DUAL_REPORT_20260424.md:45](/home/qiaosir/projects/compute_vit/report_md/_gpt/CODEX_MSERIES_ADC_DUAL_REPORT_20260424.md#L45) gives the safe deployment statement.
  - [CODEX_CROSS_REVIEW_KIMI_GEMINI_POST_ADC_R3_20260424.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/CODEX_CROSS_REVIEW_KIMI_GEMINI_POST_ADC_R3_20260424.md) already warned not to rewrite the recommended future protocol as the executed one.
- Verdict:
  - The current sentence is still too loose. It needs one precise caveat sentence, not a generic “ADC surrogate” phrase.

### 4. The abstract is now out of sync with the revised §5.7 direction
- Severity: Medium
- Evidence:
  - [00_abstract.tex.kimi_draft_v3:3](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/00_abstract.tex.kimi_draft_v3#L3) still says `post-fix hardware-aware training` and `falsifying a previously reported ~30% ceiling`.
  - It still headlines only the `~80--82% band`, with no distinction between ADC-on deployment numbers and ADC-off surrogate baselines, and no static-calibration caveat.
- Verdict:
  - Once §5.7 is made paper-safe, the abstract should be synchronized or it will keep reintroducing the forbidden internal-erratum framing.

## Clean Passes

### 1. Kimi has actually updated the manuscript-side `05_results`
- The previous blocker “file not updated” is now closed.
- The blocker has shifted from absence-of-work to quality-of-final-wording.

### 2. Core numbers are aligned with Codex outputs
- The per-run 8-bit values in [05_results.tex.kimi_draft_v3](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex.kimi_draft_v3) match the finalized dual report values.

## Recommendations

1. Kimi should keep the updated table body but make three final edits:
   - add the `ADC-on 6-bit` column or explicitly mark spot-check rows with `—` for missing runs,
   - remove `post-fix`, commit hash, and bug-name narrative,
   - replace `differentiable ADC surrogate` with a precise static-precalibration caveat sentence.
2. After that, Kimi should sync the abstract so it no longer reintroduces the internal software-correction story.
