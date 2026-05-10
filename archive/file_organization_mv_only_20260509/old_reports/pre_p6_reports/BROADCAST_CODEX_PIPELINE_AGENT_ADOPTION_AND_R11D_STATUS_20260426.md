# BROADCAST — Pipeline Agent Adoption + R11D Status
**Date:** 2026-04-26 19:25 CST
**From:** Codex
**To:** Claude / Kimi / Gemini / DeepSeek / Remote
**User update:** User has created a local pipeline agent system documented in `/home/qiaosir/projects/流水线.md`.

## 1. New coordination rule
Read `/home/qiaosir/projects/流水线.md`.

Future task coordination should default to the local pipeline agent instead of manually splitting work by role in chat.

Key commands:
```bash
agents-up
agents-do path/to/task.md
agents-down
```

For this project, preferred working directory:
```bash
cd /home/qiaosir/projects/compute_vit
WORK_DIR=/home/qiaosir/projects/compute_vit agents-up
agents-do path/to/task.md
```

Pipeline architecture:
```text
user -> kimi planner -> ds_flash coder -> codex reviewer -> gemini critic -> kimi_cli doc
```

Broadcast bus:
```text
$WORK_DIR/broadcast.md
```

Outputs:
```text
$WORK_DIR/outputs/<task_id>.md
```

Fallback tiers:
- Tier 1: `CODE=ds_flash REVIEW=codex CRITIC=gemini_pro`
- Tier 2: `REVIEW=double` if Codex quota is low
- Tier 3: `CODE=kimi REVIEW=kimi CRITIC=kimi`

Operational meaning for this project:
- User can provide one task once.
- Codex should not manually decompose Kimi/DS/Gemini assignments unless debugging, emergency GPU control, or pipeline failure requires intervention.
- Existing manual R11D GPU jobs remain under direct tmux control until they finish; do not migrate a running GPU process mid-run.

## 2. R11D-1 final result
R11D-1 AIHWKit 4-bit completed.

Training:
- output dir: `paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/`
- best source/test accuracy: **15.01%**
- early stopped at epoch 21
- final epoch: train **10.144%**, test **10.09%**

Fresh eval:
- file: `paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/fresh_eval.json`
- protocol: 10 fresh instances × 5 MC repeats
- fresh mean: **14.6368%**
- fresh std across instances: **0.1059%**

Verdict: AIHWKit collapses under 4-bit precision in this setup. This is strong Path-C evidence that the operating-envelope story matters.

## 3. R11D-2 duplicate-contamination event
Detected two concurrent R11D-2 processes writing the same directory:
```text
paper2_aihwkit_baseline/checkpoints/r11d_2_sigma020/
```

Sources:
- Codex queued process: `r11d_2_sigma020`
- Claude-launched process: `r11d2_sigma020`

Because both wrote the same `best.pt`, that directory is contaminated and must not be used for final claims.

Marker written:
```text
paper2_aihwkit_baseline/checkpoints/r11d_2_sigma020/CONTAMINATED_DO_NOT_USE.md
```

Both conflicting processes were stopped.

## 4. Clean R11D-2 replacement
Clean replacement launched in a fresh directory.

Session:
```bash
tmux attach -t codex_r11d23_clean
```

Output:
```text
paper2_aihwkit_baseline/checkpoints/r11d_2_sigma020_clean/
```

Log:
```text
paper2_aihwkit_baseline/logs/r11d_2_sigma020_clean_20260426_192045.log
```

If clean R11D-2 fresh mean is >80%, the same clean queue launches conditional R11D-3:
```text
paper2_aihwkit_baseline/checkpoints/r11d_3_sigma030_clean/
```

## 5. Required alignment
- Do not use `r11d_2_sigma020/` for paper numbers.
- Do not start another local R11D-2 in the same save dir.
- Future high-level multi-agent tasks should be submitted through `agents-do` unless explicitly marked as direct/manual GPU control.
