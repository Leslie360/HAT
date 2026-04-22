# CODEX J1d Ceiling-Broken Report

Trigger:
- `J1d_fresh_instance_accuracy` exceeded `50%`.

Immediate action:
- Stop tier-2 auto-launch.
- Mark the first-order-only ceiling narrative as falsified.
- Trigger Branch B for rewrite planning.

Experiment identity:
- Name: `V4_hybrid_standard_noise_hat_second_order_ste`
- Source log: `logs/_gpt/cx_j1d_20260421.log`
- Source JSON: `report_md/_gpt/json_gpt/second_order_ste.json`

Required evidence to fill:
- Fresh-instance mean: `TBD`
- Fresh-instance std: `TBD`
- Best checkpoint accuracy: `TBD`
- Best epoch: `TBD`

Interpretation:
- The new result would indicate that the first-order surrogate is insufficient.
- It would not, by itself, prove that all attention-side nonlinear-write limits disappear.
- The safe claim is "higher-order surrogate breaks the current ceiling under this diagnostic setting."

Operational note:
- Do not auto-edit frozen paper files here.
- This report exists to justify the Branch B handoff at loop closure.
