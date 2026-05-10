import sys
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src" / "compute_vit"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import torch
import torch.nn as nn
import numpy as np
import json
import os
from train_tinyvit import build_model, evaluate, get_dataloaders, TinyViTExperimentConfig, DATASET_STATS, set_seed
import dataclasses

def resample_all_d2d_noise(model):
    """Force all analog layers to resample their fixed D2D mismatch buffers."""
    for m in model.modules():
        if hasattr(m, 'resample_d2d_noise'):
            m.resample_d2d_noise()

def run_ablation():
    device = 'cuda'
    dataset = 'cifar10'
    num_classes = DATASET_STATS[dataset]['num_classes']
    ckpt_path = 'checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt'
    
    print(f"Loading Ensemble Checkpoint: {ckpt_path}")
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    exp_cfg_dict = ckpt['exp_cfg']
    valid_keys = {f.name for f in dataclasses.fields(TinyViTExperimentConfig)}
    filtered = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
    cfg = TinyViTExperimentConfig(**filtered)
    cfg.noise_enabled = True
    
    _, loader = get_dataloaders(dataset, batch_size=256)
    criterion = nn.CrossEntropyLoss()
    
    ensemble_accs = []
    
    print("\n--- Evaluating Ensemble HAT (V4) on 10 Fresh Instances ---")
    for i in range(10):
        # We need a new model instance each time to ensure isolation
        set_seed(42 + i)
        model = build_model(cfg, num_classes, device)
        model.load_state_dict(ckpt['model_state_dict'])
        
        # KEY ACTION: Simulating fresh hardware
        resample_all_d2d_noise(model)
        
        _, acc = evaluate(model, loader, criterion, device, cfg)
        ensemble_accs.append(acc)
        print(f"Instance {i+1}: Accuracy = {acc:.2f}%")
        
    results = {
        "ensemble_hat": {
            "mean": float(np.mean(ensemble_accs)),
            "std": float(np.std(ensemble_accs)),
            "raw": ensemble_accs
        }
    }

    # Save results
    output_path = "report_md/_gpt/ablation_ensemble_results.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\nAblation data saved to {output_path}")

if __name__ == "__main__":
    run_ablation()
