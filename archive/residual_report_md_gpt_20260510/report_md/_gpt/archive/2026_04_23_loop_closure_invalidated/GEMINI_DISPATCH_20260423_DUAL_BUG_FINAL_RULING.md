# Gemini Dispatch — Dual-Bug Final Ruling (2026-04-23)

## Context
Two implementation questions are now active together:
1. second-order coefficient (`nl*(nl-1)` vs `(nl-1)`)
2. gradient-to-update branch mapping (`grad_output` sign routed to LTP/LTD scales)

`Kimi` has elevated branch-swap to verified local code-review status.

## Deliverable
Create exactly one file:
- `GEMINI_DUAL_BUG_FINAL_RULING_20260423.md`

## Required contents
1. Define the actual update variable and sign convention under SGD/Adam.
2. State whether `grad_output >= 0` should map to LTP or LTD scale.
3. State the correct second-order coefficient once the mapping is fixed.
4. Give one final canonical backward form in pseudocode.
5. State whether both fixes should land in one commit or sequentially.
6. State the minimal canonical rerun after the fixes.

## Inputs you must inspect
- `analog_layers.py`
- `analog_layers_ensemble.py`
- `GEMINI_SECOND_ORDER_COEFFICIENT_RULING_20260423.md`
- `GEMINI_RE_DERIVATION_BRANCH_SWAP_20260423.md`
- `BROADCAST_KIMI_BRANCH_SWAP_VERIFIED_20260423.md`

## Hard rules
- One final ruling only.
- No new broad experiment tree.
- No manuscript prose.
