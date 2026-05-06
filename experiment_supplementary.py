#!/usr/bin/env python3
"""Supplementary experiments: D2D-only, C2C-only, multi-seed last2."""
import json, os, subprocess, sys, time

HAT_DIR = "/home/lisq753/projects/HAT/HAT"
OUT_DIR = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107"
CKPT_BASE = os.path.join(OUT_DIR, "checkpoints")
PYTHON = "/home/lisq753/miniconda3/envs/LLM/bin/python"
NUM_GPUS = 8  # GPU0 is running Pythia-1B
POLL_INTERVAL = 15

# Configs: (tag, sigma_d2d, sigma_c2c, layers, seed, description)
CONFIGS = [
    ("d2d_only_last2",  0.02, 0.00, [22, 23], 42,  "D2D-only last2"),
    ("c2c_only_last2",  0.00, 0.01, [22, 23], 42,  "C2C-only last2"),
    ("combined_last2_s123", 0.02, 0.01, [22, 23], 123, "Combined last2 seed123"),
    ("combined_last2_s456", 0.02, 0.01, [22, 23], 456, "Combined last2 seed456"),
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
    # Map tags to checkpoint names
    seed_map = {"d2d_only_last2": 42, "c2c_only_last2": 42, "combined_last2_s123": 123, "combined_last2_s456": 456}
    return "supp_%s_v2_seed%d" % (tag, seed_map.get(tag, 42))
def ckpt_dir(tag): return os.path.join(CKPT_BASE, name(tag))
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

print("="*60)
print("SUPPLEMENTARY: D2D-only / C2C-only / Multi-seed last2")
print("="*60)
for t,d2d,c2c,ly,sd,desc in CONFIGS:
    print("  %-20s σd=%.2f σc=%.2f layers=%s seed=%d (%s)" % (t,d2d,c2c,ly,sd,desc))

# Step 1: Train
pending = [(t,d2d,c2c,ly,sd,desc) for t,d2d,c2c,ly,sd,desc in CONFIGS if not os.path.isdir(ckpt_dir(t))]
if pending:
    print("\nTraining: %s" % [t[0] for t in pending])
    launched = set()
    for t,d2d,c2c,ly,sd,desc in pending:
        free = get_free_gpus(allowed=list(range(1, NUM_GPUS)))  # skip GPU0
        for gpu in free:
            if gpu in launched: continue
            layers_str = ",".join(str(x) for x in ly)
            cmd = ("%s p3_hat_train.py --name supp_%s_v2 "
                   "--sigma_d2d %.4f --sigma_c2c %.4f "
                   "--max_steps 500 --seed %d --analog_layers \"%s\"") % (
                PYTHON, t, d2d, c2c, sd, layers_str)
            lf = os.path.join(OUT_DIR, "train_supp_%s.log" % t)
            full = "cd %s && CUDA_VISIBLE_DEVICES=%d nohup %s > %s 2>&1 &" % (HAT_DIR,gpu,cmd,lf)
            print("  [TRAIN] GPU%d: %s (σd=%.2f, seed=%d)" % (gpu,t,d2d,sd))
            subprocess.run(full,shell=True,check=False)
            launched.add(gpu); time.sleep(3); break
    # Wait for all
    while True:
        done = sum(1 for t,_,_,_,_,_ in CONFIGS if os.path.isdir(ckpt_dir(t)))
        print("  Training: %d/%d" % (done,len(CONFIGS)))
        if done == len(CONFIGS): break
        time.sleep(30)
    # Fix hat_config
    for t,_,_,ly,_,_ in CONFIGS:
        cfg = os.path.join(ckpt_dir(t),"hat_config.json")
        if not os.path.isfile(cfg):
            json.dump({"analog_layers":ly,"d2d_seed":None,"n_states":256},open(cfg,"w"))

print("\nAll trained!")

# Step 2: Eval
evals = []
for t,_,_,_,_,_ in CONFIGS:
    bn = name(t)
    ck = ckpt_dir(t)
    if not os.path.isdir(ck): continue
    for l,sd2d,sc2c,seeds in EVAL_SCENARIOS:
        for seed in seeds:
            if os.path.isfile(os.path.join(OUT_DIR, eval_fname(bn,sd2d,sc2c,seed))): continue
            evals.append((ck,bn,t,l,sd2d,sc2c,seed))

print("\nEval tasks: %d" % len(evals))
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
        free = [g for g in get_free_gpus() if g not in active and g != 0]
        for gpu in free:
            if not evals: break
            ck,bn,t,l,sd2d,sc2c,seed = evals.pop(0)
            cmd = ("%s p3_hat_eval.py --checkpoint_dir %s --n_states 256 "
                   "--sigma_d2d %.4f --sigma_c2c %.4f --max_length 512 "
                   "--output_dir %s --d2d-seed %d") % (PYTHON,ck,sd2d,sc2c,OUT_DIR,seed)
            full = "cd %s && CUDA_VISIBLE_DEVICES=%d HF_HUB_OFFLINE=1 nohup %s > %s 2>&1 &" % (
                HAT_DIR,gpu,cmd,os.path.join(OUT_DIR,"eval_supp_%s_seed%d.log"%(t,seed)))
            print("  [LAUNCH] GPU%d: %s %s seed=%d"%(gpu,t,l,seed))
            subprocess.run(full,shell=True,check=False)
            active[gpu] = (ck,bn,t,l,sd2d,sc2c,seed); time.sleep(2)
        time.sleep(POLL_INTERVAL*2 if not active else POLL_INTERVAL)

# Results
print("\n" + "="*60)
print("SUPPLEMENTARY RESULTS")
print("="*60)
print("%-24s %-8s %-8s %-8s %-8s %-8s"%("Model","clean","C2C","D2Dw","D2Ds","comb"))
print("-"*70)
for t,d2d,c2c,ly,sd,desc in CONFIGS:
    bn = name(t)
    vals = []
    for l,sd2d,sc2c,seeds in EVAL_SCENARIOS:
        ppls = []
        for seed in seeds:
            f = os.path.join(OUT_DIR, eval_fname(bn,sd2d,sc2c,seed))
            if os.path.isfile(f):
                try: ppls.append(json.load(open(f)).get("ppl",-1))
                except: pass
        vals.append("%.1f"%(sum(ppls)/len(ppls)) if ppls else "?")
    print("%-16s (σd=%.2f σc=%.2f s=%d)"%(t,d2d,c2c,sd))
    print("  %-11s %-8s %-8s %-8s %-8s %-8s"%("",vals[0],vals[1],vals[2],vals[3],vals[4]))

print("\nReference: Combined last2 (σd=0.02/σc=0.01 seed42):")
print("  %-11s %-8s %-8s %-8s %-8s %-8s"%("","18.1","18.4","18.6","19.0","18.6"))
