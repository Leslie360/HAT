# Handoff: Kimi Code CLI → Codex (Round Q Day 1)
**Date:** 2026-04-21 22:50
**From:** Kimi Code CLI (interactive session)
**To:** Codex executor
**Context:** Round Q broadcast read, CX-K1/K2/K3 partially executed

---

## 1. 已完成的任务

### CX-K1: J1d Reconciliation Audit ✅
- 发现三重矛盾报告（CEILING_BROKEN / BRANCH_A / AMBIGUOUS）
- 确认 **41.53±8.87% (N=10)** 为唯一权威结果
- 验证 J2/J3/J4 **未实际运行**（JSON stubs 无日志/无 checkpoint）
- 文件：`CODEX_J1D_RECONCILIATION_20260421.md`（已重写）

### CX-K2: N=30 Fresh-Instance Extension ✅
- 完成 20 个额外 seed（1042–2942）+ 原有 10 个 = **N=30**
- 结果：**38.95% ± 9.85%**，范围 22.03%–61.69%
- 结论：双峰分布**真实存在**，非 seed artifact
- 文件：`CODEX_CX_K2_SUMMARY.md`、`cx_k2_fresh_eval.json`

### CX-K3: delta_g_eff Sweep — Run #1 完成 ✅
- Run #1 (delta=0.05)：100 epochs 完成，best=**91.52%**
- Checkpoint：`checkpoints/_gpt/cx_k3_dgeff/k3_dgeff_0p05/V4_hybrid_standard_noise_hat_k3_dgeff_0p05_best.pt`
- **未启用 compile**（作为选项 A 的基准 run）

### 代码优化补丁（已应用）
- `train_tinyvit_ensemble.py`：
  - 默认启用 **TF32**（`torch.set_float32_matmul_precision('high')`）
  - 新增 `--compile` CLI flag（`torch.compile(model, mode="reduce-overhead")`）
  - **注意**：`run_experiment()` 的 `compile_model` 参数曾因替换不完全导致签名缺失，已修复并清除 pycache

---

## 2. 遇到的问题

### 问题 A：torch.compile + batch_size=256 → OOM
- 现象：`torch.AcceleratorError: CUDA error: out of memory`
- 触发条件：batch_size=256 + `--compile` + num_workers=2 + pin_memory
- 根因：torch.compile 增加显存开销，叠加后超出 16GB
- 状态：Run #2 (delta=0.10) **启动失败**，continuation driver 崩溃

### 问题 B：watcher 已退出
- watcher (PID 1514328) 在 run #1 完成后正常退出
- 当前 **无后台进程监控**，GPU 空闲

### 问题 C：run #1 训练速度偏慢
- run #1 实际 epoch 速率：**~4.3 min/epoch**（batch_size 实际为 64，因 `patched_get_configs` 覆盖）
- 而非预期的 1.8 min/epoch（K3 driver 传了 `--batch-size 256` 但被 wrapper 覆盖为 64）

---

## 3. 当前状态

| 组件 | 状态 |
|:---|:---|
| GPU | 空闲 (253MiB / 16GB) |
| Run #1 (0.05) | ✅ 完成，best=91.52%，checkpoint 已保存 |
| Run #2 (0.10) | ❌ 失败（OOM at startup） |
| Run #3-5 | ⏸ 未启动 |
| 后台进程 | 无 |
| `train_tinyvit_ensemble.py` | 已打补丁（TF32 + --compile），pycache 已清除 |

---

## 4. 下一步行动（需 Codex 执行）

### P0：修复并重启 K3

**决策 needed**：以下两个方案二选一

**方案 A：保守（推荐）**
- Run #2-5 **不带 torch.compile**，仅依赖 TF32 + num_workers=2
- 优点：OOM 风险为零，与 run #1 配置一致（仅 delta_g_eff 不同）
- 修改：continuation driver 中移除 `--compile`，保留 `--num-workers 2`

**方案 B：激进**
- Run #2-5 带 torch.compile，但 **batch_size 降为 128**
- 先做一个 1-epoch smoke test 验证 OOM 是否解决
- 如通过则继续，如失败则回退方案 A

### P1：启动 continuation driver

无论选 A 还是 B，需要：
1. 修改 `/tmp/cx_k3_optimized.py`（或重写）
2. `nohup` 后台启动
3. 每个 run 完成后自动执行 10×5 fresh eval
4. 所有 5 个值完成后写 `CODEX_CX_K3_SUMMARY.md`

### P2：监控与日志

- 每 30 分钟检查一次训练进度
- 任何失败立即记录到 `AGENT_SYNC_gpt.md`
- 如果某个 delta 值连续失败 2 次，跳过并记录

---

## 5. 关键文件路径

| 文件 | 路径 |
|:---|:---|
| Run #1 checkpoint | `checkpoints/_gpt/cx_k3_dgeff/k3_dgeff_0p05/V4_hybrid_standard_noise_hat_k3_dgeff_0p05_best.pt` |
| K2 JSON | `report_md/_gpt/json_gpt/cx_k2_fresh_eval.json` |
| K3 run #1 log | `logs/_gpt/cx_k3_train_k3_dgeff_0p05.log` |
| Continuation driver | `/tmp/cx_k3_optimized.py` |
| 训练脚本（已补丁） | `train_tinyvit_ensemble.py` |
| Reconciliation | `report_md/_gpt/CODEX_J1D_RECONCILIATION_20260421.md` |
| K2 Summary | `report_md/_gpt/CODEX_CX_K2_SUMMARY.md` |

---

## 6. 广播规则提醒

- **Rule B 仍生效**：禁止编辑 paper/、paper/thesis/、cover_letter 等
- **K3 授权条件**：K2 mean ∈ [35, 50) → 已满足，K3 已授权
- **Tier-2 (J2/J3/J4)**：暂停，等 K3 完成后根据结果决定
- **Friday mini-checkpoint** (2026-04-25)：Codex 需汇报 K1/K2/K3 状态

---

*End of handoff. Codex should read this file and the referenced JSON/logs before proceeding.*
