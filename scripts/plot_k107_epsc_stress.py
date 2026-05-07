"""
Figure 2: EPSC proxy stress.
Reads: deliverable/results_v3/epsc_stress/summary.csv
Output: deliverable/figures/k107_epsc_stress.pdf + .png
"""
import csv
import matplotlib.pyplot as plt
import numpy as np
import os

BASE = "deliverable/results_v3"
OUT_DIR = "deliverable/figures"
os.makedirs(OUT_DIR, exist_ok=True)

rows = []
with open(os.path.join(BASE, "epsc_stress", "summary.csv")) as f:
    reader = csv.DictReader(f)
    for row in reader:
        rows.append(row)

from collections import defaultdict
by_config = defaultdict(list)
for r in rows:
    by_config[r["config"]].append(float(r["ppl"]))

configs = ["EPSC-e1", "EPSC-e2", "EPSC-e3", "EPSC-e4", "EPSC-e5"]
means = [np.mean(by_config[c]) for c in configs]
stds = [np.std(by_config[c], ddof=1) for c in configs]
maxs = [np.max(by_config[c]) for c in configs]
sigmas = ["0.05/0.05", "0.10/0.10", "0.15/0.15", "0.00/0.20", "0.01/0.10"]

x = np.arange(len(configs))
width = 0.35

fig, ax = plt.subplots(figsize=(7, 4.5))
bars = ax.bar(x, means, width, color="#2980b9", edgecolor="white", linewidth=0.5, label="Mean PPL")
ax.errorbar(x, means, yerr=stds, fmt="none", ecolor="black", capsize=3, linewidth=1)

# Overlay max as red diamond
ax.scatter(x, maxs, color="#e74c3c", marker="D", s=40, zorder=5, label="Max PPL")

ax.axhline(y=25, color="gray", linestyle="--", linewidth=1.2, label="Kill threshold (25 PPL)")
ax.set_xticks(x)
ax.set_xticklabels([f"{c}\n({s})" for c, s in zip(configs, sigmas)], fontsize=9)
ax.set_ylabel("Perplexity (PPL)", fontsize=11)
ax.set_title("K107 EPSC Proxy Stress Test\n(Pythia-410M, selective terminal-layer analog KV)", fontsize=12)
ax.set_ylim(0, 28)
ax.legend(loc="upper left", fontsize=8)
ax.text(0.98, 0.02, "Eval: ctx=512, stride=256, bs=1, WikiText-2 test", transform=ax.transAxes,
        fontsize=7, ha="right", va="bottom", style="italic", color="#555555")

fig.tight_layout()
fig.savefig(os.path.join(OUT_DIR, "k107_epsc_stress.pdf"), dpi=300)
fig.savefig(os.path.join(OUT_DIR, "k107_epsc_stress.png"), dpi=200)
print(f"Saved to {OUT_DIR}/k107_epsc_stress.{{pdf,png}}")
