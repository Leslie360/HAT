# Codex Phase P1 Final Acceptance — Source-Data Canonicalization

Date: 2026-05-09
Owner: Codex
Phase: P1 Source-data canonicalization and release guard
Input reports: Kimi P1, DS P1 audit, Mimo P1 audit, Gemini logic-lock broadcast

## Verdict

**ACCEPTED after Codex repair. Release-safe for the active Paper-1 source-data path.**

Kimi completed the canonical JSON quarantine and both DS/Mimo audits passed. Codex independently re-ran the checks and found three small but real issues that were repaired before final acceptance:

1. Removed an accidental zero-byte `PYEOF` heredoc residue from `paper/latex_gpt/source_data/canonical_json/`.
2. Updated `paper/latex_gpt/source_data/canonical_json/README.md`, which still pointed to `manifest_canonical_json_20260501` and described 6-bit as three-seed evidence.
3. Reconciled `Delta Drift` semantics after Gemini's logic pass: the active manuscript now defines `Delta Drift` as retention-eval 0s to 24h/1d drop, matching `tab_pcm_precision_ladder.csv` and `check_local_pcm_precision_ladder.py`.

## Accepted Active Canonical State

- Active canonical manifest: `paper/latex_gpt/source_data/canonical_json/manifest_canonical_json_20260509.json`
- Manifest item count: 46
- Missing files: 0
- SHA-256 mismatches: 0
- Unexpected active files: 0
- Deprecated old protocol: `paper/latex_gpt/source_data/canonical_json/deprecated_20260501_old_protocol/`
- Active old 6-bit `seed456_full100` references: 0

## Locked PCM Ladder Numbers

| Precision | Fresh Acc. | 1 h Acc. | 24 h Acc. | Delta Drift | Role |
|---|---:|---:|---:|---:|---|
| 8-bit PCM | 77.60% | 77.49% | 77.57% | 0.04 pp | Drift-flat reference |
| 6-bit PCM | 68.55% | 68.57% | 68.46% | 0.07 pp | D2D-sensitive transition zone |
| 4-bit PCM | 76.68% | 74.04% | 72.64% | 4.01 pp | Drift-limited regime |

Definition: `Delta Drift` is retention-eval 0s accuracy minus retention-eval 24h/1d accuracy. It is not computed from the separate fresh-eval mean.

## Verification Performed By Codex

```bash
python scripts/_gpt/check_local_pcm_precision_ladder.py
rg -n "77\.86|77\.88|77\.83|77\.76|78\.49|Pareto midpoint|best observed Pareto|critical Pareto|6-bit midpoint|seed456_full100|r11d_6bit_pcm_seed456_full100" \
  paper/latex_gpt/sections paper/latex_gpt/supplementary.tex paper/latex_gpt/supplementary/*.tex paper/latex_gpt/cover_letter.tex paper/latex_gpt/source_data scripts/_gpt \
  --glob '!paper/latex_gpt/source_data/canonical_json/deprecated_20260501_old_protocol/**'
tectonic main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex
pdftotext main.pdf - | rg -n "77\.86|75\.43|72\.67|seed456_full100|6-bit midpoint|Pareto midpoint|pending|78\.49" || true
pdftotext supplementary_main.pdf - | rg -n "77\.86|75\.43|72\.67|seed456_full100|6-bit midpoint|Pareto midpoint|6-bit.*pending|pending.*6-bit|78\.49" || true
```

Results:

- Precision-ladder guard: PASS.
- Active stale grep: zero hits.
- Manifest/hash check: 46 items, 0 missing, 0 mismatches, 0 unexpected active files.
- `main.pdf`: rebuilt successfully, no overfull table warning after the Delta header repair.
- `supplementary_main.pdf`: rebuilt successfully, 39 pages.
- PDF text stale scans: zero hits.

Known non-blocking warnings:

- `algorithm.sty` UTF-8 replacement warning in `tectonic main.tex`.
- Tectonic repeated `main.bbl` rerun consistency warning.
- One underfull hbox in supplementary around the retention-decay paragraph.

## Notes On Auditor Reports

Kimi's report stated that README/manifest files were included in the 46 active items. The actual manifest contains 46 data artifacts; README and manifest files are active package metadata but not manifest entries. This is acceptable and clearer than self-including the manifest.

Mimo/Gemini's internal-consistency point about `Fresh Acc. - 24h Acc.` was valid as a table-reading concern, but the source-data field is explicitly a retention-eval drift metric. Codex resolved this by clarifying the caption/header and restoring the source-data/guard values.

## Final Decision

Phase P1 is closed. The next phase should not alter scientific semantics. Proceed to P2: release-candidate bundle assembly and clean-room validation.
