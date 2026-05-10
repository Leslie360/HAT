# Codex LaTeX Integration Audit — 2026-05-01

Reviewer: Codex
Scope: local verification of Gemini's reported LaTeX integration and guard pass.

## Executive Verdict

**Technical compile: passes. Content integration: fails.**

Gemini correctly integrated the new precision-ladder content into `sections/05_results.tex` and `supplementary.tex`, and the locked-number guard passes. However, the paper is not architecturally consistent yet. Abstract, Introduction, Discussion, and Conclusion still carry the older organic/OPECT/NL=2.0 narrative, while Results now follows the acting-architect ruling: pure 4-bit failure + Ensemble HAT rescue + PCM 4/6/8-bit precision ladder.

Do not declare Paper-1 structurally complete until the stale sections are rewritten.

## What Passed

### Locked-number guard

Command:

```bash
python scripts/_gpt/check_locked_numbers.py
```

Result: `22/22 passed`.

Relevant locked values confirmed:

- Ensemble HAT 3-seed: 86.16%
- AIHWKit 8-bit: 87.28%
- AIHWKit 4-bit: 14.64%

### Compile/log status

Current logs show:

- `main.pdf`: generated, 13 pages.
- `supplementary_main.pdf`: generated, 40 pages.
- No local grep hits for undefined references/citations or fatal LaTeX errors in the inspected logs.

### Results section

`paper/latex_gpt/sections/05_results.tex` now includes:

- AIHWKit 8-bit `87.28 ± 0.13%`.
- AIHWKit 4-bit `14.64 ± 0.11%`.
- Ensemble HAT 4-bit `86.16 ± 0.19%`.
- PCM UnitCell precision ladder: 8-bit / 6-bit / 4-bit.
- 107 only as one future-work sentence.

This section is broadly aligned with the acting-architect ruling.

## Blocking Content Failures

### 1. Abstract still follows old organic/OPECT/NL=2.0 story

File: `paper/latex_gpt/sections/00_abstract.tex`
Line: 3

The abstract still frames the paper as:

- profile-driven organic optoelectronic CIM inference;
- ADC cliff;
- OPECT zero-shot transfer;
- severe nonlinear write `NL=2.0` recovery to 80-82%;
- residual gap to digital baseline.

This does not match the new paper-1 spine. The abstract must be rewritten around:

1. AIHWKit pure 4-bit failure (`14.64 ± 0.11%`).
2. Ensemble HAT rescue (`86.16 ± 0.19%`).
3. PCM UnitCell 4/6/8-bit precision ladder.
4. 6-bit as best tested Pareto midpoint.
5. 4-bit as trainable but drift-limited.

### 2. Introduction still declares old contribution list

File: `paper/latex_gpt/sections/01_introduction.tex`
Lines: 5-11

Current contributions are still:

- organic optoelectronic CIM framework;
- ADC cliff;
- inverse-gamma front-end compensation;
- OPECT profile;
- severe nonlinear write.

This conflicts with the final ruling. The introduction must be rewritten or minimally re-scoped so that the contribution list includes the new AIHWKit/PCM precision ladder. If old OPECT/ADC/front-end work remains, it must become background/supporting evidence, not the main contribution list.

### 3. Discussion contains stale, wrong PCM result

File: `paper/latex_gpt/sections/06_discussion.tex`
Line: 48

Current text says:

```text
Training with AIHWKit's PCMPresetUnitCell under AnalogSGD recovers only 61.10%, leaving a ~26 pp gap...
```

This is now invalid. The canonical PCM UnitCell numbers are:

- 8-bit fresh: `77.5953 ± 0.6392%`.
- 6-bit fresh: `77.8611 ± 0.5639%`.
- 4-bit fresh: `76.6836 ± 0.3737%`.

The discussion must replace the stale 61.10% paragraph with the precision-ladder interpretation.

### 4. Conclusion still follows old framework story

File: `paper/latex_gpt/sections/07_conclusion.tex`
Lines: 5-9

The conclusion still emphasizes:

- profile-driven organic optoelectronic simulation;
- ADC cliff;
- OPECT zero-shot transfer;
- severe nonlinear write.

It does not conclude the new precision-ladder story. Rewrite required.

### 5. Supplement still contains stale AIHWKit PCM 8-bit 61.10% table row

File: `paper/latex_gpt/supplementary.tex`
Line: 678

Current row:

```text
AIHWKit PCM 8-bit ... 61.10 ...
```

This appears to be an older diagnostic/result and conflicts with the current canonical PCM precision-ladder table. It must be either removed, marked diagnostic/non-canonical, or replaced with canonical 4/6/8-bit UnitCell results.

## Non-Blocking Notes

- `supplementary/S_energy_provenance.tex` still uses phrase `before tape-out`, but as a caveat about design-space exploration rather than a claim of tape-out readiness. Acceptable but should be reviewed in final wording pass.
- `supplementary.tex` still contains old OPECT/front-end/NL sections. These may remain as SI only if the main text clearly repositions them as supporting or legacy non-ideality analyses. They must not dominate the main narrative.

## Required Fix Plan

Priority order:

1. Rewrite `sections/00_abstract.tex` around the new spine.
2. Rewrite `sections/01_introduction.tex` contribution paragraph around the new spine.
3. Replace stale PCM paragraph in `sections/06_discussion.tex`.
4. Rewrite `sections/07_conclusion.tex` to close on precision ladder / deployment frontier.
5. Clean or annotate stale `AIHWKit PCM 8-bit 61.10` row in `supplementary.tex`.
6. Re-run:
   - `python scripts/_gpt/check_locked_numbers.py`
   - LaTeX compile for `main.tex` and `supplementary_main.tex`
   - grep for undefined refs/citations and forbidden/unsafe phrases.

## Final Status

Current status: **compile-safe but narrative-inconsistent**.

Gemini's integration is not ready for final acceptance. It must undergo a cross-section narrative consistency repair before manuscript-level signoff.
