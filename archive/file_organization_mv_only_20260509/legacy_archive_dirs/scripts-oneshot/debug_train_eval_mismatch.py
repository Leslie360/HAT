#!/usr/bin/env python3
"""
Debug the train/eval mismatch for R3 (standard training with analog layers).

R3 Config:
- Training: noise_enabled=False, sigma_c2c=0.0 (clean training)
- Eval: set_noise_for_eval enables noise_enabled=True, sigma_c2c=0.05 (noisy eval)

This distribution mismatch may cause the model to fail.
"""

import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from analog_layers import AnalogLinearConfig, convert_resnet_to_analog, AnalogLinear, AnalogConv2d

def create_resnet18_cifar(num_classes=100):
    model = torchvision.models.resnet18(weights=None, num_classes=num_classes)
    model.conv1 = nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
    model.maxpool = nn.Identity()
    return model

def get_cifar100_loader(batch_size=128, train=True):
    if train:
        transform = transforms.Compose([
            transforms.RandomCrop(32, padding=4),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize((0.5071, 0.4867, 0.4408), (0.2675, 0.2565, 0.2761)),
        ])
    else:
        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize((0.5071, 0.4867, 0.4408), (0.2675, 0.2565, 0.2761)),
        ])
    dataset = torchvision.datasets.CIFAR100(root='./data', train=train, download=True, transform=transform)
    loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=train, num_workers=0)
    return loader

def set_noise_for_eval(model, noise_enabled=True, sigma_c2c=0.05, sigma_d2d=0.1):
    """Mirror of train_resnet18.py::set_noise_for_eval"""
    for module in model.modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            module.config.noise_enabled = noise_enabled
            module.config.sigma_c2c = sigma_c2c
            module.config.sigma_d2d = sigma_d2d

def set_noise_for_train(model, hat_training=False, noise_enabled=False, sigma_c2c=0.0, sigma_d2d=0.1):
    """Mirror of train_resnet18.py::set_noise_for_train"""
    for module in model.modules():
        if isinstance(module, (AnalogLinear, AnalogConv2d)):
            if hat_training:
                module.config.noise_enabled = noise_enabled
                module.config.sigma_c2c = sigma_c2c
            else:
                module.config.noise_enabled = False
                module.config.sigma_c2c = 0.0

@torch.no_grad()
def evaluate_with_config(model, testloader, device, eval_noise=True, sigma_c2c=0.05):
    """Evaluate with specified noise config."""
    model.eval()
    if eval_noise:
        set_noise_for_eval(model, noise_enabled=True, sigma_c2c=sigma_c2c, sigma_d2d=0.1)
    else:
        set_noise_for_eval(model, noise_enabled=False, sigma_c2c=0.0, sigma_d2d=0.0)
    
    model.to(device)
    correct = 0
    total = 0
    
    for inputs, targets in testloader:
        inputs, targets = inputs.to(device), targets.to(device)
        outputs = model(inputs)
        _, predicted = outputs.max(1)
        correct += predicted.eq(targets).sum().item()
        total += targets.size(0)
    
    return 100.0 * correct / total

def train_one_batch(model, trainloader, optimizer, criterion, device):
    """Train for one batch only."""
    model.train()
    set_noise_for_train(model, hat_training=False)  # R3 config: no noise during training
    
    inputs, targets = next(iter(trainloader))
    inputs, targets = inputs.to(device), targets.to(device)
    
    optimizer.zero_grad()
    outputs = model(inputs)
    loss = criterion(outputs, targets)
    loss.backward()
    optimizer.step()
    
    return loss.item()

def main():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}\n")
    
    # Create R3 config model
    analog_cfg = AnalogLinearConfig(
        n_states=16,
        sigma_c2c=0.0,  # Training: no C2C noise for standard training
        sigma_d2d=0.1,
        noise_enabled=False,  # Training: noise off
        restore_weight_scale=True,
    )
    model = create_resnet18_cifar(num_classes=100)
    model = convert_resnet_to_analog(model, config=analog_cfg, skip_first_conv=False)
    model.to(device)
    
    # Get data
    trainloader = get_cifar100_loader(batch_size=128, train=True)
    testloader = get_cifar100_loader(batch_size=128, train=False)
    
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=0.1, momentum=0.9, weight_decay=5e-4)
    
    print("="*70)
    print("R3 Experiment Simulation")
    print("="*70)
    
    # Step 1: Before training, evaluate with clean (no noise)
    acc_clean_before = evaluate_with_config(model, testloader, device, eval_noise=False)
    print(f"\n1. Before training, clean eval: {acc_clean_before:.2f}%")
    
    # Step 2: Before training, evaluate with noise (R3 eval config)
    acc_noisy_before = evaluate_with_config(model, testloader, device, eval_noise=True, sigma_c2c=0.05)
    print(f"2. Before training, noisy eval: {acc_noisy_before:.2f}%")
    
    # Step 3: Train for one batch (clean)
    print(f"\n3. Training for one batch (clean, no noise)...")
    loss = train_one_batch(model, trainloader, optimizer, criterion, device)
    print(f"   Loss: {loss:.4f}")
    
    # Step 4: After training, evaluate with clean
    acc_clean_after = evaluate_with_config(model, testloader, device, eval_noise=False)
    print(f"\n4. After 1 batch training, clean eval: {acc_clean_after:.2f}%")
    
    # Step 5: After training, evaluate with noise (this is where R3 fails!)
    acc_noisy_after = evaluate_with_config(model, testloader, device, eval_noise=True, sigma_c2c=0.05)
    print(f"5. After 1 batch training, noisy eval: {acc_noisy_after:.2f}%")
    
    # Analysis
    print("\n" + "="*70)
    print("ANALYSIS")
    print("="*70)
    
    clean_improvement = acc_clean_after - acc_clean_before
    noisy_improvement = acc_noisy_after - acc_noisy_before
    
    print(f"\nClean eval improvement: {clean_improvement:+.2f}%")
    print(f"Noisy eval improvement: {noisy_improvement:+.2f}%")
    
    if noisy_improvement < 0.1 and acc_noisy_after < 2.0:
        print("\n⚠️  KEY FINDING: Model learns on clean training but fails on noisy eval!")
        print("   This explains why R3 test_acc stays at ~1% despite train_acc rising.")
        print("\n   ROOT CAUSE: Train/eval distribution mismatch")
        print("   - Training: noise_enabled=False (clean)")
        print("   - Eval: noise_enabled=True, sigma_c2c=0.05 (noisy)")
        print("   - The model never sees noise during training, so it cannot handle")
        print("     the sudden noise injection during evaluation.")

if __name__ == '__main__':
    main()
