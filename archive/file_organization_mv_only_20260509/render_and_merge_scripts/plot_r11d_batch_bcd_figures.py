#!/usr/bin/env python3
"""Generate Batch B/C/D figures with publication-quality styling.

Matches Codex visual standards:
- Tinos font family
- Colorblind-safe palette
- Larger typography
- Light grid lines
- Bold key labels
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / "paper2_aihwkit_baseline" / "figures"
CKPT = ROOT / "paper2_aihwkit_baseline" / "checkpoints"
TINOS_DIR = Path("/usr/share/fonts/truetype/croscore")

for font_file in TINOS_DIR.glob("Tinos-*.ttf"):
    font_manager.fontManager.addfont(str(font_file))

FIG_DIR.mkdir(parents=True, exist_ok=True)

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


def apply_rc() -> None:
    plt.rcParams.update(
        {
            "font.family": "Tinos",
            "font.serif": ["Tinos", "Times New Roman", "Nimbus Roman", "Liberation Serif", "DejaVu Serif"],
            "mathtext.fontset": "stix",
            "font.size": 10.5,
            "axes.titlesize": 12.5,
            "axes.labelsize": 11.0,
            "xtick.labelsize": 9.5,
            "ytick.labelsize": 9.5,
            "legend.fontsize": 9.0,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.edgecolor": COL["ink"],
            "axes.labelcolor": COL["ink"],
            "text.color": COL["ink"],
            "xtick.color": COL["ink"],
            "ytick.color": COL["ink"],
        }
    )


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def read_training_acc(run_id: str) -> list[float]:
    """Read test accuracy history from checkpoint."""
    path = CKPT / run_id / "training_history.json"
    if not path.exists():
        return []
    data = load_json(path)
    if "test_acc_history" in data:
        return data["test_acc_history"]
    if "history" in data:
        return [float(e["test_acc"]) for e in data["history"]]
    return []


# ═══════════════════════════════════════════════════════════════════════════════
# Figure 1: Drift comparison over time
# ═══════════════════════════════════════════════════════════════════════════════
def fig_drift_comparison() -> None:
    apply_rc()

    times = np.array([0, 1, 24], dtype=float)
    time_labels = ["0 s", "1 h", "1 d"]

    configs = [
        {
            "label": "4-bit PCM  UnitCell",
            "values": [76.64, 74.04, 72.64],
            "color": COL["red"],
            "marker": "o",
            "ls": "-",
            "lw": 2.2,
        },
        {
            "label": "4-bit PCM  PCMPresetDevice",
            "values": [76.37, 74.72, 73.19],
            "color": COL["red"],
            "marker": "s",
            "ls": "--",
            "lw": 1.8,
        },
        {
            "label": "6-bit PCM  seed 123",
            "values": [77.35, 77.26, 77.19],
            "color": COL["gold"],
            "marker": "o",
            "ls": "-",
            "lw": 2.2,
        },
        {
            "label": "6-bit PCM  seed 789",
            "values": [77.69, 77.75, 77.65],
            "color": COL["gold"],
            "marker": "s",
            "ls": "--",
            "lw": 1.8,
        },
        {
            "label": "8-bit PCM  UnitCell",
            "values": [77.61, 77.49, 77.57],
            "color": COL["green"],
            "marker": "o",
            "ls": "-",
            "lw": 2.2,
        },
        {
            "label": "8-bit PCM  PCMPresetDevice",
            "values": [76.94, 76.70, 76.87],
            "color": COL["green"],
            "marker": "s",
            "ls": "--",
            "lw": 1.8,
        },
        {
            "label": "8-bit Oracle  (no modifier noise)",
            "values": [76.94, 76.66, 76.67],
            "color": COL["blue"],
            "marker": "D",
            "ls": "-.",
            "lw": 2.0,
        },
    ]

    fig, ax = plt.subplots(figsize=(9.2, 5.2), facecolor="white")

    for cfg in configs:
        vals = np.array(cfg["values"])
        ax.plot(
            times,
            vals,
            label=cfg["label"],
            color=cfg["color"],
            marker=cfg["marker"],
            linestyle=cfg["ls"],
            linewidth=cfg["lw"],
            markersize=6.5,
            markeredgecolor="white",
            markeredgewidth=0.6,
            zorder=3,
        )
        drop = vals[-1] - vals[0]
        offset_y = -12 if drop < -1.0 else (-8 if drop < 0 else 10)
        ax.annotate(
            f"{drop:+.2f} pp",
            xy=(times[-1], vals[-1]),
            xytext=(7, offset_y),
            textcoords="offset points",
            fontsize=8.2,
            color=cfg["color"],
            fontweight="bold",
            ha="left",
            va="center",
        )

    ax.set_xlabel("Retention time")
    ax.set_ylabel("Test accuracy (%)")
    ax.set_title("PCM retention drift across bit-widths, presets and oracle", fontweight="bold")
    ax.set_xticks(times)
    ax.set_xticklabels(time_labels)
    ax.set_ylim(70.5, 79.0)
    ax.set_xlim(-1.5, 27.0)
    ax.grid(axis="y", color=COL["rule"], linewidth=0.55, alpha=0.65, zorder=0)
    ax.grid(axis="x", color=COL["rule"], linewidth=0.55, alpha=0.65, zorder=0)
    ax.tick_params(length=3, width=0.7, color=COL["ink"], labelcolor=COL["ink"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(
        loc="lower left",
        frameon=True,
        fancybox=False,
        edgecolor=COL["rule"],
        facecolor="white",
        framealpha=0.95,
    )

    plt.tight_layout()
    fig.savefig(FIG_DIR / "r11d_drift_comparison_all_configs.pdf", dpi=300, bbox_inches="tight")
    fig.savefig(FIG_DIR / "r11d_drift_comparison_all_configs.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("Saved drift comparison figure.")


# ═══════════════════════════════════════════════════════════════════════════════
# Figure 2: Precision–drift scatter
# ═══════════════════════════════════════════════════════════════════════════════
def fig_precision_drift_scatter() -> None:
    apply_rc()

    points = [
        ("4-bit UnitCell", 76.71, -4.01, COL["red"], "o"),
        ("4-bit PCMPresetDevice", 76.47, -3.18, COL["red"], "s"),
        ("6-bit seed 123", 77.33, -0.16, COL["gold"], "o"),
        ("6-bit seed 789", 77.81, -0.04, COL["gold"], "s"),
        ("8-bit UnitCell", 77.64, -0.04, COL["green"], "o"),
        ("8-bit PCMPresetDevice", 76.88, -0.07, COL["green"], "s"),
        ("8-bit Oracle", 76.80, -0.27, COL["blue"], "D"),
    ]

    fig, ax = plt.subplots(figsize=(7.2, 5.6), facecolor="white")

    annot_offsets = {
        "4-bit UnitCell": (8, -14),
        "4-bit PCMPresetDevice": (8, 6),
        "6-bit seed 123": (8, 6),
        "6-bit seed 789": (8, 6),
        "8-bit UnitCell": (8, 6),
        "8-bit PCMPresetDevice": (-10, 8),
        "8-bit Oracle": (8, -14),
    }
    for label, source, drop, color, marker in points:
        ax.scatter(
            source,
            drop,
            s=140,
            c=color,
            marker=marker,
            edgecolors="white",
            linewidths=0.8,
            zorder=3,
            alpha=0.95,
        )
        ox, oy = annot_offsets.get(label, (8, 5))
        ax.annotate(
            label,
            (source, drop),
            textcoords="offset points",
            xytext=(ox, oy),
            fontsize=8.5,
            color=COL["ink"],
            fontweight="bold",
        )

    ax.axhline(0, color=COL["rule"], linewidth=1.0, linestyle="-", zorder=0)
    ax.axhline(-0.5, color=COL["rule"], linewidth=0.7, linestyle="--", zorder=0, alpha=0.6)
    ax.axvline(77.0, color=COL["rule"], linewidth=0.7, linestyle="--", zorder=0, alpha=0.6)

    ax.set_xlabel("Source best accuracy (%)")
    ax.set_ylabel("Drift drop 0 s → 1 d (percentage points)")
    ax.set_title("Precision–drift trade-off", fontweight="bold")
    ax.set_xlim(75.8, 78.2)
    ax.set_ylim(-4.8, 0.6)
    ax.grid(axis="y", color=COL["rule"], linewidth=0.55, alpha=0.65, zorder=0)
    ax.grid(axis="x", color=COL["rule"], linewidth=0.55, alpha=0.65, zorder=0)
    ax.tick_params(length=3, width=0.7, color=COL["ink"], labelcolor=COL["ink"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Zone labels
    ax.text(0.02, 0.18, "Binary regime:\n4-bit  →  high drift", transform=ax.transAxes,
            fontsize=9.0, color=COL["red"], fontweight="bold", va="bottom",
            bbox=dict(boxstyle="round,pad=0.25", facecolor=COL["red_fill"], edgecolor=COL["red"], linewidth=0.6, alpha=0.85))
    ax.text(0.02, 0.98, "Drift-safe:\n6/8-bit  →  low drift", transform=ax.transAxes,
            fontsize=9.0, color=COL["green"], fontweight="bold", va="top",
            bbox=dict(boxstyle="round,pad=0.25", facecolor=COL["green_fill"], edgecolor=COL["green"], linewidth=0.6, alpha=0.85))

    plt.tight_layout()
    fig.savefig(FIG_DIR / "r11d_precision_drift_scatter.pdf", dpi=300, bbox_inches="tight")
    fig.savefig(FIG_DIR / "r11d_precision_drift_scatter.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("Saved precision–drift scatter.")


# ═══════════════════════════════════════════════════════════════════════════════
# Figure 3: Source / Fresh / Drift bars
# ═══════════════════════════════════════════════════════════════════════════════
def fig_source_fresh_drift_bars() -> None:
    apply_rc()

    configs = [
        ("4-bit\nUnitCell", [76.71, 76.68, 72.64], COL["red"]),
        ("4-bit\nPCMPreset", [76.47, 76.38, 73.19], COL["red"]),
        ("6-bit\nseed 123", [77.33, 77.36, 77.19], COL["gold"]),
        ("6-bit\nseed 789", [77.81, 77.75, 77.65], COL["gold"]),
        ("8-bit\nUnitCell", [77.64, 77.60, 77.57], COL["green"]),
        ("8-bit\nPCMPreset", [76.88, 76.80, 76.87], COL["green"]),
        ("8-bit\nOracle", [76.80, 76.70, 76.67], COL["blue"]),
    ]

    fig, ax = plt.subplots(figsize=(9.8, 5.0), facecolor="white")

    n = len(configs)
    x = np.arange(n)
    width = 0.22

    source_vals = [c[1][0] for c in configs]
    fresh_vals = [c[1][1] for c in configs]
    drift_vals = [c[1][2] for c in configs]
    colors = [c[2] for c in configs]

    bars1 = ax.bar(x - width, source_vals, width, label="Source best",
                   color=colors, edgecolor="white", linewidth=0.6, alpha=0.95, zorder=2)
    bars2 = ax.bar(x, fresh_vals, width, label="Fresh eval",
                   color=colors, edgecolor="white", linewidth=0.6, alpha=0.65, zorder=2)
    bars3 = ax.bar(x + width, drift_vals, width, label="Drift @ 1 d",
                   color=colors, edgecolor="white", linewidth=0.6, alpha=0.35, zorder=2)

    for bars in (bars1, bars2, bars3):
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                height + 0.35,
                f"{height:.1f}",
                ha="center",
                va="bottom",
                fontsize=7.0,
                color=COL["ink"],
                fontweight="bold",
            )

    ax.set_ylabel("Test accuracy (%)")
    ax.set_title("Source, fresh and 1-day drift accuracy by configuration", fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels([c[0] for c in configs], fontsize=8.5)
    ax.set_ylim(68, 80)
    ax.grid(axis="y", color=COL["rule"], linewidth=0.55, alpha=0.65, zorder=0)
    ax.tick_params(length=3, width=0.7, color=COL["ink"], labelcolor=COL["ink"])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(
        loc="upper right",
        frameon=True,
        fancybox=False,
        edgecolor=COL["rule"],
        facecolor="white",
        framealpha=0.95,
    )

    plt.tight_layout()
    fig.savefig(FIG_DIR / "r11d_source_fresh_drift_bars.pdf", dpi=300, bbox_inches="tight")
    fig.savefig(FIG_DIR / "r11d_source_fresh_drift_bars.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("Saved source/fresh/drift bars.")


# ═══════════════════════════════════════════════════════════════════════════════
# Figure 4: Training curves overlay
# ═══════════════════════════════════════════════════════════════════════════════
def fig_training_curves() -> None:
    apply_rc()

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.0), facecolor="white")

    # 4-bit configs
    four_bit = [
        ("r11d_7_pcm_4bit_seed123", "seed 123", COL["red"], "-"),
        ("r11d_7_pcm_4bit_seed456_clean", "seed 456", COL["red"], "--"),
        ("r11d_7_pcm_4bit_seed789", "seed 789", COL["red"], "-."),
    ]
    for run_id, label, color, ls in four_bit:
        acc = read_training_acc(run_id)
        if acc:
            axes[0].plot(
                range(1, len(acc) + 1),
                acc,
                label=label,
                color=color,
                linestyle=ls,
                linewidth=1.6,
                alpha=0.9,
            )

    # 8-bit configs
    eight_bit = [
        ("r11d_5a_pcm_seed123", "seed 123", COL["green"], "-"),
        ("r11d_5a_pcm_seed456", "seed 456", COL["green"], "--"),
        ("r11d_5a_pcm_seed789", "seed 789", COL["green"], "-."),
    ]
    for run_id, label, color, ls in eight_bit:
        acc = read_training_acc(run_id)
        if acc:
            axes[1].plot(
                range(1, len(acc) + 1),
                acc,
                label=label,
                color=color,
                linestyle=ls,
                linewidth=1.6,
                alpha=0.9,
            )

    # 6-bit configs
    six_bit = [
        ("r11d_6bit_pcm_seed123", "seed 123", COL["gold"], "-"),
        ("r11d_6bit_pcm_seed789", "seed 789", COL["gold"], "--"),
    ]
    for run_id, label, color, ls in six_bit:
        acc = read_training_acc(run_id)
        if acc:
            axes[2].plot(
                range(1, len(acc) + 1),
                acc,
                label=label,
                color=color,
                linestyle=ls,
                linewidth=1.6,
                alpha=0.9,
            )

    titles = ["4-bit PCM training", "8-bit PCM training", "6-bit PCM training"]
    for ax, title in zip(axes, titles):
        ax.set_xlabel("Epoch")
        ax.set_ylabel("Test accuracy (%)")
        ax.set_title(title, fontweight="bold")
        ax.set_ylim(0, 90)
        ax.grid(axis="y", color=COL["rule"], linewidth=0.55, alpha=0.65, zorder=0)
        ax.grid(axis="x", color=COL["rule"], linewidth=0.55, alpha=0.65, zorder=0)
        ax.tick_params(length=3, width=0.7, color=COL["ink"], labelcolor=COL["ink"])
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.legend(
            loc="lower right",
            frameon=True,
            fancybox=False,
            edgecolor=COL["rule"],
            facecolor="white",
            framealpha=0.95,
        )

    plt.tight_layout()
    fig.savefig(FIG_DIR / "r11d_training_curves_overlay.pdf", dpi=300, bbox_inches="tight")
    fig.savefig(FIG_DIR / "r11d_training_curves_overlay.png", dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("Saved training curves overlay.")


if __name__ == "__main__":
    fig_drift_comparison()
    fig_precision_drift_scatter()
    fig_source_fresh_drift_bars()
    fig_training_curves()
    print("All 4 Batch B/C/D figures regenerated with Codex visual standards.")
