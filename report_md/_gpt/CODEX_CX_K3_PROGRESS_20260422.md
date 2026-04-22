# CX-K3 Progress Snapshot

**Timestamp:** 2026-04-22 10:06 CST  
**Status:** in progress (`delta_g_eff = 0.25` fresh eval still running)

## Authoritative completed points so far

| tag | delta_g_eff | train best acc | train best epoch | fresh mean | fresh std |
|:--|--:|--:|--:|--:|--:|
| k3_dgeff_0p05 | 0.05 | 91.52 | 72 | 36.21 | 9.61 |
| k3_dgeff_0p10 | 0.10 | 90.97 | 92 | 30.79 | 11.59 |
| k3_dgeff_0p15 | 0.15 | 91.27 | 82 | 27.85 | 7.37 |
| k3_dgeff_0p20 | 0.20 | 91.50 | 93 | 33.25 | 10.29 |

## Comparison against authoritative local baselines

- Canonical `J1d` / `K2` reference: `38.95 ± 9.85%` (`N=30` fresh-instance)
- Canonical `J1d` original (`N=10`) reference: `41.53 ± 8.87%`

## Interim interpretation

1. The `delta_g_eff` sweep has **not** produced a clear lift above the authoritative `K2` baseline.
2. All completed points (`0.05, 0.10, 0.15, 0.20`) remain **at or below** the `K2` mean.
3. The current best completed point is `delta_g_eff = 0.05`, but it still underperforms the authoritative `K2` mean.
4. So far, the sweep supports the interpretation that naive curvature-strength tuning does **not** break the Round-Q ambiguous regime.

## Remaining live point

- `delta_g_eff = 0.25`
  - training is complete (`best = 91.24% @ epoch 76`)
  - fresh-instance evaluation is still running

## Next step

- Wait for `cx_k3_eval_k3_dgeff_0p25.json`
- Then let `run_cx_k3_continuation.py` emit:
  - `report_md/_gpt/json_gpt/cx_k3_dgeff_continuation.json`
  - `report_md/_gpt/CODEX_CX_K3_CONTINUATION_20260421.md`
