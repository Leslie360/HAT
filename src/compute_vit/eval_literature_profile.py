import json
import torch
import numpy as np
from pathlib import Path
from inference_analysis_utils import load_model_bundle, run_mc_eval, apply_device_profile
from device_profile_utils import load_device_profiles_json

def evaluate_on_profile(model_type, exp_id, checkpoint_path, device, profile, eval_runs=10):
    bundle = load_model_bundle(model_type, exp_id, device, checkpoint_path)
    print(f"\nApplying profile {profile.device_type} to {exp_id} from {checkpoint_path}...")
    
    seed = 42
    torch.manual_seed(seed)
    np.random.seed(seed)
    
    apply_device_profile(bundle.model, profile, resample_d2d=True)
    
    stats = run_mc_eval(bundle, eval_runs=eval_runs, label=f"{exp_id} on {profile.device_type}")
    print(f"Result for {exp_id}: Mean Acc = {stats['test_acc_mean']:.2f}%, Std = {stats['test_acc_std']:.2f}%\n")
    return stats

def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    profiles = load_device_profiles_json("report_md/_gpt/json_gpt/literature_fitted_profile.json")
    profile = profiles[0]
    
    std_stats = evaluate_on_profile(
        "tinyvit", "V4", "checkpoints/V4_hybrid_standard_noise_hat_best.pt", device, profile
    )
    
    ens_stats = evaluate_on_profile(
        "tinyvit", "V4", "checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt", device, profile
    )
    
    results = {
        "V4_Standard": std_stats,
        "V4_Ensemble": ens_stats
    }
    
    output_path = Path("report_md/_gpt/json_gpt/literature_profile_eval.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
