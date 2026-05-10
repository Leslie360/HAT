# Thesis Big-Picture Figure Spec v2

**Purpose:** Frontispiece cover figure. One glance shows the full arc: device noise → overfitting → ensemble recovery → severe-NL ceiling → deployment envelope with hard limits.

**Concept:** 2×2 grid read left-to-right as causal chain. Show both what works and what fails.

---

## Panel Breakdown

**A — Device-level noise.** Crossbar array with colored conductance cells and Gaussian D2D curve overlaid. σ marks spread; red halo on outliers. Inset shows nonlinear IV curve separating mild from severe regimes.

**B — Training trajectories (THREE curves).** Fixed-mask HAT (solid red): 88 % → 10 % collapse. Ensemble HAT mild NL (dashed green): steady rise to ~86 %. Severe-NL mitigations (dot-dash orange): plateau at ~30 %, labeled "NL ≥ 2.0 ceiling." Semi-transparent variance bands.

**C — Distribution contrast.** Top strip: bars clustering at 86 % (±1.5 %). Bottom strip: cluster near 30 %, "severe NL." Lone red bar at 10 % far left, "fixed mask." Gray divider between strips.

**D — Deployment envelope with do-not-ship zone.** x-axis σ_D2D, y-axis NL severity. Green/yellow/red zones. Bold red band at NL ≥ 2.0: "DO NOT SHIP — structural ceiling." White star at nominal; gray star in red zone: "measured ceiling, ~30 %." Hatching in red zone.

## Visual Style
Blues/greens good, reds/oranges danger, gray for limits. Sans-serif, axes ≤8 pt, labels bold 12 pt. Subtle gray arrows A→B→C→D. White background, vector output.

## ASCII Sketch

```
+------------------------------------------+
|  A                  |  B                  |
|  [====|====]        |   /\        ___     |
|  [===|=====]  ~~    |  /  \  ~  /   \    |
|  [====|====]  ||    | / gr \~ / oran \   |
|  [===|=====]  ||    |/  86%  X   30%   \  |
|  Gaussian  IV inset |  red 88%→10%      |
|  crossbar   σ       |  (three curves)    |
+---------------------|--------------------+
|  C                  |  D                  |
|  ||||||||||| 86%    |  GGG|YY|RRRRRR     |
|  ||||||||||| 86%    |  GGG|YY|RRRRRR     |
|  --------- divider  |  GGY|YR|RRRRRR     |
|  ||||| 30% severe   |  GYY|RR|DO NOT SHIP|
|  [red 10%] fixed    |  YYY|RR|≥2.0 zone  |
|                     |  ★nom  ☒ceiling~30%|
|                     |  σ_D2D →   NL ↑    |
+------------------------------------------+
```

## Tool & Data
**TikZ (LaTeX)** with `pgfplots` for the three-curve panel. Matplotlib regenerates B and D if needed.

**Data:** A: `figS2_nonideality.png`, `figS_corr_d2d.png`. B: `fresh_instance_eval.json` (red), `ensemble_hat_ablation_FIXED.json` (green), severe-NL sweep logs (orange). C: `ensemble_hat_ablation_FIXED.json` (86.57 % ± 1.66 %), `v4_nl2_*_results_gpt.md` (severe NL). D: `iso_accuracy_contour_data.json`, extended to NL ≥ 2.0 via `plot_paper_figures.py`.
