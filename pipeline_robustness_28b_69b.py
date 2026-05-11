#!/usr/bin/env python3
"""
Robustness Sweep Pipeline for 2.8B and 6.9B HAT checkpoints.

Runs AFTER lm-eval finishes on GPUs 4/5/6/7.
Evaluates existing p28b_fixed500 and p69b_fixed500 checkpoints under
various noise configurations to verify robustness trends match 410M.

Scans:
  1. σ_c2c sweep (0.0 → 0.10)
  2. σ_d2d sweep (0.0 → 0.10)
  3. Eval mismatch (train σ ≠ eval σ)
  4. D2D seed cross-instance (5 seeds)
  5. n_states sweep (128 → 1024)

Usage:
    python pipeline_robustness_28b_69b.py [--dry-run]
"""

import argparse
import json
import os
import subprocess
import sys
import time

HAT_DIR = "/home/lisq753/projects/HAT/HAT"
OUT_DIR = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107"
CKPT_DIR = os.path.join(OUT_DIR, "checkpoints")
PYTHON = "/home/lisq753/miniconda3/envs/LLM/bin/python"

# ONLY use GPUs 4/5/6/7 (per user constraint)
ALLOWED_GPUS = [4, 5, 6, 7]
POLL_INTERVAL = 30

# ── Checkpoints to evaluate ──
CHECKPOINTS = {
    "p28b": os.path.join(CKPT_DIR, "p28b_fixed500_seed42"),
    "p69b": os.path.join(CKPT_DIR, "p69b_fixed500_seed42"),
}

# ── Scan configurations ──
# 1. σ_c2c sweep (train: c2c=0.01, d2d=0.02)
SIGMA_C2C_VALUES = [0.0, 0.005, 0.01, 0.02, 0.05, 0.10]

# 2. σ_d2d sweep
def _d2d_vals():
    return [0.0, 0.01, 0.02, 0.04, 0.05, 0.10]

# 3. Eval mismatch: specific (train_eval) combos
MISMATCH_SCENARIOS = [
    # (train_c2c, train_d2d, eval_c2c, eval_d2d, label)
    (0.01, 0.02, 0.02, 0.02, "c2c_2x"),
    (0.01, 0.02, 0.05, 0.02, "c2c_5x"),
    (0.01, 0.02, 0.10, 0.02, "c2c_10x"),
    (0.01, 0.02, 0.01, 0.04, "d2d_2x"),
    (0.01, 0.02, 0.01, 0.10, "d2d_5x"),
]

# 4. D2D seed cross-instance
D2D_SEEDS = [42, 123, 456, 789, 1001]

# 5. n_states sweep
N_STATES_VALUES = [128, 256, 512, 1024]


def eval_result_exists(ckpt_name, sigma_c2c, sigma_d2d, d2d_seed, n_states=256):
    fname = f"eval_{ckpt_name}_c2c{sigma_c2c}_d2d{sigma_d2d}_seed{d2d_seed}_ns{n_states}.json"
    return os.path.isfile(os.path.join(OUT_DIR, fname))


def build_eval_cmd(ckpt_path, sigma_c2c, sigma_d2d, d2d_seed, n_states, gpu_id):
    ckpt_name = os.path.basename(ckpt_path)
    env = f"CUDA_VISIBLE_DEVICES={gpu_id} HF_HUB_OFFLINE=1 "
    cmd = (
        f"{PYTHON} p3_hat_eval.py "
        f"--checkpoint_dir {ckpt_path} "
        f"--n_states {n_states} "
        f"--sigma_c2c {sigma_c2c} "
        f"--sigma_d2d {sigma_d2d} "
        f"--max_length 512 "
        f"--output_dir {OUT_DIR} "
        f"--d2d-seed {d2d_seed} "
        f"--fp16"
    )
    log = os.path.join(OUT_DIR, f"eval_{ckpt_name}_c2c{sigma_c2c}_d2d{sigma_d2d}_seed{d2d_seed}_ns{n_states}.log")
    return f"cd {HAT_DIR} && {env} nohup {cmd} > {log} 2>&1 &", log


def get_free_gpus():
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=index,utilization.gpu",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10
        )
        free = []
        for line in result.stdout.strip().split("\n"):
            if not line.strip():
                continue
            idx_str, util_str = line.split(",")
            idx, util = int(idx_str.strip()), int(util_str.strip())
            if util < 30 and idx in ALLOWED_GPUS:
                free.append(idx)
        return free
    except Exception as e:
        print(f"[WARN] nvidia-smi failed: {e}")
        return []


def wait_for_lm_eval():
    """Block until no p3_hat_lm_eval.py processes remain."""
    print("=" * 60)
    print("Waiting for lm-eval to finish on GPUs 4/5/6/7...")
    print("=" * 60)
    while True:
        result = subprocess.run(
            ["pgrep", "-f", "p3_hat_lm_eval.py"],
            capture_output=True, text=True
        )
        if result.returncode != 0 or not result.stdout.strip():
            print("lm-eval finished! Launching robustness sweep.")
            break
        pids = result.stdout.strip().split("\n")
        print(f"  Still running: {len(pids)} lm-eval process(es)")
        time.sleep(60)


def generate_tasks():
    """Generate all eval tasks. Returns list of dicts."""
    tasks = []
    base_d2d_seed = 0xD2D  # default from training

    for model_key, ckpt_path in CHECKPOINTS.items():
        ckpt_name = os.path.basename(ckpt_path)
        if not os.path.isdir(ckpt_path):
            print(f"[SKIP] Checkpoint not found: {ckpt_path}")
            continue

        # 1. σ_c2c sweep (fix d2d=0.02)
        for sc2c in SIGMA_C2C_VALUES:
            if not eval_result_exists(ckpt_name, sc2c, 0.02, base_d2d_seed):
                tasks.append({
                    "ckpt_path": ckpt_path, "ckpt_name": ckpt_name,
                    "sc2c": sc2c, "sd2d": 0.02, "d2d_seed": base_d2d_seed,
                    "n_states": 256, "tag": f"{model_key}_c2c_sweep"
                })

        # 2. σ_d2d sweep (fix c2c=0.01)
        for sd2d in _d2d_vals():
            if not eval_result_exists(ckpt_name, 0.01, sd2d, base_d2d_seed):
                tasks.append({
                    "ckpt_path": ckpt_path, "ckpt_name": ckpt_name,
                    "sc2c": 0.01, "sd2d": sd2d, "d2d_seed": base_d2d_seed,
                    "n_states": 256, "tag": f"{model_key}_d2d_sweep"
                })

        # 3. Mismatch scenarios
        for tc2c, td2d, ec2c, ed2d, label in MISMATCH_SCENARIOS:
            if not eval_result_exists(ckpt_name, ec2c, ed2d, base_d2d_seed):
                tasks.append({
                    "ckpt_path": ckpt_path, "ckpt_name": ckpt_name,
                    "sc2c": ec2c, "sd2d": ed2d, "d2d_seed": base_d2d_seed,
                    "n_states": 256, "tag": f"{model_key}_mismatch_{label}"
                })

        # 4. D2D seed cross-instance (eval at train noise level)
        for ds in D2D_SEEDS:
            if not eval_result_exists(ckpt_name, 0.01, 0.02, ds):
                tasks.append({
                    "ckpt_path": ckpt_path, "ckpt_name": ckpt_name,
                    "sc2c": 0.01, "sd2d": 0.02, "d2d_seed": ds,
                    "n_states": 256, "tag": f"{model_key}_d2dseed"
                })

        # 5. n_states sweep
        for ns in N_STATES_VALUES:
            if not eval_result_exists(ckpt_name, 0.01, 0.02, base_d2d_seed, ns):
                tasks.append({
                    "ckpt_path": ckpt_path, "ckpt_name": ckpt_name,
                    "sc2c": 0.01, "sd2d": 0.02, "d2d_seed": base_d2d_seed,
                    "n_states": ns, "tag": f"{model_key}_nstates"
                })

    return tasks


def run_pipeline(dry_run=False):
    sys.stdout.reconfigure(line_buffering=True)

    if not dry_run:
        wait_for_lm_eval()

    tasks = generate_tasks()
    print(f"\n{'=' * 60}")
    print(f"Robustness Sweep: {len(tasks)} eval tasks")
    print(f"Models: {list(CHECKPOINTS.keys())}")
    print(f"GPUs: {ALLOWED_GPUS}")
    if dry_run:
        print("*** DRY RUN ***")
    print(f"{'=' * 60}\n")

    if not tasks:
        print("All tasks already completed!")
        return

    task_iter = iter(tasks)
    active = {}  # gpu_id -> task
    completed = 0

    while True:
        # Check finished
        finished = []
        for gpu, task in list(active.items()):
            if eval_result_exists(task["ckpt_name"], task["sc2c"], task["sd2d"],
                                   task["d2d_seed"], task["n_states"]):
                finished.append((gpu, task))
                completed += 1
                print(f"  ✅ GPU{gpu} done: {task['ckpt_name']} c2c={task['sc2c']} d2d={task['sd2d']} ns={task['n_states']} seed={task['d2d_seed']}")

        for gpu, _ in finished:
            del active[gpu]

        # Launch new tasks on free GPUs
        free_gpus = get_free_gpus()
        free_gpus = [g for g in free_gpus if g not in active]

        for gpu in free_gpus:
            try:
                task = next(task_iter)
            except StopIteration:
                break

            cmd, log = build_eval_cmd(
                task["ckpt_path"], task["sc2c"], task["sd2d"],
                task["d2d_seed"], task["n_states"], gpu
            )
            if dry_run:
                print(f"  [DRY-RUN] GPU{gpu}: {task['tag']} {task['ckpt_name']} c2c={task['sc2c']} d2d={task['sd2d']}")
                completed += 1
                continue

            print(f"  🚀 GPU{gpu}: {task['tag']} {task['ckpt_name']} c2c={task['sc2c']} d2d={task['sd2d']} ns={task['n_states']} seed={task['d2d_seed']}")
            subprocess.run(cmd, shell=True, check=False)
            active[gpu] = task
            time.sleep(2)

        if not active and completed >= len(tasks):
            print(f"\n{'=' * 60}")
            print(f"All {len(tasks)} tasks completed!")
            print(f"{'=' * 60}")
            break

        if not active:
            print(f"  ⏳ All tasks launched or waiting... {completed}/{len(tasks)} done")
            time.sleep(POLL_INTERVAL * 2)
        else:
            running = ", ".join(f"GPU{g}:{active[g]['tag'][:10]}" for g in sorted(active))
            print(f"  ⏳ Running: {len(active)}/{len(ALLOWED_GPUS)} — {running} | {completed}/{len(tasks)} done")
            time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    run_pipeline(dry_run=args.dry_run)
