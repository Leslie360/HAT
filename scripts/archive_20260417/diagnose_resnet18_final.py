"""
Final Diagnosis of ResNet-18 CIFAR-100 Issue

Root cause analysis with correct API usage
"""

import torch
import torch.nn as nn
import numpy as np
import random
import sys
import os

sys.path.insert(0, '/home/qiaosir/projects/compute_vit')

import torchvision.transforms as transforms
import torchvision

from train_resnet18 import (
    build_model, evaluate, get_dataloaders,
    ExperimentConfig, load_experiment_config_from_checkpoint, set_noise_for_eval
)

def set_seed(seed=42):
    import random
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

def diagnose_r4_checkpoint():
    """Diagnose the R4 (HAT) checkpoint"""
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    
    print("="*70)
    print("ResNet-18 R4 (HAT) Checkpoint Diagnosis")
    print("="*70)
    
    checkpoint_path = 'checkpoints/R4_4bit_noise_HAT_best.pt'
    if not os.path.exists(checkpoint_path):
        print(f"ERROR: Checkpoint not found: {checkpoint_path}")
        return
    
    ckpt = torch.load(checkpoint_path, map_location=device)
    
    print(f"\nCheckpoint: {checkpoint_path}")
    print(f"  Epoch: {ckpt.get('epoch', 'N/A')}")
    print(f"  Best acc: {ckpt.get('best_acc', 'N/A')}")
    
    # Get config
    cfg = load_experiment_config_from_checkpoint(ckpt)
    
    print(f"\nConfig from checkpoint:")
    print(f"  use_analog: {cfg.use_analog}")
    print(f"  hat_training: {cfg.hat_training}")
    print(f"  noise_enabled: {cfg.noise_enabled}")
    print(f"  sigma_c2c: {cfg.sigma_c2c}")
    print(f"  sigma_d2d: {cfg.sigma_d2d}")
    print(f"  n_states: {cfg.n_states}")
    
    # Test on CIFAR-10
    print("\n" + "="*70)
    print("TEST 1: CIFAR-10")
    print("="*70)
    
    _, loader_c10 = get_dataloaders('cifar10', batch_size=256)
    criterion = nn.CrossEntropyLoss()
    
    model_c10 = build_model(cfg, num_classes=10, device=device)
    model_c10.load_state_dict(ckpt['model_state_dict'])
    
    loss_c10, acc_c10 = evaluate(model_c10, loader_c10, criterion, device, cfg)
    print(f"  Loss: {loss_c10:.4f}")
    print(f"  Accuracy: {acc_c10:.2f}%")
    
    # Test on CIFAR-100
    print("\n" + "="*70)
    print("TEST 2: CIFAR-100")
    print("="*70)
    
    _, loader_c100 = get_dataloaders('cifar100', batch_size=256)
    
    model_c100 = build_model(cfg, num_classes=100, device=device)
    
    # Check state dict compatibility
    state_dict = ckpt['model_state_dict']
    print(f"\n  State dict keys (sample):")
    for k in list(state_dict.keys())[:5]:
        print(f"    {k}: {state_dict[k].shape}")
    
    # Try loading
    try:
        model_c100.load_state_dict(state_dict)
        print(f"  ✓ State dict loaded successfully")
    except Exception as e:
        print(f"  ✗ State dict loading failed: {e}")
        return
    
    loss_c100, acc_c100 = evaluate(model_c100, loader_c100, criterion, device, cfg)
    print(f"  Loss: {loss_c100:.4f}")
    print(f"  Accuracy: {acc_c100:.2f}%")
    
    # Detailed analysis if accuracy is low
    if acc_c100 < 10.0:
        print("\n" + "="*70)
        print("DETAILED ANALYSIS: Why is accuracy ~1%?")
        print("="*70)
        
        model_c100.eval()
        set_noise_for_eval(model_c100, cfg)
        
        with torch.no_grad():
            for inputs, labels in loader_c100:
                inputs = inputs.to(device)
                outputs = model_c100(inputs)
                
                print(f"\n  Output statistics:")
                print(f"    Shape: {outputs.shape}")
                print(f"    Range: [{outputs.min():.2f}, {outputs.max():.2f}]")
                print(f"    Mean: {outputs.mean():.4f}")
                print(f"    Std: {outputs.std():.4f}")
                
                _, predicted = outputs.max(1)
                print(f"\n  Prediction statistics:")
                print(f"    First 20 predictions: {predicted[:20].tolist()}")
                print(f"    Unique predictions: {predicted.unique().numel()}/100")
                
                # Class distribution
                class_counts = predicted.bincount(minlength=100)
                print(f"    Top-5 predicted classes: {class_counts.topk(5).indices.tolist()}")
                print(f"    Top-5 counts: {class_counts.topk(5).values.tolist()}")
                
                if predicted.unique().numel() == 1:
                    print(f"\n  ⚠️  CRITICAL: ALL predictions are class {predicted[0].item()}")
                
                break

def test_config_variations():
    """Test different configurations to isolate the issue"""
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    checkpoint_path = 'checkpoints/R4_4bit_noise_HAT_best.pt'
    
    print("\n" + "="*70)
    print("CONFIG VARIATION TESTS")
    print("="*70)
    
    ckpt = torch.load(checkpoint_path, map_location=device)
    _, loader = get_dataloaders('cifar100', batch_size=256)
    criterion = nn.CrossEntropyLoss()
    
    variations = [
        ("Original config (noise ON)", {'noise_enabled': True, 'hat_training': True}),
        ("Noise OFF", {'noise_enabled': False, 'hat_training': False}),
        ("C2C only (no D2D)", {'noise_enabled': True, 'sigma_c2c': 0.05, 'sigma_d2d': 0.0}),
        ("D2D only (no C2C)", {'noise_enabled': True, 'sigma_c2c': 0.0, 'sigma_d2d': 0.10}),
    ]
    
    for name, overrides in variations:
        print(f"\n{name}:")
        
        cfg = load_experiment_config_from_checkpoint(ckpt)
        
        # Apply overrides
        for k, v in overrides.items():
            setattr(cfg, k, v)
        
        model = build_model(cfg, num_classes=100, device=device)
        try:
            model.load_state_dict(ckpt['model_state_dict'])
            loss, acc = evaluate(model, loader, criterion, device, cfg)
            print(f"  Accuracy: {acc:.2f}%")
        except Exception as e:
            print(f"  Error: {e}")

def main():
    set_seed(42)
    
    diagnose_r4_checkpoint()
    test_config_variations()
    
    print("\n" + "="*70)
    print("DIAGNOSIS COMPLETE")
    print("="*70)

if __name__ == '__main__':
    main()
