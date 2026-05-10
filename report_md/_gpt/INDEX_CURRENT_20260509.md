# Current Report Index

Date: 2026-05-09
Purpose: Compatibility index after R3 report/coordination migration.

## Active files kept here

- `AGENT_SYNC_gpt.md` — active multi-agent sync log
- `CLAUDE_TASK_gpt.md` — active Claude/Codex task entry
- `FILE_PURPOSE_INVENTORY_20260509.tsv` — machine-readable full file inventory
- `FILE_PURPOSE_INVENTORY_SUMMARY_20260509.md` — inventory summary
- `ROOT_ENTRY_PURPOSE_MAP_20260509.md` — root entry purpose map

## Paper-1 reports moved to `paper1/reports/`

| Phase | Location |
|---|---|
| P6 Kimi reports | `paper1/reports/P6/KIMI/` |
| P6 DS audits | `paper1/reports/P6/audits/DS/` |
| P6 Mimo audits | `paper1/reports/P6/audits/MIMO/` |
| P6 Codex acceptance | `paper1/reports/P6/acceptance/` |
| P7 Kimi reports | `paper1/reports/P7/KIMI/` |
| P7 DS audits | `paper1/reports/P7/audits/DS/` |
| P7 Mimo audits | `paper1/reports/P7/audits/MIMO/` |
| P7 Codex acceptance | `paper1/reports/P7/acceptance/` |
| P8 Kimi reports | `paper1/reports/P8/KIMI/` |
| P8 Claude/self-cleanup audits | `paper1/reports/P8/audits/Claude/` |

## Coordination moved to `coordination/`

| Type | Location |
|---|---|
| P6 dispatch | `coordination/dispatches/P6/` |
| P7 dispatch | `coordination/dispatches/P7/` |
| P8 dispatch | `coordination/dispatches/P8/` |
| Remote 105 P8 task | `coordination/remote_tasks/105/` |
| Remote 107 P8 task | `coordination/remote_tasks/107/` |
| Codex protocol/review notes | `coordination/audits/Codex/` |
| Claude broadcast note | `coordination/agent_reports/Claude/` |

## Residual old files archived

Residual simulated files, beamer build outputs, old validation JSONs, and old 6-bit repair side reports were moved to:

`archive/reorg_20260509/report_md_residuals/`

Restore script:

`archive/reorg_20260509/restore/R3_REPORT_MD_RESIDUALS_RESTORE.sh`

## Restore current migration

P6/P7/P8 report migration restore script:

`archive/reorg_20260509/restore/R3_REPORTS_COORDINATION_RESTORE.sh`
