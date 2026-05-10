# Codex R10A Final Integration Report

Date: 2026-04-26  
Owner: Codex  
Status: COMPLETE for R10A; R10D continuing in background

## Executive Verdict

R10A is complete. The protocol-matched canonical Ensemble HAT fresh-instance aggregate is:

- **86.16 +/- 0.19%** across three training seeds.
- Statistic: mean +/- sample standard deviation of seed-level fresh-instance means.
- Per seed: 10 fresh D2D instances x 5 Monte Carlo passes per instance.

This supersedes using the historical `87.95 +/- 0.27%` source-domain sanity value as any fresh-instance headline. The original plotted checkpoint remains valid as a single-checkpoint deployment panel:

- **86.37 +/- 1.54%** across 10 fresh instances for the original canonical checkpoint.

## Per-Seed Results

| Seed | Checkpoint | Source Best | Fresh Mean +/- Std |
|---|---|---:|---:|
| 123 / canonical | `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` | 91.94% | 86.37 +/- 1.54% |
| 456 | `checkpoints/_ensemble/V4_hybrid_seed456/V4_hybrid_standard_noise_hat_best.pt` | 89.58% | 86.12 +/- 0.72% |
| 789 | `checkpoints/_ensemble/V4_hybrid_seed789/V4_hybrid_standard_noise_hat_best.pt` | 90.66% | 85.99 +/- 1.94% |

Aggregate:

- Seed means: `[86.3650, 86.1232, 85.9880]`.
- Cross-seed mean +/- sample std: `86.16 +/- 0.19%`.
- Pooled 30 fresh-instance means: `86.16 +/- 1.52%`.

## Artifacts

- Aggregate JSON: `report_md/_gpt/json_gpt/r10a_canonical_ensemble_hat_3seed_fresh_eval.json`
- Seed 456 JSON: `report_md/_gpt/json_gpt/r10a_seed456_fresh_eval.json`
- Seed 789 JSON: `report_md/_gpt/json_gpt/r10a_seed789_fresh_eval.json`
- Seed 456 train log: `logs/_gpt/r10a_seed456.log`
- Seed 789 train log: `logs/_gpt/r10a_seed789.log`

## Manuscript Integration

Patched:

- `paper/latex_gpt/sections/00_abstract.tex`
- `paper/latex_gpt/sections/01_introduction.tex`
- `paper/latex_gpt/sections/03_methodology.tex`
- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/sections/06_discussion.tex`
- `paper/latex_gpt/sections/07_conclusion.tex`
- `paper/latex_gpt/sections/08_appendix.tex`
- `paper/latex_gpt/supplementary.tex`
- `paper/latex_gpt/supplementary/design_rules_box.tex`
- `paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex`
- `paper/latex_gpt/cover_letter.tex`
- `scripts/_gpt/check_locked_numbers.py`
- `report_md/_gpt/KIMI_R10A_INTEGRATION_TEMPLATE_20260426.md`

Text policy now used:

- Use `86.16 +/- 0.19%` as the three-seed fresh-instance headline.
- Use `86.37 +/- 1.54%` only when referring to the original plotted single-checkpoint fresh-instance panel.

## Verification

Commands run:

```bash
cd /home/qiaosir/projects/compute_vit/paper/latex_gpt
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex
grep -i "warning\|undefined\|error" main.log supplementary_main.log | grep -v infwarerr || true
cd /home/qiaosir/projects/compute_vit
/home/qiaosir/miniconda3/envs/LLM/bin/python scripts/_gpt/check_locked_numbers.py
```

Results:

- `main.tex`: compile RC 0.
- `supplementary_main.tex`: compile RC 0.
- Warning/undefined/error grep: empty.
- Locked-number guard: `17/17 passed` with new `H4_R10A` check.

## Continuing GPU Work

R10D remains active:

- `NL=1.2`: training complete at source best `83.12%`; fresh-instance eval is running.
- `NL=1.5`: training running.
- `NL=1.8`: training running.
