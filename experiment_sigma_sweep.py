#!/usr/bin/env python3
"""
Direction 1: Sigma ratio sweep for combined training.

Current combined: sigma_d2d=0.02, sigma_c2c=0.01 → D2D_strong=71.9 (vs D2D-only 62.9)
Hypothesis: the sigma ratio matters. Sweep 5 ratios to find optimal.

Train 5 combined models (all-layer, 500 steps, seed=42) then eval each.
"""
import argparse
import json
import os
import subprocess
import sys
import time

HAT_DIR = "/home/lisq753/projects/HAT/HAT"
OUT_DIR = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107"
CKPT_BASE = os.path.join(OUT_DIR, "checkpoints")
PYTHON = "/home/lisq753/miniconda3/envs/LLM/bin/python"
NUM_GPUS = 4
POLL_INTERVAL = 30

SWEEP = [
    ("d2d02_c2c005", 0.02, 0.005, "less C2C"),
    ("d2d02_c2c01",  0.02, 0.01,  "current baseline"),
    ("d2d02_c2c02",  0.02, 0.02,  "more C2C"),
    ("d2d01_c2c01",  0.01, 0.01,  "less D2D"),
    ("d2d03_c2c01",  0.03, 0.01,  "more D2D"),
]

D2D_SEEDS = [42, 123, 456, 789, 1001]
EVAL_SCENARIOS = [
    ("clean",      0.0,  0.0,  [42]),
    ("C2C",        0.0,  0.01, [42]),
    ("D2D_weak",   0.02, 0.0,  D2D_SEEDS),
    ("D2D_strong", 0.05, 0.0,  D2D_SEEDS),
    ("combined",   0.02, 0.01, D2D_SEEDS),
]


def name(suffix):
    return "hat_combined_sweep_%s_v2_seed42" % suffix


def ckpt_dir(suffix):
    return os.path.join(CKPT_BASE, name(suffix))


def _fmt(x):
    s = str(x)
    if "." not in s: s += ".0"
    return s


def eval_fname(ckpt_basename, sd2d, sc2c, seed):
    return "eval_%s_c2c%s_d2d%s_seed%d.json" % (ckpt_basename, _fmt(sc2c), _fmt(sd2d), seed)


def all_tasks_done():
    for tag, d2d, c2c, _ in SWEEP:
        bn = name(tag)
        for _, sd2d, sc2c, seeds in EVAL_SCENARIOS:
            for seed in seeds:
                if not os.path.isfile(os.path.join(OUT_DIR, eval_fname(bn, sd2d, sc2c, seed))):
                    return False
    return True


def train_cmds(gpu_offset=0):
    cmds = []
    for i, (tag, d2d, c2c, desc) in enumerate(SWEEP):
        gpu = (i + gpu_offset) % NUM_GPUS
        ckpt = ckpt_dir(tag)
        if os.path.isdir(ckpt):
            print("  [SKIP] %s (checkpoint exists)" % tag)
            continue
        env = "CUDA_VISIBLE_DEVICES=%d " % gpu
        cmd = (
            "%s p3_hat_train.py "
            "--name combined_sweep_%s_v2 "
            "--sigma_d2d %.4f "
            "--sigma_c2c %.4f "
            "--max_steps 500 "
            "--seed 42"
        ) % (PYTHON, tag, d2d, c2c)
        lf = os.path.join(OUT_DIR, "train_sweep_%s.log" % tag)
        cmds.append((gpu, tag, "cd %s && %s nohup %s > %s 2>&1 &" % (HAT_DIR, env, cmd, lf)))
    return cmds


def eval_cmds(gpu_offset=0):
    cmds = []
    for tag, _, _, _ in SWEEP:
        bn = name(tag)
        ckpt = ckpt_dir(tag)
        if not os.path.isdir(ckpt):
            continue
        for l, sd2d, sc2c, seeds in EVAL_SCENARIOS:
            for seed in seeds:
                if os.path.isfile(os.path.join(OUT_DIR, eval_fname(bn, sd2d, sc2c, seed))):
                    continue
                env = "CUDA_VISIBLE_DEVICES=%d " % ((len(cmds) + gpu_offset) % NUM_GPUS)
                env += "HF_HUB_OFFLINE=1 "
                cmd = (
                    "%s p3_hat_eval.py "
                    "--checkpoint_dir %s "
                    "--n_states 256 "
                    "--sigma_d2d %.4f "
                    "--sigma_c2c %.4f "
                    "--max_length 512 "
                    "--output_dir %s "
                    "--d2d-seed %d"
                ) % (PYTHON, ckpt, sd2d, sc2c, OUT_DIR, seed)
                cmds.append((cmd, tag, l, seed))
    return cmds


def get_free_gpus(allowed=[0,1,2,3]):
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=index,utilization.gpu",
             "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10)
        free = []
        for line in result.stdout.strip().split("\n"):
            if not line.strip(): continue
            idx_s, util_s = line.split(",")
            idx, util = int(idx_s.strip()), int(util_s.strip())
            if util < 30 and idx in allowed:
                free.append(idx)
        return free
    except:
        return []


print("=" * 60)
print("DIRECTION 1: COMBINED SIGMA RATIO SWEEP")
print("=" * 60)
print("\nSweep configs:")
for tag, d2d, c2c, desc in SWEEP:
    print("  %-15s sigma_d2d=%.2f sigma_c2c=%.2f (%s)" % (tag, d2d, c2c, desc))

# Step 1: Train
print("\n" + "-" * 60)
print("STEP 1: Training %d models" % len(SWEEP))
print("-" * 60)

pending_train = [(tag, d2d, c2c, desc) for tag, d2d, c2c, desc in SWEEP if not os.path.isdir(ckpt_dir(tag))]
if pending_train:
    print("Need to train: %s" % [t[0] for t in pending_train])
    # Launch one per GPU, sequentially per GPU
    launched = set()
    for tag, d2d, c2c, desc in pending_train:
        for gpu in range(NUM_GPUS):
            if gpu not in launched:
                env = "CUDA_VISIBLE_DEVICES=%d " % gpu
                cmd = (
                    "%s p3_hat_train.py "
                    "--name combined_sweep_%s_v2 "
                    "--sigma_d2d %.4f "
                    "--sigma_c2c %.4f "
                    "--max_steps 500 "
                    "--seed 42"
                ) % (PYTHON, tag, d2d, c2c)
                lf = os.path.join(OUT_DIR, "train_sweep_%s.log" % tag)
                full_cmd = "cd %s && %s nohup %s > %s 2>&1 &" % (HAT_DIR, env, cmd, lf)
                print("  [TRAIN] GPU%d: %s (%s)" % (gpu, tag, desc))
                subprocess.run(full_cmd, shell=True, check=False)
                launched.add(gpu)
                time.sleep(3)
                break

    # Wait for training to finish (check checkpoints appear)
    while True:
        done = sum(1 for t, _, _, _ in SWEEP if os.path.isdir(ckpt_dir(t)))
        print("  Training: %d/%d done" % (done, len(SWEEP)))
        if done == len(SWEEP):
            break
        time.sleep(30)

print("All models trained!")

# Step 2: Verify hat_config.json
print("\n" + "-" * 60)
print("STEP 1.5: Ensure hat_config.json has correct analog_layers")
print("-" * 60)
for tag, _, _, _ in SWEEP:
    ckpt = ckpt_dir(tag)
    cfg_path = os.path.join(ckpt, "hat_config.json")
    if os.path.isfile(cfg_path):
        al = json.load(open(cfg_path)).get("analog_layers", "?")
        print("  %s: analog_layers=%s" % (tag, al))
    else:
        # Training script should have saved it, but just in case
        with open(cfg_path, "w") as f:
            json.dump({"analog_layers": list(range(24)), "d2d_seed": None, "n_states": 256}, f)
        print("  %s: CREATED hat_config.json" % tag)

# Step 3: Eval
print("\n" + "-" * 60)
print("STEP 2: Evaluate all sweep models")
print("-" * 60)

pending = eval_cmds()
print("%d eval tasks total" % len(pending))

if pending:
    active = {}
    while pending or active:
        finished = []
        for gpu, atup in list(active.items()):
            cmd, tag, l, seed = atup
            bn = name(tag)
            for _, sd2d, sc2c, seeds in EVAL_SCENARIOS:
                for s in seeds:
                    if s == seed:
                        fname = eval_fname(bn, sd2d, sc2c, seed)
                        break
            if os.path.isfile(os.path.join(OUT_DIR, fname)):
                finished.append((gpu, atup))
                print("  [DONE] GPU%d: %s %s seed=%d" % (gpu, tag, l, seed))

        for gpu, _ in finished:
            del active[gpu]

        free = get_free_gpus()
        free = [g for g in free if g not in active]

        for gpu in free:
            if not pending:
                break
            cmd, tag, l, seed = pending.pop(0)
            env = "CUDA_VISIBLE_DEVICES=%d " % gpu
            env += "HF_HUB_OFFLINE=1 "
            full = "cd %s && %s nohup %s > %s 2>&1 &" % (HAT_DIR, env, cmd,
                os.path.join(OUT_DIR, "eval_sweep_%s_seed%d.log" % (tag, seed)))
            print("  [LAUNCH] GPU%d: %s %s seed=%d" % (gpu, tag, l, seed))
            subprocess.run(full, shell=True, check=False)
            active[gpu] = (cmd, tag, l, seed)
            time.sleep(2)

        if not active:
            time.sleep(POLL_INTERVAL * 2)
        else:
            time.sleep(POLL_INTERVAL)

# Step 4: Report
print("\n" + "=" * 60)
print("SWEEP RESULTS")
print("=" * 60)

print("")
print("%-20s %-10s %-10s %-10s %-10s %-10s" % ("Model", "clean", "C2C", "D2Dw", "D2Ds", "comb"))
print("-" * 70)
for tag, d2d, c2c, desc in SWEEP:
    bn = name(tag)
    vals = []
    for l, sd2d, sc2c, seeds in EVAL_SCENARIOS:
        ppls = []
        for seed in seeds:
            fname = eval_fname(bn, sd2d, sc2c, seed)
            fpath = os.path.join(OUT_DIR, fname)
            if os.path.isfile(fpath):
                try:
                    with open(fpath) as f:
                        ppls.append(json.load(f).get("ppl", -1))
                except: pass
        if ppls:
            vals.append("%.1f" % (sum(ppls)/len(ppls)))
        else:
            vals.append("?")
    print("%-20s sigma=%.2f/%.2f (%s)" % (tag, d2d, c2c, desc))
    print("  %-17s %-10s %-10s %-10s %-10s %-10s" % ("", vals[0], vals[1], vals[2], vals[3], vals[4]))

print("\nReference: D2D-only training (sigma_d2d=0.02):")
print("  %-17s %-10s %-10s %-10s %-10s %-10s" % ("", "20.9", "22.6", "26.3", "62.9", "27.4"))
