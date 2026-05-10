# Codex Execution Scope (2026-04-23)

## Role
Codex is execution-only for the current phase.

## Do now
- keep GPU idle
- keep remote in holding pattern
- wait for:
  - `KIMI_RECOVERY_MASTER_STATUS_20260423.md`
  - `KIMI_DOC_PATCH_PRIORITY_20260423.md`
  - `KIMI_MINIMAL_RERUN_REQUIREMENTS_20260423.md`
  - `GEMINI_DUAL_BUG_FINAL_RULING_20260423.md`

## Then do
1. patch local code once
2. add/adjust tests once
3. run minimal smoke pair
4. run first clean canonical rerun only after smoke passes

## Do not do now
- no new GPU experiments
- no remote launches
- no manuscript numeric updates
