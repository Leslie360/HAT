# Codex Main-Figure Visual Repair — 2026-05-03

## Scope

User feedback targeted main-text figure readability, especially Fig. 2 typography and figure size. Gemini also raised a visual-review note about Fig. 1C using a twin-y-axis bar/line design.

## Decisions

1. Fig. 2 should be enlarged rather than merely retouched locally.
2. Main-text figures keep Tinos / Times-compatible typography because the manuscript body is Times-like and the user explicitly requested Times-style readability.
3. Gemini's twin-axis criticism is accepted for Fig. 1C; the panel now uses a single-coordinate precision-retention Pareto view.
4. Auxiliary linework and palette were lightened; primary numeric claims remain bold and large.

## Changes Applied

### Fig. 2: results-to-deployment decision map

- Increased LaTeX insertion from `\textwidth` to centered `1.16\textwidth`.
- Increased figure canvas from `8.6 x 3.55` to `9.4 x 5.10` inches.
- Increased global figure font size to 12 pt.
- Enlarged panel headers, card titles, headline percentages, drift values, decision-step labels, and footer text.
- Switched main palette to a lighter colorblind-safe set: blue / orange-red / green / gold with soft fills.
- Regenerated vector PDF and PNG.

### Fig. 1: experimental spine

- Removed the twin-y-axis PCM precision/retention panel.
- Replaced Fig. 1C with a single-axis Pareto-style scatter/line plot:
  - x-axis: 1-day drift drop (pp, log scale)
  - y-axis: fresh accuracy (%)
  - 8-bit, 6-bit, and 4-bit are connected as a precision-retention frontier.
  - 6-bit is annotated as the midpoint.
- Removed heavy capped error bars from the main visual; uncertainty remains in canonical tables and source data.
- Increased main figure typography and panel-title weight.
- Lightened color palette and bar outlines.

## Validation

- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`: PASS
- LaTeX log scan for undefined references/citations and overfull/underfull boxes: PASS
- `python -m py_compile scripts/_gpt/plot_paper1_spine.py scripts/_gpt/plot_paper1_decision_map.py`: PASS
- `python scripts/_gpt/check_locked_numbers.py`: PASS, 22/22 locked numbers
- `python scripts/_gpt/check_local_pcm_precision_ladder.py`: PASS
- Fig. 1/Fig. 2 PDF fonts: Tinos/Tinos-Bold embedded; STIX appears only for math labels in Fig. 1.

## Files Updated

- `scripts/_gpt/plot_paper1_spine.py`
- `scripts/_gpt/plot_paper1_decision_map.py`
- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/figures/fig1_paper1_spine.pdf`
- `paper/latex_gpt/figures/fig1_paper1_spine.png`
- `paper/latex_gpt/figures/fig2_paper1_decision_map.pdf`
- `paper/latex_gpt/figures/fig2_paper1_decision_map.png`
- `paper/latex_gpt/main.pdf`
