# Nano Banana 图像生成 Prompts

> 场外视觉援助请求清单

---

## Prompt 1: 差分对不对称性示意图 (Fig S1)

**用途：** 补充§6.6和EXP-A的说明，展示differential pair asymmetry概念

**Prompt:**
```
Scientific diagram illustration for a research paper on neuromorphic computing.
Show a differential pair crossbar array with two branches:
- LEFT branch labeled "Positive Branch (G+)" with conductance values
- RIGHT branch labeled "Negative Branch (G-)" with conductance values
- Center shows "Differential Output = G+ - G-"

Top panel: "Ideal Symmetric Case" with balanced branches
Bottom panel: "With Asymmetry" where one branch is 10% larger than the other

Use clean academic style, blue and orange color scheme, white background,
minimalist design similar to Nature/Science journal figures.
Include small equation: "Asymmetry = (G+ - G-) / (G+ + G-)"
```

**对应：** EXP-A实验，§6.6 Differential-Pair Symmetry limitation

---

## Prompt 2: 物理非理想性示意图 (Fig S2)

**用途：** 展示IR drop和sneak path效应，补充§6.6和EXP-B

**Prompt:**
```
Scientific diagram showing two physical non-idealities in memory arrays:

LEFT PANEL - "IR Drop Effect":
- Show a crossbar array with wordlines and bitlines
- Voltage gradient from VDD at top to VDD-ΔV at bottom
- Color gradient showing voltage drop along lines
- Label: "Position-dependent voltage drop"

RIGHT PANEL - "Sneak Path Currents":
- Show a 3x3 crossbar array
- Highlight one cell in red (target cell)
- Show unintended current paths (sneak paths) in dotted gray lines
- Label: "Leakage through adjacent cells"

Clean academic style, gradient blue color scheme, white background.
Include equivalent circuit diagrams below each panel.
```

**对应：** EXP-B实验，§6.6 Hardware Array Non-Idealities

---

## Prompt 3: 混合模拟/数字架构图 (Fig 1 优化版)

**用途：** 替代或增强现有的系统架构图

**Prompt:**
```
System architecture diagram for an AI accelerator chip. Clean scientific illustration style.

Show three horizontal layers:
TOP LAYER - "Digital Domain" (blue):
- Input: Image patch embeddings
- Attention QK^T computation
- Softmax normalization
- Label: "Dynamic Operations → Digital"

MIDDLE LAYER - "Analog Domain" (green):
- Crossbar array grid pattern
- Matrix-vector multiplication blocks
- Label: "Dense Linear Ops → Analog CIM"

BOTTOM LAYER - "Peripherals" (gray):
- ADC/DAC converters
- Digital scale recovery
- Label: "Interface Circuits"

Show data flow with arrows from top to bottom.
Include small icon labels: "87.7% params analog" and "57.9% energy digital"
Clean minimalist style, suitable for Nature Communications journal.
```

**对应：** §3.1 Hybrid Analog/Digital Deployment, Fig 1

---

## Prompt 4: Ensemble HAT概念图 (Fig S3)

**用途：** 展示Ensemble HAT的核心创新——训练时D2D重采样

**Prompt:**
```
Scientific concept diagram showing "Ensemble Hardware-Aware Training" for neural networks.

TOP ROW - "Standard HAT":
- Single D2D noise mask (fixed pattern shown as grid)
- Arrow → "Trained Model"
- Result: "Overfits to single instance"

BOTTOM ROW - "Ensemble HAT (Our Method)":
- Multiple D2D masks shown in sequence (Epoch 1, Epoch 2, ..., Epoch N)
- Each epoch has different noise pattern
- Arrow → "Robust Model"
- Result: "Generalizes across instances"

Show comparison with accuracy bars on the right:
- Standard: 10% (chance level on fresh instance)
- Ensemble: 86% (high accuracy on fresh instance)

Clean academic style, purple and teal color scheme, white background.
Suitable for Nature/Science supplementary figure.
```

**对应：** §5.8 Ensemble HAT, 核心贡献亮点

---

## Prompt 5: 有机光电突触器件图 (装饰性)

**用途：** 作为graphical abstract或TOC (Table of Contents)图像

**Prompt:**
```
Artistic scientific illustration of an organic optoelectronic synaptic device.

Central focus:
- Organic semiconductor layer with molecular structure pattern
- Light shining from top (optical programming)
- Electrical contacts on sides (source/drain electrodes)
- Green glow indicating photoresponse

Background elements:
- Faint circuit patterns
- Neural network node connections
- Gradient from blue (digital) to green (organic)

Style: Modern scientific journal cover art, blend of realism and abstraction,
suitable for Nature Communications graphical abstract.
High contrast, professional lighting, 16:9 aspect ratio.
```

**对应：** 投稿封面/TOC图像

---

## 优先级建议

| 优先级 | Prompt | 用途 | 尺寸 |
|:-------|:-------|:-----|:-----|
| **HIGH** | Prompt 4 (Ensemble HAT) | 核心贡献可视化 | 单栏 |
| **HIGH** | Prompt 1 (Asymmetry) | EXP-A支撑 | 单栏 |
| **MED** | Prompt 2 (Non-ideality) | EXP-B支撑 | 单栏 |
| **MED** | Prompt 3 (Architecture) | 系统图优化 | 双栏 |
| **LOW** | Prompt 5 (TOC) | 装饰性 | 灵活 |

---

## 输出格式要求

请生成：
- **格式：** PNG 或 PDF
- **分辨率：** 300 DPI (print quality)
- **背景：** 白色或透明
- **字体：**  sans-serif, 清晰可读

---

*Kimi prepared, 2026-04-11*
