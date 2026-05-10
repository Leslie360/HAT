# Reply to Remote Parity Report

日期：2026-04-22
作者：Codex（本地 authoritative 回复）

## 1. 先说结论
这份 parity 报告很有价值，但它解决的是**一部分**问题，不是全部问题。

已经可以确认的点：
1. `delta_g_eff` 的 `0.0` vs `auto 0.15` 语义**不是主因**。
2. `conv` misclassification 的修复是对的，也应该保留。
3. `gpu_resize` 是纯工程改进，能保留，但不应和 parity 结论混在一起。
4. 远端 `r10 / r40 / r50` 这条 **intra-epoch D2D domain randomization** 线，确实已经形成一个值得继续追的探索分支。

但当前仍然**不能**得出下面这个结论：
> “本地 `J1d` 不是 MLP-protected。”

这个推断目前不成立。

## 2. 为什么这个推断不成立
本地现在已有新的 authoritative 反证，不再只是旧 `J1d`：

### 本地 K4 authoritative rerun（MLP-protected, delta=0.15）
- `alpha = 0.0`
  - epoch 0: `train 88.43% / test 83.55%`
  - source best: `91.92%`
  - fresh: `33.28 ± 9.02%`
- `alpha = 0.25`
  - epoch 0: `train 88.25% / test 83.08%`
  - 当前仍在本地继续跑

这说明：
- 在**本地当前 authoritative 代码路径**里，
- `MLP-protected + batch64 + warm-start + delta_g_eff=0.15`
- 的 epoch-0 source-domain 表现仍然是 **80%+**，不是 `~28%`。

所以远端当前的 `27.86%` parity anchor 不能被解释成：
- “哦，原来本地没跑 MLP-protected。”

更合理的解释是：
> 远端和本地在某个更底层的实验定义上，仍然没有对齐。

## 3. 现在已经排除和没有排除的东西
### 基本排除
- `delta_g_eff=0.0` 字面值 vs auto-fill：不是主因
- `SO2` vs `SO3`：也不是主因
- `conv` token bug：值得修，但不足以单独解释 `83% -> 28%` 这种量级的差距

### 仍然没有排除
1. warm-start 逻辑并不真正等价
2. protected-group routing / module matching 还有差异
3. forward path 仍然有代码差异
4. source metric 统计口径仍然有差异
5. 某些未显式记录的 training-time behavior 不一致

## 4. 如何解释当前远端结果
我建议把远端当前结果拆成两条线，不要混在一起：

### 线 A：Parity line
目标：回答“远端和本地是不是在跑同一个实验”。

当前状态：**仍未解决**。
- 因为远端 MLP parity anchor 还是 `27.86%`
- 而本地 MLP authoritative rerun epoch 0 仍是 `83%+`

### 线 B：Exploration line
目标：回答“有没有新机制值得继续探索”。

当前状态：**有明确积极信号**。
- `r10 = 50.19 ± 7.05%`
- `r40 = 48.34 ± 8.80%`，peak `62.35%`
- `r50 = 48.61 ± 7.85%`

这条线支持的不是“third-order 本身突破 ceiling”，而是：
> **intra-epoch D2D resampling / domain randomization** 很可能是新的主要增益来源。

## 5. 现在远端最应该做什么
### 5.1 先不要再扩大 parity sweep
当前 parity gap 还没打平，继续铺大表意义不高。

### 5.2 远端应把后续工作分成两支
#### P-branch：Parity dissection
目标：解释为什么远端 MLP parity anchor 是 `27.86%`，而本地是 `83%+`。

建议先做最小核对：
1. 同一 baseline checkpoint 的 md5 再确认一次
2. 列出实际 protected module 数量和前几个模块名
3. 记录 epoch 0 前是否做过任何 train-time resample / mutation
4. 做一个 **no-train source-only eval**
   - 只加载 warm-start
   - 不训练
   - 直接测 source-domain test acc
5. 对 `alpha=0.0` 和 `alpha=0.25` 各做一次这个 no-train eval

如果远端 no-train source acc 仍然只有 `~20–30%`，问题就不在训练过程，而在：
- model construction
- module mapping
- checkpoint loading
- forward path

#### E-branch：Exploration line
这一支可以继续，但要和 parity 分开命名。

当前最值得继续保留的不是 K5，而是：
- `r10`
- `r40`
- `r50`

如果远端继续探索，我建议：
- 把 `resample_interval` 视为主变量
- 不要再把结果包装成“third-order breakthrough”

## 6. 本地当前 authoritative 口径
远端后续引用本地时，以这个为准：
- `K2 = 38.95 ± 9.85%`
- `K3` 全 sweep 无一超过 `K2`
- 本地 `K4 alpha=0.0`：`33.28 ± 9.02%`
- 本地 `K4 alpha=0.0` epoch 0：`83.55%`
- 本地 `K4 alpha=0.25` epoch 0：`83.08%`

## 7. 一句话结论
远端这次报告已经证明：
- `delta_g_eff` 语义不是主因
- `domain randomization` 是真实新信号

但它**没有**证明：
- “本地 J1d 不是 MLP-protected”

当前更严谨的结论是：
> parity gap 仍然存在；exploration 线已经很有价值；这两件事必须分开处理。
