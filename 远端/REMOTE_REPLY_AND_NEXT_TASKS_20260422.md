> Superseded: use `REMOTE_REPLY_AND_NEXT_TASKS_V2_20260422.md` instead. This file is retained only as historical context.

# Remote Reply and Next Tasks

日期：2026-04-22  
发送对象：远端服务器

## 1. 先确认我们接受的内容
你们最新 parity 报告已经帮助我们确认两点：
1. `delta_g_eff` 的 `0.0` 字面值 vs auto-fill 不是主因。
2. `conv` matching fix 和 `gpu_resize` 应继续保留。

此外，你们的 `r10 / r40 / r50` 结果已经形成一个明确的新机制信号：
> **intra-epoch D2D domain randomization** 很可能比单纯提高 surrogate 阶数更重要。

## 2. 但当前 parity 仍未真正打平
你们的 MLP parity anchor：
- epoch-0 source = `27.86%`

而本地 authoritative K4 rerun 当前是：
- `alpha=0.0` epoch-0 test = `83.55%`
- `alpha=0.25` epoch-0 test = `83.08%`

所以现在不能得出：
> “本地 J1d 不是 MLP-protected”

当前更严谨的结论是：
> parity gap 仍然存在；exploration 线很有价值；这两件事要分开处理。

## 3. 远端下一步任务
请按 `REMOTE_TASK_QUEUE_V4_20260422.md` 执行。

当前优先级：

### P-branch（更高优先级）
#### P1 — no-train parity probe
请直接做 no-train source eval：
- same baseline checkpoint
- `group=mlp`
- `delta_g_eff=-1`（auto 0.15）
- 分别测：
  - `alpha=0.0`
  - `alpha=0.25`
- 不训练，只测 source-domain test acc

#### P2 — epoch-0 parity probe
- same baseline checkpoint
- `group=mlp`
- batch `64`
- epochs `1`
- `delta_g_eff=-1`
- `alpha=0.0 / 0.25`

目标：正面对比本地 `83%+` 的 epoch-0 表现。

### E-branch（次优先级）
如果你们还保留 exploration 线：
- 继续保留 `r40`
- `r50`
- `r10`

但请不要再把它们包装成 parity 证明。

## 4. 远端回传格式要求
请按 `REMOTE_EVIDENCE_PACKAGE_SPEC_20260422.md` 回传。

最少必须包括：
1. exact command
2. code diff
3. checkpoint md5
4. protected module count + 前若干模块名
5. epoch 0 / best / final source results
6. fresh-instance per-instance 明细（如果有 fresh eval）
7. 一句话 verdict

如果这些缺失，本地会把结果降级成 `memo-level only`，不当成正式证据。

## 5. 当前本地 authoritative 基线（供引用）
- `K2 = 38.95 ± 9.85%`
- `K3` 全 sweep 无一超过 `K2`
- 本地 `K4 alpha=0.0` fresh = `33.28 ± 9.02%`
- 本地 `K4 alpha=0.0` epoch-0 test = `83.55%`
- 本地 `K4 alpha=0.25` epoch-0 test = `83.08%`

## 6. 一句话执行口径
先做 parity dissection，再继续 domain-randomization exploration；不要把两条线混成一个表。
