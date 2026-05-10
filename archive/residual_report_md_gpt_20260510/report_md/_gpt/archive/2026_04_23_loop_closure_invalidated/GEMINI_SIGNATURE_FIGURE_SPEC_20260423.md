# G-SLIM-2: Signature Figure Spec (Updated)
**Date:** 2026-04-23
**Scope:** Round Q SLIM (Empirically Updated post-CX-K2)

## 1. Concept
This is the signature figure for the thesis: "The High-Variance Structural Limit of Analog Attention." It visually communicates the massive stochastic spread of device-to-device (D2D) noise under severe non-ideality, and explicitly demonstrates the absence of bimodal attractors.

## 2. Layout & Data Mapping
**Main Plot: D2D Variance Scatter**
- **X-axis:** Hardware Instance Index (1 to 30), sorted by accuracy.
- **Y-axis:** Fresh-Instance Accuracy (%).
- **Data Points:** Scatter plot of the N=30 instances from CX-K2.
- **Color Coding:** A continuous colormap (e.g., Viridis or Magma) based on the Y-value, demonstrating a continuous slide from 22% to 61% rather than two discrete clusters.
- **Horizontal Lines:** A solid red line for the mean (38.95%), with a shaded error band (±9.85%) illustrating the massive standard deviation.

**Right Panel: Marginal KDE (Kernel Density Estimate)**
- **Y-axis:** Aligned with the main plot's Y-axis (Fresh-Instance Accuracy).
- **X-axis:** Density.
- **Visualization:** A filled KDE curve showing a **single, extremely broad and flat peak** (unimodal), with an annotation pointing out "Hartigan's Dip $p=0.98$ (Unimodal)" to mathematically seal the structural limit argument.

## 3. Instruction for Codex
Plot the figure using the actual `cx_k2_bimodality_test.json` data according to this updated unimodal specification.
