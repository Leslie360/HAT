<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 9cdbe77 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# NC Submission Final Audit — K-V18

**Date:** 2026-04-20  
**Bundle:** `outputs/submission_bundle_20260419/`

---

## 1. Residual dependency on something not on disk?

**FAIL.** `source_data/source_data_v1.zip` is a symlink to `release_artifacts/source_data_v1.zip`. The target exists, but symlinks break during portal upload. Dereference to a physical copy before archiving.

## 2. Broken cross-refs between manuscript and Zenodo archive?

**PASS.** The manuscript Data Availability statement correctly states the Zenodo archive "will be assigned a DOI at acceptance." The Zenodo README and SHA-256 manifest are present and consistent.

## 3. Placeholders beyond user-owned fields?

**PASS.** Only `TBD` appears in `README_SUBMISSION.txt` for author name, email, and affiliation. No `TODO`, `FIXME`, or `PLACEHOLDER` strings remain in the manuscript, cover letter, or supplementary source.

## 4. Does the bundle contain all required files per K-T7 checklist?

**FAIL.** The bundle is missing `.bbl` files for both main and supplementary manuscripts. Nature Communications does not accept raw `\bibliography` commands; references must be inlined or supplied as `.bbl`. Furthermore, the `.tex` and `.bib` citation keys are mismatched (see Item 7), so recompilation from the bundle source would fail even if `.bbl` files were present.

## 5. Locked numbers consistent with Zenodo source-data README?

**PASS.** The `check_locked_numbers.py` guard script reports **16/16 PASS**. All headline numbers (89.85 %, 86.37 %, 10.00 %, 27.72 %, 88.53 %, etc.) match their canonical JSON sources within tolerance. The Zenodo manifest cross-references the same files.

## 6. Abstract ≤ 150 words?

**PASS.** `detex sections/00_abstract.tex | wc -w` = **142 words**.

## 7. Unresolved citations (?? in PDF)?

**PASS in compiled PDFs — FAIL in bundle source.**

Both compiled PDFs contain **zero** unresolved `[?]` markers. However, the source files have a critical citation-key inversion:

| Key | Manuscript `.tex` | Manuscript `.bib` | Supplementary `.tex` | Supplementary `.bib` |
|---|---|---|---|---|
| Zhang OPECT | `zhang2026opect` | `zhang2025opect` ❌ | `zhang2025opect` | `zhang2026opect` ❌ |
| Vincze dual-plasticity | `vincze2026dualplasticity` | `vincze2025dualplasticity` ❌ | `vincze2025dualplasticity` | `vincze2026dualplasticity` ❌ |
| IconNiV | `iconniv2025` | `iconniv2026` ❌ | — | `iconniv2025` ✅ |

**Fix:** Harmonise keys to a single suffix (recommend 2025 for Zhang/Vincze, 2026 for IconNiV to match the repo master) and include the matching `.bbl` files.

## 8. Cover letter ready except user-specific fields?

**PASS.** `cover_letter.tex` contains the editorial summary, fit statement, four key contributions, and transparency disclosures. Remaining blanks (ORCID, suggested reviewers, full contact details) are correctly deferred to the portal form.

## 9. Response letter references figures that exist?

**N/A.** No response/rebuttal file is included in `submission_bundle_20260419/`. Not required for an initial submission.

## 10. Bundle size reasonable for NC portal upload?

**PASS.** Core PDFs are small (`main.pdf` 264 K, `supplementary_main.pdf` 2.1 M, `cover_letter.pdf` 32 K). The total bundle is 104 M only because figure assets are duplicated across `manuscript/` and `supplementary/` folders. Per-file portal limits (~30 MB) are not exceeded.

---

## Summary

| # | Item | Verdict |
|---|---|---|
| 1 | Off-disk dependency | **FAIL** |
| 2 | Manuscript ↔ Zenodo cross-refs | **PASS** |
| 3 | Placeholders | **PASS** |
| 4 | Required files (K-T7) | **FAIL** |
| 5 | Locked numbers | **PASS** |
| 6 | Abstract ≤ 150 words | **PASS** |
| 7 | Unresolved citations | **PASS** (PDF) / **FAIL** (source) |
| 8 | Cover letter ready | **PASS** |
| 9 | Response letter | **N/A** |
| 10 | Bundle size | **PASS** |

## Final Verdict

**Not ready — see items above.**

**Must-fix before submission:**
1. Copy `main.bbl` and `supplementary_main.bbl` into the bundle (or inline references per NC guidelines).
2. Harmonise citation keys so `.tex` and `.bib` agree, then regenerate `.bbl` from a single `refs_gpt.bib`.

**Should-fix:**
3. Replace the `source_data_v1.zip` symlink with a physical copy.

After these fixes, the bundle will be **submission-ready pending user metadata** (ORCID, affiliation, email, suggested reviewers, acknowledgements).
