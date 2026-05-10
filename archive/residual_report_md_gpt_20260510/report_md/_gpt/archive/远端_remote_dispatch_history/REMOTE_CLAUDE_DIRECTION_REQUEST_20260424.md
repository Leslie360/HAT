# Remote-Claude Direction Request 2026-04-24

## Why This Exists

Remote returned a clean delivery packet on 2026-04-24. It conflicts with the newest local post-fix rerun stream. Before any new remote compute is launched, Claude needs to choose the main direction.

## Remote Position

Remote's recommendation:

- Abandon mixed-NL.
- Promote domain randomization.
- Best remote result: `r40 replica`, source `90.03%`, fresh `54.69% +- 9.75%`.
- Safe fallback: ALL-linear uniform `NL=1.0`, source about `89.93%`, but fresh about chance.

Remote code fixes:

- Config sharing fixed by per-layer `copy.copy(config)`.
- LTP/LTD swap fixed by mapping positive gradient to LTD and negative gradient to LTP.

## Local Position As Of 2026-04-24

Local has applied the config-copy conversion patch and already had the LTP/LTD mapping fix.

Local post-fix evidence:

| Local result | Same-instance | Fresh | Status |
|:--|--:|--:|:--|
| Uniform Ensemble HAT | `82.26% @ epoch 41` metadata | `81.6948% +- 0.6381%` | Cross-reviewed, but earlier broadcast wording stale |
| Uniform Standard HAT | `83.27% @ epoch 86` | `82.6346% +- 0.5624%` | JSON/log evidence; formal review pending |
| Proportional HAT | `91.10% @ epoch 95` | `90.8766% +- 0.1089%` | Strongest number; config-consistency review pending |

Major caution:

- Proportional checkpoint metadata says `nl_ltp=1.0`, `nl_ltd=-1.0`, but fresh eval forced `NL=2.0/-2.0`. This may be a training-command/provenance issue or a checkpoint metadata issue. It must be resolved before citation.

## Decisions Claude Must Make

1. Does local post-fix HAT recovery supersede the old K2 structural-limit narrative?
2. Does remote `r40` remain useful as a domain-randomization comparison, or is it now a secondary/legacy line?
3. Should remote re-run a minimal canonical packet using the exact local post-fix code and commands?
4. What is the canonical Work 1 paper story now:
   - structural limit under corrected code,
   - HAT recovery under corrected code,
   - domain-randomization recovery,
   - proportional-noise recovery,
   - or a split story by noise law?
5. What is the minimum evidence threshold before paper-1 rewrite resumes?

## Recommended Interim Policy

Until Claude rules:

- No broad remote sweeps.
- Keep remote in holding pattern.
- Ask remote only for full evidence packets for `r40/r50/r10/r50v2` if needed:
  - exact commands,
  - git diff or patch,
  - JSON logs,
  - stdout logs,
  - checkpoint metadata,
  - per-instance fresh table,
  - md5/sha256 of code and checkpoints where possible.

## Files Claude Should Read First

1. `远端/REMOTE_DELIVERY_20260424.md`
2. `report_md/_gpt/BROADCAST_REMOTE_DELIVERY_20260424.md`
3. `report_md/_gpt/CODEX_CROSS_REVIEW_FRESH_EVAL_20260423.md`
4. `report_md/_gpt/json_gpt/postfix_ensemble_hat_v4_nl20_fresh_eval.json`
5. `report_md/_gpt/json_gpt/V3_hybrid_standard_noise_standard_train_best_fresh_eval.json`
6. `report_md/_gpt/json_gpt/V4_hybrid_standard_noise_hat_best_fresh_eval.json`
