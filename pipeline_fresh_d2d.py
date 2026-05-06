#!/usr/bin/env python3
"""
HAT Fresh-D2D Cross-Instance Pipeline — Codex P1.

Trains selective-layer checkpoints (if missing), then evaluates ALL 4 required
checkpoints at D2D={0.02,0.04,0.05} × d2d_seed={42,123,456,789,1001} with
EXPLICIT --d2d-seed override. This measures fresh-device generalization,
NOT same-instance adaptation.

Checkpoints:
  1. all-layer D2D=0.02  d2d_seed=42  (from pipeline_d2d_seed.py Phase 1)
  2. all-layer D2D=0.04  d2d_seed=42  (from pipeline_d2d_seed.py Phase 2)
  3. last1    D2D=0.02  d2d_seed=42  analog_layers=23       (trained here)
  4. last2    D2D=0.02  d2d_seed=42  analog_layers=22,23    (trained here)

Total: 2 train + 60 eval = 62 tasks.

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

# ── Required checkpoints ──
# (ckpt_dir_name, needs_training, train_kwargs)
REQUIRED_CKPTS = [
    {
        "name": "hat_d2d002_500_freshd2d_all_seed42",
        "ckpt_dir": os.path.join(CKPT_DIR, "hat_d2d002_500_v2_d2dseed42_seed42"),
        "needs_train": False,  # from pipeline_d2d_seed.py Phase 1
        "train_sigma_d2d": 0.02,
        "analog_layers": None,  # all 24 layers
        "label": "all-layer D2D=0.02",
    },
    {
        "name": "hat_d2d004_500_freshd2d_all_seed42",
        "ckpt_dir": os.path.join(CKPT_DIR, "hat_d2d004_500_v2_d2dseed42_seed42"),
        "needs_train": False,  # from pipeline_d2d_seed.py Phase 2
        "train_sigma_d2d": 0.04,
        "analog_layers": None,
        "label": "all-layer D2D=0.04",
    },
    {
        "name": "hat_d2d002_500_freshd2d_last1",
        "ckpt_dir": os.path.join(CKPT_DIR, "hat_d2d002_500_freshd2d_last1_seed42"),
        "needs_train": True,  # train now
        "train_sigma_d2d": 0.02,
        "analog_layers": "23",
        "label": "last1 D2D=0.02",
    },
    {
        "name": "hat_d2d002_500_freshd2d_last2",
        "ckpt_dir": os.path.join(CKPT_DIR, "hat_d2d002_500_freshd2d_last2_seed42"),
        "needs_train": True,  # train now
        "train_sigma_d2d": 0.02,
        "analog_layers": "22,23",
        "label": "last2 D2D=0.02",
    },
]

TASK_STATE_FILE = os.path.join(OUT_DIR, ".pipeline_fresh_d2d_state.json")


def make_train_task(ckpt_info):
    """Build a training task for a selective checkpoint."""
    return {
        "type": "train",
        "name": ckpt_info["name"],
        "ckpt_dir": ckpt_info["ckpt_dir"],
        "n_states": 256,
        "sigma_d2d": ckpt_info["train_sigma_d2d"],
        "sigma_c2c": 0.0,
        "max_steps": 500,
        "max_length": 512,
        "seed": 42,
        "d2d_seed": 42,
        "analog_layers": ckpt_info["analog_layers"],
        "desc": f"Train {ckpt_info['label']}",
    }


def make_eval_task(ckpt_info, eval_sigma_d2d, eval_d2d_seed):
    """Build an eval task with explicit --d2d-seed override."""
    return {
        "type": "eval",
        "checkpoint_dir": ckpt_info["ckpt_dir"],
        "sigma_d2d": eval_sigma_d2d,
        "sigma_c2c": 0.0,
        "d2d_seed": eval_d2d_seed,  # EXPLICIT override
        "n_states": 256,
        "max_length": 512,
        "analog_layers": ckpt_info.get("analog_layers"),
        "desc": f"Eval {ckpt_info['label']} D2D={eval_sigma_d2d} seed={eval_d2d_seed}",
    }


def build_all_tasks():
    """Build train (selective) + eval (all 4 ckpts) tasks."""
    tasks = []

    # Phase A: Train selective checkpoints that don't exist yet
    for ckpt in REQUIRED_CKPTS:
        if ckpt["needs_train"] and not os.path.isdir(ckpt["ckpt_dir"]):
            tasks.append(make_train_task(ckpt))

    # Phase B: Cross-instance eval — ALL 4 checkpoints
    for ckpt in REQUIRED_CKPTS:
        for d2d_level in EVAL_D2D_LEVELS:
            for ds in D2D_SEEDS:
                tasks.append(make_eval_task(ckpt, d2d_level, ds))

    return tasks


# ═══════════════════════════════════════════════════════════════
# Pipeline Engine
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
    if task["type"] == "train":
        fname = f"{task['name']}_seed{task['seed']}.json"
        return os.path.isfile(os.path.join(OUT_DIR, fname))
    else:
        ckpt_name = os.path.basename(task["checkpoint_dir"])
        ds = task.get("d2d_seed", 0xD2D)
        fname = f"eval_{ckpt_name}_c2c{task['sigma_c2c']}_d2d{task['sigma_d2d']}_seed{ds}.json"
        return os.path.isfile(os.path.join(OUT_DIR, fname))


def log_file(task):
    if task["type"] == "train":
        return os.path.join(OUT_DIR, f"{task['name']}_seed{task['seed']}.log")
    else:
        ckpt_name = os.path.basename(task["checkpoint_dir"])
        ds = task.get("d2d_seed", 0xD2D)
        return os.path.join(OUT_DIR, f"eval_{ckpt_name}_c2c{task['sigma_c2c']}_d2d{task['sigma_d2d']}_seed{ds}.log")


def build_cmd(task, gpu_id):
    env = f"CUDA_VISIBLE_DEVICES={gpu_id} "
    env += f"HF_HUB_OFFLINE=1 "

    if task["type"] == "train":
        cmd = (
            f"{PYTHON} p3_hat_train.py "
            f"--name {task['name']} "
            f"--n_states {task['n_states']} "
            f"--sigma_d2d {task['sigma_d2d']} "
            f"--sigma_c2c {task['sigma_c2c']} "
            f"--max_steps {task['max_steps']} "
            f"--max_length {task['max_length']} "
            f"--seed {task['seed']} "
            f"--d2d-seed {task['d2d_seed']} "
        )
        if task.get("analog_layers"):
            cmd += f"--analog_layers {task['analog_layers']} "
    else:
        cmd = (
            f"{PYTHON} p3_hat_eval.py "
            f"--checkpoint_dir {task['checkpoint_dir']} "
            f"--n_states {task['n_states']} "
            f"--sigma_d2d {task['sigma_d2d']} "
            f"--sigma_c2c {task['sigma_c2c']} "
            f"--max_length {task['max_length']} "
            f"--output_dir {OUT_DIR} "
            f"--d2d-seed {task['d2d_seed']} "
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
    if task["type"] == "train":
        return f"train:{task['name']}:seed{task['seed']}:ds{task.get('d2d_seed', 0xD2D)}"
    ds = task.get("d2d_seed", None)
    return f"eval:{os.path.basename(task['checkpoint_dir'])}:d2d{task['sigma_d2d']}:c2c{task['sigma_c2c']}:ds{ds}"


def run_pipeline(dry_run=False):
    sys.stdout.reconfigure(line_buffering=True)

    tasks = build_all_tasks()
    state = load_state()
    completed_keys = set(state["completed"])

    n_train = sum(1 for t in tasks if t["type"] == "train")
    n_eval = sum(1 for t in tasks if t["type"] == "eval")

    print("=" * 60)
    print("HAT Fresh-D2D Cross-Instance Pipeline (Codex P1)")
    print(f"Checkpoints: {len(REQUIRED_CKPTS)} (2 all-layer + 2 selective)")
    print(f"Train tasks: {n_train} (selective ckpts only)")
    print(f"Eval tasks:  {n_eval} (4 ckpts × 3 D2D × 5 seeds)")
    print(f"Completed:   {len(completed_keys)}")
    if dry_run:
        print("*** DRY RUN ***")
    print("=" * 60)

    pending = [t for t in tasks if task_key(t) not in completed_keys]
    # Sort: train tasks first, then eval tasks whose checkpoints exist
    def dispatch_priority(t):
        if t["type"] == "train":
            return 0
        if os.path.isdir(t["checkpoint_dir"]):
            return 1
        return 2  # waiting for checkpoint
    pending.sort(key=dispatch_priority)

    if not pending:
        print("All done!")
        return

    print(f"Pending: {len(pending)}")
    pending_idx = 0
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
                # Re-sort remaining pending tasks (new checkpoints may now exist)
                remaining = [t for t in pending if task_key(t) not in completed_keys]
                remaining.sort(key=dispatch_priority)

                # Find next dispatchable task (not already active)
                active_keys = {task_key(t) for t in active.values()}
                next_t = None
                for t in remaining:
                    if task_key(t) in completed_keys or task_key(t) in active_keys:
                        continue
                    if t["type"] == "eval" and not os.path.isdir(t["checkpoint_dir"]):
                        continue  # still waiting
                    next_t = t
                    break

                if next_t is None:
                    break

                if dry_run:
                    print(f"  [DRY-RUN] GPU{gpu}: {next_t['desc']}")
                    completed_keys.add(task_key(next_t))
                    continue

                cmd = build_cmd(next_t, gpu)
                print(f"  🚀 GPU{gpu} → {next_t['desc']}")
                subprocess.run(cmd, shell=True, check=False)
                active[gpu] = next_t
                time.sleep(2)

        if not dry_run and (finished or len(active) < NUM_GPUS):
            state["completed"] = list(completed_keys)
            save_state(state)

        if all(task_key(t) in completed_keys for t in tasks):
            print("  ✅ All fresh-D2D tasks complete!")
            break

        if not active:
            if all(task_key(t) in completed_keys for t in tasks):
                break
            # Check if remaining tasks are just waiting for checkpoints
            remaining = [t for t in tasks if task_key(t) not in completed_keys]
            waiting = [t for t in remaining if t["type"] == "eval" and not os.path.isdir(t["checkpoint_dir"])]
            if waiting:
                print(f"  ⏳ Waiting for {len(waiting)} checkpoints...")
            else:
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
        if t["type"] == "train":
            fname = f"{t['name']}_seed{t['seed']}.json"
            fpath = os.path.join(OUT_DIR, fname)
            if os.path.isfile(fpath):
                try:
                    with open(fpath) as f:
                        d = json.load(f)
                    print(f"  {t['desc']:60s} → {d.get('ppl_before', '?'):.1f} → {d.get('ppl_after', '?'):.2f}")
                except:
                    pass
        else:
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
    parser = argparse.ArgumentParser(description="HAT Fresh D2D Cross-Instance Pipeline (Codex P1)")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    if not args.resume and not args.dry_run and os.path.isfile(TASK_STATE_FILE):
        os.remove(TASK_STATE_FILE)

    run_pipeline(dry_run=args.dry_run)
