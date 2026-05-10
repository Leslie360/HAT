# Remote Task Queue V5

日期：2026-04-22
状态：基于 corrected local parity re-anchor 的新队列

## 主路线已经确定
远端后续主任务只服务这一条：
- **uniform-NL (`group=all`) + domain randomization / D2D resampling cadence**

`group=mlp` mixed-NL 现在降级为诊断线，不再是主路线。

## 不再作为主任务的内容
不要继续把这些当主攻方向：
- 试图把 `group=mlp` mixed-NL 救成主方案
- 再围绕旧 `27 / 58 / 81` 数字争论 parity
- 大规模 mixed-NL 网格搜索

## V5 远端优先级
### R1 — corrected all-linear cadence replica
目标：在 corrected code 下重建最有希望的 uniform-NL + resampling 结果。

要求：
- `group=all`
- severe global NL (`--nl-ltp 2.0 --nl-ltd -2.0`) unless the specific route says otherwise
- corrected code only
- fixed warm-start baseline checkpoint
- fresh protocol fixed and explicit

优先跑：
1. `r40`
2. `r50`
3. `r10`

每条至少回传：
- exact command
- source best
- fresh mean ± std
- peak instance
- per-instance table
- whether training used per-epoch or intra-epoch resampling

### R2 — corrected training-length check
目标：确认“更长训练伤 fresh”在 corrected code 下是否仍成立。

最低要求：
- compare `r50 50ep` vs `r50 100ep`
- same code, same checkpoint base, same eval protocol

### R3 — corrected source/fresh tradeoff table
目标：输出一张只包含 corrected all-linear runs 的紧凑表。

必须列：
- cadence
- epochs
- source best
- fresh mean
- fresh std
- peak instance
- verdict

## Mixed-NL 只允许的小任务
### M1 — tiny diagnostic only
如果还有空余资源，mixed-NL 只允许做很小的诊断：
- 1-epoch or no-train checks
- no large fresh-instance campaigns
- no long K-series sweep trees

目的仅限：
- sanity check
- selector / routing / parity debug

## 当前本地 corrected 锚点（供远端引用）
- `mlp + SO2 + auto(-1.0)` -> `46.75%`
- `mlp + SO2 + literal zero(0.0)` -> `57.00%`
- `mlp + no SO2` -> `55.65%`
- `all + SO2 + auto(-1.0)` -> `83.34%`

## 一句话执行口径
远端现在的价值是：
**快速筛 corrected uniform-NL + domain-randomization 的最佳配置。**
不是继续为 mixed-NL 寻找主路线身份。
