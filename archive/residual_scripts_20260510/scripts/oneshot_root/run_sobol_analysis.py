#!/usr/bin/env python3
"""Sobol first-order sensitivity indices from contour sweep data."""

import json
import numpy as np
from pathlib import Path

DATA_PATH = "report_md/_gpt/iso_accuracy_contour_data.json"
OUTPUT_PATH = "report_md/_gpt/sobol_sensitivity.json"

def main():
    with open(DATA_PATH) as f:
        data = json.load(f)
    
    d2d_vals = sorted(set(r["d2d_pct"] for r in data))
    adc_vals = sorted(set(r["adc_bits"] for r in data))
    
    # Build mean accuracy matrix
    grid = np.zeros((len(d2d_vals), len(adc_vals)))
    for r in data:
        i = d2d_vals.index(r["d2d_pct"])
        j = adc_vals.index(r["adc_bits"])
        grid[i, j] = r["mean"]
    
    total_var = np.var(grid)
    
    # First-order: variance of conditional means
    # S_d2d: fix D2D, average over ADC
    mean_over_adc = grid.mean(axis=1)  # shape (7,)
    var_d2d = np.var(mean_over_adc)
    S_d2d = var_d2d / total_var
    
    # S_adc: fix ADC, average over D2D
    mean_over_d2d = grid.mean(axis=0)  # shape (9,)
    var_adc = np.var(mean_over_d2d)
    S_adc = var_adc / total_var
    
    # Also compute for the "operational" region only (6-bit+, D2D<=15%)
    mask_d2d = [i for i, d in enumerate(d2d_vals) if d <= 15]
    mask_adc = [j for j, a in enumerate(adc_vals) if a >= 6]
    sub = grid[np.ix_(mask_d2d, mask_adc)]
    sub_total_var = np.var(sub)
    
    sub_mean_adc = sub.mean(axis=1)
    sub_mean_d2d = sub.mean(axis=0)
    S_d2d_op = np.var(sub_mean_adc) / sub_total_var if sub_total_var > 0 else 0
    S_adc_op = np.var(sub_mean_d2d) / sub_total_var if sub_total_var > 0 else 0
    
    result = {
        "full_grid": {
            "total_variance": float(total_var),
            "S_d2d": float(S_d2d),
            "S_adc": float(S_adc),
            "S_interaction": float(1 - S_d2d - S_adc),
            "interpretation": "S_d2d + S_adc + S_interaction = 1.0"
        },
        "operational_region": {
            "filter": "D2D <= 15%, ADC >= 6-bit",
            "total_variance": float(sub_total_var),
            "S_d2d": float(S_d2d_op),
            "S_adc": float(S_adc_op),
            "S_interaction": float(1 - S_d2d_op - S_adc_op),
        },
        "conditional_means": {
            "d2d_values": d2d_vals,
            "mean_acc_by_d2d": [float(v) for v in mean_over_adc],
            "adc_values": adc_vals,
            "mean_acc_by_adc": [float(v) for v in mean_over_d2d],
        }
    }
    
    Path(OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)
    
    print(f"Full grid: S_d2d={S_d2d:.3f}, S_adc={S_adc:.3f}, S_interaction={1-S_d2d-S_adc:.3f}")
    print(f"Operational: S_d2d={S_d2d_op:.3f}, S_adc={S_adc_op:.3f}")
    print(f"Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()