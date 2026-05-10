# Kimi P4 Track A Report: Bundle Split

**Date:** 2026-05-09
**Dispatch:** `DISPATCH_SUPERPHASE_P4_SUBMISSION_GRADE_FINALIZATION_20260509.md`
**Executor:** kimi
**Verdict:** SPLIT COMPLETE

---

## 1. Submission Bundle

**Path:** `release_artifacts/paper1_submission_bundle_20260509_final/`

**Files:** 139 (138 checksums)

**Contents:**
- `main.pdf`, `supplementary_main.pdf`, `cover_letter.pdf`
- `main.tex`, `supplementary.tex`, `supplementary_main.tex`, `cover_letter.tex`
- `refs_gpt.bib`
- `sections/` — 9 active section files
- `supplementary/` — 11 tex files (supplementary sections + TikZ sources)
- `figures/` — 38 files (only referenced figures + TikZ sources)
- `source_data/` — active canonical JSON, CSVs, manifests (no deprecated)
- `RELEASE_README.md`, `MANIFEST_FILES.txt`, `SHA256SUMS.txt`

**Excluded from submission bundle (moved to provenance archive):**
- `source_data/canonical_json/deprecated_20260501_old_protocol/` — old-protocol 6-bit artifacts
- `figures/deprecated_20260424/` — pre-plotrefresh figures
- 35 orphan figures not referenced by current LaTeX
- All build artifacts (`.aux`, `.log`, `.out`, etc.)

---

## 2. Provenance Archive

**Path:** `release_artifacts/paper1_provenance_archive_20260509/`

**Files:** 72 (71 checksums)

**Contents:**
- `deprecated_20260501_old_protocol/` — superseded old-protocol 6-bit JSON
- `deprecated_20260424/` — pre-plotrefresh figure versions
- `orphan_figures/` — 35 unreferenced legacy figures
- `PROVENANCE_README.md`
- `MANIFEST_FILES.txt`, `SHA256SUMS.txt`

---

## 3. Verdict

Two-artifact split complete. Submission bundle is reviewer-facing and contains no deprecated paths or stale strings. Provenance archive is clearly separated and documented.

---

*Report by kimi. Split executed on 2026-05-09.*
