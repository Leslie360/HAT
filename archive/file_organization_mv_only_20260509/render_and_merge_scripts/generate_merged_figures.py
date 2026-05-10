#!/usr/bin/env python3
"""Generate the merged multi-panel figures for Paper-1."""

import json
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
from matplotlib.lines import Line2D
import matplotlib.gridspec as gridspec

ROOT = Path(__file__).resolve().parents[2]
FIG_DIR = ROOT / "paper" / "latex_gpt" / "figures"
SRC_DIR = ROOT / "paper" / "latex_gpt" / "source_data"
JSON_DIR = ROOT / "report_md" / "_gpt" / "json_gpt"

NATURE_TEAL = "#2A9D8F"
NATURE_CORAL = "#E76F51"
NATURE_GOLD = "#E9C46A"
NATURE_NAVY = "#264653"
GRAY_DARK = "#333333"
GRAY_LIGHT = "#AAAAAA"
COL = {
    "ink": GRAY_DARK,
    "muted": "#666666",
    "grid": "#E1E6EB",
    "blue": NATURE_NAVY,
    "red": NATURE_CORAL,
    "green": NATURE_TEAL,
    "gold": NATURE_GOLD,
    "gray": GRAY_LIGHT,
}

plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Times", "DejaVu Serif"],
    "font.size": 9.5,
    "axes.labelsize": 10,
    "axes.titlesize": 10.5,
    "axes.titleweight": "bold",
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "axes.linewidth": 0.8,
    "axes.edgecolor": GRAY_DARK,
    "xtick.color": GRAY_DARK,
    "ytick.color": GRAY_DARK,
    "pdf.fonttype": 42,
    "ps.fonttype": 42,
})

def format_panel(ax, title):
    ax.set_title(title, loc="left", fontweight="bold", pad=12)
    ax.spines[["top", "right"]].set_visible(False)

# ==============================================================================
# FIGURE 1: Algorithmic Failure and Rescue
# ==============================================================================
fig1 = plt.figure(figsize=(10.5, 3.25))
fig1.patch.set_facecolor("white")
gs1 = gridspec.GridSpec(1, 3, width_ratios=[1.1, 0.9, 1.2], wspace=0.35)

# --- Panel A: Schematic ---
ax1a = fig1.add_subplot(gs1[0])
ax1a.set_axis_off()
ax1a.set_xlim(0, 1)
ax1a.set_ylim(0, 1)
format_panel(ax1a, "A. Standard vs. Ensemble HAT")

def draw_box(ax, x, y, w, h, text, color, fill):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.03",
                                linewidth=1.2, facecolor=fill, edgecolor=color))
    ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=9, fontweight="bold", color=color)

def draw_arrow(ax, x0, y0, x1, y1):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>,head_width=4,head_length=6",
                                 linewidth=1.2, color=COL["muted"]))

# Standard HAT
draw_box(ax1a, 0.05, 0.70, 0.35, 0.2, "Standard HAT\n(Fixed Mask)", COL["red"], "#FDF3F0")
draw_arrow(ax1a, 0.42, 0.80, 0.58, 0.80)
draw_box(ax1a, 0.60, 0.70, 0.35, 0.2, "Fresh Instance\nCollapse", COL["red"], "white")

# Ensemble HAT
draw_box(ax1a, 0.05, 0.20, 0.35, 0.2, "Ensemble HAT\n(Resampled)", COL["green"], "#EDF7F6")
draw_arrow(ax1a, 0.42, 0.30, 0.58, 0.30)
draw_box(ax1a, 0.60, 0.20, 0.35, 0.2, "Robust Transfer\nRecovery", COL["green"], "white")

# --- Panel B: Bar Chart ---
ax1b = fig1.add_subplot(gs1[1])
labels_a = ["IdealDevice\n8-bit", "IdealDevice\n4-bit", "Ensemble HAT\n4-bit"]
means_a = [87.28, 14.64, 86.16]
stds_a = [0.13, 0.11, 0.19]
colors_a = [COL["blue"], COL["red"], COL["green"]]

ax1b.bar(np.arange(3), means_a, yerr=stds_a, color=colors_a, width=0.65, alpha=0.9,
         error_kw=dict(ecolor=COL["ink"], lw=1.2, capsize=0))
ax1b.set_ylim(0, 100)
ax1b.set_ylabel("Fresh-Instance Accuracy (%)")
ax1b.set_xticks(np.arange(3))
ax1b.set_xticklabels(labels_a)
ax1b.axhline(10, color=COL["gray"], linestyle="--", linewidth=1.0, zorder=-1)
for idx, value in enumerate(means_a):
    ax1b.text(idx, value + 4.0, f"{value:.1f}%", ha="center", va="bottom", fontsize=8.5, color=COL["ink"], fontweight="bold")
format_panel(ax1b, "B. Pure 4-bit failure and rescue")

# --- Panel C: Loss Landscape ---
ax1c = fig1.add_subplot(gs1[2])
landscape_data = json.load(open(JSON_DIR / "d2d_loss_landscape.json"))["summary"]
alphas = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
std_acc = [d["acc_mean"] for d in landscape_data["canonical_standard"]]
std_err = [d["acc_std"] for d in landscape_data["canonical_standard"]]
ens_acc = [d["acc_mean"] for d in landscape_data["canonical_ensemble"]]
ens_err = [d["acc_std"] for d in landscape_data["canonical_ensemble"]]

ax1c.plot(alphas, std_acc, marker="o", color=COL["red"], label="Standard HAT", linewidth=1.5, markersize=5)
ax1c.fill_between(alphas, np.array(std_acc)-np.array(std_err), np.array(std_acc)+np.array(std_err), color=COL["red"], alpha=0.15, edgecolor="none")
ax1c.plot(alphas, ens_acc, marker="s", color=COL["green"], label="Ensemble HAT", linewidth=1.5, markersize=5)
ax1c.fill_between(alphas, np.array(ens_acc)-np.array(ens_err), np.array(ens_acc)+np.array(ens_err), color=COL["green"], alpha=0.15, edgecolor="none")

ax1c.set_ylim(0, 100)
ax1c.set_xlabel(r"Interpolation $\alpha$ (0=Source, 1=Fresh)")
ax1c.set_ylabel("Accuracy (%)")
ax1c.axvline(1.0, color=COL["gray"], linestyle=":", linewidth=1.0, zorder=0)
ax1c.legend(frameon=False, fontsize=8.5)
ax1c.grid(True, linestyle=":", alpha=0.4, zorder=0)
format_panel(ax1c, "C. D2D-direction loss landscape")

fig1.savefig(FIG_DIR / "fig1_algorithmic_rescue.pdf", bbox_inches="tight", dpi=300)
fig1.savefig(FIG_DIR / "fig1_algorithmic_rescue.png", bbox_inches="tight", dpi=300)

# ==============================================================================
# FIGURE 2: Physical Constraints and Frontiers
# ==============================================================================
fig2 = plt.figure(figsize=(10.5, 3.25))
fig2.patch.set_facecolor("white")
gs2 = gridspec.GridSpec(1, 3, width_ratios=[1.1, 0.95, 0.95], wspace=0.35)

# --- Panel A: Iso-accuracy Contour Map ---
ax2a = fig2.add_subplot(gs2[0])
import matplotlib.colors as mcolors
contour_data = json.load(open(JSON_DIR / "iso_accuracy_contour_data.json"))
# Reconstruct grid
d2d_vals = sorted(list(set(r["d2d_pct"] for r in contour_data)))
adc_vals = sorted(list(set(r["adc_bits"] for r in contour_data)))
grid = np.full((len(d2d_vals), len(adc_vals)), np.nan)
for r in contour_data:
    i = d2d_vals.index(r["d2d_pct"])
    j = adc_vals.index(r["adc_bits"])
    grid[i, j] = r["mean"]

cmap = plt.get_cmap("cividis")
norm = mcolors.Normalize(vmin=10.0, vmax=90.0)
im = ax2a.imshow(grid, cmap=cmap, norm=norm, aspect="auto", origin="lower")
contour_levels = [80.0, 85.0, 88.0]
contour_styles = [(0, (4.0, 2.0)), (0, (2.2, 1.4)), "solid"]
ax2a.contour(np.arange(len(adc_vals)), np.arange(len(d2d_vals)), grid, levels=contour_levels, colors="#202020", linewidths=0.9, linestyles=contour_styles)

for i in range(len(d2d_vals)):
    for j in range(len(adc_vals)):
        v = grid[i, j]
        if not np.isnan(v):
            lum = 0.2126*cmap(norm(v))[0] + 0.7152*cmap(norm(v))[1] + 0.0722*cmap(norm(v))[2]
            tc = "white" if lum < 0.48 else "#111111"
            ax2a.text(j, i, f"{v:.1f}", ha="center", va="center", fontsize=7.5, color=tc, fontweight="bold")

ax2a.set_xticks(np.arange(len(adc_vals)))
ax2a.set_xticklabels([str(v) for v in adc_vals])
ax2a.set_yticks(np.arange(len(d2d_vals)))
ax2a.set_yticklabels([f"{v:.0f}" for v in d2d_vals])
ax2a.set_xlabel("ADC Resolution (bits)")
ax2a.set_ylabel(r"$\sigma_{\mathrm{D2D}}$ (%)")
format_panel(ax2a, "A. Operating envelope (ADC vs D2D)")
ax2a.spines[["top", "right"]].set_visible(True) # Heatmaps look better with frames
cbar = fig2.colorbar(im, ax=ax2a, fraction=0.046, pad=0.04)
cbar.set_label("Accuracy (%)", size=9)

# --- Panel B: Retention Decay ---
ax2b = fig2.add_subplot(gs2[1])
# Data from precision ladder (3-seed means)
times = [0, 1, 24] # Categorical hours
acc_8b = [77.60, 77.49, 77.57]
acc_6b = [68.44, 68.46, 68.36]
acc_4b = [76.68, 74.04, 72.64]

ax2b.plot(times, acc_8b, marker="o", color=COL["blue"], label="8-bit PCM", linewidth=1.5)
ax2b.plot(times, acc_6b, marker="s", color=COL["green"], label="6-bit PCM", linewidth=1.5)
ax2b.plot(times, acc_4b, marker="^", color=COL["gold"], label="4-bit PCM", linewidth=1.5)

ax2b.set_ylim(60, 80)
ax2b.set_xticks(times)
ax2b.set_xticklabels(["0s", "1h", "24h"])
ax2b.set_xlabel("Inference Delay")
ax2b.set_ylabel("Accuracy (%)")
ax2b.grid(True, linestyle=":", alpha=0.4)
ax2b.legend(frameon=False, fontsize=8.5)
format_panel(ax2b, "B. Conductance drift impact")

# --- Panel C: Precision-retention regimes ---
ax2c = fig2.add_subplot(gs2[2])
drift_b = [0.04, 0.04, 4.01]
fresh_b = [77.60, 68.44, 76.68]
labels_b = ["8-bit PCM", "6-bit PCM", "4-bit PCM"]
colors_b = [COL["blue"], COL["green"], COL["gold"]]

ax2c.plot(drift_b, fresh_b, color=COL["gray"], linewidth=1.5, linestyle="--", zorder=1)

for i in range(3):
    ax2c.plot(drift_b[i], fresh_b[i], marker='o', color=colors_b[i], markersize=9,
              markeredgecolor='white', markeredgewidth=1.5, zorder=3, label=labels_b[i])

    if i == 1: # 6-bit
        ax2c.annotate("Transition\nZone", xy=(drift_b[i], fresh_b[i]), xytext=(25, -5),
                 textcoords="offset points", ha="left", va="center",
                 fontsize=8.5, color=COL["green"],
                 arrowprops=dict(arrowstyle="->", color=COL["green"], connectionstyle="arc3,rad=-0.2"))

ax2c.set_xlim(-0.5, 4.5)
ax2c.set_ylim(60, 80)
ax2c.set_xlabel("1-Day Drift Drop (pp)")
ax2c.set_ylabel("Fresh Accuracy (%)")
ax2c.grid(True, linestyle=":", alpha=0.4, zorder=0)
ax2c.legend(loc='lower left', frameon=False, fontsize=8.5)
format_panel(ax2c, "C. Precision-retention frontier")

fig2.savefig(FIG_DIR / "fig2_physical_frontier.pdf", bbox_inches="tight", dpi=300)
fig2.savefig(FIG_DIR / "fig2_physical_frontier.png", bbox_inches="tight", dpi=300)

print("Merged Figures 1 and 2 generated successfully.")
