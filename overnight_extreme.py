#!/usr/bin/env python3
"""Extreme sigma + 410M last1 ablation."""
import json, os, subprocess, time

HAT_DIR = "/home/lisq753/projects/HAT/HAT"
OUT_DIR = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107"
CKPT_BASE = os.path.join(OUT_DIR, "checkpoints")
PYTHON = "/home/lisq753/miniconda3/envs/LLM/bin/python"
MODEL_1B = "/tmp/pythia-1b-local"
MODEL_410M = "EleutherAI/pythia-410m-deduped"
NUM_GPUS = 8
POLL_INTERVAL = 15

# Group A: Pythia-1B last1 extreme sigma (GPUs 0-3)
GROUP_A = [
    ("p1b_last1_e10", MODEL_1B,   0.10, 0.01, [15], 42, "1B last1 sigma_d=0.10"),
    ("p1b_last1_e15", MODEL_1B,   0.15, 0.01, [15], 42, "1B last1 sigma_d=0.15"),
    ("p1b_last1_e20", MODEL_1B,   0.20, 0.01, [15], 42, "1B last1 sigma_d=0.20"),
]

# Group B: 410M last1/last4 ablation (GPUs 4-7)
GROUP_B = [
    ("410m_last1",    MODEL_410M, 0.02, 0.01, [23],     42, "410M last1"),
    ("410m_last4",    MODEL_410M, 0.02, 0.01, [20,21,22,23], 42, "410M last4"),
    ("p1b_last1_d2d", MODEL_1B,   0.02, 0.00, [15],     42, "1B last1 D2D-only"),
    ("p1b_last1_c2c", MODEL_1B,   0.00, 0.01, [15],     42, "1B last1 C2C-only"),
]

ALL = GROUP_A + GROUP_B

D2D_SEEDS = [42, 123, 456, 789, 1001]
EVAL_SCENARIOS = [
    ("clean",      0.0,  0.0,  [42]),
    ("C2C",        0.0,  0.01, [42]),
    ("D2D_weak",   0.02, 0.0,  D2D_SEEDS),
    ("D2D_strong", 0.05, 0.0,  D2D_SEEDS),
    ("combined",   0.02, 0.01, D2D_SEEDS),
]

def name(tag, seed): return "%s_v2_seed%d" % (tag, seed)
def ckpt_dir(tag, seed): return os.path.join(CKPT_BASE, name(tag, seed))
def _fmt(x):
    s = str(x)
    if "." not in s: s += ".0"
    return s
def eval_fname(bn, sd2d, sc2c, seed):
    return "eval_%s_c2c%s_d2d%s_seed%d.json" % (bn, _fmt(sc2c), _fmt(sd2d), seed)

def get_free_gpus(allowed=None):
    if allowed is None: allowed = list(range(NUM_GPUS))
    try:
        r = subprocess.run(["nvidia-smi","--query-gpu=index,utilization.gpu",
            "--format=csv,noheader,nounits"], capture_output=True, text=True, timeout=10)
        free = []
        for line in r.stdout.strip().split("\n"):
            if not line.strip(): continue
            i,u = line.split(",")
            if int(u.strip()) < 30 and int(i.strip()) in allowed:
                free.append(int(i.strip()))
        return free
    except: return []

print("="*70)
print("EXTREME SIGMA + 410M LAST1 ABLATION")
print("="*70)
for t,mp,d2d,c2c,ly,sd,desc in ALL:
    print("  %-18s %s" % (t, desc))

# Train
pending = [(t,mp,d2d,c2c,ly,sd,desc) for t,mp,d2d,c2c,ly,sd,desc in ALL if not os.path.isdir(ckpt_dir(t,sd))]
if pending:
    print("\n=== TRAINING %d models ===" % len(pending))
    active = {}
    group_a_tags = {x[0] for x in GROUP_A}
    group_b_tags = {x[0] for x in GROUP_B}

    def launch(item, gpu):
        t, mp, d2d, c2c, ly, sd, desc = item
        layers_str = ",".join(str(x) for x in ly)
        max_steps = 500
        cmd = ("%s p3_hat_train.py --name %s_v2 "
               "--model_name %s "
               "--sigma_d2d %.4f --sigma_c2c %.4f "
               "--max_steps %d --seed %d --analog_layers \"%s\"") % (
            PYTHON, t, mp, d2d, c2c, max_steps, sd, layers_str)
        lf = os.path.join(OUT_DIR, "train_%s.log" % t)
        full = "cd %s && CUDA_VISIBLE_DEVICES=%d nohup %s > %s 2>&1 &" % (HAT_DIR, gpu, cmd, lf)
        print("  [TRAIN] GPU%d: %s (%s)" % (gpu, t, desc))
        subprocess.run(full, shell=True, check=False)
        active[gpu] = (t, sd)
        time.sleep(3)

    # Initial launch
    for item in pending:
        t, mp, d2d, c2c, ly, sd, desc = item
        allowed = [0,1,2,3] if t in group_a_tags else [4,5,6,7]
        free = get_free_gpus(allowed=allowed)
        for gpu in free:
            if gpu not in active:
                launch(item, gpu)
                break

    while True:
        done = sum(1 for t,_,_,_,_,sd,_ in ALL if os.path.isdir(ckpt_dir(t,sd)))
        print("  Training: %d/%d done" % (done, len(ALL)))
        if done == len(ALL): break
        finished = [g for g, (t,sd) in active.items() if os.path.isdir(ckpt_dir(t,sd))]
        for g in finished: del active[g]
        for item in pending:
            t, mp, d2d, c2c, ly, sd, desc = item
            if os.path.isdir(ckpt_dir(t, sd)): continue
            already = any(active.get(g) == (t, sd) for g in active)
            if already: continue
            allowed = [0,1,2,3] if t in group_a_tags else [4,5,6,7]
            free = get_free_gpus(allowed=allowed)
            for gpu in free:
                if gpu not in active:
                    launch(item, gpu)
                    break
        time.sleep(30)

    for t,_,_,_,ly,sd,_ in ALL:
        cfg = os.path.join(ckpt_dir(t,sd), "hat_config.json")
        if not os.path.isfile(cfg):
            json.dump({"analog_layers":ly,"d2d_seed":None,"n_states":256}, open(cfg,"w"))

print("\nAll trained!")

# Eval
evals = []
for t,mp,d2d,c2c,ly,sd,desc in ALL:
    bn = name(t, sd)
    ck = ckpt_dir(t, sd)
    if not os.path.isdir(ck): continue
    for l, sd2d, sc2c, seeds in EVAL_SCENARIOS:
        for seed in seeds:
            if os.path.isfile(os.path.join(OUT_DIR, eval_fname(bn, sd2d, sc2c, seed))): continue
            evals.append((ck, bn, t, l, sd2d, sc2c, seed))

print("\n=== EVAL %d tasks ===" % len(evals))
if evals:
    active = {}
    while evals or active:
        finished = []
        for gpu,atup in list(active.items()):
            ck,bn,t,l,sd2d,sc2c,seed = atup
            if os.path.isfile(os.path.join(OUT_DIR, eval_fname(bn,sd2d,sc2c,seed))):
                finished.append((gpu,atup))
                print("  [DONE] GPU%d: %s %s seed=%d" % (gpu,t,l,seed))
        for gpu,_ in finished: del active[gpu]
        free = [g for g in get_free_gpus() if g not in active]
        for gpu in free:
            if not evals: break
            ck,bn,t,l,sd2d,sc2c,seed = evals.pop(0)
            cmd = ("%s p3_hat_eval.py --checkpoint_dir %s --n_states 256 "
                   "--sigma_d2d %.4f --sigma_c2c %.4f --max_length 512 "
                   "--output_dir %s --d2d-seed %d") % (PYTHON,ck,sd2d,sc2c,OUT_DIR,seed)
            full = "cd %s && CUDA_VISIBLE_DEVICES=%d HF_HUB_OFFLINE=1 nohup %s > %s 2>&1 &" % (
                HAT_DIR,gpu,cmd,os.path.join(OUT_DIR,"eval_%s_%s_seed%d.log"%(t,l,seed)))
            print("  [LAUNCH] GPU%d: %s %s seed=%d"%(gpu,t,l,seed))
            subprocess.run(full,shell=True,check=False)
            active[gpu] = (ck,bn,t,l,sd2d,sc2c,seed); time.sleep(2)
        time.sleep(POLL_INTERVAL*2 if not active else POLL_INTERVAL)

# Results
print("\n" + "="*70)
print("RESULTS")
print("="*70)
print("%-18s %-8s %-8s %-8s %-8s %-8s" % ("Model","clean","C2C","D2Dw","D2Ds","comb"))
print("-"*70)
for t,mp,d2d,c2c,ly,sd,desc in ALL:
    bn = name(t, sd)
    vals = []
    for l,sd2d,sc2c,seeds in EVAL_SCENARIOS:
        ppls = []
        for seed in seeds:
            f = os.path.join(OUT_DIR, eval_fname(bn,sd2d,sc2c,seed))
            if os.path.isfile(f):
                try: ppls.append(json.load(open(f)).get("ppl",-1))
                except: pass
        vals.append("%.1f"%(sum(ppls)/len(ppls)) if ppls else "?")
    print("%-12s %s" % (t, desc))
    print("  %-11s %-8s %-8s %-8s %-8s %-8s"%("",vals[0],vals[1],vals[2],vals[3],vals[4]))

print("\nReferences:")
print("  410M last2 baseline: 18.1  18.4  18.6  19.0  18.6")
print("  1B last1 baseline:   13.9  13.9  13.9  14.1  13.9")
print("  1B last2 baseline:   13.9  14.0  14.0  14.5  14.1")
