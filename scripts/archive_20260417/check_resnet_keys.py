import torch
import os

def check_keys(path):
    print(f"\nChecking keys in {path}...")
    if not os.path.exists(path):
        print("Not found.")
        return
    ckpt = torch.load(path, map_location='cpu', weights_only=False)
    keys = list(ckpt['model_state_dict'].keys())
    print(f"Total keys: {len(keys)}")
    print("First 10 keys:", keys[:10])
    
    # Check for d2d_noise
    d2d_keys = [k for k in keys if 'd2d_noise' in k]
    print(f"D2D noise keys found: {len(d2d_keys)}")
    if d2d_keys:
        print("First 2 D2D keys:", d2d_keys[:2])

if __name__ == "__main__":
    check_keys('checkpoints/R4_4bit_noise_HAT_best.pt')
    check_keys('checkpoints/resnet18_cifar100/R4_4bit_noise_HAT_best.pt')
