#!/usr/bin/env python3
"""Render the CX-K2 structural-limit signature figure."""
from __future__ import annotations

import json
import os
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", "/tmp/mplconfig-cxfig")

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import colors
from scipy.signal import find_peaks
from scipy.stats import gaussian_kde


ROOT = Path(__file__).resolve().parents[2]
FRESH_PATH = ROOT / "report_md/_gpt/json_gpt/cx_k2_fresh_eval.json"
BIMODALITY_PATH = ROOT / "report_md/_gpt/json_gpt/cx_k2_bimodality_test.json"
PNG_PATH = ROOT / "images_gpt/fig_structural_limit_signature.png"
PDF_PATH = ROOT / "images_gpt/fig_structural_limit_signature.pdf"
SUMMARY_PATH = ROOT / "CODEX_CX_FIG_SUMMARY_20260423.md"


def load_payloads() -> tuple[dict, dict]:
    fresh = json.loads(FRESH_PATH.read_text(encoding="utf-8"))
    bimodality = json.loads(BIMODALITY_PATH.read_text(encoding="utf-8"))
    return fresh, bimodality


def format_values(values: np.ndarray) -> str:
    return ", ".join(f"{value:.3f}" for value in values)


def main() -> None:
    fresh, bimodality = load_payloads()
    values = np.asarray(fresh["instance_means"], dtype=float)
    sorted_values = np.sort(values)
    ranks = np.arange(1, len(sorted_values) + 1)

    mean = float(fresh["cross_instance_mean"])
    std = float(fresh["cross_instance_std"])
    band_low = mean - std
    band_high = mean + std
    min_value = float(sorted_values.min())
    max_value = float(sorted_values.max())

    dip_p = float(bimodality["p_value"])
    dip_statistic = float(bimodality["dip_statistic"])

    kde = gaussian_kde(values)
    y_grid = np.linspace(min_value - 5.0, max_value + 5.0, 800)
    density = kde(y_grid)
    peak_indices, _ = find_peaks(density, prominence=float(density.max()) * 0.01)
    peak_locations = y_grid[peak_indices]
    peak_heights = density[peak_indices]

    if len(peak_indices) != 1:
        raise RuntimeError(
            "Default-bandwidth KDE did not validate as unimodal: "
            f"{len(peak_indices)} peaks at {peak_locations.tolist()}"
        )

    sns.set_theme(context="paper", style="whitegrid", font_scale=1.12)
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "axes.titleweight": "bold",
        "axes.labelweight": "bold",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    })

    fig = plt.figure(figsize=(8.6, 5.2), constrained_layout=False)
    grid = fig.add_gridspec(
        1,
        2,
        width_ratios=(4.6, 1.15),
        left=0.09,
        right=0.94,
        bottom=0.16,
        top=0.90,
        wspace=0.05,
    )
    ax = fig.add_subplot(grid[0, 0])
    ax_kde = fig.add_subplot(grid[0, 1], sharey=ax)

    cmap = plt.get_cmap("viridis")
    norm = colors.Normalize(vmin=min_value, vmax=max_value)

    ax.axhspan(band_low, band_high, color="#d62728", alpha=0.12, linewidth=0)
    ax.axhline(mean, color="#d62728", linewidth=2.0, zorder=1)
    ax.scatter(
        ranks,
        sorted_values,
        c=sorted_values,
        cmap=cmap,
        norm=norm,
        s=72,
        edgecolors="white",
        linewidths=0.8,
        zorder=3,
    )

    ax.annotate(
        f"Mean {mean:.2f}%\n+/- {std:.2f}%",
        xy=(30.0, mean),
        xytext=(23.3, mean + 3.8),
        color="#a50f15",
        fontsize=9.5,
        arrowprops={
            "arrowstyle": "-",
            "color": "#a50f15",
            "linewidth": 1.1,
            "shrinkA": 2,
            "shrinkB": 2,
        },
    )
    ax.annotate(
        f"Range {min_value:.2f}%-{max_value:.2f}%",
        xy=(0.03, 0.95),
        xycoords="axes fraction",
        ha="left",
        va="top",
        fontsize=10,
        color="#222222",
        bbox={
            "boxstyle": "round,pad=0.25",
            "facecolor": "white",
            "edgecolor": "#d9d9d9",
            "alpha": 0.92,
        },
    )

    ax.set_xlim(0.25, 30.75)
    ax.set_ylim(min_value - 5.0, max_value + 5.0)
    ax.set_xticks([1, 5, 10, 15, 20, 25, 30])
    ax.set_xlabel("Fresh hardware instance rank")
    ax.set_ylabel("Fresh-instance accuracy (%)")
    ax.set_title("High-Variance Structural Limit Under Severe Non-Ideality", loc="left", pad=12)
    ax.grid(axis="y", color="#e6e6e6", linewidth=0.8)
    ax.grid(axis="x", color="#f2f2f2", linewidth=0.6)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    ax_kde.fill_betweenx(y_grid, 0.0, density, color="#3b528b", alpha=0.24)
    ax_kde.plot(density, y_grid, color="#2c3e73", linewidth=2.2)
    ax_kde.axhspan(band_low, band_high, color="#d62728", alpha=0.08, linewidth=0)
    ax_kde.axhline(mean, color="#d62728", linewidth=1.6)
    ax_kde.annotate(
        "Hartigan dip\np=0.98 (unimodal)",
        xy=(float(peak_heights[0]), float(peak_locations[0])),
        xytext=(float(density.max()) * 0.07, max_value - 1.6),
        ha="left",
        va="top",
        fontsize=9.2,
        color="#1f2a44",
        arrowprops={
            "arrowstyle": "->",
            "color": "#1f2a44",
            "linewidth": 1.0,
            "shrinkA": 2,
            "shrinkB": 2,
        },
    )
    ax_kde.set_xlabel("Density")
    ax_kde.tick_params(axis="y", labelleft=False, left=False)
    ax_kde.set_xlim(0.0, float(density.max()) * 1.16)
    ax_kde.set_xticks([0.0, round(float(density.max()) / 2.0, 3), round(float(density.max()), 3)])
    ax_kde.grid(axis="y", color="#efefef", linewidth=0.8)
    ax_kde.grid(axis="x", color="#f3f3f3", linewidth=0.6)
    for spine in ("top", "right", "left"):
        ax_kde.spines[spine].set_visible(False)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    colorbar = fig.colorbar(sm, ax=[ax, ax_kde], location="right", fraction=0.035, pad=0.025)
    colorbar.set_label("Accuracy (%)")
    colorbar.outline.set_linewidth(0.6)

    fig.text(
        0.09,
        0.055,
        f"N=30 fresh instances; default Gaussian KDE bandwidth (Scott factor {kde.factor:.3f}).",
        fontsize=8.5,
        color="#555555",
    )

    PNG_PATH.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(PNG_PATH, dpi=300)
    fig.savefig(PDF_PATH)
    plt.close(fig)

    summary = f"""# CODEX CX Figure Summary 20260423

**Script path:** `scripts/_gpt/plot_structural_limit_signature.py`

**Outputs:**
- `images_gpt/fig_structural_limit_signature.png` (300 dpi)
- `images_gpt/fig_structural_limit_signature.pdf` (vector)

**Library versions:**
- matplotlib `{matplotlib.__version__}`
- seaborn `{sns.__version__}`

**Exact numbers rendered:**
- N = `{len(values)}`
- Mean line = `{mean:.14f}%` rendered as `{mean:.2f}%`
- Standard-deviation band = `+/- {std:.14f}%` rendered as `+/- {std:.2f}%`
- Band bounds = `{band_low:.14f}%` to `{band_high:.14f}%`
- Range annotation = `{min_value:.14f}%` to `{max_value:.14f}%` rendered as `{min_value:.2f}%-{max_value:.2f}%`
- Hartigan dip statistic = `{dip_statistic:.4f}`
- Hartigan dip p-value = `{dip_p:.4f}` rendered as `p=0.98`
- Sorted per-instance means = `{format_values(sorted_values)}`
- KDE method = `scipy.stats.gaussian_kde` default bandwidth (Scott)
- KDE Scott factor = `{kde.factor:.16f}`
- KDE validation peaks = `{len(peak_indices)}` at `{format_values(peak_locations)}%`

**Caption candidate:** CX-K2 fresh-instance evaluation shows a broad high-variance accuracy distribution (38.95 +/- 9.85%, range 22.03%-61.69%) with no statistically supported bimodal attractor (Hartigan dip p=0.98).
"""
    SUMMARY_PATH.write_text(summary, encoding="utf-8")

    print(f"Wrote {PNG_PATH}")
    print(f"Wrote {PDF_PATH}")
    print(f"Wrote {SUMMARY_PATH}")
    print(f"KDE peaks: {len(peak_indices)} at {format_values(peak_locations)}")


if __name__ == "__main__":
    main()
