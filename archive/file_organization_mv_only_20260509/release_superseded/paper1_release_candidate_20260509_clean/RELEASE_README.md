# Paper-1 Clean Release Candidate Bundle

**Date:** 2026-05-09
**Bundle:** `paper1_release_candidate_20260509_clean`
**Status:** Clean release candidate — P3 Track A completed

---

## Build Instructions

### Main Paper
```bash
tectonic main.tex
```

### Supplementary
```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex
```

### Cover Letter
`cover_letter.tex` is source-only; no automated build path configured.

---

## Canonical Numbers (PCM Precision Ladder)

| Precision | Fresh Mean | Fresh Std | 1h Drift | 1d Drift | 24h Drop | Role |
|-----------|-----------|-----------|----------|----------|----------|------|
| 8-bit PCM | 77.60% | 0.64 pp | 77.49% | 77.57% | ~0 pp | Deployment-stable practical point |
| 6-bit PCM | 68.55% | 6.03 pp | 68.57% | 68.46% | ~0 pp | D2D-sensitive transition zone |
| 4-bit PCM | 76.68% | 0.37 pp | 74.04% | 72.64% | -4.0 pp | Quantization-dominated, drift-costly |

**6-bit note:** Old protocol results (77.86%) have been superseded. New protocol values reflect `enable_during_test=True` training, which eliminates catastrophic fresh-instance collapse but lowers absolute accuracy.

---

## Deprecated Data Status

Old-protocol 6-bit artifacts are preserved under:
`source_data/canonical_json/deprecated_20260501_old_protocol/`

These are **not active release data** and are retained only for historical provenance.

---

## Bundle Contents

- `main.pdf` — Main paper (202.61 KiB)
- `supplementary_main.pdf` — Supplementary information (2.71 MiB)
- `cover_letter.tex` — Cover letter source
- `main.tex`, `supplementary_main.tex`, `supplementary.tex` — LaTeX sources
- `sections/` — Main text sections
- `supplementary/` — Supplementary sections and TikZ figure sources
- `figures/` — Active figures (includes unreferenced legacy figures retained for thesis use)
- `source_data/` — Canonical JSON, CSVs, manifests
- `MANIFEST_FILES.txt` — File listing (207 files)
- `SHA256SUMS.txt` — Cryptographic checksums (206 entries, self-excluded)

---

## Verification

Guard script: `python scripts/_gpt/check_local_pcm_precision_ladder.py`
Result: **PASS**

Stale-keyword scan: `rg -n "77.86|Pareto midpoint|seed456_full100" ...`
Result: **0 active hits**

PDF stale scans: **0 hits** in both `main.pdf` and `supplementary_main.pdf`

File-size scan: **0 files** larger than 20 MB

Checkpoint scan: **0** `.pt`/`.pth`/`.ckpt` files

SHA256 verification: **All OK**

---

## Known Orphan Figures

The following 35 figure files in `figures/` are **not referenced** by the current Paper-1 LaTeX sources. They are retained for thesis dual-use and backward compatibility:

- `fig1_paper1_spine.*`, `fig1_system_architecture.*`, `fig2_paper1_decision_map.*`, `fig2_weight_mapping.*`
- `fig3_snr_curves.*`, `fig4_accuracy_comparison.*`, `fig5_hat_recovery.*`
- `fig7_retention_curve.*`, `fig8_pareto_energy_accuracy.*`
- `fig10_zero_shot_transferability.*`, `fig11_energy_breakdown.*`
- `figA.*`, `figB.*`, `figC.*`, `figD.*`
- `figS1_asymmetry_concept.*`, `figS1_asymmetry_concept_gptimage.*`
- `figS2_nonideality.*`, `figS2_nonideality_gptimage.*`
- `figS3_ensemble_hat.*`, `figS3_weight_mapping_gptimage.*`
- `figS4_system_architecture_gptimage.*`
- `figS_aihwkit_comparison.*`, `figS_cross_host_parity.*`
- `figS_nl_sweep_ensemble.*`, `figS_standard_hat_postfix_mseries_distribution_20260426.*`
- `fig_attention_differences.*`, `fig_contour_map.*`, `fig_layer_sensitivity.*`
- `fig_nl_gradient_distortion_pilot.*`, `fig_postfix_severe_nl.*`
- `graphical_abstract.*`, `energy_breakdown_pie.*`, `energy_breakdown_stacked.*`

---

## Contact

For reproducibility questions, refer to `source_data/canonical_json/manifest_canonical_json_20260509.json`.
