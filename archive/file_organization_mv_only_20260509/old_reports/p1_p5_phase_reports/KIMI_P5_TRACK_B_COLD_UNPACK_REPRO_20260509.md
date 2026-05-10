# Kimi P5 Track B Report: Cold-Unpack Submission Reproducibility

**Date:** 2026-05-09
**Dispatch:** `DISPATCH_SUPERPHASE_P5_POST_AUDIT_REMOTE_AND_EXPERIMENT_GOVERNANCE_20260509.md`
**Executor:** kimi
**Verdict:** PASS

---

## 1. Unpack Path

```
outputs/p5_cold_unpack_20260509/
├── paper1_submission_bundle_20260509_final/
└── paper1_provenance_archive_20260509/
```

---

## 2. File Counts

| Archive | Files | Size |
|---------|-------|------|
| `paper1_submission_bundle_20260509_final.tar.gz` | 133 | 9.8 MiB |
| `paper1_provenance_archive_20260509.tar.gz` | 73 | 38 MiB |

---

## 3. SHA256 Verification

```bash
cd outputs/p5_cold_unpack_20260509/paper1_submission_bundle_20260509_final/
sha256sum -c SHA256SUMS.txt
```

**Result:** All OK

---

## 4. Build Results

| Document | Builder | Result | Size |
|----------|---------|--------|------|
| `main.tex` | tectonic | SUCCESS | 202.97 KiB |
| `supplementary_main.tex` | latexmk | SUCCESS | 2.71 MiB |
| `cover_letter.tex` | tectonic | SUCCESS | 20.53 KiB |

---

## 5. Guard Results on Rebuilt PDFs

### Stale Scans
```bash
pdftotext main.pdf - | rg -n "77\.86|seed456_full100|Pareto midpoint|78\.49|\?\?"
pdftotext supplementary_main.pdf - | rg -n "77\.86|seed456_full100|Pareto midpoint|78\.49|\?\?"
```
**Result:** ZERO HITS

### Undefined Citations/References in Final Logs
```bash
grep -c 'Citation .* undefined' supplementary_main.log  # 0
grep -c 'Reference .* undefined' supplementary_main.log  # 0
grep -c 'Citation .* undefined' main.log                  # 0
grep -c 'Reference .* undefined' main.log                  # 0
```

---

## 6. Build Residue Check

Original submission bundle after cold build:
```bash
cd release_artifacts/paper1_submission_bundle_20260509_final/
find . -type f \( -name '*.aux' -o -name '*.log' -o -name '*.out' \) | wc -l
```
**Result:** 0

No build residue contaminated the original bundle.

---

## 7. Provenance Archive Check

`PROVENANCE_README.md` in the unpacked archive states:
> "Do not cite paths in this archive as active Paper-1 claims."

Clear separation from active claims.

---

## 8. Warnings

| Warning | Count | Classification |
|---------|-------|----------------|
| algorithm.sty UTF-8 | 6 | Cosmetic (known tectonic issue) |
| Tectonic bbl consistency | 5 | Cosmetic (bibtex rerun loop) |
| Underfull hbox | 3 | Cosmetic (layout) |

**No blocking warnings.**

---

## 9. Verdict

**PASS.**

The tarball unpacks cleanly, SHA256s verify, all three PDFs rebuild successfully, stale scans are zero, final logs have zero undefined citations/references, and the original bundle remains uncontaminated.

---

*Report by kimi. Cold-unpack test executed on 2026-05-09.*
