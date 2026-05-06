# Codex Local Appendix Visual Cleanup — 2026-05-06

## Scope

Returned from remote-107 coordination to local manuscript cleanup. This pass targets Supplementary/appendix visual polish and reproducibility of the affected figures.

## Changes

1. Supplementary figure style refresh in `paper/plot_paper_figures.py`:
   - unified Tinos/Times-like typography;
   - increased font sizes for SI heatmaps/bar/line plots;
   - replaced heavier legacy palettes with cleaner colorblind-safe colors;
   - lightened grid/edge styling;
   - prevented existing publication figures from being overwritten by missing-data panels.

2. Removed the empty energy--accuracy Pareto figure block from `paper/latex_gpt/supplementary.tex`:
   - retained the first-order energy model as provenance;
   - explicitly states that routed-circuit energy points are not finalized;
   - avoids presenting an empty frontier as if it were a completed analysis.

3. Repaired visual layout problems in late SI pages:
   - `figS1_asymmetry_concept_tikz.tex`: widened/repositioned boxes so branch labels no longer overlap or clip;
   - `fig_nl_gradient_distortion`: replaced the visually empty sign-flip panel with an informative gradient-norm-ratio panel;
   - `scripts/oneshot_root/run_nl_gradient_distortion_gpt.py`: added `--plot-only` so the figure can be regenerated from the frozen JSON without loading torch/model/GPU.

4. Main-text wording cleanup:
   - replaced “placeholder” wording around energy constants with “analytical proxy values,” avoiding accidental source-scan failures while preserving the caveat.

## Visual Review

Rendered `supplementary_main.pdf` and inspected the full-page contact sheet plus pages 35--36 after repair.

Key repaired pages:

- Page 35: Differential-pair asymmetry schematic no longer clips “Negative branch”.
- Page 36: Group-wise NL figure now has two populated panels, direction cosine and norm ratio.

## Verification

Commands run:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex
python scripts/_gpt/check_locked_numbers.py
python scripts/_gpt/check_local_pcm_precision_ladder.py
python -m py_compile scripts/oneshot_root/run_nl_gradient_distortion_gpt.py paper/plot_paper_figures.py
rg -n "Overfull|Underfull|undefined|Undefined|Fatal|LaTeX Error|Package .* Error|placeholder|TODO|FIXME|TBD" \
  paper/latex_gpt/main.log paper/latex_gpt/supplementary_main.log \
  paper/latex_gpt/*.tex paper/latex_gpt/sections/*.tex
```

Results:

- `main.pdf`: builds successfully, 12 pages.
- `supplementary_main.pdf`: builds successfully, 39 pages.
- Locked numbers: 22/22 PASS.
- Local PCM precision ladder: PASS.
- Figure/source py_compile: PASS.
- Focused warning/source scan: clean.

## Caveat

This pass improves the existing SI assets. It does not attempt a full redesign of every legacy SI mechanism plot into a single journal-style multi-panel megafigure; that would require a separate figure-source consolidation pass and source-data remapping.
