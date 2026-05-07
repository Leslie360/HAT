"""Aggregate P1 EPSC results into CSV."""
import os, json, csv, glob

OUT_DIR = "/home/lisq753/projects/HAT/HAT/deliverable/results_v3/epsc_stress"
rows = []

for path in sorted(glob.glob(os.path.join(OUT_DIR, "*.json"))):
    d = json.load(open(path))
    name = os.path.basename(path)
    ckpt = d["model"].rstrip("/").split("/")[-1]
    train_seed = ckpt.split("seed")[-1] if "seed" in ckpt else ""

    # Determine config tag
    c2c, d2d = d["sigma_c2c"], d["sigma_d2d"]
    if c2c == 0.05 and d2d == 0.05:
        tag = "EPSC-e1"
    elif c2c == 0.10 and d2d == 0.10:
        tag = "EPSC-e2"
    elif c2c == 0.15 and d2d == 0.15:
        tag = "EPSC-e3"
    elif c2c == 0.00 and d2d == 0.20:
        tag = "EPSC-e4"
    elif c2c == 0.01 and d2d == 0.10:
        tag = "EPSC-e5"
    else:
        tag = "unknown"

    rows.append({
        "checkpoint": ckpt,
        "train_seed": train_seed,
        "config": tag,
        "sigma_c2c": c2c,
        "sigma_d2d": d2d,
        "eval_d2d_seed": d.get("eval_d2d_seed", ""),
        "ppl": d["ppl"],
        "ctx_len": d.get("ctx_len", 512),
        "stride": d.get("stride", 256),
        "batch_size": d.get("batch_size", 1),
        "json_path": name,
    })

csv_path = os.path.join(OUT_DIR, "summary.csv")
with open(csv_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "checkpoint", "train_seed", "config", "sigma_c2c", "sigma_d2d",
        "eval_d2d_seed", "ppl", "ctx_len", "stride", "batch_size", "json_path"
    ])
    writer.writeheader()
    writer.writerows(rows)

print(f"Aggregated {len(rows)} rows -> {csv_path}")
