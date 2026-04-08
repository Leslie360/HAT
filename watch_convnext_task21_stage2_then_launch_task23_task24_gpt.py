#!/usr/bin/env python3
"""Watch ConvNeXt Task 21 Flowers stage and auto-launch Task 23/24 pipeline."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from pathlib import Path


ROOT = Path("/home/qiaosir/projects/compute_vit")
GPT_DIR = ROOT / "report_md" / "_gpt"
LAUNCH_MARKER = ROOT / "logs" / "_gpt" / "task23_task24_after_task21_launch_gpt.json"
PY = Path("/home/qiaosir/miniconda3/envs/LLM/bin/python")


def pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def log(msg: str, fh):
    stamp = time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{stamp}] {msg}", file=fh, flush=True)


def stage2_finished(log_path: Path) -> bool:
    if not log_path.exists():
        return False
    text = log_path.read_text(encoding="utf-8", errors="ignore")
    return "Experiment C4:" in text and "SUMMARY" in text and "Results exported to:" in text


def parse_results(path: Path) -> dict[str, tuple[float, float, float]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("results", [])
    out: dict[str, tuple[float, float, float]] = {}
    for row in rows:
        exp = row.get("experiment")
        if not exp:
            continue
        best = float(row.get("best_test_acc", row.get("best_acc", float("nan"))))
        mc = float(row.get("mc_mean_acc", best))
        std = float(row.get("mc_std_acc", 0.0))
        out[exp] = (best, mc, std)
    return out


def append_sync(stage2_log: Path, driver_log: Path, launched_pid: int,
                results: dict[str, tuple[float, float, float]]):
    c1 = results.get("C1")
    c3 = results.get("C3")
    c4 = results.get("C4")

    ag_block = [
        "",
        f"## [Codex] {time.strftime('%Y-%m-%d %H:%M')}",
        "",
        "### Task 21 Flowers-102 自动收尾 + Task 24/23 自动接续",
        "",
        "- `Flowers-102` ConvNeXt stage 已完成，主图已刷新，并已自动启动 stage 3：",
        f"  - `C1 = {c1[0]:.2f}%`, `MC = {c1[1]:.2f} ± {c1[2]:.2f}%`" if c1 else "  - `C1` missing",
        f"  - `C3 = {c3[0]:.2f}%`, `MC = {c3[1]:.2f} ± {c3[2]:.2f}%`" if c3 else "  - `C3` missing",
        f"  - `C4 = {c4[0]:.2f}%`, `MC = {c4[1]:.2f} ± {c4[2]:.2f}%`" if c4 else "  - `C4` missing",
        "",
        "- 已刷新：",
        "  - `/home/qiaosir/projects/compute_vit/paper/figures/fig4_accuracy_comparison.png`",
        "  - `/home/qiaosir/projects/compute_vit/paper/figures/fig5_hat_recovery.png`",
        "",
        "- 已自动启动：",
        "  - `Task 24`: `V4` proportional-noise MC eval",
        "  - `Task 23`: `V4_NL_moderate`, `V4_NL_severe`, `C4_NL_moderate`",
        "- 采用独立 save-dir / report artifact，未污染 canonical `V4/C4` 结果。",
        f"- Stage-2 log: `{stage2_log}`",
        f"- Stage-3 driver log: `{driver_log}`",
        f"- Stage-3 launcher PID: `{launched_pid}`",
    ]

    handoff_block = [
        "",
        f"## {time.strftime('%Y-%m-%d %H:%M')} Codex",
        "### Read",
        f"- `{stage2_log}`",
        "- `/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/convnext_flowers102_c134_results_gpt.json`",
        "- `/home/qiaosir/projects/compute_vit/paper/plot_paper_figures.py`",
        "",
        "### Findings",
        "- Flowers-102 ConvNeXt stage finished cleanly and stage 3 was auto-launched.",
        f"- `C1 = {c1[0]:.2f}%`, `C3 = {c3[0]:.2f}%`, `C4 = {c4[0]:.2f}%`" if c1 and c3 and c4 else "- Some Flowers rows were missing in JSON at sync time.",
        "",
        "### Changes",
        "- regenerated:",
        "  - `/home/qiaosir/projects/compute_vit/paper/figures/fig4_accuracy_comparison.png`",
        "  - `/home/qiaosir/projects/compute_vit/paper/figures/fig5_hat_recovery.png`",
        "- auto-launched stage 3 driver:",
        f"  - `{driver_log}`",
        "",
        "### Next suggested step",
        "- let Task 24/23 stage 3 complete, then fold results into §5 / final figures",
    ]

    changelog_block = [
        "",
        f"## {time.strftime('%Y-%m-%d %H:%M')} Codex",
        "### Findings",
        "- Flowers-102 ConvNeXt stage finished; figure refresh and stage-3 launch were completed automatically.",
        f"- Flowers results: C1={c1[0]:.2f}%, C3={c3[0]:.2f}%, C4={c4[0]:.2f}%" if c1 and c3 and c4 else "- Flowers JSON was incomplete at sync time.",
        "",
        "### Changes",
        "- regenerated:",
        "  - `/home/qiaosir/projects/compute_vit/paper/figures/fig4_accuracy_comparison.png`",
        "  - `/home/qiaosir/projects/compute_vit/paper/figures/fig5_hat_recovery.png`",
        "- launched:",
        f"  - `{driver_log}`",
    ]

    (GPT_DIR / "AGENT_SYNC_gpt.md").open("a", encoding="utf-8").write("\n".join(ag_block) + "\n")
    (GPT_DIR / "LLM_HANDOFF_gpt.md").open("a", encoding="utf-8").write("\n".join(handoff_block) + "\n")
    (GPT_DIR / "LLM_CHANGELOG_gpt.md").open("a", encoding="utf-8").write("\n".join(changelog_block) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Watch Flowers stage and launch Task 23/24.")
    parser.add_argument("--stage2-pid", type=int, required=True)
    parser.add_argument("--stage2-log", type=str, required=True)
    parser.add_argument("--watch-log", type=str, required=True)
    parser.add_argument("--poll-seconds", type=int, default=60)
    args = parser.parse_args()

    stage2_log = Path(args.stage2_log)
    watch_log = Path(args.watch_log)
    stage3_script = ROOT / "run_task23_task24_after_task21_gpt.sh"
    watch_log.parent.mkdir(parents=True, exist_ok=True)

    with watch_log.open("a", encoding="utf-8") as fh:
        log(f"Task23/24 watcher armed for Flowers PID {args.stage2_pid}", fh)
        log(f"Stage-2 log: {stage2_log}", fh)
        log(f"Launch marker: {LAUNCH_MARKER}", fh)

        while True:
            if LAUNCH_MARKER.exists():
                log("Launch marker already exists; watcher exits.", fh)
                return
            if pid_alive(args.stage2_pid):
                log("Stage-2 still running; sleeping.", fh)
                time.sleep(args.poll_seconds)
                continue

            log("Stage-2 process exited; checking for clean completion.", fh)
            if not stage2_finished(stage2_log):
                log("Stage-2 log has no clean summary; watcher exits without launch.", fh)
                return

            plot_cmd = [str(PY), str(ROOT / "paper" / "plot_paper_figures.py")]
            log("Refreshing paper figures.", fh)
            subprocess.run(plot_cmd, cwd=ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

            result_path = GPT_DIR / "json_gpt" / "convnext_flowers102_c134_results_gpt.json"
            if not result_path.exists():
                log("Flowers JSON export missing after stage completion; watcher exits without stage-3 launch.", fh)
                return
            results = parse_results(result_path)

            ts = time.strftime("%Y%m%d_%H%M%S")
            driver_log = ROOT / "logs" / "_gpt" / f"task23_task24_after_task21_{ts}_driver_gpt.log"
            proc = subprocess.Popen(
                ["/bin/bash", str(stage3_script), ts],
                cwd=ROOT,
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            marker_payload = {
                "launched_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "stage2_log": str(stage2_log),
                "driver_log": str(driver_log),
                "launcher_pid": proc.pid,
            }
            LAUNCH_MARKER.write_text(json.dumps(marker_payload, indent=2), encoding="utf-8")
            append_sync(stage2_log, driver_log, proc.pid, results)
            log(f"Stage-3 launched with PID {proc.pid}.", fh)
            log(f"Driver log: {driver_log}", fh)
            return


if __name__ == "__main__":
    main()
