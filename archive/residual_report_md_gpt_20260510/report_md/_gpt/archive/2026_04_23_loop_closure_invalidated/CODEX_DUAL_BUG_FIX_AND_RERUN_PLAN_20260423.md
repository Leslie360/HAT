# Codex Dual-Bug Fix And Minimal Rerun Plan (2026-04-23)

## Current code-state check
A direct inspection of the current working tree shows that both local implementation fixes are already present:

1. **Branch-swap fixed**
- `analog_layers.py`: `grad_output >= 0` now maps to `ltd_scale`, and `grad_output < 0` maps to `ltp_scale`.
- `analog_layers_ensemble.py`: same mapping.

2. **Second-order coefficient fixed**
- `analog_layers.py`: second-order correction now uses `-0.5 * (nl - 1.0) * ...`, i.e. no extraneous leading `nl` multiplier.

Therefore the project is not blocked on writing the fix itself. The real remaining work is:
- lock the corrected semantics with tests / provenance
- run the minimal post-fix rerun set
- avoid reusing any contaminated numbers from `K4R`, `P1-C`, or `P1-C2`

## Engineering judgment
The safest way to recover a canonical anchor is **not** to jump straight back into a 100-epoch SO2 run.
That would spend GPU before we re-establish a clean baseline under the newly fixed backward path.

The correct order is:

### Step 1 — Freeze and label contaminated results
Do this first, no GPU.
- `K4R`: invalid as canonical anchor
- `P1-C`: invalid as contaminated run
- `P1-C2`: invalid as contaminated run
- preserve as forensic logs only

### Step 2 — Lock semantics in code review / tests
Before any rerun, add or update tests so the following are explicit:
- positive gradient uses LTD scale
- negative gradient uses LTP scale
- second-order coefficient is `-0.5 * (nl - 1)`
- first-order remains no-multiplier

Without this, we risk drifting again under broadcast pressure.

### Step 3 — Run the smallest possible post-fix parity smoke
This is the first GPU step.
Goal: verify the corrected code is numerically sane before any long run.

#### Smoke A: first-order only
- `group=all`
- `use_second_order_ste = False`
- `epochs = 1`
- warm-start from `checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- expected use: establish clean epoch-0 / epoch-1 behavior

#### Smoke B: second-order on
- `group=all`
- `use_second_order_ste = True`
- `second_order_alpha = 0.25`
- `epochs = 1`
- same warm-start
- expected use: check whether corrected SO2 now behaves comparably in early source-domain training

Acceptance criterion:
- no crash
- no absurd epoch-0 collapse
- both produce sensible same-instance numbers in the low/mid 80s or better

If Smoke B still shows immediate pathological behavior, do not proceed to long SO2 reruns.

### Step 4 — Establish the new canonical anchor with first-order only
This is the minimal canonical rerun.

#### Canonical Rerun R1
- `group=all`
- **no SO2**
- full HAT training schedule
- 100 epochs
- warm-start from `V4_hybrid_standard_noise_hat_best.pt`
- then `10 x 5` fresh-instance eval

Reason:
- first-order no-multiplier semantics is the least disputed part of the stack
- it gives us one clean post-fix anchor without mixing in unresolved second-order value claims
- it directly answers whether the route itself (`group=all`, uniform path) still survives after both implementation bugs are removed

This rerun should become the first new authoritative post-fix anchor.

### Step 5 — Only then test second-order value-add
Only after R1 is complete.

#### Conditional Rerun R2
- same as R1 but with:
  - `use_second_order_ste = True`
  - `second_order_alpha = 0.25`

Purpose:
- measure whether corrected SO2 helps, hurts, or is neutral relative to the corrected first-order-only anchor

If R2 underperforms R1 materially on fresh-instance transfer, SO2 should be demoted to optional / diagnostic rather than mainline.

## What not to do
- Do not relaunch `K4R` immediately as the first rerun.
- Do not relaunch `P1-C2` as a canonical path.
- Do not let remote start anything before R1 exists locally.
- Do not update manuscript/rebuttal numbers from contaminated runs.

## Minimal decision tree
1. Confirm code fixes are present and tested.
2. Run 1-epoch Smoke A + Smoke B.
3. If both sane, run R1 (first-order-only full rerun).
4. After R1 finishes, decide whether R2 is worth GPU.

## Recommendation
My prioritized recommendation is:
1. **Do not spend GPU on SO2-first.**
2. **Use first-order-only `group=all` as the first clean rerun anchor.**
3. **Treat corrected SO2 as a follow-up comparison, not the first recovery experiment.**
