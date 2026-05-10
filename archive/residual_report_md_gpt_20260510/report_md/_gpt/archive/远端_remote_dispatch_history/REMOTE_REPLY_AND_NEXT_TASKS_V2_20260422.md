# Remote Reply and Next Tasks V2

日期：2026-04-22
发送对象：远端服务器

## 1. 路线已经选定
感谢你们前面的 parity dissection 和 resampling 探索。

基于：
- 你们确认的 config-sharing bug
- 本地后续确认的 STE multiplier bug
- 修复后的本地 corrected parity re-anchor

我们现在正式把主路线定为：
- **uniform-NL (`group=all`)**
- **domain randomization / D2D resampling cadence**

`group=mlp` mixed-NL 不再是主路线，只保留诊断价值。

## 2. 本地 corrected parity anchor
当前本地 corrected 1-epoch anchor：
- `mlp + SO2 + auto(-1.0)` -> `46.75%`
- `mlp + SO2 + literal zero(0.0)` -> `57.00%`
- `mlp + no SO2` -> `55.65%`
- `all + SO2 + auto(-1.0)` -> `83.34%`

所以：
- 旧本地 `81.86%` 不再可当 mixed-NL corrected anchor
- 旧远端 `~27%` 也不再可当 mixed-NL corrected anchor
- 现在 mixed-NL 只应被视为中等表现的诊断线
- `group=all` 仍明显健康

## 3. 远端下一步任务
请按：
- `REMOTE_TASK_QUEUE_V5_20260422.md`
执行。

最重要的是：
1. corrected `r40`
2. corrected `r50`
3. corrected `r10`
4. corrected `r50 50ep vs 100ep`

## 4. Mixed-NL 的使用方式
可以保留极小的 sanity checks，
但不要再把 mixed-NL 当成主路线去烧大算力。

## 5. 回传要求
仍按：
- `REMOTE_EVIDENCE_PACKAGE_SPEC_20260422.md`

缺 exact command / per-instance table / corrected code note 的结果，
本地会继续降级成 memo-level only。
