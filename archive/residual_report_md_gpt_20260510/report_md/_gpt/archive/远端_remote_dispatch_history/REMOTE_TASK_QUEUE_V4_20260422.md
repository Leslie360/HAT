> Superseded: use `REMOTE_TASK_QUEUE_V5_20260422.md` instead. This file is retained only as historical context.

# Remote Task Queue V4

日期：2026-04-22
状态：在收到 parity 报告后的更新版任务口径

## 新原则
远端后续任务分成两条线：
1. **P-branch**：parity dissection
2. **E-branch**：domain-randomization exploration

不要再把这两条线混成一个表。

## P-branch（优先级更高）
### P1 — no-train parity probe
目的：判断远端 `27.86%` 是训练问题还是 model construction / warm-start 问题。

要求：
- same baseline checkpoint
- `group=mlp`
- `delta_g_eff=-1`（auto 0.15）
- 分别测：
  - `alpha=0.0`
  - `alpha=0.25`
- **不训练**
- 直接做 source-domain test eval

回传：
- source test acc
- protected analog module count
- 前若干模块名
- checkpoint md5
- command

### P2 — epoch-0 parity probe
目的：和本地 `epoch-0 83%+` 做正面对比。

要求：
- MLP-protected
- batch `64`
- epochs `1`
- same warm-start
- `delta_g_eff=-1`
- 分别测 `alpha=0.0 / 0.25`

回传：
- epoch 0 train acc
- epoch 0 test acc
- 和 P1 的差值

## E-branch（次优先级）
### E1 — keep domain-randomization line alive
当前已知值得保留：
- `r10`
- `r40`
- `r50`

但用途是：
- 探索新机制
- 不是 parity 证明

### E2 — if continuing exploration
如果远端继续跑，优先顺序：
1. `r40`
2. `r50`
3. `r10`

并且固定：
- all-linear
- SO2
- `delta_g_eff = 0.15`

## 暂停项
- 暂停把 `K5 MLP SO3` 当成主要叙事中心
- 暂停把 “local J1d was not MLP-protected” 当作工作假设
- 暂停继续铺无关 robustness 表
