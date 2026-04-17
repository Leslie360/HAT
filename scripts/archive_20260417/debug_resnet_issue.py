#!/usr/bin/env python3
"""
Debug script to diagnose ResNet-18 CIFAR-100 test accuracy stuck at 1% issue.
"""

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from analog_layers import AnalogLinearConfig, convert_resnet_to_analog, AnalogLinear, AnalogConv2d

def create_resnet18_cifar(num_classes=100):
    """Create ResNet-18 for CIFAR."""
    model = torchvision.models.resnet18(weights=None, num_classes=num_classes)
    model.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
    model.maxpool = nn.Identity()
    return model

def get_cifar100_test_loader(batch_size=128):
    """Get CIFAR-100 test loader."""
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize((0.5071, 0.4867, 0.4408), (0.2675, 0.2565, 0.2761)),
    ])
    testset = torchvision.datasets.CIFAR100(root='./data', train=False, download=True, transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=0)
    return testloader

@torch.no_grad()
def diagnose_model(model, testloader, device='cuda'):
    """Diagnose model outputs."""
    model.eval()
    model.to(device)
    
    # Get one batch
    inputs, targets = next(iter(testloader))
    inputs, targets = inputs.to(device), targets.to(device)
    
    # Forward pass
    outputs = model(inputs)
    
    print(f"\n=== Diagnostic Information ===")
    print(f"Input shape: {inputs.shape}")
    print(f"Output shape: {outputs.shape}")
    print(f"Output min: {outputs.min().item():.4f}")
    print(f"Output max: {outputs.max().item():.4f}")
    print(f"Output mean: {outputs.mean().item():.4f}")
    print(f"Output std: {outputs.std().item():.4f}")
    print(f"Any NaN in output: {torch.isnan(outputs).any().item()}")
    print(f"Any Inf in output: {torch.isinf(outputs).any().item()}")
    
    # Check predictions
    _, predicted = outputs.max(1)
    print(f"\nPredicted classes (first 20): {predicted[:20].tolist()}")
    print(f"Target classes (first 20): {targets[:20].tolist()}")
    print(f"Unique predicted classes: {predicted.unique().numel()}")
    print(f"Accuracy on this batch: {predicted.eq(targets).sum().item() / targets.size(0) * 100:.2f}%")
    
    # Check if all predictions are the same
    if predicted.unique().numel() == 1:
        print(f"\n⚠️ WARNING: All predictions are the same class ({predicted[0].item()})!")
    
    return outputs

def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    
    # Load test data
    testloader = get_cifar100_test_loader(batch_size=128)
    
    # Test 1: Standard ResNet-18 (FP32)
    print("\n" + "="*70)
    print("Test 1: Standard ResNet-18 (FP32)")
    print("="*70)
    model_fp32 = create_resnet18_cifar(num_classes=100)
    diagnose_model(model_fp32, testloader, device)
    
    # Test 2: Analog ResNet-18 with noise (simulating R3/R4)
    print("\n" + "="*70)
    print("Test 2: Analog ResNet-18 (R3 config - noise eval)")
    print("="*70)
    
    analog_cfg = AnalogLinearConfig(
        n_states=16,
        sigma_c2c=0.05,
        sigma_d2d=0.10,
        noise_enabled=True,  # This is what set_noise_for_eval does
        restore_weight_scale=True,
    )
    model_analog = create_resnet18_cifar(num_classes=100)
    model_analog = convert_resnet_to_analog(model_analog, config=analog_cfg, skip_first_conv=False)
    diagnose_model(model_analog, testloader, device)
    
    # Test 3: Check if analog layers are properly configured
    print("\n" + "="*70)
    print("Test 3: Analog layer configuration check")
    print("="*70)
    
    analog_layer_count = 0
    for name, module in model_analog.named_modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            analog_layer_count += 1
            if analog_layer_count <= 3:  # Show first 3
                print(f"\nLayer: {name}")
                print(f"  noise_enabled: {module.config.noise_enabled}")
                print(f"  sigma_c2c: {module.config.sigma_c2c}")
                print(f"  sigma_d2d: {module.config.sigma_d2d}")
                print(f"  n_states: {module.config.n_states}")
                print(f"  restore_weight_scale: {module.config.restore_weight_scale}")
    
    print(f"\nTotal analog layers: {analog_layer_count}")

if __name__ == '__main__':
    main()
