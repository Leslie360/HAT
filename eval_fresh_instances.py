import argparse
import json
import torch
import numpy as np
from pathlib import Path

from inference_analysis_utils import load_model_bundle, run_mc_eval, set_uniform_noise
from train_tinyvit import get_v_experiment_configs

def evaluate_on_fresh_instances(model_type, exp_id, checkpoint_path, device, num_instances=10, mc_runs_per_instance=5):
    bundle = load_model_bundle(model_type, exp_id, device, checkpoint_path)
    cfg = bundle.exp_cfg
    
    instance_accs = []
    print(f"\nEvaluating {exp_id} from {checkpoint_path} on {num_instances} fresh instances...")
    
    for instance_idx in range(num_instances):
        # Change seed to get a fresh D2D instantiation
        seed = 42 + instance_idx * 100
        torch.manual_seed(seed)
        np.random.seed(seed)
        
        # Re-apply noise to generate a new fixed D2D buffer for this instance
        set_uniform_noise(bundle.model, sigma_c2c=cfg.sigma_c2c, sigma_d2d=cfg.sigma_d2d, 
                          noise_enabled=cfg.noise_enabled, resample_d2d=True, noise_mode=cfg.noise_mode)
        
        # Run MC eval (resamples C2C each forward pass)
        stats = run_mc_eval(bundle, eval_runs=mc_runs_per_instance, label=f"Instance {instance_idx+1}/{num_instances}")
        instance_accs.append(stats["test_acc_mean"])
        print(f"  Instance {instance_idx+1}: {stats['test_acc_mean']:.2f}%")
        
    mean_acc = np.mean(instance_accs)
    std_acc = np.std(instance_accs)
    print(f"Result for {exp_id}: Mean Acc = {mean_acc:.2f}%, Cross-Instance Std = {std_acc:.2f}%\n")
    return mean_acc, std_acc, instance_accs

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    results = {}
    
    # Evaluate Standard V4
    std_mean, std_std, std_accs = evaluate_on_fresh_instances(
        "tinyvit", "V4", "checkpoints/V4_hybrid_standard_noise_hat_best.pt", device
    )
    results["V4_Standard"] = {"mean": std_mean, "std": std_std, "instances": std_accs}
    
    # Evaluate Ensemble V4
    ens_mean, ens_std, ens_accs = evaluate_on_fresh_instances(
        "tinyvit", "V4", "checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt", device
    )
    results["V4_Ensemble"] = {"mean": ens_mean, "std": ens_std, "instances": ens_accs}
    
    # Save results
    output_path = Path("report_md/_gpt/json_gpt/fresh_instance_eval.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
        
    print(f"Saved results to {output_path}")

if __name__ == "__main__":
    main()
