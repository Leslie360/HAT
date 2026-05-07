"""Aggregate P0-B results into CSV."""
import os, json, csv, glob

OUT_DIR = "/home/lisq753/projects/HAT/HAT/deliverable/results_v3/p0b_ablation"
rows = []

for path in sorted(glob.glob(os.path.join(OUT_DIR, "*.json"))):
    d = json.load(open(path))
    name = os.path.basename(path)
    # Determine mode
    if "digital_noanalog" in name:
        mode = "B1"
    elif d["sigma_c2c"] == 0.0 and d["sigma_d2d"] == 0.0:
        mode = "B2"
    elif d["sigma_c2c"] == 0.0 and d["sigma_d2d"] == 0.02:
        mode = "B3"
    elif d["sigma_c2c"] == 0.0 and d["sigma_d2d"] == 0.05:
        mode = "B4"
    else:
        mode = "unknown"

    ckpt = d["model"].rstrip("/").split("/")[-1]
    train_seed = ckpt.split("seed")[-1] if "seed" in ckpt else ""

    rows.append({
        "checkpoint": ckpt,
        "train_seed": train_seed,
        "mode": mode,
        "analog_patch": not ("digital_noanalog" in name),
        "n_states": d.get("n_states", 256),
        "sigma_c2c": d.get("sigma_c2c", 0),
        "sigma_d2d": d.get("sigma_d2d", 0),
        "eval_d2d_seed": d.get("eval_d2d_seed", ""),
        "ppl": d["ppl"],
        "ctx_len": d.get("ctx_len", 512),
        "stride": d.get("stride", 256),
        "batch_size": d.get("batch_size", 1),
        "git_commit": d.get("git_commit", ""),
        "json_path": name,
    })

csv_path = os.path.join(OUT_DIR, "summary.csv")
with open(csv_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "checkpoint", "train_seed", "mode", "analog_patch", "n_states",
        "sigma_c2c", "sigma_d2d", "eval_d2d_seed", "ppl",
        "ctx_len", "stride", "batch_size", "git_commit", "json_path"
    ])
    writer.writeheader()
    writer.writerows(rows)

print(f"Aggregated {len(rows)} rows -> {csv_path}")
for r in rows:
    print(f"  {r['checkpoint']} {r['mode']} d2d={r['sigma_d2d']} seed={r['eval_d2d_seed']} ppl={r['ppl']:.2f}")
