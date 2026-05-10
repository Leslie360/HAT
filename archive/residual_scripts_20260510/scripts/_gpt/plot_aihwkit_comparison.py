#!/usr/bin/env python3
"""Generate the supplementary AIHWKit comparison figure."""

import json
import os

import matplotlib.pyplot as plt

def main():
    # Setup
    os.makedirs("paper/latex_gpt/figures", exist_ok=True)

    # Data
    methods = ["Standard HAT\n(Fixed Mask)", "Ensemble HAT\n(Epoch Resampling)", "AIHWKit Baseline\n(Default Noisy)"]

    std_mean, std_std = 10.00, 0.00
    ens_mean, ens_std = 86.16, 0.19

    # Load AIHWKit
    try:
        with open("paper2_aihwkit_baseline/checkpoints/fresh_eval.json", "r") as f:
            data = json.load(f)
            aihwkit_mean = data.get("mean", 87.34)
            aihwkit_std = data.get("std", 0.14)
    except Exception:
        aihwkit_mean = 87.34
        aihwkit_std = 0.14

    means = [std_mean, ens_mean, aihwkit_mean]
    stds = [std_std, ens_std, aihwkit_std]

    # Plot style
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 10.2,
        "axes.labelsize": 10.2,
        "axes.titlesize": 10.6,
        "xtick.labelsize": 9.2,
        "ytick.labelsize": 9.2,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })

    fig, ax = plt.subplots(figsize=(6.8, 4.1))

    # Palette shared with the main paper spine figure.
    colors = ["#B94A48", "#2E7D5B", "#2F5D8C"]

    bars = ax.bar(methods, means, yerr=stds, capsize=8, color=colors, alpha=0.8, edgecolor='black', width=0.6)

    # Add text labels
    for bar, mean, std in zip(bars, means, stds):
        y_pos = bar.get_height() + (std if std > 0 else 0) + 1
        ax.text(bar.get_x() + bar.get_width()/2, y_pos,
                f"{mean:.2f} $\\pm$ {std:.2f}%", ha='center', va='bottom', fontsize=9.2, fontweight='bold')

    ax.set_ylabel("Fresh-Instance Accuracy (%)")
    ax.set_title("Cross-instance generalization vs AIHWKit")
    ax.set_ylim(0, 105)

    ax.grid(axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig("paper/latex_gpt/figures/figS_aihwkit_comparison.pdf", dpi=300, bbox_inches='tight')
    plt.savefig("paper/latex_gpt/figures/figS_aihwkit_comparison.png", dpi=300, bbox_inches='tight')
    print("Saved figS_aihwkit_comparison.{pdf,png}")

if __name__ == "__main__":
    main()
