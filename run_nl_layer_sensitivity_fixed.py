#!/usr/bin/env python3
"""
Fixed NL Layer-wise Sensitivity Script (GM-KP-1)
Loads a trained checkpoint first!
"""

import torch
import torch.nn as nn
import json
import os
import dataclasses
from pathlib import Path
from train_tinyvit import build_model, TinyViTExperimentConfig, get_dataloaders, evaluate

def apply_nl_to_group(model, target_group, nl_val=2.0):
    """
    Inject NL only into specific groups.
    Groups: 'patch_embed', 'blocks.0', 'blocks.2', 'blocks.5', 'head'
    """
    count = 0
    for name, m in model.named_modules():
        if hasattr(m, 'config'):
            if target_group == 'all' or target_group in name:
                m.config.nl_ltp = nl_val
                m.config.nl_ltd = -nl_val
                count += 1
            else:
                m.config.nl_ltp = 1.0
                m.config.nl_ltd = -1.0
    return count

def run_sensitivity():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    ckpt_path = "checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt"
    if not os.path.exists(ckpt_path):
        # Fallback to canonical V4
        ckpt_path = "checkpoints/V4_hybrid_standard_noise_hat_best.pt"
    
    print(f"Loading checkpoint: {ckpt_path}")
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    
    exp_cfg_dict = ckpt['exp_cfg']
    valid_keys = {f.name for f in dataclasses.fields(TinyViTExperimentConfig)}
    filtered_cfg_dict = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
    exp_cfg = TinyViTExperimentConfig(**filtered_cfg_dict)
    
    # Baseline check: 5% C2C, 10% D2D, 8-bit ADC, NO NL
    exp_cfg.adc_bits = 8
    
    groups = ['baseline_linear', 'patch_embed', 'blocks.0', 'blocks.2', 'blocks.5', 'head', 'all']
    results = {}

    _, test_loader = get_dataloaders("cifar10", batch_size=128, num_workers=4)
    criterion = nn.CrossEntropyLoss()

    for group in groups:
        print(f"\n[+] Testing group: {group}")
        # Build fresh model to avoid config pollution
        model = build_model(exp_cfg, num_classes=10, device=device)
        model.load_state_dict(ckpt['model_state_dict'], strict=True)
        
        if group == 'baseline_linear':
            layers_affected = apply_nl_to_group(model, 'none', nl_val=1.0)
        else:
            layers_affected = apply_nl_to_group(model, group, nl_val=2.0)
            
        print(f"    Layers affected: {layers_affected}")
        
        # Since NL only affects backward, how do we test sensitivity?
        # WE MUST FINE-TUNE! 
        # But wait, Claude's CORRECTION_BROADCAST says the 15% was a bug.
        # If NL only affects backward, then a pure eval should indeed give 91% for ALL groups.
        # If the previous results were 15%, it means the model was broken during LOAD or CONFIG.
        
        loss, acc = evaluate(model, test_loader, criterion, device, exp_cfg)
        print(f"    Inference Accuracy: {acc:.2f}%")
        results[group] = acc

    # Save results
    output_path = "report_md/_gpt/layer_wise_nl_sensitivity_corrected.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {output_path}")

if __name__ == "__main__":
    run_sensitivity()
