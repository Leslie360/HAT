#!/usr/bin/env python3
"""Check that all LaTeX citation keys exist in refs_gpt.bib."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PAPER = ROOT / "paper" / "latex_gpt"
OUT = PAPER / "source_data" / "manifest_bib_key_audit_20260501.json"

tex_files = [PAPER / "main.tex", PAPER / "supplementary_main.tex", PAPER / "supplementary.tex"]
tex_files += sorted((PAPER / "sections").glob("*.tex"))
tex_files += sorted((PAPER / "supplementary").glob("*.tex"))

cite_re = re.compile(r"\\cite(?:alp|alt|author|p|t|year|yearpar)?\*?(?:\[[^\]]*\])*\{([^}]+)\}")
bib_re = re.compile(r"@\w+\s*\{\s*([^,]+)")

used: dict[str, list[str]] = {}
for tex in tex_files:
    if not tex.exists():
        continue
    text = tex.read_text(encoding="utf-8", errors="ignore")
    for match in cite_re.finditer(text):
        for key in match.group(1).split(","):
            key = key.strip()
            if key:
                used.setdefault(key, []).append(str(tex.relative_to(ROOT)))

bib_text = (PAPER / "refs_gpt.bib").read_text(encoding="utf-8", errors="ignore")
bib_keys = set(bib_re.findall(bib_text))
used_keys = set(used)
missing = sorted(used_keys - bib_keys)
unused = sorted(bib_keys - used_keys)

summary = {
    "generated_by": str(Path(__file__).relative_to(ROOT)),
    "bib_file": "paper/latex_gpt/refs_gpt.bib",
    "used_key_count": len(used_keys),
    "bib_key_count": len(bib_keys),
    "missing_key_count": len(missing),
    "unused_key_count": len(unused),
    "missing_keys": missing,
    "unused_keys": unused,
    "used_locations": used,
    "scope_note": "This is a local consistency audit. It verifies citation-key coverage, not external DOI authenticity.",
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(json.dumps({k: summary[k] for k in ["used_key_count", "bib_key_count", "missing_key_count", "unused_key_count"]}, indent=2))
if missing:
    raise SystemExit(1)
