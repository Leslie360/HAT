# Paper-1 Release Candidate Bundle

**Date:** 2026-05-09
**Bundle:** `paper1_release_candidate_20260509`
**Status:** Release candidate — pending DS/Mimo audit and Codex final acceptance

---

## Build Instructions

### Main Paper
```bash
cd paper/latex_gpt/
tectonic main.tex
```

### Supplementary
```bash
cd paper/latex_gpt/
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
- `main.tex`, `supplementary_main.tex` — LaTeX sources
- `sections/` — Main text sections
- `supplementary/` — Supplementary sections
- `figures/` — Active figures
- `source_data/` — Canonical JSON, CSVs, manifests
- `MANIFEST_FILES.txt` — File listing
- `SHA256SUMS.txt` — Cryptographic checksums

---

## Verification

Guard script: `python scripts/_gpt/check_local_pcm_precision_ladder.py`
Result: **PASS**

Stale-keyword scan: `rg -n "77.86|Pareto midpoint|seed456_full100" ...`
Result: **0 active hits**

---

## Contact

For reproducibility questions, refer to `source_data/canonical_json/manifest_canonical_json_20260509.json`.
