# Codex Main-Figure Font Pass — 2026-05-02

## Reason

Main-text figure proportions were fixed in the previous pass, but inserted-PDF figure text was still too small for comfortable reading. The figure font also needed to be explicitly Times-compatible rather than relying on Matplotlib fallback behavior.

## Changes

Files updated:

- `scripts/_gpt/plot_paper1_spine.py`
- `scripts/_gpt/plot_paper1_decision_map.py`
- `paper/latex_gpt/figures/fig1_paper1_spine.pdf/png`
- `paper/latex_gpt/figures/fig2_paper1_decision_map.pdf/png`
- `paper/latex_gpt/main.pdf`

Specific changes:

1. Forced Matplotlib to load the system Tinos font files from `/usr/share/fonts/truetype/croscore/Tinos-*.ttf`.
2. Set figure font family to `Tinos`, a Times-compatible serif family.
3. Kept math text on STIX for clean math symbols.
4. Increased figure height and text size for main-text readability.
5. Kept key labels and numerical callouts bold.
6. Rebalanced Fig.2 decision-rule text to avoid overlap after font enlargement.

## Font Verification

```bash
pdffonts paper/latex_gpt/figures/fig1_paper1_spine.pdf
pdffonts paper/latex_gpt/figures/fig2_paper1_decision_map.pdf
pdffonts paper/latex_gpt/main.pdf | rg "Tinos|STIX|DejaVu|name"
```

Observed embedded fonts:

- `Tinos`
- `Tinos-Bold`
- `STIXGeneral-Regular`
- `STIXGeneral-Italic`

No DejaVu figure font remains in the main figure PDFs.

## Visual QA

Rendered pages 3-4 from the main PDF at 180 dpi. Result:

- Fig.1 text is larger and readable after insertion into the manuscript.
- Fig.2 card text and decision-rule text remain inside boxes.
- Panel labels, titles, key values, and axis labels are bold/readable.

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
- Critical log scan: PASS
- Locked-number guard: 22/22 PASS
- PCM precision-ladder guard: PASS
- Figure scripts compile: PASS
