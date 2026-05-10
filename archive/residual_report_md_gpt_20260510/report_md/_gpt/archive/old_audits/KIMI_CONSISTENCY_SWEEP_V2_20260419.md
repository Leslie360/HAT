# K-R5: Consistency Sweep v2

Searched all `.tex` files in `compute_vit/paper/latex_gpt/` for the four target patterns.

## (a) 86.37 ± 1.54 pairing
- **PASS** — 0 issues found
- All 10 occurrences of `86.37` are paired with `±1.54` (or `\pm 1.54`) in the same sentence/paragraph.
  - `supplementary.tex:480`, `supplementary.tex:789`
  - `sections/00_abstract.tex:5`, `sections/01_introduction.tex:15`, `sections/01_introduction.tex:17`
  - `sections/05_results.tex:63`, `sections/06_discussion.tex:13`, `sections/07_conclusion.tex:7`
  - `cover_letter.tex:26`, `cover_letter.tex:39`

## (b) 10.00% collapsed-predictor labelling
- **2 issues found**
- Required label (`collapsed`, `predictor`, `chance`, or `single-class`) missing within a 20-word window.

1. **`cover_letter.tex:26`**
   > An Ensemble HAT strategy that resamples D2D masks raises fresh-instance accuracy from `10.00\%` to 86.37$\pm$1.54\%.
   - No required label in the sentence or within 20 words before/after.

2. **`supplementary.tex:638`**
   > `0.10 (10\%) & 10.00\% & 0.00\% & 81.78\% \\
   - Table cell in the differential-pair asymmetry sensitivity table. Neither the caption above nor the surrounding rows contain a required label within 20 words of the token.

- All other 10 occurrences are properly labelled (e.g., "chance level", "collapses to chance", "collapsed single-class predictor").

## (c) 14.43 forward-pointer/preliminary pairing
- **PASS** — 0 issues found
- Single occurrence at `sections/06_discussion.tex:47`:
  > A **preliminary** cross-framework comparison ... a large qualitative divergence of `14.43`~pp at $n=3$, **preliminary** ...
  - The word "preliminary" appears twice in the same sentence, satisfying the pairing requirement.
  - Note: `Supplementary Note~SX.Y` appears in the following sentence, not the same one.

## (d) 32.12 / 32.60 diagnostic/deployment-grade framing
- **PASS** — 0 issues found
- Single occurrence at `supplementary.tex:789`:
  - `$32.12\pm7.72$\%` is accompanied by "fresh-instance transfer accuracy", "training-diagnostic tool", and "deployment-grade mitigation" in the same sentence.
  - `$32.60\pm9.18$\%` is accompanied by "fresh-instance transfer" and "deployment-grade transfer" in the same sentence.
