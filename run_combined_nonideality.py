#!/usr/bin/env python3
"""
GM-E5: Combined Non-Ideality Stress Test.
Shows that Tiny-ViT (V4 Ensemble) remains functional even when all 
modeled non-idealities are active simultaneously.
"""

import torch
import torch.nn as nn
import numpy as np
import json
import os
from train_tinyvit import build_model, evaluate, get_dataloaders, set_seed, TinyViTExperimentConfig, DATASET_STATS
from inference_analysis_utils import ADCQuantHookManager, calibrate_adc_ranges
from dataclasses import replace
import dataclasses

def run_combined_stress():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    dataset = "cifar10"
    num_classes = DATASET_STATS[dataset]["num_classes"]
    ckpt_path = "checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt"
    
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    exp_cfg_dict = ckpt['exp_cfg']
    valid_keys = {f.name for f in dataclasses.fields(TinyViTExperimentConfig)}
    filtered_cfg_dict = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
    base_cfg = TinyViTExperimentConfig(**filtered_cfg_dict)
    
    # 1. SETUP COMBINED STRESS PARAMETERS
    base_cfg.sigma_c2c = 0.02
    base_cfg.sigma_d2d = 0.03
    base_cfg.noise_enabled = True
    base_cfg.ir_drop_factor = 0.01
    base_cfg.sneak_factor = 0.01
    base_cfg.retention_enabled = True
    base_cfg.inference_time = 1000.0
    adc_bits = 6
    
    _, train_loader = get_dataloaders(dataset, batch_size=256, num_workers=4)
    _, test_loader = get_dataloaders(dataset, batch_size=256, num_workers=4)
    criterion = nn.CrossEntropyLoss()
    
    print("\n--- Running Combined Stress Test ---")
    print(f"Settings: C2C={base_cfg.sigma_c2c}, D2D={base_cfg.sigma_d2d}, ADC={adc_bits}, IR={base_cfg.ir_drop_factor}, Sneak={base_cfg.sneak_factor}, Time={base_cfg.inference_time}s")
    
    set_seed(42)
    model = build_model(base_cfg, num_classes, device)
    model.load_state_dict(ckpt['model_state_dict'])
    
    # Calibration for ADC
    class Bundle:
        def __init__(self, model, loader, device):
            self.model = model
            self.testloader = loader
            self.device = device
            self.frontend = None
            self.amp_enabled = False
    
    bundle = Bundle(model, train_loader, device)
    print("Calibrating ADC ranges...")
    output_ranges = calibrate_adc_ranges(bundle, max_batches=5)
    
    with ADCQuantHookManager(model, output_ranges, adc_bits=adc_bits):
        _, acc = evaluate(model, test_loader, criterion, device, base_cfg)
    
    print(f"Final Accuracy under combined stress: {acc:.2f}%")
    
    # Save results
    results = {
        "combined_stress_accuracy": float(acc),
        "settings": {
            "sigma_c2c": base_cfg.sigma_c2c,
            "sigma_d2d": base_cfg.sigma_d2d,
            "adc_bits": adc_bits,
            "ir_drop": base_cfg.ir_drop_factor,
            "sneak": base_cfg.sneak_factor,
            "inference_time": base_cfg.inference_time
        }
    }
    output_path = "report_md/_gpt/combined_stress_results.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_combined_stress()
