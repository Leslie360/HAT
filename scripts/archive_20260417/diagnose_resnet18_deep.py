"""
Deep Diagnosis of ResNet-18 CIFAR-100 Issue

Systematically identify why ResNet-18 shows 1.00% accuracy
"""

import torch
import torch.nn as nn
import numpy as np
import sys

sys.path.insert(0, '/home/qiaosir/projects/compute_vit')

import torchvision.transforms as transforms
import torchvision

# Try to import ResNet training module
try:
    from train_resnet18 import (
        build_model, evaluate, get_dataloaders,
        DATASET_STATS, ExperimentConfig, load_experiment_config_from_checkpoint, set_seed
    )
    print("✓ train_resnet18 imported successfully")
except Exception as e:
    print(f"✗ Failed to import train_resnet18: {e}")
    sys.exit(1)

def diagnose_checkpoint(checkpoint_path, device='cuda'):
    """Comprehensive checkpoint diagnosis"""
    print("\n" + "="*70)
    print(f"DIAGNOSING: {checkpoint_path}")
    print("="*70)
    
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    
    # 1. Basic checkpoint info
    print("\n1. CHECKPOINT METADATA")
    print("-" * 40)
    print(f"  Epoch: {ckpt.get('epoch', 'N/A')}")
    print(f"  Best acc: {ckpt.get('best_acc', 'N/A')}")
    print(f"  Keys: {list(ckpt.keys())}")
    
    # 2. Config analysis
    exp_cfg_dict = ckpt.get('exp_cfg', {})
    print("\n2. TRAINING CONFIG")
    print("-" * 40)
    critical_params = ['use_analog', 'hat_training', 'noise_enabled', 'sigma_d2d', 'sigma_c2c', 'adc_bits', 'n_states']
    for param in critical_params:
        print(f"  {param}: {exp_cfg_dict.get(param, 'N/A')}")
    
    # 3. State dict analysis
    state_dict = ckpt['model_state_dict']
    print("\n3. STATE DICT ANALYSIS")
    print("-" * 40)
    print(f"  Total keys: {len(state_dict)}")
    
    # Check for ResNet-specific keys
    resnet_keys = [k for k in state_dict.keys() if 'layer' in k or 'conv' in k or 'fc' in k]
    print(f"  ResNet-like keys: {len(resnet_keys)}")
    
    # Check for D2D noise
    d2d_keys = [k for k in state_dict.keys() if 'd2d' in k.lower()]
    print(f"  D2D noise keys: {len(d2d_keys)}")
    
    # Check classifier
    classifier_keys = [k for k in state_dict.keys() if 'fc' in k or 'classifier' in k]
    print(f"  Classifier keys: {classifier_keys[:5]}")
    
    # 4. Weight statistics
    print("\n4. WEIGHT STATISTICS")
    print("-" * 40)
    
    # Sample a few layers
    sample_layers = ['conv1.weight', 'layer1.0.conv1.weight', 'layer4.1.conv2.weight', 'fc.weight']
    for layer_name in sample_layers:
        if layer_name in state_dict:
            w = state_dict[layer_name]
            print(f"  {layer_name}: shape={list(w.shape)}, mean={w.mean():.4f}, std={w.std():.4f}")
    
    return ckpt, exp_cfg_dict

def test_basic_inference(ckpt, exp_cfg_dict, dataset='cifar100', device='cuda'):
    """Test basic inference with exact training config"""
    print("\n" + "="*70)
    print(f"TEST: Basic Inference on {dataset.upper()}")
    print("="*70)
    
    # Build model with exact config
    cfg = load_experiment_config_from_checkpoint({"exp_cfg": exp_cfg_dict})
    
    print(f"\nConfig used:")
    print(f"  use_analog: {cfg.use_analog}")
    print(f"  hat_training: {cfg.hat_training}")
    print(f"  noise_enabled: {cfg.noise_enabled}")
    print(f"  sigma_d2d: {cfg.sigma_d2d}")
    print(f"  sigma_c2c: {cfg.sigma_c2c}")
    
    num_classes = DATASET_STATS[dataset]['num_classes']
    _, loader = get_dataloaders(dataset, batch_size=256)
    
    # Test 1: Load and evaluate as-is
    print("\n1. EVALUATE AS-IS (with loaded D2D)")
    print("-" * 40)
    
    model = build_model(cfg, num_classes, device)
    model.load_state_dict(ckpt['model_state_dict'])
    model.eval()
    
    acc = evaluate(model, loader, device)
    print(f"  Accuracy: {acc:.2f}%")
    
    # Test 2: Evaluate with noise disabled
    print("\n2. EVALUATE WITH NOISE DISABLED")
    print("-" * 40)
    
    cfg_noise_off = load_experiment_config_from_checkpoint({"exp_cfg": exp_cfg_dict})
    cfg_noise_off.noise_enabled = False
    cfg_noise_off.sigma_d2d = 0.0
    cfg_noise_off.sigma_c2c = 0.0
    
    model2 = build_model(cfg_noise_off, num_classes, device)
    # Try to load weights (might fail due to D2D noise shape mismatch)
    try:
        model2.load_state_dict(ckpt['model_state_dict'], strict=False)
        acc2 = evaluate(model2, loader, device)
        print(f"  Accuracy: {acc2:.2f}%")
    except Exception as e:
        print(f"  Error: {e}")
    
    # Test 3: Check output distribution
    print("\n3. OUTPUT DISTRIBUTION ANALYSIS")
    print("-" * 40)
    
    model.eval()
    with torch.no_grad():
        # Get one batch
        for inputs, labels in loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            
            print(f"  Output shape: {outputs.shape}")
            print(f"  Output range: [{outputs.min():.2f}, {outputs.max():.2f}]")
            print(f"  Output mean: {outputs.mean():.4f}")
            print(f"  Output std: {outputs.std():.4f}")
            
            # Check predictions
            _, predicted = outputs.max(1)
            print(f"  Predicted classes: {predicted[:20].tolist()}")
            print(f"  Unique predictions: {predicted.unique().numel()}/{num_classes}")
            print(f"  Prediction distribution: {predicted.bincount(minlength=num_classes)[:10]}")
            
            # Check if all predictions are the same
            if predicted.unique().numel() == 1:
                print(f"  ⚠️  ALL PREDICTIONS ARE THE SAME CLASS: {predicted[0].item()}")
            
            break
    
    return acc

def compare_train_eval_mismatch(ckpt, exp_cfg_dict, device='cuda'):
    """Compare training vs evaluation config differences"""
    print("\n" + "="*70)
    print("ANALYSIS: Training vs Evaluation Config Mismatch")
    print("="*70)
    
    # What was the training config?
    print("\nTraining config (from checkpoint):")
    train_noise = exp_cfg_dict.get('noise_enabled', False)
    train_hat = exp_cfg_dict.get('hat_training', False)
    print(f"  noise_enabled: {train_noise}")
    print(f"  hat_training: {train_hat}")
    
    # What happens in evaluation?
    print("\nEvaluation behavior:")
    print("  If noise_enabled=True and hat_training=False:")
    print("    → Uses training-time D2D noise (fixed)")
    print("  If noise_enabled=True and hat_training=True:")
    print("    → Should resample D2D per epoch (Ensemble HAT)")
    
    # Check for common issues
    issues = []
    
    if train_noise and not train_hat:
        issues.append("Standard HAT: Fixed D2D, should work on training instance but fail on fresh instances")
    
    if not train_noise:
        issues.append("No noise during training: model not trained with noise")
    
    if train_hat and train_noise:
        issues.append("Ensemble HAT: Should work with D2D resampling")
    
    print(f"\nPotential issues identified: {len(issues)}")
    for issue in issues:
        print(f"  - {issue}")

def diagnose_data_pipeline(dataset='cifar100', device='cuda'):
    """Check data pipeline"""
    print("\n" + "="*70)
    print(f"DIAGNOSIS: Data Pipeline for {dataset.upper()}")
    print("="*70)
    
    _, loader = get_dataloaders(dataset, batch_size=256)
    
    # Check a few batches
    print("\nData batch analysis:")
    for i, (inputs, labels) in enumerate(loader):
        print(f"  Batch {i+1}:")
        print(f"    Input shape: {inputs.shape}")
        print(f"    Input range: [{inputs.min():.2f}, {inputs.max():.2f}]")
        print(f"    Labels: {labels[:20].tolist()}")
        print(f"    Unique labels: {labels.unique().numel()}/{DATASET_STATS[dataset]['num_classes']}")
        
        if i >= 2:
            break

def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print("="*70)
    print("ResNet-18 Deep Diagnosis")
    print("="*70)
    print(f"Device: {device}")
    
    # Find checkpoint
    checkpoint_candidates = [
        'checkpoints/R4_4bit_noise_HAT_best.pt',
        'checkpoints/R6_6bit_noise_HAT_best.pt',
        'checkpoints/R3_4bit_noise_standard_best.pt',
    ]
    
    checkpoint_path = None
    for path in checkpoint_candidates:
        if os.path.exists(path):
            checkpoint_path = path
            break
    
    if not checkpoint_path:
        print("ERROR: No ResNet-18 checkpoint found!")
        return
    
    # Run diagnosis
    ckpt, exp_cfg_dict = diagnose_checkpoint(checkpoint_path, device)
    
    # Test on both datasets
    for dataset in ['cifar10', 'cifar100']:
        try:
            test_basic_inference(ckpt, exp_cfg_dict, dataset, device)
        except Exception as e:
            print(f"\nERROR during {dataset} inference: {e}")
            import traceback
            traceback.print_exc()
    
    # Config analysis
    compare_train_eval_mismatch(ckpt, exp_cfg_dict, device)
    
    # Data pipeline
    diagnose_data_pipeline('cifar100', device)
    
    print("\n" + "="*70)
    print("DIAGNOSIS COMPLETE")
    print("="*70)

if __name__ == '__main__':
    import os
    main()
