# Release Audit - 2026-04-11

**Owner:** Codex  
**Scope:** Public-facing repository hygiene and submission-artifact readiness

## What was checked

### Public docs

- `README.md`
- `docs/README.md`
- `docs/DEVICE_PROFILE_GUIDE.md`
- `docs/EXPERIMENT_REGISTRY.md`
- `docs/PHYSICS_STACK.md`

### Paper build

- `paper/latex_gpt/main.tex`
- `paper/latex_gpt/main.log`

### Repository hygiene

- `LICENSE`
- `.gitignore`
- presence of transient cache directories

## Findings

### 1. License status

- `LICENSE` exists and is Apache 2.0
- `README.md` license section matches the repository license

**Status:** pass

### 2. Docs linkage

- `docs/README.md` exists
- `README.md` links readers to the `docs/` index and core guides

**Status:** pass

### 3. Public-facing path hygiene

Fixed in this round:

- removed `report_md/_gpt/` references from `README.md`
- replaced the example checkpoint path with a generic `checkpoints/path/to/...` placeholder
- `README.md` / `docs/` now contain no `/home/qiaosir/projects/...` absolute paths

**Status:** pass for public docs

### 4. LaTeX build status

- `paper/latex_gpt/main.tex` recompiles successfully
- `main.log` shows no undefined citations or undefined references

**Status:** pass

### 5. Internal coordination footprint

The repository still contains many `_gpt` coordination files and helper scripts with absolute paths, for example under:

- `report_md/_gpt/`
- `paper/latex_gpt/*_gpt.md`
- watcher / helper scripts in the repo root and `scripts/_gpt/`

These are not a problem for paper compilation, but they are **not ideal for a clean public release** unless deliberately retained as internal provenance artifacts.

**Status:** reviewer-safe, but release-curation still recommended

### 6. Transient cache directories

Removed in this round:

- `__pycache__/`
- `paper/__pycache__/`

These were harmless locally and already ignored by `.gitignore`, but they no longer need manual cleanup.

**Status:** pass

### 7. Internal-coordination files likely not suitable for public release

The following categories are currently present and should be curated before a public code drop unless there is a deliberate decision to preserve the full internal provenance trail:

- `report_md/_gpt/AGENT_SYNC_gpt.md`
- `report_md/_gpt/CLAUDE_TASK_gpt.md`
- `report_md/_gpt/CODEX_*_gpt.md`
- `report_md/_gpt/GEMINI_*_gpt.md`
- `report_md/_gpt/KIMI_*_gpt.md`
- `paper/latex_gpt/CITATION_BACKLOG_gpt.md`
- `paper/latex_gpt/CITATION_MAP_gpt.md`
- `paper/latex_gpt/CLOSEOUT_CHECKLIST_gpt.md`
- `paper/latex_gpt/README_gpt.md`
- `paper/latex_gpt/SUBMISSION_PACKET_gpt.md`
- `paper/latex_gpt/TEMPLATE_MIGRATION_GUIDE_gpt.md`

These files are useful internally, but they are not canonical end-user documentation.

**Status:** curation decision still required

## Recommended next cleanup before public release

1. Decide whether `_gpt` coordination files are meant to ship.
   - If not, curate or exclude `report_md/_gpt/` and `paper/latex_gpt/*_gpt.md`
2. Remove LaTeX build byproducts before tagging a release, even though they are already ignored.

## Overall assessment

For manuscript submission, the repository and paper sources are in good shape.

For a polished public code release, the main remaining work is **curation**, not technical repair:

- decide how much internal `_gpt` coordination history should remain public
- trim release artifacts to canonical docs, code, and reproducibility outputs
