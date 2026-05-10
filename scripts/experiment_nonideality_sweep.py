#!/usr/bin/env python3
"""
Experiment B: Physical Non-Ideality Sensitivity Sweep
Addresses Reviewer Issue #59: Physical non-ideality sensitivity

Quantifies impact of IR drop and sneak path effects to upgrade §6.6 from
qualitative "out-of-scope" to quantitative bounds.

Based on ReRAM literature estimates: IR drop 1-3%, sneak paths 1-2%

Author: Kimi (2026-04-11)
"""

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "compute_vit"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import torch
import torch.nn as nn
from pathlib import Path

from train_tinyvit import get_tinyvit_model, evaluate_model, get_cifar10_loaders
from analog_layers import AnalogLinear, AnalogConv2d, AnalogLinearConfig


class NonIdealAnalogLinear(AnalogLinear):
    """AnalogLinear with IR drop and sneak path modeling.
    
    Non-ideality models:
    1. IR drop: Effective weight reduced by factor (1 - ir_drop_factor)
       Models voltage drop along wordlines/bitlines
    
    2. Sneak path: Conductance leakage between adjacent cells
       Models as additional noise proportional to conductance
    """
    
    def __init__(self, *args, ir_drop_factor=0.0, sneak_factor=0.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.ir_drop_factor = ir_drop_factor
        self.sneak_factor = sneak_factor
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if not self.analog_enabled:
            return super().forward(x)
        
        cfg = self.config
        
        # Step 1: Weight → conductance
        G_pos, G_neg = self._weight_to_conductance(self.weight)
        
        # Step 2: Apply non-idealities (NEW for this experiment)
        
        # IR drop: systematic reduction in effective conductance
        # Models position-dependent voltage drop in array
        if self.ir_drop_factor > 0:
            # Average IR drop reduces effective differential signal
            ir_drop_pos = torch.rand_like(G_pos) * self.ir_drop_factor
            ir_drop_neg = torch.rand_like(G_neg) * self.ir_drop_factor
            G_pos = G_pos * (1.0 - ir_drop_pos)
            G_neg = G_neg * (1.0 - ir_drop_neg)
        
        # Sneak paths: leakage between adjacent cells
        # Models as additional conductance noise
        if self.sneak_factor > 0:
            sneak_noise_pos = torch.randn_like(G_pos) * self.sneak_factor * cfg.G_max
            sneak_noise_neg = torch.randn_like(G_neg) * self.sneak_factor * cfg.G_max
            G_pos = G_pos + sneak_noise_pos.clamp(-cfg.G_max * 0.1, cfg.G_max * 0.1)
            G_neg = G_neg + sneak_noise_neg.clamp(-cfg.G_max * 0.1, cfg.G_max * 0.1)
        
        # Step 3: Retention
        G_pos, G_neg = self._apply_retention(G_pos, G_neg)
        
        # Step 4: Noise and differential readout
        W_eff = self._apply_noise(G_pos, G_neg)
        
        # Step 5: Analog MAC
        out = torch.nn.functional.linear(x, W_eff, self.bias)
        return out


class NonIdealAnalogConv2d(AnalogConv2d):
    """AnalogConv2d with IR drop and sneak path modeling."""
    
    def __init__(self, *args, ir_drop_factor=0.0, sneak_factor=0.0, **kwargs):
        super().__init__(*args, **kwargs)
        self.ir_drop_factor = ir_drop_factor
        self.sneak_factor = sneak_factor
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if not self.analog_enabled:
            return super().forward(x)
        
        cfg = self.config
        
        # Weight → conductance
        G_pos, G_neg = self._weight_to_conductance(self.weight)
        
        # Apply non-idealities
        if self.ir_drop_factor > 0:
            ir_drop_pos = torch.rand_like(G_pos) * self.ir_drop_factor
            ir_drop_neg = torch.rand_like(G_neg) * self.ir_drop_factor
            G_pos = G_pos * (1.0 - ir_drop_pos)
            G_neg = G_neg * (1.0 - ir_drop_neg)
        
        if self.sneak_factor > 0:
            sneak_noise_pos = torch.randn_like(G_pos) * self.sneak_factor * cfg.G_max
            sneak_noise_neg = torch.randn_like(G_neg) * self.sneak_factor * cfg.G_max
            G_pos = G_pos + sneak_noise_pos.clamp(-cfg.G_max * 0.1, cfg.G_max * 0.1)
            G_neg = G_neg + sneak_noise_neg.clamp(-cfg.G_max * 0.1, cfg.G_max * 0.1)
        
        # Retention, noise, convolution
        G_pos, G_neg = self._apply_retention(G_pos, G_neg)
        W_eff = self._apply_noise(G_pos, G_neg)
        
        out = self._conv_forward(x, W_eff, self.bias)
        return out


def replace_modules_with_nonideality(model, ir_drop, sneak_factor, base_config):
    """Replace all Analog modules with non-ideal versions."""
    
    def replace_module(parent, name, module):
        if isinstance(module, AnalogLinear) and not isinstance(module, NonIdealAnalogLinear):
            new_module = NonIdealAnalogLinear(
                in_features=module.in_features,
                out_features=module.out_features,
                bias=(module.bias is not None),
                config=base_config,
                ir_drop_factor=ir_drop,
                sneak_factor=sneak_factor,
            )
            new_module.weight = module.weight
            if module.bias is not None:
                new_module.bias = module.bias
            setattr(parent, name, new_module)
            
        elif isinstance(module, AnalogConv2d) and not isinstance(module, NonIdealAnalogConv2d):
            new_module = NonIdealAnalogConv2d(
                in_channels=module.in_channels,
                out_channels=module.out_channels,
                kernel_size=module.kernel_size,
                stride=module.stride,
                padding=module.padding,
                bias=(module.bias is not None),
                config=base_config,
                ir_drop_factor=ir_drop,
                sneak_factor=sneak_factor,
            )
            new_module.weight = module.weight
            if module.bias is not None:
                new_module.bias = module.bias
            setattr(parent, name, new_module)
    
    for name, module in model.named_children():
        replace_module(model, name, module)
        replace_modules_with_nonideality(module, ir_drop, sneak_factor, base_config)


def run_nonideality_sweep(
    checkpoint_path="checkpoints/V4_4bit_noise_hat_best.pt",
    ir_drop_levels=[0.0, 0.01, 0.02, 0.03],  # 0%, 1%, 2%, 3%
    sneak_levels=[0.0, 0.01, 0.02],  # 0%, 1%, 2%
    num_runs=10,
    device="cuda"
):
    """Run Tiny-ViT V4 inference with varying non-ideality levels.
    
    Based on ReRAM literature:
    - IR drop: 1-3% (position-dependent voltage drop)
    - Sneak paths: 1-2% (leakage between cells)
    """
    
    device = torch.device(device if torch.cuda.is_available() else "cpu")
    train_loader, test_loader = get_cifar10_loaders(batch_size=256)
    
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
    
    # Sweep both parameters
    for ir_drop in ir_drop_levels:
        for sneak in sneak_levels:
            key = f"IR{ir_drop*100:.0f}_SK{sneak*100:.0f}"
            print(f"\n{'='*60}")
            print(f"Testing: IR drop = {ir_drop*100:.0f}%, Sneak = {sneak*100:.0f}%")
            print(f"{'='*60}")
            
            accuracies = []
            
            for run in range(num_runs):
                model = get_tinyvit_model(
                    num_classes=10,
                    pretrained=True,
                    analog_config=base_config,
                )
                
                checkpoint = torch.load(checkpoint_path, map_location=device)
                model.load_state_dict(checkpoint["model_state_dict"], strict=False)
                
                replace_modules_with_nonideality(model, ir_drop, sneak, base_config)
                model = model.to(device)
                model.eval()
                
                for m in model.modules():
                    if hasattr(m, 'analog_enabled'):
                        m.analog_enabled = True
                
                acc = evaluate_model(model, test_loader, device, desc=f"Run {run+1}/{num_runs}")
                accuracies.append(acc)
                print(f"  Run {run+1}: {acc:.2f}%")
            
            import numpy as np
            mean_acc = np.mean(accuracies)
            std_acc = np.std(accuracies)
            
            results[key] = {
                "ir_drop": ir_drop,
                "sneak": sneak,
                "accuracies": accuracies,
                "mean": mean_acc,
                "std": std_acc,
            }
            
            print(f"\n  Summary: {mean_acc:.2f} ± {std_acc:.2f}%")
    
    # Save
    import json
    output_file = "report_md/_gpt/nonideality_sweep_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n{'='*60}")
    print("NON-IDEALITY SWEEP COMPLETE")
    print(f"{'='*60}")
    print(f"\nResults saved to: {output_file}")
    
    # Summary table
    print("\nSummary Table (Accuracy %):")
    print("{:<10}".format("IR\\Sneak"), end="")
    for sk in sneak_levels:
        print(f"{sk*100:>5.0f}%   ", end="")
    print()
    print("-" * (10 + 9 * len(sneak_levels)))
    
    baseline = results["IR0_SK0"]["mean"]
    for ir in ir_drop_levels:
        print(f"{ir*100:>5.0f}%     ", end="")
        for sk in sneak_levels:
            key = f"IR{ir*100:.0f}_SK{sk*100:.0f}"
            acc = results[key]["mean"]
            print(f"{acc:>5.1f}   ", end="")
        print()
    
    print(f"\nBaseline (ideal): {baseline:.2f}%")
    print("Degradation vs baseline:")
    for key, val in results.items():
        if key != "IR0_SK0":
            deg = baseline - val["mean"]
            print(f"  {key}: -{deg:.2f}%")
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Physical Non-Ideality Sensitivity Sweep")
    parser.add_argument("--checkpoint", default="checkpoints/V4_4bit_noise_hat_best.pt")
    parser.add_argument("--ir-drop", nargs="+", type=float, default=[0.0, 0.01, 0.02, 0.03])
    parser.add_argument("--sneak", nargs="+", type=float, default=[0.0, 0.01, 0.02])
    parser.add_argument("--runs", type=int, default=10)
    parser.add_argument("--device", default="cuda")
    
    args = parser.parse_args()
    
    results = run_nonideality_sweep(
        checkpoint_path=args.checkpoint,
        ir_drop_levels=args.ir_drop,
        sneak_levels=args.sneak,
        num_runs=args.runs,
        device=args.device,
    )
