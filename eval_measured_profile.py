import json
import torch
from inference_analysis_utils import load_model_bundle, run_mc_eval, apply_device_profile
from device_profile_utils import load_profiles

def main():
    bundle = load_model_bundle("tinyvit", "V4", "cuda" if torch.cuda.is_available() else "cpu", checkpoint_path="checkpoints/V4_hybrid_standard_noise_hat_best.pt")
    
    profiles = load_profiles("report_md/_gpt/json_gpt/measured_sample_profile.json")
    
    apply_device_profile(bundle.model, profiles[0])
    
    stats = run_mc_eval(bundle, 5)
    
    print(f"Measured Profile Accuracy: {stats['accuracy']:.2f}% ± {stats['std']:.2f}%")

if __name__ == "__main__":
    main()
