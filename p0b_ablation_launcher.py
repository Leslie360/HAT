"""
P0-B Paired HAT Checkpoint Ablations launcher.

For each checkpoint (seed42, 123, 456), run:
  B1: digital (no analog patch)
  B2: analog ON, c2c=0, d2d=0
  B3: analog ON, c2c=0, d2d=0.02  (3 seeds)
  B4: analog ON, c2c=0, d2d=0.05  (3 seeds)
"""

import os
import time
import subprocess

PYTHON = "/home/lisq753/miniconda3/envs/LLM/bin/python"
EVAL_PY = "/home/lisq753/projects/HAT/HAT/p3_hat_eval.py"
EVAL_NOANALOG_PY = "/home/lisq753/projects/HAT/HAT/p3_hat_eval_noanalog.py"
OUT_DIR = "/home/lisq753/projects/HAT/HAT/deliverable/results_v3/p0b_ablation"
CKPT_BASE = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints"

os.makedirs(OUT_DIR, exist_ok=True)

CHECKPOINTS = [
    ("k107_a1_last1_seed42", "k107_a1_last1_seed42"),
    ("k107_a1_last1_seed123", "k107_a1_last1_seed123"),
    ("k107_a1_last1_seed456", "k107_a1_last1_seed456"),
]

EVAL_JOBS = []
for ckpt_name, ckpt_dir in CHECKPOINTS:
    ckpt_path = os.path.join(CKPT_BASE, ckpt_dir)
    # B1: digital no-analog
    EVAL_JOBS.append((ckpt_name, "B1", ckpt_path, EVAL_NOANALOG_PY, [
        "--max_length", "512", "--output_dir", OUT_DIR,
    ]))
    # B2: analog ON, no noise
    EVAL_JOBS.append((ckpt_name, "B2", ckpt_path, EVAL_PY, [
        "--sigma_c2c", "0.0", "--sigma_d2d", "0.0",
        "--max_length", "512", "--output_dir", OUT_DIR,
    ]))
    # B3: analog ON, D2D=0.02 (3 seeds)
    for es in [42, 456, 1001]:
        EVAL_JOBS.append((ckpt_name, "B3", ckpt_path, EVAL_PY, [
            "--sigma_c2c", "0.0", "--sigma_d2d", "0.02",
            "--max_length", "512", "--output_dir", OUT_DIR,
            "--d2d-seed", str(es),
        ]))
    # B4: analog ON, D2D=0.05 (3 seeds)
    for es in [42, 456, 1001]:
        EVAL_JOBS.append((ckpt_name, "B4", ckpt_path, EVAL_PY, [
            "--sigma_c2c", "0.0", "--sigma_d2d", "0.05",
            "--max_length", "512", "--output_dir", OUT_DIR,
            "--d2d-seed", str(es),
        ]))


def get_free_gpus(allowed=(0,1,2,3,4,5,6,7)):
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
    print(f"[P0B] Starting {len(EVAL_JOBS)} ablation eval jobs...")
    active = {}
    completed = []

    while EVAL_JOBS or active:
        done_gpus = []
        for gpu, (proc, item) in active.items():
            ret = proc.poll()
            if ret is not None:
                ckpt, mode, ckpt_path, eval_py, extra = item
                print(f"  [GPU {gpu}] DONE: {ckpt} {mode} return={ret}")
                completed.append((item, ret))
                done_gpus.append(gpu)
        for g in done_gpus:
            del active[g]

        free_gpus = get_free_gpus()
        for gpu in free_gpus:
            if gpu in active:
                continue
            if not EVAL_JOBS:
                break
            ckpt, mode, ckpt_path, eval_py, extra = EVAL_JOBS.pop(0)
            cmd = [PYTHON, eval_py, "--checkpoint_dir", ckpt_path] + extra
            print(f"  [GPU {gpu}] START: {ckpt} {mode}")
            active[gpu] = (launch(cmd, gpu), (ckpt, mode, ckpt_path, eval_py, extra))

        time.sleep(2)

    print(f"[P0B] Complete. {len(completed)} ablation eval jobs finished.")


if __name__ == "__main__":
    main()
