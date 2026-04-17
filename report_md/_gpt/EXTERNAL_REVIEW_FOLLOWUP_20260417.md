# External Review Follow-up — 2026-04-17

## Scope

This memo consolidates the newest batch of external review-style comments and records which points were acted on immediately versus intentionally deferred.

## High-Consensus Reviewer Themes

Across the latest external assessments, the strongest points of agreement were:

1. Keep the manuscript positioned as a `first-order behavioral` / `decision-aid` study rather than a chip-predictive simulator.
2. Avoid describing the literature-anchored OPECT case as `validation`.
3. Present AIHWKIT / CrossSim only as shared-regime sanity checks or complements, not as defeated baselines.
4. Keep Flowers-102 framed as a low-data stress test because the ConvNeXt baseline is only a single-run boundary estimate.
5. Keep the ResNet-18 CIFAR-100 collapse framed as a recipe-specific optimization failure, not as a backbone-level physical conclusion.
6. Avoid overclaiming the IR-drop / sneak-path probe as full parasitic validation for organic arrays.

## Changes Applied In This Pass

### 1. Cover letter now states the cross-framework role more explicitly
- File: [cover_letter.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/cover_letter.tex)
- Added a sentence explaining that the revision includes shared-regime sanity checks against AIHWKIT and CrossSim.
- Current framing: the workflow is an organic-specific complement, not a replacement for mature inorganic simulators.

### 2. Main-text limitations now explicitly mention robustness evidence without overclaiming validation
- File: [06_discussion.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/06_discussion.tex)
- Added a sentence stating that the supplementary proxy-sensitivity sweeps and parameter-risk tables do not reverse the main ADC-vs-D2D ranking within the tested uncertainty ranges.
- This addresses repeated reviewer requests to make the robustness evidence more visible in the main paper.

### 3. Supplementary parasitic-effect conclusion was softened
- File: [supplementary.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex)
- Replaced `validating that first-order behavioral models ... are sufficient` with a narrower statement:
  - the IR-drop / sneak-path section now describes the result as a lower-bound sensitivity check consistent with early-stage exploration, not as full parasitic validation for scaled organic arrays.

## What Was Intentionally Not Changed

### 1. No new experiments were added
The following reviewer asks were judged too expensive or too disruptive for the current closeout stage:
- new multi-method HAT baselines beyond fixed-mask HAT
- NL sweeps beyond the locked `NL=2.0` result
- broader AIHWKIT / CrossSim benchmarking
- new task domains such as detection / segmentation
- additional measured-device physical validation

### 2. No locked result numbers were changed
Known tracked caveats remain documented rather than silently rewritten, especially:
- Tiny-ViT CIFAR-10 FP32 `98.06` vs `97.48` statistic-family issue
- source of record: [TX14_TABLE2_RESPONSE_20260417.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/TX14_TABLE2_RESPONSE_20260417.md)

### 3. No manuscript restructure was attempted
The requests to deepen Flowers-102 analysis, expand ResNet failure diagnostics, or broaden the Sobol space were treated as possible future revision items, not as safe pre-submission edits.

## Current Editorial Judgment

After these wording fixes, the remaining external-review pressure is concentrated in high-cost requests rather than easy correctness issues. In practical terms:

- the manuscript is now stronger on scope discipline and reviewer-facing transparency
- the remaining risks are mainly `simulation-only` scope and `additional validation requested`, not obvious wording overreach or packaging errors

## Verification

After the edits above, the following were recompiled successfully:
- [main.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.tex)
- [supplementary_main.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary_main.tex)
- [cover_letter.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/cover_letter.tex)

Current logs remain clean for:
- `undefined reference`
- `multiply defined`
- `Overfull \hbox`
- `Underfull \hbox`
