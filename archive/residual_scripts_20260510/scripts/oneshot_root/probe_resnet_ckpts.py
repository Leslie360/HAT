import torch
import os

def probe_ckpt(path):
    print(f"\nProbing {path}...")
    if not os.path.exists(path):
        print("File not found.")
        return
    ckpt = torch.load(path, map_location='cpu', weights_only=False)
    print("exp_cfg:", ckpt.get('exp_cfg', 'MISSING'))
    print("best_acc:", ckpt.get('best_acc', 'MISSING'))
    print("epoch:", ckpt.get('epoch', 'MISSING'))

if __name__ == "__main__":
    probe_ckpt('checkpoints/R2_4bit_no_noise_best.pt')
    probe_ckpt('checkpoints/R4_4bit_noise_HAT_best.pt')
    probe_ckpt('checkpoints/resnet18_cifar100/R4_4bit_noise_HAT_best.pt')
