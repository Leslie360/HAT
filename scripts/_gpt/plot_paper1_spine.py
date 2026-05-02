#!/usr/bin/env python3
"""Generate the main Paper-1 multi-panel spine figure and source-data tables."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / "paper" / "latex_gpt" / "figures"
SRC_DIR = ROOT / "paper" / "latex_gpt" / "source_data"
CKPT = ROOT / "paper2_aihwkit_baseline" / "checkpoints"
TINOS_DIR = Path("/usr/share/fonts/truetype/croscore")

for font_file in TINOS_DIR.glob("Tinos-*.ttf"):
    font_manager.fontManager.addfont(str(font_file))

FIG_DIR.mkdir(parents=True, exist_ok=True)
SRC_DIR.mkdir(parents=True, exist_ok=True)

COL = {
    "ink": "#1E252B",
    "muted": "#66717A",
    "rule": "#E1E6EB",
    "blue": "#0072B2",
    "blue_fill": "#E7F3FB",
    "red": "#D55E00",
    "red_fill": "#FBEADE",
    "green": "#009E73",
    "green_fill": "#E4F4EF",
    "gold": "#E69F00",
    "gold_fill": "#FFF1D8",
    "gray_fill": "#F5F6F7",
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
        "font.family": "Tinos",
        "font.serif": ["Tinos", "Times New Roman", "Nimbus Roman", "Liberation Serif", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 10.2,
        "axes.labelsize": 10.6,
        "axes.titlesize": 10.8,
        "xtick.labelsize": 9.4,
        "ytick.labelsize": 9.4,
        "axes.linewidth": 0.75,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)


def panel_header(ax, label: str, title: str, y: float = 1.04) -> None:
    ax.text(0.0, y, label, transform=ax.transAxes, ha="left", va="bottom", fontsize=12.6, fontweight="bold", color=COL["ink"])
    ax.text(0.14, y + 0.004, title, transform=ax.transAxes, ha="left", va="bottom", fontsize=10.8, fontweight="bold", color=COL["ink"])


def box(ax, x: float, y: float, w: float, h: float, text: str, fc: str, ec: str, fs: float = 7.5, weight: str = "bold") -> None:
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.010,rounding_size=0.020",
        linewidth=0.95,
        facecolor=fc,
        edgecolor=ec,
    )
    ax.add_patch(patch)
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, fontweight=weight, color=COL["ink"], linespacing=1.0)


def arrow(ax, x0: float, y0: float, x1: float, y1: float, color: str = COL["muted"], lw: float = 1.0) -> None:
    ax.add_patch(
        FancyArrowPatch(
            (x0, y0),
            (x1, y1),
            arrowstyle="-|>",
            mutation_scale=11,
            linewidth=lw,
            color=color,
        )
    )


def style_axis(ax) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color=COL["rule"], linewidth=0.55, alpha=0.65)
    ax.set_axisbelow(True)
    ax.tick_params(length=3, width=0.7, color=COL["ink"], labelcolor=COL["ink"])


fig = plt.figure(figsize=(9.0, 4.05), facecolor="white")
gs = fig.add_gridspec(1, 3, width_ratios=[1.42, 1.0, 1.05], wspace=0.40)
ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[0, 1])
ax_c = fig.add_subplot(gs[0, 2])
fig.subplots_adjust(left=0.055, right=0.985, top=0.88, bottom=0.18)

# Panel A: aligned schematic.
ax_a.set_axis_off()
ax_a.set_xlim(0, 1)
ax_a.set_ylim(0, 1)
panel_header(ax_a, "A", "Training objective", y=1.02)

row_y = [0.62, 0.25]
row_name = [("Fixed-mask HAT", COL["red"]), ("D2D-resampled HAT", COL["green"])]
for idx, y in enumerate(row_y):
    label, color = row_name[idx]
    ax_a.text(0.06, y + 0.205, label, ha="left", va="center", fontsize=8.8, color=color, fontweight="bold")
    box(ax_a, 0.06, y, 0.18, 0.15, "digital\nweights", COL["gray_fill"], "#9DA5AD", fs=8.6)
    arrow(ax_a, 0.245, y + 0.075, 0.315, y + 0.075)
    if idx == 0:
        box(ax_a, 0.32, y, 0.15, 0.15, "$M_0$", COL["red_fill"], COL["red"], fs=10.6)
        arrow(ax_a, 0.475, y + 0.075, 0.555, y + 0.075, color=COL["red"])
        box(ax_a, 0.56, y, 0.18, 0.15, "fresh\nchip", COL["gold_fill"], COL["gold"], fs=8.6)
        ax_a.text(0.78, y + 0.075, "fail", ha="left", va="center", fontsize=8.3, color=COL["red"], fontweight="bold")
    else:
        for k, x0 in enumerate([0.305, 0.385, 0.465]):
            box(ax_a, x0, y, 0.060, 0.15, f"$M_{k+1}$", COL["green_fill"], COL["green"], fs=8.2)
        ax_a.text(0.535, y + 0.075, "$\cdots$", ha="center", va="center", fontsize=12.0, color=COL["green"])
        arrow(ax_a, 0.56, y + 0.075, 0.615, y + 0.075, color=COL["green"])
        box(ax_a, 0.62, y, 0.18, 0.15, "fresh\nchip", COL["gold_fill"], COL["gold"], fs=8.6)
        ax_a.text(0.835, y + 0.075, "pass", ha="left", va="center", fontsize=8.3, color=COL["green"], fontweight="bold")

ax_a.plot([0.02, 0.97], [0.50, 0.50], color=COL["rule"], linewidth=0.7)
ax_a.text(0.06, 0.065, "Train over hardware-instance distribution.", ha="left", va="center", fontsize=8.1, color=COL["muted"])

# Panel B: failure/rescue data.
labels = ["8-bit\nideal", "4-bit\nfixed", "4-bit\nEnsemble"]
means = [float(row["fresh_mean"]) for row in ideal_rows]
stds = [float(row["fresh_std"]) for row in ideal_rows]
colors = [COL["blue"], COL["red"], COL["green"]]
x = np.arange(3)
ax_b.bar(
    x,
    means,
    yerr=stds,
    capsize=0,
    width=0.56,
    color=colors,
    edgecolor="white",
    linewidth=0.7,
    error_kw={"elinewidth": 0.8, "ecolor": "#555555"},
)
panel_header(ax_b, "B", "4-bit collapse and rescue", y=1.02)
ax_b.set_ylabel("Fresh accuracy (%)")
ax_b.set_ylim(0, 100)
ax_b.set_xticks(x)
ax_b.set_xticklabels(labels)
ax_b.axhline(10, color=COL["muted"], linestyle=(0, (1, 2)), linewidth=0.8)
for i, v in enumerate(means):
    ax_b.text(i, v + 3.0, f"{v:.1f}", ha="center", va="bottom", fontsize=8.8, fontweight="bold", color=COL["ink"])
style_axis(ax_b)

# Panel C: PCM precision/retention frontier.
labels_pcm = ["8-bit", "6-bit", "4-bit"]
fresh = [float(row["fresh_mean"]) for row in pcm_rows]
drift = [float(row["drift_drop_1d_pp"]) for row in pcm_rows]
bar_colors = ["#79A7C8", COL["green"], COL["gold"]]
panel_header(ax_c, "C", "PCM precision-retention frontier", y=1.02)
ax_c.set_ylabel("Fresh accuracy (%)")
ax_c.set_xlabel("1-day drift drop (pp, log scale)")
ax_c.set_xscale("log")
ax_c.set_xlim(0.025, 5.3)
ax_c.set_ylim(76.1, 78.6)
ax_c.set_xticks([0.04, 0.10, 1.0, 4.0])
ax_c.set_xticklabels(["0.04", "0.10", "1", "4"])
ax_c.plot(drift, fresh, color=COL["muted"], linewidth=1.25, zorder=1)
ax_c.scatter(drift, fresh, s=[54, 78, 60], color=bar_colors, edgecolor="white", linewidth=0.8, zorder=3)
for i, (label, xval, yval, dval) in enumerate(zip(labels_pcm, drift, fresh, drift)):
    dx = 1.06 if i < 2 else 0.88
    ha = "left" if i < 2 else "right"
    dy = 0.13 if i != 1 else 0.10
    ax_c.text(xval * dx, yval + dy, f"{label}\n{yval:.1f}%, {dval:.2f} pp", ha=ha, va="bottom", fontsize=8.8, fontweight="bold", color=COL["ink"], linespacing=1.0)
ax_c.annotate(
    "midpoint",
    xy=(drift[1], fresh[1]),
    xytext=(0.38, 78.25),
    textcoords="data",
    arrowprops={"arrowstyle": "-|>", "color": COL["green"], "lw": 0.9},
    ha="left",
    va="center",
    fontsize=9.2,
    fontweight="bold",
    color=COL["green"],
)
style_axis(ax_c)

for ext in ["pdf", "png"]:
    fig.savefig(FIG_DIR / f"fig1_paper1_spine.{ext}", dpi=300, bbox_inches="tight", pad_inches=0.04)

print(FIG_DIR / "fig1_paper1_spine.pdf")
print(SRC_DIR / "fig1_paper1_spine.csv")
print(SRC_DIR / "tab_pcm_precision_ladder.csv")
