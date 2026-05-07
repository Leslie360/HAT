"""
K107-A Canonical Selective KV Re-run Launcher

Trains and evaluates 410M models with selective analog KV layers.
Runs on 8 GPUs with queue-based allocation.
"""

import os
import sys
import time
import subprocess
import json
import csv

PYTHON = "/home/lisq753/miniconda3/envs/LLM/bin/python"
TRAIN_PY = "/home/lisq753/projects/HAT/HAT/p3_hat_train.py"
EVAL_PY = "/home/lisq753/projects/HAT/HAT/p3_hat_eval.py"
OUT_DIR = "/home/lisq753/projects/HAT/HAT/deliverable/results_v3/k107_a"
CKPT_BASE = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints"

os.makedirs(OUT_DIR, exist_ok=True)

# ── Training jobs ──────────────────────────────────────────────────────────
# (tag, analog_layers, sigma_d2d, train_seed)
TRAIN_JOBS = [
    # K107-A1: last1
    ("k107_a1_last1", "23", 0.02, 42),
    ("k107_a1_last1", "23", 0.02, 123),
    ("k107_a1_last1", "23", 0.02, 456),
    # K107-A2: last2
    ("k107_a2_last2", "22,23", 0.02, 42),
    ("k107_a2_last2", "22,23", 0.02, 123),
    ("k107_a2_last2", "22,23", 0.02, 456),
    # K107-A3: all layers
    ("k107_a3_all", "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23", 0.02, 42),
]

# ── Evaluation matrix ─────────────────────────────────────────────────────
EVAL_D2D_LEVELS = [0.02, 0.04, 0.05]
EVAL_SEEDS = [42, 123, 456, 789, 1001]


def get_free_gpus(allowed=(0, 1, 2, 3, 4, 5, 6, 7)):
    """Return sorted list of GPUs with 0%% util and <200 MiB used."""
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


def run_train_jobs():
    """Queue all training jobs across available GPUs."""
    remaining = list(TRAIN_JOBS)
    active = {}  # gpu -> (proc, job_tuple)
    completed = []

    print(f"[K107-A] Starting {len(remaining)} training jobs...")
    while remaining or active:
        # Poll active jobs
        done_gpus = []
        for gpu, (proc, job) in active.items():
            ret = proc.poll()
            if ret is not None:
                tag, layers, sd, seed = job
                print(f"  [GPU {gpu}] TRAIN DONE: {tag} seed={seed}  return={ret}")
                completed.append((job, ret))
                done_gpus.append(gpu)
        for g in done_gpus:
            del active[g]

        # Launch new jobs on free GPUs
        free_gpus = get_free_gpus()
        for gpu in free_gpus:
            if gpu in active:
                continue
            if not remaining:
                break
            tag, layers, sd, seed = remaining.pop(0)
            ckpt_dir = os.path.join(CKPT_BASE, f"{tag}_seed{seed}")
            cmd = [
                PYTHON, TRAIN_PY,
                "--name", tag,
                "--model_name", "EleutherAI/pythia-410m-deduped",
                "--sigma_d2d", str(sd),
                "--sigma_c2c", "0.0",
                "--analog_layers", layers,
                "--seed", str(seed),
                "--d2d-seed", str(seed),
                "--max_steps", "100",
                "--output_dir", CKPT_BASE,
            ]
            print(f"  [GPU {gpu}] TRAIN START: {tag} seed={seed} layers=[{layers}]")
            active[gpu] = (launch(cmd, gpu), (tag, layers, sd, seed))

        time.sleep(5)

    print(f"[K107-A] Training complete. {len(completed)} jobs finished.")
    return completed


def run_eval_jobs(train_completed):
    """Launch all eval jobs for completed checkpoints."""
    # Build eval queue from successfully completed train jobs
    eval_queue = []
    for (tag, layers, sd, seed), retcode in train_completed:
        if retcode != 0:
            print(f"  SKIP eval for {tag} seed={seed} (train failed)")
            continue
        ckpt_dir = os.path.join(CKPT_BASE, f"{tag}_seed{seed}")
        for eval_d2d in EVAL_D2D_LEVELS:
            for eval_seed in EVAL_SEEDS:
                eval_queue.append((tag, seed, ckpt_dir, eval_d2d, eval_seed))

    print(f"[K107-A] Starting {len(eval_queue)} evaluation jobs...")
    active = {}
    completed = []

    while eval_queue or active:
        done_gpus = []
        for gpu, (proc, item) in active.items():
            ret = proc.poll()
            if ret is not None:
                tag, tseed, ckpt, eval_d2d, eval_seed = item
                print(f"  [GPU {gpu}] EVAL DONE: {tag} tseed={tseed} d2d={eval_d2d} eseed={eval_seed}  return={ret}")
                completed.append((item, ret))
                done_gpus.append(gpu)
        for g in done_gpus:
            del active[g]

        free_gpus = get_free_gpus()
        for gpu in free_gpus:
            if gpu in active:
                continue
            if not eval_queue:
                break
            tag, tseed, ckpt, eval_d2d, eval_seed = eval_queue.pop(0)
            cmd = [
                PYTHON, EVAL_PY,
                "--checkpoint_dir", ckpt,
                "--n_states", "256",
                "--sigma_d2d", str(eval_d2d),
                "--sigma_c2c", "0.0",
                "--max_length", "512",
                "--output_dir", OUT_DIR,
                "--d2d-seed", str(eval_seed),
            ]
            print(f"  [GPU {gpu}] EVAL START: {tag} tseed={tseed} d2d={eval_d2d} eseed={eval_seed}")
            active[gpu] = (launch(cmd, gpu), (tag, tseed, ckpt, eval_d2d, eval_seed))

        time.sleep(2)

    print(f"[K107-A] Evaluation complete. {len(completed)} jobs finished.")
    return completed


def write_summary():
    """Aggregate all result JSONs into a summary CSV."""
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
            "ppl": data.get("ppl"),
            "wall_clock_time": data.get("wall_clock_time"),
            "gpu_id": data.get("gpu_id"),
        })

    csv_path = os.path.join(OUT_DIR, "summary.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else [])
        writer.writeheader()
        writer.writerows(rows)
    print(f"[K107-A] Summary written: {csv_path}")


def main():
    train_completed = run_train_jobs()
    eval_completed = run_eval_jobs(train_completed)
    write_summary()
    print("[K107-A] All done.")


if __name__ == "__main__":
    main()
