# CODEX R9B TIKZ REPORT — 2026-04-26

**Date:** 2026-04-26 00:35 CST
**Executor:** DeepSeek (Codex proxy)
**Status:** ALL 3 FIGURES COMPLETE (first pass)

---

## 1. Build Summary

| Figure | TikZ Source | Compiled PDF | Size | Status |
|:--|:--|:--|:--|:--|
| fig1 System Architecture | `tikz/fig1_system_architecture.tex` | `figures/fig1_system_architecture.pdf` | 88 KB | Done |
| fig2 Weight Mapping | `tikz/fig2_weight_mapping.tex` | `figures/fig2_weight_mapping.pdf` | 130 KB | Done |
| figS3 Ensemble HAT Concept | `tikz/figS3_ensemble_hat.tex` | `figures/figS3_ensemble_hat.pdf` | 118 KB | Done |

All compile cleanly with `pdflatex` (RC 0, no overfull/underfull warnings).

---

## 2. Design Decisions

### Color palette (consistent across all 3 figures)
- Analog blue: RGB(80,140,210) — crossbar, analog operations
- Digital orange: RGB(220,140,60) — peripheral circuits, digital ops
- Noise red: RGB(200,70,70) — D2D/C2C injection points
- Flow gray: RGB(140,140,145) — signal flow paths

### fig1 — System Architecture
- 3-panel vertical stack: device (a), array (b), network (c)
- Panel (a): Cross-section with substrate → bottom electrode → organic semiconductor → dielectric → top gate
- Panel (b): 4×4 crossbar grid with DAC/ADC endpoints, D2D/C2C labels, digital domain bracket
- Panel (c): 9-row table with analog/digital colored tags per layer type
- Known issue: table "Mapping" column labels use manual positioning — could be refined

### fig2 — Weight Mapping
- 7-stage horizontal flow: Input → Quantize → Diff Pair → Noise → MAC → ADC → Scale Recovery
- Each stage box contains 1-line title + 1-line math snippet
- Domain bands (digital/analog/digital) on background layer
- Noise injection point marked with red exclamation marker

### figS3 — Ensemble HAT Concept
- Side-by-side comparison: Standard HAT (red/failure) vs Ensemble HAT (green/success)
- Standard HAT: single M_0 mask → every epoch same → collapses to 10%
- Ensemble HAT: resampled M_i per epoch → distribution-matched → 86.37±1.54%
- Key mechanism box at top for paper context

---

## 3. Issues & TODOs

1. **PDF sizes are modest (88-130KB)** vs 150KB+ target. Could add more visual density (fine details, hatched patterns, gradient fills). Acceptable for first pass but should iterate.
2. **fig1 table (c)** uses manual row positioning — fragile if layer count changes. Could use `tabular` inside TikZ node for robustness.
3. **figS3 readability** at journal column width (~3.5") needs testing. Text may be too small.
4. **Full integration test** (compile main.tex with new figures) pending — verify no reference breakage.

---

## 4. Next Steps

- Claude/Gemini cross-review for aesthetic quality and narrative accuracy
- Iterate based on feedback (Day 2-3 if needed)
- Integration test with main.tex after any revisions
- Fallback not needed (TikZ approach works)

---

## 5. Files

| File | Path |
|:--|:--|
| fig1 source | `paper/latex_gpt/figures/tikz/fig1_system_architecture.tex` |
| fig1 PDF | `paper/latex_gpt/figures/fig1_system_architecture.pdf` |
| fig2 source | `paper/latex_gpt/figures/tikz/fig2_weight_mapping.tex` |
| fig2 PDF | `paper/latex_gpt/figures/fig2_weight_mapping.pdf` |
| figS3 source | `paper/latex_gpt/figures/tikz/figS3_ensemble_hat.tex` |
| figS3 PDF | `paper/latex_gpt/figures/figS3_ensemble_hat.pdf` |
| This report | `report_md/_gpt/CODEX_R9B_TIKZ_REPORT_20260426.md` |
