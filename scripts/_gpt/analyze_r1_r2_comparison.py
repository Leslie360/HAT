#!/usr/bin/env python3
"""Analyze and compare R1 (first-order-only) vs R2 (second-order) results."""
import json
import sys
from pathlib import Path

def load_json(path):
    with open(path) as f:
        return json.load(f)

def summarize(name, train_json, fresh_json):
    print(f"\n{'='*60}")
    print(f"  {name}")
    print(f"{'='*60}")
    
    train = load_json(train_json)
    fresh = load_json(fresh_json)
    
    # Training summary
    best = train.get("best", {})
    print(f"  Training best_acc:  {best.get('acc', 'N/A'):.2f}% (epoch {best.get('epoch', 'N/A')})")
    print(f"  Training final_acc: {train.get('final_test_acc', 'N/A'):.2f}%")
    
    # Fresh eval summary
    print(f"  Fresh-instance:     {fresh.get('cross_instance_mean', 'N/A'):.2f}% ± {fresh.get('cross_instance_std', 'N/A'):.2f}%")
    print(f"  Instance range:     {min(fresh.get('instance_means', [])):.2f}% ~ {max(fresh.get('instance_means', [])):.2f}%")
    
    return {
        "train_best_acc": best.get("acc", 0),
        "train_best_epoch": best.get("epoch", 0),
        "fresh_mean": fresh.get("cross_instance_mean", 0),
        "fresh_std": fresh.get("cross_instance_std", 0),
    }

def main():
    root = Path("/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt")
    
    r1_train = root / "r1_clean_anchor_train.json"
    r1_fresh = root / "r1_clean_anchor_fresh_eval.json"
    r2_train = root / "r2_so2_comparison_train.json"
    r2_fresh = root / "r2_so2_comparison_fresh_eval.json"
    
    results = {}
    
    if r1_train.exists() and r1_fresh.exists():
        results["R1"] = summarize("R1: First-Order Only (α=0)", r1_train, r1_fresh)
    else:
        print(f"R1 results not yet available")
    
    if r2_train.exists() and r2_fresh.exists():
        results["R2"] = summarize("R2: Second-Order (α=0.25)", r2_train, r2_fresh)
    else:
        print(f"R2 results not yet available")
    
    if "R1" in results and "R2" in results:
        print(f"\n{'='*60}")
        print(f"  COMPARISON")
        print(f"{'='*60}")
        r1 = results["R1"]
        r2 = results["R2"]
        print(f"  Train best delta:   {r2['train_best_acc'] - r1['train_best_acc']:+.2f}%")
        print(f"  Fresh mean delta:   {r2['fresh_mean'] - r1['fresh_mean']:+.2f}%")
        print(f"  Fresh std delta:    {r2['fresh_std'] - r1['fresh_std']:+.2f}%")
        
        if r2["fresh_mean"] > r1["fresh_mean"]:
            print(f"\n  → R2 (SO2) IMPROVES fresh-instance by {r2['fresh_mean'] - r1['fresh_mean']:.2f}%")
        else:
            print(f"\n  → R2 (SO2) DEGRADES fresh-instance by {r1['fresh_mean'] - r2['fresh_mean']:.2f}%")

if __name__ == "__main__":
    main()
