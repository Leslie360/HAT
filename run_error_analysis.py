"""
Error Analysis Suite

Analyzes:
1. Most confused class pairs
2. Hardest test samples
3. Prediction confidence distribution
4. Error patterns by class
"""

import torch
import torch.nn as nn
import numpy as np
import sys
import dataclasses

sys.path.insert(0, '/home/qiaosir/projects/compute_vit')
sys.stdout.reconfigure(line_buffering=True)

from train_tinyvit import (
    build_model, get_dataloaders, set_seed,
    TinyViTExperimentConfig
)
from collections import defaultdict

def analyze_errors(dataset='cifar10', device='cuda'):
    """Comprehensive error analysis"""
    print("="*70)
    print("Error Analysis - V4 Ensemble HAT")
    print("="*70)
    
    checkpoint_path = 'checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt'
    ckpt = torch.load(checkpoint_path, map_location=device, weights_only=False)
    
    exp_cfg_dict = ckpt.get('exp_cfg', {})
    valid_keys = {f.name for f in dataclasses.fields(TinyViTExperimentConfig)}
    filtered = {k: v for k, v in exp_cfg_dict.items() if k in valid_keys}
    cfg = TinyViTExperimentConfig(**filtered)
    cfg.noise_enabled = True
    
    _, loader = get_dataloaders(dataset, batch_size=256)
    
    model = build_model(cfg, num_classes=10, device=device)
    model.load_state_dict(ckpt['model_state_dict'])
    
    # Resample D2D
    for m in model.modules():
        if hasattr(m, 'resample_d2d_noise') and callable(m.resample_d2d_noise):
            m.resample_d2d_noise()
    
    model.eval()
    
    # Collect predictions with confidence
    all_preds = []
    all_labels = []
    all_confidences = []
    all_probs = []
    
    print("\nCollecting predictions...")
    with torch.no_grad():
        for inputs, labels in loader:
            inputs = inputs.to(device)
            outputs = model(inputs)
            probs = torch.softmax(outputs, dim=1)
            confidences, predicted = probs.max(1)
            
            all_preds.extend(predicted.cpu().numpy())
            all_labels.extend(labels.numpy())
            all_confidences.extend(confidences.cpu().numpy())
            all_probs.extend(probs.cpu().numpy())
    
    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)
    all_confidences = np.array(all_confidences)
    all_probs = np.array(all_probs)
    
    # 1. Overall accuracy
    accuracy = (all_preds == all_labels).mean()
    print(f"\n1. OVERALL ACCURACY: {accuracy*100:.2f}%")
    
    # 2. Per-class accuracy
    print("\n2. PER-CLASS ACCURACY:")
    print("-" * 50)
    for c in range(10):
        mask = all_labels == c
        if mask.sum() > 0:
            class_acc = (all_preds[mask] == all_labels[mask]).mean()
            class_conf = all_confidences[mask].mean()
            print(f"  Class {c}: Acc={class_acc*100:.2f}%, AvgConf={class_conf:.3f}")
    
    # 3. Confusion pairs
    print("\n3. TOP CONFUSION PAIRS:")
    print("-" * 50)
    confusion_pairs = defaultdict(int)
    for true, pred in zip(all_labels, all_preds):
        if true != pred:
            confusion_pairs[(true, pred)] += 1
    
    sorted_pairs = sorted(confusion_pairs.items(), key=lambda x: x[1], reverse=True)
    for (true, pred), count in sorted_pairs[:10]:
        print(f"  True={true} → Pred={pred}: {count} times")
    
    # 4. Confidence analysis
    print("\n4. CONFIDENCE ANALYSIS:")
    print("-" * 50)
    correct_mask = all_preds == all_labels
    correct_conf = all_confidences[correct_mask].mean()
    wrong_conf = all_confidences[~correct_mask].mean()
    
    print(f"  Correct predictions: AvgConf={correct_conf:.3f}")
    print(f"  Wrong predictions: AvgConf={wrong_conf:.3f}")
    print(f"  Confidence gap: {correct_conf - wrong_conf:.3f}")
    
    # 5. High-confidence errors
    print("\n5. HIGH-CONFIDENCE ERRORS (>90% confident but wrong):")
    print("-" * 50)
    high_conf_wrong = (~correct_mask) & (all_confidences > 0.9)
    print(f"  Count: {high_conf_wrong.sum()} / {(~correct_mask).sum()} errors")
    if high_conf_wrong.sum() > 0:
        for idx in np.where(high_conf_wrong)[0][:5]:
            print(f"    True={all_labels[idx]}, Pred={all_preds[idx]}, Conf={all_confidences[idx]:.3f}")
    
    # 6. Low-confidence correct (<50% confident but right)
    print("\n6. LOW-CONFIDENCE CORRECT (<60% confident but right):")
    print("-" * 50)
    low_conf_correct = correct_mask & (all_confidences < 0.6)
    print(f"  Count: {low_conf_correct.sum()} / {correct_mask.sum()} correct")
    
    # 7. Prediction entropy analysis
    print("\n7. PREDICTION ENTROPY:")
    print("-" * 50)
    # Entropy = -sum(p * log(p))
    epsilon = 1e-10
    entropy = -np.sum(all_probs * np.log(all_probs + epsilon), axis=1)
    
    correct_entropy = entropy[correct_mask].mean()
    wrong_entropy = entropy[~correct_mask].mean()
    print(f"  Correct predictions: AvgEntropy={correct_entropy:.3f}")
    print(f"  Wrong predictions: AvgEntropy={wrong_entropy:.3f}")
    print(f"  Lower entropy = more confident/certain")
    
    # Save results
    results = {
        'overall_accuracy': float(accuracy),
        'per_class_accuracy': {},
        'top_confusion_pairs': [(f"{t}->{p}", int(c)) for (t, p), c in sorted_pairs[:10]],
        'confidence_analysis': {
            'correct_avg': float(correct_conf),
            'wrong_avg': float(wrong_conf),
            'gap': float(correct_conf - wrong_conf)
        },
        'high_confidence_errors': int(high_conf_wrong.sum()),
        'entropy_analysis': {
            'correct_avg': float(correct_entropy),
            'wrong_avg': float(wrong_entropy)
        }
    }
    
    for c in range(10):
        mask = all_labels == c
        if mask.sum() > 0:
            class_acc = (all_preds[mask] == all_labels[mask]).mean()
            results['per_class_accuracy'][f'class_{c}'] = float(class_acc)
    
    import json
    with open('report_md/_gpt/error_analysis_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved: report_md/_gpt/error_analysis_results.json")
    print("="*70)

def main():
    set_seed(42)
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    analyze_errors(device=device)

if __name__ == '__main__':
    main()
