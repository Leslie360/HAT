import re

with open("paper/plot_paper_figures.py", "r") as f:
    code = f.read()

# 1. Upgrade global style
style_new = """def configure_style():
    plt.style.use("seaborn-v0_8-paper")
    plt.rcParams.update({
        "figure.dpi": 300,
        "savefig.dpi": 300,
        "font.family": "serif",
        "font.serif": ["Times New Roman", "DejaVu Serif"],
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "axes.labelsize": 12,
        "axes.labelweight": "medium",
        "legend.fontsize": 10,
        "legend.frameon": True,
        "legend.edgecolor": "#cccccc",
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 1.0,
        "axes.edgecolor": "#333333",
        "axes.grid": False,
        "grid.linewidth": 0.5,
        "grid.alpha": 0.3,
        "grid.color": "#b0b0b0",
        "figure.autolayout": False,
        "hatch.linewidth": 0.5,
    })
"""
code = re.sub(r"def configure_style\(\):.*?(?=\ndef )", style_new, code, flags=re.DOTALL)

# 2. Add edgecolors to bar charts
code = re.sub(r"ax\.bar\((.*?)color=(.*?)\)", r"ax.bar(\1color=\2, edgecolor='#222222', linewidth=0.8)", code)
code = re.sub(r"axes\[1\]\.bar\((.*?)color=(.*?)\)", r"axes[1].bar(\1color=\2, edgecolor='#222222', linewidth=0.8)", code)
code = re.sub(r"stack_ax\.barh\((.*?)color=(.*?)\)", r"stack_ax.barh(\1color=\2, edgecolor='#222222', linewidth=0.8)", code)
code = re.sub(r"ax\.barh\((.*?)color=(.*?)\)", r"ax.barh(\1color=\2, edgecolor='#222222', linewidth=0.8)", code)

# 3. Upgrade palettes
# Original: colors = {"convnext": "#4C78A8", "tinyvit": "#54A24B"}
code = re.sub(r'"#4C78A8"', r'"#2E5B88"', code) # Deeper blue
code = re.sub(r'"#54A24B"', r'"#3A8231"', code) # Deeper green

# 4. Enhance Fig 11 (Energy breakdown)
# colors = ["#4c78a8", "#f58518", "#e45756", "#72b7b2", "#54a24b", "#b279a2"]
new_colors_fig11 = 'colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]'
code = re.sub(r'colors = \["#4c78a8".*?\]', new_colors_fig11, code)

with open("paper/plot_paper_figures.py", "w") as f:
    f.write(code)
print("Plots upgraded.")
