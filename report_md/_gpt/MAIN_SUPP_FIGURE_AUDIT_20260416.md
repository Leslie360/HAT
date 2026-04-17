# Main + Supplementary Figure Audit — 2026-04-16

## Scope

Post-fix audit of:

- main manuscript external figures
- supplementary external figures
- main/supplementary figure reuse
- caption-to-artwork consistency
- main-to-supplementary reference consistency

Key files:

- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex`
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex`
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.aux`
- `/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary_main.aux`

## Fixes Applied

### 1. Supplementary Figure S1 is no longer a duplicated main contour map

Previous issue:

- `S1` reused `fig_contour_map` from main Figure 3 while captioning it as a Zhang-proxy `C2C × D2D` sweep.

Current state:

- `S1` now uses `fig_proxy_sensitivity_map`.
- The figure content matches the surrounding proxy-sensitivity text and the companion tables.
- The caption now correctly describes a Zhang-proxy `C2C/D2D` sweep with the nominal point outlined.

Relevant files:

- [`supplementary.tex`](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex#L95)
- [`fig_proxy_sensitivity_map.png`](/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig_proxy_sensitivity_map.png)
- [`supplementary_main.aux`](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary_main.aux#L43)

### 2. Supplementary Figure S4 is no longer a duplicate of main Figure 5

Previous issue:

- `S4` reused `fig10_zero_shot_transferability` from main Figure 5 while captioning it as a fresh-instance/ablation figure.

Current state:

- `S4` now uses `fig_fresh_instance_ablation`.
- Left panel: fresh fixed-D2D instance transfer across 10 unseen arrays.
- Right panel: D2D-resampling frequency ablation.
- The caption now describes the artwork actually shown.

Relevant files:

- [`supplementary.tex`](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex#L226)
- [`fig_fresh_instance_ablation.png`](/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig_fresh_instance_ablation.png)
- [`supplementary_main.aux`](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary_main.aux#L70)

### 3. The stale `representative CIFAR-10 inputs are shown above the panels` sentence was removed

Current state:

- No remaining caption text claims image strips or panels that are absent from the exported artwork.

Relevant file:

- [`supplementary.tex`](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex#L229)

### 4. Main-text reference to Supplementary Figure S4 is now consistent again

Current state:

- Main text still points to `Supplementary Fig. S4` for fresh-hardware evidence.
- `S4` now genuinely contains a fresh-instance panel plus the associated resampling ablation, so the reference is coherent again.

Relevant files:

- [`05_results.tex`](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex#L54)
- [`05_results.tex`](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex#L90)

## Verification

### Figure reuse check

Current external figure overlap between main and supplementary:

- none

Main external figures:

- `fig4_accuracy_comparison`
- `fig5_hat_recovery`
- `fig_contour_map`
- `figS3_ensemble_hat`
- `fig10_zero_shot_transferability`

Supplementary external figures:

- `fig_proxy_sensitivity_map`
- `fig_sobol_sensitivity`
- `fig9_noise_sensitivity`
- `fig_fresh_instance_ablation`
- `fig_attention_maps`
- `fig7_retention_curve`
- `fig6_physical_compensation`
- `fig3_snr_curves`
- `fig8_pareto_energy_accuracy`
- `figS1_asymmetry_concept`
- `figS2_nonideality`

### Compiled label check

Compiled auxiliary files now resolve to the corrected captions:

- main Figure 3: [`main.aux`](/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.aux#L81)
- main Figure 5: [`main.aux`](/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.aux#L100)
- supplementary Figure S1: [`supplementary_main.aux`](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary_main.aux#L43)
- supplementary Figure S4: [`supplementary_main.aux`](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary_main.aux#L70)

### Build state

The manuscript and supplement were rebuilt after the figure replacements:

- [`main.pdf`](/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.pdf)
- [`supplementary_main.pdf`](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary_main.pdf)

## Remaining Issues

No blocking main/supplementary figure-duplication or caption-to-artwork mismatches remain in the audited external figure set.
