"""
K107-C eval re-run for checkpoints that were in wrong directory.
"""
import os
import time
import subprocess

PYTHON = "/home/lisq753/miniconda3/envs/LLM/bin/python"
EVAL_PY = "/home/lisq753/projects/HAT/HAT/p3_hat_eval.py"
OUT_DIR = "/home/lisq753/projects/HAT/HAT/deliverable/results_v3/k107_c"
CKPT_BASE = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107/checkpoints"

os.makedirs(OUT_DIR, exist_ok=True)

# (tag, n_states, ckpt_name, eval_d2d, eval_seed)
EVAL_JOBS = []
for tag, nst, ckpt_name in [
    ("k107_c_16states", 16, "k107_c_16states_seed42"),
    ("k107_c_32states", 32, "k107_c_32states_seed42"),
    ("k107_c_64states", 64, "k107_c_64states_seed42"),
    ("k107_c_128states", 128, "k107_c_128states_seed42"),
]:
    for d2d in [0.02, 0.05]:
        for es in [42, 123, 456]:
            EVAL_JOBS.append((tag, nst, ckpt_name, d2d, es))

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
    print(f"[K107-C Fix] {len(EVAL_JOBS)} eval jobs queued.")
    active = {}
    completed = []
    while EVAL_JOBS or active:
        done_gpus = []
        for gpu, (proc, item) in active.items():
            ret = proc.poll()
            if ret is not None:
                tag, nst, ckpt, d2d, es = item
                print(f"  [GPU {gpu}] EVAL DONE: {tag} d2d={d2d} eseed={es} return={ret}")
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
            tag, nst, ckpt_name, d2d, es = EVAL_JOBS.pop(0)
            ckpt_dir = os.path.join(CKPT_BASE, ckpt_name)
            cmd = [
                PYTHON, EVAL_PY,
                "--checkpoint_dir", ckpt_dir,
                "--n_states", str(nst),
                "--sigma_d2d", str(d2d),
                "--sigma_c2c", "0.0",
                "--max_length", "512",
                "--output_dir", OUT_DIR,
                "--d2d-seed", str(es),
            ]
            print(f"  [GPU {gpu}] EVAL START: {tag} d2d={d2d} eseed={es}")
            active[gpu] = (launch(cmd, gpu), (tag, nst, ckpt_name, d2d, es))
        time.sleep(2)
    print(f"[K107-C Fix] Complete. {len(completed)} eval jobs finished.")

if __name__ == "__main__":
    main()
