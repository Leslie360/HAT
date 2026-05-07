#!/usr/bin/env python3
"""
FW-2: State-Dependent Retention Comparison.
Evaluates Tiny-ViT V4 on CIFAR-10 under uniform vs state-dependent retention.
"""

import os
import sys
import torch
from datetime import datetime

# Add root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from inference_analysis_utils import (
    load_model_bundle,
    run_mc_eval,
    iter_analog_modules,
)
from train_tinyvit import RunLogger

def set_retention_mode(model, t, state_dependent):
    for _, module in iter_analog_modules(model):
        module.config.retention_enabled = t > 0
        module.config.inference_time = t
        module.config.retention_state_dependent = state_dependent
        # Standard calibration for V4
        module.config.retention_recalibrate_scale = True
        module.config.retention_scales_d2d = True

def main():
    checkpoint = "checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt"
    if not os.path.exists(checkpoint):
        checkpoint = "checkpoints/_gpt/V4_hybrid_standard_noise_hat_best.pt"
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    bundle = load_model_bundle("tinyvit", "V4", device=device, checkpoint_path=checkpoint)
    
    log_dir = "logs/_gpt"
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, f"retention_uniform_vs_statedep_{datetime.now().strftime('%Y%m%d')}.log")
    
    logger = RunLogger(log_path)
    logger.log(f"Starting FW-2 Retention Comparison on {checkpoint}")
    
    times = [0, 1, 10, 100, 1000]
    results = {"uniform": [], "state_dep": []}
    
    for t in times:
        # 1. Uniform
        set_retention_mode(bundle.model, float(t), False)
        summary_u = run_mc_eval(bundle, eval_runs=10, logger=logger, label=f"Uniform t={t}")
        results["uniform"].append(summary_u["test_acc_mean"])
        
        # 2. State-dependent
        set_retention_mode(bundle.model, float(t), True)
        summary_s = run_mc_eval(bundle, eval_runs=10, logger=logger, label=f"State-Dep t={t}")
        results["state_dep"].append(summary_s["test_acc_mean"])
        
    logger.log("\nComparison Table:")
    logger.log("| t (s) | Uniform Acc (%) | State-Dep Acc (%) | Diff (pp) |")
    logger.log("|-------|-----------------|-------------------|-----------|")
    for i, t in enumerate(times):
        u = results["uniform"][i]
        s = results["state_dep"][i]
        logger.log(f"| {t:5} | {u:15.2f} | {s:17.2f} | {s-u:9.2f} |")

if __name__ == "__main__":
    main()
