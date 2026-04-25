#!/usr/bin/env python3
"""Real-time R1 training progress monitor."""
import re
import sys
from pathlib import Path
from datetime import datetime

def parse_log(log_path):
    epochs = []
    with open(log_path) as f:
        for line in f:
            m = re.search(r'Epoch\s+(\d+)/100:.*test_acc=([0-9.]+)%.*best=([0-9.]+)%', line)
            if m:
                epochs.append({
                    'epoch': int(m.group(1)),
                    'test_acc': float(m.group(2)),
                    'best': float(m.group(3)),
                })
    return epochs

def main():
    log_path = Path("/home/qiaosir/projects/compute_vit/logs/_gpt/r1_clean_anchor_train_20260423_131610.log")
    if not log_path.exists():
        print("Log not found yet.")
        return
    
    epochs = parse_log(log_path)
    if not epochs:
        print("No epoch data in log yet.")
        return
    
    latest = epochs[-1]
    print(f"[{datetime.now().strftime('%H:%M:%S')}] R1 Progress:")
    print(f"  Epoch {latest['epoch']}/100 | test_acc={latest['test_acc']:.2f}% | best={latest['best']:.2f}%")
    
    if len(epochs) >= 2:
        # Estimate completion
        first = epochs[0]
        last = epochs[-1]
        epochs_done = last['epoch'] - first['epoch']
        if epochs_done > 0:
            # Rough time estimate based on file timestamps
            import os
            mtime = log_path.stat().st_mtime
            # We don't have exact per-epoch timing from log alone
            # Just show trend
            acc_delta = latest['test_acc'] - epochs[0]['test_acc']
            print(f"  Progress: +{latest['epoch']} epochs from start, test_acc Δ = {acc_delta:+.2f}%")
    
    if latest['epoch'] >= 99:
        print("  ✅ TRAINING NEAR COMPLETION")

if __name__ == "__main__":
    main()
