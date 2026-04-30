#!/usr/bin/env python3
"""
HAT Next-Batch Pipeline — Phase 5–8 auto-dispatch, 8 GPUs.

Usage:  python pipeline_next.py [--dry-run] [--resume]

Phases:
  5. Selective layer generalization eval (12 runs)
     — noise-sweep the best last1 checkpoints
  6. C2C noise sweep training (5 runs)
     — train at σ_c2c = 0.005, 0.015, 0.02, 0.025, 0.03
  7. C2C sweep generalization eval (42 runs)
     — noise-sweep each C2C checkpoint inc. re-eval of c2c001
  8. Retention probe (8 eval runs)
     — enable retention decay at multiple step times on best checkpoints
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

PHASES = []


# ── helpers ─────────────────────────────────────────────────

def make_eval_task(ckpt_name, eval_sigma_d2d, eval_sigma_c2c,
                   analog_layers=None, retention_step_time=0.0, desc=""):
    task = {
        "type": "eval",
        "checkpoint_dir": os.path.join(CKPT_DIR, ckpt_name),
        "sigma_d2d": eval_sigma_d2d,
        "sigma_c2c": eval_sigma_c2c,
        "n_states": 256,
        "max_length": 512,
        "retention_step_time": retention_step_time,
        "desc": desc or f"eval {ckpt_name} d2d={eval_sigma_d2d} c2c={eval_sigma_c2c}",
    }
    if analog_layers is not None:
        task["analog_layers"] = ",".join(str(x) for x in analog_layers)
    return task


def make_train_task(name, sigma_d2d, sigma_c2c, max_steps,
                    analog_layers=None, seed=42, desc=""):
    task = {
        "type": "train",
        "name": name,
        "n_states": 256,
        "sigma_d2d": sigma_d2d,
        "sigma_c2c": sigma_c2c,
        "max_steps": max_steps,
        "max_length": 512,
        "seed": seed,
        "desc": desc or name,
    }
    if analog_layers is not None:
        task["analog_layers"] = ",".join(str(x) for x in analog_layers)
    return task


# ── Phase 5: Selective Layer Generalization Eval (12 runs) ──

phase5_tasks = []

# 5a. Best D2D selective: last1 (PPL 18.28) → sweep 6 noise levels
for d2d in [0.00, 0.01, 0.02, 0.03, 0.04, 0.05]:
    phase5_tasks.append(make_eval_task(
        "hat_d2d002_last1_500_v2_seed42",
        eval_sigma_d2d=d2d, eval_sigma_c2c=0.0,
        analog_layers=[23],
        desc=f"D2Dlast1 eval D2D={d2d}",
    ))

# 5b. Best C2C selective: last1 (PPL 18.14) → sweep 6 noise levels
for c2c in [0.000, 0.005, 0.010, 0.015, 0.020, 0.025]:
    phase5_tasks.append(make_eval_task(
        "hat_c2c001_last1_500_v2_seed42",
        eval_sigma_d2d=0.0, eval_sigma_c2c=c2c,
        analog_layers=[23],
        desc=f"C2Clast1 eval C2C={c2c}",
    ))

PHASES.append(("Phase 5: Selective Gen Eval", phase5_tasks))


# ── Phase 6: C2C Noise Sweep Training (5 runs) ──

phase6_tasks = [
    make_train_task("hat_c2c0005_500_v2",  0.0, 0.005, 500, desc="C2C=0.005"),
    make_train_task("hat_c2c0015_500_v2",  0.0, 0.015, 500, desc="C2C=0.015"),
    make_train_task("hat_c2c002_500_v2",   0.0, 0.020, 500, desc="C2C=0.020"),
    make_train_task("hat_c2c0025_500_v2",  0.0, 0.025, 500, desc="C2C=0.025"),
    make_train_task("hat_c2c003_500_v2",   0.0, 0.030, 500, desc="C2C=0.030"),
]
PHASES.append(("Phase 6: C2C Sweep Training", phase6_tasks))


# ── Phase 7: C2C Sweep Generalization Eval (25 runs) ──

phase7_tasks = []
c2c_ckpts = [
    "hat_c2c0005_500_v2_seed42",
    "hat_c2c001_500_v2_seed42",     # existing, but re-eval for completeness
    "hat_c2c0015_500_v2_seed42",
    "hat_c2c002_500_v2_seed42",
    "hat_c2c0025_500_v2_seed42",
    "hat_c2c003_500_v2_seed42",
]
# Drop the existing one if we don't want duplicates — but re-eval ensures
# consistent comparison with same code version
for ckpt in c2c_ckpts:
    for c2c in [0.000, 0.005, 0.010, 0.015, 0.020, 0.025, 0.030]:
        # Skip self-train-level eval to stay under ~30 runs
        phase7_tasks.append(make_eval_task(
            ckpt, eval_sigma_d2d=0.0, eval_sigma_c2c=c2c,
            desc=f"{ckpt} eval C2C={c2c}",
        ))
# c2c001_seed42 already evaluated in Phase 1; skip existing to save compute
# Filter out tasks whose result file already exists
PHASES.append(("Phase 7: C2C Gen Eval", phase7_tasks))


# ── Phase 8: Retention Probe (8 eval runs) ──

phase8_tasks = []
# Best D2D=0.02 checkpoint, retention at step times 1e-3, 5e-3, 1e-2, 5e-2
for rt in [1e-3, 5e-3, 1e-2, 5e-2]:
    phase8_tasks.append(make_eval_task(
        "hat_d2d002_500_v2_seed42",
        eval_sigma_d2d=0.02, eval_sigma_c2c=0.0,
        retention_step_time=rt,
        desc=f"Retention D2D=0.02 stepTime={rt:.0e}",
    ))
    phase8_tasks.append(make_eval_task(
        "hat_c2c001_500_v2_seed42",
        eval_sigma_d2d=0.0, eval_sigma_c2c=0.01,
        retention_step_time=rt,
        desc=f"Retention C2C=0.01 stepTime={rt:.0e}",
    ))

PHASES.append(("Phase 8: Retention Probe", phase8_tasks))


# ═══════════════════════════════════════════════════════════════
# Pipeline Engine (identical to pipeline_runner.py)
# ═══════════════════════════════════════════════════════════════

TASK_STATE_FILE = os.path.join(OUT_DIR, ".pipeline_next_state.json")


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
    if task["type"] == "eval":
        ckpt_name = os.path.basename(task["checkpoint_dir"])
        fname = f"eval_{ckpt_name}_c2c{task['sigma_c2c']}_d2d{task['sigma_d2d']}.json"
        return os.path.isfile(os.path.join(OUT_DIR, fname))
    else:
        fname = f"{task['name']}_seed{task['seed']}.json"
        return os.path.isfile(os.path.join(OUT_DIR, fname))


def log_file(task):
    if task["type"] == "eval":
        ckpt_name = os.path.basename(task["checkpoint_dir"])
        return os.path.join(OUT_DIR, f"eval_{ckpt_name}_c2c{task['sigma_c2c']}_d2d{task['sigma_d2d']}.log")
    else:
        return os.path.join(OUT_DIR, f"{task['name']}_seed{task['seed']}.log")


def build_cmd(task, gpu_id):
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
            f"--retention_step_time {task.get('retention_step_time', 0.0)} "
            f"--output_dir {OUT_DIR} "
        )
        if "analog_layers" in task:
            cmd += f"--analog_layers {task['analog_layers']} "
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
        )
        if "analog_layers" in task:
            cmd += f"--analog_layers {task['analog_layers']} "

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
    if task["type"] == "eval":
        rt = task.get("retention_step_time", 0.0)
        return f"eval:{os.path.basename(task['checkpoint_dir'])}:d2d{task['sigma_d2d']}:c2c{task['sigma_c2c']}:rt{rt}"
    return f"train:{task['name']}:seed{task['seed']}"


def run_pipeline(dry_run=False, resume=False):
    sys.stdout.reconfigure(line_buffering=True)
    state = load_state() if resume else {"completed": [], "started_at": time.strftime("%Y-%m-%d %H:%M:%S")}
    completed_keys = set(state["completed"])
    total_all = sum(len(tasks) for _, tasks in PHASES)

    print("=" * 60)
    print("HAT Next-Batch Pipeline Runner")
    print(f"Started: {state['started_at']}")
    print(f"Phases: {len(PHASES)}, Total tasks: {total_all}")
    print(f"Completed already: {len(completed_keys)}")
    if dry_run:
        print("*** DRY RUN ***")
    print("=" * 60)

    for phase_name, tasks in PHASES:
        pending = [t for t in tasks if task_key(t) not in completed_keys]
        completed_phase = [t for t in tasks if task_key(t) in completed_keys]
        print(f"\n{'─' * 50}")
        print(f"{phase_name}: {len(completed_phase)}/{len(tasks)} done, {len(pending)} pending")

        if not pending:
            continue

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
                print(f"  ✅ {phase_name} complete!")
                break

            if not active:
                if all(task_key(t) in completed_keys for t in tasks):
                    break
                print("  ⏳ All tasks launched, waiting...")
                time.sleep(POLL_INTERVAL * 2)
            else:
                running_str = ", ".join(f"GPU{g}:{t['desc'][:30]}" for g, t in sorted(active.items()))
                print(f"  ⏳ Running: {len(active)}/8 — {running_str}")
                time.sleep(POLL_INTERVAL)

    if not dry_run:
        state["completed"] = list(completed_keys)
        state["finished_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        save_state(state)

    print(f"\n{'=' * 60}")
    print(f"Pipeline complete! {len(completed_keys)}/{total_all} tasks done.")
    print(f"Finished at: {state['finished_at']}")

    # Print summary
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
                        except:
                            pass
                else:
                    fname = f"{t['name']}_seed{t['seed']}.json"
                    fpath = os.path.join(OUT_DIR, fname)
                    if os.path.isfile(fpath):
                        try:
                            with open(fpath) as f:
                                d = json.load(f)
                            print(f"  {t['desc']:40s} → {d['ppl_before']:.1f} → {d['ppl_after']:.2f}")
                        except:
                            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HAT Next-Batch Pipeline Runner")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    if not args.resume and not args.dry_run and os.path.isfile(TASK_STATE_FILE):
        os.remove(TASK_STATE_FILE)

    run_pipeline(dry_run=args.dry_run, resume=args.resume)
