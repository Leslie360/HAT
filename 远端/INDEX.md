# 远端协同索引

日期：2026-04-24
范围：远端服务器实验、远端任务队列、本地-远端 parity 核对

## 目的
这个目录是远端协同的单点入口。后续核对不要再分别翻 `report_md/_gpt`、`docs`、`outputs/remote_github_handoff_*`。

## 当前最先读的文件
1. `REMOTE_DELIVERY_20260424.md`
2. `REMOTE_CLAUDE_DIRECTION_REQUEST_20260424.md`
3. `REMOTE_HOLDING_PATTERN_V2_20260423.md`
4. `REMOTE_TASK_QUEUE_V5_20260422.md`

## 当前 authoritative 文件
0. `REMOTE_DELIVERY_20260424.md`
   - 远端 2026-04-24 delivery 原始留存：mixed-NL abandoned, domain randomization best, r40 fresh 54.69%.
0. `REMOTE_CLAUDE_DIRECTION_REQUEST_20260424.md`
   - 本地给 Claude 的方向裁决请求：远端 r40 路线与本地 post-fix rerun 路线冲突，需先裁决再给远端新任务。
1. `REMOTE_PARITY_REPORT_20260422.md`
   - 远端最新 parity 报告原始留存。
2. `REMOTE_REPLY_TO_PARITY_REPORT_20260422.md`
   - 本地对这份 parity 报告的正式回复。
3. `REMOTE_RESULTS_V3_UPDATE2_20260422.md`
   - 远端 V3 Update 2 的完整结果表和当前解释。
4. `REMOTE_TASK_QUEUE_V4_20260422.md`
   - 收到 parity 报告后的更新任务队列。
5. `REMOTE_PARITY_AND_LOCAL_STATE_20260422.md`
   - 本地 authoritative 基线、parity 关键点、与远端当前差异。
6. `REMOTE_EVIDENCE_PACKAGE_SPEC_20260422.md`
   - 远端回传最小证据包规范。
7. `REMOTE_REPLY_AND_NEXT_TASKS_20260422.md`
   - 可直接发给远端的回复 + 新任务说明。
8. `REMOTE_ANSWER_TO_4_PARITY_QUESTIONS_20260422.md`
   - 对远端 4 个 parity 问题的逐条 authoritative 回答。
9. `REMOTE_LOCAL_SOURCE_AUDIT_20260422.md`
   - 本地源码审计结论摘要，以及已应用的本地修复。
10. `REMOTE_REPLY_TO_PARITY_FOLLOWUP_20260422.md`
   - 对远端 follow-up parity 问题的正式回复；包含 corrected semantics 下的 A/B/C/D 实验建议。

## 关键结论
- 远端 `V3 Update 2` 已经显示出一个明确的新方向：**intra-epoch D2D domain randomization** 可能比单纯提高 surrogate 阶数更有信息增益。
- 最新 parity 报告表明：`delta_g_eff` 语义和 `conv` fix 不是解释远端 `27.86%` parity anchor 的主因。
- 之后的本地源码审计又确认：higher-order wrapper 里确实存在一个会影响 parity 解释的本地语义问题，但它主要影响 `J1d/K2/K3/K4` 这条诊断分支，不直接推翻主论文主结论。
- 但远端结果还不能直接等同于本地 canonical `J1d`，因为 parity 仍未完全打平。
- 本地 authoritative 结果当前是：
  - `K2 = 38.95 ± 9.85%`
  - `K3` 全 sweep 为负结果，最好点 `0.05 -> 36.21 ± 9.61%`
  - 本地 `K4 alpha=0.0` fresh 为 `33.28 ± 9.02%`
  - 本地 `K4 alpha=0.0/0.25` 的 epoch-0 test 仍是 `83%+`

## GitHub 远端 handoff
- GitHub account / username: `Leslie360`
- repo: `https://github.com/Leslie360/HAT.git`
- branch: `remote-exploration`
- last synced local note: key source + parity artifacts 已补到 handoff 分支。

## 上游来源
如需追源，优先看：
- `report_md/_gpt/CODEX_RESPONSE_TO_REMOTE_V3_20260422.md`
- `report_md/_gpt/CODEX_REMOTE_PARITY_TRIAGE_20260422.md`
- `report_md/_gpt/CODEX_CX_K2_SUMMARY.md`
- `report_md/_gpt/CODEX_CX_K3_INTERPRETATION_20260422.md`
- `report_md/_gpt/CODEX_K4_K5_PROVENANCE_AUDIT_20260422.md`
- `logs/_gpt/cx_k4_alpha_tmux_20260422.log`

## GitHub branch status
- Repo: https://github.com/Leslie360/HAT.git
- Branch: remote-exploration
- Latest remote-exploration head: 50863aa
- This branch is now the primary remote execution mirror.

- `REMOTE_REPLY_TO_PARITY_DISSECTION_20260422.md` — local response after confirming the additional STE multiplier bug; reclassifies the remote parity-dissection ceiling as pre-fix/provisional.

- `REMOTE_LOCAL_PARITY_REANCHOR_20260422.md` — corrected local 4-probe parity anchor after the config-sharing and STE-multiplier fixes.

- `REMOTE_ROUTE_DECISION_20260422.md` — authoritative statement that the mainline route is now uniform-NL + domain randomization; mixed-NL is demoted to a diagnostic branch.

- `REMOTE_TASK_QUEUE_V5_20260422.md` — corrected remote queue aligned to the chosen mainline route.

- `REMOTE_REPLY_AND_NEXT_TASKS_V2_20260422.md` — concise remote-facing reply reflecting the corrected local parity re-anchor and the new route choice.

## 2026-04-22 Late Arbitration Freeze
- Local execution is temporarily frozen on the corrected-mainline queue pending a `STE` semantics arbitration.
- Do **not** treat any post-22:35 local corrected cadence output as authoritative until the arbitration memo closes.
- Canonical local arbitration docs now live under `report_md/_gpt/STE_SEMANTICS_ARBITRATION_TASKBOARD_20260422.md` and `report_md/_gpt/CODEX_STE_SEMANTICS_EVIDENCE_PACK_20260422.md`.

## 2026-04-23 00:24 CST runtime note
- `K4R` is genuinely live on Branch A canonical code.
- Do **not** cite `cx_k4_train_k4_alpha_0p25.json` / `cx_k4_eval_k4_alpha_0p25.json` as current K4R results; they predate the live run and are stale pre-Branch-A artifacts.
- Current authoritative evidence is the live log `logs/_gpt/cx_k4r_alpha_0p25_20260422_231615.log` plus live checkpoints until canonical fresh-eval reruns.

## 2026-04-23 00:35 CST hold note
- Remote is in an explicit no-new-jobs holding pattern while local `K4R` is still live.
- Read `REMOTE_HOLDING_PATTERN_20260423.md` before launching anything.

## 2026-04-23 11:50 CST status update
- `K4R` source training completed successfully, but fresh-instance eval is poor (`34.99 +- 10.70`) and current `Gemini` coefficient ruling marks this run invalid as a canonical Branch A anchor.
- Local active GPU focus has shifted to `P1-C` (first-order only) and `P1-C2` (comparison path).
- Treat `BROADCAST_BRANCH_A_SCRUB_COMPLETE_20260423.md` as partial history; for current state prefer the newer disaster + coefficient-ruling documents.

## 2026-04-23 12:06 CST stop-loss confirmed
- `P1-C` and `P1-C2` have been stopped locally.
- There is currently no active canonical GPU run.
- Remote should follow `REMOTE_HOLDING_PATTERN_V2_20260423.md` until a post-fix rerun queue is issued.

## 2026-04-24 remote delivery received
- Remote delivered `DELIVERY — 2026-04-24`.
- Remote conclusion:
  - mixed-NL should be abandoned;
  - domain randomization is the best remote route;
  - `r40 replica` reports `90.03%` source / `54.69% +- 9.75%` fresh;
  - `r50v2`, `r10`, and `r50` are weaker but still informative.
- Remote requests local application of:
  - config-sharing fix;
  - LTP/LTD swap fix.
- Local status:
  - LTP/LTD branch mapping was already fixed;
  - conversion-site config-copy patch has now been applied to `analog_layers.py` and `analog_layers_ensemble.py`;
  - related tests pass.
- Holding policy remains active until Claude chooses the main direction, because local 2026-04-24 post-fix reruns now show much stronger fresh numbers but still require provenance review.

## 2026-04-24 M-series queue prepared
- Remote remains non-running unless the user explicitly releases it.
- Prepared packet: `REMOTE_TASK_QUEUE_20260424_M_SERIES_EXPLORATION.md`.
- Once released, priority is:
  - R-M0 source parity gate;
  - R-M1 Standard HAT V3 true train/eval NL=2.0 seed 123;
  - R-M2 Ensemble HAT V4 true train/eval NL=2.0 seed 123;
  - R-M3 Proportional HAT V4 true train/eval NL=2.0 seed 123;
  - R-M4 Proportional seed 456 only if R-M3 is useful.
