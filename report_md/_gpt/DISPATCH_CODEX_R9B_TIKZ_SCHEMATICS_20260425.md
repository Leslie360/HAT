# DISPATCH CODEX R9B — TikZ Schematic Rebuild
**Date:** 2026-04-25 22:30 CST
**Issued by:** Claude
**Assignee:** Codex
**Authority:** CLAUDE_ROUND9_PAPER1_HARDENING_PLAN_20260425 §3 Track B
**Priority:** HIGH (presentation quality fix)
**Time budget:** 5-7 days (~5-10% of Codex bandwidth, doesn't block W2)
**Constraint:** No GPU. Pure LaTeX/TikZ work. W2 Phase 2 GPU work continues independently.

---

## 0. Mission

Rebuild **3 critical schematic figures** as proper TikZ code: replace the current 24-34KB matplotlib auto-output with publication-quality vector schematics that match Nature Electronics aesthetic standards.

---

## 1. Problem (why this matters)

| Figure | Current state | Why ugly |
|:--|:--|:--|
| `fig1_system_architecture.pdf` | 24KB matplotlib (April 9) | Auto-rendered boxes/arrows; no proper layered architecture; doesn't show device→array→network flow |
| `fig2_weight_mapping.pdf` | 34KB matplotlib (April 9) | Doesn't communicate analog-to-digital pipeline; tiny labels |
| `figS3_ensemble_hat.pdf` | 32KB matplotlib (April 19) | Concept figure for the paper's signature method — currently unclear |

Compare: typical Nature Electronics published schematic = 200-500KB vector PDF, multi-panel, uses TikZ or Inkscape.

---

## 2. Three figures to build

### 2.1 fig1 — System Architecture (3-panel)

**Layout**: 3 panels stacked vertically (full page width, ~7" wide × 6" tall)

**Panel (a) Device level**: Cross-section schematic of organic optoelectronic memory cell
- Top electrode (gate)
- Organic semiconductor layer (label: photoresponsive)
- Bottom electrode (source/drain)
- Optional photon arrow incident on top
- Conductance G label on side
- Caption: "Multilevel conductance state controlled by gate-charge profile; sub-linear photoresponse $I_{\text{photo}} \propto P^{\gamma_{\text{phys}}}$"

**Panel (b) Array level**: Crossbar schematic with hybrid analog-digital partitioning
- 4×4 abstracted crossbar grid (rows = WL, cols = BL)
- ADC blocks at column ends (label: 6-bit + DNL)
- DAC blocks at row inputs (label: 4-bit weight quantization)
- Highlight which ops are analog (multiply-accumulate inside crossbar) vs digital (softmax, normalization, residual sum) outside
- Annotations: D2D mismatch (per-cell), C2C noise (per-read)

**Panel (c) Network level**: ViT block conversion table
- Three columns: TinyViT block layer name | Analog vs Digital | Noise injection point
- Row entries: PatchEmbed (analog), QKV proj (analog), Softmax (digital), Output proj (analog), MLP fc1 (analog), MLP fc2 (analog), LayerNorm (digital), Residual sum (digital)
- Caption: "Hybrid analog-digital deployment policy: dense linear ops on crossbar, dynamic ops digital."

**Style spec**:
- Use TikZ + `tikz-cd` for arrow logic if needed
- Color palette: 3 colors max (analog blue, digital orange, signal flow gray)
- Sans-serif labels (\sffamily) ~9pt
- Panel labels (a)/(b)/(c) bold ~11pt
- White space: ~10% margin around each panel
- Total file: 200-400KB target

**File output**: 
- `paper/latex_gpt/figures/tikz/fig1_system_architecture.tex` — TikZ source
- `paper/latex_gpt/figures/fig1_system_architecture.pdf` — compiled output

### 2.2 fig2 — Weight Mapping (flow diagram)

**Layout**: Single panel, horizontal flow (6" wide × 3" tall)

**Flow stages (left → right)**:

1. **Input**: Software weight tensor W (32-bit float)
   - Show small heatmap-style 4x4 grid with continuous values
   
2. **Quantization**: 4-bit weight quantization
   - Arrow labeled `quantize`
   - Output: W_q (16 levels)

3. **Mapping**: Differential pair encoding
   - Arrow labeled `differential pair`
   - Output: G_pos / G_neg conductance pair
   - Math snippet: `G_pos - G_neg = W_q`

4. **Device noise**: D2D mismatch + C2C noise
   - Arrow labeled `D2D + C2C`
   - Symbol: $W_{\text{eff}} = (W_q \cdot G_{\text{pair}}) \odot (1 + M_{\text{D2D}}) + \xi_{\text{C2C}}$
   - Color the D2D box differently to highlight per-cell-fixed nature

5. **MAC**: Crossbar matrix-vector multiply
   - Arrow labeled `analog MAC`
   - Output: I_out (current)

6. **ADC**: Output current quantization
   - Arrow labeled `ADC` 
   - 6-bit (b=6) labeled
   - Output: digital activation

7. **Scale recovery**: Calibrated gain
   - Arrow labeled `scale recovery`
   - Math: `y = (I_out / G_max) * scale`
   - Output: y (final activation)

**Style spec**:
- Boxes for each stage, rounded corners
- Each box has a 1-line label + 1-line math snippet
- Arrows flow left-to-right, label noise injection points
- Same color palette as fig1 (analog blue, digital orange, flow gray)
- 200-400KB target

**File output**:
- `paper/latex_gpt/figures/tikz/fig2_weight_mapping.tex` — TikZ source
- `paper/latex_gpt/figures/fig2_weight_mapping.pdf` — compiled output

### 2.3 figS3 — Ensemble HAT Concept (side-by-side comparison)

**Layout**: 2 panels side-by-side (full page width, 6" wide × 4" tall)

**Panel (a) Standard HAT (left)**:
- Top: training loop showing single fixed mask M_0 used every epoch
- Below: Each epoch icon → same M_0 inserted
- Bottom: "Test on fresh hardware instance M_new" → red collapse arrow → 10.00% accuracy
- Color: red/orange to indicate failure

**Panel (b) Ensemble HAT (right)**:
- Top: training loop showing per-epoch resampled masks {M_1, M_2, M_3, ...}
- Below: Each epoch icon → different M_i inserted
- Bottom: "Test on fresh hardware instance M_new" → green checkmark → 86.37 ± 1.54% accuracy
- Color: green/blue to indicate success

**Center label** (between panels): "Hardware-instance overfitting" (left) vs "Distribution-matched training" (right)

**Style spec**:
- Match the visual logic of "fixed point" vs "distribution sampling"
- Use small icons: hammer/wrench for "fixed", multiple dice for "resampled"
- Match Round-7 sprint Phase 2 mechanism figure aesthetic
- Same color palette as fig1+fig2
- 200-400KB target

**File output**:
- `paper/latex_gpt/figures/tikz/figS3_ensemble_hat.tex` — TikZ source
- `paper/latex_gpt/figures/figS3_ensemble_hat.pdf` — compiled output

---

## 3. Reference aesthetics

Look at these published papers (open-access PDFs) for layout inspiration:
- Sebastian et al. 2018 Nature Communications "Mixed-precision in-memory computing" — fig 1 system architecture
- Burr et al. 2017 IEEE TED "Neuromorphic computing using non-volatile memory" — crossbar schematic
- Rasch et al. 2023 IBM AIHWKit Nature Communications — fig 2 hybrid analog-digital flow
- Foret et al. 2021 ICLR SAM — concept comparison figures (sharp vs flat)

Don't copy them. Match the cleanliness/professionalism level.

---

## 4. Workflow (suggested)

### Day 1-2: fig1 system architecture
- Sketch panel layout on paper or whiteboard first
- Translate to TikZ
- Iterate 2-3 times for spacing/labels
- Compile + check PDF size + visual quality

### Day 3-4: fig2 weight mapping
- Same workflow

### Day 5-6: figS3 Ensemble HAT
- Same workflow

### Day 7: Integration test
- Verify all 3 figures embed cleanly in main.tex
- Run full compile; check no figure-related warnings
- Commit TikZ sources + compiled PDFs

---

## 5. TikZ practical tips

- Use `\usepackage{tikz}` + `\usetikzlibrary{positioning,arrows.meta,shapes.geometric}`
- `\node[draw, rounded corners, fill=blue!20, ...]` for analog boxes
- `\draw[->, thick, >=stealth]` for arrows
- Standalone compile pattern: each `tikz/figX.tex` is `\documentclass{standalone}` + content; produces standalone PDF
- Then `\includegraphics{figures/fig1_system_architecture.pdf}` in main.tex
- Compilation: `cd paper/latex_gpt/figures/tikz && pdflatex fig1_system_architecture.tex && mv fig1_system_architecture.pdf ../`

---

## 6. Constraints (HARD)

- **No matplotlib for these 3 figures.** Pure TikZ.
- **No replacing the data figures** (figS_d2d_loss_landscape, figS_hessian_spectrum, etc. — those are matplotlib by intent).
- **Must compile cleanly** with current main.tex; no breaking existing figure refs.
- **Vector PDF only**: no rasterized output.
- **Color palette consistency**: 3 colors max across all 3 figures.
- **Don't change figure references** in main.tex — output filenames must match: `fig1_system_architecture.pdf`, `fig2_weight_mapping.pdf`, `figS3_ensemble_hat.pdf`.

---

## 7. Fallback (if TikZ takes too long)

If after Day 4 fig1 isn't acceptable: fallback to high-quality matplotlib using:
- `matplotlib.patches` for proper boxes (not auto)
- Larger font sizes (12pt min)
- Designed color palette
- Annotated arrows with `FancyArrowPatch`

This is plan B; aim for plan A (TikZ) first.

---

## 8. Deliverables

| File | Type |
|:--|:--|
| `paper/latex_gpt/figures/tikz/fig1_system_architecture.tex` | TikZ source |
| `paper/latex_gpt/figures/tikz/fig2_weight_mapping.tex` | TikZ source |
| `paper/latex_gpt/figures/tikz/figS3_ensemble_hat.tex` | TikZ source |
| `paper/latex_gpt/figures/fig1_system_architecture.pdf` | Compiled (replaces 24KB matplotlib) |
| `paper/latex_gpt/figures/fig2_weight_mapping.pdf` | Compiled (replaces 34KB matplotlib) |
| `paper/latex_gpt/figures/figS3_ensemble_hat.pdf` | Compiled (replaces 32KB matplotlib) |
| `CODEX_R9B_TIKZ_REPORT_20260425.md` | Status + design decisions + iteration log |

---

## 9. Success criteria

- All 3 schematics ≥ 150KB vector PDF (vs current 24-34KB)
- TikZ source is git-friendly (text, diff-able)
- Aesthetic at Nature Electronics standard (judged by Claude review + Gemini cross-review)
- main.tex compiles RC 0 with new figures
- Caption text in main.tex is improved to be self-contained

---

## 10. Coordination

- Track A (Kimi length surgery) runs parallel — your TikZ work doesn't conflict
- Track C (Kimi defense paragraphs) parallel — different surface area
- Round-8 W2 Phase 2 continues on local GPU — your TikZ is CPU-only, no contention
- 8×40GB cross-arch independent

**No deadline.** 5-7 days expected.
