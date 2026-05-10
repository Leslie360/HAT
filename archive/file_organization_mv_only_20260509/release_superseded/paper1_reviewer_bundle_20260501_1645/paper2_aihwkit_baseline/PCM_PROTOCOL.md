# PCM Precision-Ladder Protocol

**Last updated:** 2026-04-30
**Status:** locked (do not modify without explicit user approval)

## Canonical Numbers (Locked)

| Precision | Source best mean | Fresh mean (10 inst × 5 MC) | 1d drift drop | Role |
|---:|---:|---:|---:|---|
| 8-bit PCM | 77.64 ± 0.68% | 77.60 ± 0.64% | 0.04pp | drift-flat reference |
| 6-bit PCM | 77.88 ± 0.58% | 77.86 ± 0.56% | 0.10pp | Pareto midpoint |
| 4-bit PCM | 76.71 ± 0.46% | 76.68 ± 0.37% | 4.01pp | trainable, drift-limited |

**6-bit multi-seed confirmed (2026-04-30):** seeds 123 (77.33/77.36), 456 (78.49/78.47), 789 (77.81/77.75) all within tolerance. seed456 full 100-epoch run confirmed — the early-stopped seed456 (69.07%) is diagnostic-only, excluded from canonical stats.

Sources:
- `report_md/_gpt/R11D_FINAL_3SEED_SUMMARY_20260429.md`
- `report_md/_gpt/CODEX_LOCAL_R11D_6BIT_CORRECTED_FINAL_20260430.md`
- Multi-seed eval JSONs: `checkpoints/r11d_6bit_pcm_seed{123,456,789}/fresh_eval.json`, `drift_eval.json`
- Batch B/C eval JSONs: `checkpoints/*PCMPresetDevice*/`, `checkpoints/r11d_5a_pcm_oracle_seed123_clean/`

## Mandatory Training Rules

1. **Full-schedule completion.** Canonical PCM precision-ladder evidence must complete the intended 100-epoch schedule. The preferred wrapper setting is `--early-stop-patience 0`; one canonical run (`r11d_6bit_pcm_seed789`) recorded `early_stop_patience=10` but did not trigger early stop and logged all 100 epochs. PCM has late-recovery dynamics (e.g., 6-bit seed456 appeared to plateau at ~69% with patience=10 but recovered to 78.49% at full 100 epochs), so any early-stopped PCM run is diagnostic-only unless explicitly re-qualified.

2. **Use canonical `r11d4_train_pcm.py`** for UnitCell runs. Use `r11d4_train_pcm_extended.py` for PCMPresetDevice runs (adds `--pcm-preset` with strict resolution, no silent fallback).

3. **Full 100-epoch schedule.** All PCM runs train for 100 epochs with CosineAnnealingLR (T_max=100, eta_min=1e-6).

## Evaluation Rules

1. **Fresh eval:** Use `eval_aihwkit_fresh.py` with `--n-fresh 10 --mc-repeats 5`. Script forces `enable_during_test=True` after checkpoint load.

2. **Drift eval:** Use `eval_aihwkit_drift_extended.py` with `--drift-times 0 3600 86400`. Preset is read from checkpoint and passed to model build (no fallback).

3. **Checkpoint provenance:** Every checkpoint must record `pcm_preset`, precision (`inp_res`/`out_res`), `modifier_std_dev`, `seed`, and `--early-stop-patience` in metadata.

## Preset Comparison — Complete
- PCMPresetDevice runs use strict mode: if the preset fails to load, the script errors out immediately (no fallback to UnitCell).
- **Batch B/C complete (2026-04-30):** 8-bit PCMPresetDevice within 0.3pp of UnitCell, 4-bit PCMPresetDevice within 0.2pp of UnitCell, Clean Oracle (modifier=0.0) reaches 76.80% — flips old oracle 61.36% narrative (modifier noise is NOT essential regularization).

## Kill / Defer List
- **Killed:** Progressive quantization (R11D-11), lr sweeps, DOREFA (R11D-10), Analog-SAM pre-submission
- **Deferred:** Adaptive noise schedule, 105 seed789 (wait for server), 107 selective-layer fresh-D2D (Work-2)
