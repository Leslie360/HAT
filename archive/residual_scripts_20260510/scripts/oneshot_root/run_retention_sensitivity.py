#!/usr/bin/env python3
"""
GM-E3: Retention Sensitivity Sweep.
Quantifies how accuracy degrades over time and how sensitive it is to 
the choice of A_0 and Tau proxy parameters.
"""

import torch
import torch.nn as nn
import numpy as np
import json
import os
from train_tinyvit import build_model, evaluate, get_dataloaders, set_seed, TinyViTExperimentConfig, DATASET_STATS
from dataclasses import replace
import dataclasses

def run_retention_sensitivity():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    dataset = "cifar10"
    num_classes = DATASET_STATS[dataset]["num_classes"]
    # Using the verified ensemble checkpoint
    ckpt_path = "checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt"
    
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    exp_cfg_dict = ckpt['exp_cfg']
    valid_keys = {f.name for f in dataclasses.fields(TinyViTExperimentConfig)}
    filtered_cfg_dict = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
    base_cfg = TinyViTExperimentConfig(**filtered_cfg_dict)
    
    # Ensure retention is enabled and noise is on for MC eval
    base_cfg.retention_enabled = True
    base_cfg.noise_enabled = True
    
    _, test_loader = get_dataloaders(dataset, batch_size=256, num_workers=4)
    criterion = nn.CrossEntropyLoss()
    
    times = [1, 100, 1000, 10000]
    a0_values = [0.4, 0.6, 0.8] # persistent fraction
    
    results = []
    
    for a0 in a0_values:
        for t in times:
            print(f"\nTesting A_0 = {a0}, time = {t}s")
            set_seed(42)
            
            # Create config override
            # We override AnalogLinearConfig properties via build_model passthrough if supported, 
            # or we might need to modify build_model. 
            # Current build_model doesn't take A_0 as param. I will use a config patcher.
            
            current_cfg = replace(base_cfg, inference_time=float(t))
            
            model = build_model(current_cfg, num_classes, device)
            
            # Manually patch the modules with the desired A_0
            for m in model.modules():
                if hasattr(m, 'config') and hasattr(m.config, 'A_0'):
                    m.config.A_0 = a0
                    # V7 logic uses recalibrate_scale=True and scale_d2d=True
                    m.config.retention_recalibrate_scale = True
                    m.config.retention_scales_d2d = True
            
            model.load_state_dict(ckpt['model_state_dict'])
            
            _, acc = evaluate(model, test_loader, criterion, device, current_cfg)
            
            results.append({
                "A_0": a0,
                "time_s": t,
                "accuracy": float(acc)
            })
            print(f"Accuracy: {acc:.2f}%")
            
    # Save results
    output_path = "report_md/_gpt/retention_sensitivity_results.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nRetention sensitivity data saved to {output_path}")

if __name__ == "__main__":
    run_retention_sensitivity()
