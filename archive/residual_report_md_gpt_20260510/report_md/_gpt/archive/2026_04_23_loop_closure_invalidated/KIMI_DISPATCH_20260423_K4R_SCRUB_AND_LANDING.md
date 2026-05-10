<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Kimi Dispatch — K4R Scrub And Landing (2026-04-23)

## Context
- Branch A is now the canonical path.
- `K4R` is the first live canonical Branch A run.
- Current live evidence comes only from:
  - `logs/_gpt/cx_k4r_alpha_0p25_20260422_231615.log`
  - `checkpoints/_gpt/cx_k4_alpha/k4_alpha_0p25/*`
- The following artifacts are stale pre-Branch-A files and must not be cited as K4R outputs:
  - `report_md/_gpt/json_gpt/cx_k4_train_k4_alpha_0p25.json`
  - `report_md/_gpt/json_gpt/cx_k4_eval_k4_alpha_0p25.json`
  - `report_md/_gpt/csv_gpt/cx_k4_train_k4_alpha_0p25.csv`
  - `report_md/_gpt/cx_k4_train_k4_alpha_0p25.md`

## Your role
You are NOT doing theory. You are NOT designing new experiments. You are doing contamination scrub + canonical landing support.

## Deliverables
Produce exactly these 3 files:

### 1. `KIMI_K4R_CONTAMINATION_SWEEP_20260423.md`
Goal:
- identify every file that still risks citing stale `k4_alpha_0p25` outputs as if they were live Branch A K4R outputs.

Required structure:
- `Must-correct now`
- `Can remain as historical log`
- `Already safe`

For each `Must-correct now` item include:
- path
- exact risky phrase / numeric claim
- replacement wording

### 2. `KIMI_K4R_COMPLETION_PACKET_20260423.md`
Goal:
- prepare the canonical completion packet structure for when K4R finishes.

Include placeholders only for:
- train best acc / best epoch
- final train acc / final test acc
- fresh-instance mean/std
- interpretation bucket:
  - `supports uniform-NL route strongly`
  - `supports route weakly`
  - `re-open route decision`

Important:
- do NOT invent numbers
- do NOT copy stale `44.29 +- 13.78`

### 3. `KIMI_BRANCH_A_DOC_PATCHLIST_20260423.md`
Goal:
- list the specific Branch A-facing docs that should be patched after K4R completes.

At minimum audit:
- `REMOTE_HANDOFF_PACKET_20260422.md`
- `REMOTE_ROUTE_DECISION_20260422.md`
- `REMOTE_REPLY_AND_NEXT_TASKS_V2_20260422.md`
- `CODEX_ROUTE_DECISION_20260422.md`
- `远端/INDEX.md`

For each file say:
- `patch after K4R`
- `leave as historical`
- `add errata header only`

## Hard rules
- Do not discuss first-order multiplier theory.
- Do not discuss second-order coefficient derivation.
- Do not propose new GPU experiments.
- Do not treat stale JSON as reusable evidence.
