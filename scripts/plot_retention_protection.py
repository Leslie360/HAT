#!/usr/bin/env python3
"""Plot retention × protection curves."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
SUMMARY = ROOT / "thesis" / "results" / "retention_protection" / "retention_protection_summary_10x3_20260511_223530.tsv"
SOURCE_OUT = ROOT / "thesis" / "results" / "retention_protection" / "retention_protection_plot_source_10x3_20260511_223530.tsv"
OUT_DIR = ROOT / "thesis" / "figures" / "retention_protection"

LABELS = {
    "fresh_all_analog": "Fresh all-analog",
    "freeze_top30_d2d": "Freeze top-30 D2D",
    "freeze_top42_d2d": "Freeze top-42 D2D",
}
COLORS = {
    "fresh_all_analog": "#6C8EBF",
    "freeze_top30_d2d": "#2A9D8F",
    "freeze_top42_d2d": "#264653",
}
MARKERS = {
    "fresh_all_analog": "o",
    "freeze_top30_d2d": "s",
    "freeze_top42_d2d": "^",
}
ORDER = ["fresh_all_analog", "freeze_top30_d2d", "freeze_top42_d2d"]


def configure_style():
    plt.style.use("seaborn-v0_8-paper")
    plt.rcParams.update({
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "font.size": 10.5,
        "axes.titlesize": 11.2,
        "axes.titleweight": "bold",
        "axes.labelsize": 10.7,
        "legend.fontsize": 9.0,
        "xtick.labelsize": 9.3,
        "ytick.labelsize": 9.3,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 0.8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def main():
    configure_style()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SOURCE_OUT.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(SUMMARY, sep="\t")
    df["strategy"] = pd.Categorical(df["strategy"], categories=ORDER, ordered=True)
    df = df.sort_values(["strategy", "retention_time_s"]).copy()
    df["label"] = df["strategy"].astype(str).map(LABELS)
    base = df[df["retention_time_s"] == 0.0].set_index("strategy")["accuracy_mean"].to_dict()
    df["delta_vs_0s"] = df.apply(lambda row: row["accuracy_mean"] - base[str(row["strategy"])], axis=1)
    df.to_csv(SOURCE_OUT, sep="\t", index=False)

    fig, ax = plt.subplots(figsize=(6.7, 4.15))
    for strategy in ORDER:
        group = df[df["strategy"] == strategy]
        ax.errorbar(
            group["retention_time_s"],
            group["accuracy_mean"],
            yerr=group["accuracy_std"],
            marker=MARKERS[strategy],
            linewidth=2.0,
            capsize=3.5,
            markersize=5.3,
            color=COLORS[strategy],
            label=LABELS[strategy],
            zorder=3,
        )

    ax.set_xscale("symlog", linthresh=1.0)
    ax.set_xticks([0, 1000, 10000])
    ax.set_xticklabels(["0", "1k", "10k"])
    ax.set_xlabel("Retention time (s)")
    ax.set_ylabel("CIFAR-100 accuracy (%)")
    ax.set_title("Retention drift preserves the protected-layer ordering")
    ax.set_ylim(53.5, 63.2)
    ax.grid(axis="y", linestyle=(0, (2, 2)), linewidth=0.55, color="#E1E6EB", zorder=0)
    ax.legend(loc="lower right", frameon=True, edgecolor="#D8DEE4", framealpha=0.94)
    ax.text(
        0.02,
        0.96,
        "10 fresh D2D instances × 3 MC\nscale recalibration and D2D decay enabled",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=8.4,
        color="#555555",
        bbox={"facecolor": "white", "edgecolor": "#D8DEE4", "boxstyle": "round,pad=0.28", "alpha": 0.92},
    )

    fig.tight_layout()
    png = OUT_DIR / "fig_retention_protection_10x3_20260511.png"
    pdf = OUT_DIR / "fig_retention_protection_10x3_20260511.pdf"
    fig.savefig(png, bbox_inches="tight")
    fig.savefig(pdf, bbox_inches="tight")
    print(f"wrote {SOURCE_OUT}")
    print(f"wrote {png}")
    print(f"wrote {pdf}")


if __name__ == "__main__":
    main()
