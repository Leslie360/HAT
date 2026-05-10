import torch
import os

def check_weights(path):
    print(f"\nChecking weights in {path}...")
    if not os.path.exists(path):
        print("Not found.")
        return
    ckpt = torch.load(path, map_location='cpu', weights_only=False)
    state = ckpt['model_state_dict']
    
    # Check a few layers
    layers = ['conv1.weight', 'layer1.0.conv1.weight', 'layer4.1.conv2.weight', 'fc.weight']
    for l in layers:
        if l in state:
            w = state[l]
            print(f"  {l:25s}: shape={list(w.shape)}, min={w.min():.4f}, max={w.max():.4f}, mean={w.mean():.4f}, has_nan={torch.isnan(w).any()}")
        else:
            print(f"  {l:25s}: MISSING")

if __name__ == "__main__":
    check_weights('checkpoints/R4_4bit_noise_HAT_best.pt')
    check_weights('checkpoints/resnet18_cifar100/R4_4bit_noise_HAT_best.pt')
