# GEMINI R11B-1: Figure Inventory & Audit
**Date:** 2026-04-26
**Author:** Gemini
**Status:** COMPLETE

## 1. Directory Inventory (`paper/latex_gpt/figures/*.pdf`)
There are 28 unique PDFs in the root figures directory, plus 3 TikZ rebuilds in `tikz/`.

**Orphan PDFs (exist in folder, but NOT included in any `.tex` via `\includegraphics`):**
1. `fig11_energy_breakdown.pdf`
2. `figS_cross_host_parity.pdf`
3. `figS_standard_hat_postfix_mseries_distribution_20260426.pdf`
4. `fig_attention_differences.pdf`

## 2. In-Text Reference Audit

### Main Text (`sections/05_results.tex`, `06_discussion.tex`)
**Included via `\includegraphics`:**
1. `fig4_accuracy_comparison.pdf` — **ORPHAN REF:** Included with `\label{fig:accuracy-comparison}`, but **NEVER** referenced in the text (Kimi deleted the sentence "Figs 4-5" during R9A surgery).
2. `fig5_hat_recovery.pdf` — **ORPHAN REF:** Included with `\label{fig:hat-recovery}`, but **NEVER** referenced.
3. `fig_contour_map.pdf` — Referenced as `Figure \ref{fig:contour-map}`. (Valid)
4. `figS3_ensemble_hat.pdf` — Referenced as `Figure \ref{fig:ensemble-hat-concept}`. (Valid)
5. `fig10_zero_shot_transferability.pdf` — Referenced as `Figure \ref{fig:case-study-transfer}`. (Valid)

*Note on Main Text numbering:* Because Kimi removed the references to Fig 4 and 5, but left the `\begin{figure}` blocks, LaTeX is blindly numbering them 1, 2, 3, 4, 5 based on insertion order. The numbering is contiguous in the PDF, but the filenames (4, 5, 10, S3) are completely divorced from the actual flow.

### Supplementary Text (`supplementary.tex`, `S_mechanism_empirical.tex`)
**Included via `\includegraphics`:**
1. `fig1_system_architecture.pdf`
2. `fig2_weight_mapping.pdf`
3. `fig3_snr_curves.pdf`
4. `fig6_physical_compensation.pdf`
5. `fig7_retention_curve.pdf`
6. `fig8_pareto_energy_accuracy.pdf`
7. `fig9_noise_sensitivity.pdf`
8. `fig_attention_maps.pdf`
9. `fig_fresh_instance_ablation.pdf`
10. `fig_nl_gradient_distortion.pdf`
11. `fig_proxy_sensitivity_map.pdf`
12. `fig_sobol_sensitivity.pdf`
13. `figS_standard_hat_collapse_mechanism.pdf`
14. `figS_d2d_loss_landscape.pdf`
15. `figS_per_layer_sensitivity.pdf`
16. `figS_hessian_spectrum.pdf`
17. `figS_cka_mseries.pdf`
18. `figS_checkpoint_avg.pdf`
19. `figS_corr_d2d.pdf`

**Missing PDFs (Included in `.tex` but no PDF found):**
1. `figS1_asymmetry_concept` (Line 575 in `supplementary.tex`)
2. `figS2_nonideality` (Line 625 in `supplementary.tex`)

*(Note: These missing PDFs might cause LaTeX compilation errors if they aren't generated or commented out).*

## 3. Renumbering Plan (Recommendation for R11C)

**Action for Kimi (R11C):**
1. **Delete** the `\begin{figure}` blocks for `fig4_accuracy_comparison` and `fig5_hat_recovery` from `05_results.tex`. Since the text no longer discusses them, they are wasting space and inflating the word/page count.
2. If those two are deleted, the Main Text will cleanly have exactly **3 Figures**:
   - **Fig 1**: `fig_contour_map` (Iso-accuracy)
   - **Fig 2**: `figS3_ensemble_hat` (Ensemble HAT concept)
   - **Fig 3**: `fig10_zero_shot_transferability` (OPECT Zero-shot)
   - *(Note: We will add the R11D AIHWKit Envelope Plot later as Fig 4)*.
3. Move `fig1_system_architecture` and `fig2_weight_mapping` entirely to the Supplementary Materials.
4. Rename all `\SuppFig...` macros to match a contiguous S1, S2, S3 sequence.
5. Resolve the missing `figS1_asymmetry_concept.pdf` and `figS2_nonideality.pdf` (either remove the includes or have Gemini regenerate them).
