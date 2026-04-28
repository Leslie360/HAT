#!/usr/bin/env python3
"""Post-training pipeline: waits for all training to finish, then runs
fresh-instance eval in parallel across GPUs, finally generates a summary report.

Usage:
    nohup python -u run_post_pipeline.py > post_pipeline.log 2>&1 &
"""
import subprocess
import time
import os
import sys
import json
from pathlib import Path
from datetime import datetime

SAVE_DIR = "checkpoints/_gpt/cross_arch_tinyimagenet"
EXPECTED_TASKS = 12          # 2 seeds × 2 archs × 3 hats
GPUS = [1, 2, 3, 4, 5, 6, 7]
MAX_PARALLEL_EVAL = 6        # keep 1 GPU free
EVAL_SCRIPT = "eval_fresh_instances_vit.py"
REPORT_DIR = "report_md/_gpt"
CHECK_INTERVAL = 300         # 5 minutes


def log(msg):
    stamped = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(stamped, flush=True)


def is_task_complete(task_dir: Path) -> bool:
    """A task is complete if best.pt exists and train.log shows 'Finished.' or '[EARLY STOP]'."""
    log_file = task_dir / "train.log"
    best_file = task_dir / "best.pt"
    if not log_file.exists() or not best_file.exists():
        return False
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            # Read last 1KB to avoid loading huge files
            f.seek(0, 2)
            size = f.tell()
            f.seek(max(0, size - 2048), 0)
            tail = f.read()
    except Exception:
        return False
    return "Finished." in tail or "[EARLY STOP]" in tail


def count_completed_tasks():
    if not Path(SAVE_DIR).exists():
        return 0
    count = 0
    for d in Path(SAVE_DIR).iterdir():
        if not d.is_dir():
            continue
        if is_task_complete(d):
            count += 1
    return count


def wait_for_training():
    log("Waiting for training to complete...")
    while True:
        completed = count_completed_tasks()
        log(f"Training progress: {completed}/{EXPECTED_TASKS} tasks complete")
        if completed >= EXPECTED_TASKS:
            log("All training tasks complete!")
            break
        time.sleep(CHECK_INTERVAL)


def collect_checkpoints():
    ckpts = []
    for d in sorted(Path(SAVE_DIR).iterdir()):
        if not d.is_dir():
            continue
        best = d / "best.pt"
        if best.exists():
            ckpts.append(str(best))
    return ckpts


def launch_eval_task(checkpoint, gpu_id):
    name = Path(checkpoint).parent.name
    log_path = os.path.join(SAVE_DIR, f"{name}_eval.log")
    cmd = (
        f"PYTHONUNBUFFERED=1 "
        f"CUDA_VISIBLE_DEVICES={gpu_id} "
        f"conda run -n hat python -u {EVAL_SCRIPT} "
        f"--checkpoint {checkpoint} --device cuda "
        f"> {log_path} 2>&1"
    )
    log(f"[EVAL] Launching {name} on GPU {gpu_id}")
    proc = subprocess.Popen(cmd, shell=True, preexec_fn=os.setsid)
    return proc.pid


def is_process_running(pid):
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError):
        return False


def run_evaluation(checkpoints):
    log(f"Starting evaluation phase ({len(checkpoints)} checkpoints)...")
    task_idx = 0
    launched = {}  # gpu_id -> (checkpoint_path, pid)

    while task_idx < len(checkpoints) or launched:
        # Launch new eval tasks up to MAX_PARALLEL_EVAL
        for gpu in GPUS:
            if gpu in launched:
                continue
            if len(launched) >= MAX_PARALLEL_EVAL:
                break
            if task_idx >= len(checkpoints):
                break
            ckpt = checkpoints[task_idx]
            pid = launch_eval_task(ckpt, gpu)
            launched[gpu] = (ckpt, pid)
            task_idx += 1
            time.sleep(10)

        # Check for finished eval jobs
        finished = []
        for gpu, (ckpt, pid) in list(launched.items()):
            if not is_process_running(pid):
                name = Path(ckpt).parent.name
                log(f"[DONE] {name} eval finished on GPU {gpu}")
                finished.append(gpu)
        for gpu in finished:
            del launched[gpu]

        if task_idx < len(checkpoints) or launched:
            time.sleep(60)

    log("Evaluation phase complete.")


def generate_report():
    log("Generating summary report...")
    json_dir = Path(REPORT_DIR) / "json_gpt"
    if not json_dir.exists():
        log("WARNING: No eval JSONs found.")
        return

    records = []
    for json_path in sorted(json_dir.glob("*_fresh_eval.json")):
        try:
            with open(json_path) as f:
                data = json.load(f)
        except Exception as e:
            log(f"WARNING: failed to load {json_path}: {e}")
            continue

        records.append({
            "experiment": data.get("exp_id", json_path.stem),
            "arch": data.get("checkpoint_arch"),
            "hat_type": data.get("checkpoint_hat_type"),
            "seed": data.get("checkpoint_seed"),
            "checkpoint_best_acc": data.get("checkpoint_best_acc"),
            "fresh_mean": data.get("cross_instance_mean"),
            "fresh_std": data.get("cross_instance_std"),
            "fresh_median": data.get("fresh_aggregate", {}).get("median"),
            "fresh_range": data.get("fresh_aggregate", {}).get("range"),
        })

    if not records:
        log("WARNING: no valid records to report.")
        return

    # Markdown report
    report_md = Path(REPORT_DIR) / "pipeline_summary.md"
    report_md.parent.mkdir(parents=True, exist_ok=True)
    with open(report_md, "w") as f:
        f.write("# Cross-Architecture HAT Pipeline Summary\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        f.write("| Experiment | Arch | HAT | Seed | Best Acc | Fresh Mean | Fresh Std | Fresh Median |\n")
        f.write("|---|---|---|---|---|---|---|---|\n")
        for r in records:
            f.write(
                f"| {r['experiment']} | {r['arch']} | {r['hat_type']} | {r['seed']} | "
                f"{r['checkpoint_best_acc']:.2f}% | {r['fresh_mean']:.2f}% | {r['fresh_std']:.2f}% | "
                f"{r['fresh_median']:.2f}% |\n"
            )
        f.write("\n")
        # Group by HAT type for quick comparison
        f.write("## Grouped by HAT Type\n\n")
        for hat in ["standard", "ensemble", "proportional"]:
            subset = [r for r in records if r["hat_type"] == hat]
            if not subset:
                continue
            mean_fresh = sum(r["fresh_mean"] for r in subset) / len(subset)
            f.write(f"- **{hat}**: avg fresh mean = {mean_fresh:.2f}% ({len(subset)} runs)\n")

    # JSON report
    report_json = Path(REPORT_DIR) / "pipeline_summary.json"
    with open(report_json, "w") as f:
        json.dump(records, f, indent=2)

    log(f"Report saved to {report_md} and {report_json}")


def main():
    wait_for_training()
    checkpoints = collect_checkpoints()
    log(f"Found {len(checkpoints)} checkpoints.")
    if not checkpoints:
        log("ERROR: No checkpoints found. Exiting.")
        sys.exit(1)
    run_evaluation(checkpoints)
    generate_report()
    log("=== ALL DONE ===")


if __name__ == "__main__":
    main()
