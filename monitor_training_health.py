#!/usr/bin/env python3
"""
Real-time training health monitor.
Run this alongside training to catch anomalies early.
"""
import sys
import json
import time
import argparse
from pathlib import Path

def parse_log_line(line):
    """Extract metrics from train_tinyvit_ensemble.py log lines."""
    if "Epoch" not in line or "train_loss=" not in line:
        return None
    try:
        parts = line.split("Epoch")[1].split(":")
        epoch_str = parts[0].strip().split("/")[0].strip()
        epoch = int(epoch_str)
        
        rest = parts[1] if len(parts) > 1 else ""
        metrics = {}
        for token in rest.split(","):
            if "=" in token:
                k, v = token.strip().split("=")
                metrics[k.strip()] = v.strip()
        
        return {
            "epoch": epoch,
            "train_loss": float(metrics.get("train_loss", 0)),
            "train_acc": float(metrics.get("train_acc", "0").replace("%", "")),
            "test_acc": float(metrics.get("test_acc", "0").replace("%", "")),
            "best": float(metrics.get("best", "0").replace("%", "")) if "best" in metrics else None,
        }
    except Exception:
        return None

def check_health(metrics, prev_metrics):
    """Return list of warnings if anything looks anomalous."""
    warnings = []
    
    if metrics["train_loss"] > 3.0:
        warnings.append(f"🔴 Train loss very high: {metrics['train_loss']:.4f}")
    
    if metrics["train_acc"] < 10.0 and metrics["epoch"] > 5:
        warnings.append(f"🔴 Train acc near chance: {metrics['train_acc']:.2f}%")
    
    if metrics["test_acc"] < 10.0 and metrics["epoch"] > 10:
        warnings.append(f"🔴 Test acc near chance: {metrics['test_acc']:.2f}%")
    
    if prev_metrics and metrics["train_loss"] > prev_metrics["train_loss"] * 1.5:
        warnings.append(f"⚠️  Train loss spiked: {prev_metrics['train_loss']:.4f} -> {metrics['train_loss']:.4f}")
    
    if prev_metrics and metrics["test_acc"] < prev_metrics["test_acc"] - 20.0:
        warnings.append(f"⚠️  Test acc dropped >20pp: {prev_metrics['test_acc']:.2f}% -> {metrics['test_acc']:.2f}%")
    
    # For NL=2.0 training, expect lower initial accuracy than NL=1.0
    if metrics["epoch"] == 0 and metrics["test_acc"] > 85.0:
        warnings.append(f"⚠️  Epoch 0 test_acc suspiciously high for NL=2.0: {metrics['test_acc']:.2f}%")
    
    return warnings

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-file", required=True)
    parser.add_argument("--poll-interval", type=int, default=30)
    parser.add_argument("--json-out", default=None)
    args = parser.parse_args()
    
    log_path = Path(args.log_file)
    prev_metrics = None
    history = []
    
    print(f"Monitoring: {log_path}")
    print("=" * 60)
    
    while True:
        if not log_path.exists():
            print(f"Waiting for {log_path}...")
            time.sleep(args.poll_interval)
            continue
        
        lines = log_path.read_text().splitlines()
        new_metrics = None
        for line in lines:
            m = parse_log_line(line)
            if m:
                new_metrics = m
        
        if new_metrics and (not history or new_metrics["epoch"] != history[-1]["epoch"]):
            history.append(new_metrics)
            warnings = check_health(new_metrics, prev_metrics)
            
            status = "✅" if not warnings else "⚠️"
            print(f"{status} Epoch {new_metrics['epoch']:3d}: "
                  f"train_loss={new_metrics['train_loss']:.4f}, "
                  f"train_acc={new_metrics['train_acc']:.2f}%, "
                  f"test_acc={new_metrics['test_acc']:.2f}%")
            
            for w in warnings:
                print(f"   {w}")
            
            prev_metrics = new_metrics
            
            if args.json_out:
                with open(args.json_out, "w") as f:
                    json.dump(history, f, indent=2)
        
        time.sleep(args.poll_interval)

if __name__ == "__main__":
    main()
