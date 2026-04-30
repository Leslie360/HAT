#!/usr/bin/env python3
"""
HAT D2D Seed Ablation Pipeline — device-instance variation sweep.

Train D2D=0.02 and D2D=0.04 at d2d_seed ∈ {42, 123, 456, 789, 1001},
then evaluate each checkpoint at D2D ∈ {0.02, 0.04, 0.05}.

Total: 10 training + 30 eval = 40 tasks, 8 GPUs.

Usage:  python pipeline_d2d_seed.py [--dry-run] [--resume]
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


def make_train_task(name, sigma_d2d, sigma_c2c, max_steps,
                    analog_layers=None, seed=42, d2d_seed=0xD2D, desc=""):
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


# ── Phase 1: Train D2D=0.02 at 5 d2d_seeds ──
D2D_SEEDS = [42, 123, 456, 789, 1001]

phase1_train = []
for ds in D2D_SEEDS:
    name = f"hat_d2d002_500_v2_d2dseed{ds}"
    phase1_train.append(make_train_task(
        name, sigma_d2d=0.02, sigma_c2c=0.0, max_steps=500,
        seed=42, d2d_seed=ds,
        desc=f"D2D=0.02 train d2d_seed={ds}",
    ))
PHASES.append(("Phase 1: Train D2D=0.02 × 5 seeds", phase1_train))

# ── Phase 2: Train D2D=0.04 at 5 d2d_seeds ──
phase2_train = []
for ds in D2D_SEEDS:
    name = f"hat_d2d004_500_v2_d2dseed{ds}"
    phase2_train.append(make_train_task(
        name, sigma_d2d=0.04, sigma_c2c=0.0, max_steps=500,
        seed=42, d2d_seed=ds,
        desc=f"D2D=0.04 train d2d_seed={ds}",
    ))
PHASES.append(("Phase 2: Train D2D=0.04 × 5 seeds", phase2_train))

# ── Phase 3: Eval all 10 checkpoints at D2D={0.02, 0.04, 0.05} ──
EVAL_D2D_LEVELS = [0.02, 0.04, 0.05]

phase3_eval = []
for sigma in [0.02, 0.04]:
    for ds in D2D_SEEDS:
        ckpt_name = f"hat_d2d00{int(sigma*100)}_500_v2_d2dseed{ds}_seed42"
        for ed2d in EVAL_D2D_LEVELS:
            phase3_eval.append(make_eval_task(
                ckpt_name, eval_sigma_d2d=ed2d, eval_sigma_c2c=0.0,
                desc=f"Eval {ckpt_name} D2D={ed2d}",
            ))
PHASES.append(("Phase 3: Eval 10 ckpts × 3 D2D levels", phase3_eval))


# ═══════════════════════════════════════════════════════════════
# Pipeline Engine
# ═══════════════════════════════════════════════════════════════

TASK_STATE_FILE = os.path.join(OUT_DIR, ".pipeline_d2dseed_state.json")


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
        ds = task.get("d2d_seed", None)
        return f"eval:{os.path.basename(task['checkpoint_dir'])}:d2d{task['sigma_d2d']}:c2c{task['sigma_c2c']}:ds{ds}"
    return f"train:{task['name']}:seed{task['seed']}:ds{task.get('d2d_seed', 0xD2D)}"


def run_pipeline(dry_run=False, resume=False):
    sys.stdout.reconfigure(line_buffering=True)
    state = load_state() if resume else {"completed": [], "started_at": time.strftime("%Y-%m-%d %H:%M:%S")}
    completed_keys = set(state["completed"])
    total_all = sum(len(tasks) for _, tasks in PHASES)

    print("=" * 60)
    print("HAT D2D Seed Ablation Pipeline")
    print(f"D2D seeds: {D2D_SEEDS}")
    print(f"Eval D2D levels: {EVAL_D2D_LEVELS}")
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
                            print(f"  {t['desc']:50s} → PPL {d['ppl']:.2f}")
                        except:
                            pass
                else:
                    fname = f"{t['name']}_seed{t['seed']}.json"
                    fpath = os.path.join(OUT_DIR, fname)
                    if os.path.isfile(fpath):
                        try:
                            with open(fpath) as f:
                                d = json.load(f)
                            print(f"  {t['desc']:50s} → {d['ppl_before']:.1f} → {d['ppl_after']:.2f}")
                        except:
                            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HAT D2D Seed Ablation Pipeline")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    if not args.resume and not args.dry_run and os.path.isfile(TASK_STATE_FILE):
        os.remove(TASK_STATE_FILE)

    run_pipeline(dry_run=args.dry_run, resume=args.resume)
