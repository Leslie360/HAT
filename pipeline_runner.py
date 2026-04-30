#!/usr/bin/env python3
"""
HAT Pipeline Runner — 8-GPU auto-dispatch, self-contained, holiday-proof.

Usage:  python pipeline_runner.py [--dry-run] [--resume]

Phases:
  1. Generalization eval (20 runs) — uses existing v2 checkpoints
  2. Selective layer sweep (5 training runs)
  3. Seed 123/456 repeats (8 training runs)
  4. D2D sweep + convergence (7 training runs)
  E. Retention probe (1 training run, optional)

Each phase must finish before the next starts (eval depends on checkpoints).
Within a phase, tasks are dispatched to any free GPU.
"""

import argparse
import json
import os
import subprocess
import sys
import time
import re

HAT_DIR = "/home/lisq753/projects/HAT/HAT"
OUT_DIR = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107"
CKPT_DIR = os.path.join(OUT_DIR, "checkpoints")
PYTHON = "/home/lisq753/miniconda3/envs/LLM/bin/python"
NUM_GPUS = 8
POLL_INTERVAL = 15  # seconds

# ── Task definitions ─────────────────────────────────────────────

PHASES = []

# ── Phase 1: Generalization Eval (20 runs) ──

def make_eval_task(ckpt_name, eval_sigma_d2d, eval_sigma_c2c, d2d_seed=None, desc=""):
    task = {
        "type": "eval",
        "checkpoint_dir": os.path.join(CKPT_DIR, ckpt_name),
        "sigma_d2d": eval_sigma_d2d,
        "sigma_c2c": eval_sigma_c2c,
        "n_states": 256,
        "max_length": 512,
        "desc": desc or f"eval {ckpt_name} d2d={eval_sigma_d2d} c2c={eval_sigma_c2c}",
    }
    if d2d_seed is not None:
        task["d2d_seed"] = d2d_seed
    return task

phase1_tasks = []

# 1a. D2D=0.02 ckpt → 6 noise levels
for d2d in [0.00, 0.01, 0.02, 0.03, 0.04, 0.05]:
    phase1_tasks.append(make_eval_task(
        "hat_d2d002_500_v2_seed42", eval_sigma_d2d=d2d, eval_sigma_c2c=0.0,
        desc=f"D2D0.02ckpt eval D2D={d2d}"
    ))

# 1b. D2D=0.04 ckpt → 6 noise levels
for d2d in [0.00, 0.01, 0.02, 0.03, 0.04, 0.05]:
    phase1_tasks.append(make_eval_task(
        "hat_d2d004_500_v2_seed42", eval_sigma_d2d=d2d, eval_sigma_c2c=0.0,
        desc=f"D2D0.04ckpt eval D2D={d2d}"
    ))

# 1c. C2C=0.01 ckpt → 5 noise levels
for c2c in [0.000, 0.005, 0.010, 0.015, 0.020]:
    phase1_tasks.append(make_eval_task(
        "hat_c2c001_500_v2_seed42", eval_sigma_d2d=0.0, eval_sigma_c2c=c2c,
        desc=f"C2C0.01ckpt eval C2C={c2c}"
    ))

# 1d. Combined ckpt → 3 cross-type
for d2d, c2c in [(0.0, 0.0), (0.04, 0.0), (0.0, 0.02)]:
    phase1_tasks.append(make_eval_task(
        "hat_combined_500_v2_seed42", eval_sigma_d2d=d2d, eval_sigma_c2c=c2c,
        desc=f"Combinedckpt eval D2D={d2d} C2C={c2c}"
    ))

PHASES.append(("Phase 1: Generalization Eval", phase1_tasks))

# ── Phase 2: Selective Layer Sweep (5 training runs) ──

def make_train_task(name, sigma_d2d, sigma_c2c, max_steps, analog_layers=None, seed=42, d2d_seed=0xD2D, desc=""):
    task = {
        "type": "train",
        "name": name,
        "n_states": 256,
        "sigma_d2d": sigma_d2d,
        "sigma_c2c": sigma_c2c,
        "max_steps": max_steps,
        "max_length": 512,
        "seed": seed,
        "d2d_seed": d2d_seed,
        "desc": desc or name,
    }
    if analog_layers is not None:
        task["analog_layers"] = ",".join(str(x) for x in analog_layers)
    return task

phase2_tasks = [
    make_train_task("hat_d2d002_last2_500_v2", 0.02, 0.0, 500,
                    analog_layers=[22, 23],
                    desc="D2D=0.02 selective last2"),
    make_train_task("hat_d2d002_last4_500_v2", 0.02, 0.0, 500,
                    analog_layers=[20,21,22,23],
                    desc="D2D=0.02 selective last4"),
    make_train_task("hat_c2c001_last2_500_v2", 0.0, 0.01, 500,
                    analog_layers=[22, 23],
                    desc="C2C=0.01 selective last2"),
    make_train_task("hat_c2c001_last4_500_v2", 0.0, 0.01, 500,
                    analog_layers=[20,21,22,23],
                    desc="C2C=0.01 selective last4"),
    make_train_task("hat_combined_last2_500_v2", 0.02, 0.01, 500,
                    analog_layers=[22, 23],
                    desc="Combined selective last2"),
]
PHASES.append(("Phase 2: Selective Layer", phase2_tasks))

# ── Phase 3: Seed 123/456 Repeats (8 runs) ──

phase3_tasks = []
base_configs = [
    ("hat_d2d002_500_v2", 0.02, 0.0),
    ("hat_d2d004_500_v2", 0.04, 0.0),
    ("hat_c2c001_500_v2", 0.0, 0.01),
    ("hat_combined_500_v2", 0.02, 0.01),
]
for base_name, d2d, c2c in base_configs:
    for seed in [123, 456]:
        phase3_tasks.append(make_train_task(
            base_name, d2d, c2c, 500, seed=seed,
            desc=f"{base_name} seed={seed}",
        ))
PHASES.append(("Phase 3: Seed Repeat", phase3_tasks))

# ── Phase 4: D2D Sweep + Convergence (7 runs) ──

phase4_tasks = [
    make_train_task("hat_d2d0025_500_v2", 0.025, 0.0, 500, desc="D2D=0.025 500step"),
    make_train_task("hat_d2d003_500_v2", 0.030, 0.0, 500, desc="D2D=0.030 500step"),
    make_train_task("hat_d2d0035_500_v2", 0.035, 0.0, 500, desc="D2D=0.035 500step"),
    make_train_task("hat_d2d0045_500_v2", 0.045, 0.0, 500, desc="D2D=0.045 500step"),
    make_train_task("hat_d2d005_500_v2", 0.050, 0.0, 500, desc="D2D=0.050 500step"),
    make_train_task("hat_d2d002_200_500_v2", 0.02, 0.0, 200, desc="D2D=0.02 200step"),
    make_train_task("hat_d2d002_1000_500_v2", 0.02, 0.0, 1000, desc="D2D=0.02 1000step"),
]
PHASES.append(("Phase 4: D2D Sweep", phase4_tasks))

# ⏸ Phase 5: Retention probe (optional, uncomment to enable)
# phase5_tasks = [
#     make_train_task("hat_retention_d2d002_500_v2", 0.02, 0.0, 500,
#                     desc="D2D=0.02 with retention"),
# ]
# PHASES.append(("Phase 5: Retention Probe", phase5_tasks))


# ── Pipeline Engine ──────────────────────────────────────────────

TASK_STATE_FILE = os.path.join(OUT_DIR, ".pipeline_state.json")


def get_free_gpus():
    """Return list of GPU indices that are idle (0% compute utilization)."""
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
    """Check if the output file for this task already exists."""
    if task["type"] == "eval":
        ckpt_name = os.path.basename(task["checkpoint_dir"])
        fname = f"eval_{ckpt_name}_c2c{task['sigma_c2c']}_d2d{task['sigma_d2d']}.json"
        return os.path.isfile(os.path.join(OUT_DIR, fname))
    else:
        fname = f"{task['name']}_seed{task['seed']}.json"
        return os.path.isfile(os.path.join(OUT_DIR, fname))


def log_file(task):
    """Path to the log file for a task."""
    if task["type"] == "eval":
        ckpt_name = os.path.basename(task["checkpoint_dir"])
        return os.path.join(OUT_DIR, f"eval_{ckpt_name}_c2c{task['sigma_c2c']}_d2d{task['sigma_d2d']}.log")
    else:
        return os.path.join(OUT_DIR, f"{task['name']}_seed{task['seed']}.log")


def build_cmd(task, gpu_id):
    """Build the shell command for a task on a specific GPU."""
    env = f"CUDA_VISIBLE_DEVICES={gpu_id} "
    env += f"HTTP_PROXY=http://127.0.0.1:1080 HTTPS_PROXY=http://127.0.0.1:1080 "
    env += f"HF_HUB_OFFLINE=1 "

    if task["type"] == "eval":
        cmd = (
            f"{PYTHON} p3_hat_eval.py "
            f"--checkpoint_dir {task['checkpoint_dir']} "
            f"--n_states {task['n_states']} "
            f"--sigma_d2d {task['sigma_d2d']} "
            f"--sigma_c2c {task['sigma_c2c']} "
            f"--max_length {task['max_length']} "
            f"--output_dir {OUT_DIR} "
        )
        if "d2d_seed" in task:
            cmd += f"--d2d-seed {task['d2d_seed']} "
    else:
        cmd = (
            f"{PYTHON} p3_hat_train.py "
            f"--name {task['name']} "
            f"--n_states {task['n_states']} "
            f"--sigma_d2d {task['sigma_d2d']} "
            f"--sigma_c2c {task['sigma_c2c']} "
            f"--max_steps {task['max_steps']} "
            f"--max_length {task['max_length']} "
            f"--seed {task['seed']} "
            f"--d2d-seed {task.get('d2d_seed', 0xD2D)} "
        )
        if "analog_layers" in task:
            cmd += f"--analog_layers {task['analog_layers']} "

    full_cmd = f"cd {HAT_DIR} && {env} nohup {cmd} > {log_file(task)} 2>&1 &"
    return full_cmd


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
    if task["type"] == "eval":
        return f"eval:{os.path.basename(task['checkpoint_dir'])}:d2d{task['sigma_d2d']}:c2c{task['sigma_c2c']}"
    return f"train:{task['name']}:seed{task['seed']}"


def run_pipeline(dry_run=False, resume=False):
    sys.stdout.reconfigure(line_buffering=True)
    state = load_state() if resume else {"completed": [], "started_at": time.strftime("%Y-%m-%d %H:%M:%S")}
    completed_keys = set(state["completed"])
    total_all = sum(len(tasks) for _, tasks in PHASES)

    print(f"=" * 60)
    print(f"HAT Pipeline Runner")
    print(f"Started: {state['started_at']}")
    print(f"Phases: {len(PHASES)}, Total tasks: {total_all}")
    print(f"Completed already: {len(completed_keys)}")
    if dry_run:
        print(f"*** DRY RUN — no tasks will be launched ***")
    print(f"=" * 60)

    for phase_name, tasks in PHASES:
        pending = [t for t in tasks if task_key(t) not in completed_keys]
        completed_phase = [t for t in tasks if task_key(t) in completed_keys]
        print(f"\n{'─' * 50}")
        print(f"{phase_name}: {len(completed_phase)}/{len(tasks)} done, {len(pending)} pending")

        if not pending:
            continue

        # Wait for all tasks in this phase to complete
        task_iter = iter(pending)
        active = {}  # gpu_id -> task

        while True:
            # Check for completed tasks
            finished = []
            for gpu, atask in list(active.items()):
                if result_exists(atask):
                    finished.append((gpu, atask))
                    print(f"  ✅ GPU{gpu} done: {atask['desc']}")
                    completed_keys.add(task_key(atask))

            for gpu, atask in finished:
                del active[gpu]

            # Launch new tasks on free GPUs
            if not active or len(active) < NUM_GPUS:
                free_gpus = get_free_gpus()
                # Filter to GPUs not currently in use
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
                    time.sleep(2)  # stagger launches

            # Save state periodically (never in dry-run)
            if not dry_run and (finished or len(active) < NUM_GPUS):
                state["completed"] = list(completed_keys)
                save_state(state)

            # Check if phase is done
            phase_completed = all(task_key(t) in completed_keys for t in tasks)
            if phase_completed:
                print(f"  ✅ {phase_name} complete!")
                break

            if not active:
                # No tasks running and no pending tasks left (edge case)
                if all(task_key(t) in completed_keys for t in tasks):
                    break
                # All pending tasks launched, waiting for results
                print(f"  ⏳ All tasks launched, waiting...")
                time.sleep(POLL_INTERVAL * 2)
            else:
                running_str = ", ".join(f"GPU{g}:{t['desc'][:30]}" for g, t in sorted(active.items()))
                print(f"  ⏳ Running: {len(active)}/8 — {running_str}")
                time.sleep(POLL_INTERVAL)

    # Final summary (never save state in dry-run)
    if not dry_run:
        state["completed"] = list(completed_keys)
        state["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        save_state(state)

    print(f"\n{'=' * 60}")
    print(f"🎯 Pipeline complete!")
    print(f"  Total tasks: {total_all}")
    print(f"  Completed:   {len(completed_keys)}")
    print(f"  Finished at: {state['finished_at']}")

    # Collect all PPL results
    print(f"\n{'─' * 50}")
    print("Result summary:")
    for phase_name, tasks in PHASES:
        completed = [t for t in tasks if task_key(t) in completed_keys]
        if completed:
            print(f"\n{phase_name}:")
            for t in completed:
                if t["type"] == "eval":
                    ckpt_name = os.path.basename(t["checkpoint_dir"])
                    fname = f"eval_{ckpt_name}_c2c{t['sigma_c2c']}_d2d{t['sigma_d2d']}.json"
                    fpath = os.path.join(OUT_DIR, fname)
                    if os.path.isfile(fpath):
                        try:
                            with open(fpath) as f:
                                d = json.load(f)
                            print(f"  {t['desc']:40s} → PPL {d['ppl']:.2f}")
                        except: pass
                else:
                    fname = f"{t['name']}_seed{t['seed']}.json"
                    fpath = os.path.join(OUT_DIR, fname)
                    if os.path.isfile(fpath):
                        try:
                            with open(fpath) as f:
                                d = json.load(f)
                            print(f"  {t['desc']:40s} → {d['ppl_before']:.1f} → {d['ppl_after']:.2f}")
                        except: pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HAT 8-GPU pipeline runner")
    parser.add_argument("--dry-run", action="store_true", help="Print tasks without launching")
    parser.add_argument("--resume", action="store_true", help="Resume from saved state")
    args = parser.parse_args()

    # Clear stale state if not resuming
    if not args.resume and not args.dry_run and os.path.isfile(TASK_STATE_FILE):
        os.remove(TASK_STATE_FILE)

    run_pipeline(dry_run=args.dry_run, resume=args.resume)
