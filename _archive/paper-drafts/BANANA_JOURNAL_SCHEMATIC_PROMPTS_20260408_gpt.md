# Banana Prompts For Journal-Style Schematics

Use these only for **non-quantitative schematic figures**. Do **not** use AI generation for any plot that contains real numbers, axes, bars, curves, or experimental measurements.

## Style Direction

Common style requirements for all prompts:
- clean Nature/Science-style schematic
- white background
- restrained palette: teal, slate gray, muted orange, charcoal
- no glossy 3D look
- no cartoon style
- no fake chart axes
- thin, precise arrows
- professional scientific typography
- minimal text inside figure
- publication-quality vector-like composition
- clear visual hierarchy

## Prompt A: Fig.1 System Architecture

```text
Create a publication-quality scientific schematic for a paper on organic optoelectronic compute-in-memory inference for edge vision.

The figure should show a hybrid analog/digital inference stack from left to right:
1. input image
2. optoelectronic physical frontend
3. hybrid backbone split into two pathways:
   - analog CIM path for static dense operators
   - digital path for control-heavy and dynamic operators
4. peripheral / calibration stage
5. classifier / output

The analog path should visually include:
- patch embedding
- QKV projections
- attention output projection
- MLP dense layers

The digital path should visually include:
- depthwise / MBConv style blocks
- QK^T
- AV
- softmax
- normalization / control

The peripheral block should show:
- ADC / DAC
- scale recovery
- profile-driven perturbations

At the bottom or side, include a subtle annotation that literature-derived or measured device profiles can be injected into the same workflow.

Important constraints:
- make it look like a high-end journal schematic, not a presentation slide
- keep text minimal and short
- use crisp rounded rectangles and arrows
- create strong separation between analog and digital paths
- show that dynamic attention remains digital
- do not include numeric values
- do not include paragraph-like text
```

## Prompt B: Fig.2 Weight Mapping / Behavioral Abstraction

```text
Create a publication-quality horizontal flow schematic for a paper on profile-driven analog weight mapping in organic compute-in-memory simulation.

The figure should show a left-to-right pipeline with about five clean stages:
1. FP32 weight tensor
2. split into positive and negative branches
3. map into bounded conductance window and quantized states
4. apply device-profile effects
5. differential readout plus digital scale recovery

The visual message should be:
- this is a behavioral abstraction for mapping weights into analog conductance
- it is profile-driven
- it supports noise, retention, and nonlinear-write stress
- it is not a pulse-accurate circuit diagram

Design requirements:
- white background
- minimal scientific text
- elegant arrows between stages
- a small secondary inset or subtle label for profile effects, such as:
  D2D, C2C, retention, proportional noise, nonlinear write
- no vertical stack
- no crowded wording
- no decorative 3D chip art
- use a clean journal schematic aesthetic
```

## Prompt C: Optional Story Figure - Materials To System Bridge

```text
Create a conceptual journal-style bridge schematic for a paper on organic optoelectronic CIM simulation.

The visual concept should explicitly show a bridge between:
- left side: partial device characterization / measured material properties
- center: profile-driven behavioral simulator
- right side: system-level deployment outcomes on edge vision models

Left side should visually suggest:
- multilevel conductance states
- variability
- retention
- photoresponse

Center should show:
- JSON-like device profile
- hybrid analog/digital simulation
- hardware-aware training / evaluation

Right side should show:
- CNN / Transformer deployment
- accuracy
- transferability
- energy

The goal is to communicate:
"device metrics alone do not answer deployment viability; the simulator provides the bridge."

Keep it high-end, minimal, and suitable for a journal introduction figure or graphical abstract.
```

## Prompt D: Optional Limitation / Bottleneck Hierarchy Figure

```text
Create a clean scientific infographic summarizing the bottleneck hierarchy for organic optoelectronic CIM deployment.

The figure should visually rank or separate:
- nominal quantization
- standard stochastic noise
- ADC precision
- fresh-instance transfer
- proportional state-dependent noise
- nonlinear write
- digital attention energy ceiling

The visual message should be:
- nominal quantization is not the dominant bottleneck
- deployment failure is driven more by converter precision, transferability, richer physics, and digital attention cost

Important:
- no fake measured numbers
- use relative emphasis by size, grouping, or hierarchy
- white background
- journal infographic style
- concise labels only
```
