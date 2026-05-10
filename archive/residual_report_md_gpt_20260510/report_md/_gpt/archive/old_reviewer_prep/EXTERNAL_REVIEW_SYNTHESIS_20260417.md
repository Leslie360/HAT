# External Review Synthesis — 2026-04-17

## Scope

This note consolidates the external AI-review feedback supplied on 2026-04-17 (Kimi, DS, Doubao, Mimo, Gemini, Nemotron, Qwen, Sonar) into a single actionable summary for manuscript closeout.

## Consensus Verdict

High-level convergence across the reviews:

- no reviewer model recommended rejection
- the modal recommendation is `Minor Revision`
- the more favorable models view the current draft as near-accept or accept-level for a methods paper

Shared interpretation:

- the paper is publishable as a `methods / prospective simulation` contribution
- the framework must stay framed as `first-order behavioral`, not `predictive hardware validation`
- the strongest scientific value is the deployment-risk ranking and the Ensemble-HAT transfer result

## Repeated Strengths

The strongest recurring positives were:

1. `Ensemble HAT` solves a real deployment problem
   - fresh-instance collapse from `10.00%` to `86.37 ± 1.54%`

2. the `6-bit ADC cliff` is actionable
   - it gives a concrete circuit-design priority rather than a vague robustness claim

3. the `Sobol + contour` analysis substantially strengthens the paper
   - full-grid `S_ADC = 0.976`
   - operational-region `S_D2D = 0.922`

4. the framework is now honestly scoped
   - behavioral
   - simulation-based
   - pre-hardware / pre-silicon

## Repeated Risks

The most repeated concerns were:

1. the paper must not read like physical validation
   - avoid words such as `validation` for literature-anchored OPECT transfer
   - keep the work positioned as a decision aid, not a chip-predictive emulator

2. energy claims must stay explicitly bounded
   - `11.45x` should be read as an illustrative upper bound under placeholder constants

3. CrossSim / AIHWKIT comparisons must be described as shared-regime sanity checks
   - cross-framework discrepancies under noise should be attributed to mapping semantics and calibration differences, not to one simulator being categorically right

4. Flowers-102 and ResNet failure modes require careful framing
   - ConvNeXt Flowers-102 is only a single-run boundary estimate
   - ResNet CIFAR-100 collapse should not be overinterpreted as an architecture verdict

5. severe non-linear write must remain approximation-scoped
   - `NL = 2.0` is a training-recipe bottleneck under the present surrogate
   - not a fundamental materials bound

## High-Confidence Actions Chosen

We selected only low-risk textual fixes that improve reviewer robustness without changing any locked results:

1. abstract wording tightened
   - `evaluated canonical regime` -> `simulated canonical regime`
   - `primary recovery limit` -> `practical recovery bottleneck`
   - `materials-to-system bridge` -> `materials-to-system decision aid`

2. literature-profile case study softened
   - removed `validation` language
   - replaced with `literature-anchored reference point / case study`

3. energy section downgraded further
   - explicitly labeled as `first-order system-level upper bounds`
   - explicitly not `chip-predictive routed-silicon estimates`

4. limitations strengthened
   - future measured organic-array sheet-resistance data explicitly called out
   - added a manuscript-level sentence that the framework ranks deployment risk rather than forecasting exact chip outcomes

5. CrossSim discrepancy phrased more defensibly
   - now framed as a `joint-calibration problem`
   - not as an implicit claim that CrossSim is wrong

6. Flowers-102 caveat made explicit
   - ConvNeXt Flowers-102 baseline is a single-run boundary estimate
   - not a stable cross-architecture ranking benchmark

## Changes Landed

The targeted edits were applied in:

- [00_abstract.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/00_abstract.tex)
- [05_results.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex)
- [06_discussion.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/06_discussion.tex)
- [supplementary.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex)
- [cover_letter.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/cover_letter.tex)

## Deferred Items

The following suggestions were noted but intentionally not acted on in this pass because they would require new experiments, new data, or a larger manuscript rewrite:

- full physical closed-loop validation with fabricated hardware
- broader AIHWKIT / CrossSim multi-regime benchmarking
- layer-wise NL sensitivity
- larger-task or larger-model expansion
- new uncertainty-quantification experiments beyond the current supplementary sensitivity tables

## Bottom Line

The external review consensus supports the current submission strategy:

- keep the manuscript scoped as a rigorous `methods / prospective simulation` paper
- strengthen wording discipline around validation and energy
- avoid overclaiming outside the current evidence envelope
