# Final Alignment Checklist — 2026-04-17

## Scope

Final consistency check across:

- [main.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.tex)
- [00_abstract.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/00_abstract.tex)
- [07_conclusion.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/07_conclusion.tex)
- [cover_letter.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/cover_letter.tex)

## Title

- Main title: `Profile-Driven Hardware Simulation for Organic Optoelectronic Edge Vision`
- Cover-letter submission line: matches exactly

Status: `aligned`

## Framework Positioning

Checked for these phrases:

- `first-order behavioral`
- `prospective simulation` / `simulation-based`
- `decision aid`
- `not a chip-predictive emulator`

Final state:

- Abstract: `profile-driven first-order behavioral simulation framework`
- Conclusion: `first-order behavioral simulation framework` and `materials-to-system decision aid`
- Cover letter: `prospective first-order behavioral simulation study` and `decision aid rather than ... chip-predictive emulator`

Status: `aligned`

## Core Locked Results

Checked for consistent presence of:

- fresh-instance collapse to `10.00%`
- Ensemble HAT recovery to `86.37 ± 1.54%`
- OPECT zero-shot `88.53%`
- severe nonlinear write `27.72 ± 0.82%`

Final state:

- Abstract: all four present
- Conclusion: three key manuscript-facing results present; OPECT `88.53%` retained
- Cover letter: all four present

Status: `aligned`

## OPECT Case Framing

Target wording:

- `literature-anchored case study`
- avoid `validation`

Final state:

- Abstract: `literature-anchored 2025 OPECT case study`
- Conclusion: `literature-anchored OPECT case study`
- Cover letter: `literature-anchored OPECT case study`

Status: `aligned`

## Energy Claim Boundaries

Target wording:

- energy numbers are `first-order system-level upper bounds`
- not chip-predictive

Final state:

- Discussion: explicit upper-bound caveat retained
- Cover letter: explicit upper-bound caveat retained

Status: `aligned`

## Residual Risk

One known manuscript-wide caveat remains outside this four-file check:

- Tiny-ViT CIFAR-10 FP32 baseline is still presented as `98.06%` in the main-results baseline table/text, while the canonical lock file separately preserves `97.48%` for another statistic family. This is already documented in the TX-14 provenance trail and was intentionally left unchanged in this pass.

Status: `known and tracked`

## Outcome

For title / abstract / conclusion / cover-letter alignment, the package is now internally consistent and reviewer-facing wording is appropriately conservative.
