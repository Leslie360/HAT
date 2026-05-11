#!/usr/bin/env python3
"""Parse Work-2 attention-output training-step logs into TSV audits."""

from __future__ import annotations

import json
import math
import re
import statistics
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
LOG_DIR = ROOT / "archive" / "residual_logs_gpt_20260510" / "logs" / "_gpt"
RESULTS_DIR = ROOT / "paper2" / "results"
DATE_TAG = "20260511"
STEP_TSV = RESULTS_DIR / f"W2_ATTENTION_OUTPUT_STEP_SERIES_{DATE_TAG}.tsv"
RUN_TSV = RESULTS_DIR / f"W2_ATTENTION_OUTPUT_STEP_RUNS_{DATE_TAG}.tsv"
SUMMARY_TSV = RESULTS_DIR / f"W2_ATTENTION_OUTPUT_STEP_SUMMARY_{DATE_TAG}.tsv"


def extract_json_objects(text: str) -> list[dict[str, Any]]:
    decoder = json.JSONDecoder()
    objects: list[dict[str, Any]] = []
    idx = 0
    while True:
        pos = text.find("{", idx)
        if pos < 0:
            break
        try:
            obj, end = decoder.raw_decode(text[pos:])
        except json.JSONDecodeError:
            idx = pos + 1
            continue
        if isinstance(obj, dict):
            objects.append(obj)
        idx = pos + end
    return objects


def value_from_argv(argv: list[str], flag: str) -> str:
    if flag not in argv:
        return ""
    idx = argv.index(flag)
    return str(argv[idx + 1]) if idx + 1 < len(argv) else ""


def flag_present(argv: list[str], flag: str) -> int:
    return int(flag in argv)


def parse_seed_from_name(name: str) -> str:
    match = re.search(r"seed(\d+)", name)
    return match.group(1) if match else ""


def parse_scope_from_name(name: str) -> str:
    if "attention_output" in name:
        return "attention_output"
    return "unknown"


def finite_or_blank(value: Any) -> str:
    if value is None or value == "":
        return ""
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(numeric):
        return ""
    return f"{numeric:.8g}"


def summarize_run(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    text = path.read_text(encoding="utf-8", errors="replace")
    objects = extract_json_objects(text)
    start = next((obj for obj in objects if obj.get("event") == "start"), {})
    complete = next((obj for obj in objects if obj.get("event") == "complete"), {})
    eval_before = next((obj for obj in objects if obj.get("event") == "eval_before"), {})
    eval_after = next((obj for obj in objects if obj.get("event") == "eval_after"), {})
    fresh_d2d = next((obj for obj in objects if obj.get("event") == "fresh_d2d_eval"), {})
    steps = [obj for obj in objects if obj.get("event") == "step"]
    argv = [str(item) for item in start.get("argv", [])] if isinstance(start.get("argv"), list) else []

    run_id = path.stem
    losses = []
    step_rows: list[dict[str, Any]] = []
    for obj in steps:
        loss = obj.get("pre_update_loss", obj.get("loss"))
        if loss is None:
            continue
        loss_f = float(loss)
        losses.append(loss_f)
        step_rows.append(
            {
                "run_id": run_id,
                "source_log": path.as_posix(),
                "step": int(obj.get("step", -1)),
                "loss": loss_f,
                "resampled": int(obj.get("resampled", 0) or 0),
            }
        )

    sigma_d2d = start.get("sigma_d2d", value_from_argv(argv, "--sigma-d2d"))
    sigma_c2c = start.get("sigma_c2c", value_from_argv(argv, "--sigma-c2c"))
    lr = start.get("lr", value_from_argv(argv, "--lr"))
    seed = start.get("seed", value_from_argv(argv, "--seed") or parse_seed_from_name(path.name))
    steps_requested = start.get("steps", value_from_argv(argv, "--steps"))
    max_length = start.get("max_length", value_from_argv(argv, "--max-length"))
    resample_every = start.get("resample_every", value_from_argv(argv, "--resample-every"))
    analog_scope = start.get("analog_scope", value_from_argv(argv, "--analog-scope") or parse_scope_from_name(path.name))
    train_scope = start.get("train_scope", value_from_argv(argv, "--train-scope"))

    run = {
        "run_id": run_id,
        "source_log": path.as_posix(),
        "completed": int(bool(complete)),
        "model": start.get("model", ""),
        "analog_scope": analog_scope,
        "train_scope": train_scope,
        "seed": seed,
        "steps_requested": steps_requested,
        "step_count": len(losses),
        "max_length": max_length,
        "lr": lr,
        "sigma_d2d": sigma_d2d,
        "sigma_c2c": sigma_c2c,
        "resample_every": resample_every,
        "noise_enabled": start.get("noise_enabled", flag_present(argv, "--noise-enabled") if argv else ""),
        "high_precision_analog": start.get("high_precision_analog", flag_present(argv, "--high-precision-analog") if argv else ""),
        "initial_step_loss": losses[0] if losses else "",
        "final_step_loss": losses[-1] if losses else "",
        "min_step_loss": min(losses) if losses else "",
        "max_step_loss": max(losses) if losses else "",
        "mean_step_loss": statistics.mean(losses) if losses else "",
        "std_step_loss": statistics.pstdev(losses) if len(losses) > 1 else 0.0 if losses else "",
        "step_loss_delta": (losses[-1] - losses[0]) if losses else "",
        "step_loss_decreased": int(losses[-1] < losses[0]) if losses else "",
        "eval_before_mean": eval_before.get("mean_loss", complete.get("eval_before_mean", "")),
        "eval_after_mean": eval_after.get("mean_loss", complete.get("eval_after_mean", "")),
        "eval_delta": complete.get("eval_delta", ""),
        "eval_decreased": complete.get("eval_decreased", ""),
        "fresh_d2d_mean_loss": fresh_d2d.get("mean_loss", complete.get("fresh_d2d_mean_loss", "")),
        "fresh_d2d_std_loss": fresh_d2d.get("std_loss", complete.get("fresh_d2d_std_loss", "")),
        "fresh_d2d_instances": fresh_d2d.get("instances", complete.get("fresh_d2d_instances", "")),
        "fresh_d2d_repeats": fresh_d2d.get("repeats_per_instance", complete.get("fresh_d2d_repeats", "")),
        "peak_cuda_mem_gb": complete.get("peak_cuda_mem_gb", ""),
        "elapsed_s": complete.get("elapsed_s", ""),
    }
    return run, step_rows


def write_tsv(path: Path, rows: list[dict[str, Any]], columns: list[str]) -> None:
    lines = ["\t".join(columns)]
    for row in rows:
        lines.append("\t".join(finite_or_blank(row.get(column, "")) for column in columns))
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    logs = sorted(LOG_DIR.glob("*attention_output*.log"))
    runs: list[dict[str, Any]] = []
    steps: list[dict[str, Any]] = []
    for path in logs:
        run, step_rows = summarize_run(path)
        runs.append(run)
        steps.extend(step_rows)

    step_columns = ["run_id", "source_log", "step", "loss", "resampled"]
    run_columns = [
        "run_id",
        "source_log",
        "completed",
        "model",
        "analog_scope",
        "train_scope",
        "seed",
        "steps_requested",
        "step_count",
        "max_length",
        "lr",
        "sigma_d2d",
        "sigma_c2c",
        "resample_every",
        "noise_enabled",
        "high_precision_analog",
        "initial_step_loss",
        "final_step_loss",
        "min_step_loss",
        "max_step_loss",
        "mean_step_loss",
        "std_step_loss",
        "step_loss_delta",
        "step_loss_decreased",
        "eval_before_mean",
        "eval_after_mean",
        "eval_delta",
        "eval_decreased",
        "fresh_d2d_mean_loss",
        "fresh_d2d_std_loss",
        "fresh_d2d_instances",
        "fresh_d2d_repeats",
        "peak_cuda_mem_gb",
        "elapsed_s",
    ]

    grouped: dict[tuple[str, str, str, str, str], list[dict[str, Any]]] = {}
    for row in runs:
        key = (
            str(row.get("analog_scope", "")),
            str(row.get("sigma_d2d", "")),
            str(row.get("sigma_c2c", "")),
            str(row.get("steps_requested", "")),
            str(row.get("max_length", "")),
        )
        grouped.setdefault(key, []).append(row)

    summaries: list[dict[str, Any]] = []
    for (analog_scope, sigma_d2d, sigma_c2c, steps_requested, max_length), items in sorted(grouped.items()):
        final_losses = [float(item["final_step_loss"]) for item in items if item.get("final_step_loss") != ""]
        eval_deltas = [float(item["eval_delta"]) for item in items if item.get("eval_delta") != ""]
        summaries.append(
            {
                "analog_scope": analog_scope,
                "sigma_d2d": sigma_d2d,
                "sigma_c2c": sigma_c2c,
                "steps_requested": steps_requested,
                "max_length": max_length,
                "n_runs": len(items),
                "n_completed": sum(int(item.get("completed", 0)) for item in items),
                "seeds": ",".join(str(item.get("seed", "")) for item in items if item.get("seed", "") != ""),
                "mean_final_step_loss": statistics.mean(final_losses) if final_losses else "",
                "std_final_step_loss": statistics.pstdev(final_losses) if len(final_losses) > 1 else 0.0 if final_losses else "",
                "mean_eval_delta": statistics.mean(eval_deltas) if eval_deltas else "",
                "std_eval_delta": statistics.pstdev(eval_deltas) if len(eval_deltas) > 1 else 0.0 if eval_deltas else "",
            }
        )

    summary_columns = [
        "analog_scope",
        "sigma_d2d",
        "sigma_c2c",
        "steps_requested",
        "max_length",
        "n_runs",
        "n_completed",
        "seeds",
        "mean_final_step_loss",
        "std_final_step_loss",
        "mean_eval_delta",
        "std_eval_delta",
    ]

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    write_tsv(STEP_TSV, steps, step_columns)
    write_tsv(RUN_TSV, runs, run_columns)
    write_tsv(SUMMARY_TSV, summaries, summary_columns)
    print(f"logs={len(logs)}")
    print(f"runs={len(runs)}")
    print(f"steps={len(steps)}")
    print(f"step_tsv={STEP_TSV}")
    print(f"run_tsv={RUN_TSV}")
    print(f"summary_tsv={SUMMARY_TSV}")


if __name__ == "__main__":
    main()
