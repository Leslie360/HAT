# Kimi Local GPU Queue — 2026-04-30

**Owner:** Kimi local GPU scheduler
**Coordinator:** Codex
**Scope:** Local R11D / AIHWKit PCM only. Do not mix with Remote 105 multi-dataset or Remote 107 KV-cache.

## 1. Review Of Completed Local Batch A

Batch A has completed:

- `outputs/R11D_EXTENDED_DRIFT_SUMMARY_20260429.md`
- `outputs/R11D_FRESH_DRIFT_SUMMARY_20260429.md`

Locked observations:

| Config | Fresh+drift 0s | Fresh+drift 1h | Fresh+drift 1d | Extended 3d | Verdict |
|---|---:|---:|---:|---:|---|
| 4-bit PCM | 76.67 ± 0.37% | 74.21 ± 0.38% | 72.68 ± 0.69% | 71.85 ± 0.81% | stable but retention-limited |
| 8-bit PCM | 77.59 ± 0.66% | 77.57 ± 0.60% | 77.51 ± 0.67% | 77.70 ± 0.53% | drift-safe |

Evaluation-chain consistency is good:

- Extended drift and fresh+drift differ by <0.2pp at matched time points.
- Fresh+drift instance std is small, so the 4-bit degradation is actual drift behavior, not fresh-noise sampling noise.

Decision:

- UnitCell 4-bit/8-bit training/fresh/drift claim is closed.
- Do not run more UnitCell seeds unless a reviewer explicitly asks.
- Next local GPU must answer preset dependence and training-noise regularization.

## 2. Batch B — PCMPresetDevice v2 Preset Dependence

Run first.

Purpose: verify whether the R11D conclusion depends on `PCMPresetUnitCell` or survives `PCMPresetDevice`.

Command:

```bash
cd /home/qiaosir/projects/compute_vit
bash paper2_aihwkit_baseline/run_pcm_preset_comparison.sh
```

This writes fresh v2 artifact names only:

```text
paper2_aihwkit_baseline/checkpoints/t13v2_r11d_5a_pcm_PCMPresetDevice_seed123
paper2_aihwkit_baseline/checkpoints/t13v2_r11d_7_pcm_4bit_PCMPresetDevice_seed123
```

After training, run the post-eval block in `paper2_aihwkit_baseline/run_kimi_r11d_batch_bc_20260430.sh`, or simply run that full script from the start.

Interpretation:

- If PCMPresetDevice is within ~2pp source/fresh of UnitCell, claim is preset-robust.
- If PCMPresetDevice has a different drift profile but still trains, use it as material-model sensitivity.
- If PCMPresetDevice collapses, do not hide it; report as preset limitation.

Soft stop / monitor:

- Valid PCM runs improve late; do not kill before epoch 50 just because epoch 10/30 are low.
- If NaN appears, stop immediately.
- If epoch 50 test is <45%, stop and mark likely incompatible preset/regime.

## 3. Batch C — Clean Oracle / Modifier-Noise Necessity

Run after Batch B unless the user explicitly wants oracle first.

Purpose: convert the old diagnostic no-modifier result into clean provenance.

Command is included in:

```bash
bash paper2_aihwkit_baseline/run_kimi_r11d_batch_bc_20260430.sh
```

Clean oracle run ID:

```text
r11d_5a_pcm_oracle_seed123_clean
```

Expected interpretation:

- If best test remains near ~61%, training-time modifier noise is necessary regularization/noise exposure.
- If it recovers near ~77%, the previous oracle diagnostic was provenance-contaminated and must be retracted.

This run is source/fresh/drift evaluated after training.

## 4. Batch D — Optional 6-bit Pareto Bridge

Only run after B/C if GPU remains idle and no remote/local urgent task arrives.

Purpose: test whether 6-bit lies between 4-bit retention-limited and 8-bit drift-safe.

One seed first:

```bash
cd /home/qiaosir/projects/compute_vit
bash paper2_aihwkit_baseline/run_kimi_r11d_6bit_pilot_20260430.sh
```

Continue to seeds 456/789 only if seed123 gives either:

- source/fresh within 0.5pp of 8-bit, or
- 24h drift drop clearly between 4-bit and 8-bit, making a useful Pareto bridge.

## 5. What Not To Run Locally

- Do not rerun UnitCell 4-bit/8-bit seeds.
- Do not run Remote 105 architecture/multi-dataset tasks locally.
- Do not run Remote 107 KV-cache tasks locally.
- Do not run R11D11 progressive unless a new mechanism question is specified.
- Do not run multiple long training jobs in parallel on the local single RTX 5070 Ti.

## 6. Required Kimi Return Format

After Batch B:

```text
batch=B, run_id, preset, bit, seed, best_test, final_test, fresh_mean, fresh_std,
drift_0s, drift_1h, drift_24h, verdict, paper_use=yes/no
```

After Batch C:

```text
batch=C, run_id, modifier_std_dev, best_test, final_test, fresh_mean,
drift_24h, comparison_to_old_oracle, verdict
```

After Batch D:

```text
batch=D, run_id, bit=6, seed, best_test, fresh_mean, drift_24h,
compare_to_4bit_and_8bit, continue_3seed=yes/no
```
