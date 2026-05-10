#!/usr/bin/env python3
"""
Run Hartigan's dip test for bimodality on CX-K2 fresh-instance evaluation data.
"""

import json
import sys
import numpy as np
from pathlib import Path

try:
    import diptest
except ImportError:
    print("ERROR: diptest package not installed. Install with: pip install diptest")
    sys.exit(1)

# Paths
PROJECT_ROOT = Path("/home/qiaosir/projects/compute_vit")
DATA_PATH = PROJECT_ROOT / "report_md/_gpt/json_gpt/cx_k2_fresh_eval.json"
OUT_JSON_PATH = PROJECT_ROOT / "report_md/_gpt/json_gpt/cx_k2_bimodality_test.json"
OUT_MEMO_PATH = PROJECT_ROOT / "report_md/_gpt/CODEX_CX_K2_BIMODALITY_TEST_20260423.md"

# Read data
with open(DATA_PATH, "r") as f:
    data = json.load(f)

instance_means = np.array(data["instance_means"], dtype=float)
n = len(instance_means)

# Basic descriptive stats
mean_val = float(np.mean(instance_means))
std_val = float(np.std(instance_means, ddof=1))
min_val = float(np.min(instance_means))
max_val = float(np.max(instance_means))
median_val = float(np.median(instance_means))

# Hartigan's dip test
dip_stat, p_value = diptest.diptest(instance_means)

# Bimodality decision
bimodal_confirmed = bool(p_value < 0.05)

# Mode estimation via kernel density (if bimodal or for exploratory purposes)
from scipy.stats import gaussian_kde
kde = gaussian_kde(instance_means, bw_method="scott")
x_grid = np.linspace(min_val - 5, max_val + 5, 2000)
kde_vals = kde(x_grid)

# Find local maxima (modes)
from scipy.signal import find_peaks
peaks, props = find_peaks(kde_vals, height=0.0)
modes = [float(x_grid[p]) for p in peaks]
mode_heights = [float(kde_vals[p]) for p in peaks]

# Sort modes by density height descending
modes_sorted = sorted(zip(mode_heights, modes), reverse=True)
top_modes = [m for _, m in modes_sorted[:2]] if len(modes_sorted) >= 2 else modes

# Alternative: estimate modes via simple clustering if bimodal
from sklearn.mixture import GaussianMixture
gmm = GaussianMixture(n_components=2, random_state=42)
gmm.fit(instance_means.reshape(-1, 1))
gmm_means = sorted([float(m[0]) for m in gmm.means_])
gmm_weights = [float(w) for _, w in sorted(zip([float(m[0]) for m in gmm.means_], gmm.weights_))]
gmm_stds = [float(np.sqrt(c[0][0])) for _, c in sorted(zip([float(m[0]) for m in gmm.means_], gmm.covariances_))]

# Determine recommendation
recommendation = "Branch A (bimodal narrative)" if bimodal_confirmed else "Branch B (structural limit fallback)"

# Build output JSON
result = {
    "task": "CX-K2 Hartigan's Dip Test for Bimodality",
    "timestamp": "2026-04-23T15:07:47+08:00",
    "n_samples": n,
    "descriptive_stats": {
        "mean": round(mean_val, 4),
        "std": round(std_val, 4),
        "median": round(median_val, 4),
        "min": round(min_val, 4),
        "max": round(max_val, 4),
        "range": round(max_val - min_val, 4)
    },
    "hartigans_dip_test": {
        "dip_statistic": round(float(dip_stat), 6),
        "p_value": round(float(p_value), 6),
        "alpha": 0.05,
        "bimodal_confirmed": bimodal_confirmed
    },
    "mode_estimates": {
        "kde_modes": [round(m, 2) for m in top_modes],
        "gmm_component_means": [round(m, 2) for m in gmm_means],
        "gmm_component_stds": [round(s, 2) for s in gmm_stds],
        "gmm_weights": [round(w, 3) for w in gmm_weights],
        "inferred_collapse_basin": round(gmm_means[0], 1) if len(gmm_means) >= 2 else None,
        "inferred_recovery_basin": round(gmm_means[1], 1) if len(gmm_means) >= 2 else None
    },
    "recommendation": recommendation,
    "data_source": str(DATA_PATH)
}

# Write JSON
OUT_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_JSON_PATH, "w") as f:
    json.dump(result, f, indent=2)

print(json.dumps(result, indent=2))

# Write memo
memo = f"""# CODEX CX-K2 Bimodality Test Memo

**Date:** 2026-04-23  
**Task:** CX-K2 — Hartigan's Dip Test on N=30 Fresh-Instance Evaluation  
**Data Source:** `cx_k2_fresh_eval.json`

## Summary

| Metric | Value |
|--------|-------|
| N | {n} |
| Mean | {mean_val:.2f}% |
| Std | {std_val:.2f}% |
| Range | {min_val:.2f}% – {max_val:.2f}% |
| Dip Statistic | {float(dip_stat):.6f} |
| p-value | {float(p_value):.6f} |
| Bimodal (α=0.05)? | **{'YES' if bimodal_confirmed else 'NO'}** |

## Mode Estimates

- **GMM Component 1 (collapse basin):** ~{gmm_means[0]:.1f}% (σ={gmm_stds[0]:.1f}%, w={gmm_weights[0]:.3f})
- **GMM Component 2 (recovery basin):** ~{gmm_means[1]:.1f}% (σ={gmm_stds[1]:.1f}%, w={gmm_weights[1]:.3f})
- **KDE peak modes:** {', '.join(f'{m:.1f}%' for m in top_modes)}

## Interpretation

The dip test yields p = {float(p_value):.4f}, which is {'below' if bimodal_confirmed else 'above'} the α = 0.05 threshold.  
**→ {recommendation}**

## Decision

- **p < 0.05:** Bimodal confirmed → recommend **Branch A (bimodal narrative)**. The fresh-instance distribution is better described as a mixture of a lower "collapse basin" (~{gmm_means[0]:.0f}%) and an upper "recovery basin" (~{gmm_means[1]:.0f}%), supporting the Work 1 closure narrative.
- **p ≥ 0.05:** Unimodal → recommend **Branch B (structural limit fallback)**.

## Files Generated

- `report_md/_gpt/json_gpt/cx_k2_bimodality_test.json`
- `scripts/_gpt/run_hartigans_dip.py`

---
*Generated by Codex — CX-K2 Bimodality Test*
"""

OUT_MEMO_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_MEMO_PATH, "w") as f:
    f.write(memo)

print(f"\nWrote JSON: {OUT_JSON_PATH}")
print(f"Wrote memo: {OUT_MEMO_PATH}")
