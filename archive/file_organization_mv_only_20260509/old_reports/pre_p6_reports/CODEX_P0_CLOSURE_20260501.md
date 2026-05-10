# Codex P0 Closure — 2026-05-01

## Verdict
The requested P0 closure tasks are complete for the current Paper-1 draft state.

Current architecture decision remains unchanged:

- No mandatory local GPU experiment remains for Paper-1.
- Current local locked spine is sufficient for manuscript shaping: IdealDevice 8-bit stability, pure 4-bit collapse, Ensemble HAT 4-bit rescue, PCM 4/6/8 precision-retention frontier.
- Remaining work is editorial/package hygiene, not new data generation.

## Completed Tasks

### 1. Full LaTeX figure/source-data inventory
Added and ran:

- `scripts/_gpt/build_latex_artifact_manifest.py`

Generated:

- `paper/latex_gpt/source_data/manifest_all_figures_20260501.json`
- `paper/latex_gpt/source_data/manifest_all_figures_20260501.csv`

Result:

- 23 LaTeX figure artifacts detected.
- 1 figure has explicit source-data linkage: main Fig. 1.
- 22 legacy/SI figures are marked `figure_file_only`, with generator candidates recorded where detectable.

Interpretation:

- The inventory is now complete and machine-readable.
- The final journal source-data package is not falsely overclaimed: legacy SI figures are explicitly marked as figure-only unless source CSVs are later reconstructed.

### 2. Main-text hostile claim audit and softening
Patched over-strong or overly causal language in:

- `paper/latex_gpt/sections/00_abstract.tex`
- `paper/latex_gpt/sections/01_introduction.tex`
- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/sections/06_discussion.tex`
- `paper/latex_gpt/sections/07_conclusion.tex`

Key changes:

- `demonstrate` -> `show` where appropriate.
- `best tested` -> `best observed ... in this sweep`.
- `solves` -> `addresses`.
- `primary failure mode` -> `leading tested failure mode`.
- Removed broad method-superiority wording and replaced it with regime-specific advantage language.

### 3. Bibliography consistency audit
Added and ran:

- `scripts/_gpt/audit_latex_bib_keys.py`

Generated:

- `paper/latex_gpt/source_data/manifest_bib_key_audit_20260501.json`

Result:

- 43 citation keys used in LaTeX.
- 67 bib entries exist.
- 0 missing citation keys.
- 24 unused bib entries retained but harmless.

### 4. DOI/URL network resolution audit
Added and ran:

- `scripts/_gpt/audit_bib_doi_resolution.py`

Generated:

- `paper/latex_gpt/source_data/manifest_bib_doi_resolution_20260501.json`

Result:

- 67/67 bib entries have either DOI redirect or URL resolution.
- 53 entries return DOI resolver redirects.
- 14 entries resolve directly as URL/endpoint entries.
- Added missing arXiv URL for `mia2026trilinear`.

Scope note:

- This verifies endpoint existence, not a full semantic bibliography review of every title/author/page field.

### 5. Compile and guard verification
Commands rerun:

```bash
python scripts/_gpt/check_locked_numbers.py
python scripts/_gpt/check_local_pcm_precision_ladder.py
python scripts/_gpt/build_latex_artifact_manifest.py
python scripts/_gpt/audit_latex_bib_keys.py
python scripts/_gpt/audit_bib_doi_resolution.py
python -m py_compile scripts/_gpt/build_latex_artifact_manifest.py scripts/_gpt/audit_latex_bib_keys.py scripts/_gpt/audit_bib_doi_resolution.py scripts/_gpt/plot_paper1_spine.py scripts/_gpt/check_local_pcm_precision_ladder.py
cd paper/latex_gpt && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cd paper/latex_gpt && latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex
```

Results:

- Locked numbers: 22/22 PASS.
- Local PCM ladder: PASS.
- Main PDF compiles.
- Supplementary PDF compiles.
- Final LaTeX/source scan clean: no undefined refs/citations, fatal errors, Overfull boxes, placeholders, TODO/FIXME/TBD.

## Remaining Non-P0 Items

These are not blockers for the current architecture decision:

1. Reconstruct per-figure CSV source data for legacy SI figures if the target venue requires it.
2. Harmonize SI figure visual style.
3. External semantic bibliography review for every non-core reference field.
4. Optional GPU validation: PCMPresetDevice 3-seed, 105 cross-arch, 107 KV-cache Work-2.
