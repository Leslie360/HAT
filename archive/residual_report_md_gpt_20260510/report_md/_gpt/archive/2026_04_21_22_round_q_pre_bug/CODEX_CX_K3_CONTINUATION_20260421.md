# CX-K3 Continuation: delta_g_eff Full Sweep

- Warm-start: `checkpoints/_gpt/second_order_ste/V4_hybrid_standard_noise_hat_second_order_ste_best.pt`
- Epochs per run: `100`
- Batch size: `128`
- Num workers: `0`
- Fresh protocol: `10 fresh x 5 eval`

| tag | delta_g_eff | train best acc | train best epoch | fresh mean | fresh std |
|:--|--:|--:|--:|--:|--:|
| k3_dgeff_0p05 | 0.05 | 91.52 | 72 | 36.21 | 9.61 |
| k3_dgeff_0p10 | 0.10 | 90.97 | 92 | 30.79 | 11.59 |
| k3_dgeff_0p15 | 0.15 | 91.27 | 82 | 27.85 | 7.37 |
| k3_dgeff_0p20 | 0.20 | 91.50 | 93 | 33.25 | 10.29 |
| k3_dgeff_0p25 | 0.25 | 91.24 | 76 | 30.08 | 9.07 |

- Best candidate: `k3_dgeff_0p05`
- Aggregate JSON: `report_md/_gpt/json_gpt/cx_k3_dgeff_continuation.json`
