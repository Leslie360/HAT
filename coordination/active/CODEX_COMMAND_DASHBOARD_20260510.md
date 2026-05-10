# Codex Command Dashboard

Date: 2026-05-10
Owner: Codex commander
Mode: Parallel with separate CC model

## High-level status

| Lane | Status | Codex decision |
|---|---|---|
| Paper1 | Final narrative polish complete; release refreshed | Current external tarball SHA is `343ae03de1dfd9c198ae614548dee14bddf04131e160598bc064f5d8544500f6`; release directory manifest and cold-unpack manifest checks pass. |
| Workspace cleanup | Commit-prep pending | No commit or push without explicit user approval; stage exact path groups only. |
| Paper2 / 107 | Claim lock blocked after CC harvest | Do not draft claims; request signed manifest or minimal corrected-noise rerun. |
| Remote 105 | Supplement/defense only | Not a Paper1 submission blocker. |
| Thesis | CN and EN compiled after CC EN prose-flow plus Codex layout polish | PDFs rebuilt; no active old-claim hits and no current overfull hbox entries. |

## Current command priorities

1. Keep Codex and CC write scopes disjoint.
2. Keep Paper2/107 audit-only after CC confirmed metadata remains incomplete.
3. Send the remote 107 manifest/minimal-rerun request if/when the user wants Paper2 unblocked.
4. Keep Paper1 release frozen unless the user asks for another author wording pass or submission packaging.
5. Keep thesis integration focused on formal metadata/layout polish, not claim changes.
6. Push only after explicit user approval.

## Active coordination files

| File | Purpose |
|---|---|
| `coordination/active/CODEX_CC_PARALLEL_WORKPLAN_20260510.md` | No-conflict ownership map. |
| `coordination/remote_tasks/107/CC_107_REMOTE_METADATA_HARVEST_TASKLIST_20260510.md` | Tasklist for the separate CC model. |
| `coordination/remote_tasks/107/CODEX_107_EVIDENCE_GATE_LEDGER_20260510.md` | Current 107 evidence gate state. |
| `coordination/remote_tasks/107/CODEX_107_METADATA_ACCEPTANCE_PROTOCOL_20260510.md` | Codex acceptance rules for CC findings. |
| `coordination/remote_tasks/paper1/CC_PAPER1_AUTHOR_REVIEW_TASKLIST_20260510.md` | New read-only Paper1 review task for CC. |
| `coordination/agent_reports/Codex/CODEX_PAPER1_POST_BROADCAST_RELEASE_20260510.md` | Paper1 post-broadcast fix and release-refresh report. |
| `coordination/agent_reports/Codex/CODEX_THESIS_POST_CC_INTEGRATION_20260510.md` | Thesis integration report after CC EN prose-flow pass. |

## Hard boundaries

- No `git push` without explicit user approval.
- No broad `git add -A`.
- No Paper1 release refresh unless Codex integrates a scoped review finding first.
- No edits inside `/home/qiaosir/projects/remote_reviews/105` or `/home/qiaosir/projects/remote_reviews/107`.
- No checkpoint/data moves or copies.
- No GPU training/eval jobs unless the user explicitly asks.

## Watch items

| Item | Why it matters | Action |
|---|---|---|
| `paper2/results/METADATA_COMPLETENESS_107_20260510.tsv` | Appeared as untracked while parallel work is active | Do not overwrite; identify producer before integrating. |
| Gemini 107 "locked" broadcasts | Superseded by strict review | Treat as invalid for claim drafting. |
| `paper2/src/plot_107_results.py` | Generates audit plots only | Do not cite figures as manuscript evidence yet. |
| Root `BROADCAST.md` | Volatile coordination file | Keep updates concise and searchable. |
| Thesis formal metadata | Advisor, department, degree wording, university, and official date still need confirmation | Do not invent these values; fill only after user/university confirmation. |

## Integrated 107 decision

CC report integrated:

`107 CLAIM LOCK BLOCKED - RERUN/MANIFEST REQUIRED`

Reason: recovered facts are useful for planning, but no per-row producing commit, exact command, complete eval protocol, checkpoint SHA-256, or safe old-vs-corrected matched table exists in the local legacy JSON package.

## Next Codex actions

1. Keep Paper2/107 figures and TSVs audit-only.
2. Use `coordination/remote_tasks/107/REMOTE_107_METADATA_RECOVERY_OR_MINIMAL_RERUN_REQUEST_20260510.md` to unblock Paper2 when remote execution/manifest is available.
3. Treat Paper1 as release-refreshed after final narrative polish; next Paper1 action is only user-approved submission packaging or explicit wording changes.
4. For thesis, keep content/claim lock; only formal metadata confirmation remains before official submission.
