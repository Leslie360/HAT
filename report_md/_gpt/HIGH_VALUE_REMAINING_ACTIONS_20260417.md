# High-Value Remaining Actions

## Current Status

- `NL=1.5` Tiny-ViT interpolation rerun is complete:
  - log: `logs/_gpt/train_tinyvit_v4_nl_interp15_20260417_022400_gpt.log`
  - result: `best_acc=19.01% @ epoch 1`, `final_test_acc=9.76%`
  - judgment: rebuttal-side only; it does not provide a manuscript-clean intermediate anchor
- The stricter layer-wise ADC non-ideality sweep is complete and already manuscript-integrated.
- The nonlinear-write gradient-distortion diagnostic is complete and already manuscript-integrated in supplementary form.

## Worth Doing Now

### 1. `NL=1.5` rerun is now resolved

**Why it matters**

- It directly addresses the strongest remaining technical critique on the `NL=2.0` boundary: the paper currently shows one severe point and needs an interpolation anchor.
- This is cleaner evidence than speculative layer-wise NL commentary.

**Decision rule**

- The rerun finished near-collapse and did not yield a stable interpolation anchor.
- Keep the result rebuttal-side and preserve the current manuscript wording.

### 2. ADC hook-based analysis is now complete

**Why it matters**

- The old logit-level ADC script was too weak for manuscript use.
- The new hook-based full-test sweep is now complete and already integrated into the supplementary evidence package.
- It gives a cleaner hierarchy:
  - offset: nearly negligible
  - gain: small degradation
  - INL: more sensitive
  - realistic combined errors: no collapse
  - pessimistic errors: moderate but not catastrophic degradation

**Decision rule**

- No further ADC rerun is needed unless a reviewer asks for a different architecture or a larger ADC error range.

### 3. Deeper nonlinear-write follow-up is now complete

**Why it matters**

- The full-test ADC sweep is already done.
- The remaining pressure point was nonlinear write.
- A new group-wise gradient-distortion diagnostic is now complete:
  - `MLP` blocks dominate the present `NL=2.0` surrogate failure (`affected-gradient cosine = 0.815`, norm ratio `0.671`)
  - `Patch Embed`, `Attention QKV`, and `Attention Proj` remain effectively unchanged (`1.00`)
  - forward loss remains unchanged, confirming a backward-surrogate mechanism rather than a forward mismatch

**Decision rule**

- `NL=1.5` also finished near-collapse.
- Keep the new gradient diagnostic as the mechanistic explanation and avoid launching broader nonlinear-write sweeps unless a reviewer explicitly asks for them.

## Low-Value Work Right Now

### 1. More CrossSim / AIHWKIT sweeps

- Current shared-regime sanity checks are already sufficient for scope framing.
- Additional phases are unlikely to shift the editorial outcome as much as the `NL=1.5` anchor would.

### 2. More wording-only edits to the manuscript front matter

- The current abstract, discussion, and cover letter already frame the work as first-order behavioral simulation rather than chip prediction.
- More softening now gives diminishing returns.

### 3. New broad architecture / task expansion without real device data

- This would cost significant time and still not answer the main reviewer pressure points.
- It risks reopening scope instead of closing it.

## Recommended Order

1. Keep the current manuscript text and supplementary NL gradient diagnostic as the locked package.
2. Use the finished `NL=1.5` rerun only as response-side evidence of training-recipe instability.
3. Do not spend more GPU budget on broader nonlinear-write sweeps unless an actual reviewer explicitly demands them.
