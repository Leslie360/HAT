# Codex Visual / Appendix Cleanup — 2026-05-01

## Scope

This pass addresses the submission-readability issues raised by the user: inconsistent units and percent formatting, ambiguous empty table entries, overlong captions, unnecessary main-text equations, raster-only concept figures, and inconsistent plotting style.

## Changes Made

### Main text
- Reduced non-essential displayed equations in `sections/03_methodology.tex`:
  - Standard-HAT fixed-mask objective moved to prose.
  - Fresh-instance expectation moved to prose.
  - V6 inverse-gamma / photocurrent equations moved out of main-text emphasis; explicit equations remain in SI context.
  - Sobol equation moved to prose-level description.
- Updated `sections/06_discussion.tex` to avoid referencing the removed Standard-HAT equation label.
- Tightened Figure 1 and PCM table captions in `sections/05_results.tex`.
- Standardized the PCM table units:
  - Headers now carry `%` and `pp` units.
  - Table cells no longer repeat `%`/`pp` redundantly.

### Supplementary Information
- Added `\notrun` macro in `supplementary_main.tex`.
- Replaced ambiguous table entries (`-`, `--`, em dash in data cells) with explicit `n.e.` or numeric `0.00%` baselines.
- Added caption note that `n.e.` means not evaluated, not failed/missing.
- Renamed `Hybrid organic-CIM` caption to `Hybrid analog-CIM` to avoid stale substrate wording.
- Shortened long captions across quantitative SI figures and empirical-mechanism figures.
- Converted two PNG-only concept figures into TikZ vector source:
  - `supplementary/figS1_asymmetry_concept_tikz.tex`
  - `supplementary/figS2_nonideality_tikz.tex`

### Figures and plotting scripts
- Rebuilt `fig1_paper1_spine.{pdf,png}` with larger labels and a consistent palette.
- Updated `plot_paper1_spine.py` to preserve LF-only CSV output.
- Updated `paper/plot_paper_figures.py` defaults:
  - Larger plot fonts.
  - Less sparse Fig. S noise-sensitivity layout.
  - Accuracy heatmap colormap aligned to `YlGnBu`.
- Updated `plot_aihwkit_comparison.py` style for consistent palette/font if regenerated.

## Verification

- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` — PASS
- `latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex` — PASS
- Warning grep over `main.log` and `supplementary_main.log` — no undefined refs/citations, no overfull/underfull lines
- PDF pages:
  - `main.pdf`: 13 pages
  - `supplementary_main.pdf`: 40 pages
- Included figure scan:
  - 20 `\includegraphics` entries
  - 0 raster-only includes in the local build tree
- Empty-cell scan:
  - No remaining table cells matching bare `-`, `--`, em dash, `N/A`, or `n/a`
- Locked-number guard:
  - `python scripts/_gpt/check_locked_numbers.py` — 22/22 PASS
- Local PCM precision-ladder guard:
  - `python scripts/_gpt/check_local_pcm_precision_ladder.py` — PASS
- Python syntax:
  - `python -m py_compile scripts/_gpt/plot_paper1_spine.py scripts/_gpt/plot_aihwkit_comparison.py paper/plot_paper_figures.py` — PASS

## Residual Notes

- Most included figures have PDF vector counterparts in the local build tree. The two previous raster-only concept diagrams are now TikZ source and no longer required for SI compilation.
- Some historical PNG files remain in `figures/` for archival/backward compatibility but are not selected by the current SI for the two converted concept diagrams.
