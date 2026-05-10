import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Add the paper directory to sys.path so we can import from plot_paper_figures
sys.path.append('/home/qiaosir/projects/compute_vit/paper')

# Import everything needed from plot_paper_figures
from plot_paper_figures import (
    load_json, REPORT_DIR, COL, nature_compliant, save_figure_pair,
    enable_major_y_grid, load_convnext_retention, load_tinyvit_retention,
    plot_band_curve, label_pending
)

@nature_compliant
def plot_merged_s10_s11(output_dir: Path):
    # Set up 1x2 subplots
    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.5))

    # ---------------------------------------------------------
    # LEFT SUBPLOT: Retention decay (S10)
    # ---------------------------------------------------------
    ax = axes[0]
    convnext_rows = load_convnext_retention()
    tinyvit_rows = load_tinyvit_retention()

    palette_ret = {
        "ConvNeXt C9": "#2E5B88",
        "Tiny-ViT V4": "#3A8231",
    }
    tick_positions = [0.3, 1, 10, 100, 1000, 10000]
    tick_labels = ["0", "1", "10", "100", "1000", "10000"]

    if convnext_rows:
        convnext_rows = sorted(convnext_rows, key=lambda row: row["time_s"])
        x_vals = [0.3 if row["time_s"] == 0 else row["time_s"] for row in convnext_rows]
        y_vals = [row.get("mean_acc", row.get("test_acc_mean")) for row in convnext_rows]
        y_errs = [row.get("std_acc", row.get("test_acc_std", 0.0)) for row in convnext_rows]
        plot_band_curve(
            ax, x_vals, y_vals, y_errs,
            color=palette_ret["ConvNeXt C9"], marker="o", label="ConvNeXt C9"
        )
        ax.annotate(f"{y_vals[-1]:.1f}%", (x_vals[-1], y_vals[-1]), xytext=(8, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=9, color=palette_ret["ConvNeXt C9"])
    if tinyvit_rows:
        tinyvit_rows = sorted(tinyvit_rows, key=lambda row: row["time_s"])
        x_vals = [0.3 if row["time_s"] == 0 else row["time_s"] for row in tinyvit_rows]
        y_vals = [row.get("mean_acc", row.get("test_acc_mean")) for row in tinyvit_rows]
        y_errs = [row.get("std_acc", row.get("test_acc_std", 0.0)) for row in tinyvit_rows]
        plot_band_curve(
            ax, x_vals, y_vals, y_errs,
            color=palette_ret["Tiny-ViT V4"], marker="s", label="Tiny-ViT V4"
        )
        ax.annotate(f"{y_vals[-1]:.1f}%", (x_vals[-1], y_vals[-1]), xytext=(8, 0), textcoords="offset points",
                    ha="left", va="center", fontsize=9, color=palette_ret["Tiny-ViT V4"])

    ax.set_xscale("log")
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels)
    ax.set_xlabel("Time since programming (s)")
    ax.set_ylabel("Accuracy (%)")
    ax.set_ylim(0, 100)
    ax.set_title("Retention decay under programmed weight drift", loc="center", pad=10)
    ax.legend(frameon=True, loc="lower right")
    enable_major_y_grid(ax)
    ax.axvspan(0.3, 10, color="#cccccc", alpha=0.08, zorder=0)
    ax.text(0.52, 0.08, "rapid initial decay", transform=ax.transAxes, fontsize=9, color="#666666")

    # ---------------------------------------------------------
    # RIGHT SUBPLOT: Analytical SNR (S11/S12)
    # ---------------------------------------------------------
    ax = axes[1]
    data = load_json(REPORT_DIR / "json" / "a23_experiment_results.json")
    gamma_values = data["group2"]["gamma_values"]
    x_min, x_max = data["group2"]["x_range"]
    x = np.logspace(np.log10(max(x_min, 1e-3)), np.log10(x_max), 400)

    palette_snr = [COL["blue"], COL["green"], COL["orange"], COL["gold"]]
    for idx, gamma in enumerate(gamma_values):
        p_in = np.power(x, 1.0 / gamma)
        snr = x / np.sqrt(np.maximum(p_in, 1e-12))
        ax.plot(x, snr, linewidth=2.1, color=palette_snr[idx % len(palette_snr)], label=rf"$\gamma={gamma}$")

    ax.set_xscale("log")
    ax.set_xlabel("Normalized pixel intensity")
    ax.set_ylabel("Normalized SNR (a.u.)")
    ax.set_title("SNR under inverse-gamma compensation", loc="center", pad=10)
    ax.legend(
        ncol=1, # Change to 1 column for better fit in side-by-side
        frameon=True,
        loc="upper left",
        fontsize=9
    )
    enable_major_y_grid(ax)

    # ---------------------------------------------------------
    # Save the merged figure
    # ---------------------------------------------------------
    fig.tight_layout(pad=1.5)
    fig.savefig(output_dir / "merged_S10_S11_test.png", bbox_inches="tight", dpi=300)
    plt.close(fig)

if __name__ == "__main__":
    out_dir = Path("/home/qiaosir/projects/compute_vit/tmp/py_figures")
    out_dir.mkdir(parents=True, exist_ok=True)
    plot_merged_s10_s11(out_dir)
    print(f"Saved merged figure to {out_dir / 'merged_S10_S11_test.png'}")
