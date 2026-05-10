# Codex Main-Figure Story Redesign — 2026-05-02

## Scope

Responded to the visual-review request that the main manuscript should rely more on composite figures and less on dense tables/text blocks.

## Changes Made

1. Added a new main-text composite figure:
   - `paper/latex_gpt/figures/fig2_paper1_decision_map.pdf`
   - `paper/latex_gpt/figures/fig2_paper1_decision_map.png`
   - generator: `scripts/_gpt/plot_paper1_decision_map.py`
   - source data: `paper/latex_gpt/source_data/fig2_paper1_decision_map.csv`

2. Replaced the main-text PCM precision table with Figure 2.
   - The full table remains in Supplementary Information.
   - Main text now uses the figure to explain the deployment decision: diagnose collapse, train with D2D-resampled Ensemble HAT, then choose PCM precision from retention budget.

3. Removed the dense blue design-rules box from the Discussion.
   - The same content is now represented by Figure 2 plus a short design-rule paragraph.

4. Compressed the Discussion text.
   - Removed repeated explanation of ADC/D2D/PCM constraints.
   - Kept numerical anchors and claim boundaries.
   - Moved the rhetorical burden back to figures and Supplementary Information.

5. Added `float` support in `main.tex` so the decision map stays with the relevant Results paragraph and does not collide with surrounding text.

## Visual QA

Rendered and inspected main PDF pages 4-6 at 180 dpi:

- Page 4: Figure 2 is placed cleanly, no overlap with paragraph or caption.
- Page 5: Discussion is shorter and less visually dense than the previous version.
- Page 6: Limitations section is compact and transitions cleanly into Methods.

No GPT-generated bitmap was needed. The new figure is a reproducible vector/data figure, which is safer for technical review than a generated illustration.

## Verification

Commands run:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
rg -n "Undefined|undefined|Reference .*undefined|Citation .*undefined|There were undefined|multiply defined|Overfull|Underfull|Warning" paper/latex_gpt/main.log || true
python scripts/_gpt/check_locked_numbers.py
python scripts/_gpt/check_local_pcm_precision_ladder.py
python -m py_compile scripts/_gpt/plot_paper1_decision_map.py scripts/_gpt/plot_paper1_spine.py
```

Results:

- Main manuscript compile: PASS
- Main log critical warning scan: PASS
- Locked numbers guard: 22/22 PASS
- PCM precision-ladder guard: PASS
- Figure scripts py_compile: PASS

## Remaining Judgment

The current main text is now acceptable as a figure-led story for the paper-1 submission bundle. Further visual work should focus on journal-specific final styling only, not more content expansion.

## Supplementary Check

Also checked Supplementary Information after the main-text changes:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex
rg -n "Undefined|undefined|Reference .*undefined|Citation .*undefined|There were undefined|multiply defined|Overfull|Underfull|Warning" paper/latex_gpt/supplementary_main.log || true
```

Result: PASS. No critical warning output.
