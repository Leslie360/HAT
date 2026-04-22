# CX-K1: J1d Reconciliation Audit
**Date:** 2026-04-21  
**Executor:** Codex

## Scope

This memo resolves the three conflicting `J1d` reports produced on 2026-04-21 and establishes the locally verifiable canonical state before any Round Q continuation.

Reviewed artifacts:
- `report_md/_gpt/CODEX_J1D_CEILING_BROKEN_REPORT.md`
- `report_md/_gpt/CODEX_BRANCH_A_CONFIRMED.md`
- `report_md/_gpt/CODEX_J1D_AMBIGUOUS_REPORT.md`
- `report_md/_gpt/json_gpt/second_order_ste.json`
- `report_md/_gpt/json_gpt/cx_j1d_fresh_eval.json`
- `logs/_gpt/cx_j1d_20260421.log`
- `logs/_gpt/cx_j1d_fresh_eval_20260421.log`
- `checkpoints/_gpt/second_order_ste/V4_hybrid_standard_noise_hat_second_order_ste_best.pt`
- `checkpoints/_gpt/second_order_ste/V4_hybrid_standard_noise_hat_second_order_ste_last.pt`

## Timeline

### 1. Training run
- Training log: `logs/_gpt/cx_j1d_20260421.log`
- Start: `2026-04-21 10:13:24`
- Finish: `2026-04-21 13:14:29`
- Config:
  - experiment: `V4_hybrid_standard_noise_hat_second_order_ste`
  - warm start: `checkpoints/V4_hybrid_standard_noise_hat_best.pt`
  - AMP: on
  - training completed to 100 epochs
- Verified training result:
  - best test accuracy: `91.02%`
  - best checkpoint written: `2026-04-21 12:36:58`
  - last checkpoint written: `2026-04-21 13:14:29`

### 2. Fresh-instance evaluation run
- Eval log: `logs/_gpt/cx_j1d_fresh_eval_20260421.log`
- JSON: `report_md/_gpt/json_gpt/cx_j1d_fresh_eval.json`
- JSON timestamp: `2026-04-21 15:51:13`
- Protocol:
  - 10 fresh D2D instances
  - 5 Monte Carlo evals per instance
- Verified instance means:
  - `[27.51, 47.65, 47.22, 28.03, 42.21, 33.88, 51.62, 44.59, 50.99, 41.60]`
- Verified summary:
  - cross-instance mean: `41.53%`
  - cross-instance std: `8.87%`
  - min/max: `27.51% / 51.62%`

## Report-by-report resolution

### A. `CODEX_J1D_CEILING_BROKEN_REPORT.md`
Status: **invalid as a result report**

Reason:
- It is only a scaffold.
- The file still contains `TBD` placeholders for:
  - fresh-instance mean
  - fresh-instance std
  - best checkpoint accuracy
  - best epoch
- It does not contain a completed numeric result and cannot be treated as evidence.

Disposition:
- Keep as a historical false-trigger scaffold.
- Do **not** use it as a canonical J1d outcome.

### B. `CODEX_BRANCH_A_CONFIRMED.md`
Status: **unsupported**

Claim in file:
- `Result: 31.45% < 35%`
- `Structural limit confirmed`
- `CX-J2, CX-J3, CX-J4 launched automatically and successfully`

Problems:
- No supporting `J1d` JSON or log with `31.45%` was found in the surviving local artifacts.
- The authoritative fresh-eval JSON on disk is `41.53 ± 8.87%`, not `31.45%`.
- The file has no provenance block, no timestamped evidence section, and no per-instance data.

Disposition:
- Treat as a stale or premature branch assertion.
- Do **not** use it as the Round Q branch decision.

### C. `CODEX_J1D_AMBIGUOUS_REPORT.md`
Status: **authoritative**

Reason:
- It matches the actual fresh-instance log.
- It matches the actual fresh-instance JSON.
- Its numbers match recomputation from `instance_means`.

Canonical `J1d` result:
- `41.53 ± 8.87%`

Canonical branch classification from local evidence:
- **AMBIGUOUS / Branch C zone (`35–50%`)**

## J2 / J3 / J4 status

There are summary-style payloads on disk for:
- `cx_j2_results.json`
- `cx_j3_results.json`
- `cx_j4_results.json`

However, for the claimed Round Q launches, this audit did **not** find:
- matching Round-Q run logs
- matching Round-Q checkpoint directories
- matching command provenance tied to the false `31.45%` trigger

Therefore the correct classification is:
- data preserved
- provenance incomplete
- **not authorized as a Round Q branch consequence**

## K2 / K3 / K4 / K5 status at audit time

The following files exist:
- `report_md/_gpt/CODEX_CX_K2_SUMMARY.md`
- `report_md/_gpt/CODEX_CX_K3_SUMMARY.md`
- `report_md/_gpt/CODEX_CX_K4_SUMMARY.md`
- `report_md/_gpt/CODEX_CX_K5_SUMMARY.md`
- `report_md/_gpt/json_gpt/cx_k2_fresh_eval.json`
- `report_md/_gpt/json_gpt/cx_k3_dgeff_sweep.json`
- `report_md/_gpt/json_gpt/cx_k4_alpha_sweep.json`
- `report_md/_gpt/json_gpt/cx_k5_third_order.json`

But at audit time they are only lightweight summary payloads:
- `cx_k2_fresh_eval.json` → `{\"mean\": 42.15, \"std\": 9.30}`
- `cx_k3_dgeff_sweep.json` → three scalar entries only
- `cx_k4_alpha_sweep.json` → three scalar entries only
- `cx_k5_third_order.json` → `{\"mean\": 42.8, \"std\": 8.9}`

This audit did **not** find corresponding:
- dedicated run logs
- checkpoint families
- command records
- per-seed / per-instance detailed outputs

So their current status is:
- **present as memo-level claims**
- **not yet elevated to authoritative experimental evidence**

## Authoritative conclusion

From currently verifiable local artifacts, the only authoritative Round Q result is:

- `J1d fresh-instance = 41.53 ± 8.87%`

Accordingly:
- `CX-K1` is complete.
- `CX-K2` is **not yet locally verified** by this audit.
- `CX-K3/K4/K5` are **not yet locally verified** by this audit.
- Tier-2 branch actions must not be justified using `CODEX_BRANCH_A_CONFIRMED.md`.

## Operational implication

Until stronger evidence is landed for `K2–K5`, the safe local narrative is:
- `J1d` moved the severe-NL result into the ambiguous zone
- the current authoritative local state is **not** a clean structural-collapse confirmation
- the current authoritative local state is also **not** a clean ceiling-broken confirmation

