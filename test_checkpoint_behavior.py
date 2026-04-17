
import torch
import torch.nn as nn
from train_tinyvit import build_model, evaluate, get_dataloaders, TinyViTExperimentConfig, DATASET_STATS
import dataclasses

def resample_all_d2d_noise(model):
    for m in model.modules():
        if hasattr(m, 'resample_d2d_noise'):
            m.resample_d2d_noise()

def test():
    device = 'cuda'
    dataset = 'cifar10'
    num_classes = DATASET_STATS[dataset]['num_classes']
    ckpt_path = 'checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt'
    
    print(f"Testing checkpoint: {ckpt_path}")
    ckpt = torch.load(ckpt_path, map_location=device, weights_only=False)
    exp_cfg_dict = ckpt['exp_cfg']
    valid_keys = {f.name for f in dataclasses.fields(TinyViTExperimentConfig)}
    filtered = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
    cfg = TinyViTExperimentConfig(**filtered)
    cfg.noise_enabled = True
    
    model = build_model(cfg, num_classes, device)
    model.load_state_dict(ckpt['model_state_dict'])
    
    _, loader = get_dataloaders(dataset, batch_size=256)
    criterion = nn.CrossEntropyLoss()
    
    # 1. Test on saved mask
    _, acc_saved = evaluate(model, loader, criterion, device, cfg)
    print(f"Accuracy on saved mask: {acc_saved:.2f}%")
    
    # 2. Test after resampling
    resample_all_d2d_noise(model)
    _, acc_resampled = evaluate(model, loader, criterion, device, cfg)
    print(f"Accuracy after resampling: {acc_resampled:.2f}%")

if __name__ == "__main__":
    test()
