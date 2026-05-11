# Codex Command Dashboard

Date: 2026-05-10; refreshed by Claude on 2026-05-11
Owner: Claude single-commander unless user reassigns
Mode: Local execution with external agents only on explicit handoff

## High-level status

| Lane | Status | Current decision |
|---|---|---|
| Paper1 | Final narrative polish complete; release refreshed | Current external tarball SHA is `343ae03de1dfd9c198ae614548dee14bddf04131e160598bc064f5d8544500f6`; do not reopen unless user asks. |
| Workspace cleanup | Commit-prep pending | No commit or push without explicit user approval; stage exact path groups only. |
| Paper2 / 107 | 410M claim-lock package completed; 107-clean push reviewed through `19038b2`; figure-led draft polished | Use only `paper2/manuscript/source_data/remote107_selective_kv_claim_lock_20260511/` for current claim-bearing Paper2 layer-scope evidence; Qwen3-VL/2.8B/6.9B remain validation lanes until claim-locked. |
| Local GPU / Paper3 | Spatial variance 10×3 and retention×protection 10×3 completed on seed789 | GPU is free only after a fresh `nvidia-smi` check; treat completed floorplan/retention results as provisional synthetic/simulator evidence. |
| Thesis | CN/EN/XJTU lanes active; XJTU format check updated | Formal metadata remains deferred; XJTU submission lane builds with placeholder metadata, and residual issues are font/bibliography line-breaking rather than unresolved content edits. |

## Current command priorities

1. Keep Paper2/107 claim-bearing rows restricted to the 2026-05-11 Remote107 source-data package; 107-clean scale-up/Qwen3-VL pushes stay provisional until claim-locked.
2. Keep local cache-path, retention/refresh, and offline reconstruction results engineering-only.
3. Retention×protection 10×3 expansion completed: 270 raw rows plus summary/plot. Keep it provisional simulator-retention evidence and run `nvidia-smi` before choosing the next GPU lane (drift-aware SAM, measured-profile/floorplan extension, or CNN-vs-ViT).
4. Keep Paper1 release frozen unless the user asks for another author wording pass or submission packaging. Latest marker recheck found no `TinyImageNet` or `ion. n.` residue; KV-cache appears only as a separate Work-2 boundary note.
5. Push only after explicit user approval.

## Active coordination files

| File | Purpose |
|---|---|
| `coordination/active/CLAUDE_TASK_gpt.md` | Current short task handoff. |
| `coordination/active/NEXT_WORK_MASTER_TASKLIST_20260510.md` | Master workstream map and experiment closure status. |
| `report_md/_gpt/CANONICAL_EVIDENCE_LEDGER_20260510.md` | Current claim-to-artifact ledger. |
| `/home/qiaosir/projects/BROADCAST.md` | Append-only workspace broadcast. |
| `paper2/manuscript/source_data/remote107_selective_kv_claim_lock_20260511/` | Claim-bearing Paper2 source-data package. |

## Hard boundaries

- No `git push` without explicit user approval.
- No broad `git add -A`.
- No Paper1 release refresh unless a scoped review finding is integrated first.
- No edits inside `/home/qiaosir/projects/remote_reviews/105` or `/home/qiaosir/projects/remote_reviews/107`.
- No checkpoint/data moves or copies unless required by the active task and recorded in the ledger.
- No additional GPU training/eval job unless a fresh `nvidia-smi` capacity check passes.

## Watch items

| Item | Why it matters | Action |
|---|---|---|
| Legacy 107 blocked wording | It predates the 2026-05-11 claim-lock package | Treat as historical only; do not let it override the new source-data package. |
| Gemini-era 107 figures | Generated from candidate/audit lanes | Regenerate from the 2026-05-11 package before manuscript claim use. |
| Local KV probes | Useful cache-path debugging but protocol differs from Remote107 | Use only as methods/supplementary engineering evidence. |
| Root `BROADCAST.md` | Volatile coordination file | Keep updates concise and searchable. |
| Thesis formal metadata | Advisor, department, degree wording, university, and official date still need confirmation | Do not invent these values; fill only after user/university confirmation. |

## Integrated 107 decision

Historical strict-review decision:

`107 CLAIM LOCK BLOCKED - RERUN/MANIFEST REQUIRED`

Current superseding state: the 2026-05-11 Remote107 selective-KV package contains 41/41 archived original JSON artifacts, manifest/report, aggregate summary, regenerated figure, and source-data package. It is canonical for the narrow claim that terminal-layer selective analog KV remains viable under the locked protocol and all-layer analog KV is rejected as the main route.

## Next actions

1. Keep Paper2 manuscript claims tied to the 2026-05-11 source-data package.
2. Spatial variance 10×3 expansion is closed; ledger and broadcast should stay synchronized with the provisional synthetic floorplan interpretation.
3. Retention×protection 10×3 expansion is closed: 270 raw rows plus summary/plot. Next GPU choice is drift-aware SAM, measured-profile/floorplan extension, or CNN-vs-ViT after a fresh GPU capacity check.
4. Decide later whether to convert the figure-led Paper2 draft into the formal manuscript template.
