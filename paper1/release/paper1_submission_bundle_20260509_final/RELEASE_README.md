# Paper-1 Submission Bundle

**Date:** 2026-05-10
**Bundle:** `paper1_submission_bundle_20260509_final`
**Status:** Submission-grade candidate — refreshed after Codex narrative polish pass 2; retained for final author review

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
`cover_letter.pdf` is included; `cover_letter.tex` is provided as the corresponding LaTeX source.

---

## Canonical Numbers (PCM Precision Ladder)

| Precision | Fresh Mean | Fresh Std | 1h Drift | 1d Drift | 24h Drop | Role |
|-----------|-----------|-----------|----------|----------|----------|------|
| 8-bit PCM | 77.60% | 0.64 pp | 77.49% | 77.57% | ~0 pp | Deployment-stable practical point |
| 6-bit PCM | 68.44% | 6.03 pp | 68.46% | 68.36% | 0.04 pp | D2D-sensitive transition zone |
| 4-bit PCM | 76.68% | 0.37 pp | 74.04% | 72.64% | -4.0 pp | Quantization-dominated, drift-costly |

**Note on historical protocol:** The current 6-bit values reflect `enable_during_test=True` training. An earlier protocol (documented separately in the provenance archive) produced higher means with higher variance due to a training-evaluation noise separation bug. The current protocol eliminates catastrophic fresh-instance collapse.

---

## Bundle Contents

- `main.pdf` — Main paper
- `supplementary_main.pdf` — Supplementary information
- `cover_letter.pdf` — Cover letter PDF
- `cover_letter.tex` — Cover letter source
- `main.tex`, `supplementary.tex`, `supplementary_main.tex` — LaTeX sources
- `sections/` — Main text sections
- `supplementary/` — Supplementary sections and TikZ figure sources
- `figures/` — Active figures referenced by the manuscript
- `source_data/` — Canonical JSON, CSVs, manifests (active claims only)
- `MANIFEST_FILES.txt` — File listing
- `SHA256SUMS.txt` — Cryptographic checksums

---

## Exclusions

The following are intentionally excluded from this submission bundle and reside in the separate provenance archive:

- Deprecated old-protocol PCM artifacts
- Pre-plotrefresh figure versions
- Unreferenced legacy figures retained for thesis dual-use
- Build artifacts (`.aux`, `.log`, `.out`, etc.)

---

## Verification

Guard script: `python scripts/_gpt/check_local_pcm_precision_ladder.py`
Result: **PASS**

Stale-keyword scan: **0 active main-text hits for stale numeric/wording guards**

---

## Contact

For reproducibility questions, refer to `source_data/canonical_json/manifest_canonical_json_20260509.json`.
