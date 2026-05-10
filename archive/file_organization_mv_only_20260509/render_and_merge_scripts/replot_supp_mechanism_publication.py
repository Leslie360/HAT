#!/usr/bin/env python3
"""Regenerate publication-layout supplementary mechanism figures from JSON.

This script is intentionally plotting-only: it does not import torch and does
not rerun any GPU experiment. It reformats the E1--E5 mechanism diagnostics for
the appendix from archived JSON artifacts.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Patch


ROOT = Path(__file__).resolve().parents[2]
JSON_DIR = ROOT / "report_md/_gpt/json_gpt"
FIG_DIR = ROOT / "paper/latex_gpt/figures"

COL = {
    "ink": "#333333",
    "muted": "#666666",
    "grid": "#E1E6EB",
    "blue": "#2F5D76",
    "teal": "#2A9D8F",
    "coral": "#D07A5D",
    "gold": "#C88A00",
    "violet": "#6D597A",
    "gray": "#AAB4BE",
}

SOFT_TEAL_CMAP = LinearSegmentedColormap.from_list(
    "soft_teal_academic",
    ["#F7FBFC", "#DCEFF0", "#A8D4D0", "#5CA8A3", "#28666E"],
)


def style() -> None:
    plt.style.use("seaborn-v0_8-paper")
    plt.rcParams.update({
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "font.family": "serif",
        "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
        "font.size": 10.8,
        "axes.titlesize": 11.6,
        "axes.titleweight": "bold",
        "axes.labelsize": 10.8,
        "legend.fontsize": 8.9,
        "xtick.labelsize": 9.4,
        "ytick.labelsize": 9.4,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": COL["ink"],
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })


def load_json(name: str) -> dict:
    with (JSON_DIR / name).open("r", encoding="utf-8") as f:
        return json.load(f)


def save(fig: plt.Figure, stem: str) -> None:
    FIG_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG_DIR / f"{stem}.pdf", bbox_inches="tight")
    fig.savefig(FIG_DIR / f"{stem}.png", bbox_inches="tight")
    plt.close(fig)


def grid(ax) -> None:
    ax.grid(axis="y", linestyle=(0, (2, 2)), linewidth=0.55, alpha=0.72, color=COL["grid"])
    ax.set_axisbelow(True)


def plot_d2d() -> None:
    data = load_json("d2d_loss_landscape.json")
    runs = [
        ("canonical_standard", "Standard HAT", COL["coral"], "--", "o"),
        ("canonical_ensemble", "Ensemble HAT", COL["blue"], "-", "o"),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(8.3, 3.45), gridspec_kw={"wspace": 0.28})
    for key, label, color, linestyle, marker in runs:
        rows = data["summary"][key]
        alpha = np.asarray([row["alpha"] for row in rows], dtype=float)
        acc = np.asarray([row["acc_mean"] for row in rows], dtype=float)
        acc_std = np.asarray([row["acc_std"] for row in rows], dtype=float)
        loss = np.asarray([row["loss_mean"] for row in rows], dtype=float)
        axes[0].plot(alpha, acc, linestyle=linestyle, marker=marker, color=color, linewidth=2.0, label=label)
        axes[0].fill_between(alpha, acc - acc_std, acc + acc_std, color=color, alpha=0.14, linewidth=0)
        axes[1].plot(alpha, loss, linestyle=linestyle, marker=marker, color=color, linewidth=2.0, label=label)

    axes[0].set_title("A  Fresh-mask accuracy", loc="left", pad=4)
    axes[0].set_xlabel(r"D2D interpolation $\alpha$")
    axes[0].set_ylabel("Accuracy (%)")
    axes[0].set_ylim(0, 100)
    axes[0].legend(frameon=True, loc="upper right")
    grid(axes[0])

    axes[1].set_title("B  Loss along same path", loc="left", pad=4)
    axes[1].set_xlabel(r"D2D interpolation $\alpha$")
    axes[1].set_ylabel("Test loss")
    axes[1].set_ylim(0, None)
    grid(axes[1])
    fig.tight_layout(pad=0.55)
    save(fig, "figS_d2d_loss_landscape")


def plot_sensitivity() -> None:
    data = load_json("per_layer_d2d_sensitivity.json")
    rows = data["ranked_layers"]
    group_colors = {
        "mlp": COL["coral"],
        "qkv": COL["blue"],
        "proj": COL["teal"],
        "patch_embed": COL["violet"],
        "head": COL["gold"],
        "other": COL["gray"],
    }
    x = np.arange(len(rows))
    drops = np.asarray([row["acc_drop_pp"] for row in rows], dtype=float)
    colors = [group_colors.get(row["group"], COL["gray"]) for row in rows]

    fig, ax = plt.subplots(figsize=(8.2, 3.35))
    ax.axhline(0.0, color=COL["ink"], linewidth=0.8)
    ax.bar(x, drops, color=colors, width=0.78, edgecolor="white", linewidth=0.35)
    ax.set_title("Per-layer D2D sensitivity", loc="left", pad=4)
    ax.set_xlabel("Analog layer rank")
    ax.set_ylabel("Accuracy drop (pp)")
    tick_every = max(1, len(rows) // 10)
    ax.set_xticks(x[::tick_every])
    ax.set_xticklabels([str(i + 1) for i in x[::tick_every]])
    handles = [Patch(facecolor=color, edgecolor="white", label=group) for group, color in group_colors.items()]
    ax.legend(handles=handles, ncol=6, loc="upper right", frameon=True, columnspacing=0.8, handlelength=1.0)
    grid(ax)
    fig.tight_layout(pad=0.55)
    save(fig, "figS_per_layer_sensitivity")


def plot_hessian() -> None:
    summary = load_json("hessian_eigenspectrum_summary.json")
    order = ["canonical_ensemble", "canonical_standard", "cx_m1", "cx_m2", "cx_m3"]
    labels = {
        "canonical_ensemble": "Ensemble NL=1",
        "canonical_standard": "Standard NL=1",
        "cx_m1": "M1 Standard",
        "cx_m2": "M2 Ensemble",
        "cx_m3": "M3 Proportional",
    }
    colors = {
        "canonical_ensemble": COL["blue"],
        "canonical_standard": COL["coral"],
        "cx_m1": COL["gold"],
        "cx_m2": COL["teal"],
        "cx_m3": COL["violet"],
    }
    fig, ax = plt.subplots(figsize=(7.0, 4.0))
    for key in order:
        info = summary["results"].get(key)
        if not info:
            continue
        data = load_json(Path(info["json"]).name)
        vals = np.abs(np.asarray(data["ritz_eigenvalues"], dtype=float))
        ax.plot(np.arange(1, len(vals) + 1), vals, marker="o", markersize=2.2, linewidth=1.45, color=colors[key], label=labels[key])
    ax.set_yscale("log")
    ax.set_title("Hessian spectrum approximation", loc="left", pad=4)
    ax.set_xlabel("Ritz eigenvalue index")
    ax.set_ylabel("Absolute eigenvalue")
    ax.legend(frameon=True, loc="lower left")
    ax.grid(which="both", linestyle=(0, (2, 2)), linewidth=0.50, alpha=0.60, color=COL["grid"])
    fig.tight_layout(pad=0.55)
    save(fig, "figS_hessian_spectrum")


def plot_cka() -> None:
    data = load_json("cka_mseries.json")
    matrix = np.asarray(data["aggregate_matrix"], dtype=float)
    labels = ["M1\nStd", "M2\nEns", "M3\nProp", "M4\nProp", "M5\nStd", "M6\nEns"]
    fig, ax = plt.subplots(figsize=(5.65, 4.9))
    im = ax.imshow(matrix, vmin=0.0, vmax=1.0, cmap=SOFT_TEAL_CMAP)
    ax.set_title("M-series representation similarity", loc="left", pad=4)
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            color = "white" if matrix[i, j] > 0.62 else COL["ink"]
            ax.text(j, i, f"{matrix[i, j]:.2f}", ha="center", va="center", color=color, fontsize=8.6)
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.035)
    cbar.set_label("Linear CKA")
    fig.tight_layout(pad=0.50)
    save(fig, "figS_cka_mseries")


def plot_checkpoint_avg() -> None:
    data = load_json("checkpoint_average_eval.json")
    refs = data["references"]
    labels = ["Std\n123", "Std\n456", "Avg\n123/456", "Ensemble\nref"]
    values = [
        refs.get("cx_m1_fresh_mean"),
        refs.get("cx_m5_fresh_mean"),
        data["checkpoint_average"]["cross_instance_mean"],
        refs.get("canonical_ensemble_fresh_mean"),
    ]
    stds = [
        refs.get("cx_m1_fresh_std", 0.0),
        refs.get("cx_m5_fresh_std", 0.0),
        data["checkpoint_average"].get("cross_instance_std", 0.0),
        refs.get("canonical_ensemble_fresh_std", 0.0),
    ]
    colors = [COL["coral"], COL["coral"], COL["gold"], COL["blue"]]
    fig, ax = plt.subplots(figsize=(5.95, 3.35))
    x = np.arange(len(labels))
    ax.bar(
        x,
        values,
        width=0.40,
        yerr=stds,
        color=colors,
        alpha=0.88,
        edgecolor="white",
        linewidth=0.8,
        error_kw={"elinewidth": 0.85, "ecolor": "#555555", "capsize": 0.0},
    )
    for xpos, val in zip(x, values):
        ax.text(xpos, val + 1.5, f"{val:.1f}", ha="center", va="bottom", fontsize=8.9)
    ax.set_title("Checkpoint averaging probe", loc="left", pad=4)
    ax.set_ylabel("Fresh-instance accuracy (%)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, 100)
    grid(ax)
    fig.tight_layout(pad=0.55)
    save(fig, "figS_checkpoint_avg")


def main() -> None:
    style()
    plot_d2d()
    plot_sensitivity()
    plot_hessian()
    plot_cka()
    plot_checkpoint_avg()


if __name__ == "__main__":
    main()
