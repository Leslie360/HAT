#!/usr/bin/env python3
"""Plot Remote107 p28b layer ablation + adaptive schedule comparison."""
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
    return data["ppl_after"]


def plot():
    plt.rcParams.update({
        "font.size": 10,
        "axes.linewidth": 0.9,
        "xtick.major.width": 0.8,
        "ytick.major.width": 0.8,
        "font.family": "serif",
    })

    # Data: last1 fixed, last1 cosine, last2 fixed, last2 cosine, last4 fixed
    configs = ["last1\nFixed", "last1\nCosine", "last2\nFixed", "last2\nCosine", "last4\nFixed"]
    ppls = [
        load_ppl(R107 / "p28b_adaptive_fixed_v1_seed42.json"),
        load_ppl(R107 / "p28b_adaptive_cosine_v1_seed42.json"),
        13.78,  # from MASTER_TASK_LIST (R2-LAST2)
        load_ppl(R107 / "p28b_adaptive_cosine_last2_seed42.json"),
        14.12,  # from MASTER_TASK_LIST (R2-LAST4)
    ]
    colors = ["#1f77b4", "#2ca02c", "#aec7e8", "#98df8a", "#ffbb78"]

    fig, ax = plt.subplots(figsize=(7, 4.2), dpi=200)
    x = np.arange(len(configs))
    bars = ax.bar(x, ppls, color=colors, width=0.6, edgecolor="black", linewidth=0.7)

    for bar, ppl in zip(bars, ppls):
        height = bar.get_height()
        ax.annotate(f"{ppl:.2f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3), textcoords="offset points",
                    ha="center", va="bottom", fontsize=9, fontweight="bold")

    # Highlight best
    best_idx = np.argmin(ppls)
    bars[best_idx].set_edgecolor("darkgreen")
    bars[best_idx].set_linewidth(2.0)
    ax.annotate("BEST", xy=(best_idx, ppls[best_idx]),
                xytext=(0, 12), textcoords="offset points",
                ha="center", va="bottom", fontsize=9, color="darkgreen", fontweight="bold")

    ax.set_xticks(x)
    ax.set_xticklabels(configs, fontsize=9)
    ax.set_ylabel("Perplexity (PPL)", fontsize=10)
    ax.set_title("Pythia-2.8B: Layer Ablation × Adaptive Schedule", fontsize=11)
    ax.grid(True, alpha=0.25, axis="y", linewidth=0.6)
    ax.set_ylim(11.5, 15.5)

    fig.tight_layout()

    for d in [OUT_DIR, PAPER2_DIR]:
        fig.savefig(d / "fig_remote107_r3_p28b_ablation_20260513.pdf", bbox_inches="tight")
        fig.savefig(d / "fig_remote107_r3_p28b_ablation_20260513.png", bbox_inches="tight", dpi=200)

    print(f"Saved fig_remote107_r3_p28b_ablation_20260513.pdf")


if __name__ == "__main__":
    plot()
