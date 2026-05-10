# Codex Bibliography Re-Audit Fix After Hume Review

Date: 2026-04-26
Owner: Codex
Trigger: Hume independent reference audit found real metadata errors that survived the first connectivity-based validation.

## Executive Verdict

Hume's critique was correct. The first `refs_gpt_validation_20260425.json` was too weak: it verified connectivity but missed URL-only records that had since acquired DOI metadata, and it did not flag year/volume/article mismatches. Codex repaired the active BibTeX and produced a v2 validation file.

Current status:

- Active BibTeX: `paper/latex_gpt/refs_gpt.bib`
- Validation: `report_md/_gpt/refs_gpt_validation_v2_20260426.json`
- Entries: 67
- Cited keys: 45
- Missing citation keys: 0
- v2 hard metadata flags: 0
- `main.tex`: latexmk RC 0, 16 pages
- `supplementary_main.tex`: latexmk RC 0, 36 pages

## Corrections Applied

| Key | Problem Found | Fix Applied | Verification Source |
|---|---|---|---|
| `qiu2025m3dattention` | Prior report said DOI unavailable; author list used `and others` | Added full author list, pages `1--4`, DOI `10.1109/IEDM50572.2025.11353844` | https://doi.org/10.1109/IEDM50572.2025.11353844 |
| `ando2025transfer` | Prior entry used only IBM URL despite IEEE DOI existing | Added pages `1--4`, DOI `10.1109/IEDM50572.2025.11353900` | https://doi.org/10.1109/IEDM50572.2025.11353900 |
| `vincze2025dualplasticity` | Year/volume/pages mismatched Crossref print metadata | Changed to `year=2026`, `volume=12`, `number=1`, `pages=e00515`; kept note for online 2025 publication | https://doi.org/10.1002/aelm.202500515 |
| `zhang2025opect` | Title and year did not match Nature Communications record | Corrected title to include `wafer-scale`; changed formal citation year to 2026 with online-2025 note | https://doi.org/10.1038/s41467-025-66891-6 |
| `yoshioka2025jssc` | DOI typo `10.1109/JSSC.2024.3491234` did not resolve | Corrected to `10.1109/JSSC.2024.3457898` | https://doi.org/10.1109/JSSC.2024.3457898 |

Also updated:

- `report_md/_gpt/CODEX_PARALLEL_LLM_AND_BIB_AUDIT_20260425.md` to supersede the incorrect `qiu2025m3dattention` DOI-not-public statement.
- `report_md/_gpt/KIMI_R10F_LITERATURE_FRESHNESS_AUDIT_20260425.md` to fix the Yoshioka JSSC DOI snippet.

## Validation Notes

v2 validation checks:

1. BibTeX entry parsing.
2. Citation key coverage across active LaTeX files.
3. Crossref DOI resolution for DOI-bearing entries.
4. DOI-title similarity check for wrong-DOI detection.
5. arXiv existence check for eprint entries.
6. Explicit metadata spot checks for the Hume-flagged records.

v2 output excerpt:

```text
entries 67
cited_keys 45
missing []
bad 0
qiu2025m3dattention 10.1109/IEDM50572.2025.11353844 ok pages 1-4
ando2025transfer 10.1109/IEDM50572.2025.11353900 ok pages 1-4
vincze2025dualplasticity 10.1002/aelm.202500515 ok volume 12 article e00515
zhang2025opect 10.1038/s41467-025-66891-6 ok volume 17 article 197
yoshioka2025jssc 10.1109/JSSC.2024.3457898 ok volume 60 pages 1844-1855
```

## Compile Verification

Commands run:

```bash
cd /home/qiaosir/projects/compute_vit/paper/latex_gpt
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex
```

Results:

- `main.pdf`: RC 0, 16 pages.
- `supplementary_main.pdf`: RC 0, 36 pages.
- No undefined citations or hard LaTeX errors found.

## Boundary

The first validation report should now be treated as superseded for authenticity claims. It remains a historical connectivity audit only. The current active reference state is the repaired BibTeX plus `refs_gpt_validation_v2_20260426.json`.
