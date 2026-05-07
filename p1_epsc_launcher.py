"""
P1 EPSC Proxy Stress Eval launcher.

Evaluates k107_a1_last1_seed42 under extreme noise conditions.
If EPSC-e2 (c2c=0.10, d2d=0.10) is acceptable (<25 PPL),
repeat for seeds 123 and 456.
"""

import os
import time
import subprocess

PYTHON = "/home/lisq753/miniconda3/envs/LLM/bin/python"
EVAL_PY = "/home/lisq753/projects/HAT/HAT/p3_hat_eval.py"
OUT_DIR = "/home/lisq753/projects/HAT/HAT/deliverable/results_v3/epsc_stress"
CKPT_BASE = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints"

os.makedirs(OUT_DIR, exist_ok=True)

# Phase 1: seed42 checkpoint
CHECKPOINTS_PHASE1 = [
    ("k107_a1_last1_seed42", "k107_a1_last1_seed42"),
]

# Phase 2: if EPSC-e2 passes, add seeds 123 and 456
CHECKPOINTS_PHASE2 = [
    ("k107_a1_last1_seed123", "k107_a1_last1_seed123"),
    ("k107_a1_last1_seed456", "k107_a1_last1_seed456"),
]

EPSC_CONFIGS = [
    ("EPSC-e1", 0.05, 0.05),
    ("EPSC-e2", 0.10, 0.10),
    ("EPSC-e3", 0.15, 0.15),
    ("EPSC-e4", 0.00, 0.20),
    ("EPSC-e5", 0.01, 0.10),
]

EVAL_SEEDS = [42, 456, 1001]


def build_jobs(checkpoints):
    jobs = []
    for ckpt_name, ckpt_dir in checkpoints:
        ckpt_path = os.path.join(CKPT_BASE, ckpt_dir)
        for tag, c2c, d2d in EPSC_CONFIGS:
            for es in EVAL_SEEDS:
                jobs.append((ckpt_name, tag, c2c, d2d, ckpt_path, es))
    return jobs


def get_free_gpus(allowed=(0, 1, 2, 3, 4, 5, 6, 7)):
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=index,utilization.gpu,memory.used",
             "--format=csv,noheader,nounits"],
            text=True, timeout=10
        )
    except Exception:
        return []
    free = []
    for line in out.strip().splitlines():
        parts = [p.strip() for p in line.split(",")]
        idx, util, mem = int(parts[0]), int(parts[1]), int(parts[2])
        if idx in allowed and util == 0 and mem < 200:
            free.append(idx)
    return sorted(free)


def launch(cmd, gpu):
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = str(gpu)
    return subprocess.Popen(cmd, env=env)


def main():
    phase1_jobs = build_jobs(CHECKPOINTS_PHASE1)
    print(f"[EPSC] Phase 1: {len(phase1_jobs)} jobs on {CHECKPOINTS_PHASE1[0][0]}")
    active = {}
    completed = []

    all_jobs = phase1_jobs[:]
    phase2_inserted = False

    while all_jobs or active:
        done_gpus = []
        for gpu, (proc, item) in active.items():
            ret = proc.poll()
            if ret is not None:
                ckpt, tag, c2c, d2d, ckpt_path, es = item
                print(f"  [GPU {gpu}] DONE: {ckpt} {tag} c2c={c2c} d2d={d2d} eseed={es} return={ret}")
                completed.append((item, ret))
                done_gpus.append(gpu)
        for g in done_gpus:
            del active[g]

        # Check kill criterion after Phase 1 EPSC-e2 jobs complete
        if not phase2_inserted:
            epsc_e2_results = []
            for item, ret in completed:
                ckpt, tag, c2c, d2d, ckpt_path, es = item
                if tag == "EPSC-e2" and ckpt == "k107_a1_last1_seed42":
                    # read JSON to get PPL
                    json_name = f"eval_{ckpt}_c2c{c2c}_d2d{d2d}_rst0.0_seed{es}.json"
                    json_path = os.path.join(OUT_DIR, json_name)
                    if os.path.isfile(json_path):
                        import json
                        ppl = json.load(open(json_path)).get("ppl", 999)
                        epsc_e2_results.append(ppl)
            if len(epsc_e2_results) == 3:
                max_ppl = max(epsc_e2_results)
                print(f"[EPSC] Phase 1 EPSC-e2 max PPL = {max_ppl:.2f}")
                if max_ppl < 25:
                    phase2_jobs = build_jobs(CHECKPOINTS_PHASE2)
                    print(f"[EPSC] EPSC-e2 passed. Adding Phase 2: {len(phase2_jobs)} jobs.")
                    all_jobs.extend(phase2_jobs)
                    phase2_inserted = True
                else:
                    print(f"[EPSC] KILL: EPSC-e2 max PPL = {max_ppl:.2f} >= 25. Stopping.")
                    # flush remaining jobs
                    all_jobs = []

        free_gpus = get_free_gpus()
        for gpu in free_gpus:
            if gpu in active:
                continue
            if not all_jobs:
                break
            ckpt, tag, c2c, d2d, ckpt_path, es = all_jobs.pop(0)
            cmd = [
                PYTHON, EVAL_PY,
                "--checkpoint_dir", ckpt_path,
                "--n_states", "256",
                "--sigma_c2c", str(c2c),
                "--sigma_d2d", str(d2d),
                "--max_length", "512",
                "--output_dir", OUT_DIR,
                "--d2d-seed", str(es),
            ]
            print(f"  [GPU {gpu}] START: {ckpt} {tag} c2c={c2c} d2d={d2d} eseed={es}")
            active[gpu] = (launch(cmd, gpu), (ckpt, tag, c2c, d2d, ckpt_path, es))

        time.sleep(2)

    print(f"[EPSC] Complete. {len(completed)} eval jobs finished.")


if __name__ == "__main__":
    main()
