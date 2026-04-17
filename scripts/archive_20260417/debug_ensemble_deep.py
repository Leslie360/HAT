"""
Deep debug of Ensemble HAT evaluation
"""

import torch
import torch.nn as nn
import numpy as np
import sys

sys.path.insert(0, '/home/qiaosir/projects/compute_vit')

import torchvision.transforms as transforms
import torchvision
import timm

from analog_layers import AnalogLinear, AnalogConv2d, AnalogLinearConfig, convert_to_hybrid

def get_loader():
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.4914, 0.4822, 0.4465), (0.2023, 0.1994, 0.2010)),
    ])
    dataset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)
    return torch.utils.data.DataLoader(dataset, batch_size=256, shuffle=False, num_workers=2)

def evaluate(model, loader, device):
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for inputs, targets in loader:
            inputs, targets = inputs.to(device), targets.to(device)
            outputs = model(inputs)
            _, predicted = outputs.max(1)
            correct += predicted.eq(targets).sum().item()
            total += targets.size(0)
    return 100.0 * correct / total

def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    checkpoint_path = 'checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt'
    
    checkpoint = torch.load(checkpoint_path, map_location=device)
    print(f"Checkpoint epoch: {checkpoint['epoch']}")
    print(f"Checkpoint best_acc: {checkpoint['best_acc']:.2f}%")
    
    # Check what module was used during training
    sample_key = list(checkpoint['model_state_dict'].keys())[0]
    print(f"\nSample state_dict key: {sample_key}")
    
    # Build model with EXACT same config as training
    model = timm.create_model("tiny_vit_5m_224", pretrained=False, num_classes=10)
    
    cfg = AnalogLinearConfig(
        n_states=16,
        sigma_c2c=0.05,
        sigma_d2d=0.10,
        noise_enabled=True,
        noise_mode="uniform",
        NL_LTP=1.0,
        NL_LTD=-1.0,
        retention_enabled=False,
        inference_time=0.0,
        restore_weight_scale=True,  # Critical
    )
    
    model = convert_to_hybrid(model, config=cfg, verbose=False)
    model = model.to(device)
    
    # Load state dict
    model.load_state_dict(checkpoint['model_state_dict'])
    
    loader = get_loader()
    
    # Test 1: Eval as-is (should use loaded D2D noise)
    print("\n" + "="*70)
    print("Test 1: Evaluate with loaded D2D (no changes)")
    print("="*70)
    
    # Check D2D noise stats before eval
    d2d_stats = []
    for name, m in model.named_modules():
        if isinstance(m, (AnalogLinear, AnalogConv2d)):
            if hasattr(m, 'd2d_noise'):
                d2d_stats.append({
                    'name': name,
                    'mean': m.d2d_noise.mean().item(),
                    'std': m.d2d_noise.std().item(),
                    'shape': list(m.d2d_noise.shape)
                })
    
    print(f"Found {len(d2d_stats)} layers with d2d_noise")
    print(f"Sample D2D stats: mean={d2d_stats[0]['mean']:.4f}, std={d2d_stats[0]['std']:.4f}")
    
    acc1 = evaluate(model, loader, device)
    print(f"Accuracy: {acc1:.2f}%")
    
    # Test 2: Check if D2D is actually being used
    print("\n" + "="*70)
    print("Test 2: Disable noise and evaluate")
    print("="*70)
    
    model2 = timm.create_model("tiny_vit_5m_224", pretrained=False, num_classes=10)
    cfg2 = AnalogLinearConfig(
        n_states=16,
        sigma_c2c=0.0,
        sigma_d2d=0.0,
        noise_enabled=False,  # Disabled
        restore_weight_scale=True,
    )
    model2 = convert_to_hybrid(model2, config=cfg2, verbose=False)
    model2 = model2.to(device)
    model2.load_state_dict(checkpoint['model_state_dict'], strict=False)
    
    acc2 = evaluate(model2, loader, device)
    print(f"Accuracy (noise disabled): {acc2:.2f}%")
    
    # Test 3: Check analog layer count
    print("\n" + "="*70)
    print("Test 3: Layer analysis")
    print("="*70)
    
    analog_count = 0
    total_params = 0
    analog_params = 0
    
    for name, m in model.named_modules():
        if isinstance(m, (AnalogLinear, AnalogConv2d)):
            analog_count += 1
            analog_params += sum(p.numel() for p in m.parameters())
        total_params += sum(p.numel() for p in m.parameters())
    
    print(f"Analog layers: {analog_count}")
    print(f"Total params: {total_params:,}")
    print(f"Analog params: {analog_params:,}")
    
    # Test 4: Verify state dict was loaded correctly
    print("\n" + "="*70)
    print("Test 4: Verify weight loading")
    print("="*70)
    
    # Get a sample weight from checkpoint
    sample_weight_key = 'patch_embed.conv1.conv.weight'
    ckpt_weight = checkpoint['model_state_dict'][sample_weight_key]
    model_weight = dict(model.named_parameters())[sample_weight_key]
    
    diff = (ckpt_weight - model_weight).abs().max().item()
    print(f"Max weight diff for {sample_weight_key}: {diff:.8f}")
    print(f"  Checkpoint weight range: [{ckpt_weight.min():.4f}, {ckpt_weight.max():.4f}]")
    print(f"  Model weight range: [{model_weight.min():.4f}, {model_weight.max():.4f}]")

if __name__ == '__main__':
    main()
