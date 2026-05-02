# Codex Visual Redesign Pass 2 — 2026-05-02

## Scope

This pass responds to the appendix/figure readability audit: reduce figure-body text, remove overlaps, standardize the main visual style, and move explanatory load into captions or supplementary text.

## Changes Made

1. Main Figure 1 rebuilt as a journal-style composite figure:
   - Panel A: mechanism schematic for fixed-mask vs resampled-mask HAT.
   - Panel B: 8-bit baseline / 4-bit collapse / 4-bit Ensemble HAT rescue.
   - Panel C: PCM 8/6/4-bit fresh accuracy with one-day drift overlay.
   - Removed dense in-plot explanations; caption carries the interpretation.

2. Supplementary Figure S2 rebuilt and placed correctly:
   - Replaced the crowded device/crossbar/network table with a clean A/B/C schematic.
   - Removed overlapping footnote text inside the figure.
   - Added float barriers so the section heading appears before the figure.

3. Results text cleaned:
   - Deleted malformed `Sensitivity Analysis and Operating Envelope` paragraph from main Results.
   - Updated Figure 1 caption to match the new A/B/C layout.
   - Kept extended math in Supplementary Information, not the main text.

4. Supplementary math consistency:
   - Added the Ensemble HAT objective before the fresh-instance evaluation equation to avoid a dangling `theta_ens` definition.

## Visual QA

Rendered and inspected:

- Main PDF page 3: Figure 1 no longer has overlapping labels; mechanism and data panels are visually separated.
- Supplementary PDF page 2: Figure S2 no longer overlaps text, no longer appears before its section heading, and no longer has a panel-bottom strikethrough.

## Verification

- `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`: PASS
- `latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex`: PASS
- LaTeX log grep for undefined refs/cites and overfull/underfull warnings: clean
- `python -m py_compile scripts/_gpt/plot_paper1_spine.py`: PASS
- `python scripts/_gpt/check_locked_numbers.py`: 22/22 PASS
- `python scripts/_gpt/check_local_pcm_precision_ladder.py`: PASS

## Remaining Design Debt

This pass fixes the visible top-level failure modes. A full Nature-style redesign of every supplementary data panel would require rebuilding the older source figure scripts one-by-one, especially the late SI pages with legacy plots. The current paper is now defensible; further work should prioritize only figures that enter the main text or reviewer-facing summary.
