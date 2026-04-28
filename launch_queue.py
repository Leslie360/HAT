#!/usr/bin/env python3
"""Seed-grouped queue launcher. Runs one seed's 6 configs at a time,
using at most 5 GPUs so 2 cards stay free for others.
"""
import subprocess
import time
import os
import sys

SAVE_DIR = "checkpoints/_gpt/cross_arch_tinyimagenet"
GPUS = [1, 2, 3, 4, 5, 6, 7]
MAX_PARALLEL = 6           # keep 1 GPU free
SEEDS = [123, 456]
ARCHS = ["vit_small_patch16_224", "deit_small_patch16_224"]
HATS = ["standard", "ensemble", "proportional"]


def is_process_running(pid):
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def launch_task(arch, hat, seed, gpu_id):
    log_path = os.path.join(SAVE_DIR, f"{arch}_{hat}_seed{seed}.log")
    cmd = (
        f"PYTHONUNBUFFERED=1 PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True "
        f"CUDA_VISIBLE_DEVICES={gpu_id} "
        f"conda run -n hat python -u train_vit_tinyimagenet.py "
        f"--arch {arch} --hat-type {hat} "
        f"--epochs 100 --batch-size 512 --lr 0.002 --warmup-epochs 5 "
        f"--seed {seed} --device cuda --amp --pretrained "
        f"--data-root ../data/tiny-imagenet-200 "
        f"--save-dir {SAVE_DIR} "
        f"> {log_path} 2>&1"
    )
    print(f"[LAUNCH] {arch} {hat} seed={seed} on GPU {gpu_id}")
    proc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
    return proc.pid


def main():
    os.makedirs(SAVE_DIR, exist_ok=True)

    for seed in SEEDS:
        seed_tasks = []
        for arch in ARCHS:
            for hat in HATS:
                seed_tasks.append((arch, hat, seed))

        print(f"\n========== Starting seed {seed} ({len(seed_tasks)} tasks) ==========")
        task_idx = 0
        launched = {}  # gpu_id -> (arch, hat, seed, pid)

        while task_idx < len(seed_tasks) or launched:
            # Launch new tasks up to MAX_PARALLEL
            for gpu in GPUS:
                if gpu in launched:
                    continue
                if len(launched) >= MAX_PARALLEL:
                    break
                if task_idx >= len(seed_tasks):
                    break
                arch, hat, s = seed_tasks[task_idx]
                pid = launch_task(arch, hat, s, gpu)
                launched[gpu] = (arch, hat, s, pid)
                task_idx += 1
                time.sleep(5)

            # Check for finished jobs
            finished = []
            for gpu, (arch, hat, s, pid) in list(launched.items()):
                if not is_process_running(pid):
                    print(f"[DONE  ] {arch} {hat} seed={s} on GPU {gpu}")
                    finished.append(gpu)
            for gpu in finished:
                del launched[gpu]

            if task_idx < len(seed_tasks) or launched:
                time.sleep(30)

        print(f"========== Seed {seed} complete ==========\n")

    print("All seeds completed.")


if __name__ == "__main__":
    main()
