# CODEX CX Figure Summary 20260423

**Script path:** `scripts/_gpt/plot_structural_limit_signature.py`

**Outputs:**
- `images_gpt/fig_structural_limit_signature.png` (300 dpi)
- `images_gpt/fig_structural_limit_signature.pdf` (vector)

**Library versions:**
- matplotlib `3.10.8`
- seaborn `0.13.2`

**Exact numbers rendered:**
- N = `30`
- Mean line = `38.94533333333333%` rendered as `38.95%`
- Standard-deviation band = `+/- 9.85063122547128%` rendered as `+/- 9.85%`
- Band bounds = `29.09470210786205%` to `48.79596455880461%`
- Range annotation = `22.03400000000000%` to `61.69400000000000%` rendered as `22.03%-61.69%`
- Hartigan dip statistic = `0.0415`
- Hartigan dip p-value = `0.9796` rendered as `p=0.98`
- Sorted per-instance means = `22.034, 22.950, 25.704, 26.720, 27.510, 28.030, 30.828, 31.550, 31.592, 33.880, 35.602, 36.020, 36.092, 38.482, 38.920, 38.990, 40.170, 41.282, 41.604, 42.210, 43.606, 44.594, 46.152, 47.220, 47.650, 49.790, 50.988, 51.620, 54.876, 61.694`
- KDE method = `scipy.stats.gaussian_kde` default bandwidth (Scott)
- KDE Scott factor = `0.5064956841121182`
- KDE validation peaks = `1` at `39.658%`

**Caption candidate:** CX-K2 fresh-instance evaluation shows a broad high-variance accuracy distribution (38.95 +/- 9.85%, range 22.03%-61.69%) with no statistically supported bimodal attractor (Hartigan dip p=0.98).
