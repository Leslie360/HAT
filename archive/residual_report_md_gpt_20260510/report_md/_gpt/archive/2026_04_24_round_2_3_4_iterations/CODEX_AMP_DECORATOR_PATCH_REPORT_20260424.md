# Codex AMP Decorator Patch Report

Date: 2026-04-24
Task: R3-4 from `DISPATCH_CODEX_ROUND3_PATCHES_20260424.md`
Owner: Codex

## Verdict

R3-4 AMP decorator patch is complete.

This is a future-proofing patch only. Current M-series severe-NL numbers are unaffected because they were produced outside AMP-sensitive training and were already locked before this change.

## Patch

Files changed:

| File | Change |
|:--|:--|
| `analog_layers.py` | Added `torch.amp.custom_fwd/custom_bwd` decorators to `StraightThroughQuantize`; forces CUDA autocast inputs to fp32 in `forward`; computes STE backward pow paths in fp32. |
| `test_groupwise_nl_wrapper.py` | Added CUDA AMP regression test for a small `AnalogLinear` forward/backward at `NL=2.0` with second-order STE enabled. |
| `test_dual_bug_fix.py` | Updated the source-scan assertion to recognize the new `grad_output_fp32` variable name in the second-order correction line. |

Key code locations:

| Location | Purpose |
|:--|:--|
| `analog_layers.py:32` | imports `custom_fwd`, `custom_bwd` from `torch.amp` |
| `analog_layers.py:186` | `@custom_fwd(device_type=\"cuda\", cast_inputs=torch.float32)` |
| `analog_layers.py:230` | `@custom_bwd(device_type=\"cuda\")` |
| `analog_layers.py:233-265` | backward uses `grad_output_fp32` and `x_clamped_fp32` for ratio/pow calculations |
| `test_groupwise_nl_wrapper.py:119` | `test_ste_under_amp_no_nan` |

## Validation

Commands run:

```bash
/home/qiaosir/miniconda3/bin/python test_dual_bug_fix.py
/home/qiaosir/miniconda3/bin/python test_groupwise_nl_wrapper.py
```

Results:

| Test | Result |
|:--|:--|
| `test_dual_bug_fix.py` | `All 7 tests passed` |
| `test_groupwise_nl_wrapper.py` | `Ran 9 tests ... OK` |

The new AMP regression executed on CUDA and verified finite input, weight, and bias gradients.

## Impact

- No training or fresh-eval was launched.
- No M-series result is changed.
- Non-AMP fp32 behavior remains covered by existing branch-swap, no-extra-NL-multiplier, second-order mapping, `NL=1.5` guard, and groupwise config-copy tests.

## Remaining R3 Patch Item

R3-3 Stage 1 remains: per-instance ADC calibration patch + unit test. Stage 2 M-series re-eval remains gated by Claude/user signal or 8x40GB remote return.
