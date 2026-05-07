"""
Figure 1: Paired ablation ladder.
Reads: deliverable/results_v3/p0b_ablation/summary.csv, baseline_digital_current.json
Output: deliverable/figures/k107_ablation_ladder.pdf + .png
"""
import json
import csv
import matplotlib.pyplot as plt
import numpy as np
import os

BASE = "deliverable/results_v3"
OUT_DIR = "deliverable/figures"
os.makedirs(OUT_DIR, exist_ok=True)

# Load baseline
with open(os.path.join(BASE, "baseline_digital_current.json")) as f:
    baseline = json.load(f)["ppl"]

# Load ablations
rows = []
with open(os.path.join(BASE, "p0b_ablation", "summary.csv")) as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

# Aggregate across train seeds per mode
from collections import defaultdict
mode_ppls = defaultdict(list)
for r in rows:
    mode_ppls[r["mode"]].append(float(r["ppl"]))

b1 = np.mean(mode_ppls["B1"])
b2 = np.mean(mode_ppls["B2"])
b3 = np.mean(mode_ppls["B3"])
b4 = np.mean(mode_ppls["B4"])

labels = ["Digital\nBaseline", "HAT Digital\n(B1)", "Patch No Noise\n(B2)", "D2D=0.02\n(B3)", "D2D=0.05\n(B4)"]
values = [baseline, b1, b2, b3, b4]
colors = ["#2c3e50", "#3498db", "#9b59b6", "#e74c3c", "#c0392b"]

fig, ax = plt.subplots(figsize=(6, 4.5))
bars = ax.bar(labels, values, color=colors, edgecolor="white", linewidth=0.5)
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.15,
            f"{val:.2f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

ax.axhline(y=25, color="gray", linestyle="--", linewidth=1, label="Kill threshold (25 PPL)")
ax.set_ylabel("Perplexity (PPL)", fontsize=11)
ax.set_title("K107 Paired Ablation Ladder\n(selective terminal-layer analog KV, Pythia-410M)", fontsize=12)
ax.set_ylim(0, 28)
ax.legend(loc="upper left", fontsize=8)
ax.text(0.98, 0.02, "Eval: ctx=512, stride=256, bs=1, WikiText-2 test", transform=ax.transAxes,
        fontsize=7, ha="right", va="bottom", style="italic", color="#555555")

fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, "k107_ablation_ladder.pdf"), dpi=300)
fig.savefig(os.path.join(OUT_DIR, "k107_ablation_ladder.png"), dpi=200)
print(f"Saved to {OUT_DIR}/k107_ablation_ladder.{{pdf,png}}")
