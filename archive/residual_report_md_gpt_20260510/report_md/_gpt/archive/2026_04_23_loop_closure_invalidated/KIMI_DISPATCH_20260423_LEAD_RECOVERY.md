<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Kimi Dispatch — Lead Recovery Owner (2026-04-23)

## Role
You are the primary owner of the current non-GPU recovery phase.
Codex is execution-only.
Gemini is support-only for the remaining theory gap.

## Current ground truth
- No active canonical GPU runs are alive.
- `K4R` is invalid as canonical anchor.
- `P1-C` and `P1-C2` were stop-loss runs and are no longer running.
- Dual-bug state currently assumed:
  1. branch-swap in LTP/LTD mapping
  2. extraneous `nl` multiplier in second-order coefficient

## Your mandate
Own the document/control-plane cleanup and the recovery plan framing.
Do not write code. Do not launch experiments.

## Deliverables
Produce exactly four files.

### 1. `KIMI_RECOVERY_MASTER_STATUS_20260423.md`
Single authoritative status sheet containing:
- what is invalid
- what survives
- what is frozen
- what the next minimal rerun must prove

### 2. `KIMI_DOC_PATCH_PRIORITY_20260423.md`
A concrete patch queue, grouped into:
- `patch immediately`
- `patch after local code fix`
- `patch only after first clean rerun`

Must include at least:
- `report_md/_gpt/CODEX_ROUTE_DECISION_20260422.md`
- `report_md/_gpt/KIMI_BRANCH_A_QUICK_REFERENCE_20260423.md`
- `report_md/_gpt/KIMI_PRE_SUBMISSION_CHECKLIST_20260423.md`
- `远端/REMOTE_HANDOFF_PACKET_20260422.md`
- `远端/REMOTE_ROUTE_DECISION_20260422.md`
- `远端/INDEX.md`

### 3. `KIMI_MINIMAL_RERUN_REQUIREMENTS_20260423.md`
Define what the first clean rerun must include to count as canonical.
This is not an experiment proposal tree. It is a gating spec.
Required fields:
- exact artifact set
- exact metrics that must be returned
- exact provenance fields
- what cannot be omitted

### 4. `KIMI_PUBLIC_STATUS_WORDING_20260423.md`
Short wording blocks for:
- user-facing one paragraph summary
- remote-facing one paragraph hold message
- internal one paragraph "why nothing current is canonical"

## Hard rules
- No new theory derivation.
- No new experiment tree.
- No manuscript insertion prose.
- No rehabilitation of K4R/P1-C/P1-C2.
