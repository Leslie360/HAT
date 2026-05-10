# Remote V3 Update 2

日期：2026-04-22
来源：远端服务器回复
状态：**远端结果记录，不等同于本地 canonical parity 已建立**

## Complete Results

### ALL-linear, SO2, `delta_g_eff=0.15`, 50ep unless noted

| Resample | Source | Fresh | Peak | Std |
|---|---:|---:|---:|---:|
| per-epoch (15ep) | 85.80% | 20.99% | — | ±4.28% |
| per-epoch (50ep, SO3) | 89.07% | 42.62% | — | ±5.65% |
| r20 | 88.24% | 44.07% | 47.50% | ±3.08% |
| r30 | 81.55% | 39.98% | 53.38% | ±9.83% |
| r40 | 88.22% | 48.34% | 62.35% | ±8.80% |
| r50 (50ep) | 89.51% | 48.61% | 56.82% | ±7.85% |
| r50 (100ep) | 90.05% | 35.34% | 52.72% | ±11.37% |
| r10 | 86.17% | 50.19% | 58.77% | ±7.05% |

## 远端给出的 Key Findings
1. `r40` 是当前 sweet spot：peak single-instance fresh `62.35%`，source/fresh tradeoff 最平衡。
2. 更长训练会伤 fresh：`r50 100ep` 从 `48.61%` 掉到 `35.34%`。
3. `r30` 是 unstable valley：过于频繁的 resampling 破坏收敛。
4. `MLP-protected` 仍是 structural dead end：`epoch-0 test = 27.86%`。
5. `SO3` 没有明显优于 `SO2 + domain randomization`。

## 远端给出的 Config Notes
- `conv` fix: active (`43` analog modules, no conv2d conversion)
- `gpu_resize`: active (`32 -> 224` on GPU)
- `delta_g_eff`: `0.15` for ALL-linear runs; `-1` (auto `0.15`) for parity anchor
- fresh eval: `5 instances x 3 eval runs`

## 本地当前解释
### 1. 这些结果是有价值的
最强信号不是 `SO3` 本身，而是：
- `r50 -> 48.61 ± 7.85%`
- `r10 -> 50.19 ± 7.05%`
- `r40 -> 48.34 ± 8.80%` 且 peak `62.35%`

当前最合理的解读是：
> **intra-epoch D2D domain randomization** 可能是新的主要增益来源，而不是 “third-order surrogate 单独打破 ceiling”。

### 2. 但这些结果还不是 clean parity
远端 `V3` 不是单纯重跑本地 `J1d`，它混合了：
- parity checking
- bug fix
- runtime fix
- 新机制（`resample_interval`）

所以现在不能把 `V3` 直接写成“远端已经否定本地 canonical 结论”。

### 3. 当前最重要的 unresolved contradiction
- 本地 canonical `J1d` surviving epoch 0: `train 88.05% / test 81.86%`
- 远端 parity anchor epoch 0: `test 27.86%`

这个差距太大，不可能只是随机波动。说明两边还没有跑成同一个实验。

## 当前用途
这份结果现在应该被用作：
- 远端新机制探索证据
- 后续任务分流依据

不应该被用作：
- 对本地 canonical `J1d` 的直接替代
- 直接写入 paper 主结论的 parity proof
