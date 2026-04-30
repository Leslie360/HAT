#!/usr/bin/env python3
"""
HAT Fresh D2D Cross-Instance Evaluation — minimal supplement to pipeline_d2d_seed.py.

Problem: pipeline_d2d_seed.py evals do NOT pass --d2d-seed, so eval auto-loads
the SAME d2d_seed from hat_config.json. That tests "same-instance stability",
NOT "generalization to a fresh device instance."

This script: for the d2d_seed=42 checkpoints (D2D=0.02 and D2D=0.04), eval at
D2D={0.02, 0.04, 0.05} with d2d_seed={42, 123, 456, 789, 1001} explicitly set,
overriding the checkpoint's own seed. This gives the cross-instance matrix.

Total: 2 ckpts × 3 D2D levels × 5 d2d_seeds = 30 eval tasks.

Usage:  python pipeline_fresh_d2d.py [--dry-run]
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
NUM_GPUS = 8
POLL_INTERVAL = 15

D2D_SEEDS = [42, 123, 456, 789, 1001]
EVAL_D2D_LEVELS = [0.02, 0.04, 0.05]

# Only evaluate the d2d_seed=42 checkpoints (these represent specific device instances)
CKPT_NAMES = [
    "hat_d2d002_500_v2_d2dseed42_seed42",
    "hat_d2d004_500_v2_d2dseed42_seed42",
]

TASK_STATE_FILE = os.path.join(OUT_DIR, ".pipeline_fresh_d2d_state.json")


def make_eval_task(ckpt_name, eval_sigma_d2d, eval_sigma_c2c, d2d_seed, desc):
    return {
        "type": "eval",
        "checkpoint_dir": os.path.join(CKPT_DIR, ckpt_name),
        "sigma_d2d": eval_sigma_d2d,
        "sigma_c2c": eval_sigma_c2c,
        "d2d_seed": d2d_seed,  # EXPLICIT override
        "n_states": 256,
        "max_length": 512,
        "desc": desc,
    }


def build_tasks():
    """Build all cross-instance eval tasks."""
    tasks = []
    for ckpt_name in CKPT_NAMES:
        for d2d_level in EVAL_D2D_LEVELS:
            for ds in D2D_SEEDS:
                tasks.append(make_eval_task(
                    ckpt_name,
                    eval_sigma_d2d=d2d_level,
                    eval_sigma_c2c=0.0,
                    d2d_seed=ds,
                    desc=f"FreshD2D {ckpt_name} eval_d2d={d2d_level} d2d_seed={ds}",
                ))
    return tasks


# ═══════════════════════════════════════════════════════════════
# Pipeline Engine (same pattern as pipeline_d2d_seed.py)
# ═══════════════════════════════════════════════════════════════


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
            if util == 0:
                free.append(idx)
        return free
    except Exception as e:
        print(f"[WARN] nvidia-smi failed: {e}")
        return []


def result_exists(task):
    ckpt_name = os.path.basename(task["checkpoint_dir"])
    ds = task.get("d2d_seed", 0xD2D)
    fname = f"eval_{ckpt_name}_c2c{task['sigma_c2c']}_d2d{task['sigma_d2d']}_seed{ds}.json"
    return os.path.isfile(os.path.join(OUT_DIR, fname))


def log_file(task):
    ckpt_name = os.path.basename(task["checkpoint_dir"])
    ds = task.get("d2d_seed", 0xD2D)
    return os.path.join(OUT_DIR, f"eval_{ckpt_name}_c2c{task['sigma_c2c']}_d2d{task['sigma_d2d']}_seed{ds}.log")


def build_cmd(task, gpu_id):
    env = f"CUDA_VISIBLE_DEVICES={gpu_id} "
    env += f"HTTP_PROXY=http://127.0.0.1:1080 HTTPS_PROXY=http://127.0.0.1:1080 "
    env += f"HF_HUB_OFFLINE=1 "

    cmd = (
        f"{PYTHON} p3_hat_eval.py "
        f"--checkpoint_dir {task['checkpoint_dir']} "
        f"--n_states {task['n_states']} "
        f"--sigma_d2d {task['sigma_d2d']} "
        f"--sigma_c2c {task['sigma_c2c']} "
        f"--max_length {task['max_length']} "
        f"--output_dir {OUT_DIR} "
        f"--d2d-seed {task['d2d_seed']} "  # <-- THIS is the critical override
    )
    return f"cd {HAT_DIR} && {env} nohup {cmd} > {log_file(task)} 2>&1 &"


def load_state():
    if os.path.isfile(TASK_STATE_FILE):
        with open(TASK_STATE_FILE) as f:
            return json.load(f)
    return {"completed": [], "started_at": time.strftime("%Y-%m-%d %H:%M:%S")}


def save_state(state):
    os.makedirs(os.path.dirname(TASK_STATE_FILE), exist_ok=True)
    with open(TASK_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def task_key(task):
    ds = task.get("d2d_seed", None)
    return f"eval:{os.path.basename(task['checkpoint_dir'])}:d2d{task['sigma_d2d']}:c2c{task['sigma_c2c']}:ds{ds}"


def wait_for_checkpoints(tasks, timeout_min=120):
    """Block until all required checkpoints exist on disk."""
    needed = set()
    for t in tasks:
        needed.add(t["checkpoint_dir"])
    needed = sorted(needed)

    waited = 0
    while True:
        missing = [d for d in needed if not os.path.isdir(d)]
        if not missing:
            print(f"All {len(needed)} checkpoints ready.\n")
            return
        print(f"Waiting for {len(missing)} checkpoints... ({waited}m elapsed)")
        for m in missing:
            print(f"  missing: {m}")
        if waited >= timeout_min:
            print(f"ERROR: Timeout after {timeout_min}m waiting for checkpoints")
            sys.exit(1)
        time.sleep(60)
        waited += 1


def run_pipeline(dry_run=False):
    sys.stdout.reconfigure(line_buffering=True)

    tasks = build_tasks()
    state = load_state()
    completed_keys = set(state["completed"])

    print("=" * 60)
    print("HAT Fresh D2D Cross-Instance Eval Pipeline")
    print(f"Checkpoints: {CKPT_NAMES}")
    print(f"Eval D2D levels: {EVAL_D2D_LEVELS}")
    print(f"Eval d2d_seeds: {D2D_SEEDS}")
    print(f"Total tasks: {len(tasks)} (2 ckpts × 3 D2D × 5 seeds)")
    print(f"Completed already: {len(completed_keys)}")
    if dry_run:
        print("*** DRY RUN ***")
    print("=" * 60)

    # Wait for checkpoints to exist before starting
    if not dry_run:
        wait_for_checkpoints(tasks)

    pending = [t for t in tasks if task_key(t) not in completed_keys]
    completed_phase = [t for t in tasks if task_key(t) in completed_keys]
    print(f"Pending: {len(pending)}, Already done: {len(completed_phase)}")

    if not pending:
        print("All done!")
        return

    task_iter = iter(pending)
    active = {}

    while True:
        finished = []
        for gpu, atask in list(active.items()):
            if result_exists(atask):
                finished.append((gpu, atask))
                print(f"  ✅ GPU{gpu} done: {atask['desc']}")
                completed_keys.add(task_key(atask))

        for gpu, atask in finished:
            del active[gpu]

        if not active or len(active) < NUM_GPUS:
            free_gpus = get_free_gpus()
            free_gpus = [g for g in free_gpus if g not in active]

            for gpu in free_gpus:
                try:
                    atask = next(task_iter)
                except StopIteration:
                    break

                if dry_run:
                    print(f"  [DRY-RUN] GPU{gpu}: {atask['desc']}")
                    completed_keys.add(task_key(atask))
                    continue

                cmd = build_cmd(atask, gpu)
                print(f"  🚀 GPU{gpu} → {atask['desc']}")
                subprocess.run(cmd, shell=True, check=False)
                active[gpu] = atask
                time.sleep(2)

        if not dry_run and (finished or len(active) < NUM_GPUS):
            state["completed"] = list(completed_keys)
            save_state(state)

        if all(task_key(t) in completed_keys for t in tasks):
            print("  ✅ All fresh-D2D eval tasks complete!")
            break

        if not active:
            if all(task_key(t) in completed_keys for t in tasks):
                break
            print("  ⏳ All tasks launched, waiting...")
            time.sleep(POLL_INTERVAL * 2)
        else:
            running_str = ", ".join(f"GPU{g}:{t['desc'][:40]}" for g, t in sorted(active.items()))
            print(f"  ⏳ Running: {len(active)}/8 — {running_str}")
            time.sleep(POLL_INTERVAL)

    if not dry_run:
        state["completed"] = list(completed_keys)
        state["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        save_state(state)

    print(f"\n{'=' * 60}")
    print(f"Fresh D2D eval complete! {len(completed_keys)}/{len(tasks)} tasks done.")

    # Summary
    print(f"\nResult summary:")
    for t in tasks:
        if task_key(t) not in completed_keys:
            continue
        ckpt_name = os.path.basename(t["checkpoint_dir"])
        ds = t.get("d2d_seed", 0xD2D)
        fname = f"eval_{ckpt_name}_c2c{t['sigma_c2c']}_d2d{t['sigma_d2d']}_seed{ds}.json"
        fpath = os.path.join(OUT_DIR, fname)
        if os.path.isfile(fpath):
            try:
                with open(fpath) as f:
                    d = json.load(f)
                print(f"  {t['desc']:60s} → PPL {d['ppl']:.2f}")
            except:
                pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HAT Fresh D2D Cross-Instance Eval")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if not args.dry_run and os.path.isfile(TASK_STATE_FILE):
        os.remove(TASK_STATE_FILE)

    run_pipeline(dry_run=args.dry_run)
