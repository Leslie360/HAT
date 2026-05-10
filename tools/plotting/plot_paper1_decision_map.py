#!/usr/bin/env python3
"""Generate a clean main-text decision-map figure for Paper 1."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / "paper" / "latex_gpt" / "figures"
SRC_DIR = ROOT / "paper" / "latex_gpt" / "source_data"
FIG_DIR.mkdir(parents=True, exist_ok=True)
SRC_DIR.mkdir(parents=True, exist_ok=True)

# Top-tier Journal Palette (Nature style, matching fig1)
NATURE_TEAL = "#2A9D8F"
NATURE_CORAL = "#E76F51"
NATURE_GOLD = "#E9C46A"
NATURE_NAVY = "#264653"
GRAY_DARK = "#333333"
GRAY_LIGHT = "#AAAAAA"

COL = {
    "ink": GRAY_DARK,
    "muted": "#666666",
    "rule": "#E1E6EB",
    "blue": NATURE_NAVY,
    "blue_fill": "#F0F4F8",
    "red": NATURE_CORAL,
    "red_fill": "#FDF3F0",
    "green": NATURE_TEAL,
    "green_fill": "#EDF7F6",
    "gold": NATURE_GOLD,
    "gold_fill": "#FDF8ED",
}

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))

ideal_rows = read_csv(SRC_DIR / "fig1_paper1_spine.csv")
pcm_rows = read_csv(SRC_DIR / "tab_pcm_precision_ladder.csv")
ideal = {row["condition"].replace("\n", " "): row for row in ideal_rows}
pcm = {row["condition"].replace("\n", " "): row for row in pcm_rows}

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
        "condition": "PCM UnitCell 8-bit",
        "fresh_accuracy_pct": pcm["8-bit PCM"]["fresh_mean"],
        "drift_drop_1d_pp": pcm["8-bit PCM"]["drift_drop_1d_pp"],
        "decision": "deployment-stable practical point",
    },
    {
        "stage": "transition",
        "condition": "PCM UnitCell 6-bit",
        "fresh_accuracy_pct": pcm["6-bit PCM"]["fresh_mean"],
        "drift_drop_1d_pp": pcm["6-bit PCM"]["drift_drop_1d_pp"],
        "decision": "D2D-sensitive transition zone",
    },
]
with (SRC_DIR / "fig2_paper1_decision_map.csv").open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=list(summary_rows[0].keys()), lineterminator="\n")
    writer.writeheader()
    writer.writerows(summary_rows)

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 10.0,
    "axes.linewidth": 0.8,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

fig, ax = plt.subplots(figsize=(7.6, 4.2), facecolor="white")
ax.set_axis_off()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)

def panel_header(ax, label: str, title: str, x: float, y: float) -> None:
    ax.text(x, y, label, ha="left", va="bottom", fontsize=12, fontweight="bold", color=COL["ink"])
    ax.text(x + 0.035, y, title, ha="left", va="bottom", fontsize=11, fontweight="bold", color=COL["ink"])

def box(ax, x: float, y: float, w: float, h: float, fc: str, ec: str, lw: float = 0.8) -> None:
    ax.add_patch(
        FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.015,rounding_size=0.02",
            linewidth=lw, facecolor=fc, edgecolor=ec
        )
    )

def arrow(ax, x0: float, y0: float, x1: float, y1: float, color: str = COL["muted"], lw: float = 0.8) -> None:
    ax.add_patch(
        FancyArrowPatch(
            (x0, y0), (x1, y1),
            arrowstyle="-|>,head_width=4,head_length=6",
            linewidth=lw, color=color
        )
    )

fixed = float(ideal["IdealDevice 4-bit"]["fresh_mean"])
rescued = float(ideal["Ensemble HAT 4-bit"]["fresh_mean"])
base8 = float(ideal["IdealDevice 8-bit"]["fresh_mean"])
pcm_8 = pcm["8-bit PCM"]
pcm_6 = pcm["6-bit PCM"]
pcm_4 = pcm["4-bit PCM"]

# Panel A
panel_header(ax, "A", "Evidence: algorithmic failure and rescue", 0.02, 0.92)
box(ax, 0.03, 0.55, 0.16, 0.32, COL["red_fill"], COL["red"])
box(ax, 0.30, 0.55, 0.16, 0.32, COL["green_fill"], COL["green"])
arrow(ax, 0.20, 0.71, 0.29, 0.71)
ax.text(0.245, 0.73, "resample\nD2D masks", ha="center", va="bottom", fontsize=9, color=COL["muted"])

# A: Box 1
ax.text(0.11, 0.81, "4-bit fixed", ha="center", va="center", fontsize=10, fontweight="bold", color=COL["red"])
ax.text(0.11, 0.71, f"{fixed:.1f}%", ha="center", va="center", fontsize=16, fontweight="bold", color=COL["ink"])
ax.text(0.11, 0.63, "fresh", ha="center", va="center", fontsize=9, color=COL["muted"])
ax.text(0.11, 0.58, "reject", ha="center", va="center", fontsize=9, fontweight="bold", color=COL["red"])

# A: Box 2
ax.text(0.38, 0.81, "4-bit Ensemble", ha="center", va="center", fontsize=10, fontweight="bold", color=COL["green"])
ax.text(0.38, 0.71, f"{rescued:.1f}%", ha="center", va="center", fontsize=16, fontweight="bold", color=COL["ink"])
ax.text(0.38, 0.63, f"near 8-bit ({base8:.1f}%)", ha="center", va="center", fontsize=9, color=COL["muted"])
ax.text(0.38, 0.58, "rescue", ha="center", va="center", fontsize=9, fontweight="bold", color=COL["green"])

# Divider
ax.plot([0.49, 0.49], [0.5, 0.95], color=COL["rule"], linewidth=0.8, linestyle="--")

# Panel B
panel_header(ax, "B", "Evidence: physical precision-retention", 0.52, 0.92)
precision_cards = [
    (0.52, "8-bit", pcm_8, COL["blue"], COL["blue_fill"], "safe"),
    (0.675, "6-bit", pcm_6, COL["green"], COL["green_fill"], "transition"),
    (0.83, "4-bit", pcm_4, COL["gold"], COL["gold_fill"], "drift-limited"),
]
for x, label, row, color, fill, role in precision_cards:
    w = 0.135
    box(ax, x, 0.55, w, 0.32, fill, color, lw=1.2 if label == "8-bit" else 0.8)
    fresh = float(row["fresh_mean"])
    drift = float(row["drift_drop_1d_pp"])
    ax.text(x + w/2, 0.81, label, ha="center", va="center", fontsize=10, fontweight="bold", color=color)
    ax.text(x + w/2, 0.71, f"{fresh:.1f}%", ha="center", va="center", fontsize=16, fontweight="bold", color=COL["ink"])
    drift_color = COL["red"] if drift > 1.0 else COL["green"]
    ax.text(x + w/2, 0.63, f"{drift:.2f} pp drift", ha="center", va="center", fontsize=9, color=drift_color)
    ax.text(x + w/2, 0.58, role, ha="center", va="center", fontsize=9, fontweight="bold", color=color)

# Panel C
panel_header(ax, "C", "Decision rule", 0.02, 0.40)
rule_y = 0.15
rule_h = 0.20
rule_w = 0.28
steps = [
    (0.04, "1", "Diagnose", "fresh-instance collapse", COL["red"], COL["red_fill"]),
    (0.36, "2", "Train", "D2D-resampled\nEnsemble HAT", COL["green"], COL["green_fill"]),
    (0.68, "3", "Deploy", "8-bit PCM, or\nrefresh 4-bit", COL["blue"], COL["blue_fill"]),
]
for i, (x, num, head, body, color, fill) in enumerate(steps):
    box(ax, x, rule_y, rule_w, rule_h, fill, color, lw=0.8)
    ax.text(x + 0.035, rule_y + rule_h/2, num, ha="center", va="center", fontsize=11, fontweight="bold", color="white", bbox={"boxstyle": "circle,pad=0.2", "facecolor": color, "edgecolor": "none"})
    ax.text(x + 0.16, rule_y + rule_h - 0.05, head, ha="center", va="center", fontsize=10, fontweight="bold", color=color)
    ax.text(x + 0.16, rule_y + 0.06, body, ha="center", va="center", fontsize=10, color=COL["ink"])
    if i < 2:
        arrow(ax, x + rule_w + 0.01, rule_y + rule_h/2, steps[i+1][0] - 0.01, rule_y + rule_h/2)

ax.text(0.5, 0.05, "Claim boundary: algorithmic generalization and physical retention are separate deployment decisions.", ha="center", va="center", fontsize=10, color=COL["muted"], style="italic")

for ext in ["pdf", "png"]:
    fig.savefig(FIG_DIR / f"fig2_paper1_decision_map.{ext}", bbox_inches="tight", pad_inches=0.04, dpi=300)

print(FIG_DIR / "fig2_paper1_decision_map.pdf")
print(SRC_DIR / "fig2_paper1_decision_map.csv")
