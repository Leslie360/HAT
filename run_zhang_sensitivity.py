import json
import torch
import numpy as np
from pathlib import Path
from inference_analysis_utils import load_model_bundle, run_mc_eval, apply_device_profile
from device_profile_utils import load_device_profiles_json

import dataclasses
def evaluate_sensitivity(model_type, exp_id, checkpoint_path, device, base_profile, c2c_list, d2d_list, eval_runs=5):
    bundle = load_model_bundle(model_type, exp_id, device, checkpoint_path)
    print(f"\nRunning sensitivity sweep for {exp_id} on {base_profile.device_type}...")
    
    results = {}
    
    for c2c in c2c_list:
        for d2d in d2d_list:
            # Set the seed per combination to ensure deterministic MC evaluations
            seed = 42
            torch.manual_seed(seed)
            np.random.seed(seed)
            
            # Modify the profile with the current c2c and d2d
            current_profile = dataclasses.replace(base_profile, sigma_c2c=c2c / 100.0, sigma_d2d=d2d / 100.0)
            
            # Apply profile and resample d2d
            apply_device_profile(bundle.model, current_profile, resample_d2d=True)
            
            # Run MC evaluation
            label = f"c2c={c2c}%, d2d={d2d}%"
            stats = run_mc_eval(bundle, eval_runs=eval_runs, label=label)
            print(f"Result for {label}: Mean Acc = {stats['test_acc_mean']:.2f}%, Std = {stats['test_acc_std']:.2f}%")
            
            key = f"c2c_{c2c}_d2d_{d2d}"
            results[key] = stats
            
    return results

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    profiles = load_device_profiles_json("report_md/_gpt/json_gpt/literature_fitted_profile.json")
    profile = profiles[0]
    
    c2c_list = [1, 2, 5, 8]
    d2d_list = [2, 3, 5, 10, 15]
    
    ens_stats = evaluate_sensitivity(
        "tinyvit", "V4", "checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt", device, profile, c2c_list, d2d_list
    )
    
    output_path = Path("report_md/_gpt/json_gpt/zhang_sensitivity_sweep.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(ens_stats, f, indent=2)

if __name__ == "__main__":
    main()
