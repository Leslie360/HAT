# DISPATCH CODEX-ROUND3-PATCHES — AMP Decorators + Per-Instance ADC Recalibration
**Date:** 2026-04-24 22:30 CST
**Issued by:** Claude
**Assignee:** Codex
**Depends on:** CLAUDE_ROUND2_CLOSURE_RULING §2 R3-3, R3-4
**Priority:** LOW (both items; opportunistic timing)
**Time budget:** ~1 hour total code + ~3 GPU-h re-eval (gated)

---

## Part A — AMP decorators (R3-4)

### A.1 Scope

Per Gemini G-AUDIT-CODE residual finding (§3.3): `StraightThroughQuantize` lacks `@torch.cuda.amp.custom_fwd` / `custom_bwd` decorators. Under AMP mixed precision, `eps=1e-8` in critical pow regions can underflow to 0 in float16.

Current impact: NIL because AMP is disabled in current training. Future-proofing only.

### A.2 Patch

- File: `analog_layers.py`, class `StraightThroughQuantize`
- Add decorators:
  ```python
  from torch.cuda.amp import custom_fwd, custom_bwd
  
  class StraightThroughQuantize(torch.autograd.Function):
      @staticmethod
      @custom_fwd
      def forward(ctx, ...):
          ...
      
      @staticmethod
      @custom_bwd
      def backward(ctx, ...):
          ...
  ```
- Ensure all `pow()` operations in forward/backward are upcast to fp32 regardless of AMP state

### A.3 Test

Add regression test in `test_groupwise_nl_wrapper.py`:
```python
def test_ste_under_amp_no_nan():
    """Regression: AMP-enabled forward + backward must not produce NaN/Inf."""
    with torch.cuda.amp.autocast():
        # Small AnalogLinear forward + backward at NL=2.0
        # Assert no NaN/Inf in gradient
        ...
```

Also confirm existing tests still pass (7/7 + 8/8).

### A.4 Deliverable

`CODEX_AMP_DECORATOR_PATCH_REPORT_20260424.md` with:
- Patch file:line
- Test results
- Confirmation existing NL=2.0 M-series results unaffected

### A.5 Timing

Fire when GPU idle. ~10 min code + ~5 min tests.

---

## Part B — Per-instance ADC recalibration (R3-3)

### B.1 Scope

Per Gemini G-AUDIT-ADC-HOOK §3.7 FAIL: `eval_fresh_instances_adc_ablation.py` calibrates ADC ranges **once** on the ideal pre-noise array, then applies static range across all 10 fresh D2D instances. Each physical instance has a different output range due to D2D mismatch, so static calibration induces artificial clipping.

Expected effect of fix: +0.2 to +0.8 pp recovery on severe-NL ADC-on fresh numbers.

### B.2 Patch

- File: `scripts/_gpt/eval_fresh_instances_adc_ablation.py`, around lines 65, 75
- Move `calibrate_adc_ranges(...)` call **inside** the `for instance_idx in range(num_instances):` loop
- Each fresh instance reseeds D2D, then recalibrates ADC range on that specific noisy array, then evaluates

### B.3 Test

Before firing real eval:
- Unit test: confirm per-instance range differs across 3 synthetic D2D realizations (sanity check)
- Confirm calibration still converges in reasonable time (~1-2s per instance)

### B.4 GATED: Re-eval M-series

**DO NOT re-run immediately.** This is gated on:
1. R3-3 priority in queue (LOW)
2. No conflict with 8×40GB remote cross-arch returning with measured-D2D integration needs
3. User signal OR Claude explicit go-ahead

When fired:
- Re-run ADC-on 8-bit on M1..M6 with per-instance recalibration
- 6 checkpoints × 10 instances × 5 MC = ~3-4 GPU-h total
- Produce `CODEX_MSERIES_ADC_DUAL_REPORT_PER_INSTANCE_CAL_20260424.md` with:
  - New ADC-on 8-bit numbers with per-instance calibration
  - Delta vs static-calibration numbers
  - Update main dual-column CSV

### B.5 Deliverable (Part B)

Two-stage delivery:
- Stage 1 (code patch + unit test, fire now): `CODEX_ADC_PERINSTANCE_CAL_PATCH_20260424.md`
- Stage 2 (re-eval, gated): new ADC-on dual report

Kimi notifies via AGENT_SYNC when reruns are desired for thesis/paper integration pass.

### B.6 Timing

- Stage 1: opportunistic (GPU idle, 30 min code + test)
- Stage 2: on signal only

---

## Part C — NOT doing

- No changes to training path (ADC still off per D1 decision)
- No changes to hook core logic (only the eval script calling pattern)
- No new experiments beyond re-running existing ADC ablation with fixed calibration

---

## Sequencing

1. Fire Part A (AMP decorators) as soon as next GPU-idle window
2. Fire Part B Stage 1 (per-instance cal patch + unit test) in parallel with Part A
3. Stage 2 waits for signal

---

## Success criteria

- Part A: zero AMP-related NaN/Inf in any test, existing results bit-exact unchanged
- Part B Stage 1: patched script has per-instance calibration, unit test confirms different ranges per instance
- Part B Stage 2 (when fired): ADC-on 8-bit recovers by the expected +0.2 to +0.8 pp, headline numbers in §5.7 bump up slightly, narrative unchanged
