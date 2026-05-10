# Codex Local R11D 6-bit Pilot Result

**Date:** 2026-04-30 14:05 CST
**Run:** `r11d_6bit_pcm_seed123`
**Status:** seed123 COMPLETE; seed456/789 follow-up launched because pilot passed gate.

## 1. Result

| Run | Precision | Seed | Best test | Fresh mean ± std | Drift 0s | Drift 1h | Drift 1d | Drift drop 0s→1d |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `r11d_6bit_pcm_seed123` | 6-bit PCM UnitCell | 123 | 77.33% | 77.3598 ± 0.0404% | 77.35% | 77.26% | 77.19% | 0.16pp |

## 2. Interpretation

The 6-bit pilot is a strong Pareto signal:

- Fresh accuracy is within ~0.24pp of the 8-bit PCM 3-seed fresh mean (77.5955%).
- 1-day drift drop is only 0.16pp, much closer to 8-bit drift-flat behavior than 4-bit's ~4pp 1-day drop.
- It satisfies the pre-declared follow-up criterion (`fresh >= 77.0955`), so seed456/789 follow-up is justified.

## 3. Pipeline Note

The background `nohup` launch path produced header-only logs and did not start Python reliably in this local shell context. The follow-up was therefore launched via an active `bash -x` session and verified to enter `r11d4_train_pcm.py` for seed456.

## 4. Next

Run:

1. `r11d_6bit_pcm_seed456` with native early stop (`patience=10`, `min_delta=0.01`).
2. Fresh+drift eval for seed456.
3. `r11d_6bit_pcm_seed789` with same settings.
4. Fresh+drift eval for seed789.
5. Produce 3-seed 6-bit summary against 4-bit and 8-bit.
