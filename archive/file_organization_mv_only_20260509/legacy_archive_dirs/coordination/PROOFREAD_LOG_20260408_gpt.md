# Proofread Log — 2026-04-08 (Codex)

## Scope
- `paper/latex_gpt/main.tex`
- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/sections/06_discussion.tex`
- `paper/latex_gpt/sections/07_conclusion.tex`

## Submission-facing fixes applied
- softened the `ADC` wording in `§6.1` from an absolute bottleneck claim to a `critical practical threshold within the present simulator configuration`
- replaced the informal numbered prose in `§6.2` with a proper `enumerate` structure
- tightened the `Transformer vs CNN` language in `§6.2` and `§7`
  - now explicitly framed as a result from the present dual-testbed setup
  - now explicitly acknowledges the scratch-vs-fine-tune confound
- tightened the `Flowers-102` language in `§5.3`, `§6.3`, and `§7`
  - now treated as a `data-volume-floor hypothesis` / present-recipe failure boundary
  - no longer phrased as a universally established proof

## Checks performed
- searched `paper/latex_gpt/*.tex` for:
  - `Author list TBD`
  - `TODO`
  - `pending`
  - reviewer-reported typo fragments such as `rst`, `oer`, `dierent`, `eect`, `exible`
- recompiled LaTeX with:
  - `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`

## Current compile status
- `main.pdf` compiles successfully after this pass
- remaining issues are layout-level warnings only:
  - overfull / underfull boxes
  - float placement adjustments
- no hard compile failure remains from this proofread pass

## Notes
- `main.tex` no longer contains `Author list TBD`; it currently uses the provided author line plus submission note
- a broader venue-style pass is still useful later, but the highest-risk reviewer-facing wording issues targeted in this pass are now tightened
