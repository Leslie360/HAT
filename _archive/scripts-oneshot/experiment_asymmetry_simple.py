#!/usr/bin/env python3
"""
Experiment A: Differential Asymmetry Tolerance (Simplified Version)
Uses monkey-patching approach to inject asymmetry into existing Analog layers
"""

import sys
import torch
import torch.nn as nn
from pathlib import Path
import json
import numpy as np
import types

sys.path.insert(0, str(Path(__file__).parent))

from train_tinyvit import build_model, evaluate, get_dataloaders, set_seed
from analog_layers import AnalogLinear, AnalogConv2d, AnalogLinearConfig


class AsymmetryInjector:
    """Context manager to temporarily inject asymmetry into model."""
    
    def __init__(self, model, asymmetry_factor):
        self.model = model
        self.alpha = asymmetry_factor
        self.original_methods = {}
    
    def __enter__(self):
        """Patch all AnalogLinear/AnalogConv2d forward methods."""
        for name, module in self.model.named_modules():
            if isinstance(module, (AnalogLinear, AnalogConv2d)):
                # Store original forward
                self.original_methods[id(module)] = module.forward
                
                # Create patched forward
                alpha = self.alpha
                original_forward = module.forward
                
                def make_patched_forward(orig_fwd, module_ref, asym):
                    def patched_forward(x):
                        # Store original weight_to_conductance
                        orig_w2c = module_ref._weight_to_conductance
                        
                        # Create asymmetric version
                        def asymmetric_w2c(weight):
                            cfg = module_ref.config
                            G_range = cfg.G_max - cfg.G_min
                            
                            # Handle both Linear and Conv2d
                            weight_abs = weight.abs()
                            weight_max = weight_abs.max()
                            scale = weight_max if weight_max > 0 else 1.0
                            weight_norm = weight_abs / scale
                            
                            # Split
                            W_pos = weight_norm.clamp(min=0)
                            W_neg = (-weight_norm).clamp(min=0)
                            
                            # Map to conductance
                            G_pos = cfg.G_min + W_pos * G_range
                            G_neg = cfg.G_min + W_neg * G_range
                            
                            # APPLY ASYMMETRY
                            if asym != 0.0:
                                G_pos = G_pos * (1.0 + asym)
                                G_neg = G_neg * (1.0 - asym)
                            
                            return G_pos, G_neg
                        
                        # Replace method temporarily
                        module_ref._weight_to_conductance = asymmetric_w2c
                        
                        # Call original forward
                        result = orig_fwd(x)
                        
                        # Restore original method
                        module_ref._weight_to_conductance = orig_w2c
                        
                        return result
                    
                    return patched_forward
                
                # Apply patch
                module.forward = types.MethodType(
                    make_patched_forward(original_forward, module, alpha), 
                    module
                )
        
        return self.model
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Restore original forward methods."""
        for name, module in self.model.named_modules():
            if isinstance(module, (AnalogLinear, AnalogConv2d)):
                if id(module) in self.original_methods:
                    module.forward = self.original_methods[id(module)]


def run_quick_test(checkpoint_path="checkpoints/V4_hybrid_standard_noise_hat_best.pt"):
    """Quick test with just 0% and 10% asymmetry, 3 runs each."""
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Load data
    _, test_loader = get_dataloaders(dataset="cifar10", batch_size=256, num_workers=4)
    
    # Load checkpoint to get config
    checkpoint = torch.load(checkpoint_path, map_location=device)
    exp_cfg_dict = checkpoint.get('exp_cfg', {})
    
    # Build model with EXACT same config as checkpoint
    from train_tinyvit import TinyViTExperimentConfig
    exp_cfg = TinyViTExperimentConfig(
        name=exp_cfg_dict.get('name', 'V4'),
        use_hybrid=exp_cfg_dict.get('use_hybrid', True),
        n_states=exp_cfg_dict.get('n_states', 16),
        nl_ltp=exp_cfg_dict.get('nl_ltp', 1.0),
        nl_ltd=exp_cfg_dict.get('nl_ltd', -1.0),
        sigma_c2c=exp_cfg_dict.get('sigma_c2c', 0.05),
        sigma_d2d=exp_cfg_dict.get('sigma_d2d', 0.10),
        noise_mode=exp_cfg_dict.get('noise_mode', 'uniform'),
        noise_enabled=exp_cfg_dict.get('noise_enabled', True),
        hat_training=exp_cfg_dict.get('hat_training', True),
        use_physical_frontend=exp_cfg_dict.get('use_physical_frontend', False),
        retention_enabled=exp_cfg_dict.get('retention_enabled', False),
        adc_bits=exp_cfg_dict.get('adc_bits', 8),
    )
    
    asymmetry_levels = [0.0, 0.05, 0.10, 0.20]
    num_runs = 10
    results = {}
    
    for asym in asymmetry_levels:
        print(f"\n{'='*60}")
        print(f"Testing asymmetry = {asym:.2f} ({asym*100:.0f}%)")
        print(f"{'='*60}")
        
        accuracies = []
        
        for run in range(num_runs):
            set_seed(42 + run)
            
            # Build fresh model
            model = build_model(exp_cfg, num_classes=10, device=device, pretrained=False)
            model.load_state_dict(checkpoint["model_state_dict"], strict=False)
            
            # Enable analog mode
            for m in model.modules():
                if hasattr(m, 'analog_enabled'):
                    m.analog_enabled = True
            
            model.eval()
            
            # Evaluate with asymmetry injection
            with AsymmetryInjector(model, asym):
                criterion = nn.CrossEntropyLoss()
                acc, _ = evaluate(model, test_loader, criterion, device, exp_cfg, amp_enabled=True)
            
            accuracies.append(acc)
            print(f"  Run {run+1}/{num_runs}: {acc:.2f}%")
        
        mean_acc = np.mean(accuracies)
        std_acc = np.std(accuracies)
        
        results[str(asym)] = {
            "mean": float(mean_acc),
            "std": float(std_acc),
            "accuracies": [float(a) for a in accuracies]
        }
        
        print(f"\n  → Summary: {mean_acc:.2f} ± {std_acc:.2f}%")
    
    # Save
    output_file = "report_md/_gpt/asymmetry_sweep_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    # Print final summary
    print(f"\n{'='*60}")
    print("FINAL SUMMARY")
    print(f"{'='*60}")
    print(f"{'Asymmetry':<12} {'Accuracy':<20} {'Degradation':<15}")
    print("-" * 50)
    
    baseline = results["0.0"]["mean"]
    for asym_str in ["0.0", "0.05", "0.1", "0.2"]:
        if asym_str in results:
            r = results[asym_str]
            deg = baseline - r["mean"]
            print(f"{float(asym_str)*100:>5.0f}%       {r['mean']:>6.2f} ± {r['std']:>5.2f}%      {deg:>6.2f}%")
    
    print(f"\nResults saved to: {output_file}")
    return results


if __name__ == "__main__":
    run_quick_test()
