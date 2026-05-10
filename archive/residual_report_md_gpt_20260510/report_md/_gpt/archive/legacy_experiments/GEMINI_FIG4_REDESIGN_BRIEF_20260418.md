# GEMINI FIG4 REDESIGN BRIEF — 2026-04-18

**Reread of canonical state:** I have re-read `paper/latex_gpt/sections/05_results.tex`, specifically noting the caption for Figure 4: *"Cross-dataset accuracy under canonical deployment (4-bit quantization, 5% C2C, 10% D2D variability). Error bars denote $\pm 1$ standard deviation where Monte Carlo (MC) statistics are available; bars without visible error bars indicate deterministic baselines or currently available point estimates."*

## 1. Current Fig 4 Panel Inventory
Figure 4 serves as the headline baseline and noise-resilience summary chart. Based on the manuscript text and CANONICAL_RESULT_LOCK, the data composition is:
- **Digital FP32 Baselines:** ResNet-18, ConvNeXt-Tiny, Tiny-ViT (Deterministic, no error bars).
- **V2 Zero-Noise Hybrid Control:** Deterministic evaluation ($n=10$ runs yield identically $97.39\pm0.00\%$, visually no error bar).
- **Noisy Canonical (V3/V4, C3/C4, R3/R4):**
  - Tiny-ViT V4: Has 3-seed / 10-MC statistics ($87.95 \pm 0.27\%$). Has error bars.
  - ConvNeXt C4: Has 3-seed statistics ($84.75 \pm 0.72\%$). Has error bars.
  - ResNet-18 R4: Likely a single-seed point estimate based on the caption caveat. Lacks error bars.

Mixing standard-deviation error bars with raw point estimates in a single clustered bar chart is a known reviewer trigger for "sloppy statistics" (PAPER_REVIEW D13).

## 2. Redesign Options
### Option A: Split-Panel Restructuring
Split Figure 4 into two distinct subpanels (`fig4a` and `fig4b`).
- **Fig 4a (Idealized / Deterministic):** Groups the FP32 digital baselines and the zero-noise hybrid controls. The y-axis can be tightened to $[90, 100]\%$.
- **Fig 4b (Canonical Noisy Deployment):** Groups only the runs subjected to analog C2C/D2D noise (the V4/C4/R4 set).
- **Pros:** Completely sidesteps the visual confusion of missing error bars; groups data logically by evaluation type.
- **Cons:** If ResNet-18 R4 is still a single seed, Fig 4b will *still* mix error-bar and bar-less data unless R4 is re-run.

### Option B: Unified Panel with Visual Semantic Marking
Keep the single clustered bar chart but alter the matplotlib aesthetics.
- **Design:** Use solid, filled bars with error caps for all MC-quantified data (Tiny-ViT, ConvNeXt). Use hatched or hollow bars for deterministic or single-seed point estimates (FP32, ResNet R4).
- **Caption Update:** Explicitly map the texture to the statistical rigor: *"Filled bars denote 3-seed Monte Carlo distributions ($\pm 1 \sigma$); hatched bars denote deterministic architectures or single-seed estimates."*
- **Pros:** Very fast to implement (matplotlib styling change only); preserves horizontal space in a page-constrained manuscript.
- **Cons:** Still visually highlights the missing statistical rigor on ResNet-18.

## 3. Recommendation
**Recommend Option B.** Given that the NC paper is strictly locked to 14 pages main-text, introducing a two-panel layout for Figure 4 will stretch the float environment and disrupt the tightly packed `05_results.tex` layout. Marking the deterministic/single-seed runs with hatches is a standard, reviewer-accepted visualization technique that directly answers the "where are the error bars?" question without requiring a layout overhaul. (However, the ultimate fix is for Codex to actually compute the 5-seed statistics for ResNet-18, fulfilling the Exp 4 protocol).

## 4. Implementation Cost
- **Target Script:** `paper/plot_paper_figures.py` (specifically the function generating `fig4_accuracy_comparison.pdf`).
- **Action:** Add a `hatch='//'` argument to the `ax.bar()` calls for the specific dataset/model combinations that lack a `"std"` key in the underlying JSON.
- **Cost:** ~30 minutes of Python matplotlib editing (Codex). No new GPU training required. Re-generation of the PDF and `main.tex` recompile takes $< 5$ minutes.
