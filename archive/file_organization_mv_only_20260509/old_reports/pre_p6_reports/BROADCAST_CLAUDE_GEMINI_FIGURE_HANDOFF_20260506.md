# Broadcast: Paper-1 Figure Visual Handoff to Gemini

**Date:** 2026-05-06 14:14 CST
**From:** Claude
**To:** Gemini (critic/aesthetic reviewer)
**Subject:** Paper-1 remaining figure styling — handoff

---

## 1. What Claude Already Did

Batch B/C/D 4 new figures (`paper2_aihwkit_baseline/figures/`):
- `r11d_drift_comparison_all_configs.{pdf,png}`
- `r11d_precision_drift_scatter.{pdf,png}`
- `r11d_source_fresh_drift_bars.{pdf,png}`
- `r11d_training_curves_overlay.{pdf,png}`

All regenerated with Codex visual standards:
- Tinos font via `/usr/share/fonts/truetype/croscore/Tinos-*.ttf`
- Colorblind-safe palette (`#0072B2`, `#D55E00`, `#009E73`, `#E69F00`)
- Light grid (`#E1E6EB`, lw=0.55, alpha=0.65)
- Bold labels, spine-off top/right, fonttype=42 for PDF

Main-text figures re-run via `paper/plot_paper_figures.py` and copied to `paper/latex_gpt/figures/`:
- fig3–fig10, figS3, figS_corr_d2d, fig_proxy_sensitivity_map

fig1 + fig2 re-run:
- `scripts/_gpt/plot_paper1_spine.py`
- `scripts/_gpt/plot_paper1_decision_map.py` (fixed CSV newline bug)

fig_nl_gradient_distortion was already updated by Codex on May 6.

## 2. What Remains for Gemini

**Needs torch (not available in current Claude env):**
- `figS_standard_hat_collapse_mechanism` — `scripts/_gpt/run_r10b.py`
- `figS_per_layer_sensitivity` — `scripts/_gpt/empirical_mechanism_20260425.py`
- `figS_d2d_loss_landscape` — same
- `figS_hessian_spectrum` — same
- `figS_cka_mseries` — same
- `figS_checkpoint_avg` — same
- `fig_attention_maps` — `scripts/oneshot_root/visualize_attention.py`
- `fig_attention_differences` — same

**Needs data (missing source files):**
- `fig11_energy_breakdown` — needs `tinyvit_hybrid_dryrun_report_gpt.md`
- `fig_contour_map` — needs `iso_accuracy_contour_data.json`
- `fig_fresh_instance_ablation` — needs `fresh_instance_eval.json` + `ensemble_frequency_ablation.json`
- `fig_sobol_sensitivity` — needs `sobol_sensitivity.json`

**Legacy TikZ/manual figures (may need visual audit):**
- `fig1_system_architecture.pdf` (May 2)
- `fig2_weight_mapping.pdf` (Apr 26)
- `figS1_asymmetry_concept` (Codex already repaired layout)

## 3. Action Requested

Please review the remaining figures for visual consistency with the Codex standard:
1. If you have GPU/torch access, regenerate the torch-dependent SI figures with updated style.
2. If source data exists for the skipped figures, regenerate them.
3. Do a pass over all `paper/latex_gpt/figures/*.pdf` for font/color consistency.

Script locations and color constants are in:
- `scripts/_gpt/plot_paper1_spine.py` (COL dict + rcParams)
- `paper/plot_paper_figures.py` (configure_style function)

---

*Broadcast auto-written by Claude per user instruction. No ask-before-write.*
