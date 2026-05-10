# Figure / Caption Publication Audit — 2026-04-17

**Scope:** Audit main-text and high-value supplementary figures from a reviewer/editor perspective.
**Assets inspected:** `paper/latex_gpt/figures/*.png`, `main.tex`, `supplementary.tex`, `05_results.tex`.

---

## Main-Text Figures

### Figure 1 — `fig1_system_architecture`
*Not inspected visually in this audit; assumed schematic.*
**Caption (assumed):** Usually describes the hybrid analog–digital pipeline.
**Status:** No known issue from source audit.

### Figure 2 — `fig2_weight_mapping`
*Not inspected visually; assumed schematic of differential conductance mapping.*
**Status:** No known issue from source audit.

### Figure 3 — `fig_contour_map` (Iso-accuracy contour map)
- **Self-contained?** ✅ Yes. Caption states ADC resolution, D2D sweep grid, C2C=5%, NL=1.0, and 10 MC runs per point.
- **Axes/labels?** ✅ Clean serif typography; color bar labeled “Accuracy (%)”; contour lines annotated with 80%, 85%, 88% thresholds.
- **Missing conditions?** None apparent.
- **Slideware risk?** Low. The heatmap is publication-grade; legend is outside the plot area, avoiding overlap.
- **Claim strength vs. visible support?** Matched. The 6-bit cliff and D2D-dominated operational regime are both visible in the data.

### Figure 4 — `fig4_accuracy_comparison`
- **Self-contained?** ✅ Mostly. Caption defines error bars and notes that bars without visible error bars are deterministic baselines or point estimates.
- **Axes/labels?** ✅ Panel labels (a) CIFAR-10, (b) CIFAR-100, (c) Flowers-102 are clear. Legend uses FP32 / Standard-noise / HAT.
- **Missing conditions?** ⚠️ The Flowers-102 panel shows very short red/green bars for ConvNeXt (near 0%). The caption does not explicitly name the ConvNeXt baseline as a single-run estimate *inside* the figure caption (that caveat lives in the body text and in Table 1). A one-line caveat in the caption would make the panel self-contained.
- **Slideware risk?** Low. The bar charts are clean and color-blind safe (blue/red/green).
- **Claim strength?** The +0.5 pp label on ConvNeXt Flowers-102 is correct but visually tiny; this is consistent with the low-data stress-test framing in the text.

### Figure 5 — `fig5_hat_recovery`
- **Self-contained?** ✅ Yes. Dual-axis design is explained: left = accuracy change (pp), right = FP32 accuracy (%).
- **Axes/labels?** ✅ Clean; numerical labels on bars are legible.
- **Missing conditions?** The right-hand panel (HAT recovery) shows ConvNeXt CIFAR-100 with a +36.5 pp jump. The corresponding left-hand degradation bar for Tiny-ViT Flowers-102 is –93.2 pp, which is visually dramatic but numerically accurate.
- **Slideware risk?** Low. Codex already fixed a prior overflow issue with the +36.5 label; current layout has adequate headroom.
- **Claim strength?** Matched. The figure visibly supports the text claim that HAT recovery is largest on CIFAR-100.

### Figure 6 — `figS3_ensemble_hat` (Ensemble HAT concept)
- **Self-contained?** ✅ Yes. Three sub-panels clearly show Standard HAT, Ensemble HAT, and fresh-instance transfer.
- **Axes/labels?** ✅ Dot plot with mean ± std is easy to read.
- **Missing conditions?** None.
- **Slideware risk?** Very low. The schematic is paper-quality rather than slide-quality.
- **Claim strength?** The gap between 10.00% and 86.37% is immediately visible.

### Figure 7 — `fig10_zero_shot_transferability` (Case-study transfer)
- **Self-contained?** ⚠️ Partial. The caption reads: *"Zero-shot transfer across alternative device profiles. Tiny-ViT trained with standard HAT collapses to chance level (10.00%) when evaluated on literature-calibrated or measured profiles... whereas Ensemble HAT recovers >80% accuracy across the profiled regimes."*
- **Visible support vs. caption claim:** ❌ **Mismatch.** The right-hand panel (Tiny-ViT V4) shows *only* standard-HAT bars, all at 10.0%. It does **not** show any Ensemble HAT bars. Therefore the figure artwork itself does not visibly demonstrate the "whereas Ensemble HAT recovers >80%" clause—that evidence lives in supplementary `fig_fresh_instance_ablation`. The caption should either (a) remove the Ensemble HAT clause from this figure’s caption, or (b) add a sentence referencing the supplementary figure where the recovery is actually plotted.
- **Axes/labels?** ✅ Clear horizontal bar layout; "source best" dashed line is a useful visual anchor.

---

## High-Value Supplementary Figures

### Supplementary Figure S3 — `fig9_noise_sensitivity`
**Caption:** *"Continuous noise sensitivity and ADC sweep."*
- **Self-contained?** ⚠️ Weak. The caption is only three words and does not state which model, dataset, or noise mode is shown. A reader flipping through the supplement cannot interpret the figure without returning to the main text.
- **Fix:** Expand to something like *"Continuous noise sensitivity and ADC bit-width sweep for Tiny-ViT V4 on CIFAR-10 under canonical uniform-noise deployment."*

### Supplementary Figure S4 — `fig_fresh_instance_ablation`
**Caption:** *"Fresh-instance robustness and D2D-resampling ablation. Left: evaluation on 10 unseen fixed D2D realizations... Right: held-out accuracy under different D2D-resampling cadences..."*
- **Self-contained?** ✅ Excellent. Both panels, sample sizes, and statistical summary are described.
- **Visual quality?** ✅ Clean dot plot and bar chart; the per-batch bar (86.16%) is correctly distinguished from per-epoch (88.41%).

### Supplementary Figure S5 — `fig_proxy_sensitivity_map`
**Caption:** *"Zhang-proxy C2C/D2D sensitivity sweep..."*
- **Self-contained?** ✅ Yes. Annotated cell values and nominal-point outline make the figure interpretable without the text.

### Supplementary Figure S6 — `fig_sobol_sensitivity`
**Caption:** *"First-order Sobol sensitivity indices derived from the contour sweep."*
- **Self-contained?** ⚠️ Could be stronger. The figure shows two bars (full grid vs. operational region) but does not label the exact parameter ranges on the figure itself. The caption mentions the operational region restriction (≥6-bit, σ_D2D ≤ 15%) which is essential context.
- **Fix:** Add a subtitle or annotation inside the figure panels stating the restricted domain for the right-hand bar.

### Supplementary Figure S7 — `fig_attention_maps`
**Caption:** *"Attention heatmaps for three representative CIFAR-10 samples under the digital baseline, fixed-mask noisy deployment, uniform-noise HAT, and front-end-compensated deployment. Columns show cat, truck, and automobile; rows show the four deployment regimes."*
- **Self-contained?** ❌ **No.** The figure artwork has **five** rows (Original, V1, V3, V4, V6), but the caption says *"rows show the four deployment regimes"* and omits the mapping between V-labels and regime names (V1 = digital baseline, V3 = fixed-mask noisy, V4 = uniform-noise HAT, V6 = front-end compensated). A reader cannot unambiguously identify which row corresponds to which regime without external knowledge.
- **Fix options:** (a) Add row labels directly on the figure (e.g., replace "V1" with "Digital baseline"), or (b) rewrite the caption to list the row order explicitly: *"Rows show, from top to bottom: the original input image, the digital baseline (V1), fixed-mask noisy deployment (V3), uniform-noise HAT (V4), and front-end-compensated deployment (V6)."*

### Supplementary Figure S8 — `fig_attention_differences`
*Not visually inspected, but by analogy with S7, check that any V-labels are mapped to regime names in the caption.*
**Status:** Flag for verification.

### Supplementary Figure S9 — `fig7_retention_curve`
**Caption:** *"Corrected Tiny-ViT V4 retention curve."*
- **Self-contained?** ⚠️ The word "corrected" is meaningful to the authors but may confuse a reviewer who did not see the prior draft. The caption should state what is corrected (earlier V7/V8 curves used a different recalibration).
- **Fix:** Change to *"Retention accuracy vs. time for the corrected Tiny-ViT V4 ensemble-HAT model, including dynamic scale recalibration and co-decay of D2D buffers."*

### Supplementary Figure S10 — `fig6_physical_compensation`
**Caption:** *"Impact of frontend non-linearity and dark current. Inverse-gamma compensation helps in dark regimes but amplifies noise elsewhere."*
- **Self-contained?** ✅ Acceptable. The two sub-panels (ResNet R4 and Tiny-ViT V6) are visually labeled.

### Supplementary Figure S11 — `fig3_snr_curves`
**Caption:** *"Analytical SNR trends under inverse-gamma compensation..."*
- **Self-contained?** ✅ Yes.

### Supplementary Figure S12 — `fig8_pareto_energy_accuracy`
**Caption:** *"Energy–accuracy placement of the digital baseline and hybrid V2–V7 family."*
- **Self-contained?** ⚠️ The V-labels (V2, V4, V6, etc.) appear on the plot but the caption does not map them to model names or regimes. A brief mapping sentence would help.

### Supplementary Figure S13 — `figS1_asymmetry_concept`
**Caption:** *"Differential pair asymmetry concept..."*
- **Self-contained?** ✅ The schematic + table combination is clear.

### Supplementary Figure S14 — `figS2_nonideality`
**Caption:** *"Physical non-idealities in resistive arrays..."*
- **Self-contained?** ✅ The left/right schematic labels are visible in the artwork.

### Supplementary Figure S15 — `fig_nl_gradient_distortion`
**Caption:** *"Group-wise gradient distortion under severe nonlinear write."*
- **Self-contained?** ⚠️ The caption names the groups (MLP, All analog, Patch Embed, etc.) but the figure axis abbreviations may not be instantly readable at small size. Ensure axis labels are large enough in the final PDF.

---

## Top 5 Figure/Caption Fixes Still Worth Doing

Ordered by **impact / effort ratio**:

1. **`fig_attention_maps` (S7) — Add row-to-regime mapping.**
   *Impact:* High (reviewers will look at attention maps; confusion here is embarrassing).
   *Effort:* Low (caption rewrite only, or simple row-label overlay).

2. **`fig10_zero_shot_transferability` (Main Fig 7) — Soften caption claim.**
   *Impact:* High (caption currently claims Ensemble HAT recovery that is not plotted in this figure).
   *Effort:* Low (one sentence edit in `05_results.tex`).

3. **`fig9_noise_sensitivity` (S3) — Expand vague three-word caption.**
   *Impact:* Medium (supplementary figure with no context looks unprofessional).
   *Effort:* Low.

4. **`fig7_retention_curve` (S9) — Remove ambiguous "corrected" adjective.**
   *Impact:* Medium (avoids reviewer confusion about what was wrong before).
   *Effort:* Low.

5. **`fig_sobol_sensitivity` (S6) — Annotate operational-region panel.**
   *Impact:* Medium (makes the restricted-domain bar self-explanatory).
   *Effort:* Low.

---

*End of audit.*
