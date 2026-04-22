# G-GG17: Rewrite Decision Tree
**Date**: 2026-04-20
**Trigger**: Awaits CX-J1b/c/d closure

## Tree
1. **IF** CX-J1c (Full-linear attention) recovers >80% **AND** CX-J1b (QKV-only) recovers >80%:
   -> **Path A**: The problem is strictly in the attention block. Structural hypothesis CONFIRMED.
2. **IF** CX-J1d (Higher-order) recovers >80%:
   -> **Path B**: The problem was our 1st-order surrogate. Structural hypothesis FALSIFIED. Surrogate-fidelity hypothesis CONFIRMED.
3. **IF** all remain <40%:
   -> **Path C**: Deep fundamental mismatch across all blocks at NL=2.0. Severe physical limit.
