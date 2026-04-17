#!/usr/bin/env python3
"""
Experiment A: Differential Pair Asymmetry Tolerance Sweep
Addresses Reviewer Issue #15: Differential pair mapping ablation

Quantifies systematic branch asymmetry tolerance to upgrade §6.6 from 
qualitative limitation to quantitative bound.

Author: Kimi (2026-04-11)
"""

import sys
import torch
import torch.nn as nn
from pathlib import Path
import json
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))

from train_tinyvit import build_model, evaluate, get_dataloaders, TinyViTExperimentConfig
from analog_layers import AnalogLinear, AnalogConv2d, AnalogLinearConfig


class AsymmetricAnalogLinear(AnalogLinear):
    """AnalogLinear with configurable branch asymmetry."""
    
    def __init__(self, *args, asymmetry_factor=0.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.asymmetry_factor = asymmetry_factor
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if not self.analog_enabled:
            return super().forward(x)
        
        cfg = self.config
        G_pos, G_neg = self._weight_to_conductance(self.weight)
        
        if self.asymmetry_factor != 0.0:
            G_pos = G_pos * (1.0 + self.asymmetry_factor)
            G_neg = G_neg * (1.0 - self.asymmetry_factor)
        
        G_pos, G_neg = self._apply_retention(G_pos, G_neg)
        W_eff = self._apply_noise(G_pos, G_neg)
        out = torch.nn.functional.linear(x, W_eff, self.bias)
        return out


class AsymmetricAnalogConv2d(AnalogConv2d):
    """AnalogConv2d with configurable branch asymmetry."""
    
    def __init__(self, *args, asymmetry_factor=0.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.asymmetry_factor = asymmetry_factor
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if not self.analog_enabled:
            return super().forward(x)
        
        cfg = self.config
        G_pos, G_neg = self._weight_to_conductance(self.weight)
        
        if self.asymmetry_factor != 0.0:
            G_pos = G_pos * (1.0 + self.asymmetry_factor)
            G_neg = G_neg * (1.0 - self.asymmetry_factor)
        
        G_pos, G_neg = self._apply_retention(G_pos, G_neg)
        W_eff = self._apply_noise(G_pos, G_neg)
        out = self._conv_forward(x, W_eff, self.bias)
        return out


def replace_modules_with_asymmetry(model, asymmetry_factor, base_config):
    """Replace all AnalogLinear/AnalogConv2d with asymmetric versions."""
    
    def replace_module(parent, name, module):
        if isinstance(module, AnalogLinear) and not isinstance(module, AsymmetricAnalogLinear):
            new_module = AsymmetricAnalogLinear(
                in_features=module.in_features,
                out_features=module.out_features,
                bias=(module.bias is not None),
                config=base_config,
                asymmetry_factor=asymmetry_factor,
            )
            new_module.weight = module.weight
            if module.bias is not None:
                new_module.bias = module.bias
            new_module.analog_enabled = module.analog_enabled
            setattr(parent, name, new_module)
            
        elif isinstance(module, AnalogConv2d) and not isinstance(module, AsymmetricAnalogConv2d):
            new_module = AsymmetricAnalogConv2d(
                in_channels=module.in_channels,
                out_channels=module.out_channels,
                kernel_size=module.kernel_size,
                stride=module.stride,
                padding=module.padding,
                bias=(module.bias is not None),
                config=base_config,
                asymmetry_factor=asymmetry_factor,
            )
            new_module.weight = module.weight
            if module.bias is not None:
                new_module.bias = module.bias
            new_module.analog_enabled = module.analog_enabled
            setattr(parent, name, new_module)
    
    for name, module in list(model.named_children()):
        replace_module(model, name, module)
        replace_modules_with_asymmetry(module, asymmetry_factor, base_config)


def run_asymmetry_sweep(
    checkpoint_path="checkpoints/V4_hybrid_standard_noise_hat_best.pt",
    asymmetry_levels=[0.0, 0.05, 0.10],
    num_runs=5,
    device="cuda"
):
    device = torch.device(device if torch.cuda.is_available() else "cpu")
    
    # Load data
    _, test_loader = get_dataloaders(dataset="cifar10", batch_size=256, num_workers=4)
    
    # Create experiment config
    exp_cfg = TinyViTExperimentConfig(
        name="V4_asymmetry",
        n_states=16,
        noise_enabled=True,
        hat_training=True,
        sigma_c2c=0.05,
        sigma_d2d=0.10,
    )
    
    base_config = AnalogLinearConfig(
        n_states=16,
        G_min=1.0,
        G_max=10.0,
        sigma_c2c=0.05,
        sigma_d2d=0.10,
        noise_mode="uniform",
        noise_enabled=True,
    )
    
    results = {}
    
    for asym in asymmetry_levels:
        print(f"\n{'='*60}")
        print(f"Testing asymmetry_factor = {asym:.2f} ({asym*100:.0f}%)")
        print(f"{'='*60}")
        
        accuracies = []
        
        for run in range(num_runs):
            # Build model
            model = build_model(exp_cfg, num_classes=10, device=device, pretrained=True)
            
            # Load checkpoint
            checkpoint = torch.load(checkpoint_path, map_location=device)
            model.load_state_dict(checkpoint["model_state_dict"], strict=False)
            
            # Replace with asymmetric modules
            replace_modules_with_asymmetry(model, asym, base_config)
            model = model.to(device)
            model.eval()
            
            # Enable analog mode
            for m in model.modules():
                if hasattr(m, 'analog_enabled'):
                    m.analog_enabled = True
            
            # Evaluate
            criterion = nn.CrossEntropyLoss()
            acc, _ = evaluate(model, test_loader, criterion, device, exp_cfg, amp_enabled=True)
            accuracies.append(acc)
            print(f"  Run {run+1}: {acc:.2f}%")
        
        mean_acc = np.mean(accuracies)
        std_acc = np.std(accuracies)
        
        results[asym] = {
            "accuracies": accuracies,
            "mean": mean_acc,
            "std": std_acc,
        }
        
        print(f"\n  Summary: {mean_acc:.2f} ± {std_acc:.2f}%")
    
    # Save results
    output_file = "report_md/_gpt/asymmetry_sweep_results.json"
    with open(output_file, "w") as f:
        json.dump({str(k): v for k, v in results.items()}, f, indent=2)
    
    print(f"\n{'='*60}")
    print("ASYMMETRY SWEEP COMPLETE")
    print(f"{'='*60}")
    print(f"\nResults saved to: {output_file}")
    print("\nSummary Table:")
    print(f"{'Asymmetry':<12} {'Accuracy':<15} {'Degradation':<15}")
    print("-" * 45)
    
    baseline = results[0.0]["mean"]
    for asym in asymmetry_levels:
        acc = results[asym]["mean"]
        deg = baseline - acc
        print(f"{asym*100:>5.0f}%       {acc:>6.2f} ± {results[asym]['std']:.2f}%    {deg:>6.2f}%")
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Differential Asymmetry Tolerance Sweep")
    parser.add_argument("--checkpoint", default="checkpoints/V4_hybrid_standard_noise_hat_best.pt")
    parser.add_argument("--asymmetry", nargs="+", type=float, default=[0.0, 0.05, 0.10])
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--device", default="cuda")
    
    args = parser.parse_args()
    
    results = run_asymmetry_sweep(
        checkpoint_path=args.checkpoint,
        asymmetry_levels=args.asymmetry,
        num_runs=args.runs,
        device=args.device,
    )
