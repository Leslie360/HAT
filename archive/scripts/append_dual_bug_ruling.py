import os

sync_file = 'compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md'
task_file = 'compute_vit/report_md/_gpt/CLAUDE_TASK_gpt.md'

status_block = """
## [Gemini] 2026-04-23 12:45 — Final Ruling on Dual-Bug Recovery
### Topic
- Closing the theory gap for branch-swap and second-order coefficient fixes.

### Status
- **RULING:** Positive grad_output must map to ltd_scale. In SGD/Adam, positive gradients induce a decrease in weight magnitude (LTD).
- **RULING:** Second-order coefficient must be strictly (NL-1). The NL prefactor was a mathematical error.
- **RULING:** Both fixes must land in a single atomic commit.
- **ALL THEORY TASKS COMPLETE.** Gemini returning to standby support mode.

### Evidence
- `report_md/_gpt/GEMINI_DUAL_BUG_FINAL_RULING_20260423.md`
"""

for fpath in [sync_file, task_file]:
    if os.path.exists(fpath):
        with open(fpath, 'a', encoding='utf-8') as f:
            f.write(status_block)
print("Sync block added.")
