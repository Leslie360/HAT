#!/usr/bin/env python3
"""Generate the main Paper-1 multi-panel spine figure and source-data tables."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / "paper" / "latex_gpt" / "figures"
SRC_DIR = ROOT / "paper" / "latex_gpt" / "source_data"
CKPT = ROOT / "paper2_aihwkit_baseline" / "checkpoints"

FIG_DIR.mkdir(parents=True, exist_ok=True)
SRC_DIR.mkdir(parents=True, exist_ok=True)

PALETTE = {
    "blue": "#2F5D8C",
    "blue_light": "#E7F0FA",
    "red": "#B94A48",
    "red_light": "#F7E7E5",
    "green": "#2E7D5B",
    "green_light": "#E7F4EE",
    "orange": "#D59A4A",
    "orange_light": "#FFF1DD",
    "ink": "#202020",
    "muted": "#666666",
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def drift_acc(run_dir: Path, seconds: float) -> float:
    drift = load_json(run_dir / "drift_eval.json")
    for row in drift["results"]:
        if float(row["t_inference_seconds"]) == seconds:
            return float(row["accuracy"])
    raise KeyError(seconds)


def mean_std(values: list[float]) -> tuple[float, float]:
    arr = np.asarray(values, dtype=float)
    return float(arr.mean()), float(arr.std(ddof=1))


ideal_rows = [
    {
        "condition": "IdealDevice 8-bit",
        "fresh_mean": load_json(CKPT / "fresh_eval.json")["mean"],
        "fresh_std": load_json(CKPT / "fresh_eval.json")["std"],
        "role": "stable baseline",
    },
    {
        "condition": "IdealDevice 4-bit",
        "fresh_mean": load_json(CKPT / "r11d_1_4bit" / "fresh_eval.json")["mean"],
        "fresh_std": load_json(CKPT / "r11d_1_4bit" / "fresh_eval.json")["std"],
        "role": "collapse",
    },
    {
        "condition": "Ensemble HAT 4-bit",
        "fresh_mean": 86.15873333333333,
        "fresh_std": 0.19,
        "role": "algorithmic rescue",
    },
]
ensemble_hat = load_json(ROOT / "report_md" / "_gpt" / "json_gpt" / "r10a_canonical_ensemble_hat_3seed_fresh_eval.json")
ideal_rows[2]["fresh_mean"] = ensemble_hat["cross_seed"]["mean_of_seed_means"]
ideal_rows[2]["fresh_std"] = ensemble_hat["cross_seed"]["std_of_seed_means_sample"]

pcm_groups = {
    "8-bit PCM": ["r11d_5a_pcm_seed123", "r11d_5a_pcm_seed456", "r11d_5a_pcm_seed789"],
    "6-bit PCM": ["r11d_6bit_pcm_seed123", "r11d_6bit_pcm_seed456_full100", "r11d_6bit_pcm_seed789"],
    "4-bit PCM": ["r11d_7_pcm_4bit_seed123", "r11d_7_pcm_4bit_seed456_clean", "r11d_7_pcm_4bit_seed789"],
}

pcm_rows = []
for label, runs in pcm_groups.items():
    best_vals = []
    fresh_vals = []
    drift0_vals = []
    drift1d_vals = []
    for run in runs:
        run_dir = CKPT / run
        hist = load_json(run_dir / "training_history.json")
        fresh = load_json(run_dir / "fresh_eval.json")
        best_vals.append(float(hist["best_acc"]))
        fresh_vals.append(float(fresh["mean"]))
        drift0_vals.append(drift_acc(run_dir, 0.0))
        drift1d_vals.append(drift_acc(run_dir, 86400.0))
    best_mean, best_std = mean_std(best_vals)
    fresh_mean, fresh_std = mean_std(fresh_vals)
    drift_drop = float(np.mean(drift0_vals) - np.mean(drift1d_vals))
    pcm_rows.append(
        {
            "condition": label,
            "source_best_mean": best_mean,
            "source_best_std": best_std,
            "fresh_mean": fresh_mean,
            "fresh_std": fresh_std,
            "drift_drop_1d_pp": drift_drop,
        }
    )

with (SRC_DIR / "fig1_paper1_spine.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(ideal_rows[0].keys()), lineterminator="\n")
    writer.writeheader()
    writer.writerows(ideal_rows)

with (SRC_DIR / "tab_pcm_precision_ladder.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(pcm_rows[0].keys()), lineterminator="\n")
    writer.writeheader()
    writer.writerows(pcm_rows)

manifest = {
    "generated_by": "scripts/_gpt/plot_paper1_spine.py",
    "outputs": [
        "paper/latex_gpt/figures/fig1_paper1_spine.pdf",
        "paper/latex_gpt/figures/fig1_paper1_spine.png",
        "paper/latex_gpt/source_data/fig1_paper1_spine.csv",
        "paper/latex_gpt/source_data/tab_pcm_precision_ladder.csv",
    ],
    "raw_sources": [
        "paper2_aihwkit_baseline/checkpoints/fresh_eval.json",
        "paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/fresh_eval.json",
        "report_md/_gpt/json_gpt/r10a_canonical_ensemble_hat_3seed_fresh_eval.json",
        *[f"paper2_aihwkit_baseline/checkpoints/{run}/training_history.json" for runs in pcm_groups.values() for run in runs],
        *[f"paper2_aihwkit_baseline/checkpoints/{run}/fresh_eval.json" for runs in pcm_groups.values() for run in runs],
        *[f"paper2_aihwkit_baseline/checkpoints/{run}/drift_eval.json" for runs in pcm_groups.values() for run in runs],
    ],
}
with (SRC_DIR / "manifest_paper1_spine.json").open("w", encoding="utf-8") as handle:
    json.dump(manifest, handle, indent=2)

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10.0,
        "axes.labelsize": 9.8,
        "axes.titlesize": 10.4,
        "xtick.labelsize": 8.8,
        "ytick.labelsize": 8.8,
        "axes.linewidth": 0.8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)


def panel_label(ax, label: str, title: str) -> None:
    ax.text(0.0, 1.04, label, transform=ax.transAxes, ha="left", va="bottom", fontsize=11, fontweight="bold")
    ax.text(0.085, 1.045, title, transform=ax.transAxes, ha="left", va="bottom", fontsize=9.6, fontweight="bold")


def rounded_box(ax, xy, width, height, text, fc, ec, fontsize=9.2, weight="normal"):
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.018,rounding_size=0.035",
        facecolor=fc,
        edgecolor=ec,
        linewidth=1.0,
    )
    ax.add_patch(box)
    ax.text(xy[0] + width / 2, xy[1] + height / 2, text, ha="center", va="center", fontsize=fontsize, fontweight=weight, color=PALETTE["ink"])
    return box


def arrow(ax, start, end, color=None, rad=0.0):
    patch = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=12,
        lw=1.0,
        color=color or PALETTE["muted"],
        connectionstyle=f"arc3,rad={rad}",
    )
    ax.add_patch(patch)


def draw_mechanism_panel(ax):
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    panel_label(ax, "A", "Training objective")

    rounded_box(ax, (0.06, 0.75), 0.25, 0.105, "digital\nmodel", "#F6F6F6", "#999999", fontsize=8.0, weight="bold")
    rounded_box(ax, (0.40, 0.75), 0.23, 0.105, "analog\nmapping", PALETTE["blue_light"], PALETTE["blue"], fontsize=8.0, weight="bold")
    rounded_box(ax, (0.72, 0.75), 0.21, 0.105, "fresh\nchip", PALETTE["orange_light"], PALETTE["orange"], fontsize=8.0, weight="bold")
    arrow(ax, (0.31, 0.802), (0.40, 0.802))
    arrow(ax, (0.63, 0.802), (0.72, 0.802))

    ax.text(0.07, 0.60, "fixed mask", ha="left", va="center", fontsize=8.6, fontweight="bold", color=PALETTE["red"])
    rounded_box(ax, (0.37, 0.535), 0.15, 0.11, "$M_0$", PALETTE["red_light"], PALETTE["red"], fontsize=10.5, weight="bold")
    arrow(ax, (0.54, 0.59), (0.72, 0.59), color=PALETTE["red"])
    ax.text(0.75, 0.59, "fails on\nfresh chips", ha="left", va="center", fontsize=8.1, color=PALETTE["red"])

    ax.text(0.07, 0.34, "resampled\nmasks", ha="left", va="center", fontsize=8.2, fontweight="bold", color=PALETTE["green"])
    for i, x0 in enumerate([0.42, 0.51, 0.60]):
        rounded_box(ax, (x0, 0.285), 0.065, 0.105, f"$M_{i+1}$", PALETTE["green_light"], PALETTE["green"], fontsize=8.7, weight="bold")
    ax.text(0.69, 0.34, "$\cdots$", ha="center", va="center", fontsize=11, color=PALETTE["green"])
    arrow(ax, (0.72, 0.34), (0.77, 0.34), color=PALETTE["green"])
    ax.text(0.80, 0.34, "transfers to\nfresh chips", ha="left", va="center", fontsize=8.1, color=PALETTE["green"])



fig = plt.figure(figsize=(8.4, 5.2))
gs = fig.add_gridspec(2, 2, width_ratios=[1.18, 1.0], height_ratios=[1.0, 1.0], wspace=0.40, hspace=0.58)
ax_a = fig.add_subplot(gs[:, 0])
ax_b = fig.add_subplot(gs[0, 1])
ax_c = fig.add_subplot(gs[1, 1])
fig.patch.set_facecolor("white")

# Panel A: schematic mechanism.
draw_mechanism_panel(ax_a)

# Panel B: algorithmic failure and rescue.
labels_a = ["8-bit\nIdeal", "4-bit\nIdeal", "4-bit\nEnsemble"]
means_a = [row["fresh_mean"] for row in ideal_rows]
stds_a = [row["fresh_std"] for row in ideal_rows]
colors_a = [PALETTE["blue"], PALETTE["red"], PALETTE["green"]]
ax_b.bar(np.arange(len(labels_a)), means_a, yerr=stds_a, capsize=3, color=colors_a, edgecolor=PALETTE["ink"], linewidth=0.6)
ax_b.set_ylim(0, 96)
ax_b.set_ylabel("Fresh accuracy (%)")
ax_b.set_xticks(np.arange(len(labels_a)))
ax_b.set_xticklabels(labels_a)
panel_label(ax_b, "B", "4-bit collapse and rescue")
ax_b.axhline(10, color="#777777", linestyle=":", linewidth=0.8)
for idx, value in enumerate(means_a):
    ax_b.text(idx, value + 3.0, f"{value:.1f}", ha="center", va="bottom", fontsize=8.5)
ax_b.spines[["top", "right"]].set_visible(False)
ax_b.grid(axis="y", alpha=0.18, linewidth=0.6)

# Panel C: PCM precision-retention frontier.
labels_b = ["8-bit", "6-bit", "4-bit"]
fresh_b = [row["fresh_mean"] for row in pcm_rows]
fresh_std_b = [row["fresh_std"] for row in pcm_rows]
drift_b = [row["drift_drop_1d_pp"] for row in pcm_rows]
x = np.arange(len(labels_b))
ax_c.bar(x, fresh_b, yerr=fresh_std_b, capsize=3, color=["#7FA8C9", PALETTE["green"], PALETTE["orange"]], edgecolor=PALETTE["ink"], linewidth=0.6)
ax_c.set_ylim(70, 80.7)
ax_c.set_ylabel("Fresh accuracy (%)")
ax_c.set_xticks(x)
ax_c.set_xticklabels(labels_b)
panel_label(ax_c, "C", "PCM precision-retention frontier")
for idx, value in enumerate(fresh_b):
    ax_c.text(idx, value + 0.34, f"{value:.1f}", ha="center", va="bottom", fontsize=8.4)
ax_c.spines[["top"]].set_visible(False)
ax_c.grid(axis="y", alpha=0.18, linewidth=0.6)

ax2 = ax_c.twinx()
ax2.plot(x, drift_b, color="#7A2E2E", marker="o", linewidth=1.9)
ax2.set_ylim(0, 4.7)
ax2.set_ylabel("1-day drift (pp)", color="#7A2E2E")
ax2.tick_params(axis="y", colors="#7A2E2E")
ax2.spines["top"].set_visible(False)
for idx, value in enumerate(drift_b):
    ax2.text(idx + 0.04, value + 0.12, f"{value:.2f}", color="#7A2E2E", fontsize=8.0)
ax_c.text(1, 70.45, "midpoint", ha="center", va="bottom", fontsize=7.8, color=PALETTE["green"], fontweight="bold")

for ext in ["pdf", "png"]:
    fig.savefig(FIG_DIR / f"fig1_paper1_spine.{ext}", bbox_inches="tight", dpi=300)
print(FIG_DIR / "fig1_paper1_spine.pdf")
print(SRC_DIR / "fig1_paper1_spine.csv")
print(SRC_DIR / "tab_pcm_precision_ladder.csv")
