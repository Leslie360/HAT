# Gemini Dispatch — STE Semantics Ruling (2026-04-22)

## Scope
Theory only. No code patches. No remote queue planning.

## Goal
Issue a mathematical ruling on whether the first-order STE surrogate in this project should include a leading `nl` multiplier in the LTP/LTD scale.

## Inputs
- `analog_layers.py`
- `analog_layers_ensemble.py`
- current tests in `test_groupwise_nl_wrapper.py`
- methodology equations in paper/thesis files

## Deliverable
Write:
- `GEMINI_STE_SEMANTICS_RULING_20260422.md`

## Required sections
1. `Current code semantics`
2. `Equation-level derivation`
3. `Ruling: multiplier or no multiplier`
4. `Consequence for parity interpretation`

## Constraints
- One ruling only
- No ambiguity language unless the equations are genuinely underdetermined
- No route discussion beyond immediate consequence for interpreting existing parity numbers
