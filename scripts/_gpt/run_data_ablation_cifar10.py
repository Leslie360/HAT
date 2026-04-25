#!/usr/bin/env python3
"""Gated CIFAR-10 data-fraction ablation runner for Tiny-ViT V3 vs V4.

This wrapper prepares and launches one CIFAR-10 subset experiment at a time for:
  - V3: standard noisy training without HAT
  - V4: noisy training with HAT

Safety guards:
  1. Refuses to run until the R1 fresh-instance gate JSON exists and reports a
     fresh-instance mean above the requested threshold.
  2. Refuses to run if the working-tree ``analog_layers.py`` does not match the
     clean post-bugfix snapshot from commit ``49cacef``.

Use ``--dry-run`` to emit the planned commands without launching training.
Use ``--self-check`` to run lightweight pure-Python sanity checks.
"""

from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[2]
TRAIN_SCRIPT = ROOT / "train_tinyvit.py"
ANALOG_LAYERS = ROOT / "analog_layers.py"

DEFAULT_R1_GATE_JSON = ROOT / "report_md" / "_gpt" / "json_gpt" / "r1_clean_anchor_fresh_eval.json"
DEFAULT_JSON_DIR = ROOT / "report_md" / "_gpt" / "json_gpt"
DEFAULT_LOG_DIR = ROOT / "logs" / "_gpt"
DEFAULT_SAVE_ROOT = ROOT / "checkpoints" / "_gpt" / "data_ablation_cifar10"
EXPECTED_ANALOG_COMMIT = "49cacef"
R1_FRESH_THRESHOLD = 70.0

FRACTION_CHOICES = (0.1, 0.25, 0.5, 1.0)
FRACTION_TAGS = {
    0.1: "0p10",
    0.25: "0p25",
    0.5: "0p50",
    1.0: "1p00",
}


@dataclass(frozen=True)
class ConditionSpec:
    key: str
    experiment: str
    checkpoint_name: str
    label: str


CONDITIONS: tuple[ConditionSpec, ...] = (
    ConditionSpec(
        key="no_hat",
        experiment="V3",
        checkpoint_name="V3_hybrid_standard_noise_standard_train_best.pt",
        label="standard noisy training without HAT",
    ),
    ConditionSpec(
        key="hat",
        experiment="V4",
        checkpoint_name="V4_hybrid_standard_noise_hat_best.pt",
        label="noisy training with HAT",
    ),
)


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def fraction_tag(data_fraction: float) -> str:
    for allowed, tag in FRACTION_TAGS.items():
        if abs(float(data_fraction) - allowed) < 1e-12:
            return tag
    raise ValueError(f"Unsupported data fraction: {data_fraction}")


def json_dump(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def run_git(args: Iterable[str], *, strip: bool = True) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout.strip() if strip else completed.stdout


def inspect_analog_layers(expected_commit: str) -> dict:
    head = run_git(["rev-parse", "--short", "HEAD"])
    dirty = subprocess.run(
        ["git", "diff", "--quiet", "--", str(ANALOG_LAYERS.name)],
        cwd=ROOT,
        check=False,
    ).returncode != 0
    expected_text = run_git(["show", f"{expected_commit}:{ANALOG_LAYERS.name}"], strip=False)
    working_text = ANALOG_LAYERS.read_text(encoding="utf-8")
    return {
        "head_commit": head,
        "expected_commit": expected_commit,
        "analog_layers_path": str(ANALOG_LAYERS),
        "working_tree_dirty": dirty,
        "matches_expected_commit": working_text == expected_text,
    }


def load_r1_gate(gate_json: Path, fresh_threshold: float) -> dict:
    gate = {
        "gate_json": str(gate_json),
        "fresh_threshold": fresh_threshold,
        "exists": gate_json.exists(),
        "passed": False,
        "reason": "",
    }
    if not gate_json.exists():
        gate["reason"] = "R1 fresh-eval JSON is missing."
        return gate

    payload = json.loads(gate_json.read_text(encoding="utf-8"))
    fresh_mean = payload.get("cross_instance_mean")
    gate["payload"] = payload
    gate["fresh_mean"] = fresh_mean
    if fresh_mean is None:
        gate["reason"] = "R1 fresh-eval JSON has no cross_instance_mean."
        return gate

    if float(fresh_mean) <= float(fresh_threshold):
        gate["reason"] = (
            f"R1 fresh-instance mean {fresh_mean:.2f}% does not exceed "
            f"threshold {fresh_threshold:.2f}%."
        )
        return gate

    gate["passed"] = True
    gate["reason"] = (
        f"R1 fresh-instance mean {fresh_mean:.2f}% exceeds "
        f"threshold {fresh_threshold:.2f}%."
    )
    return gate


def build_output_json_path(data_fraction: float, seed: int, output_dir: Path) -> Path:
    tag = fraction_tag(data_fraction)
    return output_dir / f"cifar10_data_ablation_f{tag}_s{seed}.json"


def build_condition_paths(spec: ConditionSpec, data_fraction: float, seed: int, save_root: Path, log_dir: Path) -> dict:
    tag = fraction_tag(data_fraction)
    stem = f"{spec.experiment.lower()}_cifar10_f{tag}_s{seed}"
    save_dir = save_root / stem
    train_log = log_dir / f"{stem}_train.log"
    return {
        "save_dir": save_dir,
        "train_log": train_log,
        "checkpoint_path": save_dir / spec.checkpoint_name,
    }


def build_train_command(args, spec: ConditionSpec, save_dir: Path) -> List[str]:
    command = [
        args.python_bin,
        str(TRAIN_SCRIPT),
        "--mode", "train",
        "--dataset", "cifar10",
        "--experiment", spec.experiment,
        "--epochs", str(args.epochs),
        "--batch-size", str(args.batch_size),
        "--seed", str(args.seed),
        "--data-fraction", f"{args.data_fraction}",
        "--save-dir", str(save_dir),
        "--num-workers", str(args.num_workers),
    ]
    if args.pretrained:
        command.append("--pretrained")
    if args.amp:
        command.append("--amp")
    if args.resume_existing:
        command.append("--resume-existing")
    return command


def command_string(command: Iterable[str]) -> str:
    return shlex.join(list(command))


def stream_command(command: List[str], log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("w", encoding="utf-8") as log_fh:
        log_fh.write(f"$ {command_string(command)}\n")
        log_fh.flush()
        process = subprocess.Popen(
            command,
            cwd=ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        assert process.stdout is not None
        for line in process.stdout:
            sys.stdout.write(line)
            log_fh.write(line)
        return_code = process.wait()
        if return_code != 0:
            raise subprocess.CalledProcessError(return_code, command)


def load_checkpoint_summary(checkpoint_path: Path) -> dict:
    try:
        import torch
    except ImportError as exc:  # pragma: no cover - runtime dependency guard
        raise RuntimeError("torch is required to inspect training checkpoints.") from exc

    checkpoint = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    history = checkpoint.get("history") or {}
    exp_cfg = checkpoint.get("exp_cfg") or {}
    return {
        "checkpoint_path": str(checkpoint_path),
        "epoch": checkpoint.get("epoch"),
        "best_epoch": checkpoint.get("best_epoch"),
        "best_acc": checkpoint.get("best_acc"),
        "dataset": checkpoint.get("dataset"),
        "num_classes": checkpoint.get("num_classes"),
        "seed": checkpoint.get("seed"),
        "data_fraction": checkpoint.get("data_fraction"),
        "experiment_name": exp_cfg.get("name"),
        "history_length": {
            key: len(value) if isinstance(value, list) else 0
            for key, value in history.items()
        },
        "history_tail": {
            key: (value[-1] if isinstance(value, list) and value else None)
            for key, value in history.items()
        },
    }


def preflight_or_raise(gate: dict, analog_status: dict, force: bool) -> None:
    failures = []
    if not gate.get("passed"):
        failures.append(gate.get("reason") or "R1 gate failed.")
    if not analog_status.get("matches_expected_commit"):
        failures.append(
            "analog_layers.py does not match clean commit "
            f"{analog_status['expected_commit']}."
        )
    if force or not failures:
        return
    joined = " ".join(failures)
    raise RuntimeError(joined)


def execute_one_condition(args, spec: ConditionSpec) -> dict:
    paths = build_condition_paths(
        spec=spec,
        data_fraction=args.data_fraction,
        seed=args.seed,
        save_root=args.save_root,
        log_dir=args.log_dir,
    )
    command = build_train_command(args, spec, paths["save_dir"])
    result = {
        "label": spec.label,
        "experiment": spec.experiment,
        "command": command,
        "save_dir": str(paths["save_dir"]),
        "train_log": str(paths["train_log"]),
        "checkpoint_path": str(paths["checkpoint_path"]),
        "status": "planned" if args.dry_run else "running",
    }

    if args.dry_run:
        return result

    stream_command(command, paths["train_log"])
    if not paths["checkpoint_path"].exists():
        raise FileNotFoundError(f"Expected checkpoint missing: {paths['checkpoint_path']}")

    result["checkpoint_summary"] = load_checkpoint_summary(paths["checkpoint_path"])
    result["status"] = "completed"
    return result


def build_payload(args, gate: dict, analog_status: dict, output_json: Path) -> dict:
    return {
        "experiment": "cifar10_data_ablation",
        "generated_at": now_iso(),
        "mode": "dry-run" if args.dry_run else "train",
        "status": "planned" if args.dry_run else "pending",
        "output_json": str(output_json),
        "data_fraction": args.data_fraction,
        "fraction_tag": fraction_tag(args.data_fraction),
        "estimated_train_samples": max(1, int(50000 * args.data_fraction)),
        "seed": args.seed,
        "epochs": args.epochs,
        "batch_size": args.batch_size,
        "num_workers": args.num_workers,
        "pretrained": args.pretrained,
        "amp": args.amp,
        "resume_existing": args.resume_existing,
        "python_bin": args.python_bin,
        "save_root": str(args.save_root),
        "log_dir": str(args.log_dir),
        "r1_gate": gate,
        "analog_layers_guard": analog_status,
        "conditions": {},
    }


def run_self_check() -> None:
    import tempfile

    assert fraction_tag(0.1) == "0p10"
    assert fraction_tag(0.25) == "0p25"
    assert fraction_tag(0.5) == "0p50"
    assert fraction_tag(1.0) == "1p00"

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        gate_json = tmp_path / "gate.json"
        gate_json.write_text(json.dumps({"cross_instance_mean": 75.0}), encoding="utf-8")
        gate = load_r1_gate(gate_json, fresh_threshold=70.0)
        assert gate["passed"]

        missing_gate = load_r1_gate(tmp_path / "missing.json", fresh_threshold=70.0)
        assert not missing_gate["passed"]
        assert "missing" in missing_gate["reason"].lower()

    paths = build_condition_paths(CONDITIONS[0], 0.25, 42, DEFAULT_SAVE_ROOT, DEFAULT_LOG_DIR)
    assert "v3_cifar10_f0p25_s42" in str(paths["save_dir"])
    assert str(paths["checkpoint_path"]).endswith(CONDITIONS[0].checkpoint_name)

    class StubArgs:
        python_bin = "python"
        epochs = 100
        batch_size = 128
        seed = 42
        data_fraction = 0.25
        num_workers = 4
        pretrained = True
        amp = True
        resume_existing = False

    command = build_train_command(StubArgs, CONDITIONS[1], Path("/tmp/save"))
    assert "--experiment" in command and "V4" in command
    assert "--pretrained" in command
    assert "--amp" in command
    print("run_data_ablation_cifar10.py self-check passed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-fraction", type=float, choices=FRACTION_CHOICES, required=False, default=1.0)
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num-workers", type=int, default=4)
    parser.add_argument("--python-bin", default=os.environ.get("PYTHON_BIN") or os.environ.get("PYTHON") or sys.executable)
    parser.add_argument("--r1-gate-json", type=Path, default=DEFAULT_R1_GATE_JSON)
    parser.add_argument("--fresh-threshold", type=float, default=R1_FRESH_THRESHOLD)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_JSON_DIR)
    parser.add_argument("--save-root", type=Path, default=DEFAULT_SAVE_ROOT)
    parser.add_argument("--log-dir", type=Path, default=DEFAULT_LOG_DIR)
    parser.add_argument("--expected-analog-commit", default=EXPECTED_ANALOG_COMMIT)
    parser.add_argument("--resume-existing", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Bypass the R1 and clean-analog preflight guards.")
    parser.add_argument("--self-check", action="store_true")

    pretrained_group = parser.add_mutually_exclusive_group()
    pretrained_group.add_argument("--pretrained", dest="pretrained", action="store_true")
    pretrained_group.add_argument("--no-pretrained", dest="pretrained", action="store_false")
    parser.set_defaults(pretrained=True)

    amp_group = parser.add_mutually_exclusive_group()
    amp_group.add_argument("--amp", dest="amp", action="store_true")
    amp_group.add_argument("--no-amp", dest="amp", action="store_false")
    parser.set_defaults(amp=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.self_check:
        run_self_check()
        return

    output_json = build_output_json_path(args.data_fraction, args.seed, args.output_dir)
    gate = load_r1_gate(args.r1_gate_json, fresh_threshold=args.fresh_threshold)
    analog_status = inspect_analog_layers(args.expected_analog_commit)
    payload = build_payload(args, gate, analog_status, output_json)
    json_dump(output_json, payload)

    if args.dry_run:
        for spec in CONDITIONS:
            payload["conditions"][spec.key] = execute_one_condition(args, spec)
        payload["status"] = "planned"
        payload["generated_at"] = now_iso()
        json_dump(output_json, payload)
        print(f"Dry-run plan written to {output_json}")
        return

    preflight_or_raise(gate=gate, analog_status=analog_status, force=args.force)

    try:
        for spec in CONDITIONS:
            payload["conditions"][spec.key] = execute_one_condition(args, spec)
            payload["generated_at"] = now_iso()
            json_dump(output_json, payload)
    except Exception as exc:
        payload["status"] = "failed"
        payload["generated_at"] = now_iso()
        payload["error"] = str(exc)
        json_dump(output_json, payload)
        raise

    payload["status"] = "completed"
    payload["generated_at"] = now_iso()
    json_dump(output_json, payload)
    print(f"Saved ablation summary to {output_json}")


if __name__ == "__main__":
    main()
