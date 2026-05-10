# Auto-Finalize Dry Run — 2026-04-18

## Scope

Round F `CX-T` required a health-check of `scripts/_gpt/auto_finalize_nl_ablation.py` before the live `attn_proj-only` lane completes.

## Initial finding

The original script was **not a real finalize hook**. It only:
- loaded the lane JSONs,
- printed a console summary,
- exited without modifying any downstream artifacts.

That meant the advertised auto-finalize path would have silently failed to update:
- `report_md/_gpt/SUPP_TABLE_NL_ABLATION_SCAFFOLD.md`
- `report_md/_gpt/NL_LANE_RESULTS_20260418.md`
- `report_md/_gpt/CLAUDE_A_DECISION_FINAL_20260418.md`

## Fix applied

`auto_finalize_nl_ablation.py` now:
1. supports `--dry-run`
2. supports `--attn-proj-json <path>` for synthetic completion tests
3. computes the `attn_proj-only` row update
4. updates the three downstream markdown targets above
5. emits a concise broadcast snippet for `AGENT_SYNC_gpt.md`
6. writes a unified diff preview via `--diff-out`

## Synthetic completion event used for dry-run

A synthetic `attn_proj-only` completion JSON was created with the currently observed partial lane values from the live log:
- `best_test_acc = 18.86`
- `best_epoch = 0`
- `final_test_acc = 11.41`

This is **not** treated as a locked scientific result. It was used only to validate the finalize path.

## Dry-run command

```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python   scripts/_gpt/auto_finalize_nl_ablation.py   --dry-run   --attn-proj-json /tmp/attn_proj_synthetic_completion.json   --diff-out report_md/_gpt/AUTO_FINALIZE_DRYRUN_DIFF_20260418.patch
```

## Result

Dry-run passed. The hook now previews the expected updates to:
- `SUPP_TABLE_NL_ABLATION_SCAFFOLD.md`
- `NL_LANE_RESULTS_20260418.md`
- `CLAUDE_A_DECISION_FINAL_20260418.md`

No files were modified during the dry-run.

## Key validation conclusion

`CX-T` is now in acceptable shape: when the real `attn_proj-only` JSON lands, the finalize script can be run as an actual update path instead of a no-op.

## Remaining limitation

The current finalize path is still **manual-trigger** rather than a daemonized watcher. Round F's passive `CX-U` still requires a monitor step to invoke the script once `attn_proj-only` genuinely finishes.
