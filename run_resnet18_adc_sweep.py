#!/usr/bin/env python3
"""
ResNet-18 ADC Bit-width Sweep for CIFAR-10
Addressing NC Reviewer Minor Comment #1

Scans ADC resolution from 1-bit to 8-bit using locked R4 (HAT) checkpoint.
"""

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from analog_layers import AnalogLinearConfig, convert_resnet_to_analog, AnalogLinear, AnalogConv2d
import json
import os

def create_resnet18_cifar(num_classes=10):
    """Create ResNet-18 for CIFAR-10."""
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
    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size, shuffle=False, num_workers=4)
    return testloader

def evaluate_adc_config(model, testloader, device, n_states, mc_runs=10):
    """Evaluate model with specific ADC configuration."""
    # Update all analog layers to use specified n_states
    for module in model.modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            module.config.n_states = n_states
            module.config.noise_enabled = True
            module.config.sigma_c2c = 0.05
            module.config.sigma_d2d = 0.10
    
    model.eval()
    model.to(device)
    
    accuracies = []
    
    for mc in range(mc_runs):
        correct = 0
        total = 0
        
        with torch.no_grad():
            for inputs, targets in testloader:
                inputs, targets = inputs.to(device), targets.to(device)
                outputs = model(inputs)
                _, predicted = outputs.max(1)
                correct += predicted.eq(targets).sum().item()
                total += targets.size(0)
        
        acc = 100.0 * correct / total
        accuracies.append(acc)
    
    mean_acc = sum(accuracies) / len(accuracies)
    std_acc = (sum((x - mean_acc) ** 2 for x in accuracies) / len(accuracies)) ** 0.5
    
    return mean_acc, std_acc

def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")
    
    # Load R4 checkpoint (CIFAR-100)
    checkpoint_path = 'checkpoints/resnet18_cifar100/R4_4bit_noise_HAT_best.pt'
    if not os.path.exists(checkpoint_path):
        print(f"Error: Checkpoint not found at {checkpoint_path}")
        print("Available checkpoints:")
        import glob
        for ckpt in glob.glob('checkpoints/resnet18_cifar10/*.pt'):
            print(f"  {ckpt}")
        return
    
    print(f"Loading checkpoint: {checkpoint_path}")
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    
    # Build model with saved config
    cfg_dict = ckpt.get('exp_cfg', {})
    
    # Create base model
    model = create_resnet18_cifar(num_classes=100)
    
    # Convert to analog with config from checkpoint
    analog_cfg = AnalogLinearConfig(
        n_states=cfg_dict.get('n_states', 16),
        sigma_c2c=cfg_dict.get('sigma_c2c', 0.05),
        sigma_d2d=cfg_dict.get('sigma_d2d', 0.10),
        noise_enabled=True,
        restore_weight_scale=True,
    )
    
    import torch.nn as nn
    model = convert_resnet_to_analog(model, config=analog_cfg, skip_first_conv=False)
    model.load_state_dict(ckpt['model_state_dict'])
    
    # Get test loader
    testloader = get_cifar100_test_loader(batch_size=128)
    
    # ADC sweep
    adc_configs = [
        (2, "2-bit (4 levels)"),
        (3, "3-bit (8 levels)"),
        (4, "4-bit (16 levels)"),
        (5, "5-bit (32 levels)"),
        (6, "6-bit (64 levels)"),
        (7, "7-bit (128 levels)"),
        (8, "8-bit (256 levels)"),
    ]
    
    results = []
    
    print("\n" + "="*70)
    print("ResNet-18 CIFAR-100 ADC Bit-width Sweep")
    print("="*70)
    
    for n_states, desc in adc_configs:
        print(f"\nEvaluating {desc} (n_states={n_states})...")
        mean_acc, std_acc = evaluate_adc_config(model, testloader, device, n_states, mc_runs=10)
        print(f"  Accuracy: {mean_acc:.2f} ± {std_acc:.2f}%")
        results.append({
            'adc_bits': n_states,
            'n_states': 2 ** n_states if n_states <= 8 else n_states,
            'description': desc,
            'mean_accuracy': mean_acc,
            'std_accuracy': std_acc,
        })
    
    # Save results
    output = {
        'model': 'ResNet-18',
        'dataset': 'CIFAR-100',
        'checkpoint': checkpoint_path,
        'results': results
    }
    
    output_path = 'report_md/json/resnet18_cifar10_adc_sweep.json'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"\n{'='*70}")
    print("Summary")
    print("="*70)
    for r in results:
        print(f"{r['description']:20s}: {r['mean_accuracy']:5.2f} ± {r['std_accuracy']:4.2f}%")
    
    print(f"\nResults saved to: {output_path}")

if __name__ == '__main__':
    main()
