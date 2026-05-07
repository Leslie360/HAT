"""
Figure 3: Scale trend (410M / 1B / 2.8B).
Reads: deliverable/results_v3/p0b_ablation/summary.csv, p1b_1b/*.json, p2d8b_2d8b/*.json
Output: deliverable/figures/k107_scale_trend.pdf + .png
"""
import json
import csv
import glob
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import os

BASE = "deliverable/results_v3"
OUT_DIR = "deliverable/figures"
os.makedirs(OUT_DIR, exist_ok=True)

# 410M from ablation B3
rows = []
with open(os.path.join(BASE, "p0b_ablation", "summary.csv")) as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["mode"] == "B3":
            rows.append(float(row["ppl"]))
p410m_002 = np.mean(rows)
p410m_002_std = np.std(rows, ddof=1)
rows = []
with open(os.path.join(BASE, "p0b_ablation", "summary.csv")) as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["mode"] == "B4":
            rows.append(float(row["ppl"]))
p410m_005 = np.mean(rows)
p410m_005_std = np.std(rows, ddof=1)

# 1B
p1b = defaultdict(list)
for path in glob.glob(os.path.join(BASE, "p1b_1b", "*.json")):
    with open(path) as f:
        data = json.load(f)
    d2d = str(data.get("sigma_d2d", 0.0))
    p1b[d2d].append(data["ppl"])
p1b_002 = np.mean(p1b["0.02"])
p1b_002_std = np.std(p1b["0.02"], ddof=1)
p1b_005 = np.mean(p1b["0.05"])
p1b_005_std = np.std(p1b["0.05"], ddof=1)

# 2.8B
p2d8b = defaultdict(list)
for path in glob.glob(os.path.join(BASE, "p2d8b_2d8b", "*.json")):
    with open(path) as f:
        data = json.load(f)
    d2d = str(data.get("sigma_d2d", 0.0))
    p2d8b[d2d].append(data["ppl"])
p2d8b_002 = np.mean(p2d8b["0.02"])
p2d8b_002_std = np.std(p2d8b["0.02"], ddof=1)
p2d8b_005 = np.mean(p2d8b["0.05"])
p2d8b_005_std = np.std(p2d8b["0.05"], ddof=1)

models = ["Pythia-410M", "Pythia-1B", "Pythia-2.8B"]
x = np.arange(len(models))
width = 0.3

means_002 = [p410m_002, p1b_002, p2d8b_002]
stds_002 = [p410m_002_std, p1b_002_std, p2d8b_002_std]
means_005 = [p410m_005, p1b_005, p2d8b_005]
stds_005 = [p410m_005_std, p1b_005_std, p2d8b_005_std]

fig, ax = plt.subplots(figsize=(6.5, 4.5))
bars1 = ax.bar(x - width/2, means_002, width, color="#27ae60", edgecolor="white", linewidth=0.5, label="D2D=0.02")
bars2 = ax.bar(x + width/2, means_005, width, color="#f39c12", edgecolor="white", linewidth=0.5, label="D2D=0.05")
ax.errorbar(x - width/2, means_002, yerr=stds_002, fmt="none", ecolor="black", capsize=3, linewidth=1)
ax.errorbar(x + width/2, means_005, yerr=stds_005, fmt="none", ecolor="black", capsize=3, linewidth=1)

for bar, val in zip(bars1, means_002):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            f"{val:.2f}", ha="center", va="bottom", fontsize=8, fontweight="bold", color="#1e8449")
for bar, val in zip(bars2, means_005):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            f"{val:.2f}", ha="center", va="bottom", fontsize=8, fontweight="bold", color="#b7950b")

ax.set_xticks(x)
ax.set_xticklabels(models, fontsize=10)
ax.set_ylabel("Perplexity (PPL)", fontsize=11)
ax.set_title("Scale Trend: Selective Terminal-Layer Analog KV\n(last1 config, mean ± std)", fontsize=12)
ax.legend(loc="upper right", fontsize=9)
ax.text(0.98, 0.02, "Eval: ctx=512, stride=256, bs=1, WikiText-2 test", transform=ax.transAxes,
        fontsize=7, ha="right", va="bottom", style="italic", color="#555555")

fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, "k107_scale_trend.pdf"), dpi=300)
fig.savefig(os.path.join(OUT_DIR, "k107_scale_trend.png"), dpi=200)
print(f"Saved to {OUT_DIR}/k107_scale_trend.{{pdf,png}}")
