# R11D-4 PCM Paper Integration — Executive Summary

## Overview
R11D-4 PCM (phase-change memory) device-model results have been fully integrated into the manuscript across four LaTeX files, compiled cleanly, and verified against all locked-number and banned-wording guards.

## What Changed

| File | Edit | Key Content |
|------|------|-------------|
| `05_results.tex` | New subsection `\subsec{pcm-realism}` | ~95 words. Reports PCM training best **61.10%**, fresh eval **60.85 ± 0.17%**, drift stable within **±0.3 pp** (60.83% → 61.07% → 60.56%), and the **~26 pp** gap to the R10E IdealDevice baseline. Frames pulse-update fidelity as a distinct bottleneck alongside ADC precision and D2D mismatch. |
| `supplementary.tex` | New table `tab:pcm-comparison` | 3-row table comparing AIHWKit IdealDevice 8-bit, AIHWKit PCM 8-bit, and Ensemble HAT 4-bit on Training Best, Fresh Mean, Fresh Std, and Drift Impact. Cites `rasch2021aihwkit`. |
| `06_discussion.tex` | Extended AIHWKit paragraph | 4 sentences adding PCM pulse-update physics as an orthogonal penalty (~26 pp gap, stable drift, distinct from mismatch/variability). |
| `cover_letter.tex` | +1 sentence (~30 words) | Frames PCM non-linearity as a ~26 pp penalty independent of the mismatch-variability axis. |

## Verification Status

| Check | Result |
|-------|--------|
| `main.tex` compile | RC 0, **16 pages**, 494 KB |
| `supplementary_main.tex` compile | RC 0, **40 pages** |
| Undefined references | **0** (both main & supp) |
| Multiply-defined labels | **0** (both main & supp) |
| Word count (main body) | **4,188 / 5,700** |
| Banned wording scan | **Clean** |
| Locked numbers guard | **22 / 22 passed** |

## Narrative Integrity
- PCM results are reported honestly (61.10% training, 60.85% fresh) with no overclaiming.
- The "orthogonal penalty" framing keeps PCM non-linearity separate from D2D mismatch and ADC precision, avoiding conflated causality.
- All prior multi-agent critiques (eval-config accuracy, stale-baseline correction, avoidance of blanket superiority claims) have been addressed.

## Bottom Line
The manuscript now contains a complete, verified PCM realism section that closes the R11D-4 milestone. The paper compiles cleanly and remains well within length limits.
