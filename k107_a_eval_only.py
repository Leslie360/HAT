"""
K107-A Evaluation-only launcher.
Runs evals for already-completed K107-A checkpoints.
"""

import os
import time
import subprocess

PYTHON = "/home/lisq753/miniconda3/envs/LLM/bin/python"
EVAL_PY = "/home/lisq753/projects/HAT/HAT/p3_hat_eval.py"
OUT_DIR = "/home/lisq753/projects/HAT/HAT/deliverable/results_v3/k107_a"
CKPT_BASE = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints"

os.makedirs(OUT_DIR, exist_ok=True)

TRAIN_JOBS = [
    ("k107_a1_last1", "23", 0.02, 42),
    ("k107_a1_last1", "23", 0.02, 123),
    ("k107_a1_last1", "23", 0.02, 456),
    ("k107_a2_last2", "22,23", 0.02, 42),
    ("k107_a2_last2", "22,23", 0.02, 123),
    ("k107_a2_last2", "22,23", 0.02, 456),
    ("k107_a3_all", "0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23", 0.02, 42),
]

EVAL_D2D_LEVELS = [0.02, 0.04, 0.05]
EVAL_SEEDS = [42, 123, 456, 789, 1001]


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
    eval_queue = []
    for tag, layers, sd, seed in TRAIN_JOBS:
        ckpt_dir = os.path.join(CKPT_BASE, f"{tag}_seed{seed}")
        if not os.path.isdir(ckpt_dir):
            print(f"SKIP: checkpoint not found {ckpt_dir}")
            continue
        for eval_d2d in EVAL_D2D_LEVELS:
            for eval_seed in EVAL_SEEDS:
                eval_queue.append((tag, seed, ckpt_dir, eval_d2d, eval_seed))

    print(f"[K107-A Eval] {len(eval_queue)} eval jobs queued.")
    active = {}
    completed = []

    while eval_queue or active:
        done_gpus = []
        for gpu, (proc, item) in active.items():
            ret = proc.poll()
            if ret is not None:
                tag, tseed, ckpt, eval_d2d, eval_seed = item
                print(f"  [GPU {gpu}] EVAL DONE: {tag} tseed={tseed} d2d={eval_d2d} eseed={eval_seed} return={ret}")
                completed.append((item, ret))
                done_gpus.append(gpu)
        for g in done_gpus:
            del active[g]

        free_gpus = get_free_gpus()
        for gpu in free_gpus:
            if gpu in active:
                continue
            if not eval_queue:
                break
            tag, tseed, ckpt, eval_d2d, eval_seed = eval_queue.pop(0)
            cmd = [
                PYTHON, EVAL_PY,
                "--checkpoint_dir", ckpt,
                "--n_states", "256",
                "--sigma_d2d", str(eval_d2d),
                "--sigma_c2c", "0.0",
                "--max_length", "512",
                "--output_dir", OUT_DIR,
                "--d2d-seed", str(eval_seed),
            ]
            print(f"  [GPU {gpu}] EVAL START: {tag} tseed={tseed} d2d={eval_d2d} eseed={eval_seed}")
            active[gpu] = (launch(cmd, gpu), (tag, tseed, ckpt, eval_d2d, eval_seed))

        time.sleep(2)

    print(f"[K107-A Eval] Complete. {len(completed)} eval jobs finished.")


if __name__ == "__main__":
    main()
