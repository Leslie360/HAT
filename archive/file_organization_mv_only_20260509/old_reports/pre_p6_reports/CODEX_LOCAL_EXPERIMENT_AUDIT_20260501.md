# Codex Local Experiment Audit — 2026-05-01

## Verdict

PASS for the local Paper-1 experimental spine, after provenance/report corrections.

The canonical local results support the locked spine:

1. AIHWKit IdealDevice 8-bit remains robust: `87.28 ± 0.13%` fresh.
2. AIHWKit/pure 4-bit fixed-instance path collapses: `14.64 ± 0.11%` fresh.
3. Ensemble HAT rescues the pure 4-bit regime: `86.16 ± 0.19%` fresh.
4. PCM UnitCell precision ladder is internally consistent across 3 seeds:
   - 8-bit: `77.64 ± 0.68%` source, `77.60 ± 0.64%` fresh, `0.04pp` 1d drift drop.
   - 6-bit: `77.88 ± 0.58%` source, `77.86 ± 0.56%` fresh, `0.10pp` 1d drift drop.
   - 4-bit: `76.71 ± 0.46%` source, `76.68 ± 0.37%` fresh, `4.01pp` 1d drift drop.

Conclusion: 6-bit remains the best tested Pareto midpoint in the tested PCM UnitCell matrix; 4-bit is trainable/fresh-stable but retention-limited.

## Findings And Fixes

### Finding 1 — Batch B/C report had stale PCMPresetDevice numbers

`report_md/_gpt/CODEX_LOCAL_R11D_BATCHBC_RESULTS_20260430.md` did not match the current raw artifacts for the `t13v2_*` PCMPresetDevice reruns. The same artifact paths appear to have been rewritten by later corrected runs.

Raw current values:

| Run | Best | Final | Fresh | Drift 0s | Drift 1h | Drift 1d |
|---|---:|---:|---:|---:|---:|---:|
| `t13v2_r11d_5a_pcm_PCMPresetDevice_seed123` | 76.88 | 76.84 | 76.8026 ± 0.0425 | 76.94 | 76.70 | 76.87 |
| `t13v2_r11d_7_pcm_4bit_PCMPresetDevice_seed123` | 76.47 | 76.20 | 76.3798 ± 0.0407 | 76.37 | 74.72 | 73.19 |
| `r11d_5a_pcm_oracle_seed123_clean` | 76.80 | 76.74 | 76.6994 ± 0.0488 | 76.94 | 76.66 | 76.67 |

Fix: report table corrected in place and marked with a 2026-05-01 raw-artifact correction note.

Impact: no impact on the main paper spine. PCMPresetDevice is only a single-seed compatibility probe and is not used for headline 3-seed UnitCell statistics.

### Finding 2 — 6-bit seed789 provenance was misstated as `patience=0`

Raw artifact:

- run: `r11d_6bit_pcm_seed789`
- configured early stop: `patience=10`, `min_delta=0.01`
- epochs completed: `100`
- best epoch: `100`
- best test: `77.81%`

Interpretation: this run did complete the full 100-epoch schedule and is valid for the aggregate, but the provenance table was wrong to state `patience=0`.

Fixes:

- `paper/latex_gpt/supplementary.tex`: provenance paragraph/table updated to say seed789 used `patience=10, not triggered`.
- `report_md/_gpt/GEMINI_R11D_PRECISION_LADDER_TABLES_20260430.md`: same correction applied.
- Added `scripts/_gpt/check_local_pcm_precision_ladder.py` to guard the full local PCM precision-ladder aggregate directly from raw artifacts.

Impact: no numerical impact. This is a provenance correction, not a result retraction.

### Finding 3 — Introduction still contained causal overclaim wording

`paper/latex_gpt/sections/01_introduction.tex` still said PCM UnitCell characteristics “naturally enable convergence”. That overstates what the local experiments prove.

Fix: changed to tested-regime wording: convergence is observed under the tested PCM UnitCell setting where pure quantization fails.

Impact: improves defensibility of the manuscript without changing results.

## Canonical Local Artifact Set

Use these for the local Paper-1 spine:

```text
paper2_aihwkit_baseline/checkpoints/fresh_eval.json
paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/fresh_eval.json
paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/
paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456/
paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed789/
paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123/
paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456_full100/
paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/
paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed123/
paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/
paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789/
report_md/_gpt/json_gpt/r10a_canonical_ensemble_hat_3seed_fresh_eval.json
```

Do not use these for final claims:

```text
paper2_aihwkit_baseline/checkpoints/r11d_2_sigma020/
paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/SUPERSEDED_INVALID_MARKER_20260428.md  # historical marker only
paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_PCMPresetDevice_seed42/
paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_PARTIAL_PIPEFAIL_BUG_20260429_100717/
paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456/  # early-stopped diagnostic only
```

Note: `r11d_5a_pcm_seed123/SUPERSEDED_INVALID_MARKER_20260428.md` is a historical marker from an earlier bad run at the same path. The current `training_history.json` in that directory records `pcm_preset_used=PCMPresetUnitCell`, 100 epochs, `early_stop_patience=0`, and valid canonical provenance.

## Verification Commands

```bash
python scripts/_gpt/check_locked_numbers.py
python -m py_compile scripts/_gpt/check_local_pcm_precision_ladder.py
python scripts/_gpt/check_local_pcm_precision_ladder.py
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex
rg -n "undefined references|undefined citations|Reference .* undefined|Citation .* undefined|Label .* multiply defined|! LaTeX Error|Emergency stop|Fatal error|Overfull" paper/latex_gpt/main.log paper/latex_gpt/supplementary_main.log
```

Verification results:

- locked-number guard: `22/22 passed`.
- local PCM precision-ladder guard: `PASS`.
- supplementary PDF compile: passed.
- final log grep: no undefined refs/citations, fatal errors, or overfull warnings.

## Scientific Status

Ready for main text:

- Pure 4-bit failure vs Ensemble HAT rescue.
- PCM UnitCell 4/6/8 precision ladder.
- 6-bit as best tested Pareto midpoint in this local PCM UnitCell matrix.
- 4-bit as trainable/fresh-stable but retention-limited.

Keep in SI/diagnostic only:

- PCMPresetDevice single-seed compatibility.
- Clean oracle/no-modifier result.
- 6-bit seed456 early-stop failure and late-recovery curve.
- Old OPECT/front-end/severe-NL material.

## 2026-05-01 Additional Artifact Hygiene

The canonical directory `paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/` still contained a stale `INVALID_DO_NOT_USE.md` marker from an earlier bad run that used the same directory name. Because the current artifacts in that directory are valid and pass the PCM precision-ladder guard, Codex renamed the marker to:

```text
paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/SUPERSEDED_INVALID_MARKER_20260428.md
```

and added:

```text
paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/CURRENT_STATUS_VALID_20260501.md
```

The local PCM precision-ladder guard still passes after this artifact hygiene step.
