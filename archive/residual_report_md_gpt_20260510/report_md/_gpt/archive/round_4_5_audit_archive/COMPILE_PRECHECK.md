# COMPILE_PRECHECK — Pre-Compilation Verification Checklist
**Date:** 2026-04-25
**Author:** Kimi (autonomous execution, Claude offline)
**Purpose:** Prevent compilation of stale, contaminated, or placeholder-incomplete files.
**Scope:** `compute_vit/paper/latex_gpt/` (Nature Electronics manuscript) + `compute_vit/paper/thesis/` (EN thesis chapters)

---

## Checklist (execute in order)

### Step 1 — Zone-3B contamination scan
```bash
cd compute_vit/paper/latex_gpt/sections
grep -riE "(30%|32%|ceiling.*27|post-?fix.*ceiling|software artifact)" *.tex \
  | grep -v "\.kimi_draft" | grep -v "\.bak"
```
**Gate:** Zero matches required. Any match = STOP, triage before compile.

### Step 2 — Placeholder scan
```bash
cd compute_vit/paper/latex_gpt/
grep -rnE "\[PENDING_|\[STAGE2_|\[MEASURED_|\[LITERATURE_CALIBRATED_" sections/*.tex cover_letter*.tex

cd compute_vit/paper/thesis/
grep -rnE "\[PENDING_|\[STAGE2_|\[MEASURED_|\[LITERATURE_CALIBRATED_" *.tex
```
**Gate:** Zero unresolved placeholders required.

### Step 3 — Canonical number lock verification (severe-NL M-series)
Verify the following numbers appear **exactly** in all tables and inline quotes:

| Task | ADC-on 8-bit (%) | Std (%) | ADC-off baseline (%) |
|:-----|:----------------:|:-------:|:--------------------:|
| M1   | 81.89            | 1.02    | 82.03                |
| M5   | 80.37            | 0.08    | 80.47                |
| M2   | 80.37            | 0.59    | 80.45                |
| M6   | 81.04            | 1.73    | 81.18                |
| M3   | 80.64            | 0.13    | 80.71                |
| M4   | 80.67            | 0.41    | 80.75                |

**Files to check:**
- `paper/latex_gpt/sections/05_results.tex`
- `paper/thesis/chapter_5_mitigation.tex`

**Gate:** All six rows must match. Any deviation = STOP, audit source JSON.

### Step 4 — Sidecar sync verification
```bash
cd compute_vit/paper/latex_gpt/sections
for f in 00_abstract 01_introduction 05_results 06_discussion 07_conclusion; do
  diff "${f}.tex" "${f}.tex.kimi_draft_v3" >/dev/null && echo "✅ $f synced" || echo "⚠️  $f DRIFT"
done
```
**Gate:** All critical sections synced. Drift = resolve before compile.

### Step 5 — Bib integrity
```bash
cd compute_vit/paper/latex_gpt
bibtex -terse main.aux 2>&1 | grep -i "error\|warning" || echo "✅ Bib clean"
```
**Gate:** No bib errors. Duplicate entries or missing fields = fix before compile.

### Step 6 — Compilation test
```bash
cd compute_vit/paper/latex_gpt
latexmk -pdf -interaction=nonstopmode main.tex
```
**Gate:** `main.pdf` generated. Warnings logged but do not block unless:
- Undefined citations (missing bib entry)
- Missing figure files (`./figures/*.pdf` or `./figures/*.png` not found)
- LaTeX fatal errors (package conflicts, math mode errors)

**Known non-blocking warnings (Round-5 Claude integration scope):**
- `Reference 'eq:hat-ensemble' undefined` — label missing in `03_methodology.tex`, to be added during Round-5 Ensemble HAT equation integration.
- `Reference 'subsec:methodology-nl' undefined` — label missing, to be added during Round-5.

---

## Post-Compile Verification

After `main.pdf` generates:

1. **Page count sanity:** Expected ~18–22 pages for full manuscript (current: 19).
2. **Table 1 visual check:** Open PDF, verify `tab:severe-nl-recovery` shows Stage-2 numbers (81.89, 80.37, 80.64, 80.67, 80.37, 81.04).
3. **Figure presence:** All `\includegraphics` calls resolve (no blank rectangles with filenames).
4. **Reference list completeness:** Bib entries for Wager 2013, Tobin 2017, Kirkpatrick 2017, Hochreiter 1997 present (KIMI-THEORY-1 citations).

---

## Automation

To run the full precheck in one command:

```bash
cd compute_vit
bash scripts/compile_precheck.sh   # (create this wrapper when convenient)
```

For now, manual execution of Steps 1–6 above is required before every compile intended for external eyes (advisor, collaborator, submission).

---

## History

| Date | Event |
|:-----|:------|
| 2026-04-25 | Created after Stage-2 emergency audit discovered false-negative compilation risk. |
| 2026-04-25 | First compile test passed: `main.pdf` 19 pages, 4 undefined refs (pre-existing, Round-5 scope). |
