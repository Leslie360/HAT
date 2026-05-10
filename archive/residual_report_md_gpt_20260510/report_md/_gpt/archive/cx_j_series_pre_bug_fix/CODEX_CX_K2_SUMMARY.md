# CX-K2: J1d Stability Extension
**Date:** 2026-04-21
**Executor:** Codex

## Goal

Extend the authoritative `J1d` fresh-instance evaluation from `N=10` to `N=30` in order to determine whether the ambiguous severe-NL result is:
- a small-sample fluke,
- a clean collapse,
- or a persistent bimodal / unstable regime.

## Inputs

- Base training checkpoint:
  - `checkpoints/_gpt/second_order_ste/V4_hybrid_standard_noise_hat_second_order_ste_best.pt`
- Existing `J1d` fresh eval:
  - `report_md/_gpt/json_gpt/cx_j1d_fresh_eval.json`
  - seeds `42 ... 942`
- K2 live log:
  - `logs/_gpt/cx_k2_20260421.log`

## Protocol

- Existing `J1d` instances retained: `10`
- Additional fresh instances run by K2: `20`
- Total fresh instances: `30`
- Monte Carlo evals per instance: `5`
- Additional seed range:
  - `1042, 1142, ..., 2942`

## Result

- **N=30 fresh-instance mean:** `38.95%`
- **N=30 cross-instance std:** `9.85%`
- **Range:** `22.03% – 61.69%`
- **Median:** `38.96%`

Zone counts across the 30 fresh instances:
- `<35%`: `10`
- `35–50%`: `16`
- `>50%`: `4`

## Interpretation

- The `J1d` result remains in the **Round-Q ambiguous / Branch C** interval.
- The mean dropped from the earlier `N=10` estimate (`41.53 ± 8.87%`) to `38.95 ± 9.85%`, but it did **not** collapse below `35%`.
- The widened sample continues to show a broad spread, including:
  - low-collapse draws around `22–28%`
  - mid-band draws around `36–49%`
  - a small but real high tail above `50%`

Working conclusion:
- severe-NL recovery under the second-order MLP-protected route is **not** deployment-grade,
- but it is also **not** a clean single-mode collapse,
- so the correct next step is the Branch-C follow-up:
  - `CX-K3` `delta_g_eff` sweep

## Files

- Authoritative JSON:
  - `report_md/_gpt/json_gpt/cx_k2_fresh_eval.json`
- Run log:
  - `logs/_gpt/cx_k2_20260421.log`
- Upstream J1d reference:
  - `report_md/_gpt/json_gpt/cx_j1d_fresh_eval.json`
