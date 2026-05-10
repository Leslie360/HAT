# [✅ NO ERRATA — Branch A] CODEX Source Audit: Hidden Bug Review

> **ℹ️ NO ERRATA (2026-04-22):** This audit's findings (auto-fill semantics, higher-order state persistence, eval script dataset specificity) are independent of the Branch A resolutions. The ratification of the no-multiplier form and the second-order sign fix (`+0.5` → `-0.5`) do not affect any claims made herein. No corrections required.

---

*Original report follows below for archival purposes:*

# CODEX Source Audit: Hidden Bug Review

Date: 2026-04-22
Scope: local source paths that can affect the interpretation of `J1d / K2 / K3 / K4`

## Findings

### 1. Higher-order wrapper semantics were ambiguous and could distort parity

File:
- `scripts/_gpt/run_tinyvit_groupwise_nl_comp.py`

Problem:
- `delta_g_eff <= 0` was treated as auto-fill.
- Auto-fill used `exp_cfg.sigma_d2d + exp_cfg.sigma_c2c`, i.e. nominal config values.
- In standard noisy training, the effective train-time `sigma_c2c` is often forced to `0.0`, so the old auto-fill could include C2C that was not actually active during training.

Impact:
- This does not invalidate the main paper conclusions.
- It does affect the interpretation of the higher-order parity/diagnostic line (`J1d/K2/K3/K4`), especially any branch that described `delta_g_eff=0.0` as a literal-zero baseline.

Fix applied:
- Auto-fill now triggers only for `delta_g_eff < 0`.
- Auto-fill now uses the effective values already written into `module.config`.

### 2. Higher-order state could persist when a model object was reused

File:
- `scripts/_gpt/run_tinyvit_groupwise_nl_comp.py`

Problem:
- When `use_second_order_ste=False`, the wrapper did not explicitly clear:
  - `use_second_order_ste`
  - `delta_g_eff`
  - `second_order_alpha`

Impact:
- Low-to-medium risk.
- Usually masked because most experiment launches build a fresh model.
- Still a real state-management bug if multiple runs reuse the same in-process model object.

Fix applied:
- The wrapper now explicitly resets all higher-order fields when SO2 is disabled.

### 3. Joint fresh-eval script was silently CIFAR-10-specific

File:
- `scripts/_gpt/eval_joint_fresh_instance.py`

Problem:
- The script hard-coded:
  - `dataset="cifar10"`
  - `num_classes=10`
  - `batch_size=256`

Impact:
- Current local `TinyViT/CIFAR-10` conclusions are not invalidated.
- But the script was not a safe general-purpose evaluator and could silently mis-evaluate other checkpoints.

Fix applied:
- The script now derives `dataset` and `num_classes` from the checkpoint unless explicitly overridden by CLI.
- Evaluation batch size is now configurable.

## Net conclusion

- No hidden bug was found that directly overturns the main paper conclusions.
- A real semantics bug did exist in the higher-order wrapper and could affect parity interpretation.
- That bug has now been fixed locally and future runs should use the corrected semantics.
