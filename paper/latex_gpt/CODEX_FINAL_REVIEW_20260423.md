# Codex Final Independent Review - 2026-04-23

Scope reviewed: `paper/latex_gpt/sections/*.tex`, `paper/latex_gpt/cover_letter_v3.tex`, `paper/latex_gpt/supplementary.tex`, `paper/latex_gpt/main.tex`, current generated LaTeX artifacts where relevant, canonical CX-K/J JSONs under `report_md/_gpt/json_gpt/`, and local 2026-04-23 recovery/provenance reports.

Verdict: **issues found; not submit-ready.** The manuscript is mostly internally consistent with the old CX-K2 JSON values, but it conflicts with later local provenance documents that explicitly invalidate the same Work 1 severe-NL / K-series / Ensemble-HAT result family. That conflict must be resolved before any submission or cover-letter claims.

## Blocking Findings

1. **Current manuscript cites result families that local recovery documents mark invalid.**

   The manuscript repeatedly uses old Work 1 headline values: Ensemble HAT `86.37±1.54%`, severe-NL retraining `27.72±0.82%`, proportional-noise HAT `97.37±0.05%`, joint MLP-linear + Ensemble HAT `30.53±7.07%`, CX-K2 `38.95±9.85%`, K4 `44.29±13.78%`, and OPECT transfer `88.53±0.08%` (`00_abstract.tex:3`, `01_introduction.tex:15-17`, `05_results.tex:63,74,78,90`, `06_discussion.tex:13,43,45`, `07_conclusion.tex:7-9`, `cover_letter_v3.tex:23-27,33`).

   Local provenance documents now say these are not safe citation targets. `KIMI_CANONICAL_SURVIVORS_20260423.md:21-35` marks K-series/J-series severe-NL runs, Ensemble HAT, NL-HAT retraining, MLP/all-linear fresh transfer, OPECT transfer, and proportional-noise HAT invalid. `KIMI_DUAL_BUG_INVALIDATION_MATRIX_20260423.md:36-44` repeats the same invalidation. `CODEX_REVIEW_OF_KIMI_RECOVERY_20260423.md:52-74` identifies R1 as the first clean post-fix anchor candidate (`34.5612±8.7878%` fresh), and `:88` says paper insertion should remain frozen until post-fix comparison work is reviewed.

   This is not a rounding or wording issue. It is an authority conflict: the manuscript treats pre-fix JSONs as canonical, while later local records say they are contaminated. Either the recovery invalidation matrix is wrong and must be formally superseded, or the manuscript must remove/rewrite every claim that depends on those invalidated runs.

2. **The severe-NL `27.72±0.82%` claim conflates the surviving forward-only result with invalid retraining results.**

   `KIMI_CANONICAL_SURVIVORS_20260423.md:16` says only the V4 severe-NL **inference-only** result `27.72%` survives. The same file marks `NL-HAT retraining (27.37%, 27.72±0.82%)` invalid at `:31`. The manuscript uses `27.72±0.82%` as a severe-nonlinearity recovery/training result (`01_introduction.tex:15`, `05_results.tex:63`, `07_conclusion.tex:7`). If the valid result is the forward-only stress test, drop the retraining-style uncertainty and rewrite the provenance; if it is a retrained NL-HAT number, it is currently invalid under the local survivor list.

3. **The claimed severe-NL ceiling is numerically inconsistent across the paper and with the canonical K2/K4 values.**

   The abstract and cover letter claim an approximately `30%` fresh-instance ceiling (`00_abstract.tex:3`, `cover_letter_v3.tex:25,33`), while the introduction and discussion claim an approximately `40%` structural limit (`01_introduction.tex:17`, `06_discussion.tex:45`). The CX-K2 JSON reports `38.9453±9.8506%` over `N=30`; K4 alpha `0.25` reports `44.291±13.783%`; Kimi's Work 1 loop-closure analysis itself frames the central claim as approximately `40%` (`KIMI_WORK1_LOOP_CLOSURE_ANALYSIS_20260423.md:11,23-32,80-84`). Calling the limit `~30%` under-reports the stated best recipe and makes the cover-letter novelty claim look cherry-picked. Use a single framing, likely "roughly 30-45%, with K2 mean ~39% and K4 peak ~44%" if these data remain valid.

## Major Findings

4. **Hartigan dip-test wording overstates what `p=0.98` proves.**

   `cx_k2_bimodality_test.json` says `p > 0.05: cannot reject unimodal null hypothesis` and `bimodal_significant=false`. The manuscript sometimes uses the correct cautious form, but also says the result "confirms a wide unimodal structural limit" (`07_conclusion.tex:9`) and that the figure "refut[es] the multi-attractor hypothesis" (`05_results.tex:83`). A non-rejection of unimodality is not confirmation of unimodality, and it does not refute multi-attractor behavior. Safer wording: "does not provide statistical evidence for bimodality at N=30."

5. **Supplementary figure/table references in the main text are stale because they are hard-coded.**

   `main.tex:30-36` defines fixed labels: `S3`, `S4`, `S6`, `S7`, `S8`, and `S7`. The current supplementary auxiliary numbering shows different targets:

   - Noise/ADC sweep is `fig:supp-noise-sensitivity = S5`, but `\SuppFigNoiseSweep` is `S3` (`05_results.tex:31`).
   - Fresh-instance/D2D cadence ablation is `fig:supp-zero-shot-transfer = S6`, but `\SuppFigZeroShot` is `S4` (`05_results.tex:63`).
   - Retention curve is `fig:supp-retention-curve = S8`, but `\SuppFigRetention` is `S6` (`05_results.tex:36`).
   - Front-end compensation/SNR are `S9--S10`, but `\SuppFigFrontend--\SuppFigSnr` expands to `S7--S8` (`05_results.tex:46`).
   - Flowers-102 is `tab:supp-flowers-results = S10`, but `\SuppTableFlowers` is `S7` (`05_results.tex:29`, `06_discussion.tex:34`).

   LaTeX cannot warn about this because these are plain text macros, not references. Replace the hard-coded macros with real `\ref{...}` links or update all macros after every supplementary reorder.

6. **Supplementary build artifacts are stale enough to create a citation warning.**

   The current source line uses `crosssim2024` (`supplementary.tex:714`) and `refs_gpt.bib` defines `crosssim2024`, but checked/generated artifacts are stale: `paper/latex_gpt/supplementary_main.aux:111` still cites `crosssim2026`, `paper/latex_gpt/supplementary_main.blg` reports the missing `crosssim2026` entry, and `paper/latex_gpt/supplementary_main.bbl` omits the CrossSim bibliography item. Rebuilding the supplement in `/tmp/latex_gpt_supp_current2` still left `crosssim2024` unresolved because the stale source-directory `.bbl` was reused. Clean auxiliary files and regenerate the supplement `.bbl` before packaging.

7. **The supplementary/provenance text still asserts Branch A ratification despite later bug invalidation.**

   `supplementary.tex:131` says the second-order correction was "Branch A ratified in canonical commit `ab56c2d`." Later recovery documents say `ab56c2d` itself contained the branch-swap and extraneous-`nl` bugs (`KIMI_DUAL_BUG_INVALIDATION_MATRIX_20260423.md:4-8,26-36`). This footnote is directly misleading under the current local provenance state.

8. **The K2/K4/K5 mitigation sweep is not sufficiently disclosed in the paper/supplement.**

   The main text says parameter sweeps and `N=30` establish a structural limit (`01_introduction.tex:17`, `05_results.tex:78`), and the cover letter admits K4 alpha `0.75` and `1.00` were not evaluated (`cover_letter_v3.tex:27`). The supplement has Table S16 for group-wise ablations, but I do not see a complete K2/K3/K4/K5 source-data table that reports alpha/delta-g/order settings, valid/invalid provenance, sample sizes, means, standard deviations, and missing points. The cover-letter disclosure is more complete than the manuscript. If this remains a central claim, add a supplementary table with the full severe-NL mitigation matrix and explicit missing/invalid entries.

## Medium Findings

9. **Mechanistic explanations go beyond the measured evidence.**

   The discussion claims the softmax Lipschitz constant is "bounded below by the inverse temperature," perturbations are amplified "exponentially in the direction of the dominant eigenvector," and this explains the structural limit (`06_discussion.tex:45`). I found JSON evidence for accuracy distributions and group-wise gradient diagnostics, not for this spectral mechanism. Mark this as a hypothesis or remove the unsupported spectral language.

10. **The physical interpretation of `NL=2.0` is too strong for a proxy stress setting.**

   `supplementary.tex:251` says the literature-derived physical profile indicates `NL_LTP=2.0`, `NL_LTD=-2.0`, maps to an approximately `3:1` conductance saturation asymmetry, and is consistent with reported long-pulse dynamics. Elsewhere the manuscript frames severe NL as a stress test and the Zhang OPECT profile as not having an NL fit (`supplementary.tex:236`). Unless a pulse-level extraction is provided, this should be softened to a proxy stress parameter rather than a derived physical profile.

11. **Main-section order is unusual and creates backwards narrative dependencies.**

   `main.tex:50-56` orders sections as Introduction, Related Work, Results, Discussion, Methodology, Experimental Setup, Conclusion. The result text repeatedly references equations and definitions that are formalized later (`05_results.tex:13,41,51,63`). This compiles, but it is awkward for a Nature Communications-style article unless the journal template explicitly wants Methods after Discussion. If retained, keep the forward references minimal and make sure the Methods placement is intentional.

12. **`sections/08_appendix.tex` is not included in the main manuscript.**

   The user-requested glob includes `sections/*.tex`, but `main.tex:50-56` does not input `sections/08_appendix.tex`. If this appendix is meant to be part of the paper, it is currently omitted. If it is intentionally dead/stale, remove it from the submission source tree or clearly mark it non-submission to avoid reviewer/editor confusion.

13. **Cover letter has submission placeholders and overclaims deployment.**

   `cover_letter_v3.tex:9` still has `[Corresponding author name]`, and `:46` has `[To be provided]`. More importantly, `:23` says the old Ensemble-HAT number enables "robust deployment without per-device calibration"; even ignoring the invalidation issue, the evidence is simulation-only and does not include fabricated-array validation. Say "simulated fresh-instance transfer under the modeled D2D distribution" instead.

## Checks That Passed

- The CX-K2 numeric transcription itself is accurate: `cx_k2_fresh_eval.json` gives `38.94533333333333±9.850631225471282`, with observed range `22.034--61.694`; `05_results.tex:78,83` rounds this correctly.
- The Hartigan value is transcribed accurately: `cx_k2_bimodality_test.json` gives `p_value=0.9796`, rounded to `0.98`.
- The joint MLP-linear + Ensemble HAT value in `05_results.tex:74` matches `joint_mlp_linear_ensemble_hat_full_fresh.json` (`30.5324±7.0659`) before considering provenance invalidation.
- The OPECT value in `05_results.tex:90` matches `literature_profile_eval.json` (`88.53±0.0827`) before considering provenance invalidation.
- `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=/tmp/latex_gpt_main_current2 main.tex` produced a 19-page PDF. The main manuscript has no final unresolved-reference warnings in that build, but the hard-coded supplementary-number issue above is invisible to LaTeX.
- `latexmk` produced a 24-page supplementary PDF in `/tmp/latex_gpt_supp_current2`, but with the stale CrossSim citation/bbl issue noted above.
- `cover_letter_v3.tex` compiles, but content placeholders remain.

## Required Resolution Before Submission

1. Decide and document the active authority: either supersede the dual-bug invalidation matrix with evidence, or remove every manuscript claim that relies on invalidated pre-fix runs.
2. Reframe the severe-NL ceiling consistently (`~40%` or a stated `30-45%` band, not both `~30%` and `~40%`).
3. Replace hard-coded supplementary numbering with real references or update the macros from the current supplementary `.aux`.
4. Regenerate clean `.aux/.bbl/.pdf` artifacts for the supplement.
5. Add a complete severe-NL mitigation provenance table, including missing K4 alpha points and valid/invalid status.
