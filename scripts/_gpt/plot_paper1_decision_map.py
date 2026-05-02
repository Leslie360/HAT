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
TINOS_DIR = Path("/usr/share/fonts/truetype/croscore")
FIG_DIR.mkdir(parents=True, exist_ok=True)
SRC_DIR.mkdir(parents=True, exist_ok=True)

for font_file in TINOS_DIR.glob("Tinos-*.ttf"):
    font_manager.fontManager.addfont(str(font_file))

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
        "font.family": "Tinos",
        "font.serif": ["Tinos", "Times New Roman", "Nimbus Roman", "Liberation Serif", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 12.0,
        "axes.linewidth": 0.75,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)


def panel_header(ax, label: str, title: str, x: float, y: float) -> None:
    ax.text(x, y, label, ha="left", va="bottom", fontsize=15.2, fontweight="bold", color=COL["ink"])
    ax.text(x + 0.044, y + 0.003, title, ha="left", va="bottom", fontsize=13.4, fontweight="bold", color=COL["ink"])


def box(ax, x: float, y: float, w: float, h: float, fc: str, ec: str, lw: float = 0.95) -> None:
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.012,rounding_size=0.025",
            linewidth=lw,
            facecolor=fc,
            edgecolor=ec,
        )
    )


def arrow(ax, x0: float, y0: float, x1: float, y1: float, color: str = COL["muted"], lw: float = 1.0) -> None:
    ax.add_patch(
        FancyArrowPatch(
            (x0, y0),
            (x1, y1),
            arrowstyle="-|>",
            mutation_scale=12,
            linewidth=lw,
            color=color,
        )
    )


fixed = float(ideal["IdealDevice 4-bit"]["fresh_mean"])
rescued = float(ideal["Ensemble HAT 4-bit"]["fresh_mean"])
base8 = float(ideal["IdealDevice 8-bit"]["fresh_mean"])
pcm_8 = pcm["8-bit PCM"]
pcm_6 = pcm["6-bit PCM"]
pcm_4 = pcm["4-bit PCM"]

fig, ax = plt.subplots(figsize=(9.4, 5.10), facecolor="white")
ax.set_axis_off()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
fig.subplots_adjust(left=0.030, right=0.990, top=0.950, bottom=0.070)

# Panel A/B: evidence cards.
panel_header(ax, "A", "Evidence: failure and rescue", 0.02, 0.90)
panel_header(ax, "B", "Evidence: physical precision", 0.57, 0.90)

card_y = 0.55
card_h = 0.31
card_w = 0.168
cards = [
    (0.03, "4-bit fixed", f"{fixed:.1f}%", "fresh", "reject", COL["red"], COL["red_fill"]),
    (0.250, "4-bit Ensemble", f"{rescued:.1f}%", f"near 8-bit ({base8:.1f}%)", "rescue", COL["green"], COL["green_fill"]),
]
for x, title, number, sub, footer, color, fill in cards:
    box(ax, x, card_y, card_w, card_h, fill, color, lw=1.15)
    ax.text(x + card_w / 2, card_y + 0.238, title, ha="center", va="center", fontsize=11.8, fontweight="bold", color=color)
    ax.text(x + card_w / 2, card_y + 0.148, number, ha="center", va="center", fontsize=25.0, fontweight="bold", color=COL["ink"])
    ax.text(x + card_w / 2, card_y + 0.070, sub, ha="center", va="center", fontsize=10.8, color=COL["muted"])
    ax.text(x + card_w / 2, card_y - 0.060, footer, ha="center", va="top", fontsize=10.8, fontweight="bold", color=color)
arrow(ax, 0.198, card_y + card_h / 2, 0.247, card_y + card_h / 2)
ax.text(0.226, card_y + card_h / 2 + 0.074, "resample\nD2D masks", ha="center", va="center", fontsize=11.6, color=COL["muted"])

precision_cards = [
    (0.565, "8-bit", pcm_8, COL["blue"], COL["blue_fill"], "safe"),
    (0.715, "6-bit", pcm_6, COL["green"], COL["green_fill"], "midpoint"),
    (0.865, "4-bit", pcm_4, COL["gold"], COL["gold_fill"], "drift-limited"),
]
for x, label, row, color, fill, role in precision_cards:
    w = 0.115
    box(ax, x, card_y, w, card_h, fill, color, lw=1.55 if label == "6-bit" else 1.0)
    fresh = float(row["fresh_mean"])
    drift = float(row["drift_drop_1d_pp"])
    ax.text(x + w / 2, card_y + 0.238, label, ha="center", va="center", fontsize=13.4, fontweight="bold", color=color)
    ax.text(x + w / 2, card_y + 0.133, f"{fresh:.1f}%", ha="center", va="center", fontsize=19.4, fontweight="bold", color=COL["ink"])
    drift_color = COL["red"] if drift > 1.0 else COL["green"]
    ax.text(x + w / 2, card_y + 0.078, f"{drift:.2f} pp", ha="center", va="center", fontsize=11.5, fontweight="bold", color=drift_color)
    ax.text(x + w / 2, card_y + 0.030, "1-day drift", ha="center", va="center", fontsize=9.6, color=COL["muted"])
    ax.text(x + w / 2, card_y - 0.060, role, ha="center", va="top", fontsize=10.6, fontweight="bold", color=color)

# Vertical divider.
ax.plot([0.515, 0.515], [0.48, 0.88], color=COL["rule"], linewidth=0.9)

# Panel C: decision rule chain.
panel_header(ax, "C", "Decision rule", 0.02, 0.360)
rule_y = 0.080
rule_h = 0.245
rule_w = 0.245
steps = [
    (0.075, "1", "diagnose", "fresh-instance\ncollapse", COL["red"], COL["red_fill"]),
    (0.382, "2", "train", "D2D-resampled\nEnsemble HAT", COL["green"], COL["green_fill"]),
    (0.690, "3", "deploy", "6-bit PCM unless\nrefreshing 4-bit", COL["blue"], COL["blue_fill"]),
]
for i, (x, num, head, body, color, fill) in enumerate(steps):
    box(ax, x, rule_y, rule_w, rule_h, fill, color, lw=1.05)
    ax.text(x + 0.043, rule_y + rule_h / 2, num, ha="center", va="center", fontsize=15.2, fontweight="bold", color="white", bbox={"boxstyle": "circle,pad=0.18", "facecolor": color, "edgecolor": "none"})
    ax.text(x + 0.142, rule_y + 0.166, head, ha="center", va="center", fontsize=12.2, fontweight="bold", color=color)
    ax.text(x + 0.142, rule_y + 0.085, body, ha="center", va="center", fontsize=11.2, color=COL["ink"], linespacing=1.0)
    if i < 2:
        arrow(ax, x + rule_w + 0.012, rule_y + rule_h / 2, x + 0.285, rule_y + rule_h / 2)

ax.text(0.50, 0.016, "Claim boundary: algorithmic generalization and physical retention are separate deployment decisions.", ha="center", va="bottom", fontsize=10.5, color=COL["muted"])

for ext in ["pdf", "png"]:
    fig.savefig(FIG_DIR / f"fig2_paper1_decision_map.{ext}", bbox_inches="tight", pad_inches=0.04, dpi=300)

print(FIG_DIR / "fig2_paper1_decision_map.pdf")
print(SRC_DIR / "fig2_paper1_decision_map.csv")
