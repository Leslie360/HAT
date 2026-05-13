#!/usr/bin/env python3
"""Plot Remote107 R3 adaptive noise schedule PPL comparison across scales."""
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "thesis" / "figures" / "remote107"
OUT_DIR.mkdir(parents=True, exist_ok=True)
PAPER2_DIR = ROOT / "paper2" / "figures"
PAPER2_DIR.mkdir(parents=True, exist_ok=True)
R107 = Path("/home/qiaosir/projects/remote_reviews/107/paper2/results/remote107")


def load_ppl(path):
    data = json.load(open(path))
    return data["ppl_after"], data.get("ppl_before")


def plot():
    plt.rcParams.update({
        "font.size": 10,
        "axes.linewidth": 0.9,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "font.family": "serif",
    })

    # Load data
    schedules = ["Fixed", "Cosine", "Layer-wise"]
    models = ["Pythia-410M", "Pythia-2.8B", "Pythia-6.9B"]
    files = [
        [
            R107 / "p410m_adaptive_fixed_v4_seed42.json",
            R107 / "p410m_adaptive_cosine_v4_seed42.json",
            R107 / "p410m_adaptive_layerwise_v4_seed42.json",
        ],
        [
            R107 / "p28b_adaptive_fixed_v1_seed42.json",
            R107 / "p28b_adaptive_cosine_v1_seed42.json",
            R107 / "p28b_adaptive_layerwise_v1_seed42.json",
        ],
        [
            R107 / "p69b_adaptive_fixed_v1_seed42.json",
            R107 / "p69b_adaptive_cosine_v1_seed42.json",
            R107 / "p69b_adaptive_layerwise_v1_seed42.json",
        ],
    ]

    ppls = []
    baselines = []
    for row in files:
        ppls.append([load_ppl(f)[0] for f in row])
        baselines.append(load_ppl(row[0])[1])

    fig, ax = plt.subplots(figsize=(7.5, 4.5), dpi=200)
    x = np.arange(len(models))
    width = 0.22
    colors = ["#1f77b4", "#2ca02c", "#ff7f0e"]

    for i, (sched, color) in enumerate(zip(schedules, colors)):
        vals = [ppls[m][i] for m in range(len(models))]
        bars = ax.bar(x + (i - 1) * width, vals, width, label=sched, color=color,
                      edgecolor="black", linewidth=0.6)
        for bar, val in zip(bars, vals):
            ax.annotate(f"{val:.2f}",
                        xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
                        xytext=(0, 2), textcoords="offset points",
                        ha="center", va="bottom", fontsize=8)

    # Baseline (pre-HAT) markers
    for i, bl in enumerate(baselines):
        if bl:
            ax.hlines(bl, i - 0.4, i + 0.4, colors="gray", linestyles="--", linewidth=1.0)
            ax.text(i, bl + 0.3, f"Pre-HAT\n{bl:.2f}", ha="center", va="bottom",
                    fontsize=7, color="gray")

    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=10)
    ax.set_ylabel("Perplexity (PPL)", fontsize=10)
    ax.set_title("Adaptive Noise Schedule Comparison Across Model Scales", fontsize=11)
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(True, alpha=0.25, axis="y", linewidth=0.6)
    ax.set_ylim(0, 26)

    fig.tight_layout()

    for d in [OUT_DIR, PAPER2_DIR]:
        fig.savefig(d / "fig_remote107_r3_adaptive_ppl_20260513.pdf", bbox_inches="tight")
        fig.savefig(d / "fig_remote107_r3_adaptive_ppl_20260513.png", bbox_inches="tight", dpi=200)

    print(f"Saved fig_remote107_r3_adaptive_ppl_20260513.pdf")


if __name__ == "__main__":
    plot()
