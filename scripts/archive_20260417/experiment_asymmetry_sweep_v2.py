#!/usr/bin/env python3
"""
Experiment A: Differential Pair Asymmetry Tolerance Sweep (Simplified)
Addresses Reviewer Issue #15

Author: Kimi (2026-04-11)
"""

import sys
import torch
import torch.nn as nn
from pathlib import Path
import json
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

from train_tinyvit import build_model, evaluate, get_dataloaders, TinyViTExperimentConfig, set_seed
from analog_layers import AnalogLinear, AnalogConv2d, AnalogLinearConfig


def apply_asymmetry_to_model(model, asymmetry_factor):
    """
    Apply asymmetry to all AnalogLinear/AnalogConv2d modules in-place.
    Asymmetry model: G_pos *= (1+alpha), G_neg *= (1-alpha)
    """
    for name, module in model.named_modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            # Hook to modify forward behavior
            def make_asymmetric_forward(orig_forward, alpha):
                def asymmetric_forward(self, x):
                    # Temporarily modify behavior by patching internal method
                    original_weight_to_conductance = module._weight_to_conductance
                    
                    def asymmetric_weight_to_conductance(weight):
                        # Call original
                        if isinstance(module, AnalogLinear):
                            # Use parent's method
                            cfg = module.config
                            G_range = cfg.G_max - cfg.G_min
                            
                            # Normalize weight to [0,1]
                            weight_abs = weight.abs()
                            weight_max = weight_abs.max()
                            if weight_max > 0:
                                weight_norm = weight_abs / weight_max
                            else:
                                weight_norm = torch.zeros_like(weight_abs)
                            
                            # Split to differential pair
                            W_pos = weight_norm.clamp(min=0)
                            W_neg = (-weight_norm).clamp(min=0)
                            
                            # Map to conductance
                            G_pos = cfg.G_min + W_pos * G_range
                            G_neg = cfg.G_min + W_neg * G_range
                            
                            # Apply asymmetry HERE
                            if alpha != 0.0:
                                G_pos = G_pos * (1.0 + alpha)
                                G_neg = G_neg * (1.0 - alpha)
                            
                            return G_pos, G_neg
                        else:
                            # AnalogConv2d - similar logic
                            cfg = module.config
                            G_range = cfg.G_max - cfg.G_min
                            
                            weight_abs = weight.abs()
                            weight_max = weight_abs.max()
                            if weight_max > 0:
                                weight_norm = weight_abs / weight_max
                            else:
                                weight_norm = torch.zeros_like(weight_abs)
                            
                            W_pos = weight_norm.clamp(min=0)
                            W_neg = (-weight_norm).clamp(min=0)
                            
                            G_pos = cfg.G_min + W_pos * G_range
                            G_neg = cfg.G_min + W_neg * G_range
                            
                            if alpha != 0.0:
                                G_pos = G_pos * (1.0 + alpha)
                                G_neg = G_neg * (1.0 - alpha)
                            
                            return G_pos, G_neg
                    
                    # Patch temporarily
                    module._weight_to_conductance = asymmetric_weight_to_conductance
                    
                    # Call original forward
                    result = orig_forward(x)
                    
                    # Restore original method
                    module._weight_to_conductance = original_weight_to_conductance
                    
                    return result
                
                return asymmetric_forward
            
            # Bind the new forward
            import types
            module.forward = types.MethodType(make_asymmetric_forward(module.forward, asymmetry_factor), module)


def run_asymmetry_sweep(
    checkpoint_path="checkpoints/V4_hybrid_standard_noise_hat_best.pt",
    asymmetry_levels=[0.0, 0.05, 0.10, 0.20],
    num_runs=5,
    device="cuda",
    seed=42
):
    device = torch.device(device if torch.cuda.is_available() else "cpu")
    
    # Load data
    _, test_loader = get_dataloaders(dataset="cifar10", batch_size=256, num_workers=4)
    
    # Create experiment config (matching V4)
    exp_cfg = TinyViTExperimentConfig(
        name="V4",
        use_hybrid=True,
        n_states=16,
        nl_ltp=1.0,
        nl_ltd=-1.0,
        sigma_c2c=0.05,
        sigma_d2d=0.10,
        noise_mode="uniform",
        noise_enabled=True,
        hat_training=True,
        adc_bits=8,
    )
    
    results = {}
    
    for asym in asymmetry_levels:
        print(f"\n{'='*60}")
        print(f"Testing asymmetry_factor = {asym:.2f} ({asym*100:.0f}%)")
        print(f"{'='*60}")
        
        accuracies = []
        
        for run in range(num_runs):
            set_seed(seed + run)
            
            # Build fresh model
            model = build_model(exp_cfg, num_classes=10, device=device, pretrained=False)
            
            # Load checkpoint
            checkpoint = torch.load(checkpoint_path, map_location=device)
            model.load_state_dict(checkpoint["model_state_dict"], strict=False)
            
            # Apply asymmetry
            apply_asymmetry_to_model(model, asym)
            
            # Enable analog mode
            for m in model.modules():
                if hasattr(m, 'analog_enabled'):
                    m.analog_enabled = True
            
            model.eval()
            
            # Evaluate
            criterion = nn.CrossEntropyLoss()
            acc, loss = evaluate(model, test_loader, criterion, device, exp_cfg, amp_enabled=True)
            accuracies.append(acc)
            print(f"  Run {run+1}: {acc:.2f}%")
        
        mean_acc = np.mean(accuracies)
        std_acc = np.std(accuracies)
        
        results[str(asym)] = {
            "accuracies": accuracies,
            "mean": mean_acc,
            "std": std_acc,
        }
        
        print(f"\n  Summary: {mean_acc:.2f} ± {std_acc:.2f}%")
    
    # Save results
    output_file = "report_md/_gpt/asymmetry_sweep_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*60}")
    print("ASYMMETRY SWEEP COMPLETE")
    print(f"{'='*60}")
    print(f"\nResults saved to: {output_file}")
    print("\nSummary Table:")
    print(f"{'Asymmetry':<12} {'Accuracy':<20} {'Degradation':<15}")
    print("-" * 50)
    
    baseline = results["0.0"]["mean"]
    for asym_str in ["0.0", "0.05", "0.1", "0.2"]:
        if asym_str in results:
            acc = results[asym_str]["mean"]
            std = results[asym_str]["std"]
            deg = baseline - acc
            print(f"{float(asym_str)*100:>5.0f}%       {acc:>6.2f} ± {std:>5.2f}%      {deg:>6.2f}%")
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Differential Asymmetry Tolerance Sweep")
    parser.add_argument("--checkpoint", default="checkpoints/V4_hybrid_standard_noise_hat_best.pt")
    parser.add_argument("--asymmetry", nargs="+", type=float, default=[0.0, 0.05, 0.10, 0.20])
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--seed", type=int, default=42)
    
    args = parser.parse_args()
    
    results = run_asymmetry_sweep(
        checkpoint_path=args.checkpoint,
        asymmetry_levels=args.asymmetry,
        num_runs=args.runs,
        device=args.device,
        seed=args.seed,
    )
