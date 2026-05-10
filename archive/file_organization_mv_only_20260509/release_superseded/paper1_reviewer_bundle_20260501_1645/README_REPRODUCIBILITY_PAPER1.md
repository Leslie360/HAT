# Paper-1 Reproducibility Notes

This package supports the locked Paper-1 result spine:

1. 8-bit AIHWKit baseline is stable under fresh device instances.
2. Pure 4-bit analog quantization collapses.
3. Ensemble HAT rescues the 4-bit regime.
4. PCM UnitCell training yields a 4/6/8-bit precision-retention frontier, with 6-bit as the best tested Pareto midpoint.

## Quick Verification

Run from the project root:

```bash
python scripts/_gpt/check_locked_numbers.py
python scripts/_gpt/check_local_pcm_precision_ladder.py
python scripts/_gpt/audit_latex_bib_keys.py
```

Expected results:

- `check_locked_numbers.py`: `22/22 passed`
- `check_local_pcm_precision_ladder.py`: `Result: PASS`
- `audit_latex_bib_keys.py`: `missing_key_count: 0`

## LaTeX Build

Run from `paper/latex_gpt`:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex
```

Current verified outputs:

- `paper/latex_gpt/main.pdf`: 14 pages
- `paper/latex_gpt/supplementary_main.pdf`: 41 pages

## Canonical Evidence

Small JSON evidence is copied into:

```text
paper/latex_gpt/source_data/canonical_json/
```

This directory includes the canonical fresh-instance, drift, and training-history JSONs needed to verify the locked numbers without shipping large `.pt` checkpoints.

Key manifest files:

```text
paper/latex_gpt/source_data/canonical_json/manifest_canonical_json_20260501.csv
paper/latex_gpt/source_data/canonical_json/manifest_canonical_json_20260501.json
paper/latex_gpt/source_data/manifest_all_figures_20260501.csv
paper/latex_gpt/source_data/manifest_bib_key_audit_20260501.json
paper/latex_gpt/source_data/manifest_bib_doi_resolution_20260501.json
```

## Locked Numbers

Primary locked-number table:

```text
outputs/CANONICAL_NUMBERS_FROZEN_20260430.md
```

Protocol details:

```text
paper2_aihwkit_baseline/PCM_PROTOCOL.md
```

Important protocol note: canonical PCM ladder artifacts completed the intended 100-epoch schedule. Most runs used `--early-stop-patience 0`; `r11d_6bit_pcm_seed789` recorded `early_stop_patience=10` but did not trigger early stop and logged 100 epochs. Use per-run `training_history.json` and provenance fields as the source of truth.

## Full Training Regeneration

Full regeneration requires CUDA and AIHWKit. The reviewer bundle is designed for verification from JSON evidence first; full retraining is optional and expensive.

Canonical scripts:

```text
paper2_aihwkit_baseline/r11d4_train_pcm.py
paper2_aihwkit_baseline/eval_aihwkit_fresh.py
paper2_aihwkit_baseline/eval_aihwkit_drift_extended.py
paper2_aihwkit_baseline/run_pcm_multi_seed_validation.sh
paper2_aihwkit_baseline/run_kimi_r11d_6bit_multiseed_20260430.sh
paper2_aihwkit_baseline/run_r11d7_pcm_4bit.sh
```

## What Is Excluded

Large checkpoint weights are intentionally excluded from reviewer bundles:

```text
*.pt
paper2_aihwkit_baseline/checkpoints/**/best.pt
paper2_aihwkit_baseline/checkpoints/**/last.pt
```

Do not exclude the small canonical JSON evidence listed above.

## Scope Boundary

Remote 105 cross-architecture results and Remote 107 Analog KV-cache results are not required for Paper-1. They are optional validation or separate Work-2 material.
