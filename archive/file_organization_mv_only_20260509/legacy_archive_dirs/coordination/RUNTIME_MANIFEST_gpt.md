# Runtime Manifest (GPT)

更新时间：`2026-04-06 22:05 +0800`

## Current Phase

- `MASTER_PLAN` 的 `Task 34 / 35 / 36` 已经全部完成并锁定结果。
- 当前没有活跃训练或 watcher 进程。
- 当前阶段已回到：
  - final manuscript integration
  - figure / caption consistency pass
  - LaTeX 收口
  - Gemini 继续维护 `paper_zh/`，Codex 仅维护英文主稿 / LaTeX / 运行留痕

## Active Training

- 当前无活跃训练。
- 最近一次 submission-critical 训练链已完成：
  1. `Task 34`: Tiny-ViT `V4_proportional_HAT`
  2. `Task 35`: Tiny-ViT `V4_NL2_HAT`
  3. `Task 36`: ConvNeXt `C4_proportional_HAT`

## Latest Locked Results

- `Task 21 / ConvNeXt Flowers-102`
  - `C1 = 33.22%`
  - `C3 = 3.79%`, `MC = 1.57 ± 0.83%`
  - `C4 = 3.35%`, `MC = 2.03 ± 0.68%`
- `Task 34 / V4_proportional_HAT`
  - train best = `97.48%`
  - proportional-noise eval = `97.37 ± 0.05%`
  - uniform-noise transfer eval = `10.38 ± 0.44%`
- `Task 35 / V4_NL2_HAT`
  - train best = `27.37%`
  - NL=2.0 eval = `27.72 ± 0.82%`
- `Task 36 / C4_proportional_HAT`
  - train best = `91.98%`
  - MC = `91.91 ± 0.08%`
  - note: initial run crashed only in the auto-appended retention hook; final train export was repaired via no-retrain rerun with `--skip-retention`

## Active Watchers

- 当前没有活跃 watcher 进程。
- 历史 watcher 仍然有效，作为 `Task 21 -> Task 23/24` 自动接续成功的留痕证据。

## Superseded / Stale Watchers

- 旧 `Flowers summary-only watcher` 已不再活跃：
  - `/home/qiaosir/projects/compute_vit/watch_convnext_task21_stage2_completion_gpt.py`
  - 对应旧日志：
    - `/home/qiaosir/projects/compute_vit/logs/_gpt/watch_convnext_task21_stage2_20260406_0057_gpt.log`
  - 现由新的 stage-3 watcher 完整接管

## Completed Automatic Stage

`Flowers-102` clean completion后，已自动完成：

1. `Task 24`
   - `V4` proportional-noise MC eval
2. `Task 23`
   - `V4_NL_moderate`
3. `Task 23`
   - `V4_NL_severe`
4. `Task 23`
   - `C4_NL_moderate`

### Stage-3 Results

- `Task 24 / V4 proportional-noise`
  - 结果：`10.00 ± 0.00%`
  - 日志：
    - `/home/qiaosir/projects/compute_vit/logs/_gpt/task23_task24_after_task21_20260406_014325_driver_gpt.log`
- `Task 23 / V4_NL_moderate`
  - best=`27.91%`
- `Task 23 / V4_NL_severe`
  - best=`27.54%`
- `Task 23 / C4_NL_moderate`
  - best=`65.86%`, `MC = 65.34 ± 0.42%`

## Stage-3 Scripts

- `/home/qiaosir/projects/compute_vit/run_task24_v4_proportional_eval_gpt.sh`
- `/home/qiaosir/projects/compute_vit/run_task23_tinyvit_nl_suite_gpt.sh`
- `/home/qiaosir/projects/compute_vit/run_task23_convnext_c4_nl_moderate_gpt.sh`
- `/home/qiaosir/projects/compute_vit/run_task23_task24_after_task21_gpt.sh`

## Marker Files

- 未触发前：
  - `/home/qiaosir/projects/compute_vit/logs/_gpt/task23_task24_after_task21_launch_gpt.json`
  - 当前状态：`created`

## Canonical Planning Sources

1. `/home/qiaosir/projects/compute_vit/MASTER_PLAN.md`
2. `/home/qiaosir/projects/compute_vit/report_md/_gpt/CLAUDE_REPLAY_POINTERS_gpt.md`
3. `/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md`

## Latest Replay Order

1. 看本文件确认当前 runtime 已经 idle
2. 看 `Task 34/35/36` 核心日志：
   - `/home/qiaosir/projects/compute_vit/logs/_gpt/train_tinyvit_v4_proportional_hat_20260406_121400_gpt.log`
   - `/home/qiaosir/projects/compute_vit/logs/_gpt/eval_tinyvit_v4_proportional_hat_prop_20260406_121400_gpt.log`
   - `/home/qiaosir/projects/compute_vit/logs/_gpt/eval_tinyvit_v4_proportional_hat_uniform_20260406_121400_gpt.log`
   - `/home/qiaosir/projects/compute_vit/logs/_gpt/train_tinyvit_v4_nl2_hat_20260406_121400_gpt.log`
   - `/home/qiaosir/projects/compute_vit/logs/_gpt/eval_tinyvit_v4_nl2_hat_20260406_121400_gpt.log`
   - `/home/qiaosir/projects/compute_vit/logs/_gpt/train_convnext_c4_proportional_hat_20260406_154500_gpt.log`
3. 看结果文件：
   - `/home/qiaosir/projects/compute_vit/report_md/_gpt/v4_proportional_hat_train_results_gpt.md`
   - `/home/qiaosir/projects/compute_vit/report_md/_gpt/v4_nl2_hat_train_results_gpt.md`
   - `/home/qiaosir/projects/compute_vit/report_md/_gpt/c4_proportional_hat_train_results_gpt.md`
4. 看 `/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md`

## Manuscript Closeout Status

- 英文主稿：
  - `paper/05_results.md`
  - `paper/06_discussion.md`
  - `paper/07_conclusion.md`
  已按最终结果锁定
- `latex_gpt`：
  - Sections `00`--`07` 已全部具备同步 prose draft
  - 当前剩余主要是引用键统一、手工 `Fig.1/2`、以及投稿模板迁移
- 中文主稿：
  - `paper_zh/` 由 Gemini 维护
  - 结果口径需与英文锁定版本保持一致
