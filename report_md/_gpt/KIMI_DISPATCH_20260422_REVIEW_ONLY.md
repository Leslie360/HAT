# Kimi Dispatch — Review Only Split

Date: 2026-04-22
Owner split: Codex = GPU/runtime/parity probes; Kimi = review/audit/documentation only.

## Hard boundary
Do not launch GPU experiments.
Do not modify runtime scripts for performance.
Do not edit frozen paper prose under Rule B.

## Kimi tasks
1. Audit the config-sharing bug landing.
- Verify `analog_layers.py` and `analog_layers_ensemble.py` now isolate `AnalogLinearConfig` per module.
- Confirm no remaining conversion path still passes a shared config object.
- Deliverable: `KIMI_CONFIG_ISOLATION_AUDIT_20260422.md`

2. Audit the parity-probe command set after the `delta_g_eff` semantics fix.
- Check that local parity docs and scripts consistently distinguish:
  - `--delta-g-eff -1.0` => auto-fill
  - `--delta-g-eff 0.0` => literal zero
- Deliverable: `KIMI_PARITY_COMMAND_AUDIT_20260422.md`

3. Audit historical memo contamination.
- Identify local docs/memos that still describe old mixed-NL results as if they were trustworthy under fixed code.
- Focus on `J1d/K2/K3/K4/K5` summaries and remote-facing parity notes.
- Deliverable: `KIMI_MIXED_NL_MEMO_CONTAMINATION_20260422.md`

4. Audit deprecated old-path usage.
- Confirm `run_ensemble_hat_fixed.py` and `analog_layers_ensemble.py` are clearly marked deprecated everywhere they are referenced.
- Flag any remaining live docs/scripts that still imply they are canonical.
- Deliverable: `KIMI_DEPRECATED_PATH_AUDIT_20260422.md`

## Context
Current local priority is a minimal parity probe under fixed code. Those runtime results will come from Codex. Kimi should review the landing and documentation consistency, not rerun experiments.
