# STE Semantics Arbitration Taskboard (2026-04-22)

## Status
- GPU branch `corr_allcad_q` is frozen.
- No new corrected-mainline numbers may be cited until arbitration closes.
- All post-22:35 corrected cadence outputs are forensic-only.

## Arbitration question
Exactly one of the following must become authoritative:
1. **No-multiplier semantics** is the intended first-order STE behavior.
2. **With-multiplier semantics** is the intended first-order STE behavior.

Until that is decided, the current code, tests, route memo, and remote handoff packet are not logically aligned.

## Hard rule
- No new GPU experiments.
- No new remote queue changes.
- No manuscript/rebuttal claim changes except freeze notes.
- Only arbitration work is allowed.

## Task chain
### T0 — Freeze verification
- Owner: Codex
- Status: DONE
- Acceptance:
  - no active `run_corrected_all_linear_cadence.py`
  - no active `corr_allcad_q` tmux session

### T1 — Local evidence pack
- Owner: Codex
- Goal:
  - produce one compact local evidence memo answering:
    - what current code does
    - what current tests assert
    - what broadcast files claim
    - which parity numbers are affected
- Inputs:
  - `analog_layers.py`
  - `analog_layers_ensemble.py`
  - `test_groupwise_nl_wrapper.py`
  - `CODEX_CX_PARITY_MINIMAL_20260422.md`
  - `CODEX_ROUTE_DECISION_20260422.md`
  - `REMOTE_HANDOFF_PACKET_20260422.md`
  - `AGENT_SYNC_gpt.md`
- Output:
  - `CODEX_STE_SEMANTICS_EVIDENCE_PACK_20260422.md`
- Acceptance:
  - every claim tied to file+line reference
  - clear statement of whether current parity numbers came from current code state or not

### T2 — Review contamination sweep
- Owner: Kimi
- Goal:
  - identify every doc/memo/broadcast that currently states the multiplier fix as fact
  - classify each as:
    - must-correct now
    - can leave as historical log
- Inputs:
  - all `report_md/_gpt/*.md`
  - `远端/*.md`
- Output:
  - `KIMI_STE_SEMANTICS_CONTAMINATION_SWEEP_20260422.md`
- Acceptance:
  - explicit path list
  - replacement wording for each must-correct item
  - no theory speculation

### T3 — Theory/notation ruling
- Owner: Gemini
- Goal:
  - decide whether the first-order surrogate should mathematically include the leading `nl` multiplier
  - compare:
    - current code
    - manuscript equations
    - intended physical surrogate meaning
- Inputs:
  - `analog_layers.py`
  - `analog_layers_ensemble.py`
  - thesis/paper methodology equations
- Output:
  - `GEMINI_STE_SEMANTICS_RULING_20260422.md`
- Acceptance:
  - explicit yes/no ruling
  - one derivation
  - one paragraph on consequence for parity interpretation

### T4 — Final arbitration
- Owner: Codex
- Blocked by: T1, T2, T3
- Goal:
  - choose the authoritative semantics
  - define required branch action
- Output:
  - `CODEX_STE_SEMANTICS_ARBITRATION_20260422.md`
- Acceptance:
  - one ruling only
  - one branch only
  - explicit instruction whether GPU may resume

## Branch actions after arbitration
### Branch A — no-multiplier is authoritative
- Code: keep current implementation
- Tests: keep current tests
- Docs: correct all files that claim multiplier fix
- GPU follow-up: rerun minimal parity only if provenance of `46.75/57.00/55.65/83.34` remains unclear after T1

### Branch B — multiplier is authoritative
- Code: patch both `analog_layers.py` and `analog_layers_ensemble.py`
- Tests: rewrite LTP/LTD surrogate tests
- Docs: keep multiplier-fix narrative, but invalidate all parity numbers produced under the wrong code state
- GPU follow-up: rerun minimal parity first, then decide on cadence relaunch

## Stop condition
Arbitration is complete only when:
1. code, tests, and route docs all point to the same STE semantics
2. `CODEX_STE_SEMANTICS_ARBITRATION_20260422.md` names the chosen branch
3. GPU restart is explicitly authorized in that memo
