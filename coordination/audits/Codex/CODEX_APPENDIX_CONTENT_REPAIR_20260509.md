# Codex Appendix Content Repair — 2026-05-09

## Scope

Gemini visual editing is stopped. Codex took over supplementary content-level repair only. Main-text figures were not touched.

Edited files:

- `paper/latex_gpt/supplementary.tex`
- `paper/latex_gpt/supplementary/S_tooling_comparison.tex`
- `paper/latex_gpt/supplementary/S_mechanism_empirical.tex`
- `paper/latex_gpt/supplementary/fig_late_recovery_tikz.tex`
- Rebuilt `paper/latex_gpt/supplementary_main.pdf`

## Changes

### 1. PCM 6-bit stale-data repair

- Retired the old 6-bit canonical table based on the obsolete training-time protocol.
- Replaced the 6-bit table with corrected new-protocol fresh values:
  - seed123: `68.93 ± 0.03%`, 1d drift `68.98%`, drift delta `-0.05 pp`
  - seed456: best `62.60%`, fresh `62.47 ± 0.06%`, drift pending
  - seed457: best `76.63%`, fresh `76.69 ± 0.05%`, drift pending
  - seed789: best `65.86%`, fresh `66.13 ± 0.04%`, drift pending
  - four-seed fresh mean: `68.55%`, seed std `6.03 pp`
- Reframed 6-bit as a D2D-sensitive transition regime, not a frontier optimum.
- Kept 4-bit and 8-bit canonical tables unchanged.

### 2. 5-bit kill visibility

Added an explicit supplementary note that strict 5-bit PCMPresetUnitCell reached only `63.44 ± 0.07%` fresh accuracy with `2.52 pp` one-day drift drop, below the 70% continuation gate. It is now visible as non-frontier rather than silently omitted.

### 3. Retired old late-recovery figure

- Removed the old 6-bit late-recovery figure from active supplementary content.
- Replaced the subsection with a text-only correction explaining that the old diagnostic used the obsolete protocol.
- Converted `fig_late_recovery_tikz.tex` into a retired placeholder to prevent accidental reuse of stale values.

### 4. Provenance repair

Updated 6-bit provenance rows:

- `r11d_6bit_pcm_seed123` — new protocol, history missing
- `r11d_6bit_pcm_seed456` — new protocol, best epoch 30
- `r11d_6bit_pcm_seed457` — new protocol, best epoch 100
- `r11d_6bit_pcm_seed789` — new protocol, best epoch 44

Removed the stale `r11d_6bit_pcm_seed456_full100` active provenance row.

### 5. Reviewer-risk repairs outside PCM table

- CrossSim note now states the 14.4 pp gap is a convention mismatch and not an apples-to-apples superiority claim.
- D2D interpolation caption now marks alpha>1 as extrapolated beyond the training distribution.
- Hessian section now explicitly frames global Hessian flatness as a negative control, with D2D-directional interpolation as the relevant metric.
- CKA section now clarifies that 0.455 is an internal intermediate-similarity result, not a universal baseline.

## Verification

Commands run:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex
pdftotext supplementary_main.pdf - | rg "77\.86|77\.88|77\.83|77\.76|78\.49|Pareto midpoint|best observed Pareto|critical Pareto|6-bit midpoint|seed456_full100|r11d_6bit_pcm_seed456_full100"
```

Results:

- `supplementary_main.pdf` rebuilt successfully.
- PDF length: 39 pages.
- No stale old 6-bit values or old midpoint phrases found in generated PDF text.
- LaTeX log has one harmless `Underfull \hbox` warning; no fatal errors or undefined references remain.

## Remaining Dependencies

- Kimi still needs to close new-protocol 6-bit drift for seeds 456/457/789.
- Main-text stale PCM wording and cover letter remain separate tasks; Codex did not touch them in this appendix-only pass.
