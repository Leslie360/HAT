# LaTeX Supplementary Figure Review — 2026-04-16

## Scope

Review target:

- supplementary entry: [supplementary_main.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary_main.tex)
- included body: [supplementary.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex)

Supplementary figures actually included:

- `fig9_noise_sensitivity`
- `fig10_zero_shot_transferability`
- `fig_attention_maps`
- `fig7_retention_curve`
- `fig6_physical_compensation`
- `fig3_snr_curves`
- `fig8_pareto_energy_accuracy`
- `figS1_asymmetry_concept`
- `figS2_nonideality`

## Findings

### 1. `figS1_asymmetry_concept` and `figS2_nonideality` are readable but still stylistically slide-like

Affected files:

- [supplementary.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex#L313)
- [supplementary.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex#L361)
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/figS1_asymmetry_concept.png`
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/figS2_nonideality.png`

Observed issue:

- Both concept figures use very large embedded headings and sentence-like explanations inside the image.

Why this matters:

- They are acceptable for supplementary use.
- They are not the highest-priority fixes, but they still look more like presentation schematics than archival scientific figures.

## Non-issues

- The supplementary package is pointing at the correct figure directory.
- `supplementary_main.tex` now compiles successfully with the local Tectonic toolchain.
- `fig8_pareto_energy_accuracy.png` was regenerated in this turn from the archived Tiny-ViT dry-run energy report plus the canonical `V1/V2-V7` result JSONs; it is no longer a placeholder panel.
- `fig3_snr_curves.png`, `fig6_physical_compensation.png`, and `fig7_retention_curve.png` were regenerated in this turn without baked-in `Fig. X` titles or footer-style explanatory prose.
- `fig9_noise_sensitivity.png` was regenerated in this turn and no longer contains the `ConvNeXt C4 Data pending` placeholder panel. The current export honestly shows the available Tiny-ViT heatmap plus the ADC sweep curve.
- `fig10_zero_shot_transferability.png` was regenerated in this turn. The current export removes the baked-in `Fig. 10` title, mirrors the y-axis labels across both panels, and marks the ConvNeXt-only missing profile explicitly as `n/a`.
- `fig_attention_maps.png` was re-exported in this turn at `3126x3946` in the same sans-serif font family used by the regenerated paper figures, which is adequate for the near-full-width supplementary placement.
- `figS1_asymmetry_concept.png` and `figS2_nonideality.png` have adequate resolution.
- `fig7_retention_curve.png`, `fig6_physical_compensation.png`, and `fig3_snr_curves.png` are now clean enough for supplementary use.

## Recommended order of fixes

1. Keep `fig9` as-is unless matching ConvNeXt continuous-sweep data are later exported; the current single-model version is acceptable because it is explicit rather than fake-complete.
2. Only after higher-priority manuscript edits, consider simplifying `figS1` and `figS2` for visual polish.
