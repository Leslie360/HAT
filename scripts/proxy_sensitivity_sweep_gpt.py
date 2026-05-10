import sys
import os
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "compute_vit"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import json
import torch
import numpy as np
import logging
import datetime
from inference_analysis_utils import load_model_bundle, run_mc_eval, apply_device_profile
from device_profile_utils import load_device_profiles_json
import dataclasses

# Setup logging
log_path = Path("logs/_gpt/proxy_sensitivity_sweep_20260408.log")
log_path.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

def evaluate_sensitivity(model_type, exp_id, checkpoint_path, device, base_profile, c2c_list, d2d_list, eval_runs=10):
    bundle = load_model_bundle(model_type, exp_id, device, checkpoint_path)
    logger.info(f"Running sensitivity sweep for {exp_id} on {base_profile.device_type} with N={eval_runs} MC evals...")
    print(f"Running sensitivity sweep for {exp_id} on {base_profile.device_type} with N={eval_runs} MC evals...")
    
    results = {}
    
    for c2c in c2c_list:
        for d2d in d2d_list:
            seed = 42
            torch.manual_seed(seed)
            np.random.seed(seed)
            
            # Create modified profile
            current_profile = dataclasses.replace(base_profile, sigma_c2c=c2c / 100.0, sigma_d2d=d2d / 100.0)
            
            # Apply profile (resamples d2d)
            apply_device_profile(bundle.model, current_profile, resample_d2d=True)
            
            label = f"c2c={c2c}%, d2d={d2d}%"
            # We don't use the standard logger inside run_mc_eval to avoid clutter, we log the result ourselves
            stats = run_mc_eval(bundle, eval_runs=eval_runs, label=label)
            
            res_str = f"Result for {label}: Mean Acc = {stats['test_acc_mean']:.2f}%, Std = {stats['test_acc_std']:.2f}%"
            logger.info(res_str)
            print(res_str)
            
            key = f"c2c_{c2c}_d2d_{d2d}"
            results[key] = stats
            
    return results

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    profiles = load_device_profiles_json("report_md/_gpt/json_gpt/literature_fitted_profile.json")
    profile = profiles[0]
    
    c2c_list = [1, 2, 5, 8]
    d2d_list = [2, 3, 5, 10, 15]
    
    logger.info("--- Starting Proxy Sensitivity Sweep ---")
    logger.info(f"Parameters: c2c_list={c2c_list}, d2d_list={d2d_list}")
    
    ens_stats = evaluate_sensitivity(
        "tinyvit", "V4", "checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt", device, profile, c2c_list, d2d_list, eval_runs=10
    )
    
    output_path = Path("report_md/_gpt/json_gpt/zhang_sensitivity_sweep_10mc.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(ens_stats, f, indent=2)
    
    logger.info(f"Sweep complete. JSON saved to {output_path}")
    print(f"Sweep complete. JSON saved to {output_path}")

if __name__ == "__main__":
    main()
