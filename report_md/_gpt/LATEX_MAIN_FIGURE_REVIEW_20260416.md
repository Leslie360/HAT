# LaTeX Main Figure Review — 2026-04-16

## Scope

Review target:

- main entry: [main.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.tex)
- figures actually used in the compiled main paper:
  - `fig4_accuracy_comparison`
  - `fig5_hat_recovery`
  - `figS3_ensemble_hat`
  - `fig10_zero_shot_transferability`

Important context:

- `main.tex` uses [`./figures/`](/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.tex#L5).
- The methodology figures are not external PNG assets; they are inline TikZ figures in [03_methodology.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/03_methodology.tex#L13) and [03_methodology.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/03_methodology.tex#L89).

## Findings

No blocking main-figure issues remain after the 2026-04-16 regeneration pass.

Residual editorial consideration:

- `figS3_ensemble_hat` is now clean enough for main-text use, but it remains a conceptual schematic rather than a primary measurement figure. If page budget tightens, it is still the most natural candidate to move into the Supplementary Information.

## Non-issues

- Resolution is adequate for the four main external figures:
  - `fig4_accuracy_comparison.png`: `3364x1483`
  - `fig5_hat_recovery.png`: `3083x1553`
  - `fig10_zero_shot_transferability.png`: `3684x1508`
  - `figS3_ensemble_hat.png`: `2683x1297`
- `main.tex` is pointing at the correct figure directory.
- The missing-file issue seen in `paper/figures/` does not apply to the compiled LaTeX package under `paper/latex_gpt/figures/`.
- `fig4_accuracy_comparison.png`, `fig5_hat_recovery.png`, and `fig10_zero_shot_transferability.png` were regenerated in this turn without baked-in `Fig. X` titles.
- `fig4_accuracy_comparison.png` now shows uncertainty bars where Monte Carlo statistics are available, and its caption no longer overclaims `10`-run statistics for every bar.
- `fig5_hat_recovery.png` no longer contains the stray bottom-margin annotation or the overlapping center-axis labels seen in the earlier export.
- `fig10_zero_shot_transferability.png` was regenerated in this turn. The previous baked-in `Fig. 10` title, missing right-panel y-axis labels, and orphan-looking category problem are no longer present in the current export.
- `figS3_ensemble_hat.png` was redrawn in the same font and line-weight system used by the generated paper figures. The previous slide-like headings, repeated emphasis labels, and bottom-banner takeaway text are gone.

## Recommended order of fixes

1. No blocking figure changes are required before submission.
2. If main-text space becomes tight, consider moving `figS3_ensemble_hat` to the Supplementary Information.
