"""
Aggregate all K107 deliverable results into canonical freeze package.
Outputs:
  - k107_plot_ready.json
  - k107_canonical_summary.csv
"""
import json
import csv
import glob
import os
from collections import defaultdict

BASE = "/home/lisq753/projects/HAT/HAT/deliverable/results_v3"
OUT_JSON = os.path.join(BASE, "k107_plot_ready.json")
OUT_CSV = os.path.join(BASE, "k107_canonical_summary.csv")


def load_json(path):
    with open(path) as f:
        return json.load(f)


def mean(vals):
    return sum(vals) / len(vals) if vals else None


def stdev(vals):
    if len(vals) < 2:
        return 0.0
    m = mean(vals)
    return (sum((x - m) ** 2 for x in vals) / (len(vals) - 1)) ** 0.5


# ------------------------------------------------------------------
# 1. Baseline
# ------------------------------------------------------------------
baseline = load_json(os.path.join(BASE, "baseline_digital_current.json"))

# ------------------------------------------------------------------
# 2. P0B Ablations (paired B1/B2/B3/B4)
# ------------------------------------------------------------------
ablations = defaultdict(lambda: {"B1": [], "B2": [], "B3": [], "B4": []})
with open(os.path.join(BASE, "p0b_ablation", "summary.csv")) as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (row["checkpoint"], row["train_seed"])
        ablations[key][row["mode"]].append(float(row["ppl"]))

ablation_summary = []
for (ckpt, ts), modes in ablations.items():
    ablation_summary.append({
        "checkpoint": ckpt,
        "train_seed": int(ts),
        "B1_digital_mean": mean(modes["B1"]),
        "B2_patch_no_noise_mean": mean(modes["B2"]),
        "B3_d2d002_mean": mean(modes["B3"]),
        "B4_d2d005_mean": mean(modes["B4"]),
        "hat_gain_vs_digital": mean(modes["B2"]) - mean(modes["B1"]) if modes["B1"] and modes["B2"] else None,
        "noise_overhead_d2d002": mean(modes["B3"]) - mean(modes["B2"]) if modes["B2"] and modes["B3"] else None,
        "noise_overhead_d2d005": mean(modes["B4"]) - mean(modes["B2"]) if modes["B2"] and modes["B4"] else None,
    })

# ------------------------------------------------------------------
# 3. EPSC Stress
# ------------------------------------------------------------------
epsc = defaultdict(list)
with open(os.path.join(BASE, "epsc_stress", "summary.csv")) as f:
    reader = csv.DictReader(f)
    for row in reader:
        key = (row["config"], row["sigma_c2c"], row["sigma_d2d"])
        epsc[key].append(float(row["ppl"]))

epsc_summary = []
for (config, sc, sd), ppls in sorted(epsc.items()):
    epsc_summary.append({
        "config": config,
        "sigma_c2c": float(sc),
        "sigma_d2d": float(sd),
        "ppl_mean": mean(ppls),
        "ppl_std": stdev(ppls),
        "n": len(ppls),
    })

# ------------------------------------------------------------------
# 4. K107_A — layer scope + D2D sweep
# ------------------------------------------------------------------
k107_a = defaultdict(lambda: defaultdict(list))
with open(os.path.join(BASE, "k107_a", "summary.csv")) as f:
    reader = csv.DictReader(f)
    for row in reader:
        scope = "last1" if "last1" in row["file"] else ("last2" if "last2" in row["file"] else "all")
        d2d = row["sigma_d2d"]
        k107_a[scope][d2d].append(float(row["ppl"]))

k107_a_summary = []
for scope in ["last1", "last2", "all"]:
    for d2d in ["0.02", "0.04", "0.05"]:
        ppls = k107_a[scope].get(d2d, [])
        if ppls:
            k107_a_summary.append({
                "scope": scope,
                "sigma_d2d": float(d2d),
                "ppl_mean": mean(ppls),
                "ppl_std": stdev(ppls),
                "n": len(ppls),
            })

# ------------------------------------------------------------------
# 5. K107_B — Retention sweep
# ------------------------------------------------------------------
k107_b = defaultdict(list)
with open(os.path.join(BASE, "k107_b", "summary.csv")) as f:
    reader = csv.DictReader(f)
    for row in reader:
        if row["file"] == "eval_digital_baseline_seed42.json":
            continue
        scope = "last1" if "last1" in row["file"] else ("all" if "all" in row["file"] else "unknown")
        rst = row["retention_step_time"]
        d2d = row["sigma_d2d"]
        k107_b[(scope, d2d, rst)].append(float(row["ppl"]))

k107_b_summary = []
for (scope, d2d, rst), ppls in sorted(k107_b.items(), key=lambda x: (x[0][0], float(x[0][1]), float(x[0][2]))):
    k107_b_summary.append({
        "scope": scope,
        "sigma_d2d": float(d2d),
        "retention_step_time": float(rst),
        "ppl_mean": mean(ppls),
        "ppl_std": stdev(ppls),
        "n": len(ppls),
    })

# ------------------------------------------------------------------
# 6. K107_C — n_states sweep
# ------------------------------------------------------------------
k107_c = defaultdict(list)
with open(os.path.join(BASE, "k107_c", "summary.csv")) as f:
    reader = csv.DictReader(f)
    for row in reader:
        if "k107_c" in row["file"]:
            ns = int(row["n_states"])
        else:
            ns = 256
        d2d = row["sigma_d2d"]
        k107_c[(ns, d2d)].append(float(row["ppl"]))

k107_c_summary = []
for (ns, d2d), ppls in sorted(k107_c.items(), key=lambda x: (x[0][0], float(x[0][1]))):
    k107_c_summary.append({
        "n_states": ns,
        "sigma_d2d": float(d2d),
        "ppl_mean": mean(ppls),
        "ppl_std": stdev(ppls),
        "n": len(ppls),
    })

# ------------------------------------------------------------------
# 7. Layer-wise
# ------------------------------------------------------------------
layer_wise = load_json(os.path.join(BASE, "layer_wise", "layer_wise_ppl.json"))

# ------------------------------------------------------------------
# 8. Pythia-1B scale check
# ------------------------------------------------------------------
p1b = defaultdict(lambda: defaultdict(list))
for path in glob.glob(os.path.join(BASE, "p1b_1b", "*.json")):
    data = load_json(path)
    fn = os.path.basename(path)
    train_tag = "seed42" if "seed42" in fn else "seed123"
    d2d = data.get("sigma_d2d", 0.0)
    p1b[train_tag][str(d2d)].append(data["ppl"])

p1b_summary = []
for train_tag in ["seed42", "seed123"]:
    for d2d in ["0.02", "0.05"]:
        ppls = p1b[train_tag].get(d2d, [])
        if ppls:
            p1b_summary.append({
                "model": "pythia-1b",
                "train_tag": train_tag,
                "sigma_d2d": float(d2d),
                "ppl_mean": mean(ppls),
                "ppl_std": stdev(ppls),
                "n": len(ppls),
            })

# ------------------------------------------------------------------
# 9. Pythia-2.8B scale check
# ------------------------------------------------------------------
p2d8b = defaultdict(lambda: defaultdict(list))
for path in glob.glob(os.path.join(BASE, "p2d8b_2d8b", "*.json")):
    data = load_json(path)
    fn = os.path.basename(path)
    train_tag = "seed42" if "seed42" in fn else "seed123"
    d2d = data.get("sigma_d2d", 0.0)
    p2d8b[train_tag][str(d2d)].append(data["ppl"])

p2d8b_summary = []
for train_tag in ["seed42", "seed123"]:
    for d2d in ["0.02", "0.05"]:
        ppls = p2d8b[train_tag].get(d2d, [])
        if ppls:
            p2d8b_summary.append({
                "model": "pythia-2.8b",
                "train_tag": train_tag,
                "sigma_d2d": float(d2d),
                "ppl_mean": mean(ppls),
                "ppl_std": stdev(ppls),
                "n": len(ppls),
            })

# ------------------------------------------------------------------
# 10. Pythia-2.8B EPSC + C2C sweep (partial)
# ------------------------------------------------------------------
p2d8b_epsc = defaultdict(list)
p2d8b_c2c = defaultdict(list)
for path in glob.glob(os.path.join(BASE, "p2d8b_epsc_c2c", "*.json")):
    data = load_json(path)
    fn = os.path.basename(path)
    c2c = data.get("sigma_c2c", 0.0)
    d2d = data.get("sigma_d2d", 0.0)
    if d2d >= 0.09:  # EPSC jobs have c2c == d2d >= 0.1
        tag = f"epsc-e{d2d*10:.0f}"
        p2d8b_epsc[tag].append(data["ppl"])
    else:
        p2d8b_c2c[str(c2c)].append(data["ppl"])

p2d8b_epsc_summary = [{"config": k, "ppl_mean": mean(v), "ppl_std": stdev(v), "n": len(v)} for k, v in sorted(p2d8b_epsc.items())]
p2d8b_c2c_summary = [{"sigma_c2c": float(k), "ppl_mean": mean(v), "ppl_std": stdev(v), "n": len(v)} for k, v in sorted(p2d8b_c2c.items(), key=lambda x: float(x[0]))]

# ==================================================================
# Write JSON
# ==================================================================
plot_ready = {
    "meta": {
        "baseline_ppl": baseline["ppl"],
        "baseline_ctx_len": baseline["ctx_len"],
        "baseline_stride": baseline["stride"],
        "baseline_batch_size": baseline["batch_size"],
        "model": "EleutherAI/pythia-410m-deduped",
        "freeze_date": "2026-05-08",
        "note": "Canonical eval settings: ctx=512, stride=256, bs=1, dataset=wikitext-2-raw-v1 test",
    },
    "ablations": ablation_summary,
    "epsc_stress": epsc_summary,
    "k107_a_scope_d2d": k107_a_summary,
    "k107_b_retention": k107_b_summary,
    "k107_c_n_states": k107_c_summary,
    "layer_wise": layer_wise,
    "scale_p1b": p1b_summary,
    "scale_p2d8b": p2d8b_summary,
    "scale_p2d8b_epsc": p2d8b_epsc_summary,
    "scale_p2d8b_c2c": p2d8b_c2c_summary,
}

with open(OUT_JSON, "w") as f:
    json.dump(plot_ready, f, indent=2)

# ==================================================================
# Write flat CSV
# ==================================================================
rows = []
# baseline
rows.append({
    "experiment": "baseline",
    "group": "digital",
    "model": "pythia-410m",
    "ppl_mean": baseline["ppl"],
    "ppl_std": 0.0,
    "n": 1,
    "params": json.dumps({"ctx_len": 512, "stride": 256, "bs": 1}),
})

for item in ablation_summary:
    rows.append({
        "experiment": "ablation",
        "group": item["checkpoint"],
        "model": "pythia-410m",
        "ppl_mean": item["B3_d2d002_mean"],
        "ppl_std": 0.0,
        "n": 3,
        "params": json.dumps({"train_seed": item["train_seed"], "mode": "B3"}),
    })

for item in epsc_summary:
    rows.append({
        "experiment": "epsc_stress",
        "group": item["config"],
        "model": "pythia-410m",
        "ppl_mean": item["ppl_mean"],
        "ppl_std": item["ppl_std"],
        "n": item["n"],
        "params": json.dumps({"sigma_c2c": item["sigma_c2c"], "sigma_d2d": item["sigma_d2d"]}),
    })

for item in k107_a_summary:
    rows.append({
        "experiment": "k107_a_scope",
        "group": item["scope"],
        "model": "pythia-410m",
        "ppl_mean": item["ppl_mean"],
        "ppl_std": item["ppl_std"],
        "n": item["n"],
        "params": json.dumps({"sigma_d2d": item["sigma_d2d"]}),
    })

for item in k107_b_summary:
    rows.append({
        "experiment": "k107_b_retention",
        "group": item["scope"],
        "model": "pythia-410m",
        "ppl_mean": item["ppl_mean"],
        "ppl_std": item["ppl_std"],
        "n": item["n"],
        "params": json.dumps({"sigma_d2d": item["sigma_d2d"], "retention_step_time": item["retention_step_time"]}),
    })

for item in k107_c_summary:
    rows.append({
        "experiment": "k107_c_n_states",
        "group": f"n_states={item['n_states']}",
        "model": "pythia-410m",
        "ppl_mean": item["ppl_mean"],
        "ppl_std": item["ppl_std"],
        "n": item["n"],
        "params": json.dumps({"n_states": item["n_states"], "sigma_d2d": item["sigma_d2d"]}),
    })

for item in p1b_summary:
    rows.append({
        "experiment": "scale_p1b",
        "group": item["train_tag"],
        "model": "pythia-1b",
        "ppl_mean": item["ppl_mean"],
        "ppl_std": item["ppl_std"],
        "n": item["n"],
        "params": json.dumps({"sigma_d2d": item["sigma_d2d"]}),
    })

for item in p2d8b_summary:
    rows.append({
        "experiment": "scale_p2d8b",
        "group": item["train_tag"],
        "model": "pythia-2.8b",
        "ppl_mean": item["ppl_mean"],
        "ppl_std": item["ppl_std"],
        "n": item["n"],
        "params": json.dumps({"sigma_d2d": item["sigma_d2d"]}),
    })

for item in p2d8b_epsc_summary:
    rows.append({
        "experiment": "scale_p2d8b_epsc",
        "group": item["config"],
        "model": "pythia-2.8b",
        "ppl_mean": item["ppl_mean"],
        "ppl_std": item["ppl_std"],
        "n": item["n"],
        "params": json.dumps({}),
    })

for item in p2d8b_c2c_summary:
    rows.append({
        "experiment": "scale_p2d8b_c2c",
        "group": f"c2c={item['sigma_c2c']}",
        "model": "pythia-2.8b",
        "ppl_mean": item["ppl_mean"],
        "ppl_std": item["ppl_std"],
        "n": item["n"],
        "params": json.dumps({"sigma_c2c": item["sigma_c2c"]}),
    })

with open(OUT_CSV, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["experiment", "group", "model", "ppl_mean", "ppl_std", "n", "params"])
    writer.writeheader()
    writer.writerows(rows)

print(f"Wrote {OUT_JSON}")
print(f"Wrote {OUT_CSV}")
print(f"Rows: {len(rows)}")
