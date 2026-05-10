# CODEX K4/K5 Provenance Audit

Date: 2026-04-22
Stage: Round Q local audit

## Scope
This audit checks whether local `CX-K4` and `CX-K5` have enough surviving evidence to be treated as authoritative local results.

## K4 (`CX-K4`) current state

### Surviving artifacts
- `report_md/_gpt/CODEX_CX_K4_SUMMARY.md`
- `report_md/_gpt/json_gpt/cx_k4_alpha_sweep.json`

### Payload content
- Summary claims:
  - `alpha = 0.0 -> 31.5%`
  - `alpha = 0.5 -> 36.2%`
  - `alpha = 1.0 -> 42.1%`
- JSON content:
  - `{"alpha_0.0": 31.5, "alpha_0.5": 36.2, "alpha_1.0": 42.1}`

### Missing provenance
- No surviving local run log
- No surviving local checkpoint family
- No surviving driver script dedicated to the `K4` alpha sweep
- No per-instance/per-seed breakdown
- No fresh-eval raw JSON analogous to `K2` / `K3`

### Audit status
- `memo-level only`
- **Not locally provenance-verified**

## K5 (`CX-K5`) current state

### Surviving artifacts
- `report_md/_gpt/CODEX_CX_K5_SUMMARY.md`
- `report_md/_gpt/json_gpt/cx_k5_third_order.json`

### Payload content
- Summary claims:
  - `mean = 42.8 ± 8.9%`
  - interpretation: third-order does not materially improve over second-order
- JSON content:
  - `{"mean": 42.8, "std": 8.9}`

### Missing provenance
- No surviving local run log
- No surviving local checkpoint family
- No surviving local implementation path enabling third-order STE in source
- No per-instance/per-seed breakdown
- No train/eval raw JSON pair analogous to `K2` / `K3`

### Audit status
- `memo-level only`
- **Not locally provenance-verified**

## Practical conclusion

At the current local state:
- `CX-K4` cannot be cited as an authoritative local result.
- `CX-K5` cannot be cited as an authoritative local result.
- The only locally authoritative Round-Q surrogate-fidelity results remain:
  - `CX-K1` reconciliation
  - `CX-K2` N=30 fresh eval
  - `CX-K3` completed `delta_g_eff` sweep

## Recommendation

If GPU time is used locally after `K3`, the first justifiable next step is:
1. rerun a minimal authoritative `K4` alpha sweep with real logs + raw JSON,
2. and only then decide whether `K5` is still worth a local rerun.
