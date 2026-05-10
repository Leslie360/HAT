# Paper-1 Provenance Archive

**Date:** 2026-05-09
**Archive:** `paper1_provenance_archive_20260509`
**Purpose:** Historical provenance and deprecated data excluded from the active submission bundle.

---

## Why This Archive Exists

The submission bundle (`paper1_submission_bundle_20260509_final/`) contains only active claims and reviewer-facing materials. This archive preserves historical data for traceability, reproducibility audits, and thesis dual-use.

---

## Contents

### 1. Deprecated Old-Protocol PCM Artifacts

`deprecated_20260501_old_protocol/`

Old-protocol 6-bit PCM results from an earlier training configuration where `enable_during_test=False` caused noise-free training evaluation. These values are **superseded** and are retained solely for historical provenance.

**Status:** Not active release data.

### 2. Pre-Plotrefresh Figure Versions

`deprecated_20260424/`

Earlier versions of figures before a plot-refresh pass on 2026-04-24. Retained for visual provenance.

**Status:** Not active release figures.

### 3. Unreferenced Legacy Figures

`orphan_figures/`

Figure files not referenced by the current Paper-1 LaTeX sources. These include:
- Alternate versions of main-text figures
- GPT-image prompt variants
- Pilot and exploratory figures
- Graphical abstract and energy breakdown alternatives

**Status:** Retained for thesis dual-use and backward compatibility.

---

## Data-Use Policy

- Do not cite paths in this archive as active Paper-1 claims.
- Do not mix deprecated old-protocol values with current canonical numbers.
- For active claims, always use the submission bundle.

---

## Contact

For provenance questions, refer to the submission bundle's `source_data/canonical_json/manifest_canonical_json_20260509.json`.
