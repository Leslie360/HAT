# CODEX R10 Takeover Audit — R10B/R10E Guardrails + R10A Monitor
**Date:** 2026-04-26 01:25 CST  
**Author:** Codex  
**Status:** ACTIVE — R10A training running; R10B canonical full diagnostic running on CPU

## 1. Executive Summary

Codex resumed ownership after Gemini/DeepSeek proxy work and found two correctness risks before final R10 integration:

1. **R10B evidence-chain risk:** the completed `run_r10b.py` output evaluated post-fix M-series checkpoints, not the canonical Standard-HAT checkpoint that produces the paper-locked `10.00%` fresh-instance collapse. Those results are useful as a diagnostic control but cannot be used as the canonical collapse-mechanism evidence.
2. **R10E false-baseline risk:** `train_aihwkit_baseline.py` used a two-layer `TinyViTDummy` placeholder. Any accuracy from that script would be scientifically invalid as an AIHWKit head-to-head baseline.

Both risks are now guarded in code. No GPU training process was interrupted.

## 2. R10A Monitor Status

R10A training remains healthy on the local RTX 5070 Ti. Text logs are sparse because `log_interval=20`; checkpoint metadata is the authoritative progress signal between log points.

| Seed | Last checkpoint epoch | Best epoch | Best test acc | Status |
|---:|---:|---:|---:|---|
| 456 | 34 | 28 | 88.76% | healthy |
| 789 | 33 | 33 | 88.84% | healthy |

No R10A escalation trigger is active. Both best accuracies are above the expected 80% floor and above the initial epoch-19 readings.

## 3. R10B Correction

### Finding

The previous R10B JSON (`report_md/_gpt/json_gpt/r10b_standard_hat_class_distribution.json`) and figure were generated from:

- `checkpoints/_gpt/postfix_m_series/cx_m1_standard_seed123/V3_hybrid_standard_noise_standard_train_best.pt`
- `checkpoints/_gpt/postfix_m_series/cx_m2_ensemble_seed123/V4_hybrid_standard_noise_hat_best.pt`

This explains the near-uniform entropy and ~80% accuracy. It does **not** test the canonical fixed-mask collapse checkpoint:

- `checkpoints/V4_hybrid_standard_noise_hat_best.pt`

### Action Taken

- Archived old M-series output:
  - `report_md/_gpt/json_gpt/r10b_postfix_mseries_class_distribution_20260426.json`
  - `paper/latex_gpt/figures/figS_standard_hat_postfix_mseries_distribution_20260426.pdf`
  - `paper/latex_gpt/figures/figS_standard_hat_postfix_mseries_distribution_20260426.png`
- Rewrote `scripts/_gpt/run_r10b.py` to make probe families explicit:
  - `canonical_standard_hat`
  - `canonical_ensemble_hat`
  - `postfix_mseries_standard_hat`
  - `postfix_mseries_ensemble_hat`
- Added structured provenance, summary stats, `max_freq`, entropy fraction vs `ln(10)`, and a warning that M-series controls must not be cited as canonical collapse evidence.
- Smoke test on CPU, one batch:
  - canonical Standard HAT: `6.25%` batch accuracy, entropy ~`0`, max class frequency `100%`.
  - canonical Ensemble HAT: `93.75%` batch accuracy, non-collapsed prediction distribution.

### Current Run

Full canonical R10B is running in a persistent CPU PTY session:

```bash
OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 \
/home/qiaosir/miniconda3/envs/LLM/bin/python scripts/_gpt/run_r10b.py \
  --mode canonical \
  --device cpu \
  --num-instances 5 \
  --batch-size 64 \
  --num-workers 0 \
  --output-json report_md/_gpt/json_gpt/r10b_standard_hat_class_distribution.json \
  --output-figure-pdf paper/latex_gpt/figures/figS_standard_hat_collapse_mechanism.pdf \
  --output-figure-png paper/latex_gpt/figures/figS_standard_hat_collapse_mechanism.png
```

This run uses CPU only to avoid interfering with R10A.

## 4. R10E Guardrail

### Finding

The previous AIHWKit script trained a placeholder two-layer CNN (`TinyViTDummy`). This is not Tiny-ViT, does not contain grouped/depthwise/operator coverage issues, and would produce a false baseline.

### Action Taken

- Replaced `scripts/_gpt/train_aihwkit_baseline.py` with a real Tiny-ViT AIHWKit conversion feasibility probe.
- The new script refuses to train a dummy model.
- It writes `report_md/_gpt/json_gpt/r10e_aihwkit_conversion_probe.json` with one of:
  - `blocked_aihwkit_import_failed`
  - `blocked_real_tinyvit_conversion_failed`
  - `conversion_succeeded_training_not_run`
- Updated `scripts/_gpt/run_r10e.sh` wording from baseline training to conversion feasibility probe.

Paper-safe rule: R10E can support a tooling-coverage limitation if conversion fails; it must not be framed as AIHWKit being numerically worse unless a real Tiny-ViT AIHWKit training/eval protocol succeeds.

## 5. Verification

Completed:

- `py_compile` passed for:
  - `scripts/_gpt/run_r10b.py`
  - `scripts/_gpt/train_aihwkit_baseline.py`
- `bash -n` passed for:
  - `scripts/_gpt/run_r10a.sh`
  - `scripts/_gpt/run_r10d.sh`
  - `scripts/_gpt/run_r10e.sh`
- Direct dual-bug regression script passed all 7 checks:
  - LTP/LTD branch swap
  - no extraneous NL multiplier
  - second-order branch mapping
  - eval provenance mismatch rejection
  - NL=1.5 gradient finite check

Not completed:

- `pytest` is unavailable in the active `LLM` environment.
- The CUDA AMP groupwise unittest was not pursued because stale `nvidia-smi` monitor processes entered D-state; GPU training is left untouched.

## 6. Immediate Next Steps

1. Let R10A continue until early-stop or 100 epochs, then run fresh-eval for seeds 456 and 789.
2. When full canonical R10B lands, replace the current M-series wording in `05_results.tex` and `supplementary.tex` with canonical collapse-mechanism language if the full-data result matches the smoke test.
3. Do not launch R10D until R10A training and fresh-eval have completed, unless user explicitly prioritizes parallel GPU contention.
4. Treat R10E as a conversion-coverage probe unless real Tiny-ViT conversion succeeds.
