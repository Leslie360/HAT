# CLAUDE Stop-Loss Synthesis Template
**Date:** 2026-04-23
**Scope:** Post Dual-Bug Synthesis Prep

## What failed
- K4R and all previous severe-NL runs (J1d, K2, K3, etc.) collapsed or gave false signals due to the dual-bugs (branch swap and wrong coefficient/sign) in the physical surrogate.

## What remains valid
- The framework architecture, V4 baseline (NL=1.0), and the theoretical mathematical derivation of the surrogate constraints.

## What is now frozen
- Codebase physics in `analog_layers.py`. No further theoretical tweaking is allowed until the minimal rerun provides empirical grounding.
- All paper drafting is frozen.

## Minimal fix set
- Atomic commit containing: 1) `grad_output >= 0` mapped to `ltd_scale`; 2) removal of `nl` multiplier in second-order coefficient; 3) negative sign for both LTP/LTD second-order correction.

## Minimal rerun set
- A clean first-order-only run (`group=all`, no SO2) to serve as the absolute baseline.
- Followed by a corrected SO2 run to compare the true effect of the physical brake.

## Manuscript / rebuttal wording consequences
- The narrative of a "structural limit" or "bimodal basin" must be completely re-evaluated based on the clean rerun. If the fixed engine solves the collapse, the narrative pivots back to successful mitigation. If it still collapses, the physical limit narrative is restored, but with correct provenance.
