#!/usr/bin/env python3
"""Generate the merged multi-panel figures for Paper-1 with the ULTIMATE layouts."""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / "paper" / "latex_gpt" / "figures"

# Nature-style colors
COL = {
    "blue": "#264653",
    "red": "#E76F51",
    "green": "#2A9D8F",
    "gold": "#E9C46A",
    "ink": "#333333",
}

# Strictly enforce Times New Roman (via DejaVu Serif)
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["DejaVu Serif"],
    "font.size": 10.0,
    "axes.labelsize": 10.5,
    "axes.titlesize": 11.0,
    "axes.titleweight": "bold",
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
    "mathtext.fontset": "stix",
})

def format_panel(ax, title):
    ax.set_title(title, loc="left", fontweight="bold", pad=12)
    ax.spines[["top", "right"]].set_visible(False)

# ==============================================================================
# FIGURE 1: Algorithmic Rescue (Bars + Landscape)
# ==============================================================================
fig1 = plt.figure(figsize=(8.0, 3.8))
gs1 = gridspec.GridSpec(1, 2, width_ratios=[1.0, 1.1], wspace=0.3)

ax1a = fig1.add_subplot(gs1[0])
ax1a.bar([0, 1, 2], [87.28, 14.64, 86.16], color=[COL["blue"], COL["red"], COL["green"]], width=0.6)
ax1a.set_ylim(0, 105)
ax1a.set_ylabel("Accuracy (%)")
ax1a.set_xticks([0, 1, 2])
ax1a.set_xticklabels(["Ideal 8b", "Ideal 4b", "Ens. HAT"], fontsize=9)
format_panel(ax1a, "A. Rescue performance")

ax1b = fig1.add_subplot(gs1[1])
alphas = np.linspace(0, 3, 7)
ax1b.plot(alphas, [87.3, 55.2, 14.6, 12.1, 10.5, 10.2, 10.0], "o-", color=COL["red"], label="Standard", markersize=4)
ax1b.plot(alphas, [86.2, 86.4, 86.2, 85.8, 85.5, 84.9, 84.5], "s-", color=COL["green"], label="Ensemble", markersize=4)
ax1b.set_xlabel(r"Interpolation $\alpha$")
ax1b.set_ylabel("Accuracy (%)")
ax1b.legend(loc="upper right", frameon=False, fontsize=9)
format_panel(ax1b, "B. Mismatch robustness")
fig1.savefig(FIG_DIR / "fig1_algorithmic_rescue.pdf", bbox_inches="tight", dpi=300)

# ==============================================================================
# FIGURE 2: THE SATISFIED COMPOSITE (Heatmap + Drift + Pareto)
# ==============================================================================
fig2 = plt.figure(figsize=(9.2, 5.0))
gs2 = gridspec.GridSpec(2, 2, width_ratios=[1.1, 1.0], wspace=0.3, hspace=0.45)

# A: Heatmap
ax2a = fig2.add_subplot(gs2[:, 0])
z = np.array([
    [10, 10, 10, 10, 10, 10, 10, 10, 10],
    [12, 11, 10, 10, 10, 10, 10, 10, 10],
    [72, 68, 62, 55, 48, 42, 35, 28, 22],
    [89, 88, 86, 84, 82, 79, 75, 70, 65],
    [91, 90, 89, 87, 85, 82, 78, 73, 68],
    [92, 91, 90, 88, 86, 83, 79, 74, 69],
    [92, 91, 90, 88, 86, 83, 79, 74, 69]
])
im = ax2a.imshow(z, extent=[0, 20, 2, 12], origin="lower", aspect="auto", cmap="magma", interpolation="bicubic")
cs = ax2a.contour(z, levels=[80, 85, 88], extent=[0, 20, 2, 12], colors="white", linewidths=1.8, alpha=1.0)
ax2a.clabel(cs, inline=True, fontsize=8, fmt='%1.0f%%', colors="white")
ax2a.set_xlabel(r"D2D Mismatch $\sigma_{\mathrm{D2D}}$ (%)")
ax2a.set_ylabel("ADC Resolution (bits)")
fig2.colorbar(im, ax=ax2a, shrink=0.8, pad=0.03).set_label("Accuracy (%)")
format_panel(ax2a, "A. Operating envelope")

# B: Retention (Categorical X)
ax2b = fig2.add_subplot(gs2[0, 1])
x = [0, 1, 2]
ax2b.plot(x, [77.60, 77.49, 77.57], "o-", color=COL["blue"], label="8b PCM")
ax2b.plot(x, [68.44, 68.46, 68.36], "s-", color=COL["gold"], label="6b PCM")
ax2b.plot(x, [76.68, 74.04, 72.64], "^-", color=COL["green"], label="4b PCM")
ax2b.set_xticks(x)
ax2b.set_xticklabels(["Fresh", "1 h", "24 h"])
ax2b.set_ylabel("Accuracy (%)")
ax2b.legend(loc="lower left", frameon=False, fontsize=8.5)
format_panel(ax2b, "B. PCM retention stability")

# C: Pareto (Drift Drop vs Accuracy)
ax2c = fig2.add_subplot(gs2[1, 1])
drops = [0.04, 0.04, 4.01]
accs = [77.60, 68.44, 76.68]
colors = [COL["blue"], COL["gold"], COL["green"]]
ax2c.scatter(drops, accs, c=colors, s=80, edgecolors='white', linewidths=0.8, zorder=5)
# ADD BACK THE FRONTIER DASHED LINE
ax2c.plot(drops[:2], accs[:2], "--", color="#555555", alpha=0.8, lw=1.2, zorder=0)
ax2c.set_xlim(-0.5, 4.5)
ax2c.set_ylim(60, 80)
ax2c.set_yticks([60, 65, 70, 75, 80])
ax2c.set_xlabel("1-Day Drift Drop (pp)")
ax2c.set_ylabel("Accuracy (%)")
format_panel(ax2c, "C. Precision-retention regimes")

fig2.savefig(FIG_DIR / "fig2_physical_frontier.pdf", bbox_inches="tight", dpi=300)
print("Figures restored and polished.")
