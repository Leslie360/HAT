# Remote Parity Report

日期：2026-04-22
来源：远端服务器
状态：远端 parity 报告原始留存

## Config Clarifications

1. `delta_g_eff=0.0`
   - 在远端代码里，`delta_g_eff=0.0` 是**字面 0.0**。
   - 只有 `delta_g_eff < 0`（例如 `-1.0`）才会 auto-fill 到 `0.15`。
   - 远端已修复：`make_groupwise_setter` 中从 `<= 0` 改成 `< 0`。

2. `conv` matching fix
   - 已生效：`"conv"` 已从 analog matching token 中移除。
   - 远端说明：baseline checkpoint 缺少 Conv2d 层的 `d2d_noise` buffer。
   - 如果不修这个问题，把 Conv2d 转成 AnalogConv2d 会在 `std=0.9` 下随机化 `d2d_noise`。

3. `gpu_resize`
   - 已生效（自 2026-04-22 13:40 起）。
   - DataLoader 读 `32×32` 原始图，训练/评估时在 GPU 上 `F.interpolate` 到 `224×224`。
   - 远端说明：这消除了 CPU resize 瓶颈，吞吐提升约 `40x`。

4. `Fresh(single)` protocol
   - `5 fresh instances × 3 eval runs`
   - 每个 instance：先重采样一次 `d2d_noise`，再在**相同噪声**下评估 3 次。
   - 报告的 `mean ± std` 是跨 5 个 instance 的统计。

## Complete Results Table

| Run | Group | SO2/SO3 | alpha | delta_g_eff | resample | epochs | batch | source best | fresh mean ± std |
|---|---|---|---:|---|---|---:|---:|---:|---:|
| SO2 baseline | all | SO2 | 1.0 | 0.0 (literal) | per-epoch | 15 | 512 | 85.80% | 20.99 ± 4.28% |
| SO3 50ep | all | SO3 | 1.0 | 0.15 | per-epoch | 50 | 512 | 89.07% | 42.62 ± 5.65% |
| r20 50ep | all | SO2 | 1.0 | 0.15 | every 20 batches | 50 | 512 | 88.24% | 44.07 ± 3.08% |
| r30 50ep | all | SO2 | 1.0 | 0.15 | every 30 batches | 50 | 512 | 81.55% | 39.98 ± 9.83% |
| r35 50ep | all | SO2 | 1.0 | 0.15 | every 35 batches | 50 | 512 | 89.62% | 28.38 ± 8.52% |
| r40 50ep | all | SO2 | 1.0 | 0.15 | every 40 batches | 50 | 512 | 88.22% | 48.34 ± 8.80% |
| r45 50ep | all | SO2 | 1.0 | 0.15 | every 45 batches | 50 | 512 | 84.80% | 44.97 ± 10.15% |
| r50 50ep | all | SO2 | 1.0 | 0.15 | every 50 batches | 50 | 512 | 89.51% | 48.61 ± 7.85% |
| r50 100ep | all | SO2 | 1.0 | 0.15 | every 50 batches | 100 | 512 | 90.05% | 35.34 ± 11.37% |
| r10 50ep | all | SO2 | 1.0 | 0.15 | every 10 batches | 50 | 512 | 86.17% | 50.19 ± 7.05% |
| K5 MLP SO3 | mlp | SO3 | 1.0 | 0.15 | per-epoch | 100 | 64 | 27.39% | N/A |
| Parity MLP SO2 | mlp | SO2 | 1.0 | -1 (auto 0.15) | per-epoch | 100 | 64 | 27.86% | N/A |

## Key Findings（远端原始表述）
### 1. Parity anchor result
- Parity MLP SO2 (`delta_g_eff=-1` / auto `0.15`): source = `27.86% @ epoch 0`, early stopped.
- 远端解释：这与 `K5 MLP SO3 = 27.39%` 基本一致，说明 MLP-protected collapse **不是**由 `delta_g_eff` 语义导致。
- 远端推断：local `J1d (epoch-0 test 81.86%)` 可能不是 MLP-protected，或本地代码仍有其他根本差异。

### 2. Domain randomization is the strongest signal
- `r40`: peak instance `62.35%`（最高 single-instance fresh）
- `r10`: fresh `50.19%`（最稳的 mean）
- `r50`: fresh `48.61%`（source/fresh 平衡最好）
- `r30`: `39.98%`（unstable valley）
- 远端判断：sweet spot 在 `r40–r50`，不是单调趋势。

### 3. Longer training hurts fresh-instance
- `r50 50ep`: fresh `48.61%`
- `r50 100ep`: fresh `35.34%`
- 远端判断：更长训练提升 source，但损害跨实例 transfer。

### 4. Third-order STE shows no benefit
- `SO3 50ep: 89.07% / 42.62%`
- `r50 50ep: 89.51% / 48.61%`
- 远端判断：domain randomization (`r50`) 优于 third-order (`SO3`)。
