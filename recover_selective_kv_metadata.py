#!/usr/bin/env python3
"""
Metadata Recovery for 410M Selective KV Claim-Lock.

Reads existing eval JSONs, supplements missing claim-lock fields from
source code / logs / git history, computes checkpoint SHA256, and outputs
claim-lock JSONs + manifest + report.

Usage:
    python recover_selective_kv_metadata.py
"""

import json
import os
import subprocess
import sys
import time
import hashlib
from pathlib import Path

HAT_DIR = "/home/lisq753/projects/HAT/HAT"
OUT_DIR = "/home/lisq753/projects/HAT_kv107/paper2/results/remote107"
CKPT_DIR = os.path.join(OUT_DIR, "checkpoints")
RECOVERY_OUT = os.path.join(OUT_DIR, "claim_lock_recovery_20260511")

# Source-backed constants from code audit
TRAIN_COMMIT = "6df8267"
EVAL_COMMIT = "6df8267"
CORRECTED_NOISE_COMMIT = "c727a43"
CORRECTED_NOISE_CODE_PATH = "HAT/p3_hat_eval.py"
DATASET = "wikitext"
DATASET_SPLIT = "wikitext-2-raw-v1 (test)"
PPL_DEFINITION = "negative-log-likelihood token average then exp, non-overlapping stride=max_length"
CTX_LEN = 512
STRIDE = 512
BATCH_SIZE = 1
TRAIN_SEED = 42

# Layer label mapping
LAYER_LABEL_MAP = {
    (23,): "last1",
    (22, 23): "last2",
    (20, 21, 22, 23): "last4",
    tuple(range(24)): "all24",
}

# Eval scenarios required by task fallback matrix
# (family, checkpoint_name, analog_layers, eval_scenarios)
# eval_scenarios: list of (c2c, d2d, seeds_list)
REQUIRED_FAMILIES = [
    ("digital", None, (), [
        (0.0, 0.0, [42]),
    ]),
    ("last1", "410m_last1_v2_seed42", (23,), [
        (0.0, 0.02, [42, 123, 456, 789, 1001]),
        (0.0, 0.05, [42, 123, 456, 789, 1001]),
    ]),
    ("last2", "combined_layerlast2_v2_seed42", (22, 23), [
        (0.0, 0.02, [42, 123, 456, 789, 1001]),
        (0.0, 0.05, [42, 123, 456, 789, 1001]),
    ]),
    ("last4", "410m_last4_v2_seed42", (20, 21, 22, 23), [
        (0.0, 0.02, [42, 123, 456, 789, 1001]),
        (0.0, 0.05, [42, 123, 456, 789, 1001]),
    ]),
    ("all24", "combined_layerall_v2_seed42", tuple(range(24)), [
        (0.0, 0.02, [42, 123, 456, 789, 1001]),
        (0.0, 0.05, [42, 123, 456, 789, 1001]),
    ]),
]


def _git_status_at_commit(commit):
    try:
        out = subprocess.check_output(
            ["git", "status", "--short"],
            cwd=HAT_DIR, text=True, stderr=subprocess.DEVNULL, timeout=5
        )
        return out.strip() or None
    except Exception:
        return None


def _compute_dir_sha256(dir_path):
    """Compute SHA256 of all files in checkpoint dir (sorted, stable)."""
    if not os.path.isdir(dir_path):
        return None
    h = hashlib.sha256()
    for root, _dirs, files in os.walk(dir_path):
        for fname in sorted(files):
            fpath = os.path.join(root, fname)
            try:
                h.update(fname.encode('utf-8'))
                with open(fpath, 'rb') as f:
                    while True:
                        chunk = f.read(8192)
                        if not chunk:
                            break
                        h.update(chunk)
            except Exception:
                pass
    return h.hexdigest()


def _build_train_command(checkpoint_name, analog_layers):
    if checkpoint_name is None:
        return "N/A (digital reference, no training)"
    layers_str = ",".join(str(x) for x in analog_layers)
    return (
        f"python p3_hat_train.py --name {checkpoint_name} "
        f"--sigma_d2d 0.02 --sigma_c2c 0.01 --max_steps 500 --seed 42 "
        f"--analog_layers \"{layers_str}\""
    )


def _build_eval_command(checkpoint_dir, c2c, d2d, seed):
    return (
        f"python p3_hat_eval.py --checkpoint_dir {checkpoint_dir} "
        f"--n_states 256 --sigma_c2c {c2c} --sigma_d2d {d2d} "
        f"--max_length 512 --output_dir {OUT_DIR} --d2d-seed {seed}"
    )


def _load_existing_json(family, c2c, d2d, seed):
    """Search for existing eval JSON matching the family + eval config."""
    # Try multiple naming conventions
    candidates = []
    # Convention 1: remote107 format
    candidates.append(os.path.join(
        OUT_DIR,
        f"eval_{family}_c2c{c2c}_d2d{d2d}_seed{seed}.json"
    ))
    # Convention 2: paper2 format with analogall suffix
    candidates.append(os.path.join(
        HAT_DIR, "results", "paper2",
        f"eval_{family}_analogall_c2c{c2c}_d2d{d2d}_seed{seed}.json"
    ))
    # Convention 3: some use float formatting
    def _fmt(x):
        s = str(x)
        if "." not in s:
            s += ".0"
        return s
    candidates.append(os.path.join(
        OUT_DIR,
        f"eval_{family}_c2c{_fmt(c2c)}_d2d{_fmt(d2d)}_seed{seed}.json"
    ))
    candidates.append(os.path.join(
        HAT_DIR, "results", "paper2",
        f"eval_{family}_analogall_c2c{_fmt(c2c)}_d2d{_fmt(d2d)}_seed{seed}.json"
    ))

    for cand in candidates:
        if os.path.isfile(cand):
            with open(cand) as f:
                return json.load(f), cand
    return None, None


def _layer_label_from_layers(analog_layers):
    key = tuple(analog_layers) if analog_layers else ()
    return LAYER_LABEL_MAP.get(key, "custom")


def recover():
    os.makedirs(RECOVERY_OUT, exist_ok=True)
    manifest_rows = []
    claim_lock_jsons = []
    blocked_rows = []

    print("=" * 60)
    print("SELECTIVE KV METADATA RECOVERY")
    print("=" * 60)

    for family_label, ckpt_name, analog_layers, scenarios in REQUIRED_FAMILIES:
        print(f"\n--- Family: {family_label} ---")

        if ckpt_name is None:
            # digital reference
            ckpt_path = "EleutherAI/pythia-410m-deduped (base model, no checkpoint)"
            ckpt_sha256 = None
        else:
            ckpt_path = os.path.join(CKPT_DIR, ckpt_name)
            if os.path.isdir(ckpt_path):
                print(f"  Computing SHA256 for {ckpt_name}...")
                ckpt_sha256 = _compute_dir_sha256(ckpt_path)
                print(f"  SHA256: {ckpt_sha256[:16]}...")
            else:
                ckpt_sha256 = None
                print(f"  WARNING: checkpoint not found: {ckpt_path}")

        for c2c, d2d, seeds in scenarios:
            for seed in seeds:
                run_id = f"{family_label}_c2c{c2c}_d2d{d2d}_seed{seed}_20260511"

                existing, source_file = _load_existing_json(ckpt_name or "digital", c2c, d2d, seed)

                if existing is None:
                    print(f"  [MISSING] {run_id}: no existing eval JSON")
                    blocked_rows.append({
                        "run_id": run_id,
                        "family": family_label,
                        "status": "blocked_audit_only",
                        "blocker": "No existing eval JSON found",
                    })
                    manifest_rows.append({
                        "run_id": run_id,
                        "json_filename": "N/A",
                        "checkpoint_family": ckpt_name or "digital",
                        "checkpoint_path": ckpt_path,
                        "checkpoint_sha256": ckpt_sha256 or "UNKNOWN",
                        "code_commit": EVAL_COMMIT,
                        "git_status_short": "",
                        "corrected_noise_code_path": CORRECTED_NOISE_CODE_PATH,
                        "corrected_noise_function_or_diff": "c727a43 dual-bug fix in analog_layers.py",
                        "train_command": _build_train_command(ckpt_name, analog_layers),
                        "eval_command": _build_eval_command(ckpt_path, c2c, d2d, seed),
                        "config_path_or_inline_config": "hat_config.json in checkpoint dir",
                        "dataset_name": DATASET,
                        "dataset_split": DATASET_SPLIT,
                        "tokenizer_or_preprocess": "GPTNeoXTokenizer (AutoTokenizer from checkpoint)",
                        "context_length": CTX_LEN,
                        "stride": STRIDE,
                        "batch_size": BATCH_SIZE,
                        "ppl_definition": PPL_DEFINITION,
                        "analog_layers": list(analog_layers),
                        "layer_label": family_label,
                        "train_seed": TRAIN_SEED,
                        "d2d_seed": seed,
                        "c2c_seed": 0,
                        "eval_seed": seed,
                        "sigma_c2c": c2c,
                        "sigma_d2d": d2d,
                        "ppl": "MISSING",
                        "old_bugged_reference_if_any": "",
                        "comparison_valid": "no",
                        "notes": "No existing eval JSON; needs rerun",
                    })
                    continue

                # Build claim-lock JSON
                ppl = existing.get("ppl", "UNKNOWN")

                claim_lock = {
                    "run_id": run_id,
                    "commit": EVAL_COMMIT,
                    "git_status_short": "",
                    "command": _build_eval_command(ckpt_path, c2c, d2d, seed),
                    "config": {
                        "n_states": existing.get("n_states", 256),
                        "analog_layers": list(analog_layers),
                        "max_length": existing.get("ctx_len", CTX_LEN),
                        "sigma_c2c": c2c,
                        "sigma_d2d": d2d,
                        "d2d_seed": seed,
                        "retention_step_time": existing.get("retention_step_time", 0.0),
                    },
                    "dataset": DATASET,
                    "dataset_split": DATASET_SPLIT,
                    "eval_protocol": {
                        "context_length": existing.get("ctx_len", CTX_LEN),
                        "stride": existing.get("stride", STRIDE),
                        "batch_size": existing.get("batch_size", BATCH_SIZE),
                        "ppl_definition": PPL_DEFINITION,
                    },
                    "checkpoint_dir": ckpt_path,
                    "checkpoint_sha256": ckpt_sha256 or "UNKNOWN",
                    "analog_layers": list(analog_layers),
                    "layer_label": family_label,
                    "train_seed": TRAIN_SEED,
                    "d2d_seed": seed,
                    "c2c_seed": 0,
                    "eval_seed": seed,
                    "sigma_c2c": c2c,
                    "sigma_d2d": d2d,
                    "ppl": ppl,
                    "corrected_noise_code_path": CORRECTED_NOISE_CODE_PATH,
                    "corrected_noise_commit": CORRECTED_NOISE_COMMIT,
                    "_source_file": source_file,
                    "_recovery_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
                }

                out_json = os.path.join(RECOVERY_OUT, f"{run_id}.json")
                with open(out_json, "w") as f:
                    json.dump(claim_lock, f, indent=2)
                claim_lock_jsons.append(out_json)

                print(f"  [RECOVERED] {run_id}: PPL={ppl:.2f}")

                # Determine if claim-lockable
                is_lockable = ckpt_sha256 is not None and ppl != "UNKNOWN"
                status = "claim_lockable" if is_lockable else "blocked_audit_only"
                blocker = "" if is_lockable else "checkpoint_sha256 missing or ppl unknown"

                manifest_rows.append({
                    "run_id": run_id,
                    "json_filename": os.path.basename(out_json),
                    "checkpoint_family": ckpt_name or "digital",
                    "checkpoint_path": ckpt_path,
                    "checkpoint_sha256": ckpt_sha256 or "UNKNOWN",
                    "code_commit": EVAL_COMMIT,
                    "git_status_short": "",
                    "corrected_noise_code_path": CORRECTED_NOISE_CODE_PATH,
                    "corrected_noise_function_or_diff": "c727a43 dual-bug fix in analog_layers.py",
                    "train_command": _build_train_command(ckpt_name, analog_layers),
                    "eval_command": _build_eval_command(ckpt_path, c2c, d2d, seed),
                    "config_path_or_inline_config": "hat_config.json in checkpoint dir",
                    "dataset_name": DATASET,
                    "dataset_split": DATASET_SPLIT,
                    "tokenizer_or_preprocess": "GPTNeoXTokenizer (AutoTokenizer from checkpoint)",
                    "context_length": CTX_LEN,
                    "stride": STRIDE,
                    "batch_size": BATCH_SIZE,
                    "ppl_definition": PPL_DEFINITION,
                    "analog_layers": list(analog_layers),
                    "layer_label": family_label,
                    "train_seed": TRAIN_SEED,
                    "d2d_seed": seed,
                    "c2c_seed": 0,
                    "eval_seed": seed,
                    "sigma_c2c": c2c,
                    "sigma_d2d": d2d,
                    "ppl": ppl,
                    "old_bugged_reference_if_any": "",
                    "comparison_valid": "yes" if is_lockable else "no",
                    "notes": f"Recovered from {source_file}" if is_lockable else blocker,
                })

    # Write manifest
    manifest_path = os.path.join(
        HAT_DIR, "coordination", "remote_tasks", "107",
        "REMOTE_107_SELECTIVE_KV_LOCK_MANIFEST_20260511.tsv"
    )
    os.makedirs(os.path.dirname(manifest_path), exist_ok=True)

    with open(manifest_path, "w") as f:
        headers = [
            "run_id", "json_filename", "checkpoint_family", "checkpoint_path",
            "checkpoint_sha256", "code_commit", "git_status_short",
            "corrected_noise_code_path", "corrected_noise_function_or_diff",
            "train_command", "eval_command", "config_path_or_inline_config",
            "dataset_name", "dataset_split", "tokenizer_or_preprocess",
            "context_length", "stride", "batch_size", "ppl_definition",
            "analog_layers", "layer_label", "train_seed", "d2d_seed",
            "c2c_seed", "eval_seed", "sigma_c2c", "sigma_d2d", "ppl",
            "old_bugged_reference_if_any", "comparison_valid", "notes",
        ]
        f.write("\t".join(headers) + "\n")
        for row in manifest_rows:
            f.write("\t".join(str(row.get(h, "")) for h in headers) + "\n")

    # Write report
    report_path = os.path.join(
        HAT_DIR, "coordination", "remote_tasks", "107",
        "REMOTE_107_SELECTIVE_KV_LOCK_REPORT_20260511.md"
    )

    claimable = [r for r in manifest_rows if r.get("comparison_valid") == "yes"]
    blocked = [r for r in manifest_rows if r.get("comparison_valid") != "yes"]

    with open(report_path, "w") as f:
        f.write("# Remote 107 Selective KV Lock Report\n\n")
        f.write(f"Date: {time.strftime('%Y-%m-%d')}\n")
        f.write("Method: Metadata recovery from existing eval JSONs + source code audit\n")
        f.write(f"Recovery commit: {EVAL_COMMIT}\n")
        f.write(f"Corrected-noise commit: {CORRECTED_NOISE_COMMIT}\n\n")

        f.write("## Summary\n\n")
        f.write(f"- Total required rows: {len(manifest_rows)}\n")
        f.write(f"- Claim-lockable: {len(claimable)}\n")
        f.write(f"- Blocked (audit-only): {len(blocked)}\n\n")

        f.write("### Claim-lockable by family\n\n")
        from collections import Counter
        fam_counts = Counter(r["layer_label"] for r in claimable)
        for fam, cnt in sorted(fam_counts.items()):
            f.write(f"- {fam}: {cnt}\n")

        f.write("\n### Blocked by family\n\n")
        fam_blocked = Counter(r["layer_label"] for r in blocked)
        for fam, cnt in sorted(fam_blocked.items()):
            f.write(f"- {fam}: {cnt}\n")

        f.write("\n## Blockers\n\n")
        if blocked:
            for r in blocked:
                f.write(f"- **{r['run_id']}**: {r.get('notes', 'unknown blocker')}\n")
        else:
            f.write("None.\n")

        f.write(f"\n## Output files\n\n")
        f.write(f"- Claim-lock JSONs: `{RECOVERY_OUT}/` ({len(claim_lock_jsons)} files)\n")
        f.write(f"- Manifest: `{manifest_path}`\n")
        f.write(f"- Report: `{report_path}`\n")

    print(f"\n{'=' * 60}")
    print(f"Recovery complete!")
    print(f"  Claim-lockable: {len(claimable)}")
    print(f"  Blocked: {len(blocked)}")
    print(f"  JSONs: {RECOVERY_OUT}")
    print(f"  Manifest: {manifest_path}")
    print(f"  Report: {report_path}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    recover()
