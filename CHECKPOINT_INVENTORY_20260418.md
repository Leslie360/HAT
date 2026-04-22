# Checkpoint Inventory — 2026-04-18

**Scope:** All `.pt` files under `compute_vit/checkpoints/` as of 2026-04-18.
**Total:** 29 files, ~25 GB.
**Status:** Preliminary scaffold. Tier A/B/C assignment pending PROVENANCE_AUDIT triage.
**Note:** NL mitigation lanes (MLP-only, QKV-only, all-linear, attn_proj-only) write to `checkpoints/` but are not yet listed here because they are either already archived or still in-flight.

---

## Canonical Regime Checkpoints (Tiny-ViT V-series)

| File | Size | Date | Description | Tier candidate |
|:--|:--:|:--|:--|:--|
| V1_fp32_digital_baseline_best.pt | 20M | 2026-04-04 19:27 | FP32 digital baseline | A |
| V2_hybrid_no_noise_best.pt | 77M | 2026-04-04 22:37 | Zero-noise hybrid control (4-bit, no analog noise) | A |
| V2_hybrid_no_noise_last.pt | 77M | 2026-04-04 22:45 | Zero-noise hybrid control (last epoch) | B |
| V3_hybrid_standard_noise_standard_train_best.pt | 77M | 2026-04-05 00:41 | Standard-noise fixed-mask deployment | A |
| V3_hybrid_standard_noise_standard_train_last.pt | 77M | 2026-04-05 00:41 | Standard-noise fixed-mask (last epoch) | B |
| V4_hybrid_standard_noise_hat_best.pt | 77M | 2026-04-05 02:07 | Canonical HAT (uniform noise) — **main load-bearing** | A |
| V4_hybrid_standard_noise_hat_last.pt | 77M | 2026-04-05 02:07 | Canonical HAT (last epoch) | B |
| V5_hybrid_pessimistic_noise_hat_last.pt | 77M | 2026-04-05 03:24 | Pessimistic-noise HAT | B |
| V5_hybrid_pessimistic_noise_hat_best.pt | 77M | 2026-04-05 03:33 | Pessimistic-noise HAT (best) | B |
| V6_hybrid_hat_with_physical_frontend_best.pt | 77M | 2026-04-05 04:56 | HAT + physical frontend (inverse-gamma, shot noise) | A |
| V6_hybrid_hat_with_physical_frontend_last.pt | 77M | 2026-04-05 04:59 | Physical frontend (last epoch) | B |
| V7_hybrid_hat_with_retention_best.pt | 77M | 2026-04-05 06:21 | HAT + retention drift (uniform model) | A |
| V7_hybrid_hat_with_retention_last.pt | 77M | 2026-04-05 06:24 | Retention (last epoch) | B |
| V8_hybrid_hat_with_retention_aware_training_best.pt | 77M | 2026-04-09 06:40 | Retention-aware training (scale recalibration) | A |
| V8_hybrid_hat_with_retention_aware_training_last.pt | 77M | 2026-04-09 06:48 | Retention-aware training (last epoch) | B |

## Canonical Regime Checkpoints (ResNet-18 R-series)

| File | Size | Date | Description | Tier candidate |
|:--|:--:|:--|:--|:--|
| R1_FP32_baseline_best.pt | 86M | 2026-04-03 10:21 | FP32 digital baseline | A |
| R2_4bit_no_noise_best.pt | 128M | 2026-04-03 10:59 | Zero-noise hybrid control | A |
| R3_4bit_noise_standard_best.pt | 128M | 2026-04-03 11:04 | Standard-noise fixed-mask | A |
| R4_4bit_noise_HAT_best.pt | 128M | 2026-04-03 12:12 | Canonical HAT | A |
| R5_4bit_pessimistic_HAT_best.pt | 128M | 2026-04-03 12:50 | Pessimistic-noise HAT | B |
| R6_6bit_noise_HAT_best.pt | 128M | 2026-04-03 13:26 | 6-bit ADC HAT | B |

## Canonical Regime Checkpoints (ConvNeXt C-series)

| File | Size | Date | Description | Tier candidate |
|:--|:--:|:--|:--|:--|
| C1_FP32_baseline_best.pt | 107M | 2026-04-04 16:05 | FP32 digital baseline | A |
| C2_4bit_no_noise_best.pt | 211M | 2026-04-03 22:52 | Zero-noise hybrid control | A |
| C3_4bit_noise_standard_best.pt | 211M | 2026-04-03 23:31 | Standard-noise fixed-mask | A |
| C4_4bit_noise_HAT_best.pt | 211M | 2026-04-04 00:57 | Canonical HAT | A |
| C5_4bit_pessimistic_HAT_best.pt | 211M | 2026-04-04 11:55 | Pessimistic-noise HAT | B |
| C6_6bit_noise_HAT_best.pt | 211M | 2026-04-04 12:56 | 6-bit ADC HAT | B |
| C7_4bit_HAT_ADC4_best.pt | 211M | 2026-04-04 13:58 | 4-bit ADC HAT | B |
| C8_4bit_HAT_ADC6_best.pt | 211M | 2026-04-04 14:58 | 6-bit ADC HAT (alt config) | B |

---

## Tier Summary (preliminary)

| Tier | Files | Est. size | Strategy |
|:--|:--:|:--:|:--|
| **A** — paper-load-bearing | ~12 | ~1.5 GB | Zenodo DOI at submission |
| **B** — supp-load-bearing | ~12 | ~1.8 GB | Zenodo second record or tar shard |
| **C** — exploratory / last-epoch duplicates | ~5 | ~0.4 GB | Stay local; catalogued here |

## Open items

1. **NL mitigation lanes:** MLP-only, QKV-only, all-linear, attn_proj-only checkpoints need to be added to this inventory once lanes finish.
2. **Fresh-instance eval ckpts:** OPECT zero-shot transfer ckpt (Ensemble HAT V4) must be added.
3. **CrossSim phase ckpts:** ConvNeXt C4 checkpoint used for CrossSim comparison must be added.
4. **SHA-256:** Not yet computed. Will be added at Zenodo tar time.
5. **Tier finalization:** Pending Claude triage against `PROVENANCE_AUDIT_20260418.md`.
