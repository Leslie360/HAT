# CODEX NL Guard Patch Report

- Date: 2026-04-24
- Base HEAD: `33bed9cbb8ade7676d71074490ad45e68347950e`
- Worktree state: dirty, patch uncommitted

## Patch

- File: [analog_layers.py](/home/qiaosir/projects/compute_vit/analog_layers.py#L263)
- Change: disabled second-order correction for `1 < NL < 2` in `StraightThroughQuantize.backward`.
- Rationale: for `NL < 2`, exponent `(NL - 2)` is negative, so `pow(eps, NL - 2)` explodes near conductance bounds and can generate numerically unsafe gradients.

## Testability Cleanup

- File: [eval_fresh_instances_postfix.py](/home/qiaosir/projects/compute_vit/eval_fresh_instances_postfix.py#L79)
- Change: moved `inference_analysis_utils` import inside `evaluate_on_fresh_instances()`.
- Reason: `test_dual_bug_fix.py` only needs `resolve_eval_overrides`; it should not fail at import time because optional runtime dependencies such as `torchvision` are absent from the plotting/test environment.

## Validation

- `test_dual_bug_fix.py`: passed, `All 7 tests passed!`
- `test_groupwise_nl_wrapper.py`: passed, `Ran 8 tests ... OK`
- New regression covered:
  - `test_nl_1p5_no_gradient_explosion()`
  - Asserts finite gradients and bounded magnitude for `NL=1.5`, `use_second_order_ste=True`, `delta_g_eff=0.15`

## Impact

- Existing `NL=2.0` M-series fresh-eval results are unaffected.
- The guard only activates when `1 < |NL| < 2`; all current M-series severe-NL runs used `|NL| = 2.0`.
