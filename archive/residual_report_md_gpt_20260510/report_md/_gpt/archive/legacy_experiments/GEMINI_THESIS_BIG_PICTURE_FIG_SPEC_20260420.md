# Thesis Big-Picture Figure Spec

**Purpose:** Frontispiece cover figure. One glance tells the full arc: device noise → overfitting → ensemble fix → safe deployment envelope.

**Concept:** 2×2 grid read left-to-right as a causal chain. Minimal vignettes with subtle arrows threading problem to solution to map.

---

## Panel Breakdown

**A — Device-level noise.** Crossbar array with colored conductance cells (viridis/plasma) and a Gaussian D2D distribution curve overlaid. σ symbol marks spread; red warning halo on outlier cells.

**B — Training-level overfitting.** Dual accuracy curve. Fixed-mask HAT (red) spikes to 88 % on training-instance validation, then crashes to 10 % on fresh instance. Ensemble HAT (dashed green) rises steadily to ~86 % on both.

**C — Ensemble HAT fix.** Horizontal strip of 10 narrow bars, one per fresh-instance realization, clustering around 86 % (±1.5 %). A lone red bar at 10 % labeled "fixed mask" sits far left for contrast.

**D — Deployment envelope.** 2D decision matrix: x-axis σ_D2D, y-axis NL severity. Smooth contour field with green (operational), yellow (degraded), red (collapse) zones. White star marks nominal design point.

## Visual Style
- **Palette:** Blues/greens good, reds/oranges danger. Add hatching for accessibility.
- **Type:** Sans-serif, axes ≤8 pt. Labels (A–D) bold 12 pt, top-left.
- **Flow:** Subtle gray arrows A→B→C→D. White background, vector output.

## ASCII Sketch

```
+----------------------------------+
|  A                |  B            |
|  [====|====]      |   /\    ___   |
|  [===|=====]  ~~  |  /  \  /   \  |
|  [====|====]  ||  | /    \/     \ |
|  [===|=====]  ||  |/  red  green~|
|  Gaussian      σ   |  88%   86%   |
|  crossbar          |  10%         |
+--------------------|--------------+
|  C                |  D            |
|  |||||||||||      |  GGG|YY|RR    |
|  |||||||||||      |  GGG|YY|RR    |
|  |||||||||||      |  GGY|YR|RR    |
|  |||||||||||      |  GYY|RR|RR    |
|  ★86%  ★86%       |  YYY|RR|RR    |
|  [red 10%]        |  ★nominal     |
|                    |  σ_D2D → NL ↑ |
+----------------------------------+
```

## Tool Recommendation
**TikZ (LaTeX)** is best: scales to full-page width, matches thesis fonts, and stays editable. Matplotlib can generate panels B–D if data regeneration is needed, but final assembly should be TikZ.

## Data Sources
- **A:** `figS2_nonideality.png`; D2D from `figS_corr_d2d.png` / `GEMINI_FIG_CORR_D2D_FINAL_SPEC_20260420.md`.
- **B:** `fig5_hat_recovery.pdf` generator; trajectories in `fresh_instance_eval.json`.
- **C:** `ensemble_hat_ablation_FIXED.json` (mean 86.57 %, std 1.66 %); contrast from `fresh_instance_eval.json`.
- **D:** `fig_contour_map.pdf` (`iso_accuracy_contour_data.json`). Swap ADC→NL severity via `plot_paper_figures.py`.
