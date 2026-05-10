# Codex Main-Figure Redesign Pass 4 — 2026-05-02

## Reason

The previous main-text figures were not acceptable visually: uneven proportions, loose alignment, text placed too close to box boundaries, cropped cards, and inconsistent visual hierarchy.

## What Changed

### Figure 1: Paper-1 Experimental Spine

Files:

- `paper/latex_gpt/figures/fig1_paper1_spine.pdf`
- `paper/latex_gpt/figures/fig1_paper1_spine.png`
- generator: `scripts/_gpt/plot_paper1_spine.py`

Changes:

- Rebuilt as a strict three-column layout: schematic, rescue data, PCM frontier.
- Removed left-side lane labels that overlapped boxes.
- Repositioned all schematic labels within safe margins.
- Reduced free-floating text and removed clutter around the 6-bit midpoint.
- Unified panel headers, colors, line weights, rounded boxes, and chart styling.
- Kept the output vector-first for publication.

### Figure 2: Results-to-Deployment Decision Map

Files:

- `paper/latex_gpt/figures/fig2_paper1_decision_map.pdf`
- `paper/latex_gpt/figures/fig2_paper1_decision_map.png`
- generator: `scripts/_gpt/plot_paper1_decision_map.py`

Changes:

- Rebuilt as a strict evidence-row plus decision-row grid.
- Fixed right-edge clipping of the 4-bit card.
- Standardized card width, row spacing, arrows, and text hierarchy.
- Kept all text within boxes and removed loose label overflow.
- Retained the same data values and claim boundaries.

## Visual QA

Rendered main PDF pages 3-4 at 180 dpi:

```bash
pdftoppm -f 3 -l 4 -png -r 180 paper/latex_gpt/main.pdf /tmp/codex_mainfig_redesign/main
```

Inspection:

- Figure 1: no text leaves boxes; no panel overlap; schematic and plots align on a single row.
- Figure 2: no clipped right card; decision boxes and arrows are aligned; text fits inside boxes.
- Main PDF now compiles to 12 pages after figure-size/layout changes.

## Verification

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
rg -n "Undefined|undefined|Reference .*undefined|Citation .*undefined|There were undefined|multiply defined|Overfull|Underfull|Warning" paper/latex_gpt/main.log || true
python scripts/_gpt/check_locked_numbers.py
python scripts/_gpt/check_local_pcm_precision_ladder.py
python -m py_compile scripts/_gpt/plot_paper1_spine.py scripts/_gpt/plot_paper1_decision_map.py
```

Results:

- Main compile: PASS
- Log critical warning scan: PASS
- Locked-number guard: 22/22 PASS
- PCM precision-ladder guard: PASS
- Figure scripts compile: PASS

## Image Prompt Status

No GPT Image prompt was used or needed for this pass. The main-text figures are data-bearing/vector figures, so reproducible Matplotlib/PDF output is more defensible than raster illustration.
