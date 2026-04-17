# Nano Banana Schematic Prompts

These prompts are for **non-quantitative schematic figures only**. Do **not** use AI-generated art for plots that encode measured or simulated numbers. The target visual language is a clean journal-style scientific schematic: white background, crisp vector-like edges, restrained palette, no decorative glow, no fake 3D chrome, and no excessive embedded text.

## Prompt 1: Fig.1 System Architecture

```text
Create a clean scientific schematic for a journal paper on "organic optoelectronic compute-in-memory inference for edge vision".

Scene:
- A left-to-right system overview with five main stages:
  1. optical scene / image input
  2. organic optoelectronic front-end sensing
  3. analog CIM crossbar blocks for dense linear operators
  4. digital attention / softmax / normalization blocks
  5. final classification output

Content requirements:
- Show that early optical sensing feeds a hybrid analog-digital inference pipeline.
- The analog domain should be represented by crossbar arrays and current-summing arrows.
- The digital domain should be represented by compact processor-like blocks for QK^T, softmax, A·V, and LayerNorm.
- Clearly indicate that only dense projections / MLP layers are mapped to analog CIM, while dynamic attention operations remain digital.
- Include a small side annotation for "profile-driven non-idealities": quantization, C2C noise, D2D mismatch, retention, ADC/DAC effects.
- Include one compact label for "hardware-aware training / evaluation framework".

Visual style:
- Publication-quality schematic, minimal text, no paragraph labels inside the figure.
- Muted palette: steel blue, dark teal, warm gray, soft orange accents.
- Flat scientific illustration, not cartoonish, not photorealistic.
- Precise spacing, balanced composition, strong hierarchy, easy to read when scaled down.
- White background.
- Landscape layout, approximately 16:9.

Avoid:
- No decorative circuit-board wallpaper.
- No neon glow.
- No duplicated captions like "Fig.1" inside the image.
- No long sentences inside blocks.
- No random icons unrelated to optics or compute.
```

## Prompt 2: Fig.2 Weight Mapping and Behavioral Model

```text
Create a clean journal-style scientific schematic illustrating differential conductance mapping and behavioral non-idealities for analog compute-in-memory.

Scene:
- Three horizontally arranged panels:
  Panel A: digital weights mapped to positive/negative conductance pair (G+ and G-)
  Panel B: quantized conductance states on a discrete ladder between Gmin and Gmax
  Panel C: behavioral perturbations applied during inference/training

Panel details:
- Panel A should show a weight w being decomposed into a differential pair and programmed into two cells.
- Panel B should show discrete conductance levels, highlighting finite state resolution.
- Panel C should show compact overlays for:
  - cycle-to-cycle noise
  - device-to-device mismatch
  - retention drift over time
  - nonlinear write asymmetry
  - ADC readout quantization
- Include a small note that scale recovery is digital post-processing.

Visual style:
- Crisp vector-like scientific illustration.
- Minimal embedded text: short labels only.
- Consistent muted palette: navy, green, gray, amber.
- Flat white background, no shadow-heavy UI style.
- Balanced spacing and strong alignment.
- Designed for a high-quality engineering journal.

Avoid:
- No "Fig.2" label inside the figure.
- No dense equations inside the image.
- No hand-drawn sketch look.
- No futuristic hologram style.
- No busy background textures.
```

## Prompt 3: Optional Fig.6 Front-End Compensation Concept

```text
Create a compact scientific schematic showing the trade-off of inverse-gamma compensation in an organic optoelectronic front-end.

Scene:
- A three-step flow:
  1. sub-linear optical response curve
  2. inverse-gamma compensation block
  3. resulting trade-off: darker regions recovered, bright-region noise amplified

Visual requirements:
- Include one clean response curve before compensation and one after compensation.
- Include a small low-light patch and high-light patch to visually suggest "signal recovery" versus "noise amplification".
- Keep labels minimal and publication-ready.
- White background, restrained color palette, no decorative clutter.

Avoid:
- No exaggerated photographic collage.
- No big paragraph text.
- No fake UI widgets.
```
