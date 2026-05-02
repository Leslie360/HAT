#!/usr/bin/env python3
"""Generate a main-text decision-map figure for Paper 1."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / "paper" / "latex_gpt" / "figures"
SRC_DIR = ROOT / "paper" / "latex_gpt" / "source_data"
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
    "paper": "#FAFAF7",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


ideal_rows = read_csv(SRC_DIR / "fig1_paper1_spine.csv")
pcm_rows = read_csv(SRC_DIR / "tab_pcm_precision_ladder.csv")

ideal = {row["condition"]: row for row in ideal_rows}
pcm = {row["condition"]: row for row in pcm_rows}

summary_rows = [
    {
        "stage": "failure",
        "condition": "IdealDevice 4-bit fixed-mask",
        "fresh_accuracy_pct": ideal["IdealDevice 4-bit"]["fresh_mean"],
        "drift_drop_1d_pp": "NA",
        "decision": "reject fixed-mask 4-bit",
    },
    {
        "stage": "rescue",
        "condition": "IdealDevice 4-bit Ensemble HAT",
        "fresh_accuracy_pct": ideal["Ensemble HAT 4-bit"]["fresh_mean"],
        "drift_drop_1d_pp": "NA",
        "decision": "distribution-level HAT works",
    },
    {
        "stage": "physical_frontier",
        "condition": "PCM UnitCell 6-bit",
        "fresh_accuracy_pct": pcm["6-bit PCM"]["fresh_mean"],
        "drift_drop_1d_pp": pcm["6-bit PCM"]["drift_drop_1d_pp"],
        "decision": "best tested deployment midpoint",
    },
]
with (SRC_DIR / "fig2_paper1_decision_map.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(summary_rows[0].keys()), lineterminator="\n")
    writer.writeheader()
    writer.writerows(summary_rows)

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 8.8,
        "axes.labelsize": 8.6,
        "axes.titlesize": 9.0,
        "xtick.labelsize": 7.8,
        "ytick.labelsize": 7.8,
        "axes.linewidth": 0.8,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)

fig = plt.figure(figsize=(8.4, 4.85), facecolor="white")
gs = fig.add_gridspec(2, 2, width_ratios=[1.02, 1.18], height_ratios=[1.0, 0.48], wspace=0.28, hspace=0.40)
ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[0, 1])
ax_c = fig.add_subplot(gs[1, :])


def panel_title(ax, label: str, title: str) -> None:
    ax.text(0.00, 1.04, label, transform=ax.transAxes, fontsize=11, fontweight="bold", va="bottom", color=PALETTE["ink"])
    ax.text(0.075, 1.045, title, transform=ax.transAxes, fontsize=9.2, fontweight="bold", va="bottom", color=PALETTE["ink"])


def rounded(ax, xy, wh, fc, ec, text=None, fontsize=8.6, weight="normal", color=None, lw=1.0):
    patch = FancyBboxPatch(
        xy,
        wh[0],
        wh[1],
        boxstyle="round,pad=0.018,rounding_size=0.035",
        facecolor=fc,
        edgecolor=ec,
        linewidth=lw,
    )
    ax.add_patch(patch)
    if text:
        ax.text(xy[0] + wh[0] / 2, xy[1] + wh[1] / 2, text, ha="center", va="center", fontsize=fontsize, fontweight=weight, color=color or PALETTE["ink"])
    return patch


def arrow(ax, start, end, color=None, lw=1.2, rad=0.0):
    ax.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=13,
            linewidth=lw,
            color=color or PALETTE["muted"],
            connectionstyle=f"arc3,rad={rad}",
        )
    )

# Panel A: failure and algorithmic treatment.
ax_a.set_axis_off()
ax_a.set_xlim(0, 1)
ax_a.set_ylim(0, 1)
panel_title(ax_a, "A", "Failure mode and treatment")

fixed = float(ideal["IdealDevice 4-bit"]["fresh_mean"])
rescued = float(ideal["Ensemble HAT 4-bit"]["fresh_mean"])
base8 = float(ideal["IdealDevice 8-bit"]["fresh_mean"])

rounded(ax_a, (0.05, 0.60), (0.34, 0.20), PALETTE["red_light"], PALETTE["red"], "fixed-mask\n4-bit HAT", fontsize=8.0, weight="bold", color=PALETTE["red"])
rounded(ax_a, (0.61, 0.60), (0.34, 0.20), PALETTE["green_light"], PALETTE["green"], "Ensemble HAT\n4-bit", fontsize=8.0, weight="bold", color=PALETTE["green"])
arrow(ax_a, (0.40, 0.695), (0.60, 0.695), color=PALETTE["muted"])
ax_a.text(0.50, 0.805, "resample D2D masks", ha="center", va="bottom", fontsize=6.9, color=PALETTE["muted"])

ax_a.text(0.22, 0.46, f"{fixed:.1f}%", ha="center", va="center", fontsize=17.5, fontweight="bold", color=PALETTE["red"])
ax_a.text(0.22, 0.35, "fresh accuracy", ha="center", va="center", fontsize=8.1, color=PALETTE["muted"])
ax_a.text(0.78, 0.46, f"{rescued:.1f}%", ha="center", va="center", fontsize=17.5, fontweight="bold", color=PALETTE["green"])
ax_a.text(0.78, 0.35, f"near 8-bit baseline ({base8:.1f}%)", ha="center", va="center", fontsize=7.3, color=PALETTE["muted"])

rounded(ax_a, (0.12, 0.10), (0.76, 0.12), "#F6F6F6", "#CCCCCC", "Randomize hardware instances, not data labels.", fontsize=7.2, color=PALETTE["ink"])

# Panel B: PCM deployment frontier as compact card table.
ax_b.set_axis_off()
ax_b.set_xlim(0, 1)
ax_b.set_ylim(0, 1)
panel_title(ax_b, "B", "PCM precision choice")

cards = [
    ("8-bit", pcm["8-bit PCM"], PALETTE["blue"], PALETTE["blue_light"], "safe\nreference"),
    ("6-bit", pcm["6-bit PCM"], PALETTE["green"], PALETTE["green_light"], "chosen\nmidpoint"),
    ("4-bit", pcm["4-bit PCM"], PALETTE["orange"], PALETTE["orange_light"], "drift\nlimited"),
]
for i, (label, row, color, fill, role) in enumerate(cards):
    x0 = 0.04 + i * 0.32
    w = 0.28
    ec = color
    lw = 1.7 if label == "6-bit" else 1.0
    rounded(ax_b, (x0, 0.18), (w, 0.65), fill, ec, lw=lw)
    ax_b.text(x0 + w / 2, 0.76, label, ha="center", va="center", fontsize=11.4, fontweight="bold", color=color)
    fresh = float(row["fresh_mean"])
    drift = float(row["drift_drop_1d_pp"])
    ax_b.text(x0 + w / 2, 0.60, f"{fresh:.1f}%", ha="center", va="center", fontsize=14.6, fontweight="bold", color=PALETTE["ink"])
    ax_b.text(x0 + w / 2, 0.50, "fresh", ha="center", va="center", fontsize=7.9, color=PALETTE["muted"])
    # Bar uses 70-80% domain to show that all PCM settings train.
    bx, by, bw, bh = x0 + 0.04, 0.405, w - 0.08, 0.035
    ax_b.add_patch(Rectangle((bx, by), bw, bh, facecolor="white", edgecolor="#D0D0D0", linewidth=0.5))
    ax_b.add_patch(Rectangle((bx, by), bw * np.clip((fresh - 70) / 10, 0, 1), bh, facecolor=color, edgecolor="none", alpha=0.86))
    ax_b.text(x0 + w / 2, 0.30, f"{drift:.2f} pp", ha="center", va="center", fontsize=10.4, fontweight="bold", color=PALETTE["red"] if drift > 1 else PALETTE["green"])
    ax_b.text(x0 + w / 2, 0.225, "1-day drift", ha="center", va="center", fontsize=7.5, color=PALETTE["muted"])
    ax_b.text(x0 + w / 2, 0.105, role, ha="center", va="top", fontsize=7.7, color=color, fontweight="bold")

# Panel C: actionable rule chain.
ax_c.set_axis_off()
ax_c.set_xlim(0, 1)
ax_c.set_ylim(0, 1)
panel_title(ax_c, "C", "Claim boundary and deployment rule")

steps = [
    ("1", "diagnose", "fresh-instance\ncollapse", PALETTE["red"], PALETTE["red_light"]),
    ("2", "train", "D2D-resampled\nEnsemble HAT", PALETTE["green"], PALETTE["green_light"]),
    ("3", "deploy", "6-bit PCM unless\nrefreshing 4-bit", PALETTE["blue"], PALETTE["blue_light"]),
]
for i, (num, head, body, color, fill) in enumerate(steps):
    x0 = 0.055 + i * 0.315
    rounded(ax_c, (x0, 0.22), (0.235, 0.48), fill, color, lw=1.1)
    ax_c.text(x0 + 0.040, 0.59, num, ha="center", va="center", fontsize=10.5, fontweight="bold", color="white", bbox={"boxstyle": "circle,pad=0.20", "facecolor": color, "edgecolor": "none"})
    ax_c.text(x0 + 0.142, 0.60, head, ha="center", va="center", fontsize=8.1, fontweight="bold", color=color)
    ax_c.text(x0 + 0.118, 0.40, body, ha="center", va="center", fontsize=7.7, color=PALETTE["ink"])
    if i < 2:
        arrow(ax_c, (x0 + 0.245, 0.46), (x0 + 0.305, 0.46), color=PALETTE["muted"], lw=1.0)

ax_c.text(0.50, 0.08, "Main claim: algorithmic generalization and physical retention are separate decisions.", ha="center", va="center", fontsize=7.8, color=PALETTE["muted"])

for ext in ["pdf", "png"]:
    fig.savefig(FIG_DIR / f"fig2_paper1_decision_map.{ext}", bbox_inches="tight", dpi=300)

print(FIG_DIR / "fig2_paper1_decision_map.pdf")
print(SRC_DIR / "fig2_paper1_decision_map.csv")
