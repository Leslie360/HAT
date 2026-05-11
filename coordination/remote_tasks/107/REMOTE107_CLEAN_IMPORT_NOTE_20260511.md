# Remote107 Clean Import Note

Date: 2026-05-11
Source branch: `origin/107-clean` at `aa6b597` (`docs: add core conclusions summary (2026-05-11)`)
Import mode: selective snapshot only; no whole-branch merge.

## Why not merge the branch wholesale

`origin/107-clean` is not a narrow result branch relative to the active `paper1-release-20260501` workspace. Its diff includes large root-level restructuring, many deletions under archive/coordination, and duplicated top-level code paths. A direct merge would risk overwriting the current thesis/Paper1/Paper2 organization and remote-task files.

## Files imported locally

- `coordination/remote_tasks/107/REMOTE107_CLEAN_CONCLUSIONS_20260511.md`
- `coordination/remote_tasks/107/REMOTE107_CLEAN_RESULTS_SUMMARY_20260511.md`
- `coordination/remote_tasks/107/REMOTE107_CLEAN_K107_CANONICAL_FREEZE_20260508.md`
- `paper2/results/REMOTE107_CLEAN_K107_CANONICAL_SUMMARY_20260511.csv`
- `paper2/results/REMOTE107_CLEAN_K107_PLOT_READY_20260511.json`

## Protocol caution

The imported Remote107 clean packet uses a canonical Pythia-410M protocol with WikiText-2 test split, context length 512, stride 256, batch size 1, and digital baseline PPL `22.1849`. This differs from the earlier local Remote 107 audit tables using digital reference PPL `15.68`. Do not mix the two baselines in the same claim table without explicitly labeling protocol differences.

## Current usable takeaways

- The clean packet supports a last1/last2 selective-KV direction under its own protocol: last1 D2D=0.02 is `19.451 ± 0.065`, last2 D2D=0.02 is `20.142 ± 0.052`, and all-layer analog is much worse (`37.132 ± 0.878`).
- It adds scale checks for Pythia-1B and Pythia-2.8B, plus EPSC/C2C stress summaries.
- It should be treated as a remote-return snapshot until its JSON sidecars and metadata are mapped into the active Paper2 manifest format.

## Next audit step

Use `coordination/remote_tasks/107/REMOTE_107_SELECTIVE_KV_CLAIM_LOCK_TASK_20260511.md` for Remote 107 follow-up. The acceptance gate remains: claim rows need source-backed commit, command, dataset/split, eval protocol, checkpoint hash, analog-layer list, seed semantics, and corrected-noise code path.
