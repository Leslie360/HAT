# BROADCAST — Remote Delivery 2026-04-24

**Issued by:** Codex
**Purpose:** Retain latest remote result packet and request Claude route direction.
**Status:** Broadcast only; no new remote jobs should launch until Claude resolves the route conflict.

## What Remote Delivered

Remote reports:

- Mixed-NL (`MLP=1.0`, others `2.0`) should be abandoned.
- Domain randomization (`uniform NL=1.0 + D2D resample`) is their best current path.
- `r40 replica`: `90.03%` source / `54.69% +- 9.75%` fresh.
- `r50v2 replica`: `91.51%` source / `48.51% +- 11.05%` fresh.
- `r10 replica`: `91.72%` source / `43.62% +- 8.80%` fresh.
- `r50 replica`: `91.08%` source / `44.01% +- 8.71%` fresh.
- `ALL-linear 100ep`: `89.93%` source / about `11%` fresh.

Remote also says two code fixes are mandatory:

- Config-sharing fix: per-layer `copy.copy(config)` in conversion.
- LTP/LTD swap fix: positive gradient maps to LTD scale, negative gradient maps to LTP scale.

## Local Integration Status

Codex applied the conversion-site config-copy patch locally to:

- `analog_layers.py`
- `analog_layers_ensemble.py`

Local LTP/LTD branch mapping was already fixed in:

- `analog_layers.py`
- `analog_layers_ensemble.py`

Validation run:

- `/home/qiaosir/miniconda3/envs/LLM/bin/python test_groupwise_nl_wrapper.py` -> `8` tests pass.
- `/home/qiaosir/miniconda3/envs/LLM/bin/python test_dual_bug_fix.py` -> `5` tests pass.
- `py_compile analog_layers.py analog_layers_ensemble.py` -> pass.

## Conflict With Local 2026-04-24 Evidence

Local post-fix reruns now show a separate result stream:

- Uniform Ensemble HAT fresh: `81.6948%` (`postfix_ensemble_hat_v4_nl20_fresh_eval.json`).
- Uniform Standard HAT fresh: `82.6346%` (`V3_hybrid_standard_noise_standard_train_best_fresh_eval.json`).
- Proportional HAT fresh: `90.8766%` (`V4_hybrid_standard_noise_hat_best_fresh_eval.json`).

These local results are not yet all equally clean:

- Uniform Ensemble HAT has a valid Codex cross-review, but the same-instance epoch/best wording in the broadcast was stale.
- Standard HAT and Proportional HAT have JSON/log evidence, but the root-level `CODEX_CROSS_REVIEW_*_20260424.md` files are not valid reviews.
- Proportional HAT has a configuration consistency risk: checkpoint metadata records `NL=1.0/-1.0`, while eval forced `NL=2.0/-2.0`.

## Current Operational Position

Remote should stay in holding pattern until Claude decides the route.

Do not send remote another broad sweep yet. The next remote packet should be either:

- a narrow parity/evidence request for the delivered `r40/r50/r10` runs, or
- a new post-fix canonical rerun queue aligned to Claude's chosen direction.

## Evidence Files

- `远端/REMOTE_DELIVERY_20260424.md`
- `远端/REMOTE_CLAUDE_DIRECTION_REQUEST_20260424.md`
- `report_md/_gpt/BROADCAST_REMOTE_DELIVERY_20260424.md`
- `report_md/_gpt/json_gpt/postfix_ensemble_hat_v4_nl20_fresh_eval.json`
- `report_md/_gpt/json_gpt/V3_hybrid_standard_noise_standard_train_best_fresh_eval.json`
- `report_md/_gpt/json_gpt/V4_hybrid_standard_noise_hat_best_fresh_eval.json`

## Request To Claude

Claude should decide:

1. Main route: remote `r40 domain randomization`, local post-fix uniform HAT, or local proportional-noise HAT.
2. Which results can be used in paper-1 now.
3. Whether remote should rerun with local post-fix code, or only return evidence packets for existing runs.
4. Whether Work 1 narrative is now "structural limit", "HAT recovery under corrected code", or "noise-law-dependent recovery".
