#!/usr/bin/env python3
"""Quick CPU diagnostic for fresh-instance standard HAT collapse (tiny subset)."""
import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""

import torch
import torch.nn as nn
import numpy as np

from train_tinyvit_ensemble import (
    build_model, get_dataloaders, resample_all_d2d_noise
)
from train_tinyvit import set_seed

CHECKPOINT = "checkpoints/V4_hybrid_standard_noise_hat_best.pt"
DEVICE = "cpu"
SUBSET_SIZE = 128

def get_subset_loader(batch_size=128):
    _, testloader = get_dataloaders(dataset="cifar10", batch_size=batch_size, num_workers=0, data_root="./data")
    all_data = []
    all_labels = []
    for inputs, targets in testloader:
        all_data.append(inputs)
        all_labels.append(targets)
        if sum(d.shape[0] for d in all_data) >= SUBSET_SIZE:
            break
    all_data = torch.cat(all_data)[:SUBSET_SIZE]
    all_labels = torch.cat(all_labels)[:SUBSET_SIZE]
    subset = torch.utils.data.TensorDataset(all_data, all_labels)
    return torch.utils.data.DataLoader(subset, batch_size=batch_size, shuffle=False)

def eval_on_loader(model, loader, criterion, device):
    model.eval()
    running_loss, correct, total = 0.0, 0, 0
    preds = []
    with torch.no_grad():
        for inputs, targets in loader:
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            running_loss += loss.item() * inputs.size(0)
            _, predicted = outputs.max(1)
            correct += predicted.eq(targets).sum().item()
            total += targets.size(0)
            preds.extend(predicted.cpu().numpy().tolist())
    return running_loss / total, 100.0 * correct / total, np.array(preds)

def main():
    print(f"Loading checkpoint: {CHECKPOINT}")
    ckpt = torch.load(CHECKPOINT, map_location=DEVICE, weights_only=False)
    cfg_dict = ckpt.get("exp_cfg", {})
    from dataclasses import fields
    from train_tinyvit_ensemble import TinyViTExperimentConfig
    valid_keys = {f.name for f in fields(TinyViTExperimentConfig)}
    filtered = {k: v for k, v in cfg_dict.items() if k in valid_keys}
    cfg = TinyViTExperimentConfig(**filtered)
    
    print(f"Config: hat_training={cfg.hat_training}, noise_enabled={cfg.noise_enabled}, "
          f"sigma_c2c={cfg.sigma_c2c}, sigma_d2d={cfg.sigma_d2d}, noise_mode={cfg.noise_mode}")
    
    loader = get_subset_loader(batch_size=128)
    criterion = nn.CrossEntropyLoss()
    
    # Original D2D
    print("\n--- Original D2D ---")
    model = build_model(cfg, num_classes=10, device=DEVICE, pretrained=False)
    model.load_state_dict(ckpt["model_state_dict"], strict=True)
    loss, acc, preds = eval_on_loader(model, loader, criterion, DEVICE)
    print(f"Accuracy: {acc:.2f}%  Loss: {loss:.4f}")
    print(f"Pred dist: {dict(zip(*np.unique(preds, return_counts=True)))}")
    
    # Fresh D2D
    print("\n--- Fresh D2D (seed=42) ---")
    set_seed(42)
    model2 = build_model(cfg, num_classes=10, device=DEVICE, pretrained=False)
    model2.load_state_dict(ckpt["model_state_dict"], strict=True)
    resample_all_d2d_noise(model2)
    loss2, acc2, preds2 = eval_on_loader(model2, loader, criterion, DEVICE)
    print(f"Accuracy: {acc2:.2f}%  Loss: {loss2:.4f}")
    unique, counts = np.unique(preds2, return_counts=True)
    print(f"Pred dist: {dict(zip(unique.tolist(), counts.tolist()))}")
    most_common = unique[np.argmax(counts)]
    print(f"Most predicted class: {most_common} ({counts.max()} times = {counts.max()/len(preds2)*100:.1f}%)")

if __name__ == "__main__":
    main()
