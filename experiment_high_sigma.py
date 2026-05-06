#!/usr/bin/env python3
"""
Direction 3: High-noise selective KV training.

Train last2 models at increasingly aggressive noise levels to find the
operating boundary of selective KV robustness.

Questions:
- Does selective KV (last2) remain robust at 5x, 8x, 10x noise?
- Where is the breaking point?
"""
import json
import os
import subprocess
import sys
import time

HAT_DIR = "/home/lisq753/projects/HAT/HAT"
OUT_DIR = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107"
CKPT_BASE = os.path.join(OUT_DIR, "checkpoints")
PYTHON = "/home/lisq753/miniconda3/envs/LLM/bin/python"
NUM_GPUS = 6
POLL_INTERVAL = 15

# Train last2 ([22,23]) at higher sigma levels
CONFIGS = [
    ("d2d05_c2c01",  0.05, 0.01, "last2", [22, 23], "high D2D"),
    ("d2d08_c2c01",  0.08, 0.01, "last2", [22, 23], "very high D2D"),
    ("d2d10_c2c01",  0.10, 0.01, "last2", [22, 23], "extreme D2D"),
    ("d2d05_c2c02",  0.05, 0.02, "last2", [22, 23], "both high"),
]

D2D_SEEDS = [42, 123, 456, 789, 1001]
EVAL_SCENARIOS = [
    ("clean",      0.0,  0.0,  [42]),
    ("C2C",        0.0,  0.01, [42]),
    ("D2D_weak",   0.02, 0.0,  D2D_SEEDS),
    ("D2D_strong", 0.05, 0.0,  D2D_SEEDS),
    ("combined",   0.02, 0.01, D2D_SEEDS),
]

def name(tag):
    return "highsigma_%s_v2_seed42" % tag

def ckpt_dir(tag):
    return os.path.join(CKPT_BASE, name(tag))

def _fmt(x):
    s = str(x)
    if "." not in s: s += ".0"
    return s

def eval_fname(bn, sd2d, sc2c, seed):
    return "eval_%s_c2c%s_d2d%s_seed%d.json" % (bn, _fmt(sc2c), _fmt(sd2d), seed)

def get_free_gpus(allowed=None):
    if allowed is None:
        allowed = list(range(NUM_GPUS))
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
print("DIRECTION 3: HIGH-NOISE SELECTIVE KV TRAINING")
print("=" * 60)
print("\nConfigs:")
for tag, d2d, c2c, sel, layers, desc in CONFIGS:
    print("  %-14s sigma_d2d=%.2f sigma_c2c=%.2f layers=%s (%s)" % (tag, d2d, c2c, str(layers), desc))

# Step 1: Train
print("\n" + "-" * 60)
print("STEP 1: Training")
print("-" * 60)

pending_train = [(tag, d2d, c2c, sel, layers, desc) for tag, d2d, c2c, sel, layers, desc in CONFIGS if not os.path.isdir(ckpt_dir(tag))]
if not pending_train:
    print("All checkpoints exist!")
else:
    print("Need to train: %s" % [t[0] for t in pending_train])
    launched = set()
    for tag, d2d, c2c, sel, layers, desc in pending_train:
        for gpu in range(NUM_GPUS):
            if gpu not in launched:
                env = "CUDA_VISIBLE_DEVICES=%d " % gpu
                layers_str = ",".join(str(x) for x in layers)
                cmd = (
                    "%s p3_hat_train.py "
                    "--name highsigma_%s_v2 "
                    "--sigma_d2d %.4f --sigma_c2c %.4f "
                    "--max_steps 500 --seed 42 "
                    "--analog_layers \"%s\""
                ) % (PYTHON, tag, d2d, c2c, layers_str)
                lf = os.path.join(OUT_DIR, "train_highsigma_%s.log" % tag)
                full = "cd %s && %s nohup %s > %s 2>&1 &" % (HAT_DIR, env, cmd, lf)
                print("  [TRAIN] GPU%d: %s (sigma=%.2f/%.2f, %s)" % (gpu, tag, d2d, c2c, desc))
                subprocess.run(full, shell=True, check=False)
                launched.add(gpu)
                time.sleep(3)
                break

    while True:
        done = sum(1 for t, _, _, _, _, _ in CONFIGS if os.path.isdir(ckpt_dir(t)))
        print("  Training: %d/%d done" % (done, len(CONFIGS)))
        if done == len(CONFIGS): break
        time.sleep(30)

    for tag, d2d, c2c, sel, layers, desc in CONFIGS:
        cfg_path = os.path.join(ckpt_dir(tag), "hat_config.json")
        if not os.path.isfile(cfg_path):
            json.dump({"analog_layers": layers, "d2d_seed": None, "n_states": 256}, open(cfg_path, "w"))

print("All models trained!")

# Step 2: Eval
print("\n" + "-" * 60)
print("STEP 2: Evaluate")
print("-" * 60)

eval_tasks = []
for tag, d2d, c2c, sel, layers, desc in CONFIGS:
    bn = name(tag)
    ckpt = ckpt_dir(tag)
    if not os.path.isdir(ckpt): continue
    for l, sd2d, sc2c, seeds in EVAL_SCENARIOS:
        for seed in seeds:
            if os.path.isfile(os.path.join(OUT_DIR, eval_fname(bn, sd2d, sc2c, seed))):
                continue
            eval_tasks.append((ckpt, bn, tag, l, sd2d, sc2c, seed))

print("%d eval tasks" % len(eval_tasks))
if eval_tasks:
    active = {}
    while eval_tasks or active:
        finished = []
        for gpu, atup in list(active.items()):
            ckpt, bn, tag, l, sd2d, sc2c, seed = atup
            if os.path.isfile(os.path.join(OUT_DIR, eval_fname(bn, sd2d, sc2c, seed))):
                finished.append((gpu, atup))
                print("  [DONE] GPU%d: %s %s seed=%d" % (gpu, tag, l, seed))
        for gpu, _ in finished: del active[gpu]

        free = get_free_gpus()
        free = [g for g in free if g not in active]

        for gpu in free:
            if not eval_tasks: break
            ckpt, bn, tag, l, sd2d, sc2c, seed = eval_tasks.pop(0)
            env = "CUDA_VISIBLE_DEVICES=%d " % gpu
            env += "HF_HUB_OFFLINE=1 "
            cmd = ("%s p3_hat_eval.py --checkpoint_dir %s --n_states 256 "
                   "--sigma_d2d %.4f --sigma_c2c %.4f --max_length 512 "
                   "--output_dir %s --d2d-seed %d") % (PYTHON, ckpt, sd2d, sc2c, OUT_DIR, seed)
            full = "cd %s && %s nohup %s > %s 2>&1 &" % (HAT_DIR, env, cmd,
                os.path.join(OUT_DIR, "eval_highsigma_%s_seed%d.log" % (tag, seed)))
            print("  [LAUNCH] GPU%d: %s %s seed=%d" % (gpu, tag, l, seed))
            subprocess.run(full, shell=True, check=False)
            active[gpu] = (ckpt, bn, tag, l, sd2d, sc2c, seed)
            time.sleep(2)

        if not active: time.sleep(POLL_INTERVAL * 2)
        else: time.sleep(POLL_INTERVAL)

# Step 3: Report
print("\n" + "=" * 60)
print("HIGH-NOISE SELECTIVE KV RESULTS")
print("=" * 60)
print("")
print("%-18s %-8s %-8s %-8s %-8s %-8s" % ("Model", "clean", "C2C", "D2Dw", "D2Ds", "comb"))
print("-" * 70)
for tag, d2d, c2c, sel, layers, desc in CONFIGS:
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
        vals.append("%.1f" % (sum(ppls)/len(ppls)) if ppls else "?")
    print("%-8s (σd=%.2f/σc=%.2f)" % (tag, d2d, c2c))
    print("  %-15s %-8s %-8s %-8s %-8s %-8s" % ("", vals[0], vals[1], vals[2], vals[3], vals[4]))

# Reference: last2 at baseline sigma from Direction 2
print("\nReference (from layer ablation):")
print("  %-15s sigma=0.02/0.01" % "last2")
print("  %-15s %-8s %-8s %-8s %-8s %-8s" % ("", "18.1", "18.4", "18.6", "19.0", "18.6"))
print("  %-15s sigma=0.02/0.01 (full 24 layers)" % "all")
print("  %-15s %-8s %-8s %-8s %-8s %-8s" % ("", "20.8", "22.5", "26.0", "59.1", "27.0"))

print("\nAll results in %s" % OUT_DIR)
