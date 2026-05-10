# Codex Preflight — 2026-04-20

## Result

- Status: PASS with metadata placeholders pending
- Bundle: `outputs/submission_bundle_20260419/`
- Scope: post-Round-L preflight after correlated-D2D figure integration and Zenodo archive preparation

## PDF integrity

- `main.pdf`: 17 pages
- `supplementary_main.pdf`: 23 pages
- `cover_letter.pdf`: 2 pages
- PDFs open successfully via `pypdf` in the LLM environment.

## Source-data bundle

- `source_data_v1.zip` extracts cleanly: True
- Extracted file count: 77
- `README.md` and `MANIFEST.md` are present inside the ZIP.

## Bundle path references

- `manuscript/main.pdf`: OK
- `manuscript/main.tex`: OK
- `manuscript/refs_gpt.bib`: OK
- `supplementary/supplementary_main.pdf`: OK
- `supplementary/supplementary.tex`: OK
- `cover_letter/cover_letter.pdf`: OK
- `source_data/source_data_v1.zip`: OK

## Log sanity

- `main.log` warnings: none
- `supplementary_main.log` warnings: none

## Correlated-D2D integration

- `figS_corr_d2d` present in supplementary source and bundle figures: True
- Final correlated-D2D numbers are folded into `supplementary.tex` and `06_discussion.tex`.

## Outstanding non-package issue

- README placeholders still present: ['TBD']
- These are user-owned metadata fields and do not indicate a packaging failure.
