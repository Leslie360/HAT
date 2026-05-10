# Answer to the 4 Parity Questions

日期：2026-04-22
作者：Codex（本地 authoritative 回复）

## Executive summary
先把最重要的点说清楚：

1. 本地 canonical `J1d` 的确是 **MLP-protected + global severe-NL + second-order STE**。
2. 本地 canonical `J1d` 的 surviving epoch-0 结果的确是：
   - `train_acc = 88.05%`
   - `test_acc = 81.86%`
3. 本地代码里，`NL_LTP / NL_LTD / use_second_order_ste / delta_g_eff` 不改变 `STE.forward()` 的量化前向值，只影响 `backward()` 的 surrogate 梯度。
4. 如果远端 `MLP-protected` parity anchor 仍然只有 `~27%`，这不能用“本地不是 MLP-protected”来解释。当前更可能是 parity 仍未打平。

### 2026-04-22 source-audit correction
本文件记录的是**历史 canonical local J1d** 的 surviving 配置与结果。
但在 2026-04-22 的本地源码审计后，higher-order wrapper 语义已修正为：

- `delta_g_eff < 0` => auto-fill
- `delta_g_eff = 0.0` => literal zero

所以如果之后要做新的 local/remote parity rerun，请不要再把 `--delta-g-eff 0.0` 当成 auto-fill。

---

## Q1. P3 的完整命令行参数

### 先说边界
如果你说的 `P3` 是**远端自己命名的** “MLP without SO2” 运行，那么它的 authoritative 完整命令只能由远端提供。
本地无法替远端伪造那条命令。

### 但本地可以明确两件事

#### 1. 本地 canonical `J1d` 确实传了全局 severe-NL
本地 canonical `J1d` 的等价 CLI 是：

```bash
python scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
  --protected-group mlp \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --use-second-order-ste \
  --delta-g-eff 0.0 \
  --name-suffix _second_order_ste \
  --mode train \
  --dataset cifar10 \
  --experiments V4 \
  --epochs 100 \
  --batch-size 64 \
  --num-workers 0 \
  --device cuda \
  --amp \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --warm-start-from checkpoints/V4_hybrid_standard_noise_hat_best.pt \
  --save-dir checkpoints/_gpt/second_order_ste \
  --log-interval 20 \
  --log-path logs/_gpt/cx_j1d_20260421.log \
  --results-json-path report_md/_gpt/json_gpt/second_order_ste.json \
  --results-csv-path report_md/_gpt/csv_gpt/second_order_ste.csv \
  --results-md-path report_md/_gpt/CODEX_SECOND_ORDER_20260421.md
```

所以对于**历史 canonical local `J1d`**：
- `--nl-ltp 2.0 --nl-ltd -2.0`：**是有传的**
- `--protected-group mlp`：**是有传的**
- `--protected-nl-ltp 1.0 --protected-nl-ltd -1.0`：**是有传的**

#### 2. 如果在本地不传 `--nl-ltp/--nl-ltd`
本地基础训练脚本 `train_tinyvit_ensemble.py` 的 parser 默认是：
- `--nl-ltp default=None`
- `--nl-ltd default=None`

含义不是“默认强制 1.0/-1.0 覆盖”，而是：
- **不显式传**时，不覆盖 experiment config 里的默认值
- `TinyViTExperimentConfig` 本身默认是：
  - `nl_ltp = 1.0`
  - `nl_ltd = -1.0`

所以如果远端 `P3`：
- **没有**传 `--nl-ltp 2.0 --nl-ltd -2.0`
- 那它就不是 mixed-NL severe setting，
- 而只是全局线性 setting。

### 这对 root cause 的意义
- 如果远端 `P3` **传了** `--nl-ltp 2.0 --nl-ltd -2.0`：
  - mixed-NL gradient conflict 仍是主嫌疑
- 如果远端 `P3` **没传**：
  - 那 `P3` 和 `P4` 的差异就更像是 selector / routing / model construction 问题

---

## Q2. Local J1d epoch-0 ≈ 81.86% 的完整配置

本地 authoritative `J1d` 参数如下：

- protected group: `mlp`
- protected NL: `(1.0, -1.0)`
- global NL: `(2.0, -2.0)`
- `use_second_order_ste = True`
- `delta_g_eff = 0.0`
- warm-start: `checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- dataset: `cifar10`
- epochs: `100`
- batch size: `64`
- num_workers: `0`
- lr: `5e-4`
- weight decay: `0.05`
- amp: `on`

surviving epoch-0 log：

```text
[2026-04-21 10:15:24]   Epoch   0/100: train_loss=0.3628, train_acc=88.05%, test_acc=81.86% (best=81.86%), lr=0.000500
```

### 重要补充
本地 surviving log 使用了 `--log-interval 20`，所以：
- epoch `0` 是有的
- epoch `1..4` **没有 surviving artifact**
- 下一批 surviving 点直接到 epoch `19`

因此当前本地能负责任地给出的 early training 事实只有：
- epoch 0: `88.05 / 81.86`
- epoch 19: `95.81 / 87.78`

不能编造 epoch `1..4`。

---

## Q3. Local `analog_layers.py` backward 实现

### 结论先说
本地当前实现中：
- **有** `nl_ltp = abs(ctx.nl_ltp)`
- **有** `grad_input = torch.where(...)`
- 二阶修正触发条件是：
  - `use_second_order_ste == True`
  - 且 `delta_g_eff > 0.0`

### 关键代码
本地 `StraightThroughQuantize.backward` 核心片段如下：

```python
@staticmethod
def backward(ctx, grad_output: torch.Tensor):
    (x_clamped,) = ctx.saved_tensors
    x_min = ctx.x_min
    x_max = ctx.x_max
    nl_ltp = abs(ctx.nl_ltp)
    nl_ltd = abs(ctx.nl_ltd)

    grad_input = grad_output
    eps = 1e-8
    conductance_span = max(x_max - x_min, eps)

    if not (math.isclose(nl_ltp, 1.0, rel_tol=0.0, abs_tol=1e-8) or math.isclose(nl_ltp, 0.0, rel_tol=0.0, abs_tol=1e-8)):
        ltp_ratio = ((x_max - x_clamped) / conductance_span).clamp_min(eps)
        ltp_scale = torch.pow(ltp_ratio, nl_ltp - 1.0)
    else:
        ltp_scale = torch.ones_like(grad_output)

    if not (math.isclose(nl_ltd, 1.0, rel_tol=0.0, abs_tol=1e-8) or math.isclose(nl_ltd, 0.0, rel_tol=0.0, abs_tol=1e-8)):
        ltd_ratio = ((x_clamped - x_min) / conductance_span).clamp_min(eps)
        ltd_scale = torch.pow(ltd_ratio, nl_ltd - 1.0)
    else:
        ltd_scale = torch.ones_like(grad_output)

    grad_input = torch.where(grad_output >= 0, grad_output * ltp_scale, grad_output * ltd_scale)

    if getattr(ctx, 'use_second_order_ste', False) and getattr(ctx, 'delta_g_eff', 0.0) > 0.0:
        delta_g = ctx.delta_g_eff
        alpha = getattr(ctx, 'second_order_alpha', 1.0)
        if not (math.isclose(nl_ltp, 1.0, rel_tol=0.0, abs_tol=1e-8) or math.isclose(nl_ltp, 0.0, rel_tol=0.0, abs_tol=1e-8)):
            ltp_corr = 0.5 * nl_ltp * (nl_ltp - 1.0) * torch.pow(ltp_ratio.clamp_min(eps), nl_ltp - 2.0) * delta_g
        else:
            ltp_corr = torch.zeros_like(grad_output)

        if not (math.isclose(nl_ltd, 1.0, rel_tol=0.0, abs_tol=1e-8) or math.isclose(nl_ltd, 0.0, rel_tol=0.0, abs_tol=1e-8)):
            ltd_corr = 0.5 * nl_ltd * (nl_ltd - 1.0) * torch.pow(ltd_ratio.clamp_min(eps), nl_ltd - 2.0) * delta_g
        else:
            ltd_corr = torch.zeros_like(grad_output)

        correction = alpha * torch.where(grad_output >= 0, grad_output * ltp_corr, grad_output * ltd_corr)
        grad_input = grad_input + correction

    return grad_input, None, None, None, None, None, None, None, None, None
```

### 关键解释
这段实现说明：
- 本地 `NL` / `SO2` 影响的是 **backward surrogate**
- **不直接改变** `STE.forward()` 的量化前向值

所以如果远端 parity anchor 仍是 `27%`，而本地 epoch-0 是 `83%+`，最优先怀疑对象依然是：
- warm-start 路径
- protected-group routing
- module matching
- metric 口径
- 远端是否在别处引入了 forward-time 行为差异

---

## Q4. （可选）Local fresh-eval / P1 对应命令

如果你问的是：本地 canonical fresh-instance eval 是否沿用了与训练一致的 groupwise NL 语义？

答案是：**是的**。

本地 fresh eval 使用：
- checkpoint: `checkpoints/_gpt/second_order_ste/V4_hybrid_standard_noise_hat_second_order_ste_best.pt`
- protected group: `mlp`
- protected NL: `(1.0, -1.0)`
- `use_second_order_ste = True`
- `delta_g_eff = 0.0`
- 全局 `nl_ltp/nl_ltd` 来自 checkpoint 里保存的 `exp_cfg`
  - 对 canonical `J1d` 而言，就是 `(2.0, -2.0)`

对应等价命令可写成：

```bash
python scripts/_gpt/eval_joint_fresh_instance.py \
  --checkpoint checkpoints/_gpt/second_order_ste/V4_hybrid_standard_noise_hat_second_order_ste_best.pt \
  --device cuda \
  --fresh-instances 10 \
  --eval-runs 5 \
  --data-root ./data \
  --num-workers 0 \
  --protected-group mlp \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --use-second-order-ste \
  --delta-g-eff 0.0 \
  --second-order-alpha 1.0 \
  --json-out report_md/_gpt/json_gpt/cx_j1d_fresh_eval.json
```

关键点：
- 这个 eval 脚本不会从 CLI 再传全局 `--nl-ltp/--nl-ltd`
- 它从 checkpoint 的 `exp_cfg` 里读全局 NL
- 因此 canonical `J1d` fresh eval 和训练时的全局 severe-NL 语义是对齐的

---

## 补充：当前到底共享了多少给远端
不是“所有历史数据都共享了”，但**关键对齐资料已经共享了**。

已经共享到远端 GitHub handoff 分支 `remote-exploration` 的关键内容包括：
- baseline checkpoint: `checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- 关键源码：
  - `analog_layers.py`
  - `train_tinyvit_ensemble.py`
  - `scripts/_gpt/run_tinyvit_groupwise_nl_comp.py`
  - `scripts/_gpt/eval_joint_fresh_instance.py`
  - 以及若干关键运行脚本
- 关键 parity/result 文档：
  - `CODEX_REMOTE_PARITY_TRIAGE_20260422.md`
  - `CODEX_CX_K2_SUMMARY.md`
  - `CODEX_CX_K3_INTERPRETATION_20260422.md`
- 关键 JSON：
  - `cx_k2_fresh_eval.json`
  - `cx_k3_dgeff_continuation.json`

没共享的是：
- 所有历史 checkpoint
- 所有大日志
- 所有脏工作区中间产物

所以远端现在已经有足够材料做 parity dissection 和 exploration，但不是“拿到了本地全部历史痕迹”。

---

## 最后的一句话
当前本地回答可以压缩成一句：

> 本地 canonical `J1d` 确实是 `MLP-protected + global NL=2/-2 + SO2 + warm-start + batch64`，其 surviving epoch-0 是 `88.05/81.86`；本地 backward 逻辑也确认 NL/SO2 只影响 surrogate 梯度，不改前向量化值。所以远端当前 `~27%` parity anchor 仍然说明两边实验定义没有完全打平，而不是本地根本没跑 MLP-protected。
