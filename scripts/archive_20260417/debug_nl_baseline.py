#!/usr/bin/env python3
"""
Debug Script for GM-KP-1: Layer-wise NL Evaluation.
"""

import torch
import torch.nn as nn
import os
import sys
import dataclasses
from train_tinyvit import build_model, get_dataloaders, evaluate, TinyViTExperimentConfig

def debug_nl_baseline():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    ckpt_path = "checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt"
    if not os.path.exists(ckpt_path):
        print(f"Checkpoint not found: {ckpt_path}")
        return

    print(f"\n[+] Loading {ckpt_path}...")
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    
    # Reconstruct config
    exp_cfg_dict = ckpt['exp_cfg']
    valid_keys = {f.name for f in dataclasses.fields(TinyViTExperimentConfig)}
    filtered_cfg_dict = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
    exp_cfg = TinyViTExperimentConfig(**filtered_cfg_dict)
    
    # ENSURE NO NOISE FOR BASELINE EVAL if that's what we want, 
    # OR follow canonical V4 noise settings.
    # The reviewer wants a "baseline_linear" which should match the checkpoint's performance.
    # Canonical V4 uses sigma_c2c=0.05, sigma_d2d=0.1.
    print(f"Config: sigma_c2c={exp_cfg.sigma_c2c}, sigma_d2d={exp_cfg.sigma_d2d}, hat={exp_cfg.hat_training}")

    # Build model
    model = build_model(exp_cfg, num_classes=10, device=device)
    model.load_state_dict(ckpt['model_state_dict'], strict=True)
    
    _, test_loader = get_dataloaders("cifar10", batch_size=256, num_workers=4)
    criterion = nn.CrossEntropyLoss()

    print("Evaluating Baseline (No additional NL)...")
    loss, acc = evaluate(model, test_loader, criterion, device, exp_cfg)
    print(f"Accuracy: {acc:.2f}% (Expected ~91% if canonical, or ~86% if Ensemble HAT)")
    print(f"Checkpoint reported best_acc: {ckpt.get('best_acc', 'N/A')}%")

if __name__ == "__main__":
    debug_nl_baseline()
