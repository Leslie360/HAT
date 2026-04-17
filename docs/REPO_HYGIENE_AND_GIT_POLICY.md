# Repo Hygiene and Git Policy

This file defines the practical version-control boundary for `compute_vit`.

## Track in Git

- source code (`*.py`)
- tests
- paper source (`paper/latex_gpt/**/*.tex`, curated figures, bibliography)
- curated markdown docs that explain decisions, methods, and submission state
- machine-readable result artifacts that are explicitly referenced by manuscript or planning docs
- small configuration files and reproducibility manifests

## Do Not Track in Git

- Python cache files:
  - `__pycache__/`
  - `*.pyc`
- local datasets and downloads:
  - `data/imagenet/`
  - `data/tiny-imagenet-200/`
- transient logs:
  - `logs/`
- heavy training checkpoints:
  - `checkpoints/`
- LaTeX build byproducts:
  - `*.aux`, `*.bbl`, `*.blg`, `*.fdb_latexmk`, `*.fls`, `*.log`, `*.out`, `*.synctex.gz`
- local scratch / archive directories:
  - `tmp/`
  - `internal/`

## PDF Policy

- Keep source-first discipline.
- Final PDFs may exist locally for review, but the source `.tex` and figure assets are the canonical tracked artifacts.
- If a PDF must be tracked for a release or handoff, do it intentionally in a dedicated commit.

## Result Artifact Policy

- A JSON/CSV/MD artifact should be tracked only if at least one of the following is true:
  1. it is cited or summarized in the manuscript,
  2. it is needed to justify a major strategic decision,
  3. it is a compact reproducibility artifact that would be expensive to regenerate.

- Otherwise, leave it out of Git or archive it outside the core repository.

## Git Workflow

- Keep generated clutter out of commits.
- Prefer small thematic commits:
  - manuscript wording
  - figures
  - experiment artifacts
  - repo hygiene
- Before committing, check:
  - `git status --short`
  - no accidental caches or build files
  - no large local datasets
  - no stale logs unless intentionally curated

## Current Hygiene Priority

The current repository still contains historical tracked generated files from earlier phases.
The immediate cleanup target is:

1. remove tracked `__pycache__/` entries from the Git index,
2. remove tracked LaTeX build byproducts from the Git index,
3. keep paper sources and curated result artifacts intact.
