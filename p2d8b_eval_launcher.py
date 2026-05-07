"""
P2 Pythia-2.8B eval launcher — seed42 + seed123.
Distributes 12 eval jobs across all 8 GPUs.
"""
import os
import time
import subprocess

PYTHON = "/home/lisq753/miniconda3/envs/LLM/bin/python"
EVAL_PY = "/home/lisq753/projects/HAT/HAT/p3_hat_eval.py"
OUT_DIR = "/home/lisq753/projects/HAT/HAT/deliverable/results_v3/p2d8b_2d8b"

CKPTS = {
    "seed42": "/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints/p2d8b_last1_d2d002_seed42",
    "seed123": "/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints/p2d8b_last1_d2d002_seed123",
}

os.makedirs(OUT_DIR, exist_ok=True)

EVAL_JOBS = []
for train_tag, ckpt in CKPTS.items():
    for d2d in [0.02, 0.05]:
        for es in [42, 456, 1001]:
            EVAL_JOBS.append((train_tag, ckpt, d2d, es))


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
        if idx in allowed and util == 0 and mem < 5000:
            free.append(idx)
    return sorted(free)


def launch(cmd, gpu):
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = str(gpu)
    return subprocess.Popen(cmd, env=env)


def main():
    print(f"[P2D8B] Starting {len(EVAL_JOBS)} eval jobs...")
    active = {}
    completed = []

    while EVAL_JOBS or active:
        done_gpus = []
        for gpu, (proc, item) in active.items():
            ret = proc.poll()
            if ret is not None:
                train_tag, ckpt, d2d, es = item
                print(f"  [GPU {gpu}] EVAL DONE: {train_tag} d2d={d2d} eseed={es} return={ret}")
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
            train_tag, ckpt, d2d, es = EVAL_JOBS.pop(0)
            cmd = [
                PYTHON, EVAL_PY,
                "--checkpoint_dir", ckpt,
                "--n_states", "256",
                "--sigma_d2d", str(d2d),
                "--sigma_c2c", "0.0",
                "--max_length", "512",
                "--output_dir", OUT_DIR,
                "--d2d-seed", str(es),
            ]
            print(f"  [GPU {gpu}] EVAL START: {train_tag} d2d={d2d} eseed={es}")
            active[gpu] = (launch(cmd, gpu), (train_tag, ckpt, d2d, es))

        time.sleep(2)

    print(f"[P2D8B] Complete. {len(completed)} eval jobs finished.")


if __name__ == "__main__":
    main()
