# coordination/

Current agent coordination and task routing lives here. Old agent Markdown should not accumulate in active paths.

## Subdirectories

| Subdir | Purpose | Retention rule |
|:--|:--|:--|
| `active/` | Current live coordination files | Keep small: current sync, current task file, broadcast symlink, active layout plan. |
| `dispatches/` | Phase dispatches by project phase | Keep recent/current dispatches; archive old rounds after freeze. |
| `audits/` | Review/audit outputs by reviewer/agent | Keep current audits relevant to active Paper1/Paper2/thesis lanes. |
| `agent_reports/` | Agent-specific reports | Keep recent reports; archive old historical reports. |
| `remote_tasks/` | Remote machine tasklists and ingestion notes | Keep current 105/107 tasklists findable. |

## Active files

- `active/AGENT_SYNC_gpt.md` — deprecated compatibility stub; do not append new work here.
- `active/CLAUDE_TASK_gpt.md` — current short task file for Codex/GPT handoff compatibility.
- `active/NEXT_WORK_MASTER_TASKLIST_20260510.md` — current post-release workstream tasklist.
- `active/broadcast.md` — symlink to `/home/qiaosir/projects/BROADCAST.md`.
- `active/COMPUTE_VIT_IDEAL_LAYOUT_PLAN_20260510.md` — ideal layout and migration plan.

## Rules

- Do not create new root-level broadcast files.
- Put cross-agent broadcast entries in `/home/qiaosir/projects/BROADCAST.md`.
- Keep current tasking in short scoped files, not the deprecated sync log.
- Archive old agent Markdown with a manifest and restore script.
- Paper-specific reports should live under the matching product lane when possible.
