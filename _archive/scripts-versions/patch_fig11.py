import re

with open("paper/plot_paper_figures.py", "r") as f:
    code = f.read()

old_func = re.search(r"def plot_fig11_energy_breakdown.*?def plot_fig12_attention_maps", code, re.DOTALL)
if old_func is None:
    old_func = re.search(r"def plot_fig11_energy_breakdown.*?$", code, re.DOTALL)

new_func = """def plot_fig11_energy_breakdown(output_dir):
    from pathlib import Path
    import matplotlib.pyplot as plt
    import math
    energy = parse_tinyvit_dryrun_energy()
    breakdown = parse_tinyvit_dryrun_breakdown()
    if not energy or not breakdown:
        save_placeholder_figure(
            output_dir / "fig11_energy_breakdown.png",
            "Fig. 11. Energy breakdown",
            "Tiny-ViT dry-run breakdown was not found.\\nExpected source: tinyvit_hybrid_dryrun_report_gpt.md",
        )
        return

    labels = list(breakdown.keys())
    values = [breakdown[key] for key in labels]
    colors = ["#4c78a8", "#f58518", "#e45756", "#72b7b2", "#54a24b", "#b279a2"]
    fp32_total = energy.get("fp32_energy_uJ", math.nan)

    fig, ax = plt.subplots(figsize=(8.0, 4.0))

    left = 0.0
    for label, value, color in zip(labels, values, colors):
        ax.barh(["Hybrid Architecture"], [value], left=left, label=label, color=color)
        left += value
    if not math.isnan(fp32_total):
        ax.barh(["Digital Baseline (GPU)"], [fp32_total], color="#bbbbbb", label="FP32 total reference")

    ax.set_xlabel("Energy per inference (µJ)")
    ax.set_title("Energy Breakdown: Hybrid Architecture vs Digital Baseline")

    handles, legend_labels = ax.get_legend_handles_labels()
    by_label = dict(zip(legend_labels, handles))
    ax.legend(by_label.values(), by_label.keys(), frameon=True, loc="lower right", fontsize=9)

    fig.suptitle("Fig. 11. Energy Comparison")
    fig.savefig(output_dir / "fig11_energy_breakdown.png", bbox_inches="tight")
    plt.close(fig)
"""

if old_func:
    # If there is another function after this
    if "def plot_fig12_attention_maps" in old_func.group(0):
        new_func += "\n\ndef plot_fig12_attention_maps" + old_func.group(0).split("def plot_fig12_attention_maps")[1]
    
    code = code.replace(old_func.group(0), new_func + ("\n" if "def plot_fig12" not in new_func else ""))
    
    with open("paper/plot_paper_figures.py", "w") as f:
        f.write(code)
    print("Patched plot_paper_figures.py")
else:
    print("Could not find function")

