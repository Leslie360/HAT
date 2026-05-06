#!/usr/bin/env python3
"""Pythia-1B last2 experiment."""
import json, os, subprocess, sys, time

HAT_DIR = "/home/lisq753/projects/HAT/HAT"
OUT_DIR = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107"
CKPT_BASE = os.path.join(OUT_DIR, "checkpoints")
PYTHON = "/home/lisq753/miniconda3/envs/LLM/bin/python"
MODEL_PATH = "/tmp/pythia-1b-local"
NUM_GPUS = 6
POLL_INTERVAL = 15

D2D_SEEDS = [42, 123, 456, 789, 1001]
EVAL_SCENARIOS = [
    ("clean",      0.0,  0.0,  [42]),
    ("C2C",        0.0,  0.01, [42]),
    ("D2D_weak",   0.02, 0.0,  D2D_SEEDS),
    ("D2D_strong", 0.05, 0.0,  D2D_SEEDS),
    ("combined",   0.02, 0.01, D2D_SEEDS),
]

def name(): return "pythia1b_last2_v2_seed42"
def ckpt_dir(): return os.path.join(CKPT_BASE, name())
def _fmt(x):
    s = str(x)
    if "." not in s: s += ".0"
    return s
def eval_fname(sd2d, sc2c, seed):
    return "eval_%s_c2c%s_d2d%s_seed%d.json" % (name(), _fmt(sc2c), _fmt(sd2d), seed)

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
print("PYTHIA-1B LAST2 SELECTIVE KV")
print("="*60)

# Step 1: Train
need_train = not os.path.isdir(ckpt_dir())
if need_train:
    print("\nTraining Pythia-1B last2...")
    gpu_assigned = None
    for gpu in range(NUM_GPUS):
        gpu_assigned = gpu; break
    env = "CUDA_VISIBLE_DEVICES=%d " % gpu_assigned
    cmd = ("%s p3_hat_train.py --name pythia1b_last2_v2 "
           "--model_name %s "
           "--sigma_d2d 0.02 --sigma_c2c 0.01 "
           "--max_steps 500 --seed 42 "
           "--analog_layers \"14,15\"") % (PYTHON, MODEL_PATH)
    lf = os.path.join(OUT_DIR, "train_pythia1b_last2.log")
    full = "cd %s && %s nohup %s > %s 2>&1 &" % (HAT_DIR, env, cmd, lf)
    print("  [TRAIN] GPU%d" % gpu_assigned)
    subprocess.run(full, shell=True, check=False)

    # Wait for training to finish
    while True:
        if os.path.isdir(ckpt_dir()):
            # Check if training is really done (model.safetensors exists)
            if os.path.isfile(os.path.join(ckpt_dir(), "model.safetensors")):
                print("  Training done!")
                break
        time.sleep(30)

    cfg_path = os.path.join(ckpt_dir(), "hat_config.json")
    if os.path.isfile(cfg_path):
        cfg = json.load(open(cfg_path))
        if cfg.get("analog_layers") != [14,15]:
            cfg["analog_layers"] = [14,15]
            json.dump(cfg, open(cfg_path, "w"))
    else:
        json.dump({"analog_layers":[14,15],"d2d_seed":None,"n_states":256}, open(cfg_path, "w"))
else:
    print("\nCheckpoint exists!")

# Step 2: Eval
evals = []
if os.path.isdir(ckpt_dir()):
    for l,sd2d,sc2c,seeds in EVAL_SCENARIOS:
        for seed in seeds:
            if os.path.isfile(os.path.join(OUT_DIR, eval_fname(sd2d,sc2c,seed))): continue
            evals.append((l,sd2d,sc2c,seed))

print("\nEval tasks: %d" % len(evals))
if evals:
    active = {}
    while evals or active:
        finished = []
        for gpu,atup in list(active.items()):
            l,sd2d,sc2c,seed = atup
            if os.path.isfile(os.path.join(OUT_DIR, eval_fname(sd2d,sc2c,seed))):
                finished.append((gpu,atup))
                print("  [DONE] GPU%d: %s seed=%d" % (gpu,l,seed))
        for gpu,_ in finished: del active[gpu]
        free = [g for g in get_free_gpus() if g not in active]
        for gpu in free:
            if not evals: break
            l,sd2d,sc2c,seed = evals.pop(0)
            cmd = ("%s p3_hat_eval.py --checkpoint_dir %s --n_states 256 "
                   "--sigma_d2d %.4f --sigma_c2c %.4f --max_length 512 "
                   "--output_dir %s --d2d-seed %d") % (
                PYTHON, ckpt_dir(), sd2d, sc2c, OUT_DIR, seed)
            full = "cd %s && CUDA_VISIBLE_DEVICES=%d HF_HUB_OFFLINE=1 nohup %s > %s 2>&1 &" % (
                HAT_DIR, gpu, cmd, os.path.join(OUT_DIR, "eval_pythia1b_seed%d.log"%seed))
            print("  [LAUNCH] GPU%d: %s seed=%d" % (gpu,l,seed))
            subprocess.run(full,shell=True,check=False)
            active[gpu] = (l,sd2d,sc2c,seed); time.sleep(2)
        time.sleep(POLL_INTERVAL*2 if not active else POLL_INTERVAL)

# Report
print("\n"+"="*60)
print("PYTHIA-1B LAST2 RESULTS")
print("="*60)
print("%-14s %-8s %-8s %-8s %-8s %-8s"%("Model","clean","C2C","D2Dw","D2Ds","comb"))
print("-"*70)
vals = []
for l,sd2d,sc2c,seeds in EVAL_SCENARIOS:
    ppls=[]
    for seed in seeds:
        f=os.path.join(OUT_DIR, eval_fname(sd2d,sc2c,seed))
        if os.path.isfile(f):
            try: ppls.append(json.load(open(f)).get("ppl",-1))
            except: pass
    vals.append("%.1f"%(sum(ppls)/len(ppls)) if ppls else "?")
print("%-8s (1B last2)"%("1B"))
print("  %-11s %-8s %-8s %-8s %-8s %-8s"%("",vals[0],vals[1],vals[2],vals[3],vals[4]))

print("\nReference: 410M last2 (σd=0.02/σc=0.01):")
print("  %-11s %-8s %-8s %-8s %-8s %-8s"%("","18.1","18.4","18.6","19.0","18.6"))
print("Reference: 410M full-layer combined:")
print("  %-11s %-8s %-8s %-8s %-8s %-8s"%("","20.8","22.5","26.0","59.1","27.0"))
