# Codex Final Acceptance Review — Paper-1 PCM Freeze

Date: 2026-05-09
Owner: Codex
Scope: combined acceptance of Kimi 6-bit drift closure, Mimo main-text rewrite, Gemini visual freeze, and Codex appendix/source-data cleanup.

## Verdict

**Accepted for the active manuscript path, with one bounded follow-up.**

The active main text, supplement, cover letter, source tables, current plotting scripts, and compiled PDFs are internally consistent with the corrected PCM interpretation:

- 8-bit PCM is the strongest drift-flat operating point.
- 6-bit PCM is drift-flat but D2D/seed-sensitive, not a Pareto midpoint.
- 4-bit PCM is trainable but drift-limited over the 24 h retention window.

The remaining issue is not the active manuscript. It is the archival/source-data packaging layer: `paper/latex_gpt/source_data/canonical_json/` still contains the old 20260501 copied 6-bit artifacts, including `pcm_6bit_seed456_full100`. That directory must be canonicalized before any release bundle is cut.

## Active Locked Numbers

| Precision | Fresh Acc. | 1 h Acc. | 24 h Acc. | 24 h Drift | Role |
|---|---:|---:|---:|---:|---|
| 8-bit PCM | 77.60% | 77.49% | 77.57% | 0.04 pp | Drift-flat reference |
| 6-bit PCM | 68.55% | 68.57% | 68.46% | 0.07 pp | D2D-sensitive transition zone |
| 4-bit PCM | 76.68% | 74.04% | 72.64% | 4.01 pp | Drift-limited regime |

6-bit provenance note: four fresh/drift seeds are used for 6-bit; seed123 lacks `training_history.json`, so source-best aggregation uses three seeds and fresh/drift aggregation uses four seeds.

## Files Changed By This Acceptance Pass

- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/cover_letter.tex`
- `paper/latex_gpt/source_data/tab_pcm_precision_ladder.csv`
- `paper/latex_gpt/source_data/fig2_paper1_decision_map.csv`
- `paper/latex_gpt/source_data/manifest_paper1_spine.json`
- `scripts/_gpt/plot_paper1_spine.py`
- `scripts/_gpt/plot_paper1_decision_map.py`
- `scripts/_gpt/generate_merged_figures.py`
- `scripts/_gpt/generate_merged_figures_v2.py`
- `scripts/_gpt/check_local_pcm_precision_ladder.py`
- regenerated figures/PDF outputs under `paper/latex_gpt/figures/`

## Verification Commands

```bash
python scripts/_gpt/plot_paper1_spine.py
python scripts/_gpt/plot_paper1_decision_map.py
python scripts/_gpt/generate_merged_figures_v2.py
python scripts/_gpt/check_local_pcm_precision_ladder.py
python -m py_compile scripts/_gpt/generate_merged_figures.py scripts/_gpt/generate_merged_figures_v2.py scripts/_gpt/plot_paper1_spine.py scripts/_gpt/plot_paper1_decision_map.py scripts/_gpt/check_local_pcm_precision_ladder.py
tectonic main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex
```

## Verification Results

- PCM precision-ladder guard: **PASS**.
- Active stale-string grep excluding archival `canonical_json`: **PASS**.
- `main.pdf`: rebuilt successfully.
- `supplementary_main.pdf`: up to date and previously rebuilt after appendix repair.
- PDF text grep for old 6-bit strings and old paths: **PASS**.
- Non-fatal main build warnings remain from `algorithm.sty` UTF-8 replacement and Tectonic's repeated `main.bbl` rerun check. PDF output is produced.

## Known Residual Risk

`paper/latex_gpt/source_data/canonical_json/` is stale as a release artifact. It contains old 6-bit copied JSON and an old manifest from 2026-05-01. It is not used by the active manuscript path after this pass, but it must be rebuilt or explicitly quarantined before release packaging.

## Decision

Proceed to the next phased task: source-data canonicalization and release guard. No more semantic edits should be made to the active manuscript unless the next audit finds a concrete inconsistency.
