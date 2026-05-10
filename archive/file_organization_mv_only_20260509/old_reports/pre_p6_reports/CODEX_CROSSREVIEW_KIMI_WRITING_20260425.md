# Codex Cross-Review of Kimi Writing / Mechanism Integration

**Date:** 2026-04-25 13:30 CST  
**Reviewer:** Codex  
**Scope:** Kimi's latest writing-polish and empirical-mechanism integration files.

Reviewed files:
- `paper/latex_gpt/sections/06_discussion.tex`
- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/sections/03_methodology.tex`
- `paper/latex_gpt/supplementary/S_mechanism_empirical.tex`
- `report_md/_gpt/KIMI_CROSSREVIEW_CODEX_EMPIRICAL_20260425.md`
- `report_md/_gpt/KIMI_WRITING_POLISH_20260425.md`

Validation run:
- `pdflatex -interaction=nonstopmode main.tex` -> RC 0
- `pdflatex -interaction=nonstopmode supplementary_main.tex` -> RC 0
- Result: PDFs are generated, but main still has unresolved references listed below.

## Findings

### P0-1: E2 protocol/caption mismatch in S-Mechanism

**Location:** `paper/latex_gpt/supplementary/S_mechanism_empirical.tex:11`, `:30`

Kimi's text says the E2 interpolation uses `alpha in {0, 1, 3}` and the figure caption says shaded regions are across five fresh masks. The final Codex JSON says:

- `report_md/_gpt/json_gpt/d2d_loss_landscape.json`: `alphas = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]`
- `report_md/_gpt/json_gpt/d2d_loss_landscape.json`: `masks = 3`

The table can still report only the headline alpha points, but the method sentence and figure caption should not imply the full protocol used only three alpha points or five masks. The caption also describes "Accuracy (solid) and loss (dashed)", while the actual plot uses model-level line styles and loss markers on the secondary axis. This is a paper-visible protocol mismatch and should be fixed before submission.

Recommended correction:
- Say the full sweep used `alpha in {0, 0.5, 1, 1.5, 2, 2.5, 3}`, with the table reporting headline points `0, 1, 3`.
- Change "five sampled fresh masks" to "three sampled fresh masks".
- Reword line-style description to match the generated figure, or regenerate the figure/caption pair together.

### P0-2: E1 Hessian limitation contains wrong batch size, misleading parameter scale, and wrong ratio wording

**Location:** `paper/latex_gpt/supplementary/S_mechanism_empirical.tex:94`, `:96`

Kimi's limitation says the Lanczos approximation uses a fixed eval batch of 256 samples and analog parameter counts exceeding `10^5`. The final E1 JSON files say:

- `fixed_batch_size = 32`
- `hessian_params = analog`
- `param_count = 4,730,016`

The severe-NL phrase `(1,000--30,000x)` is also not correct as written. The values `1,764.97`, `5,705.60`, and `30,058.40` are absolute Ritz eigenvalues, not multiplicative ratios. If ratios are intended, the denominator must be named. Relative to canonical Standard top-1 (`23.28`), they are about `76x`, `245x`, and `1291x`; relative to canonical Ensemble top-1 (`221.30`), they are about `8x`, `26x`, and `136x`.

Recommended correction:
- Replace "fixed eval batch of 256 samples" with "fixed eval batch of 32 samples".
- Replace "parameter counts exceeding `10^5`" with "4.73M analog parameters".
- Replace `(1,000--30,000x)` with either "absolute top eigenvalues of `1.76e3--3.01e4`" or a clearly defined ratio range.

### P1-1: Main-paper unresolved references remain after Kimi integration

**Locations:**
- `paper/latex_gpt/sections/05_results.tex:41`
- `paper/latex_gpt/sections/05_results.tex:65`
- `paper/latex_gpt/sections/05_results.tex:77`
- `paper/latex_gpt/sections/06_discussion.tex:14`
- target label exists at `paper/latex_gpt/sections/03_methodology.tex:37`

`main.tex` compiles, but LaTeX warns that these references are undefined:

- `eq:hat-ensemble` at Results lines 41 and 65, and Discussion line 14.
- `subsec:methodology-nl` at Results line 77.

Likely fix:
- Replace `eq:hat-ensemble` with `eq:hat-ensemble-distribution`, which is currently defined in `03_methodology.tex:37`.
- Either add `\label{subsec:methodology-nl}` to the nonlinear-write paragraph, or change the reference to the existing `subsec:modeling-nonidealities` label depending on intended target.

This is not a PDF-blocking failure, but it is a submission-readiness issue.

### P2-1: Kimi coordination docs are stale relative to Phase 2 completion

**Locations:**
- `report_md/_gpt/KIMI_WRITING_POLISH_20260425.md:36-44`
- `report_md/_gpt/KIMI_CROSSREVIEW_CODEX_EMPIRICAL_20260425.md:109-110`

The writing-polish status still marks Task B/Task E as blocked on Phase 2, even though Codex Phase 2 has landed. The cross-review doc also repeats the stale E1 concern that the default fixed batch is 256 and analog subset is "likely >100K". This is not paper body, but it can mislead future integration or audit passes.

Recommended correction:
- Mark Phase 2 as received and list the P0 fixes above as the active blocker.
- Update the E1 concern to `fixed_batch_size=32`, `param_count=4,730,016`.

## Clean Items

- `paper/latex_gpt/sections/06_discussion.tex:36-40` uses the safe mechanism wording: D2D-direction robustness, not global Hessian flatness. This is aligned with Codex E1/E2.
- `paper/latex_gpt/supplementary/S_mechanism_empirical.tex:66-96` correctly treats E1 as a negative diagnostic against ordinary full-parameter-space flatness, aside from the numeric/protocol corrections above.
- Both `main.tex` and `supplementary_main.tex` compile to PDFs under nonstop mode.

## Verdict

Kimi's narrative direction is correct and compatible with Codex Phase 2, but the current S-Mechanism draft has two P0 factual/protocol mismatches that should be fixed before using it as paper text. The remaining unresolved LaTeX references should be cleared in the same pass.
