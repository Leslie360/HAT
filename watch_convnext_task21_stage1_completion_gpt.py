#!/usr/bin/env python3
"""Watch the active ConvNeXt CIFAR-100 stage and launch Flowers-102 automatically."""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import time
from pathlib import Path


ROOT = Path("/home/qiaosir/projects/compute_vit")
PY = Path("/home/qiaosir/miniconda3/envs/LLM/bin/python")


def pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def latest_flowers_log() -> Path | None:
    matches = sorted((ROOT / "logs" / "_gpt").glob("train_convnext_flowers102_c134_fix_*_gpt.log"))
    return matches[-1] if matches else None


def log(msg: str, fh):
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{stamp}] {msg}"
    print(line, file=fh, flush=True)


def maybe_stage1_finished(log_path: Path) -> bool:
    if not log_path.exists():
        return False
    text = log_path.read_text(encoding="utf-8", errors="ignore")
    return "Finished in" in text and "Experiment C4:" in text and "SUMMARY" in text


def main():
    parser = argparse.ArgumentParser(description="Watch ConvNeXt Task 21 CIFAR-100 stage and auto-launch Flowers-102.")
    parser.add_argument("--stage1-pid", type=int, required=True)
    parser.add_argument("--stage1-log", type=str, required=True)
    parser.add_argument("--poll-seconds", type=int, default=60)
    parser.add_argument("--watch-log", type=str, required=True)
    args = parser.parse_args()

    stage1_log = Path(args.stage1_log)
    watch_log = Path(args.watch_log)
    watch_log.parent.mkdir(parents=True, exist_ok=True)

    with watch_log.open("a", encoding="utf-8") as fh:
        log(f"Watcher armed for PID {args.stage1_pid}", fh)
        log(f"Stage-1 log: {stage1_log}", fh)

        while True:
            if latest_flowers_log() is not None:
                log("Flowers-102 stage already has a log; watcher exits without relaunch.", fh)
                return
            alive = pid_alive(args.stage1_pid)
            if alive:
                log("Stage-1 still running; sleeping.", fh)
                time.sleep(args.poll_seconds)
                continue

            log("Stage-1 process exited; inspecting final state.", fh)
            if stage1_log.exists():
                tail = "\n".join(stage1_log.read_text(encoding="utf-8", errors="ignore").splitlines()[-30:])
                if "Experiment C4:" not in tail and "Experiment C3:" in tail:
                    log("Stage-1 likely stopped before reaching Flowers-102, proceeding to stage-2 launch.", fh)
                elif "SUMMARY" in tail or maybe_stage1_finished(stage1_log):
                    log("Stage-1 appears complete; proceeding to stage-2 launch.", fh)
                else:
                    log("Stage-1 ended without a clean summary, but no live process remains; proceeding to stage-2 launch.", fh)
            else:
                log("Stage-1 log missing at exit; proceeding conservatively to stage-2 launch.", fh)

            ts = time.strftime("%Y%m%d_%H%M%S")
            cmd = ["/bin/bash", str(ROOT / "run_task21_convnext_flowers102_gpt.sh"), ts]
            log(f"Launching Flowers-102 stage with timestamp {ts}", fh)
            with open(os.devnull, "rb") as devnull, open(os.devnull, "ab") as devnull_out:
                subprocess.Popen(
                    cmd,
                    cwd=ROOT,
                    stdin=devnull,
                    stdout=devnull_out,
                    stderr=subprocess.STDOUT,
                    start_new_session=True,
                )
            log("Flowers-102 stage launched; watcher exits.", fh)
            return


if __name__ == "__main__":
    main()
