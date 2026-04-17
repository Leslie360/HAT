#!/usr/bin/env python3
"""
FW-1: Multi-Seed Training Driver (Ultra Batch Size).
Runs 3 seeds (42, 123, 2026) for V1, V4, C1, C4 on CIFAR-10.
"""

import os
import subprocess
import sys
from datetime import datetime

PYTHON = "/home/qiaosir/miniconda3/envs/LLM/bin/python"
LOG_DIR = "logs/_gpt/multi_seed"
os.makedirs(LOG_DIR, exist_ok=True)

# (model_type, experiment, script, extra_args, batch_size, checkpoint_name)
TASKS = [
    (
        "tinyvit",
        "V1",
        "train_tinyvit.py",
        ["--mode", "train", "--experiment", "V1", "--pretrained", "--amp", "--num-workers", "4"],
        256,
        "V1_fp32_digital_baseline_best.pt",
    ),
    (
        "tinyvit",
        "V4",
        "train_tinyvit.py",
        ["--mode", "train", "--experiment", "V4", "--pretrained", "--amp", "--num-workers", "4"],
        256,
        "V4_hybrid_standard_noise_hat_best.pt",
    ),
    (
        "convnext",
        "C1",
        "train_convnext.py",
        ["--mode", "train", "--experiments", "C1", "--amp"],
        512,
        "C1_FP32_baseline_best.pt",
    ),
    (
        "convnext",
        "C4",
        "train_convnext.py",
        ["--mode", "train", "--experiments", "C4", "--amp"],
        512,
        "C4_4bit_noise_HAT_best.pt",
    ),
]

SEEDS = [42, 123, 2026]

def main():
    print(f"Generating suite for {len(TASKS) * len(SEEDS)} runs...")
    
    with open("scripts/_gpt/run_multi_seed_suite_gpt.sh", "w") as f:
        f.write("#!/bin/bash\n")
        f.write("set -e\n")
        for model_type, exp, script, args, bs, checkpoint_name in TASKS:
            for seed in SEEDS:
                save_dir = f"checkpoints/_gpt/multi_seed/{exp}_s{seed}"
                train_log = f"{LOG_DIR}/multi_seed_{exp}_s{seed}.log"
                eval_log = f"{LOG_DIR}/multi_seed_{exp}_s{seed}_eval.log"
                arg_str = " ".join(args)
                f.write(
                    f"{PYTHON} {script} --dataset cifar10 --seed {seed} --batch-size {bs} "
                    f"--save-dir {save_dir} {arg_str} 2>&1 | tee {train_log}\n"
                )
                if model_type == "tinyvit":
                    eval_args = f"--mode eval --experiment {exp}"
                else:
                    eval_args = f"--mode eval --experiments {exp}"
                eval_amp_flag = "--amp" if model_type == "tinyvit" or exp in {"C1", "C4"} else ""
                f.write(
                    f"{PYTHON} {script} --dataset cifar10 --seed {seed} --batch-size {bs} "
                    f"--checkpoint {save_dir}/{checkpoint_name} --eval-runs 10 {eval_args} "
                    f"{'--pretrained' if model_type == 'tinyvit' else ''} {eval_amp_flag} "
                    f"2>&1 | tee {eval_log}\n"
                )

    os.chmod("scripts/_gpt/run_multi_seed_suite_gpt.sh", 0o755)
    print("Created scripts/_gpt/run_multi_seed_suite_gpt.sh with train+eval chained runs.")

if __name__ == "__main__":
    main()
