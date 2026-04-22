# [⚠️ PROVISIONAL — Branch A] CX Minimal Parity Probes (2026-04-22)

> **⚠️ PROVISIONAL (2026-04-22):** The parity numbers below were produced on no-multiplier code with **incorrect second-order signs** (positive `+0.5` rather than ratified negative `-0.5`). They pre-date the second-order sign fix and remain **invalid pending re-run** on fully corrected code. The relative ranking (`all` > `mlp`) is noted but should not be treated as paper-grade evidence until refreshed.

---

*Original report follows below for archival purposes:*

# CX Minimal Parity Probes (2026-04-22)

- Warm-start: `checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- Mode: 1 epoch source-domain parity probes under fixed code

| tag | group | SO2 | delta_g_eff | alpha | train_acc | test_acc | best_epoch |
|:--|:--|:--:|:--:|:--:|--:|--:|--:|
| j1d_historical_auto | mlp | Y | -1.0 | 1.0 | 82.88 | 46.75 | 0 |
| j1d_literal_zero | mlp | Y | 0.0 | 1.0 | 82.47 | 57.00 | 0 |
| mlp_noso2_fixed | mlp | N | None | None | 82.34 | 55.65 | 0 |
| all_so2_auto | all | Y | -1.0 | 1.0 | 88.33 | 83.34 | 0 |
