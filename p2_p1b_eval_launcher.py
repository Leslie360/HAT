"""
P2 Pythia-1B seed123 eval launcher.
"""
import os
import time
import subprocess

PYTHON = "/home/lisq753/miniconda3/envs/LLM/bin/python"
EVAL_PY = "/home/lisq753/projects/HAT/HAT/p3_hat_eval.py"
OUT_DIR = "/home/lisq753/projects/HAT/HAT/deliverable/results_v3/p1b_1b"
CKPT = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints/p1b_last1_d2d002_seed123"

os.makedirs(OUT_DIR, exist_ok=True)

EVAL_JOBS = [
    ("d2d002", 0.0, 0.02, 42),
    ("d2d002", 0.0, 0.02, 456),
    ("d2d002", 0.0, 0.02, 1001),
    ("d2d005", 0.0, 0.05, 42),
    ("d2d005", 0.0, 0.05, 456),
    ("d2d005", 0.0, 0.05, 1001),
]


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
    print(f"[P1B-P2] Starting {len(EVAL_JOBS)} eval jobs...")
    active = {}
    completed = []

    while EVAL_JOBS or active:
        done_gpus = []
        for gpu, (proc, item) in active.items():
            ret = proc.poll()
            if ret is not None:
                tag, c2c, d2d, es = item
                print(f"  [GPU {gpu}] EVAL DONE: {tag} c2c={c2c} d2d={d2d} eseed={es} return={ret}")
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
            tag, c2c, d2d, es = EVAL_JOBS.pop(0)
            cmd = [
                PYTHON, EVAL_PY,
                "--checkpoint_dir", CKPT,
                "--n_states", "256",
                "--sigma_d2d", str(d2d),
                "--sigma_c2c", str(c2c),
                "--max_length", "512",
                "--output_dir", OUT_DIR,
                "--d2d-seed", str(es),
            ]
            print(f"  [GPU {gpu}] EVAL START: {tag} c2c={c2c} d2d={d2d} eseed={es}")
            active[gpu] = (launch(cmd, gpu), (tag, c2c, d2d, es))

        time.sleep(2)

    print(f"[P1B-P2] Complete. {len(completed)} eval jobs finished.")


if __name__ == "__main__":
    main()
