"""
K107-C State-Count Sweep Launcher

Trains last1 [23] with n_states = 16, 32, 64, 128, 256 (seed 42).
Reuses existing k107_a1_last1_seed42 for n_states=256.
Evaluates at D2D=0.02 and 0.05 with seeds 42, 123, 456.
"""

import os
import sys
import time
import subprocess

PYTHON = "/home/lisq753/miniconda3/envs/LLM/bin/python"
TRAIN_PY = "/home/lisq753/projects/HAT/HAT/p3_hat_train.py"
EVAL_PY = "/home/lisq753/projects/HAT/HAT/p3_hat_eval.py"
OUT_DIR = "/home/lisq753/projects/HAT/HAT/deliverable/results_v3/k107_c"
CKPT_BASE = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints"

os.makedirs(OUT_DIR, exist_ok=True)

# Training jobs: (tag, n_states, analog_layers, sigma_d2d, train_seed)
# n_states=256 already trained as k107_a1_last1_seed42
TRAIN_JOBS = [
    ("k107_c_16states", 16, "23", 0.02, 42),
    ("k107_c_32states", 32, "23", 0.02, 42),
    ("k107_c_64states", 64, "23", 0.02, 42),
    ("k107_c_128states", 128, "23", 0.02, 42),
]

EVAL_D2D_LEVELS = [0.02, 0.05]
EVAL_SEEDS = [42, 123, 456]


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


def run_train_jobs():
    remaining = list(TRAIN_JOBS)
    active = {}
    completed = []

    print(f"[K107-C] Starting {len(remaining)} training jobs...")
    while remaining or active:
        done_gpus = []
        for gpu, (proc, job) in active.items():
            ret = proc.poll()
            if ret is not None:
                tag, nst, layers, sd, seed = job
                print(f"  [GPU {gpu}] TRAIN DONE: {tag} n_states={nst} return={ret}")
                completed.append((job, ret))
                done_gpus.append(gpu)
        for g in done_gpus:
            del active[g]

        free_gpus = get_free_gpus()
        for gpu in free_gpus:
            if gpu in active:
                continue
            if not remaining:
                break
            tag, nst, layers, sd, seed = remaining.pop(0)
            cmd = [
                PYTHON, TRAIN_PY,
                "--name", tag,
                "--model_name", "EleutherAI/pythia-410m-deduped",
                "--sigma_d2d", str(sd),
                "--sigma_c2c", "0.0",
                "--n_states", str(nst),
                "--analog_layers", layers,
                "--seed", str(seed),
                "--d2d-seed", str(seed),
                "--max_steps", "100",
                "--output_dir", CKPT_BASE,
            ]
            print(f"  [GPU {gpu}] TRAIN START: {tag} n_states={nst}")
            active[gpu] = (launch(cmd, gpu), (tag, nst, layers, sd, seed))

        time.sleep(5)

    print(f"[K107-C] Training complete. {len(completed)} jobs finished.")
    return completed


def run_eval_jobs(train_completed):
    eval_queue = []

    # Add evals for newly trained checkpoints
    for (tag, nst, layers, sd, seed), retcode in train_completed:
        if retcode != 0:
            print(f"  SKIP eval for {tag} (train failed)")
            continue
        ckpt_dir = os.path.join(CKPT_BASE, f"{tag}_seed{seed}")
        for eval_d2d in EVAL_D2D_LEVELS:
            for eval_seed in EVAL_SEEDS:
                eval_queue.append((tag, nst, seed, ckpt_dir, eval_d2d, eval_seed))

    # Add evals for existing n_states=256 checkpoint (k107_a1_last1_seed42)
    ckpt_256 = os.path.join(CKPT_BASE, "k107_a1_last1_seed42")
    for eval_d2d in EVAL_D2D_LEVELS:
        for eval_seed in EVAL_SEEDS:
            eval_queue.append(("k107_c_256states", 256, 42, ckpt_256, eval_d2d, eval_seed))

    print(f"[K107-C] Starting {len(eval_queue)} evaluation jobs...")
    active = {}
    completed = []

    while eval_queue or active:
        done_gpus = []
        for gpu, (proc, item) in active.items():
            ret = proc.poll()
            if ret is not None:
                tag, nst, tseed, ckpt, eval_d2d, eval_seed = item
                print(f"  [GPU {gpu}] EVAL DONE: {tag} d2d={eval_d2d} eseed={eval_seed} return={ret}")
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
            tag, nst, tseed, ckpt, eval_d2d, eval_seed = eval_queue.pop(0)
            cmd = [
                PYTHON, EVAL_PY,
                "--checkpoint_dir", ckpt,
                "--n_states", str(nst),
                "--sigma_d2d", str(eval_d2d),
                "--sigma_c2c", "0.0",
                "--max_length", "512",
                "--output_dir", OUT_DIR,
                "--d2d-seed", str(eval_seed),
            ]
            print(f"  [GPU {gpu}] EVAL START: {tag} d2d={eval_d2d} eseed={eval_seed}")
            active[gpu] = (launch(cmd, gpu), (tag, nst, tseed, ckpt, eval_d2d, eval_seed))

        time.sleep(2)

    print(f"[K107-C] Evaluation complete. {len(completed)} jobs finished.")
    return completed


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
            "n_states": data.get("n_states"),
            "train_seed": data.get("train_seed"),
            "eval_d2d_seed": data.get("eval_d2d_seed"),
            "sigma_d2d": data.get("sigma_d2d"),
            "ppl": data.get("ppl"),
            "wall_clock_time": data.get("wall_clock_time"),
        })
    csv_path = os.path.join(OUT_DIR, "summary.csv")
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else [])
        writer.writeheader()
        writer.writerows(rows)
    print(f"[K107-C] Summary written: {csv_path}")


def main():
    train_completed = run_train_jobs()
    eval_completed = run_eval_jobs(train_completed)
    write_summary()
    print("[K107-C] All done.")


if __name__ == "__main__":
    main()
