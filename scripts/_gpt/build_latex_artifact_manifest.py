#!/usr/bin/env python3
"""Build a reproducibility inventory for LaTeX figures and source-data files."""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper" / "latex_gpt"
FIG_DIR = PAPER / "figures"
SRC_DIR = PAPER / "source_data"
OUT_JSON = SRC_DIR / "manifest_all_figures_20260501.json"
OUT_CSV = SRC_DIR / "manifest_all_figures_20260501.csv"

TEX_FILES = [PAPER / "main.tex", PAPER / "supplementary_main.tex", PAPER / "supplementary.tex"]
TEX_FILES += sorted((PAPER / "sections").glob("*.tex"))
TEX_FILES += sorted((PAPER / "supplementary").glob("*.tex"))

include_re = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
input_fig_re = re.compile(r"\\input\{(supplementary/fig[^}]+)\}")


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def candidate_figure_files(name: str) -> list[Path]:
    raw = Path(name)
    candidates: list[Path] = []
    if raw.suffix:
        candidates.append(FIG_DIR / raw)
    else:
        for suffix in (".pdf", ".png", ".jpg", ".jpeg"):
            candidates.append(FIG_DIR / f"{name}{suffix}")
    return [p for p in candidates if p.exists()]


def source_data_candidates(name: str) -> list[Path]:
    stem = Path(name).stem
    candidates = []
    for path in SRC_DIR.glob("*"):
        if path.is_file() and (stem in path.name or path.stem in stem):
            candidates.append(path)
    # Fig. 1 also owns the PCM table source data.
    if stem == "fig1_paper1_spine":
        extra = SRC_DIR / "tab_pcm_precision_ladder.csv"
        if extra.exists():
            candidates.append(extra)
    return sorted(set(candidates))


def generator_candidates(name: str) -> list[Path]:
    stem = Path(name).stem
    search_roots = [ROOT / "scripts", ROOT / "paper" / "latex_gpt" / "figures" / "tikz"]
    hits: list[Path] = []
    for root in search_roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.suffix not in {".py", ".sh", ".tex", ".md"}:
                continue
            try:
                text = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if stem in text or name in text:
                hits.append(path)
    return sorted(set(hits))


records = []
seen = set()
for tex in TEX_FILES:
    if not tex.exists():
        continue
    text = tex.read_text(encoding="utf-8", errors="ignore")
    for match in include_re.finditer(text):
        name = match.group(1)
        key = (rel(tex), name, match.start())
        if key in seen:
            continue
        seen.add(key)
        fig_files = candidate_figure_files(name)
        src_files = source_data_candidates(name)
        gen_files = generator_candidates(name)
        records.append(
            {
                "latex_file": rel(tex),
                "artifact": name,
                "kind": "includegraphics",
                "figure_files": [rel(p) for p in fig_files],
                "source_data_files": [rel(p) for p in src_files],
                "generator_candidates": [rel(p) for p in gen_files],
                "status": "source_data_linked" if src_files else ("figure_file_only" if fig_files else "missing_figure_file"),
            }
        )
    for match in input_fig_re.finditer(text):
        name = match.group(1)
        path = PAPER / f"{name}.tex"
        src_files = source_data_candidates(Path(name).stem)
        gen_files = generator_candidates(Path(name).stem)
        records.append(
            {
                "latex_file": rel(tex),
                "artifact": name,
                "kind": "input_tikz",
                "figure_files": [rel(path)] if path.exists() else [],
                "source_data_files": [rel(p) for p in src_files],
                "generator_candidates": [rel(p) for p in gen_files],
                "status": "source_data_linked" if src_files else ("figure_file_only" if path.exists() else "missing_figure_file"),
            }
        )

summary = {
    "generated_by": rel(Path(__file__)),
    "record_count": len(records),
    "status_counts": {},
    "records": records,
}
for rec in records:
    summary["status_counts"][rec["status"]] = summary["status_counts"].get(rec["status"], 0) + 1

SRC_DIR.mkdir(parents=True, exist_ok=True)
OUT_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")
with OUT_CSV.open("w", newline="", encoding="utf-8") as handle:
    fieldnames = ["latex_file", "artifact", "kind", "status", "figure_files", "source_data_files", "generator_candidates"]
    writer = csv.DictWriter(handle, fieldnames=fieldnames)
    writer.writeheader()
    for rec in records:
        row = dict(rec)
        for key in ("figure_files", "source_data_files", "generator_candidates"):
            row[key] = ";".join(row[key])
        writer.writerow(row)

print(json.dumps({"output_json": rel(OUT_JSON), "output_csv": rel(OUT_CSV), "summary": summary["status_counts"]}, indent=2))
