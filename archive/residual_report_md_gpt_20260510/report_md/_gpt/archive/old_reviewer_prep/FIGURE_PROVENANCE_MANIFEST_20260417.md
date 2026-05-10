# Figure Provenance Manifest — 2026-04-17

## Scope

This manifest covers the figures currently referenced by the compiled submission entrypoints:

- [main.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.tex)
- [supplementary_main.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary_main.tex)
- [supplementary.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex)

It is intended as a reviewer/archive-facing provenance map, not as a regeneration script.

## Main Manuscript Figures

### Figure 1 — system architecture
- LaTeX source: [03_methodology.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/03_methodology.tex#L13)
- Asset type: inline TikZ / manual schematic
- External data dependency: none
- Generator script: none

### Figure 2 — weight mapping schematic
- LaTeX source: [03_methodology.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/03_methodology.tex#L89)
- Asset type: inline TikZ / manual schematic
- External data dependency: none
- Generator script: none

### `fig4_accuracy_comparison`
- Included at: [05_results.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex#L31)
- Figure asset: [fig4_accuracy_comparison.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig4_accuracy_comparison.pdf)
- Generator: [plot_paper_figures.py](/home/qiaosir/projects/compute_vit/paper/plot_paper_figures.py#L469)
- Primary data files:
  - [tinyvit_v1_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_v1_results_gpt.json)
  - [tinyvit_v2v7_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_v2v7_results_gpt.json)
  - [tinyvit_cifar100_v134_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_cifar100_v134_results_gpt.json)
  - [tinyvit_flowers102_v134_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_flowers102_v134_results_gpt.json)
  - [convnext_full_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/convnext_full_results_gpt.json)
  - [resnet18_results.json](/home/qiaosir/projects/compute_vit/report_md/json/resnet18_results.json)
- Statistical note:
  - mixed-source summary figure
  - some bars reflect Monte Carlo averages with uncertainty bars
  - some entries remain best-checkpoint summaries rather than uniform 10-run MC rows

### `fig5_hat_recovery`
- Included at: [05_results.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex#L38)
- Figure asset: [fig5_hat_recovery.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig5_hat_recovery.pdf)
- Generator: [plot_paper_figures.py](/home/qiaosir/projects/compute_vit/paper/plot_paper_figures.py#L690)
- Primary data files:
  - [tinyvit_v1_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_v1_results_gpt.json)
  - [tinyvit_v2v7_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_v2v7_results_gpt.json)
  - [tinyvit_cifar100_v134_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_cifar100_v134_results_gpt.json)
  - [tinyvit_flowers102_v134_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_flowers102_v134_results_gpt.json)
  - [convnext_full_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/convnext_full_results_gpt.json)
  - [resnet18_results.json](/home/qiaosir/projects/compute_vit/report_md/json/resnet18_results.json)
- Statistical note:
  - derived delta/recovery figure built from the same locked result tables as `fig4`

### `fig_contour_map`
- Included at: [05_results.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex#L73)
- Figure asset: [fig_contour_map.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig_contour_map.pdf)
- Generator: [plot_paper_figures.py](/home/qiaosir/projects/compute_vit/paper/plot_paper_figures.py#L1341)
- Primary data file:
  - [iso_accuracy_contour_data.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/iso_accuracy_contour_data.json)
- Statistical note:
  - 63-point `sigma_D2D x ADC` grid
  - 10 Monte Carlo runs per grid point under the canonical sweep settings used in the paper

### `figS3_ensemble_hat`
- Included at: [05_results.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex#L85)
- Figure asset: [figS3_ensemble_hat.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/figS3_ensemble_hat.pdf)
- Generator: [plot_paper_figures.py](/home/qiaosir/projects/compute_vit/paper/plot_paper_figures.py#L579)
- Provenance note:
  - left-side panels are conceptual diagrams drawn directly in the plotting script
  - right-side accuracy values (`10.00%`, `86.37 ± 1.54%`) are the locked fresh-instance transfer numbers summarized in the paper text
- Audit/supporting data files:
  - [fresh_instance_eval.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/fresh_instance_eval.json)
  - [ensemble_frequency_ablation.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/ensemble_frequency_ablation.json)

### `fig10_zero_shot_transferability`
- Included at: [05_results.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex#L123)
- Figure asset: [fig10_zero_shot_transferability.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig10_zero_shot_transferability.pdf)
- Generator: [plot_paper_figures.py](/home/qiaosir/projects/compute_vit/paper/plot_paper_figures.py#L1197)
- Primary data file:
  - [device_comparison_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/device_comparison_results_gpt.json)
- Statistical note:
  - mixed-device profile comparison figure
  - main-text quantitative claim anchored to the literature-calibrated OPECT row (`88.53%`)

## Supplementary Figures With External Data Dependencies

### `fig_proxy_sensitivity_map`
- Included at: [supplementary.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex#L99)
- Figure asset: [fig_proxy_sensitivity_map.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig_proxy_sensitivity_map.pdf)
- Generator: [plot_paper_figures.py](/home/qiaosir/projects/compute_vit/paper/plot_paper_figures.py#L1435)
- Primary data file:
  - [zhang_sensitivity_sweep_10mc.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/zhang_sensitivity_sweep_10mc.json)

### `fig_sobol_sensitivity`
- Included at: [supplementary.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex#L142)
- Figure asset: [fig_sobol_sensitivity.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig_sobol_sensitivity.pdf)
- Generator: [plot_paper_figures.py](/home/qiaosir/projects/compute_vit/paper/plot_paper_figures.py#L1643)
- Primary data file:
  - [sobol_sensitivity.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/sobol_sensitivity.json)

### `fig9_noise_sensitivity`
- Included at: [supplementary.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex#L223)
- Figure asset: [fig9_noise_sensitivity.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig9_noise_sensitivity.pdf)
- Generator: [plot_paper_figures.py](/home/qiaosir/projects/compute_vit/paper/plot_paper_figures.py#L1040)
- Primary data file:
  - [noise_sweep_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/noise_sweep_results_gpt.json)

### `fig_fresh_instance_ablation`
- Included at: [supplementary.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex#L230)
- Figure asset: [fig_fresh_instance_ablation.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig_fresh_instance_ablation.pdf)
- Generator: [plot_paper_figures.py](/home/qiaosir/projects/compute_vit/paper/plot_paper_figures.py#L1527)
- Primary data files:
  - [fresh_instance_eval.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/fresh_instance_eval.json)
  - [ensemble_frequency_ablation.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/ensemble_frequency_ablation.json)

### `fig_attention_maps`
- Included at: [supplementary.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex#L237)
- Figure asset: [fig_attention_maps.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig_attention_maps.pdf)
- Generator: [visualize_attention.py](/home/qiaosir/projects/compute_vit/visualize_attention.py)
- Metadata file:
  - [attention_maps_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json/attention_maps_gpt.json)
- Provenance note:
  - qualitative visualization generated from fixed CIFAR-10 sample indices and the locked V1 / V3 / V4 / V6 checkpoints

### `fig7_retention_curve`
- Included at: [supplementary.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex#L253)
- Figure asset: [fig7_retention_curve.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig7_retention_curve.pdf)
- Generator: [plot_paper_figures.py](/home/qiaosir/projects/compute_vit/paper/plot_paper_figures.py#L863)
- Primary data files:
  - [convnext_full_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/convnext_full_results_gpt.json)
  - [tinyvit_v4_retention_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_v4_retention_results_gpt.json)

### `fig6_physical_compensation`
- Included at: [supplementary.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex#L266)
- Figure asset: [fig6_physical_compensation.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig6_physical_compensation.pdf)
- Generator: [plot_paper_figures.py](/home/qiaosir/projects/compute_vit/paper/plot_paper_figures.py#L819)
- Primary data file:
  - [a23_experiment_results.json](/home/qiaosir/projects/compute_vit/report_md/json/a23_experiment_results.json)

### `fig3_snr_curves`
- Included at: [supplementary.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex#L273)
- Figure asset: [fig3_snr_curves.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig3_snr_curves.pdf)
- Generator: [plot_paper_figures.py](/home/qiaosir/projects/compute_vit/paper/plot_paper_figures.py#L446)
- Primary data source:
  - [a23_experiment_results.json](/home/qiaosir/projects/compute_vit/report_md/json/a23_experiment_results.json)
  - analytical reconstruction in [analog_layers.py](/home/qiaosir/projects/compute_vit/analog_layers.py)

### `fig8_pareto_energy_accuracy`
- Included at: [supplementary.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary.tex#L280)
- Figure asset: [fig8_pareto_energy_accuracy.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures/fig8_pareto_energy_accuracy.pdf)
- Generator: [plot_paper_figures.py](/home/qiaosir/projects/compute_vit/paper/plot_paper_figures.py#L935)
- Primary data files:
  - [tinyvit_v1_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_v1_results_gpt.json)
  - [tinyvit_v2v7_results_gpt.json](/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/tinyvit_v2v7_results_gpt.json)
  - [tinyvit_hybrid_dryrun_report_gpt.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/archive/md/tinyvit_hybrid_dryrun_report_gpt.md)
- Provenance note:
  - energy side is based on the archived dry-run report fallback currently used by the plotting script

## Practical Use

If a reviewer or collaborator asks where a figure came from, this file should be paired with:

- [SUBMISSION_BUNDLE_CHECKLIST_20260417.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/SUBMISSION_BUNDLE_CHECKLIST_20260417.md)
- [REVIEWER_ARCHIVE_MANIFEST_20260417.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/REVIEWER_ARCHIVE_MANIFEST_20260417.md)
