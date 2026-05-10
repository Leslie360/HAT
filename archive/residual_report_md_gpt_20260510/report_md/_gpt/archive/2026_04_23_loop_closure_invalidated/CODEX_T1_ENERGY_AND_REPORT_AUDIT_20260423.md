# Codex T1 Energy And Report-Generator Audit

**Date:** 2026-04-23 18:19 CST
**Owner:** Codex
**Status:** Audit complete; stale report generator disabled fail-fast.

## Executive Verdict

There are two distinct energy artifacts and they must not be mixed.

1. `report_md/_gpt/energy_sensitivity_analysis.json.BUGGY` is invalid for manuscript use.
2. `report_md/_gpt/json_gpt/energy_scale_recovery_sensitivity.json` is arithmetically consistent with the paper's system-energy claim, but its INT8 comparison is assumption-backed, not measured.

`generate_final_report.py` was also stale and has been changed to fail fast instead of generating an invalid final report.

## Invalid Artifact

`run_energy_sensitivity.py` uses this toy baseline:

- analog energy: `65 pJ`
- digital baseline: `1 pJ`
- computed speedup: `0.015x`

This is not the same quantity as the paper energy accounting, which uses system-level TinyViT inference energy in microjoules. The `0.015x` result therefore answers a different, inconsistent toy model and must not be used to revise manuscript energy claims.

Current status:

- invalid file retained as `report_md/_gpt/energy_sensitivity_analysis.json.BUGGY`
- old `json_gpt/energy_sensitivity_analysis.json` from 2026-04-15 is also stale

## Corrected Arithmetic Artifact

`report_md/_gpt/json_gpt/energy_scale_recovery_sensitivity.json` uses the paper-scale quantities:

| Quantity | Value |
|---|---:|
| Digital FP32 energy | `273.94 uJ` |
| Analog energy | `23.924890829694323 uJ` |
| Speedup vs FP32 | `11.45x` |
| Assumed digital INT8 energy | `68.485 uJ` |
| Speedup vs assumed INT8 | `2.8625x` |

Arithmetic checks:

- `273.94 / 23.924890829694323 = 11.45`
- `68.485 / 23.924890829694323 = 2.8625`

## Required Wording Boundary

Safe wording:

> Under the first-order system-energy model, the hybrid mapping is `11.45x` lower energy than the FP32 digital baseline. If an idealized INT8 digital baseline is approximated as `FP32/4`, the corresponding advantage is `~2.86x`. Both values are analytical estimates, not silicon measurements.

Unsafe wording:

- Do not state `2.86x vs INT8` as a measured hardware result.
- Do not state that digital scale-recovery cost has been silicon-validated.
- Do not cite `0.015x` or `65 pJ` as the paper-level energy result.

## Report Generator Action

`generate_final_report.py` contained multiple stale hard-coded results, including pre-fix experimental numbers and the invalid energy downgrade path. It now exits immediately with a clear error message directing users to this audit.

This is intentional fail-fast behavior: no final report generator should run until it is rebuilt from:

- R1 train/fresh JSON
- R2 train/fresh JSON once complete
- corrected AIHWKIT JSON
- corrected energy-scale JSON
- post-dual-bug invalidation matrix

## Next Required Work

1. Kimi should decide whether to issue a formal `KIMI_T1_ENERGY_AUDIT_20260423.md` or adopt this file as the current audit.
2. Claude should not use `generate_final_report.py` for synthesis.
3. Any new final report generator must be rebuilt from post-fix artifacts only.
