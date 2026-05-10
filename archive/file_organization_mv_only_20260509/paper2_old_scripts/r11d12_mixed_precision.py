#!/usr/bin/env python3
import argparse
import time
import os
import sys
import json
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from datetime import datetime
from aihwkit.nn import AnalogLinear
from aihwkit.optim import AnalogSGD
from aihwkit.simulator.configs import InferenceRPUConfig
from aihwkit.simulator.presets import PCMPresetUnitCell, PCMPresetDevice

def _resolve_pcm_preset(preferred=None):
    PCM_PRESET_REGISTRY = [
        ("aihwkit.simulator.presets", "PCMPresetUnitCell"),
        ("aihwkit.simulator.presets", "PCMPresetDevice"),
    ]
    if preferred:
        for module_path, class_name in PCM_PRESET_REGISTRY:
            if class_name == preferred:
                import importlib
                mod = importlib.import_module(module_path)
                cls = getattr(mod, class_name)
                return cls(), class_name
        raise RuntimeError(f"Preset {preferred} not found")
    return PCMPresetUnitCell(), "PCMPresetUnitCell"

def make_rpu_config(res=1.0/256.0, mod_std=0.1, pcm_preset_inst=None):
    cfg = InferenceRPUConfig()
    if pcm_preset_inst:
        cfg = pcm_preset_inst
    cfg.forward.inp_res = res
    cfg.forward.out_res = res
    cfg.modifier.std_dev = mod_std
    cfg.modifier.enable_during_test = True
    return cfg

def replace_linear_mixed(module, res_4bit, res_8bit, layers_8bit, mod_std, pcm_inst, parent_name=""):
    for name, child in list(module.named_children()):
        full_name = f"{parent_name}.{name}" if parent_name else name
        if isinstance(child, nn.Linear):
            res = res_8bit if any(p in full_name for p in layers_8bit) else res_4bit
            cfg = make_rpu_config(res, mod_std, pcm_inst)
            analog_layer = AnalogLinear(child.in_features, child.out_features, bias=child.bias is not None, rpu_config=cfg)
            analog_layer.set_weights(child.weight, child.bias)
            setattr(module, name, analog_layer)
        else:
            replace_linear_mixed(child, res_4bit, res_8bit, layers_8bit, mod_std, pcm_inst, full_name)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-id", type=str, required=True)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--layers-8bit", type=str, default="patch_embed,head", help="Comma separated layer name substrings")
    parser.add_argument("--modifier-std-dev", type=float, default=0.1)
    parser.add_argument("--save-dir", type=str, default="paper2_aihwkit_baseline/checkpoints")
    args = parser.parse_args()

    device = torch.device("cuda")
    import timm
    model = timm.create_model("tiny_vit_5m_224", num_classes=10, pretrained=False).to("cpu")

    pcm_inst, pcm_name = _resolve_pcm_preset()
    layers_8bit_list = args.layers_8bit.split(",")

    replace_linear_mixed(model, 1.0/16.0, 1.0/256.0, layers_8bit_list, args.modifier_std_dev, pcm_inst)
    model = model.to(device)

    print(f"Run: {args.run_id} | Protected layers: {args.layers_8bit}")

    transform = transforms.Compose([transforms.Resize(224), transforms.ToTensor(), transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])
    train_set = datasets.CIFAR10(root="./data", train=True, download=True, transform=transform)
    test_set = datasets.CIFAR10(root="./data", train=False, download=True, transform=transform)
    train_loader = DataLoader(train_set, batch_size=64, shuffle=True, num_workers=2)
    test_loader = DataLoader(test_set, batch_size=64, shuffle=False, num_workers=2)

    optimizer = AnalogSGD(model.parameters(), lr=5e-4)
    criterion = nn.CrossEntropyLoss()

    best_acc = 0
    for epoch in range(args.epochs):
        model.train()
        for inputs, targets in train_loader:
            inputs, targets = inputs.to(device), targets.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, targets in test_loader:
                inputs, targets = inputs.to(device), targets.to(device)
                outputs = model(inputs)
                _, predicted = outputs.max(1)
                total += targets.size(0)
                correct += predicted.eq(targets).sum().item()

        acc = 100.0 * correct / total
        best_acc = max(best_acc, acc)
        print(f"Epoch {epoch+1}: {acc:.2f}% (Best: {best_acc:.2f}%)")

    save_path = os.path.join(args.save_dir, args.run_id)
    os.makedirs(save_path, exist_ok=True)
    torch.save({"model_state_dict": model.state_dict(), "best_acc": best_acc}, os.path.join(save_path, "best.pt"))
    with open(os.path.join(save_path, "training_history.json"), "w") as f:
        json.dump({"best_acc": best_acc, "args": vars(args)}, f)

if __name__ == "__main__":
    main()
