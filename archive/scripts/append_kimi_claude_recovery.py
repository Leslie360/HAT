import os

sync_file = 'compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md'
task_file = 'compute_vit/report_md/_gpt/CLAUDE_TASK_gpt.md'

status_block = """
## [Kimi] 2026-04-23 12:55 — Post-Dual-Bug Recovery
### Topic
- Delivered recovery master status and document patch priorities.

### Status
- **INVALIDATED:** All pre-fix runs (K4R, P1-C, etc.).
- **DOC PATCHING:** Matrix established (what to patch now, what to hold).
- **RERUN SPEC:** Defined minimal gating requirements for the next canonical anchor.

### Evidence
- `report_md/_gpt/KIMI_RECOVERY_MASTER_STATUS_20260423.md`
- `report_md/_gpt/KIMI_MINIMAL_RERUN_REQUIREMENTS_20260423.md`

## [Claude] 2026-04-23 13:00 — Stop-loss Synthesis Prep
### Topic
- Synthesis template and patch gating matrix for the clean restart.

### Status
- **FROZEN:** All paper drafting is paused until the physical engine provides a clean empirical baseline.
- **RERUN:** Mandated a clean first-order-only anchor followed by an SO2 comparison run.

### Evidence
- `report_md/_gpt/CLAUDE_STOPLOSS_SYNTHESIS_TEMPLATE_20260423.md`
- `report_md/_gpt/CLAUDE_PATCH_GATING_MATRIX_20260423.md`
"""

for fpath in [sync_file, task_file]:
    if os.path.exists(fpath):
        with open(fpath, 'a', encoding='utf-8') as f:
            f.write(status_block)
print("Sync blocks added.")
