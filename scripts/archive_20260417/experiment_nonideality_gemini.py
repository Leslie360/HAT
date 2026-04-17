#!/usr/bin/env python3
"""
EXP-B: Physical Non-Ideality Sensitivity Sweep
Tests IR drop and Sneak path effects on Tiny-ViT (V4)
"""

import torch
import torch.nn as nn
import numpy as np
import json
import os
from train_tinyvit import build_model, evaluate, get_dataloaders, set_seed, TinyViTExperimentConfig, DATASET_STATS
from dataclasses import replace
import dataclasses

def run_experiment():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    dataset = "cifar10"
    num_classes = DATASET_STATS[dataset]["num_classes"]
    
    # Load checkpoint to get its config
    ckpt_path = "checkpoints/V4_hybrid_standard_noise_hat_best.pt"
    if not os.path.exists(ckpt_path):
        print(f"Error: Checkpoint {ckpt_path} not found.")
        return
    
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    exp_cfg_dict = ckpt['exp_cfg']
    
    # Filter keys for TinyViTExperimentConfig
    valid_keys = {f.name for f in dataclasses.fields(TinyViTExperimentConfig)}
    filtered_cfg_dict = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
    base_cfg = TinyViTExperimentConfig(**filtered_cfg_dict)
    
    # Enable noise for MC evaluation
    base_cfg.noise_enabled = True 
    
    ir_drop_levels = [0.0, 0.01, 0.02, 0.03]
    sneak_levels = [0.0, 0.01, 0.02]
    num_runs = 5
    results = []
    
    # Prepare dataloader
    _, test_loader = get_dataloaders(dataset, batch_size=256, num_workers=4)
    criterion = nn.CrossEntropyLoss()
    
    for ir in ir_drop_levels:
        for sneak in sneak_levels:
            print(f"\n{'='*60}")
            print(f"Testing IR drop = {ir*100:.1f}%, Sneak path = {sneak*100:.1f}%")
            print(f"{'='*60}")
            
            accuracies = []
            
            for run in range(num_runs):
                seed = 42 + run
                set_seed(seed)
                
                # Create config with current levels
                current_cfg = replace(base_cfg, ir_drop_factor=ir, sneak_factor=sneak)
                
                # Build model
                model = build_model(current_cfg, num_classes, device)
                
                # Load weights
                model.load_state_dict(ckpt['model_state_dict'])
                model.to(device)
                
                # Evaluate
                _, acc = evaluate(model, test_loader, criterion, device, current_cfg)
                accuracies.append(acc)
                print(f"Run {run+1}/{num_runs}: Accuracy = {acc:.2f}%")
                
            res = {
                "ir_drop": ir,
                "sneak_path": sneak,
                "mean": float(np.mean(accuracies)),
                "std": float(np.std(accuracies)),
                "accuracies": accuracies,
            }
            results.append(res)
            print(f"Result for IR={ir}, Sneak={sneak}: Mean = {np.mean(accuracies):.2f}%, Std = {np.std(accuracies):.2f}%")
    
    # Save results
    output_path = "report_md/_gpt/nonideality_sweep_results_gemini.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nFinal results saved to {output_path}")
    return results

if __name__ == "__main__":
    run_experiment()
