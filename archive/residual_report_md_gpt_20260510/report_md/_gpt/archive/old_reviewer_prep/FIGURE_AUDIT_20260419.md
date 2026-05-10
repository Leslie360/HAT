# Figure Audit Report
Date: 2026-04-19
Base directory: `/home/qiaosir/projects/compute_vit/paper/latex_gpt`
Figures directory: `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures`

**Total figure references found:** 17

## Summary Inventory

| Source | Filename | Exists | Format | Size (KB) | Dimensions | DPI | Color Flag | Caption Issues |
|--------|----------|--------|--------|-----------|------------|-----|------------|----------------|
| sections/05_results.tex | fig4_accuracy_comparison.pdf | Yes | .pdf (vector) | 14.7 | N/A | N/A | No | Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.). |
| sections/05_results.tex | fig5_hat_recovery.pdf | Yes | .pdf (vector) | 17.4 | N/A | N/A | No | Caption does not explicitly mention error bars or statistical annotations.; Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.). |
| sections/05_results.tex | fig_contour_map.pdf | Yes | .pdf (vector) | 31.8 | N/A | N/A | No | Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.). |
| sections/05_results.tex | figS3_ensemble_hat.pdf | Yes | .pdf (vector) | 31.6 | N/A | N/A | No | Caption does not explicitly mention error bars or statistical annotations.; Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.). |
| sections/05_results.tex | fig10_zero_shot_transferability.pdf | Yes | .pdf (vector) | 15.2 | N/A | N/A | No | Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.). |
| supplementary.tex | fig_proxy_sensitivity_map.pdf | Yes | .pdf (vector) | 16.7 | N/A | N/A | No | Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.). |
| supplementary.tex | fig_sobol_sensitivity.pdf | Yes | .pdf (vector) | 8.3 | N/A | N/A | No | None |
| supplementary.tex | fig9_noise_sensitivity.pdf | Yes | .pdf (vector) | 16.9 | N/A | N/A | No | Caption does not explicitly mention error bars or statistical annotations.; Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.). |
| supplementary.tex | fig_fresh_instance_ablation.pdf | Yes | .pdf (vector) | 16.8 | N/A | N/A | No | Caption does not explicitly mention error bars or statistical annotations.; Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.). |
| supplementary.tex | fig_attention_maps.pdf | Yes | .pdf (vector) | 1207.2 | N/A | N/A | No | Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.). |
| supplementary.tex | fig7_retention_curve.pdf | Yes | .pdf (vector) | 15.0 | N/A | N/A | No | Caption does not explicitly mention error bars or statistical annotations.; Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.). |
| supplementary.tex | fig6_physical_compensation.pdf | Yes | .pdf (vector) | 24.8 | N/A | N/A | No | Caption does not explicitly mention error bars or statistical annotations.; Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.). |
| supplementary.tex | fig3_snr_curves.pdf | Yes | .pdf (vector) | 14.5 | N/A | N/A | No | Caption does not explicitly mention error bars or statistical annotations.; Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.). |
| supplementary.tex | fig8_pareto_energy_accuracy.pdf | Yes | .pdf (vector) | 15.3 | N/A | N/A | No | Caption does not explicitly mention error bars or statistical annotations.; Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.). |
| supplementary.tex | figS1_asymmetry_concept.png | Yes | .png | 6115.1 | 1792x2400 | N/A | No | Caption does not explicitly mention error bars or statistical annotations. |
| supplementary.tex | figS2_nonideality.png | Yes | .png | 5462.6 | 2528x1696 | N/A | No | Caption does not explicitly mention error bars or statistical annotations.; Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.). |
| supplementary.tex | fig_nl_gradient_distortion.pdf | Yes | .pdf (vector) | 23.0 | N/A | N/A | No | None |

## Detailed Assessment per Figure

### fig4_accuracy_comparison.pdf
- **Source TeX:** `sections/05_results.tex`
- **Exists:** Yes
- **Readable:** Yes
- **Format:** .pdf (vector)
- **Size:** 14.7 KB
- **DPI:** Not specified in metadata
- **Color Accessibility Flag:** No prominent red/green clash detected (manual review still recommended).
- **Caption:** Cross-dataset accuracy under canonical deployment (4-bit quantization, 5\% C2C, 10\% D2D variability). Error bars denote $\pm 1$ standard deviation where Monte Carlo (MC) statistics are available; bars without visible error bars indicate deterministic baselines or currently available point estimates.
- **Caption Issues:**
  - Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.).

### fig5_hat_recovery.pdf
- **Source TeX:** `sections/05_results.tex`
- **Exists:** Yes
- **Readable:** Yes
- **Format:** .pdf (vector)
- **Size:** 17.4 KB
- **DPI:** Not specified in metadata
- **Color Accessibility Flag:** No prominent red/green clash detected (manual review still recommended).
- **Caption:** Accuracy degradation from FP32 to noisy deployment and HAT recovery. Tiny-ViT: 10-run MC; ConvNeXt: single-run estimates shown.
- **Caption Issues:**
  - Caption does not explicitly mention error bars or statistical annotations.
  - Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.).

### fig_contour_map.pdf
- **Source TeX:** `sections/05_results.tex`
- **Exists:** Yes
- **Readable:** Yes
- **Format:** .pdf (vector)
- **Size:** 31.8 KB
- **DPI:** Not specified in metadata
- **Color Accessibility Flag:** No prominent red/green clash detected (manual review still recommended).
- **Caption:** \textbf{Iso-accuracy contour map} for the Ensemble HAT Tiny-ViT model under joint $\sigma_{\mathrm{D2D}}$ and ADC precision sweep ($\sigma_{\mathrm{C2C}}=5\%$, $NL=1.0$, 10 MC runs per point). The 6-bit ADC cliff and the D2D-dominated degradation in the operational regime are visible.
- **Caption Issues:**
  - Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.).

### figS3_ensemble_hat.pdf
- **Source TeX:** `sections/05_results.tex`
- **Exists:** Yes
- **Readable:** Yes
- **Format:** .pdf (vector)
- **Size:** 31.6 KB
- **DPI:** Not specified in metadata
- **Color Accessibility Flag:** No prominent red/green clash detected (manual review still recommended).
- **Caption:** \textbf{Ensemble HAT concept.} Standard HAT reuses one fixed D2D mismatch map throughout training, whereas Ensemble HAT resamples the mismatch map each epoch. The fresh-instance transfer panel highlights the resulting generalization gap between the two training protocols.
- **Caption Issues:**
  - Caption does not explicitly mention error bars or statistical annotations.
  - Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.).

### fig10_zero_shot_transferability.pdf
- **Source TeX:** `sections/05_results.tex`
- **Exists:** Yes
- **Readable:** Yes
- **Format:** .pdf (vector)
- **Size:** 15.2 KB
- **DPI:** Not specified in metadata
- **Color Accessibility Flag:** No prominent red/green clash detected (manual review still recommended).
- **Caption:** \textbf{Zero-shot transfer across alternative device profiles.} Bars report the accuracy of standard-HAT checkpoints when evaluated on literature-calibrated or measured alternative device profiles without profile-specific retraining. ConvNeXt C4 retains partial transfer on the OPECT and idealized profiles but degrades sharply on phase-change memory (PCM) and resistive random-access memory (RRAM), whereas Tiny-ViT V4 collapses to chance level (10.00\%) across all shown alternatives. Dashed vertical lines mark the source-profile best accuracy, and unavailable architecture/profile combinations are labeled as n/a.
- **Caption Issues:**
  - Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.).

### fig_proxy_sensitivity_map.pdf
- **Source TeX:** `supplementary.tex`
- **Exists:** Yes
- **Readable:** Yes
- **Format:** .pdf (vector)
- **Size:** 16.7 KB
- **DPI:** Not specified in metadata
- **Color Accessibility Flag:** No prominent red/green clash detected (manual review still recommended).
- **Caption:** \textbf{Zhang-proxy C2C/D2D sensitivity sweep.} Cell annotations report the mean accuracy over \(10\) Monte Carlo evaluations at each operating point. The nominal proxy point \((\sigma_{\mathrm{C2C}}=2\%, \sigma_{\mathrm{D2D}}=3\%)\) is outlined. Across the tested range, accuracy changes are almost entirely driven by D2D mismatch, while the C2C axis remains flat to within the Monte Carlo uncertainty.
- **Caption Issues:**
  - Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.).

### fig_sobol_sensitivity.pdf
- **Source TeX:** `supplementary.tex`
- **Exists:** Yes
- **Readable:** Yes
- **Format:** .pdf (vector)
- **Size:** 8.3 KB
- **DPI:** Not specified in metadata
- **Color Accessibility Flag:** No prominent red/green clash detected (manual review still recommended).
- **Caption:** \textbf{First-order Sobol sensitivity indices derived from the contour sweep.} The left group reports indices over the full \(7 \times 9\) D2D--ADC grid, where ADC resolution dominates the variance budget. The right group restricts the analysis to the deployment-relevant operating region (\(\mathrm{ADC}\geq 6\) bits, \(\sigma_{\mathrm{D2D}}\leq 15\%\)), where the residual variance is driven primarily by D2D mismatch after readout precision has saturated.
- **Caption Issues:** None

### fig9_noise_sensitivity.pdf
- **Source TeX:** `supplementary.tex`
- **Exists:** Yes
- **Readable:** Yes
- **Format:** .pdf (vector)
- **Size:** 16.9 KB
- **DPI:** Not specified in metadata
- **Color Accessibility Flag:** No prominent red/green clash detected (manual review still recommended).
- **Caption:** \textbf{Continuous noise sensitivity and ADC sweep for the Tiny-ViT V4 checkpoint.} \textbf{Left:} mean accuracy heatmap under a continuous joint sweep of \(\sigma_{\mathrm{C2C}}\) and \(\sigma_{\mathrm{D2D}}\) in the uniform-noise regime. \textbf{Right:} ADC-bit sweep for the same checkpoint, highlighting the 6-bit knee and the saturation that follows. Only the model with available continuous-sweep data is shown; no placeholder panel is inserted for missing architectures.
- **Caption Issues:**
  - Caption does not explicitly mention error bars or statistical annotations.
  - Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.).

### fig_fresh_instance_ablation.pdf
- **Source TeX:** `supplementary.tex`
- **Exists:** Yes
- **Readable:** Yes
- **Format:** .pdf (vector)
- **Size:** 16.8 KB
- **DPI:** Not specified in metadata
- **Color Accessibility Flag:** No prominent red/green clash detected (manual review still recommended).
- **Caption:** \textbf{Fresh-instance robustness and D2D-resampling ablation.} \textbf{Left:} evaluation on \(10\) unseen fixed D2D realizations. Standard HAT collapses to chance on every fresh array (10.00\%), whereas Ensemble HAT preserves \(86.37 \pm 1.54\%\) accuracy across the same deployment set; the difference is overwhelming under a Welch two-sample test (\(p<10^{-15}\)). \textbf{Right:} exploratory held-out-accuracy scan under different D2D-resampling cadences during training. In this 50-epoch scan, epoch-level resampling reaches 88.41\%, exceeding fixed-mask training, slower refresh schedules, and the corresponding short-run per-batch perturbation control. The panel is intended to show that cadence matters, rather than to serve as the final paper-locked estimate for every schedule.
- **Caption Issues:**
  - Caption does not explicitly mention error bars or statistical annotations.
  - Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.).

### fig_attention_maps.pdf
- **Source TeX:** `supplementary.tex`
- **Exists:** Yes
- **Readable:** Yes
- **Format:** .pdf (vector)
- **Size:** 1207.2 KB
- **DPI:** Not specified in metadata
- **Color Accessibility Flag:** No prominent red/green clash detected (manual review still recommended).
- **Caption:** \textbf{Attention heatmaps for three representative CIFAR-10 samples across the main deployment regimes.} Columns show cat, truck, and automobile. Rows, from top to bottom, show the original input image, the V1 digital baseline, the V3 fixed-mask noisy deployment, the V4 hardware-aware trained deployment, and the V6 front-end-compensated deployment. Color intensity denotes normalized head-averaged attention response.
- **Caption Issues:**
  - Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.).

### fig7_retention_curve.pdf
- **Source TeX:** `supplementary.tex`
- **Exists:** Yes
- **Readable:** Yes
- **Format:** .pdf (vector)
- **Size:** 15.0 KB
- **DPI:** Not specified in metadata
- **Color Accessibility Flag:** No prominent red/green clash detected (manual review still recommended).
- **Caption:** \textbf{Retention decay under programmed weight drift.} Accuracy is plotted against time since programming for ConvNeXt C9 and Tiny-ViT V4 under dynamic scale recalibration with co-decay of the retained D2D buffers. Both models exhibit a rapid early drop followed by a broad plateau, indicating partial long-horizon viability under the present uniform double-exponential retention model.
- **Caption Issues:**
  - Caption does not explicitly mention error bars or statistical annotations.
  - Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.).

### fig6_physical_compensation.pdf
- **Source TeX:** `supplementary.tex`
- **Exists:** Yes
- **Readable:** Yes
- **Format:** .pdf (vector)
- **Size:** 24.8 KB
- **DPI:** Not specified in metadata
- **Color Accessibility Flag:** No prominent red/green clash detected (manual review still recommended).
- **Caption:** \textbf{Impact of frontend non-linearity and dark current.} Inverse-gamma compensation helps in dark regimes but amplifies noise elsewhere.
- **Caption Issues:**
  - Caption does not explicitly mention error bars or statistical annotations.
  - Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.).

### fig3_snr_curves.pdf
- **Source TeX:** `supplementary.tex`
- **Exists:** Yes
- **Readable:** Yes
- **Format:** .pdf (vector)
- **Size:** 14.5 KB
- **DPI:** Not specified in metadata
- **Color Accessibility Flag:** No prominent red/green clash detected (manual review still recommended).
- **Caption:** \textbf{Analytical SNR trends under inverse-gamma compensation derived from the frontend response model used in the simulator.}
- **Caption Issues:**
  - Caption does not explicitly mention error bars or statistical annotations.
  - Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.).

### fig8_pareto_energy_accuracy.pdf
- **Source TeX:** `supplementary.tex`
- **Exists:** Yes
- **Readable:** Yes
- **Format:** .pdf (vector)
- **Size:** 15.3 KB
- **DPI:** Not specified in metadata
- **Color Accessibility Flag:** No prominent red/green clash detected (manual review still recommended).
- **Caption:** \textbf{Energy--accuracy placement of the digital baseline and hybrid V2--V7 family.}
- **Caption Issues:**
  - Caption does not explicitly mention error bars or statistical annotations.
  - Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.).

### figS1_asymmetry_concept.png
- **Source TeX:** `supplementary.tex`
- **Exists:** Yes
- **Readable:** Yes
- **Format:** .png
- **Size:** 6115.1 KB
- **Dimensions:** 1792 x 2400 px
- **DPI:** Not specified in metadata
- **Color Accessibility Flag:** No prominent red/green clash detected (manual review still recommended).
- **Caption:** \textbf{Differential pair asymmetry concept.}
    Systematic mismatch between positive and negative branches
    (asymmetry factor $\alpha$) degrades the effective differential signal.
    Quantitative sensitivity analysis shows tolerance up to 1\% asymmetry
    with $<$2\% accuracy degradation, but nonlinear collapse beyond 2\%.
- **Caption Issues:**
  - Caption does not explicitly mention error bars or statistical annotations.

### figS2_nonideality.png
- **Source TeX:** `supplementary.tex`
- **Exists:** Yes
- **Readable:** Yes
- **Format:** .png
- **Size:** 5462.6 KB
- **Dimensions:** 2528 x 1696 px
- **DPI:** Not specified in metadata
- **Color Accessibility Flag:** No prominent red/green clash detected (manual review still recommended).
- **Caption:** \textbf{Physical non-idealities in resistive arrays.}
    (Left) IR drop causes position-dependent voltage loss along wordlines.
    (Right) Sneak paths create unintended current leakage through adjacent cells.
    Quantitative sensitivity analysis (Table~\ref{tab:nonideality-sensitivity})
    indicates these non-idealities degrade accuracy by $<$2.2\% for typical
    1--3\% effect magnitudes, suggesting the qualitative advantage is robust
    to moderate array-level effects.
- **Caption Issues:**
  - Caption does not explicitly mention error bars or statistical annotations.
  - Caption may not be standalone (lacks descriptive verb like 'shows', 'illustrates', etc.).

### fig_nl_gradient_distortion.pdf
- **Source TeX:** `supplementary.tex`
- **Exists:** Yes
- **Readable:** Yes
- **Format:** .pdf (vector)
- **Size:** 23.0 KB
- **DPI:** Not specified in metadata
- **Color Accessibility Flag:** No prominent red/green clash detected (manual review still recommended).
- **Caption:** \textbf{Group-wise gradient distortion under severe nonlinear write.} A deterministic diagnostic on the frozen Tiny-ViT V4 checkpoint compares the \texttt{NL=1.0} baseline against matched forward passes where \texttt{NL=2.0} is activated only for one analog module group at a time. Results aggregate eight CIFAR-10 train batches with preserved checkpoint D2D buffers and $\sigma_{\mathrm{C2C}}=0$ so that only the backward surrogate changes.
- **Caption Issues:** None

## Red Flags

- **SUSPICIOUSLY SMALL:** `fig_sobol_sensitivity.pdf` (8.3 KB) — may be broken or placeholder.
- **OVERSIZED:** `figS1_asymmetry_concept.png` (6115.1 KB) — consider compression or vector format.
- **MISSING DPI METADATA:** `figS1_asymmetry_concept.png` is a PNG but lacks embedded DPI. Ensure export at ≥300 DPI for print.
- **OVERSIZED:** `figS2_nonideality.png` (5462.6 KB) — consider compression or vector format.
- **MISSING DPI METADATA:** `figS2_nonideality.png` is a PNG but lacks embedded DPI. Ensure export at ≥300 DPI for print.

## Unreferenced Figure Files

The following 14 files exist in `/home/qiaosir/projects/compute_vit/paper/latex_gpt/figures` but are **not referenced** by any audited `.tex` file:

- `energy_breakdown_pie.png` (96.3 KB)
- `energy_breakdown_stacked.png` (99.0 KB)
- `fig11_energy_breakdown.pdf` (21.8 KB)
- `fig11_energy_breakdown.png` (98.9 KB)
- `fig1_system_architecture.pdf` (23.9 KB)
- `fig2_weight_mapping.pdf` (33.6 KB)
- `figA.png` (5889.4 KB)
- `figB.png` (5698.6 KB)
- `figC.png` (5764.7 KB)
- `figD.png` (6532.9 KB)
- `fig_attention_differences.pdf` (665.5 KB)
- `fig_attention_differences.png` (1424.5 KB)
- `fig_layer_sensitivity.png` (161.4 KB)
- `graphical_abstract.png` (7528.3 KB)

## Recommendations

1. **Missing Files:** Locate and add any missing figure files to the `figures/` directory.
2. **Oversized Images:** Replace large PNGs with vector PDFs where possible, or compress PNGs using tools like `pngquant`.
3. **Low DPI / Missing DPI:** For raster images intended for print, ensure PNG exports are at ≥300 DPI and embed the DPI metadata.
4. **Captions:** Ensure every figure caption explicitly describes error bars, shaded confidence intervals, or Monte Carlo bands.
5. **Color Accessibility:** Avoid red/green-only differentiation; add distinct markers, line styles, or hatching patterns.
6. **JPEG Avoidance:** Convert any JPEG diagrams to PNG or PDF to avoid compression artifacts.
7. **Unreferenced Files:** Review unreferenced files and either remove them or include them in the manuscript if they are needed.

---
*Report generated automatically. Manual review of color accessibility and caption completeness is still recommended.*
