#!/usr/bin/env python3
"""Run eval for all 5 sigma sweep models, 4 GPUs."""
import json, os, subprocess, sys, time

OUT_DIR = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107"
CKPT_BASE = os.path.join(OUT_DIR, "checkpoints")
PYTHON = "/home/lisq753/miniconda3/envs/LLM/bin/python"
HAT_DIR = "/home/lisq753/projects/HAT/HAT"
ALLOWED_GPUS = [0, 1, 2, 3]

TAGS = ["d2d02_c2c005", "d2d02_c2c01", "d2d02_c2c02", "d2d01_c2c01", "d2d03_c2c01"]
D2D_SEEDS = [42, 123, 456, 789, 1001]
SCENARIOS = [
    ("clean",      0.0,  0.0,  [42]),
    ("C2C",        0.0,  0.01, [42]),
    ("D2D_weak",   0.02, 0.0,  D2D_SEEDS),
    ("D2D_strong", 0.05, 0.0,  D2D_SEEDS),
    ("combined",   0.02, 0.01, D2D_SEEDS),
]

def _fmt(x):
    s = str(x)
    if "." not in s: s += ".0"
    return s

def bn(tag):
    return "combined_sweep_%s_v2_seed42" % tag

def eval_fname(tag, sd2d, sc2c, seed):
    return "eval_%s_c2c%s_d2d%s_seed%d.json" % (bn(tag), _fmt(sc2c), _fmt(sd2d), seed)

def ckpt_dir(tag):
    return os.path.join(CKPT_BASE, bn(tag))

def get_free():
    try:
        r = subprocess.run(["nvidia-smi", "--query-gpu=index,utilization.gpu",
            "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=10)
        free = []
        for line in r.stdout.strip().split("\n"):
            if not line.strip(): continue
            i, u = line.split(",")
            idx, util = int(i.strip()), int(u.strip())
            if util < 30 and idx in ALLOWED_GPUS:
                free.append(idx)
        return free
    except:
        return []

# Build task list
tasks = []
for tag in TAGS:
    ckpt = ckpt_dir(tag)
    if not os.path.isdir(ckpt):
        print("SKIP %s: checkpoint not found" % tag)
        continue
    for l, sd2d, sc2c, seeds in SCENARIOS:
        for seed in seeds:
            f = eval_fname(tag, sd2d, sc2c, seed)
            if os.path.isfile(os.path.join(OUT_DIR, f)):
                continue
            tasks.append((tag, l, sd2d, sc2c, seed))

print("Eval tasks: %d" % len(tasks))
if not tasks:
    print("All done!")
    sys.exit(0)

active = {}
while tasks or active:
    finished = []
    for gpu, (tag, l, sd2d, sc2c, seed) in list(active.items()):
        if os.path.isfile(os.path.join(OUT_DIR, eval_fname(tag, sd2d, sc2c, seed))):
            finished.append((gpu, tag, l, seed))
            print("  [DONE] GPU%d: %s %s seed=%d" % (gpu, tag, l, seed))
    for gpu, _, _, _ in finished:
        del active[gpu]

    free = [g for g in get_free() if g not in active]
    for gpu in free:
        if not tasks: break
        tag, l, sd2d, sc2c, seed = tasks.pop(0)
        env = "CUDA_VISIBLE_DEVICES=%d HF_HUB_OFFLINE=1 " % gpu
        cmd = ("%s p3_hat_eval.py --checkpoint_dir %s --n_states 256 "
               "--sigma_d2d %.4f --sigma_c2c %.4f --max_length 512 "
               "--output_dir %s --d2d-seed %d") % (
            PYTHON, ckpt_dir(tag), sd2d, sc2c, OUT_DIR, seed)
        full = "cd %s && %s nohup %s > %s 2>&1 &" % (HAT_DIR, env, cmd,
            os.path.join(OUT_DIR, "eval_sweep_run.log"))
        print("  [LAUNCH] GPU%d: %s %s seed=%d" % (gpu, tag, l, seed))
        subprocess.run(full, shell=True, check=False)
        active[gpu] = (tag, l, sd2d, sc2c, seed)
        time.sleep(2)

    if not active:
        time.sleep(30)
    else:
        time.sleep(15)

print("\n=== RESULTS ===")
print("%-20s %-8s %-8s %-8s %-8s %-8s" % ("Model", "clean", "C2C", "D2Dw", "D2Ds", "comb"))
print("-" * 70)
for tag in TAGS:
    vals = []
    for l, sd2d, sc2c, seeds in SCENARIOS:
        ppls = []
        for seed in seeds:
            f = eval_fname(tag, sd2d, sc2c, seed)
            fp = os.path.join(OUT_DIR, f)
            if os.path.isfile(fp):
                try:
                    ppls.append(json.load(open(fp)).get("ppl", -1))
                except: pass
        vals.append("%.1f" % (sum(ppls)/len(ppls)) if ppls else "?")
    print("%-20s %-8s %-8s %-8s %-8s %-8s" % (tag, vals[0], vals[1], vals[2], vals[3], vals[4]))
