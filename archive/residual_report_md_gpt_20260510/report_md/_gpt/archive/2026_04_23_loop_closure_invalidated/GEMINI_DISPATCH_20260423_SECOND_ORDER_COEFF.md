# Gemini Dispatch — Second-Order Coefficient Ruling (2026-04-23)

## Context
Branch A has already ratified first-order no-multiplier semantics.
That question is closed.

The only theory item still open is the second-order coefficient currently used in code:
- code uses `-0.5 * nl * (nl - 1) * ...`

There is still ambiguity whether the intended coefficient should instead be:
- `-0.5 * (nl - 1) * ...`

## Your task
Produce one decisive ruling on the second-order coefficient.

## Deliverable
Create exactly one file:
- `GEMINI_SECOND_ORDER_COEFFICIENT_RULING_20260423.md`

## Required contents
1. Statement of the exact surrogate being expanded
   - define the first-order scale function explicitly
   - do not hand-wave from physical power-law unless you map it back to the implemented surrogate

2. Derivation
   - derive the Taylor correction for the actual implemented scale function
   - make explicit whether the coefficient is:
     - `nl*(nl-1)`
     - `(nl-1)`
     - or something else

3. Code verdict
   - say whether current code in `analog_layers.py` is:
     - correct
     - partially correct
     - incorrect

4. Consequence for K4R
   - say whether the currently running K4R should be treated as:
     - canonically valid
     - provisionally valid pending rerun
     - invalid and must rerun

5. One-sentence operational recommendation
   - precise and binary

## Inputs you must inspect
- `analog_layers.py`
- `analog_layers_ensemble.py`
- `GEMINI_STE_SEMANTICS_RULING_20260422.md`
- `BROADCAST_BRANCH_A_SCRUB_COMPLETE_20260423.md`

## Hard rules
- Do not revisit first-order multiplier arbitration.
- Do not speculate about remote environment bugs.
- Do not queue new experiments.
- One ruling only.
