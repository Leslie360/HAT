#!/usr/bin/env python3
"""Generate vector schematic figures for Fig.1 and Fig.2."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "paper" / "latex_gpt" / "figures"

ANALOG_FILL = "#E0F2F1"
ANALOG_EDGE = "#00695C"
DIGITAL_FILL = "#ECEFF1"
DIGITAL_EDGE = "#455A64"
NEUTRAL_FILL = "#FAFAFA"
NEUTRAL_EDGE = "#616161"
TEXT = "#222222"


def configure_style():
    plt.rcParams.update(
        {
            "figure.dpi": 300,
            "savefig.dpi": 300,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "font.family": "serif",
            "font.serif": ["Times New Roman", "DejaVu Serif"],
            "font.size": 10,
            "axes.linewidth": 0.8,
        }
    )


def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def add_box(ax, x, y, w, h, title, lines, fill, edge, title_size=11, body_size=9.2):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        linewidth=1.3,
        edgecolor=edge,
        facecolor=fill,
    )
    ax.add_patch(patch)
    ax.text(
        x + w / 2,
        y + h - 0.06,
        title,
        ha="center",
        va="top",
        fontsize=title_size,
        fontweight="bold",
        color=TEXT,
    )
    if lines:
        ax.text(
            x + w / 2,
            y + h / 2 - 0.02,
            "\n".join(lines),
            ha="center",
            va="center",
            fontsize=body_size,
            color=TEXT,
            linespacing=1.4,
        )


def add_arrow(ax, x0, y0, x1, y1, color=NEUTRAL_EDGE, style="-|>"):
    arrow = FancyArrowPatch(
        (x0, y0),
        (x1, y1),
        arrowstyle=style,
        mutation_scale=12,
        linewidth=1.2,
        color=color,
    )
    ax.add_patch(arrow)


def draw_fig1(path: Path):
    fig, ax = plt.subplots(figsize=(11.8, 4.6))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    add_box(
        ax,
        0.03,
        0.27,
        0.11,
        0.46,
        "Input image",
        ["edge-vision", "sample"],
        NEUTRAL_FILL,
        NEUTRAL_EDGE,
    )
    add_box(
        ax,
        0.17,
        0.24,
        0.13,
        0.52,
        "Physical frontend",
        ["photoresponse", "inverse-gamma", "compensation"],
        ANALOG_FILL,
        ANALOG_EDGE,
        body_size=8.9,
    )

    backbone = FancyBboxPatch(
        (0.35, 0.14),
        0.34,
        0.72,
        boxstyle="round,pad=0.02,rounding_size=0.02",
        linewidth=1.2,
        edgecolor=NEUTRAL_EDGE,
        facecolor="#FFFFFF",
        linestyle="--",
    )
    ax.add_patch(backbone)
    ax.text(
        0.52,
        0.84,
        "Hybrid backbone",
        ha="center",
        va="center",
        fontsize=11.5,
        fontweight="bold",
        color=TEXT,
    )

    add_box(
        ax,
        0.39,
        0.50,
        0.26,
        0.22,
        "Analog CIM path",
        ["Patch embed", "QKV / out proj.", "MLP fc1 / fc2"],
        ANALOG_FILL,
        ANALOG_EDGE,
        body_size=8.9,
    )
    add_box(
        ax,
        0.39,
        0.21,
        0.26,
        0.22,
        "Digital path",
        ["MBConv / DWConv", "QK^T / AV", "Softmax / LN / head"],
        DIGITAL_FILL,
        DIGITAL_EDGE,
        body_size=8.9,
    )

    add_box(
        ax,
        0.74,
        0.24,
        0.13,
        0.52,
        "Peripheral / calibration",
        ["ADC / DAC", "scale recovery", "profile effects"],
        NEUTRAL_FILL,
        NEUTRAL_EDGE,
        body_size=8.8,
    )
    add_box(
        ax,
        0.90,
        0.28,
        0.11,
        0.44,
        "Output",
        ["Classifier", "Top-1 prediction"],
        NEUTRAL_FILL,
        NEUTRAL_EDGE,
    )

    add_arrow(ax, 0.14, 0.50, 0.17, 0.50)
    add_arrow(ax, 0.30, 0.50, 0.39, 0.61, color=ANALOG_EDGE)
    add_arrow(ax, 0.30, 0.50, 0.39, 0.32, color=DIGITAL_EDGE)
    add_arrow(ax, 0.65, 0.61, 0.74, 0.61, color=ANALOG_EDGE)
    add_arrow(ax, 0.65, 0.32, 0.74, 0.39, color=DIGITAL_EDGE)
    add_arrow(ax, 0.87, 0.50, 0.90, 0.50)

    ax.text(
        0.52,
        0.45,
        "Static dense operators stay in crossbar arrays",
        ha="center",
        va="center",
        fontsize=8.9,
        color=ANALOG_EDGE,
    )
    ax.text(
        0.805,
        0.14,
        "literature / measured profile",
        ha="center",
        va="center",
        fontsize=8.4,
        color=NEUTRAL_EDGE,
    )

    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def draw_fig2(path: Path):
    fig, ax = plt.subplots(figsize=(11.6, 4.3))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    boxes = [
        ("FP32 weights", ["checkpoint tensor $W$"], DIGITAL_FILL, DIGITAL_EDGE),
        ("Branch split", [r"$W^+$ and $W^-$"], DIGITAL_FILL, DIGITAL_EDGE),
        ("Conductance map", [r"$[G_{\min}, G_{\max}]$", r"$n_{\mathrm{states}}$"], ANALOG_FILL, ANALOG_EDGE),
        ("Profile effects", ["D2D / C2C", "retention / NL", "stress laws"], ANALOG_FILL, ANALOG_EDGE),
        ("Readout + scale", [r"$G_{\mathrm{eff}}=G^+ - G^-$", r"$\hat{W}$ after calibration"], NEUTRAL_FILL, NEUTRAL_EDGE),
    ]

    x = 0.03
    w = 0.17
    h = 0.28
    y = 0.48
    centers = []
    for title, lines, fill, edge in boxes:
        add_box(ax, x, y, w, h, title, lines, fill, edge, title_size=10.5, body_size=8.8)
        centers.append((x + w / 2, y + h / 2))
        x += 0.19

    for idx in range(len(centers) - 1):
        add_arrow(ax, centers[idx][0] + 0.085, centers[idx][1], centers[idx + 1][0] - 0.085, centers[idx + 1][1])

    arrow_labels = [
        r"$\max(\pm W,0)$",
        r"normalize \& scale",
        r"forward perturbation",
        r"differential readout",
    ]
    for idx, label in enumerate(arrow_labels):
        x_mid = (centers[idx][0] + centers[idx + 1][0]) / 2
        ax.text(
            x_mid,
            0.39,
            label,
            ha="center",
            va="center",
            fontsize=8.6,
            color=NEUTRAL_EDGE,
        )

    ax.text(
        0.5,
        0.20,
        "Behavioral abstraction used for all simulator experiments",
        ha="center",
        va="center",
        fontsize=9.0,
        color=NEUTRAL_EDGE,
    )
    ax.text(
        0.5,
        0.10,
        "Detailed operator semantics are described in the caption, not embedded in the figure.",
        ha="center",
        va="center",
        fontsize=8.2,
        color=NEUTRAL_EDGE,
    )

    fig.savefig(path, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main():
    configure_style()
    ensure_dir(OUT_DIR)
    draw_fig1(OUT_DIR / "fig1_system_architecture.pdf")
    draw_fig2(OUT_DIR / "fig2_weight_mapping.pdf")
    print(f"Wrote {(OUT_DIR / 'fig1_system_architecture.pdf')}")
    print(f"Wrote {(OUT_DIR / 'fig2_weight_mapping.pdf')}")


if __name__ == "__main__":
    main()
