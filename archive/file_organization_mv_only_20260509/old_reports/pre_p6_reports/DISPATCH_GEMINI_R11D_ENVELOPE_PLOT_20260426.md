# DISPATCH GEMINI R11D — Method Operating-Envelope Plot
**Date:** 2026-04-26 16:50 CST
**Issued by:** Claude
**Assignee:** Gemini
**Authority:** CLAUDE_ROUND11D_PATH_C_EXPLORATION_PLAN
**Priority:** HIGH (key paper figure for AIHWKit comparison narrative)
**Time budget:** ~1-2 days, after DS R11D-1 through R11D-4 lands

---

## 0. Mission

Build the **method operating-envelope plot** comparing Standard HAT / per-batch (AIHWKit-style) / per-epoch (Ensemble HAT) / fixed-mask across stress regimes. This is the figure that visualizes where each method breaks. Likely becomes Fig. 4 or Fig. 5 in main text.

---

## 1. Data sources (all from existing JSONs + R11D outputs)

### Existing (from paper-1)
- Standard HAT canonical: 10.00% (paper §5.5)
- Ensemble HAT canonical: 86.37 ± 1.54% (Round-10 R10A multi-seed: 86.16 ± 0.19%)
- §5.7 cadence ablation: per-epoch 88.41% / fixed 87.18% / per-batch 86.16%
- §5.6 iso-accuracy map: 63 points across (σ_D2D, ADC_bits)

### From R10E (just landed)
- AIHWKit at canonical (σ=0.10, 8-bit): **87.34 ± 0.14%**
- Path: `paper2_aihwkit_baseline/checkpoints/fresh_eval.json`

### From R11D (DS landing over next 5-7 days)
- R11D-1: AIHWKit at 4-bit precision
- R11D-2: AIHWKit at σ=0.20
- R11D-3: AIHWKit at σ=0.30 (conditional)
- R11D-4: AIHWKit with PCM device model
- R11D-6: Per-minibatch Ensemble HAT (conditional)

### Comparison: Ensemble HAT in same stress regimes
- Mostly extracted from existing iso-accuracy map (paper §5.6)
- 4-bit Ensemble HAT: paper §5.7 already has 86.37% at canonical (4-bit hybrid)
- σ=0.20 Ensemble HAT: extract from iso-accuracy map (Fig. contour-map)
- σ=0.30 Ensemble HAT: extract or interpolate

---

## 2. Plot design

### Option A — Single-panel comparison bar chart (simpler)

Bar chart with x-axis = stress regime (canonical / 4-bit / σ=0.20 / σ=0.30 / PCM), grouped bars per method:
- Standard HAT (red, leftmost in each group)
- AIHWKit (orange, second)
- Ensemble HAT (blue, third)
- Fixed-mask HAT (gray, rightmost)

Y-axis = fresh-instance accuracy %.

**Pros**: simple, clear winner per regime
**Cons**: doesn't show the 2D operating envelope

### Option B — 2D heatmap per method (richer)

3-4 small heatmaps in a row:
- Heatmap 1: Standard HAT accuracy across (σ_D2D, ADC_bits) — mostly red (collapses everywhere)
- Heatmap 2: AIHWKit per-batch — mostly green at canonical, red at extremes (R11D-2/3)
- Heatmap 3: Ensemble HAT per-epoch — mostly green (paper §5.6 iso-accuracy)
- Heatmap 4: Fixed-mask — mostly red

**Pros**: shows operating envelope as 2D regime
**Cons**: requires more data points (current paper-1 has full grid for Ensemble HAT only)

### Option C — Frontier line plot (recommended)

X-axis = stress level (composite: e.g., noise_level × precision_factor)  
Y-axis = fresh-instance accuracy
4 lines, one per method:
- Standard HAT (flat at 10%)
- AIHWKit (high at canonical, drops at high stress)
- Ensemble HAT (high across most range)
- Fixed-mask (flat at 87% — same as Standard but in-distribution; drops on transfer)

**Pros**: clean visual of "method operating envelope"; shows winner-per-regime
**Cons**: composite x-axis can be confusing

**My recommendation: Option C** with composite x-axis. Reviewer-friendly, paper-quality.

---

## 3. Style spec (Nat Electronics standard)

- Vector PDF + 300-DPI PNG
- Color palette: 4 colors max (consistent with Round-9 TikZ figures)
- Line style: solid for ours (Ensemble + Standard), dashed for AIHWKit
- Markers: circle for Ensemble, square for AIHWKit, triangle for Standard, diamond for Fixed
- Axis labels: 10pt sans-serif
- Caption-ready: must include error bars (1σ) where multi-seed exists

---

## 4. Output file naming

- `paper/latex_gpt/figures/fig_method_envelope.{png,pdf}` — main text figure
- Source: `paper/latex_gpt/figures/scripts/plot_method_envelope.py` — reproducible matplotlib

---

## 5. Caption draft (refine after R11D lands)

> **Figure X: Cross-instance fresh accuracy across stress regimes for four hardware-aware training methods.** Standard HAT (fixed mask) collapses uniformly to chance across all regimes (red). AIHWKit per-batch noise injection (orange) achieves cross-instance robustness at canonical settings but [does/does not] degrade under <stress regime>. Ensemble HAT per-epoch resampling (blue) maintains accuracy across the operating envelope. Fixed-mask HAT (gray) tests the source instance only. Error bars show fresh-instance variance (±1σ across 10 instances × 5 MC).

---

## 6. Workflow

### Day 1 (after R11D-1, R11D-2 land — likely Day 2-3 of DS work)
- Pull existing data from JSONs
- Sketch plot with skeleton + canonical numbers
- Iterate aesthetic with Claude review

### Day 2
- Land R11D-3, R11D-4, R11D-6 numbers as they arrive
- Final plot
- Caption polish

### Day 3
- Integrate into manuscript (replace fig5 or add as new fig depending on §6 placement decision)
- Coordinate with Kimi for caption + cross-references

---

## 7. Side task — AIHWKit comparison bar chart (small)

For Discussion §6.x AIHWKit comparison paragraph, render small inline figure:
- 3 bars: Standard HAT 10.00 / AIHWKit 87.34 / Ensemble HAT 86.16
- Output: `paper/latex_gpt/figures/figS_aihwkit_canonical.{png,pdf}`
- This is the supplementary version; main fig uses operating envelope

---

## 8. Hard constraints

- **No paper text edits** (Kimi)
- **No GPU experiments** (DS)
- **Vector PDF mandatory** (no rasterized matplotlib)
- **Color palette consistent** with Round-9 TikZ schematics + Phase-2 mechanism figures
- **Reproducible**: matplotlib script saved + commit

---

## 9. Cold-start refs

- `CLAUDE_ROUND11D_PATH_C_EXPLORATION_PLAN_20260426.md` — master plan
- `paper2_aihwkit_baseline/checkpoints/fresh_eval.json` — R10E AIHWKit canonical
- `report_md/_gpt/json_gpt/r10a_*` — R10A multi-seed Ensemble HAT
- `paper/latex_gpt/figures/fig_contour_map.pdf` — current iso-accuracy reference (style)
- DS R11D outputs (landing over next 5-7 days)

**No deadline.** ~1-2 days expected after R11D-1/2 land.
