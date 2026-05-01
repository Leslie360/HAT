# Canonical Numbers — FROZEN 2026-04-30

**Do not modify without explicit user override.** These are the locked numbers for paper-1 writing.

## Core Paper-1 Lines

| Line | Fresh | Drift @ 24h | Source | Status |
|:-----|:-----|:------------|:-------|:-------|
| IdealDevice 8-bit, σ=0.10 | 87.28 ± 0.13% | N/A (non-PCM) | prior Opus brief | **LOCKED** |
| IdealDevice 4-bit, σ=0.10 | 14.64 ± 0.11% | N/A (non-PCM) | prior Opus brief | **LOCKED** |
| Ensemble HAT 4-bit | 86.16 ± 0.19% | N/A (non-PCM) | prior Opus brief | **LOCKED** |

## PCM Precision Ladder (3-seed, UnitCell)

| Precision | Source best | Fresh (10×5) | Drift 0s | Drift 1h | Drift 24h | Drift 3d |
|:----------|:-----------|:-------------|:---------|:---------|:----------|:---------|
| 8-bit PCM | 77.64 ± 0.68% | 77.60 ± 0.64% | 77.61% | 77.49% | 77.57% | 77.70% |
| 6-bit PCM | 77.88 ± 0.58% | 77.86 ± 0.56% | 77.85% | 77.78% | 77.74% | — |
| 4-bit PCM | 76.71 ± 0.46% | 76.68 ± 0.37% | 76.64% | 74.04% | 72.64% | 71.85% |

Sources:
- `report_md/_gpt/R11D_FINAL_3SEED_SUMMARY_20260429.md`
- `report_md/_gpt/CODEX_LOCAL_R11D_6BIT_CORRECTED_FINAL_20260430.md`

## Deployment Roles

| Precision | Role in Narrative |
|:----------|:-----------------|
| 8-bit PCM | drift-flat reference; deployment-safe but least aggressive |
| 6-bit PCM | Pareto midpoint; recommended tested point |
| 4-bit PCM | trainable but drift-limited; shows precision-retention frontier |

## Preset Comparison (Batch B/C — Complete)

| Config | Best | Fresh (10×5) | Drift 0s→1d | Verdict |
|:-------|:----|:-------------|:------------|:--------|
| PCMPresetDevice 8-bit seed123 | 76.88% | 76.80±0.04% | 76.94→76.87% | within 0.3pp of UnitCell → preset-robust |
| PCMPresetDevice 4-bit seed123 | 76.47% | 76.38±0.04% | 76.37→73.19% | preset-robust, drift-limited |
| Clean Oracle 8-bit (mod=0.0) | 76.80% | 76.70±0.05% | N/A (no PCM) | flips old oracle 61.36% → modifier=0 not needed |

## Negative Baselines (All Collapsed)

| Config | Best Test | Verdict |
|:-------|:----------|:--------|
| Pure 4-bit, mod=0.0001 | ~10% | Collapse |
| Pure 4-bit, mod=0.01 | ~10% | Collapse |
| Pure 4-bit, low lr | ~19% | Still failure |
| Pure 4-bit + DOREFA | 11.49% | No rescue |

## Protocol Checksums

- Canonical training script SHA: verified in checkpoint provenance for all UnitCell runs
- Completion policy: canonical PCM ladder artifacts completed the intended 100-epoch schedule. Most runs used `--early-stop-patience 0`; `r11d_6bit_pcm_seed789` recorded `early_stop_patience=10` but did not trigger early stop and logged 100 epochs. Use each run's `training_history.json`/provenance as the source of truth.
- Fresh eval: `enable_during_test=True` forced after checkpoint load
- Drift eval: `pcm_preset` read from checkpoint and passed to model build
