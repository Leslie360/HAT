# Remote Parity and Local State

日期：2026-04-22
作用：把远端核对时必须知道的本地 authoritative 信息压成一页

## 本地 authoritative 结果
### K2 — J1d N=30 fresh-instance extension
- `38.95 ± 9.85%`
- range: `22.03% – 61.69%`
- 解释：`Branch C / ambiguous-bimodal`
- 文件：
  - `report_md/_gpt/CODEX_CX_K2_SUMMARY.md`
  - `report_md/_gpt/json_gpt/cx_k2_fresh_eval.json`

### K3 — delta_g_eff sweep（已完成，负结果）
- `0.05 -> 36.21 ± 9.61%`
- `0.10 -> 30.79 ± 11.59%`
- `0.15 -> 27.85 ± 7.37%`
- `0.20 -> 33.25 ± 10.29%`
- `0.25 -> 30.08 ± 9.07%`
- 结论：没有任何点超过 `K2`
- 文件：
  - `report_md/_gpt/CODEX_CX_K3_INTERPRETATION_20260422.md`
  - `report_md/_gpt/json_gpt/cx_k3_dgeff_continuation.json`

### K4 — 本地 authoritative rerun（live）
本地现在不采信旧 K4 摘要，而是在重跑真实实验。

当前协议：
- warm-start: `checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- fixed `delta_g_eff = 0.15`
- alpha sweep: `{0.0, 0.25, 0.5, 0.75, 1.0}`
- epochs: `100`
- batch size: `64`
- workers: `0`
- fresh eval: `10 x 5`

当前已完成点：
- `alpha = 0.0`
  - train best: `91.92% @ epoch 95`
  - fresh: `33.28 ± 9.02%`
- 当前 live 状态：
  - `alpha = 0.25` 已起跑
  - live log: `logs/_gpt/cx_k4_alpha_tmux_20260422.log`

## 本地 parity 关键点
### 1. baseline checkpoint MD5
- `checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- md5:
  - `af0d9a6be75de766a2621ae058a61393`

### 2. canonical J1d surviving epoch-0 log
- `train_acc = 88.05%`
- `test_acc = 81.86%`

### 3. local code fact
在本地代码里：
- `NL_LTP / NL_LTD / use_second_order_ste / delta_g_eff`
- 不改变 `STE.forward()` 的前向量化值
- 这些设置影响的是 `backward()` 的 surrogate 梯度

因此，如果远端 `epoch 0` 只有 `~20–30%`，首先怀疑的不是“surrogate 曲率本身”，而是：
- checkpoint 不同
- warm-start 路径不同
- protected-group routing 不同
- forward-path 代码不同
- metric 统计口径不同

## 本地对 K4/K5 旧摘要的裁定
- 旧 `K4` 摘要：memo-level only
- 旧 `K5` 摘要：memo-level only
- 原因：缺 surviving run log / checkpoint family / raw eval JSON
- 文件：
  - `report_md/_gpt/CODEX_K4_K5_PROVENANCE_AUDIT_20260422.md`

## 远端使用规则
- 如果远端要声称 parity，需要先对齐：
  1. baseline checkpoint MD5
  2. warm-start 逻辑
  3. protected-group routing
  4. `delta_g_eff` 的 auto-fill 语义
  5. epoch-0 metric 定义
- 在这些没有对齐之前，远端结果只能视为：
  - 有价值的新分支探索
  - 不能直接替代本地 canonical 结论
