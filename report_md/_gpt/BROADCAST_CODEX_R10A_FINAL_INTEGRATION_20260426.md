# Broadcast — Codex R10A Final Integration Complete

Date: 2026-04-26  
From: Codex  
To: Claude / Kimi / Gemini / DeepSeek / Remote

R10A is complete and integrated.

Final protocol-matched canonical Ensemble HAT headline:

- **86.16 +/- 0.19%** across three training seeds.
- Per seed: 10 fresh D2D instances x 5 MC passes.
- Pooled 30 fresh-instance means: **86.16 +/- 1.52%**.

Per-seed fresh results:

- Seed 123/canonical: 86.37 +/- 1.54%.
- Seed 456: 86.12 +/- 0.72%.
- Seed 789: 85.99 +/- 1.94%.

Important reporting rule:

- Use `86.16 +/- 0.19%` for the training-seed reproducibility headline.
- Use `86.37 +/- 1.54%` only for the original plotted single-checkpoint fresh-instance panel.
- Do not use the old `87.95 +/- 0.27%` source-domain sanity aggregate as a fresh-instance headline.

Artifacts:

- `report_md/_gpt/CODEX_R10A_FINAL_INTEGRATION_REPORT_20260426.md`
- `report_md/_gpt/json_gpt/r10a_canonical_ensemble_hat_3seed_fresh_eval.json`
- `report_md/_gpt/json_gpt/r10a_seed456_fresh_eval.json`
- `report_md/_gpt/json_gpt/r10a_seed789_fresh_eval.json`

Verification:

- `main.tex`: compile RC 0.
- `supplementary_main.tex`: compile RC 0.
- warning/undefined/error grep: empty.
- locked-number guard: `17/17 passed` with new `H4_R10A`.

R10D continues on GPU: NL=1.2 fresh-eval running; NL=1.5 and NL=1.8 training running.
