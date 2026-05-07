"""
K107-B Retention Stress Launcher

Evaluates last1 and all-layer checkpoints under retention decay,
plus a digital baseline.
"""

import os
import sys
import time
import subprocess

PYTHON = "/home/lisq753/miniconda3/envs/LLM/bin/python"
EVAL_PY = "/home/lisq753/projects/HAT/HAT/p3_hat_eval.py"
OUT_DIR = "/home/lisq753/projects/HAT/HAT/deliverable/results_v3/k107_b"
CKPT_BASE = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints"

os.makedirs(OUT_DIR, exist_ok=True)

# ── Eval jobs ─────────────────────────────────────────────────────────────
# (tag, ckpt_dir, sigma_d2d, retention_step_time, eval_seed)
EVAL_JOBS = []

# K107-B1: last1, D2D=0.02 eval, retention sweep
for rst in [0, 0.1, 1, 10]:
    for es in [42]:
        EVAL_JOBS.append(("k107_b1_last1_d2d002", f"{CKPT_BASE}/k107_a1_last1_seed42", 0.02, rst, es))

# K107-B2: last1, D2D=0.05 eval, retention sweep
for rst in [0, 0.1, 1, 10]:
    for es in [42]:
        EVAL_JOBS.append(("k107_b2_last1_d2d005", f"{CKPT_BASE}/k107_a1_last1_seed42", 0.05, rst, es))

# K107-B4: all-layer, D2D=0.02 eval, retention sweep
for rst in [0, 0.1, 1, 10]:
    for es in [42]:
        EVAL_JOBS.append(("k107_b4_all_d2d002", f"{CKPT_BASE}/k107_a3_all_seed42", 0.02, rst, es))

# K107-B3: digital baseline (no HAT, no noise, no retention)
# Handled separately below


def get_free_gpus(allowed=(0, 1, 2, 3, 4, 5, 6, 7)):
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=index,utilization.gpu,memory.used",
             "--format=csv,noheader,nounits"],
            text=True, timeout=10
        )
    except Exception:
        return []
    free = []
    for line in out.strip().splitlines():
        parts = [p.strip() for p in line.split(",")]
        idx, util, mem = int(parts[0]), int(parts[1]), int(parts[2])
        if idx in allowed and util == 0 and mem < 200:
            free.append(idx)
    return sorted(free)


def launch(cmd, gpu):
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = str(gpu)
    return subprocess.Popen(cmd, env=env)


def run_eval_jobs():
    print(f"[K107-B] Starting {len(EVAL_JOBS)} retention eval jobs...")
    active = {}
    completed = []

    while EVAL_JOBS or active:
        done_gpus = []
        for gpu, (proc, item) in active.items():
            ret = proc.poll()
            if ret is not None:
                tag, ckpt, d2d, rst, es = item
                print(f"  [GPU {gpu}] EVAL DONE: {tag} rst={rst} d2d={d2d} eseed={es} return={ret}")
                completed.append((item, ret))
                done_gpus.append(gpu)
        for g in done_gpus:
            del active[g]

        free_gpus = get_free_gpus()
        for gpu in free_gpus:
            if gpu in active:
                continue
            if not EVAL_JOBS:
                break
            tag, ckpt, d2d, rst, es = EVAL_JOBS.pop(0)
            cmd = [
                PYTHON, EVAL_PY,
                "--checkpoint_dir", ckpt,
                "--n_states", "256",
                "--sigma_d2d", str(d2d),
                "--sigma_c2c", "0.0",
                "--max_length", "512",
                "--output_dir", OUT_DIR,
                "--d2d-seed", str(es),
                "--retention_step_time", str(rst),
            ]
            print(f"  [GPU {gpu}] EVAL START: {tag} rst={rst} d2d={d2d} eseed={es}")
            active[gpu] = (launch(cmd, gpu), (tag, ckpt, d2d, rst, es))

        time.sleep(2)

    print(f"[K107-B] Retention eval complete. {len(completed)} jobs finished.")
    return completed


def run_digital_baseline():
    """K107-B3: digital baseline eval on original pretrained model."""
    import json
    print("[K107-B3] Running digital baseline eval...")
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer
    sys.path.insert(0, '/home/lisq753/projects/HAT/HAT')
    from p3_hat_train import evaluate_ppl

    device = "cuda:0"
    model = AutoModelForCausalLM.from_pretrained("EleutherAI/pythia-410m-deduped", torch_dtype=torch.float32)
    tokenizer = AutoTokenizer.from_pretrained("EleutherAI/pythia-410m-deduped")
    tokenizer.pad_token = tokenizer.eos_token
    model = model.to(device)

    ppl = evaluate_ppl(model, tokenizer, device, max_length=512)
    print(f"Digital baseline PPL: {ppl:.2f}")

    result = {
        "git_commit": None,
        "git_status_short": None,
        "script": "k107_b_launcher.py",
        "command": "digital_baseline",
        "mode": "eval",
        "model": "EleutherAI/pythia-410m-deduped",
        "dataset_train": None,
        "dataset_eval": "wikitext-2-raw-v1 (test)",
        "train_seed": None,
        "train_d2d_seed": None,
        "eval_d2d_seed": None,
        "n_states": None,
        "sigma_c2c": 0.0,
        "sigma_d2d": 0.0,
        "retention_step_time": 0.0,
        "analog_layers": [],
        "ctx_len": 512,
        "stride": 512,
        "max_steps": None,
        "batch_size": 1,
        "ppl": ppl,
        "wall_clock_time": 0.0,
        "gpu_id": "0",
        "gpu_name": "NVIDIA PH402 SKU 200",
    }
    out_file = os.path.join(OUT_DIR, "eval_digital_baseline_seed42.json")
    with open(out_file, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved: {out_file}")


def write_summary():
    import json, csv
    rows = []
    for fname in sorted(os.listdir(OUT_DIR)):
        if not fname.endswith(".json"):
            continue
        with open(os.path.join(OUT_DIR, fname)) as f:
            data = json.load(f)
        rows.append({
            "file": fname,
            "mode": data.get("mode"),
            "model": data.get("model"),
            "analog_layers": ",".join(str(x) for x in data.get("analog_layers", [])),
            "train_seed": data.get("train_seed"),
            "eval_d2d_seed": data.get("eval_d2d_seed"),
            "sigma_d2d": data.get("sigma_d2d"),
            "retention_step_time": data.get("retention_step_time"),
            "ppl": data.get("ppl"),
            "wall_clock_time": data.get("wall_clock_time"),
            "gpu_id": data.get("gpu_id"),
        })
    csv_path = os.path.join(OUT_DIR, "summary.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else [])
        writer.writeheader()
        writer.writerows(rows)
    print(f"[K107-B] Summary written: {csv_path}")


def main():
    eval_completed = run_eval_jobs()
    run_digital_baseline()
    write_summary()
    print("[K107-B] All done.")


if __name__ == "__main__":
    main()
