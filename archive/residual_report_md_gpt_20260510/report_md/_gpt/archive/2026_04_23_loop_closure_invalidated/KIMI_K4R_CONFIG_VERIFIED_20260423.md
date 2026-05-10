<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# K4R Training ↔ Eval Config Verification

**Date**: 2026-04-23
**Checkpoint**: `checkpoints/_gpt/cx_k4_alpha/k4_alpha_0p25/V4_hybrid_standard_noise_hat_k4_alpha_0p25_best.pt`

## Training Launcher (`launch_cx_k4r_alpha_0p25.sh`)

| Parameter | Value | Effective? |
|:----------|:------|:-----------|
| `--nl-ltp` | 2.0 | ❌ Overridden by groupwise setter |
| `--nl-ltd` | -2.0 | ❌ Overridden by groupwise setter |
| `--protected-group` | `all` | ✅ All layers matched |
| `--protected-nl-ltp` | 1.0 | ✅ Applied to all layers |
| `--protected-nl-ltd` | -1.0 | ✅ Applied to all layers |
| `--use-second-order-ste` | (set) | ✅ Activated |
| `--second-order-alpha` | 0.25 | ✅ Applied |
| `--delta-g-eff` | -1.0 | ✅ Auto-computed per module |

## Why `exp_cfg.nl_ltp=2.0` in Checkpoint?

The `exp_cfg` object is instantiated **before** `make_groupwise_setter` patches the model. The setter modifies `module.config` in-place but does **not** mutate `exp_cfg`. Therefore the checkpoint records the original CLI values (`nl_ltp=2.0`) rather than the protected values (`nl_ltp=1.0`).

**This is expected and correct.** The important config is `module.config`, not `exp_cfg`.

## Eval Launcher (`launch_cx_k4r_fresh_eval.sh`)

| Parameter | Value | Matches Training? |
|:----------|:------|:------------------|
| `--protected-group` | `all` | ✅ Yes |
| `--protected-nl-ltp` | 1.0 | ✅ Yes |
| `--protected-nl-ltd` | -1.0 | ✅ Yes |
| `--use-second-order-ste` | (set) | ✅ Yes |
| `--second-order-alpha` | 0.25 | ✅ Yes |
| `--delta-g-eff` | -1.0 | ✅ Yes (auto-computed) |

## Verdict

✅ **Training and eval configurations are aligned.**

The fresh-instance eval will use the exact same groupwise NL setter, second-order brake strength, and auto-computed δg_eff as the training loop.
