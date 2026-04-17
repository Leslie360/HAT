# Nano Banana Image Generation Prompts — Nature Communications Standard

> **For:** External image generation assistant (Banana)  
> **Context:** Nature Communications submission on organic optoelectronic compute-in-memory  
> **Style:** Academic journal figure, clean minimalist, professional  
> **Author:** Kimi (2026-04-11)

---

## CRITICAL INSTRUCTIONS FOR BANANA

**Who you are:**
- A professional scientific illustrator creating figures for Nature Communications
- Style reference: Nature, Science, Cell journal figures
- Clean, minimalist, data-driven aesthetic

**What you do NOT know:**
- You do NOT have access to our paper text
- You do NOT know our specific results
- You do NOT know our model architectures

**What you MUST do:**
- Follow prompts EXACTLY
- Use placeholder text for specific numbers (we will add labels in post-processing)
- Create vector-style clean illustrations
- Output high-resolution PNG (300 DPI minimum) or PDF

**Color scheme (MANDATORY):**
- Primary: Deep blue (#1f4e79) for digital components
- Secondary: Teal green (#2e8b57) for analog/organic components
- Accent: Orange (#ff6b35) for highlights/important features
- Background: White or very light gray
- Text: Black, sans-serif (Helvetica or Arial style)

---

## PROMPT 1: Differential Pair Asymmetry Concept (Fig S1)

### Purpose
Illustrate the concept of differential pair asymmetry in analog compute-in-memory arrays. This figure will accompany our experimental results on asymmetry tolerance.

### Detailed Description

**Layout:** Two-panel vertical figure

**TOP PANEL — "Ideal Symmetric Differential Pair"**
- Show two rectangular blocks side by side, labeled:
  - Left: "Positive Branch (G⁺)"
  - Right: "Negative Branch (G⁻)"
- Both blocks same height, same color (teal green #2e8b57)
- Between them: vertical arrow pointing down to "Differential Output = G⁺ − G⁻"
- Add equation below: "Effective Weight = (G⁺ − G⁻) / 2"
- Label at top: "α = 0 (Ideal)"

**BOTTOM PANEL — "With Systematic Asymmetry"**
- Same two blocks, but:
  - Left block (G⁺): 10% taller than ideal (stretch vertically)
  - Right block (G⁻): 10% shorter than ideal (compress vertically)
- Use darker shade for G⁺, lighter shade for G⁻ to emphasize difference
- Same differential output arrow
- Label at top: "α = 0.10 (10% Asymmetry)"

**EQUATIONS (include as text in figure):**
- Top right corner: "Asymmetry Factor: α ∈ [0, 0.20]"
- Bottom: "G⁺_effective = G⁺ × (1 + α)"
- Bottom: "G⁻_effective = G⁻ × (1 − α)"

**Style notes:**
- Clean vector graphics, no 3D effects
- Thin black borders around blocks
- Arrowheads should be triangular and filled
- White background
- All text should be readable at 300 DPI when printed at single-column width (8.5 cm)

**Output:** PNG, 300 DPI, 1800×2400 pixels (portrait), white background

---

## PROMPT 2: Physical Non-Idealities in Memory Arrays (Fig S2)

### Purpose
Illustrate two common non-ideal effects in resistive memory arrays: IR drop and sneak path currents.

### Detailed Description

**Layout:** Two-panel horizontal figure

**LEFT PANEL — "IR Drop Effect"**
- Title at top: "IR Drop (Position-Dependent Voltage Loss)"
- Draw a rectangular grid representing a crossbar array (4×4 cells minimum)
- Show horizontal wordlines and vertical bitlines crossing at each cell
- Left side: label "VDD" with battery symbol
- Right side: label "VSS" (ground)
- Use color gradient: left side bright blue (#4a90e2), gradually fading to darker blue (#1a365d) toward right
- Add annotation: "Voltage decreases along wordlines due to series resistance"
- Draw small resistor symbols along wordlines to indicate resistance

**RIGHT PANEL — "Sneak Path Currents"**
- Title at top: "Sneak Paths (Unintended Current Paths)"
- Draw similar 4×4 crossbar grid
- Highlight one specific cell in center with orange fill (#ff6b35) — this is the "target cell" being read
- Draw dashed orange lines showing alternative current paths through adjacent cells
- Label: "Primary path" (solid line to target cell)
- Label: "Sneak paths" (dashed lines through neighbors)
- Add text: "Current leaks through unselected cells, causing read errors"

**Below both panels:**
- Add equation: "Effective Conductance = G_ideal + ΔG_error"
- Add text: "Error magnitude: 1–3% for typical array sizes"

**Style notes:**
- Grid lines: thin gray (#cccccc)
- Cell fills: teal green (#2e8b57) for normal cells, orange (#ff6b35) for highlighted
- Current paths: orange arrows (solid for primary, dashed for sneak)
- Clean, schematic style (not photorealistic)

**Output:** PNG, 300 DPI, 2400×1600 pixels (landscape), white background

---

## PROMPT 3: Hybrid Analog/Digital Architecture (Fig 1 Enhancement)

### Purpose
System architecture diagram showing which components of a Vision Transformer are mapped to analog vs digital hardware.

### Detailed Description

**Layout:** Three-tier horizontal flow diagram (left to right)

**TIER 1 — INPUT (Left, 20% width)**
- Draw rectangle labeled "Input Image"
- Arrow pointing right to "Patch Embedding"

**TIER 2 — PROCESSING CENTER (Middle, 60% width)**
- Divide into two vertical zones:

**Zone A — "ANALOG CIM ARRAY" (Top half, teal green background #e8f5e9)**
- Label at top: "Static Operations → Analog Crossbar"
- List items with icons:
  - □ Patch Embedding Convolutions
  - □ QKV Projections (Query, Key, Value)
  - □ Attention Output Projection
  - □ Feed-Forward Networks (MLP)
- Show small crossbar grid pattern as background watermark

**Zone B — "DIGITAL PROCESSOR" (Bottom half, light blue background #e3f2fd)**
- Label at top: "Dynamic Operations → Digital CMOS"
- List items with icons:
  - □ Depthwise Convolutions
  - □ Layer Normalization
  - □ QKᵀ Matrix Multiplication (attention scores)
  - □ Softmax Normalization
- Show CPU/chip icon as background watermark

**TIER 3 — OUTPUT (Right, 20% width)**
- Draw rectangle labeled "Classification Head"
- Arrow pointing to "Output Classes (10)"

**CONNECTING ARROWS:**
- Use thick arrows between tiers
- Analog zone: teal green arrows
- Digital zone: blue arrows

**ANNOTATIONS:**
- Top banner: "87.7% of parameters execute on analog arrays"
- Bottom banner: "57.9% of energy consumed by digital attention"
- Small text: "Differential pair encoding provides noise immunity"

**Style notes:**
- Flat design, no shadows or 3D effects
- Rounded rectangles (corner radius ~5px)
- Consistent icon style (line icons, 2px stroke)
- Plenty of white space between elements

**Output:** PNG, 300 DPI, 3200×2000 pixels (landscape), white background

---

## PROMPT 4: Ensemble Hardware-Aware Training Concept (Fig S3) — HIGHEST PRIORITY

### Purpose
Illustrate our key innovation: Ensemble HAT trains with resampled device noise to improve robustness on fresh hardware instances.

### Detailed Description

**Layout:** Two-row comparison figure with result bars on right

**ROW 1 — "Standard Hardware-Aware Training (HAT)"**
- Title: "Standard HAT"
- Draw timeline: "Epoch 1 → Epoch 2 → ... → Epoch N"
- Above each epoch: show a small grid pattern representing "D2D Noise Mask"
- CRITICAL: All grids should be IDENTICAL (same pattern)
- Label: "Single fixed D2D realization throughout training"
- Below: arrow to box labeled "Trained Model"
- Result icon: ⚠️ warning symbol with text: "Overfits to training instance"

**ROW 2 — "Ensemble HAT (Our Method)"**
- Title: "Ensemble HAT"
- Same timeline: "Epoch 1 → Epoch 2 → ... → Epoch N"
- Above each epoch: different D2D noise mask pattern for each epoch
- CRITICAL: Each grid pattern must be VISIBLY DIFFERENT (use different dot patterns)
- Use varying densities/patterns to show randomness
- Label: "Resampled D2D masks each epoch"
- Below: arrow to box labeled "Robust Model"
- Result icon: ✓ checkmark with text: "Generalizes to fresh instances"

**RIGHT SIDE — Performance Comparison Bar Chart**
- Two vertical bars:
  - Left bar (short, red/orange): "Standard HAT"
    - Height: ~15% of max
    - Label below: "Fresh Instance Accuracy: ~10% (chance level)"
  - Right bar (tall, green): "Ensemble HAT"
    - Height: ~85% of max
    - Label below: "Fresh Instance Accuracy: ~86%"
- Y-axis label: "Accuracy (%)"
- Add asterisk: "*Both trained to >97% on training instance"

**KEY MESSAGE (include as text):**
"Training with diverse hardware realizations enables zero-shot transfer to unseen device instances."

**Style notes:**
- Epoch grids: 5×5 pixel patterns, random dots representing device-to-device variation
- Use purple (#6b4c9a) for Standard HAT row
- Use teal green (#2e8b57) for Ensemble HAT row
- Bar chart: simple solid fills, no gradients
- Clean separation between rows with horizontal line

**Output:** PNG, 300 DPI, 2400×2000 pixels, white background

---

## PROMPT 5: Graphical Abstract / TOC Image

### Purpose
Eye-catching artistic representation of organic optoelectronic synaptic devices for journal cover or table of contents.

### Detailed Description

**Composition:**
- Central focus: Organic synaptic transistor device
- Artistic style: Blend of photorealism and abstract visualization

**Central Device:**
- Show layered structure (cross-section view):
  - Bottom: Substrate (light gray)
  - Middle: Organic semiconductor layer (emerald green with molecular pattern)
  - Top: Transparent electrode (gold contacts on sides)
- Green glow emanating from organic layer (indicating photoresponse)
- Light rays entering from top (optical programming)

**Background Elements:**
- Faint neural network connections (thin gray lines, nodes as small circles)
- Gradient from digital blue (top left) to organic green (bottom right)
- Subtle circuit pattern watermark

**Foreground:**
- Stylized photons as small yellow dots entering device
- Synaptic weight visualization: vertical bar graph with varying heights

**Color Palette:**
- Deep blues (#1a365d) for digital/computational elements
- Emerald greens (#2e8b57, #34d399) for organic components
- Gold/yellow (#fbbf24) for light/electrical signals
- White background with subtle texture

**Text (if any):**
- Title at bottom: "Organic Optoelectronic CIM" (clean sans-serif)
- No other text

**Style:**
- Suitable for Nature Communications cover art
- 16:9 aspect ratio
- High contrast, professional lighting
- Modern, forward-looking aesthetic

**Output:** PNG, 300 DPI, 3200×1800 pixels (landscape), white/light background

---

## GENERATION CHECKLIST

For EACH prompt, verify:
- [ ] Color scheme matches specification
- [ ] No text smaller than 8pt when printed at target size
- [ ] 300 DPI minimum resolution
- [ ] White or transparent background
- [ ] Clean vector-style appearance (no photorealistic textures unless specified)
- [ ] All scientific elements clearly labeled
- [ ] Aspect ratio matches specification

---

## PRIORITY ORDER

Generate in this order:
1. **PROMPT 4** (Ensemble HAT) — Core innovation, highest impact
2. **PROMPT 1** (Differential Asymmetry) — Supports experimental results
3. **PROMPT 2** (Physical Non-Idealities) — Supports limitation discussion
4. **PROMPT 3** (Architecture) — System overview
5. **PROMPT 5** (TOC Image) — Decorative, lowest priority

---

## USAGE RIGHTS

These figures will be used in:
- Nature Communications manuscript (main text and supplementary)
- arXiv preprint
- Conference presentations

All figures must be original generation, no copyrighted elements.

---

*Prepared by Kimi for Nature Communications submission*  
*Date: 2026-04-11*
