# CODEX CX-K3 Interpretation

Date: 2026-04-22
Stage: Round Q
Scope: authoritative local interpretation of the completed `delta_g_eff` sweep

## Inputs

- Authoritative K2 landing:
  - `report_md/_gpt/CODEX_CX_K2_SUMMARY.md`
  - `report_md/_gpt/json_gpt/cx_k2_fresh_eval.json`
- Authoritative K3 continuation:
  - `report_md/_gpt/CODEX_CX_K3_CONTINUATION_20260421.md`
  - `report_md/_gpt/json_gpt/cx_k3_dgeff_continuation.json`
  - `report_md/_gpt/CX_K3_CONTINUATION_FINAL_STATUS_20260422.md`

## Canonical comparison

### K2 baseline
- `J1d N=30`: `38.95 ± 9.85%`
- Regime: `Branch C / ambiguous-bimodal`

### K3 sweep
| delta_g_eff | train best acc | best epoch | fresh mean | fresh std |
|:--|--:|--:|--:|--:|
| 0.05 | 91.52 | 72 | 36.21 | 9.61 |
| 0.10 | 90.97 | 92 | 30.79 | 11.59 |
| 0.15 | 91.27 | 82 | 27.85 | 7.37 |
| 0.20 | 91.50 | 93 | 33.25 | 10.29 |
| 0.25 | 91.24 | 76 | 30.08 | 9.07 |

Best K3 point:
- `delta_g_eff = 0.05`
- `36.21 ± 9.61%`

Aggregate K3 mean-of-means:
- `31.636%`

## Findings

1. No completed `delta_g_eff` point exceeds the authoritative `K2` mean.
2. The best K3 point (`0.05`) still underperforms `K2` by `2.74 pp`.
3. Source-domain recovery remains strong across the sweep (`~91%` best accuracy), but fresh-instance transfer does not improve correspondingly.
4. Therefore, increasing `delta_g_eff` within this tested range does not rescue the severe-NL fresh-instance bottleneck.

## Interpretation

The local K3 result weakens the claim that the current severe-NL ceiling is primarily a missing-curvature problem that can be fixed by modest `delta_g_eff` tuning inside the second-order surrogate.

More precisely:
- `delta_g_eff` tuning changes the surrogate,
- but the fresh-instance distribution remains in the same broad ambiguous regime,
- and never outperforms the already-authoritative `K2` landing.

So the current local evidence supports the following statement:

> The `delta_g_eff` sweep does not break the severe-NL ceiling. Within the tested range `{0.05, 0.10, 0.15, 0.20, 0.25}`, second-order surrogate tuning fails to produce a fresh-instance gain over the canonical `K2` baseline.

## Round Q status impact

- `CX-K3`: complete
- Status: **negative / non-rescuing result**
- Branch implication:
  - still `Branch C / ambiguous-bimodal`
  - but the “surrogate-break” branch is now materially weaker

## Practical guidance

1. Do not treat `K3` as evidence for a narrative pivot.
2. Do not cite any `delta_g_eff` point as a breakthrough.
3. If Round Q continues locally, the next GPU steps should be justified as new probes (`K4/K5` or later), not as already-validated rescue mechanisms.

## Authoritative one-line summary

`K3` is complete and negative: the best `delta_g_eff` setting (`0.05`) reaches `36.21 ± 9.61%`, which remains below the authoritative `K2` result of `38.95 ± 9.85%`.
