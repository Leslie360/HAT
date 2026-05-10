# ⚠️ WARNING: BASELINE = 27.72 is BUG-CONTAMINATED — pre-fix NL=2.0 result invalid after commit 33bed9c.
# Do not use this script for post-fix ablation finalization.
# See report_md/_gpt/BROADCAST_REBUILD_3WEEK_20260424.md

#!/usr/bin/env python3
"""Auto-finalize NL ablation artifacts when the attn_proj lane finishes.

Usage:
    python scripts/_gpt/auto_finalize_nl_ablation.py
    python scripts/_gpt/auto_finalize_nl_ablation.py --dry-run
    python scripts/_gpt/auto_finalize_nl_ablation.py --dry-run --attn-proj-json /tmp/attn.json

This script:
1. Reads the four NL mitigation result JSONs.
2. Updates `SUPP_TABLE_NL_ABLATION_SCAFFOLD.md` row (e).
3. Updates `NL_LANE_RESULTS_20260418.md` source-domain row for `attn_proj-only`.
4. Updates `CLAUDE_A_DECISION_FINAL_20260418.md` summary row and checklist.
5. Prints a concise broadcast snippet for `AGENT_SYNC_gpt.md`.

It supports a `--dry-run` mode so the finalize path can be validated before the
real GPU lane completes.
"""

from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path
from typing import Dict, List

REPO_ROOT = Path(__file__).resolve().parents[2]
BASELINE = 27.72

NL_LANE_RESULTS_PATH = REPO_ROOT / "report_md" / "_gpt" / "NL_LANE_RESULTS_20260418.md"
SUPP_TABLE_PATH = REPO_ROOT / "report_md" / "_gpt" / "SUPP_TABLE_NL_ABLATION_SCAFFOLD.md"
CLAUDE_FINAL_PATH = REPO_ROOT / "report_md" / "_gpt" / "CLAUDE_A_DECISION_FINAL_20260418.md"


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data[0] if isinstance(data, list) else data


def replace_or_fail(text: str, pattern: str, repl: str, desc: str) -> str:
    new_text, count = re.subn(pattern, repl, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise RuntimeError(f"Failed to update {desc}: pattern not found")
    return new_text


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def preview_diff(old: str, new: str, path: Path) -> str:
    diff = difflib.unified_diff(
        old.splitlines(),
        new.splitlines(),
        fromfile=f"{path.name}:before",
        tofile=f"{path.name}:after",
        lineterm="",
    )
    lines = list(diff)
    if not lines:
        return f"# {path.name}\n(no changes)\n"
    return f"# {path.name}\n" + "\n".join(lines[:120]) + ("\n...\n" if len(lines) > 120 else "\n")


def expected_paths(attn_proj_json_override: Path | None) -> Dict[str, Path]:
    return {
        "MLP-only": REPO_ROOT / "report_md" / "_gpt" / "json_gpt" / "v4_nl2_mlp_linear_comp_train_results_gpt.json",
        "QKV-only": REPO_ROOT / "report_md" / "_gpt" / "json_gpt" / "v4_nl2_qkv_linear_comp_train_results_gpt.json",
        "all-linear": REPO_ROOT / "report_md" / "_gpt" / "json_gpt" / "v4_nl2_all_linear_comp_train_results_gpt.json",
        "attn_proj-only": attn_proj_json_override or (REPO_ROOT / "report_md" / "_gpt" / "json_gpt" / "v4_nl2_attn_proj_linear_comp_train_results_gpt.json"),
    }


def load_results(attn_proj_json_override: Path | None) -> tuple[Dict[str, dict], List[str]]:
    results: Dict[str, dict] = {}
    missing: List[str] = []
    for name, path in expected_paths(attn_proj_json_override).items():
        if path.exists():
            data = load_json(path)
            results[name] = {
                "best_test_acc": float(data.get("best_test_acc")),
                "best_epoch": int(data.get("best_epoch")),
                "final_test_acc": float(data.get("final_test_acc")),
                "path": str(path),
            }
        else:
            missing.append(name)
    return results, missing


def update_supp_table(text: str, attn_best: float, attn_epoch: int) -> str:
    delta = attn_best - BASELINE
    note = "Supports MLP-dominance" if attn_best < 40 else "Comparable recovery outside MLP"
    row = (
        f"| (e) attn_proj-only linear | attn.proj | 2.0 | **{attn_best:.2f}%** | "
        f"**{delta:+.2f} pp** | {attn_epoch} | ✅ Complete ({note}) |"
    )
    text = replace_or_fail(
        text,
        r"^\| \(e\) attn_proj-only linear \| .*?$",
        row,
        "SUPP row (e)",
    )
    text = text.replace(
        "**Status:** SCAFFOLD — numbers update as all-linear and attn_proj finish.",
        "**Status:** UPDATED — rows (a)–(f) now all have finalized source-domain values.",
    )
    text = text.replace(
        "2. **When attn_proj finishes:** paste final acc + epoch into row (e).",
        f"2. **attn_proj finalized:** row (e) locked at {attn_best:.2f}% @ epoch {attn_epoch}.",
    )
    return text


def update_lane_results(text: str, attn_best: float, attn_epoch: int, attn_final: float) -> str:
    row = (
        "| attn_proj-only linear compensation | complete | "
        f"{attn_best:.2f} | {attn_epoch} | {attn_final:.2f} | "
        "`checkpoints/_gpt/nl_mitigation/v4_nl2_attn_proj_linear_comp/V4_hybrid_standard_noise_hat_nl2_attn_proj_linear_comp_best.pt` | "
        "`logs/_gpt/train_tinyvit_v4_nl2_attn_proj_linear_comp_20260418_1700.log` | "
        "Control on the output projection path. Use this lane to test whether recovery extends beyond the MLP channel-mixing path. |"
    )
    all_linear_pattern = re.compile(r"^\| All-linear compensation \| .*?$", re.MULTILINE)
    match = all_linear_pattern.search(text)
    if not match:
        raise RuntimeError("Failed to locate all-linear row in NL lane results")
    if "| attn_proj-only linear compensation |" in text:
        text = replace_or_fail(
            text,
            r"^\| attn_proj-only linear compensation \| .*?$",
            row,
            "NL lane attn_proj row",
        )
    else:
        insert_at = match.end()
        text = text[:insert_at] + "\n" + row + text[insert_at:]
    # Add mechanistic bullet if not present.
    bullet = f"- `attn_proj-only` reaches `{attn_best:.2f}%` (final `{attn_final:.2f}%`), which "
    if bullet not in text:
        marker = "- `All-linear` reaches `87.49%`, essentially matching `MLP-only` rather than\n  materially exceeding it."
        interpretation = (
            marker + "\n"
            f"- `attn_proj-only` reaches `{attn_best:.2f}%` (final `{attn_final:.2f}%`), which "
            + ("does not challenge the current MLP-dominance reading." if attn_best < 40 else "would weaken the current MLP-localized interpretation.")
        )
        if marker in text:
            text = text.replace(marker, interpretation)
    return text


def update_claude_final(text: str, attn_best: float, attn_epoch: int) -> str:
    delta = attn_best - BASELINE
    text = replace_or_fail(
        text,
        r"^\| attn_proj-only \| TBD \| TBD \| TBD \| 🔄 Running \|$",
        f"| attn_proj-only | **{attn_best:.2f}%** | **{delta:+.2f} pp** | {attn_epoch} | ✅ Complete |",
        "CLAUDE-A final summary row",
    )
    text = text.replace(
        "- [ ] Table SX.N — row (e) pending attn_proj-only completion",
        f"- [x] Table SX.N — row (e) updated with {attn_best:.2f}%",
    )
    if "5. **attn_proj-only" not in text:
        insertion_point = "4. **No narrative rewrite needed.**  \n   The main-paper contribution count stays at 4. NL mitigation is cited as a supplementary ablation with the sentence:\n   > \"Group-wise ablation (Supplementary Table SX.N) shows that the MLP channel-mixing path is the dominant recoverable failure site under the present NL=2.0 surrogate.\""
        extra = insertion_point + "\n\n5. **attn_proj-only result does not change the placement decision.**  \n   The output-projection control is informative for the supplementary lane table, but the locked placement remains Option B unless it materially overturns the current MLP-dominance readout."
        text = text.replace(insertion_point, extra)
    return text


def apply_updates(results: Dict[str, dict]) -> Dict[Path, str]:
    attn = results["attn_proj-only"]
    out: Dict[Path, str] = {}
    out[SUPP_TABLE_PATH] = update_supp_table(read_text(SUPP_TABLE_PATH), attn["best_test_acc"], attn["best_epoch"])
    out[NL_LANE_RESULTS_PATH] = update_lane_results(read_text(NL_LANE_RESULTS_PATH), attn["best_test_acc"], attn["best_epoch"], attn["final_test_acc"])
    out[CLAUDE_FINAL_PATH] = update_claude_final(read_text(CLAUDE_FINAL_PATH), attn["best_test_acc"], attn["best_epoch"])
    return out


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--attn-proj-json", type=Path, default=None)
    p.add_argument("--diff-out", type=Path, default=None)
    return p.parse_args()


def main() -> int:
    args = parse_args()
    results, missing = load_results(args.attn_proj_json)

    print("=" * 60)
    print("NL Ablation Auto-Finalize")
    print("=" * 60)
    for name in ["MLP-only", "QKV-only", "all-linear", "attn_proj-only"]:
        if name in results:
            d = results[name]
            print(f"✅ {name}: best={d['best_test_acc']:.2f}%, epoch={d['best_epoch']}, final={d['final_test_acc']:.2f}%")
        else:
            print(f"⏳ {name}: missing")
    if missing:
        print("\nWaiting for:", ", ".join(missing))
        return 0

    updates = apply_updates(results)
    diffs = []
    for path, new_text in updates.items():
        old_text = read_text(path)
        diffs.append(preview_diff(old_text, new_text, path))
        if not args.dry_run:
            write_text(path, new_text)

    if args.diff_out:
        args.diff_out.parent.mkdir(parents=True, exist_ok=True)
        args.diff_out.write_text("\n\n".join(diffs), encoding="utf-8")

    attn = results["attn_proj-only"]
    print("\n" + "=" * 60)
    print("Decision / Broadcast")
    print("=" * 60)
    print(f"attn_proj-only: {attn['best_test_acc']:.2f}% @ ep{attn['best_epoch']} (final {attn['final_test_acc']:.2f}%)")
    print("Expected file updates:")
    for pth in updates:
        print(f"- {pth.relative_to(REPO_ROOT)}")
    print("\nSuggested AGENT_SYNC snippet:")
    print(
        f"- attn_proj-only finalized at {attn['best_test_acc']:.2f}% @ ep{attn['best_epoch']} (final {attn['final_test_acc']:.2f}%).\n"
        "- auto_finalize_nl_ablation.py updated: SUPP row (e), NL lane table, and CLAUDE-A FINAL summary.\n"
        "- Option B remains locked unless Claude explicitly overrides on editorial grounds."
    )
    if args.dry_run:
        print("\nDRY-RUN only; no files were modified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
