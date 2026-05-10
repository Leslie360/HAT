# GEMINI G-Z4: D2D-Correlation Sensitivity Figure Spec — 2026-04-19

**Reread of canonical state:** I am specifying the visualization for the `CX-CA` full sweep data (ρ ∈ {0, 0.3, 0.5}) to evaluate how spatial correlation affects the fresh-instance transfer of Standard vs. Ensemble HAT.

## Figure Specification: Robustness to Spatial Correlation

**Type**: Clustered Error Bar Chart (or Dual-Line Chart with shaded variance).
**X-Axis**: Spatial Correlation Coefficient (ρ) — Categories: {0.0 (i.i.d.), 0.3, 0.5}.
**Y-Axis**: Fresh-Instance Accuracy (%) — Range: [0, 100], break in axis at 20-70 if needed.

### Sketch / Layout
```
Accuracy (%)
  ^
  |      [Ensemble HAT]       [Standard HAT]
90|---  (86.8 ± 1.5)             (10.0 ± 0.0)
  |          |                        |
80|---       *                        |
  |                                   |
..|                                   |
15|---                                *
10|---                                |
 0+------------------------------------------->
      ρ=0.0 (i.i.d)      ρ=0.3          ρ=0.5
```

### Aesthetic Requirements
- **Curves/Bars**:
  - **Ensemble HAT (V4)**: Blue solid line with circular markers. Shaded area for ±1σ ($n=50$ total evals: 10 arrays × 5 MC).
  - **Standard HAT (V4)**: Red dashed line with square markers.
- **Hatching**: Apply the "Option B" visual marker (diagonal hatch) to any single-run data points if the full sweep is not completed for all seeds.

### Caption Draft
**Figure SX. Spatial Correlation Robustness.** Comparison of fresh-instance transfer accuracy between Standard HAT and Ensemble HAT under varying degrees of spatial device-to-device (D2D) correlation (ρ). Standard HAT (red) exhibits deterministic collapse (10.0%) across all correlation regimes, indicating representational co-adaptation to the training instance. Ensemble HAT (blue) maintains >85% accuracy even at ρ=0.5, demonstrating that stochastic resampling during training effectively regularizes the model against spatially-structured hardware noise. Error bars/shading denote ±1σ across 10 fresh hardware instances.
