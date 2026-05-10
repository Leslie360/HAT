# DISPATCH CODEX-FRESH-EVAL-MSERIES — Local M-series Fresh Instance Eval
**Date:** 2026-04-24
**Issued by:** Claude
**Assignee:** Codex
**Priority:** HIGH
**Depends on:** CX-M1..M6 training complete (done)
**Time budget:** ~3-6 GPU-h total on local GPU, no new training

---

## 1. Objective

Run fresh-instance eval (10 D2D instances × 5 MC runs) on all 6 local M-series checkpoints. Produce a single unified cross-host parity table combining local CX-M results with remote R-M results under matched methodology. No new training.

Closes the cross-host reproducibility loop without A100 time.

---

## 2. Checkpoints to evaluate

All at `checkpoints/_gpt/postfix_m_series/`:

| Checkpoint ID | Config | Path | Training best |
|:--|:--|:--|:--|
| CX-M1 | V3 Standard HAT seed 123 | `cx_m1_standard_seed123/V3_hybrid_standard_noise_standard_train_best.pt` | 82.89% |
| CX-M2 | V4 Ensemble HAT seed 123 | `cx_m2_ensemble_seed123/V4_hybrid_standard_noise_hat_best.pt` | 80.97% |
| CX-M3 | V4 Proportional HAT seed 123 | `cx_m3_proportional_seed123/V4_hybrid_standard_noise_hat_best.pt` | 80.88% |
| CX-M4 | V4 Proportional HAT seed 456 | `cx_m4_proportional_seed456/V4_hybrid_standard_noise_hat_best.pt` | 81.39% |
| CX-M5 | V3 Standard HAT seed 456 | `cx_m5_standard_seed456/V3_hybrid_standard_noise_standard_train_best.pt` | 80.69% |
| CX-M6 | V4 Ensemble HAT seed 456 | `cx_m6_ensemble_seed456/V4_hybrid_standard_noise_hat_best.pt` | 81.87% |

All trained at NL=±2.0, batch=64, local GPU.

---

## 3. Fresh-eval protocol (match remote methodology)

Use `scripts/eval_fresh_instances_postfix.py` (at commit 33bed9c) with:

- `--num-instances 10`
- `--mc-runs 5`
- `--nl-ltp 2.0 --nl-ltd -2.0` (EXPLICIT — not defaults)
- `--sigma-d2d 0.10 --sigma-c2c 0.05` (canonical)
- `--noise-mode <uniform for Standard/Ensemble; proportional for Proportional>` (must match training config — check checkpoint metadata)
- Same random seed protocol as remote R-M series (document which seeds used for fresh instance D2D sampling)

Output per checkpoint:
- `report_md/_gpt/json_gpt/cx_m{N}_fresh_eval.json`
- Fields: `fresh_per_instance_mean[]` (10 values), `fresh_aggregate.mean`, `.std`, `.median`, `.range`, `nl_ltp`, `nl_ltd`, `commit_hash`, `cuda_device_name`, `pytorch_version`

---

## 4. Consolidated parity table

After all 6 evals land, produce **one CSV + one MD table**:

`report_md/_gpt/csv_gpt/cross_host_parity_mseries.csv`:
```
run_id, host, model, hat_type, seed, batch_size, nl, train_best, fresh_mean, fresh_std, fresh_range
CX-M1, local, V3, Standard, 123, 64, 2.0, 82.89, [...], [...], [...]
CX-M2, local, V4, Ensemble, 123, 64, 2.0, 80.97, [...], [...], [...]
CX-M3, local, V4, Proportional, 123, 64, 2.0, 80.88, [...], [...], [...]
CX-M4, local, V4, Proportional, 456, 64, 2.0, 81.39, [...], [...], [...]
CX-M5, local, V3, Standard, 456, 64, 2.0, 80.69, [...], [...], [...]
CX-M6, local, V4, Ensemble, 456, 64, 2.0, 81.87, [...], [...], [...]
R-M1, remote, V3, Standard, 123, 512, 2.0, 83.75, 83.64, 0.10, 0.42
R-M2 s123, remote, V4, Proportional, 123, 512, 2.0, 84.79, 84.80, 0.08, 0.32
R-M2 s222, remote, V4, Proportional, 222, 512, 2.0, 84.71, 84.79, 0.07, 0.23
R-M2 s333, remote, V4, Proportional, 333, 512, 2.0, 83.23, [TBD], [TBD], [TBD]
R-M2 s789, remote, V4, Proportional, 789, 512, 2.0, 83.38, [TBD], [TBD], [TBD]
R-M2 s999, remote, V4, Proportional, 999, 512, 2.0, 83.72, [TBD], [TBD], [TBD]
R-M5 s567, remote, V3, Standard, 567, 512, 2.0, 83.67, [TBD], [TBD], [TBD]
R-M5 s890, remote, V3, Standard, 890, 512, 2.0, 82.20, [TBD], [TBD], [TBD]
```

Remote R-M1/R-M2 s123/s222 fresh-eval numbers user already provided (84.80±0.08, 84.79±0.07, 83.64±0.10). For rows marked [TBD], leave as TBD if user hasn't provided fresh-eval for all remote seeds.

---

## 5. Aggregate statistics

Compute aggregate per group:

| Group | n seeds | Fresh mean ± std (across seeds) |
|:--|--:|:--|
| Local V3 Standard (M1, M5) | 2 | [compute] |
| Local V4 Ensemble (M2, M6) | 2 | [compute] |
| Local V4 Proportional (M3, M4) | 2 | [compute] |
| Remote V3 Standard (R-M1 fresh) | 1-3 | [compute if user provides] |
| Remote V4 Proportional (R-M2 fresh) | 2-5 | [compute from user-provided values] |

---

## 6. Cross-host delta analysis

For each matching config, compute `remote_fresh_mean - local_fresh_mean`:
- V3 Standard: ΔR-L (seed 123)
- V4 Proportional: ΔR-L (seed 456 — nearest match; note seeds differ)

State whether the ~1-2pp remote advantage is consistent across HAT types (hypothesis: batch=512 recipe delta, ~1-2pp) or varies (hypothesis: HAT-type-specific sensitivity).

---

## 7. Deliverables

1. 6 JSON files in `json_gpt/cx_m{N}_fresh_eval.json`
2. `csv_gpt/cross_host_parity_mseries.csv`
3. `report_md/_gpt/CODEX_CX_FRESH_EVAL_MSERIES_REPORT_20260424.md` with:
   - The aggregate statistics table
   - Cross-host delta analysis paragraph
   - Any anomalies (e.g., a fresh-eval way off from training-best → could indicate checkpoint corruption)

---

## 8. Constraints

- **No new training.** Only evaluation.
- **Match remote methodology exactly**: 10 instances × 5 MC, explicit NL flags.
- **Save logs**: tee to `logs/_gpt/cx_m{N}_fresheval_<ts>.log` (per auto-memory feedback_save_logs.md).
- **Don't run concurrent with any other GPU job**: per auto-memory feedback_gpu_busy.md.
- **Document commit hash**: verify repo at `33bed9c` before eval starts; record in JSON outputs.

---

## 9. Success criteria

- Clean cross-host parity table usable as paper Supp Table directly.
- Any outlier clearly flagged (e.g., if local CX-M2 Ensemble fresh lands way below 80% it tells us something).
- Codex delivers within ~1 day of dispatch (no GPU contention).

**Time budget**: ~3-6 GPU-h total. No rush.
