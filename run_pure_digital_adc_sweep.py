#!/usr/bin/env python3
"""
GM-E2: Pure Digital ADC Sweep Control (Corrected with Calibration).
Separates the impact of ADC quantization from analog noise.
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

def run_adc_sweep():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    dataset = "cifar10"
    num_classes = DATASET_STATS[dataset]["num_classes"]
    # Using the verified ensemble checkpoint for consistency
    ckpt_path = "checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt"
    
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    exp_cfg_dict = ckpt['exp_cfg']
    valid_keys = {f.name for f in dataclasses.fields(TinyViTExperimentConfig)}
    filtered_cfg_dict = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
    base_cfg = TinyViTExperimentConfig(**filtered_cfg_dict)
    
    # 1. DISABLE ALL ANALOG NOISE
    base_cfg.sigma_c2c = 0.0
    base_cfg.sigma_d2d = 0.0
    base_cfg.noise_enabled = False
    
    # 2. Setup Dataloaders
    train_loader, test_loader = get_dataloaders(dataset, batch_size=256, num_workers=4)
    criterion = nn.CrossEntropyLoss()
    
    # 3. Calibration: Capture activation ranges for ADC quantization
    # We use a temporary model instance for calibration
    temp_model = build_model(base_cfg, num_classes, device)
    temp_model.load_state_dict(ckpt['model_state_dict'])
    
    # Mock 'bundle' object expected by calibrate_adc_ranges
    class Bundle:
        def __init__(self, model, loader, device):
            self.model = model
            self.testloader = loader
            self.device = device
            self.frontend = None
            self.amp_enabled = False
    
    bundle = Bundle(temp_model, test_loader, device)
    print("Calibrating ADC ranges...")
    output_ranges = calibrate_adc_ranges(bundle, max_batches=5)
    print(f"Captured ranges for {len(output_ranges)} layers.")
    
    adc_bits_to_test = [4, 5, 6, 7, 8]
    results = {}
    
    for bits in adc_bits_to_test:
        print(f"\nTesting Pure Digital ADC = {bits} bits")
        set_seed(42)
        # Use hooks to apply ADC quantization with calibrated ranges
        with ADCQuantHookManager(temp_model, output_ranges, adc_bits=bits):
            _, acc = evaluate(temp_model, test_loader, criterion, device, base_cfg)
        
        results[bits] = float(acc)
        print(f"Accuracy: {acc:.2f}%")
        
    # Save results
    output_path = "report_md/_gpt/pure_digital_adc_sweep.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nPure digital ADC data saved to {output_path}")

if __name__ == "__main__":
    run_adc_sweep()
