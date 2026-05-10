#!/usr/bin/env python3
"""Generate draft audit plots for 107 KV-cache candidate groups."""

import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[2]
TSV_PATH = ROOT / "paper2" / "results" / "FRESH_D2D_SUMMARY_107_20260510.tsv"
OUT_DIR = ROOT / "paper2" / "results"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TINOS_DIR = Path("/usr/share/fonts/truetype/croscore")
for font_file in TINOS_DIR.glob("Tinos-*.ttf"):
    font_manager.fontManager.addfont(str(font_file))

COL = {
    "ink": "#333333",
    "grid": "#E1E6EB",
    "blue": "#264653",
    "orange": "#E76F51",
    "green": "#2A9D8F",
}

SELECTED_CHECKPOINTS = {
    "last1_24l": "hat_d2d002_500_freshd2d_last1_seed42",
    "last2_24l": "hat_d2d002_500_freshd2d_last2_seed42",
    "last4_24l": "410m_last4_v2_seed42",
    "all24": "combined_layerall_v2_seed42",
}

FOOTNOTE = "Draft audit plot: candidate index only; missing commit/command/dataset/eval-protocol/checkpoint-hash metadata."


def configure_style():
    plt.style.use("seaborn-v0_8-paper")
    plt.rcParams.update({
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "Tinos", "DejaVu Serif"],
        "font.size": 10.4,
        "axes.titlesize": 11.0,
        "axes.titleweight": "bold",
        "axes.labelsize": 10.5,
        "legend.fontsize": 9.2,
        "legend.frameon": True,
        "legend.edgecolor": "#D8DEE4",
        "legend.facecolor": "#ffffff",
        "legend.framealpha": 0.95,
        "axes.linewidth": 1.0,
        "axes.edgecolor": "#222222",
    })


def save_with_footnote(fig, stem):
    fig.text(0.5, 0.025, FOOTNOTE, ha="center", va="bottom", fontsize=7.4, color=COL["ink"])
    fig.tight_layout(rect=(0, 0.075, 1, 1))
    fig.savefig(OUT_DIR / f"{stem}.png")
    fig.savefig(OUT_DIR / f"{stem}.pdf")
    print(f"Saved {OUT_DIR / f'{stem}.png'}")


def value_or_zero(row, column):
    return 0.0 if row is None else float(row[column])


def pick_rows(df, d2d):
    rows = []
    for label, checkpoint in SELECTED_CHECKPOINTS.items():
        match = df[
            (df["status"] == "candidate_index_not_claim_lock")
            & (df["checkpoint"] == checkpoint)
            & (df["layer_label"] == label)
            & np.isclose(df["eval_c2c"], 0.0)
            & np.isclose(df["eval_d2d"], d2d)
            & (df["n_d2d_seeds"] >= 5)
        ]
        rows.append(match.iloc[0] if not match.empty else None)
    return rows


def plot_selective_kv(df):
    rows_02 = pick_rows(df, 0.02)
    rows_05 = pick_rows(df, 0.05)
    labels = ["1 (last1)", "2 (last2)", "4 (last4)", "24 (all)"]
    x_positions = np.arange(len(labels))
    width = 0.35
    means_02 = [value_or_zero(row, "mean_ppl") for row in rows_02]
    stds_02 = [value_or_zero(row, "std_ppl") for row in rows_02]
    means_05 = [value_or_zero(row, "mean_ppl") for row in rows_05]
    stds_05 = [value_or_zero(row, "std_ppl") for row in rows_05]

    fig, ax = plt.subplots(figsize=(6.2, 4.7))
    bars_02 = ax.bar(x_positions - width / 2, means_02, width, yerr=stds_02, label="D2D=0.02 candidate", color=COL["blue"], edgecolor="#222222", linewidth=1.0, error_kw=dict(ecolor=COL["ink"], lw=1.1, capsize=4, capthick=1.1))
    bars_05 = ax.bar(x_positions + width / 2, means_05, width, yerr=stds_05, label="D2D=0.05 candidate", color=COL["orange"], edgecolor="#222222", linewidth=1.0, error_kw=dict(ecolor=COL["ink"], lw=1.1, capsize=4, capthick=1.1))
    ax.axhline(y=15.68, color=COL["green"], linestyle="--", linewidth=1.4, label="Digital reference (15.68)")
    ax.set_ylim(10, 85)
    ax.set_ylabel("Perplexity (PPL); lower is better")
    ax.set_xlabel("Analog terminal-layer subset")
    ax.set_title("Remote 107 KV-cache candidate index (not claim-locked)")
    ax.set_xticks(x_positions)
    ax.set_xticklabels(labels)
    ax.legend(loc="upper left")
    ax.grid(axis="y", linestyle=(0, (2, 2)), linewidth=0.5, alpha=0.6, color=COL["grid"])
    for bars, means in [(bars_02, means_02), (bars_05, means_05)]:
        for bar, mean in zip(bars, means):
            if mean <= 0:
                continue
            ax.text(bar.get_x() + bar.get_width() / 2, min(mean + 2, 80), f"{mean:.1f}", ha="center", va="bottom", fontsize=8.4, color=COL["ink"])
    save_with_footnote(fig, "fig_107_selective_kv")


def plot_noise_sweep(df):
    checkpoint = "hat_d2d002_500_v2_seed42"
    sub = df[
        (df["status"] == "candidate_index_not_claim_lock")
        & (df["checkpoint"] == checkpoint)
        & (df["layer_label"] == "all24")
        & np.isclose(df["eval_c2c"], 0.0)
        & (df["n_d2d_seeds"] >= 5)
    ].sort_values("eval_d2d")
    fig, ax = plt.subplots(figsize=(6.1, 4.45))
    ax.errorbar(sub["eval_d2d"], sub["mean_ppl"], yerr=sub["std_ppl"], marker="o", linestyle="none", markersize=5.5, capsize=4, color=COL["orange"], label="all24 candidate rows (n>=5)")
    ax.axhline(y=15.68, color=COL["green"], linestyle="--", linewidth=1.4, label="Digital reference (15.68)")
    for _, row in sub.iterrows():
        ax.text(row["eval_d2d"], row["mean_ppl"] + 2.0, f"n={int(row['n_d2d_seeds'])}", ha="center", va="bottom", fontsize=7.8, color=COL["ink"])
    ax.set_ylabel("Perplexity (PPL); lower is better")
    ax.set_xlabel(r"Evaluation D2D variability ($\sigma_{D2D}$)")
    ax.set_title("All-24 analog multi-seed candidate points (not claim-locked)")
    ax.set_ylim(10, max(75, float(sub["mean_ppl"].max()) + 12))
    ax.legend(loc="upper left")
    ax.grid(axis="both", linestyle=(0, (2, 2)), linewidth=0.5, alpha=0.6, color=COL["grid"])
    save_with_footnote(fig, "fig_107_noise_sweep")


def plot_training_steps(df):
    fig, ax = plt.subplots(figsize=(6.1, 4.45))
    ax.axis("off")
    lines = [
        "Training-step sweep audit gap",
        "not claim-locked",
        "",
        "No complete matched 200/500/1000/2000-step sweep was found",
        "in FRESH_D2D_SUMMARY_107_20260510.tsv under the strict grouping rules.",
        "",
        "Reason: available step-like rows are unmatched by checkpoint/protocol",
        "or lack multi-seed metadata required for claim use.",
        "",
        "Required before plotting convergence:",
        "1. Same model/checkpoint family across steps",
        "2. Same analog-layer list and eval noise",
        "3. n>=5 D2D seeds or signed rationale",
        "4. commit, command, dataset, eval protocol, checkpoint hash",
    ]
    ax.text(0.5, 0.58, "\n".join(lines), ha="center", va="center", fontsize=10.0, color=COL["ink"], linespacing=1.25)
    fig.text(0.5, 0.025, FOOTNOTE, ha="center", va="bottom", fontsize=7.4, color=COL["ink"])
    fig.tight_layout(rect=(0, 0.075, 1, 1))
    fig.savefig(OUT_DIR / "fig_107_training_steps.png")
    fig.savefig(OUT_DIR / "fig_107_training_steps.pdf")
    print(f"Saved {OUT_DIR / 'fig_107_training_steps.png'}")


def main():
    df = pd.read_csv(TSV_PATH, sep="\t")
    plot_selective_kv(df)
    plot_noise_sweep(df)
    plot_training_steps(df)


if __name__ == "__main__":
    configure_style()
    main()
