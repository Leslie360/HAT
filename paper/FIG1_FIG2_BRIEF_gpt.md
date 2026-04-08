# Fig.1 / Fig.2 Manual Figure Brief (GPT)

This document is the manual-drawing brief for the two remaining non-automated figures.

Canonical companion files:
- `paper/FIGURE_PLAN.md`
- `paper/03_methodology.md`
- `paper/latex_gpt/main.tex`

The goal is **academic clarity over decoration**. Both figures should be simple, restrained, and consistent with a materials-to-system journal style.

## Shared Style

- White background
- Black / dark gray outlines
- One restrained accent color for analog blocks
- One restrained accent color for digital blocks
- No gradients, no pseudo-3D
- Use short labels, not paragraph text
- Prefer vector output (`PDF`/`SVG`) if possible

---

## Fig.1: System Architecture Overview

### Purpose

Show the end-to-end hybrid deployment stack from image input to final prediction, and make the analog/digital split visually obvious.

### Core message

This is **not** a fully analog transformer. Static dense operators map to crossbar arrays, while dynamic attention and control-heavy operators remain digital.

### Recommended layout

Left-to-right pipeline with five large blocks:

1. **Image / Sensor Input**
   - label: `Input image`
   - optional small note: `edge vision sample`

2. **Physical Frontend (optional path)**
   - label: `Physical frontend`
   - sublabels:
     - `photoresponse`
     - `inverse-gamma compensation`
   - visually indicate this is an optional pre-array stage used in the physical-frontend experiments

3. **Hybrid Tiny-ViT / CNN Backbone**
   split into two stacked bands:
   - upper band: `Analog crossbar path`
     - `Patch embedding`
     - `Q / K / V projections`
     - `Attention output projection`
     - `MLP fc1 / fc2`
   - lower band: `Digital coprocessor path`
     - `MBConv / depthwise conv`
     - `QK^T / AV`
     - `Softmax`
     - `LayerNorm`
     - `Activation / control`

4. **Peripheral / Calibration**
   - `ADC / DAC`
   - `scale recovery`
   - `noise / retention / profile injection`

5. **Output**
   - `Classifier`
   - `Top-1 prediction`

### Must-show annotations

- A visible note near attention:
  - `Dynamic attention products remain digital`
- A visible note near arrays:
  - `Static dense weights stored in crossbar`
- A visible note near profile block:
  - `literature or measured device profile`

### Caption intent

Explain that the figure shows the materials-to-system pipeline and the analog/digital boundary, rather than claiming a fully analog transformer implementation.

---

## Fig.2: Weight-to-Conductance Mapping Flow

### Purpose

Show how a floating-point weight tensor becomes a noisy effective analog weight used during forward propagation.

### Core message

The framework operates through a **differential-pair conductance abstraction** with quantization, variability, optional nonlinear-write surrogate effects, retention, and digital scale recovery.

### Recommended layout

Top-to-bottom or left-to-right flowchart with 8 boxes:

1. `FP32 weight tensor W`
2. `Split into W+ / W-`
3. `Normalize by ||W||_inf`
4. `Map to conductance range [G_min, G_max]`
5. `Quantize to n_states (STE)`
6. `Apply device effects`
   - `D2D`
   - `C2C`
   - `retention`
   - optional note: `proportional noise / NL stress`
7. `Differential readout: G+ - G-`
8. `Digital scale recovery -> effective weight`

### Optional side inset

Small side panel for:
- `uniform noise`
- `proportional noise`
- `NL_LTP / NL_LTD surrogate`

Keep this as a compact inset, not a second figure.

### Must-show equations or mini-labels

Only minimal symbolic anchors, not full derivations:
- `W+ = max(W,0)`
- `W- = max(-W,0)`
- `G_eff = G+ - G-`
- `restore_weight_scale`

### Caption intent

Explain that this is a behavioral mapping pipeline, not a pulse-accurate circuit schematic.

---

## Priority

If only one manual figure can be polished first:

1. **Fig.1 first**
   - because it anchors the whole paper for reviewers
2. **Fig.2 second**
   - because it clarifies the simulator abstraction and caveats

---

## Ownership Note

- Codex prepared this brief for the English manuscript.
- Gemini may mirror the same logic in `paper_zh/`, but this file is the canonical manual-figure spec on the GPT side.
