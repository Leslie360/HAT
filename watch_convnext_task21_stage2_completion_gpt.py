#!/usr/bin/env python3
"""Watch ConvNeXt Task 21 Flowers-102 stage, refresh figures, and sync docs."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from pathlib import Path


ROOT = Path("/home/qiaosir/projects/compute_vit")
PY = Path("/home/qiaosir/miniconda3/envs/LLM/bin/python")
GPT_DIR = ROOT / "report_md" / "_gpt"


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
    line = f"[{stamp}] {msg}"
    print(line, file=fh, flush=True)


def maybe_stage2_finished(log_path: Path) -> bool:
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


def append_sync(results: dict[str, tuple[float, float, float]], log_path: Path):
    c1 = results.get("C1")
    c3 = results.get("C3")
    c4 = results.get("C4")

    ag_block = [
        "",
        "## [Codex] 2026-04-06 01:10",
        "",
        "### Task 21 Flowers-102 阶段自动收尾",
        "",
        "- watcher 已确认 `Flowers-102 C1/C3/C4` 完成，并自动刷新主图。",
        "- 结果：",
        f"  - `C1 = {c1[0]:.2f}%`, `MC = {c1[1]:.2f} ± {c1[2]:.2f}%`" if c1 else "  - `C1` missing",
        f"  - `C3 = {c3[0]:.2f}%`, `MC = {c3[1]:.2f} ± {c3[2]:.2f}%`" if c3 else "  - `C3` missing",
        f"  - `C4 = {c4[0]:.2f}%`, `MC = {c4[1]:.2f} ± {c4[2]:.2f}%`" if c4 else "  - `C4` missing",
        "",
        "- 已刷新：",
        "  - `/home/qiaosir/projects/compute_vit/paper/figures/fig4_accuracy_comparison.png`",
        "  - `/home/qiaosir/projects/compute_vit/paper/figures/fig5_hat_recovery.png`",
        "",
        "- 日志：",
        f"  - `{log_path}`",
    ]

    handoff_block = [
        "",
        "## 2026-04-06 01:10 Codex",
        "### Read",
        f"- `{log_path}`",
        "- `/home/qiaosir/projects/compute_vit/report_md/_gpt/json_gpt/convnext_flowers102_c134_results_gpt.json`",
        "- `/home/qiaosir/projects/compute_vit/paper/plot_paper_figures.py`",
        "",
        "### Findings",
        "- Task 21 Flowers-102 stage completed and was auto-summarized.",
        f"- `C1 = {c1[0]:.2f}%`, `C3 = {c3[0]:.2f}%`, `C4 = {c4[0]:.2f}%`" if c1 and c3 and c4 else "- Some result rows were missing in the exported JSON.",
        "",
        "### Changes",
        "- regenerated:",
        "  - `/home/qiaosir/projects/compute_vit/paper/figures/fig4_accuracy_comparison.png`",
        "  - `/home/qiaosir/projects/compute_vit/paper/figures/fig5_hat_recovery.png`",
        "",
        "### Next suggested step",
        "- move to Task 25 / Task 31 on final cross-architecture, cross-dataset figures and results restructuring",
    ]

    changelog_block = [
        "",
        "## 2026-04-06 01:10 Codex",
        "### Findings",
        "- ConvNeXt Task 21 Flowers-102 stage finished and final Task 21 figure refresh was triggered automatically.",
        f"- Flowers-102 results: C1={c1[0]:.2f}%, C3={c3[0]:.2f}%, C4={c4[0]:.2f}%" if c1 and c3 and c4 else "- Flowers-102 JSON was incomplete at sync time.",
        "",
        "### Changes",
        "- regenerated:",
        "  - `/home/qiaosir/projects/compute_vit/paper/figures/fig4_accuracy_comparison.png`",
        "  - `/home/qiaosir/projects/compute_vit/paper/figures/fig5_hat_recovery.png`",
    ]

    (GPT_DIR / "AGENT_SYNC_gpt.md").open("a", encoding="utf-8").write("\n".join(ag_block) + "\n")
    (GPT_DIR / "LLM_HANDOFF_gpt.md").open("a", encoding="utf-8").write("\n".join(handoff_block) + "\n")
    (GPT_DIR / "LLM_CHANGELOG_gpt.md").open("a", encoding="utf-8").write("\n".join(changelog_block) + "\n")


def main():
    parser = argparse.ArgumentParser(description="Watch Flowers-102 ConvNeXt stage and refresh paper figures.")
    parser.add_argument("--stage2-pid", type=int, required=True)
    parser.add_argument("--stage2-log", type=str, required=True)
    parser.add_argument("--watch-log", type=str, required=True)
    parser.add_argument("--poll-seconds", type=int, default=60)
    args = parser.parse_args()

    stage2_log = Path(args.stage2_log)
    watch_log = Path(args.watch_log)
    watch_log.parent.mkdir(parents=True, exist_ok=True)

    with watch_log.open("a", encoding="utf-8") as fh:
        log(f"Watcher armed for Flowers PID {args.stage2_pid}", fh)
        log(f"Stage-2 log: {stage2_log}", fh)

        while True:
            if pid_alive(args.stage2_pid):
                log("Stage-2 still running; sleeping.", fh)
                time.sleep(args.poll_seconds)
                continue

            log("Stage-2 process exited; inspecting final state.", fh)
            if not maybe_stage2_finished(stage2_log):
                log("Stage-2 ended without a clean summary; watcher exits without sync.", fh)
                return

            plot_cmd = [str(PY), str(ROOT / "paper" / "plot_paper_figures.py")]
            log("Refreshing paper figures.", fh)
            subprocess.run(plot_cmd, cwd=ROOT, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

            result_path = GPT_DIR / "json_gpt" / "convnext_flowers102_c134_results_gpt.json"
            if not result_path.exists():
                log("Flowers JSON export missing after stage completion; watcher exits after figure refresh.", fh)
                return

            results = parse_results(result_path)
            append_sync(results, stage2_log)
            log("Flowers summary synced to GPT coordination docs.", fh)
            return


if __name__ == "__main__":
    main()
