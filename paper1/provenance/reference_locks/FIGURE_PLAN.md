# Paper Figure Plan

This file defines the paper-facing figure contract for Fig.3--Fig.12. Figures 1 and 2 remain manual schematic drawings and are therefore excluded from the automated pipeline. Their manual brief now lives in `paper/FIG1_FIG2_BRIEF_gpt.md`.
Caption-level wording that should remain stable during template migration now lives in `paper/FIGURE_CAPTION_LOCK_gpt.md`.
Draft submission-ready captions now live in `paper/FIGURE_CAPTION_DRAFTS_gpt.md`.

## Output Convention

- Script: `paper/plot_paper_figures.py`
- Output directory: `paper/figures/`
- Style: `seaborn-v0_8-paper`
- Font size: 12 pt
- Resolution: 300 DPI

## Figure Inventory

| Fig. | Output file | Purpose | Primary data source | Generation mode | Current status |
|:--:|:--|:--|:--|:--|:--|
| 3 | `fig3_snr_curves.png` | Analytical SNR-vs-intensity curves for inverse-gamma compensation | `report_md/json/a23_experiment_results.json` + physical model in `analog_layers.py` | Reconstructed analytically in Python | Ready now |
| 4 | `fig4_accuracy_comparison.png` | Cross-dataset grouped bar chart: ConvNeXt vs Tiny-ViT under FP32 / Standard-noise / HAT | CIFAR-10 final JSONs + Tiny-ViT multi-dataset JSONs + ConvNeXt Task 21 exports | Automated grouped bar chart with pending-bar tolerance | Ready now |
| 5 | `fig5_hat_recovery.png` | Cross-dataset degradation/recovery amplitudes with explicit FP32 references | Same as Fig.4 | Automated dual-panel delta chart with secondary-axis baselines | Ready now |
| 6 | `fig6_physical_compensation.png` | Physical compensation summary: Group 1 heatmap + Group 3 robustness bars | `report_md/json/a23_experiment_results.json` | Automated composite figure | Ready now |
| 7 | `fig7_retention_curve.png` | Retention decay comparison | `report_md/_gpt/json_gpt/convnext_full_results_gpt.json` and corrected Tiny-ViT V4 retention JSON | Automated uncertainty-band plot with explicit statistical annotation | Canonical V4 data ready |
| 8 | `fig8_pareto_energy_accuracy.png` | Accuracy-energy Pareto plot | `report_md/_gpt/tinyvit_hybrid_dryrun_report_gpt.md` plus model result JSONs | Automated scatter with placeholder support | Ready draft |
| 9 | `fig9_noise_sensitivity.png` | Accuracy heatmaps under continuous $(\sigma_{C2C}, \sigma_{D2D})$ sweeps | `noise_sweep_results_gpt.json` | Automated heatmap | Ready now |
| 10 | `fig10_zero_shot_transferability.png` | Cross-device zero-shot transferability comparison | `device_comparison_results_gpt.json` | Automated bar chart | Ready now |
| 11 | `fig11_energy_breakdown.png` | Energy breakdown summary (pie + stacked bar) | `report_md/_gpt/tinyvit_hybrid_dryrun_report_gpt.md`; future cross-model energy artifacts | Partial now, expandable later | Ready draft |
| 12 | `fig_attention_maps.png` | Attention-map degradation and recovery under analog noise | `visualize_attention.py` outputs from V1 / V3 / V4 / V6 checkpoints | Standalone qualitative visualization script | Ready now |

## Figure Notes

### Fig. 3
- This figure is not copied from the existing report PNG.
- The script reconstructs normalized SNR curves from the same inverse-gamma and shot-noise assumptions used in the paper text.
- It should be described in the caption as an analytical visualization of the compensation trade-off, not as a direct empirical measurement.

### Fig. 4
- This is now the main cross-dataset figure, following Claude/Gemini's recommendation.
- The canonical structure is:
  - 3 subpanels: CIFAR-10 / CIFAR-100 / Flowers-102
  - 2 architectures per panel: ConvNeXt-Tiny and Tiny-ViT-5M
  - 3 bars per architecture: FP32, Standard-noise, HAT
- The final manuscript version is now populated with the completed Task 21 ConvNeXt results.
- The pending-bar logic remains in the script only as a safety fallback for future reruns.

### Fig. 5
- This figure now focuses on *changes* rather than raw accuracy:
  - left panel: degradation from FP32 to Standard-noise
  - right panel: recovery from Standard-noise to HAT
- This makes the complexity-dependent role of HAT much clearer than a second raw-accuracy chart.
- To avoid hiding weak absolute baselines, each panel also overlays the corresponding FP32 absolute accuracies on a secondary axis.
- For Tiny-ViT, the paper wording must use `Standard train w/ fixed D2D` for V3 rather than treating V3 as identical to ConvNeXt C3.

### Fig. 6
- Left panel: heatmap of Group 1 compensation gain $\Delta = \text{Acc}_{\text{comp}} - \text{Acc}_{\text{raw}}$ over $\gamma_{\text{phys}} \times I_{\text{dark}}$.
- Right panel: Group 3 robustness summary using clean accuracy and mean corruption error (mCE).

### Fig. 7
- ConvNeXt C9 and corrected Tiny-ViT V4 retention are both available.
- The legacy V7 retention reevaluation exists only as a superseded checkpoint note and should not be plotted as a canonical curve.
- Current visual grammar:
  - two retention curves with uncertainty bands
  - dashed/log-like time spacing with explicit `t=0` anchor
  - shaded early-time region to emphasize the rapid initial drop before the long-time plateau
  - band meaning explicitly labeled as `±1 std` across Monte Carlo runs

### Fig. 8
- Tiny-ViT V1--V6 canonical accuracy data are available.
- A fuller Pareto figure may still benefit from model-specific energy exports for ResNet and ConvNeXt, but the current draft is no longer blocked on Tiny-ViT.

### Fig. 9
- This figure is reserved for the continuous noise-sensitivity sweep introduced in Task 11.
- Tiny-ViT V4 data are available now; a ConvNeXt companion panel can be added if a matching sweep is exported later.
- Current visual grammar:
  - left/middle: annotated heatmap panels with a shared color scale when multiple models are available
  - right: ADC sensitivity curve with a marked `6-bit` knee
  - if only one model has continuous-noise data, the figure should show the available heatmap only and must not fabricate a placeholder heatmap for the missing model

### Fig. 10
- This figure must be described as `Zero-Shot Hardware Transferability`, not as a universal cross-device peak-performance comparison.
- The underlying experiment loads organic-HAT checkpoints and evaluates them under alternative device profiles at inference time.
- Current data already support this figure.
- Current visual grammar:
  - one horizontal-panel comparison per architecture
  - dashed source-checkpoint reference line in each panel
  - both panels should show the device-profile labels to keep cross-panel scanning easy
  - missing architecture/profile combinations should be labeled explicitly as `n/a`, not left as unlabeled blank rows
  - short caption note clarifying that this is transferability, not device-specific peak optimization

### Fig. 11
- The current script should already render the Tiny-ViT dry-run energy breakdown as:
  - a pie chart of analog MAC / ADC / DAC / digital MAC / special ops / buffer
  - a stacked-bar comparison between the hybrid total and the FP32 reference
- Future revisions may add ConvNeXt and ResNet breakdowns once matching profiler outputs are exported in machine-readable form.

### Fig. 12
- This figure is intentionally qualitative and is produced by the standalone `visualize_attention.py` script rather than the batch `plot_paper_figures.py` pipeline.
- The default comparison is now V1 vs V3 vs V4 vs V6 on a small fixed set of CIFAR-10 test images.
- Export at 300 DPI or better because the figure is often placed near full page width in the supplement.
- A companion difference-map output is allowed even if only `fig_attention_maps.png` is cited in the main paper.

## Planned Follow-up

1. Draw `Fig.1` and `Fig.2` from the manual brief in `paper/FIG1_FIG2_BRIEF_gpt.md`.
2. Keep Fig.7 canonical: ConvNeXt C9 plus corrected Tiny-ViT V4 retention only.
3. Export additional model energy breakdown data if a multi-model Fig.11 comparison is desired.
4. Optionally regenerate Fig.12 with more class-diverse CIFAR-10 samples for aesthetics.
5. Refresh Fig.4-Fig.11 only if new external-data experiments are added, such as ImageNet eval-only or measured-device profiles.

<!-- DATA_DEPENDENCY: Most Tiny-ViT-facing artifacts are now available. Remaining optional upgrades are figure polish, additional cross-model energy exports, and any future corrected retention-aware retraining. -->
