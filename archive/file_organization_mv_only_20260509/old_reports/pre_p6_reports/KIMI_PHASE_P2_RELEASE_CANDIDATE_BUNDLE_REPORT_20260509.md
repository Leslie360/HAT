# Kimi Phase P2 Report: Release Candidate Bundle and Clean-Room Guard

**Date:** 2026-05-09
**Issued by:** Codex dispatch `DISPATCH_PHASE_P2_RELEASE_CANDIDATE_BUNDLE_20260509.md`
**Executor:** kimi
**Verdict:** RELEASE-CANDIDATE VALID

---

## 1. Bundle Path

`/home/qiaosir/projects/compute_vit/release_artifacts/paper1_release_candidate_20260509/`

---

## 2. Files Included / Excluded

### Included (218 files)

| Category | Count | Key Files |
|----------|-------|-----------|
| PDF outputs | 2 | `main.pdf` (202.61 KiB), `supplementary_main.pdf` (2.71 MiB) |
| LaTeX sources | 2 | `main.tex`, `supplementary_main.tex` |
| Sections | ~40 | `sections/01_introduction.tex` through `sections/08_availability.tex` |
| Supplementary | ~30 | `supplementary/*.tex` |
| Figures | ~50 | `figures/*.pdf`, `figures/*.png` |
| Bibliography | 1 | `refs_gpt.bib` |
| Source data | ~60 | `source_data/canonical_json/*`, `source_data/*.csv` |
| Cover letter | 1 | `cover_letter.tex` |
| Bundle docs | 3 | `RELEASE_README.md`, `MANIFEST_FILES.txt`, `SHA256SUMS.txt` |

### Explicitly Excluded

- `.pt` checkpoint files (>80MB each)
- Raw training directories (`paper2_aihwkit_baseline/checkpoints/`)
- Temporary render/test PDFs
- Old release bundles
- ChatGPT image prompt PNGs not referenced by LaTeX

### Deprecated (included but clearly marked)

- `source_data/canonical_json/deprecated_20260501_old_protocol/` — Old-protocol 6-bit artifacts, superseded manifest

---

## 3. Build Command Outputs

### main.tex
```bash
tectonic main.tex
```
- **Result:** SUCCESS
- **Output:** `main.pdf` (202.61 KiB)
- **Warnings:** algorithm.sty UTF-8 cosmetic issue; bbl rerun consistency (cosmetic)

### supplementary_main.tex
```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex
```
- **Result:** SUCCESS
- **Output:** `supplementary_main.pdf` (2.71 MiB)
- **Warnings:** Underfull/Overfull hbox (cosmetic); bbl rerun consistency (cosmetic)

### cover_letter.tex
- **Status:** Source-only; no automated build path configured

---

## 4. Guard Outputs

### 4.1 Stale Keyword Grep

```bash
rg -n "77\.86|77\.88|77\.83|77\.76|78\.49|Pareto midpoint|best observed Pareto|critical Pareto|6-bit midpoint|seed456_full100|r11d_6bit_pcm_seed456_full100" <bundle> \
  --glob '!**/deprecated_20260501_old_protocol/**'
```

**Result:** 0 active hits.

### 4.2 PDF Stale Scans

```bash
pdftotext main.pdf - | rg -n "77\.86|75\.43|72\.67|seed456_full100|6-bit midpoint|Pareto midpoint|pending|78\.49"
```
**Result:** No hits.

```bash
pdftotext supplementary_main.pdf - | rg -n "77\.86|75\.43|72\.67|seed456_full100|6-bit midpoint|Pareto midpoint|6-bit.*pending|pending.*6-bit|78\.49"
```
**Result:** No hits.

### 4.3 Python Guard

```bash
python scripts/_gpt/check_local_pcm_precision_ladder.py
```

**Result:** PASS
- 8-bit: all checks pass
- 6-bit: all checks pass (1 expected WARN for missing seed123 training_history)
- 4-bit: all checks pass

---

## 5. File-Size Scan

```bash
find <bundle> -type f -size +20M -print
```

**Result:** 0 files larger than 20 MB.

Largest files in bundle:
| File | Size |
|------|------|
| `supplementary_main.pdf` | 2.71 MiB |
| `figures/figS2_nonideality_gptimage.png` | ~1.2 MiB |
| `main.pdf` | 202.61 KiB |

---

## 6. SHA256 Manifest Status

- `MANIFEST_FILES.txt`: 218 files listed
- `SHA256SUMS.txt`: 218 checksums generated
- Both files are inside the release candidate directory

---

## 7. Remaining Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| `cover_letter.tex` has no build path | Low | Documented in RELEASE_README.md; reviewer can read source |
| `algorithm.sty` UTF-8 warnings in tectonic | Low | Cosmetic; output PDF is correct |
| Latexmk not tested for main.tex (only tectonic) | Low | Tectonic is primary; latexmk available if reviewer prefers |
| No automated figure regeneration pipeline in bundle | Low | Figures are pre-generated PDFs/PNGs; source scripts exist in repo |

---

## 8. Verdict

**RELEASE-CANDIDATE VALID.**

The bundle is clean: no stale old-protocol artifacts in active paths, no oversized files, all guards pass, both PDFs build successfully, and the manifest/checksum infrastructure is in place. Ready for DS reproducibility audit, Mimo reviewer-facing completeness audit, and Codex final acceptance.

---

*Report by kimi. Bundle built and verified on 2026-05-09.*
