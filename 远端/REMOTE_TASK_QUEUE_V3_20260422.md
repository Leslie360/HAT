# Remote Task Queue V3

日期：2026-04-22  
状态：当前远端任务口径

## 远端当前应该做什么
### R1 — K5 third-order STE sanity
目的：验证更高阶 surrogate 是否真的能把 severe-NL fresh-instance 拉出当前本地区间。

推荐配置：
- TinyViT V4
- severe NL (`NL_LTP=+2.0`, `NL_LTD=-2.0`)
- protected group: `mlp`
- warm-start from baseline checkpoint
- fresh protocol: `10 fresh x 5 eval`
- batch size: `64`
- epochs: `100`
- workers: `0`
- AMP: `on`
- `delta_g_eff = 0.15`
- baseline second-order alpha: `1.0`

判据：
- `fresh mean > 45%`：值得本地复现
- `fresh mean > 50%`：强信号
- `<= 43%`：大概率仍是负结果

### R2 — second-order alpha overdrive (`alpha > 1.0`)
目的：本地 `K4` 正在覆盖 `alpha <= 1.0`，远端只补 overdrive 区间。

建议 sweep：
- `alpha = {1.25, 1.5, 2.0}`
- fixed `delta_g_eff = 0.15`
- 其余配置与 R1 相同

停止规则：
- 如果所有点 `<= 40%`，停止
- 如果任一点 `> 45%`，汇报为本地候选复现点

### R3 — sparse 2D rescue grid（条件任务）
只有在 `R1` 或 `R2` 任一点超过 `45%` 时才做。

建议：
- 选最佳 surrogate 设置
- `delta_g_eff = {0.05, 0.15, 0.25}`

## 远端当前不要做什么
- 不要重复本地 `K2`
- 不要重复本地 `K3`
- 不要重复本地 `K4` 的 `alpha <= 1.0`
- 不要做 `QKV-only / attn_proj-only`
- 不要做 `retention / IR-drop / ImageNet` 这类当前非主线任务

## 为什么这样排
本地 authoritative 状态：
- `K2 = 38.95 ± 9.85%`
- `K3` 全 sweep 为负结果
- 本地 `K4` authoritative rerun 已起跑，当前已完成 `alpha=0.0`，fresh `33.28 ± 9.02%`

因此远端的价值不在重复本地，而在补：
- `K5`
- `alpha > 1.0`
- 以及必要时的小型 2D grid
