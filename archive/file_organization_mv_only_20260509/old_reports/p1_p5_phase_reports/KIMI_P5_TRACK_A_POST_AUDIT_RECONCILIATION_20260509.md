# Kimi P5 Track A Report: Post-Audit Scientific Drift Reconciliation

**Date:** 2026-05-09
**Dispatch:** `DISPATCH_SUPERPHASE_P5_POST_AUDIT_REMOTE_AND_EXPERIMENT_GOVERNANCE_20260509.md`
**Executor:** kimi
**Verdict:** NO SCIENTIFIC DRIFT DETECTED

---

## 1. Comparison Scope

Compared these paths for scientific-number divergences:
- `paper/latex_gpt/sections/` (working tree)
- `paper/latex_gpt/supplementary/` (working tree)
- `paper/latex_gpt/source_data/` (working tree)
- `release_artifacts/paper1_submission_bundle_20260509_final/` (final bundle)

---

## 2. Drift Values Check

### Table 5 (PCM Precision Ladder)

| Precision | Fresh | 1h | 24h | Delta Drift | Location |
|-----------|-------|-----|-----|-------------|----------|
| 8-bit PCM | 77.60% | 77.49% | 77.57% | 0.04 pp | Working tree + Bundle — MATCH |
| 6-bit PCM | 68.55% | 68.57% | 68.46% | 0.07 pp | Working tree + Bundle — MATCH |
| 4-bit PCM | 76.68% | 74.04% | 72.64% | 4.01 pp | Working tree + Bundle — MATCH |

**Drift definition:** Table caption explicitly states `Δ_{0→24h}` = retention-eval 0s accuracy minus 24h accuracy, not fresh-eval mean minus 24h. This matches the Codex-locked definition.

**No drift-value mutations found.** The Gemini post-audit mutation (Fresh - 24h) was already corrected by Codex in the working tree.

---

## 3. Old 6-Bit String Check

```bash
rg -n "77\.86|77\.88|77\.83|77\.76|78\.49|Pareto midpoint|seed456_full100" \
  paper/latex_gpt/ --type tex --type csv
```

**Result:** 0 hits in active `.tex` and `.csv` files.

Only hits are inside `paper/latex_gpt/source_data/canonical_json/deprecated_20260501_old_protocol/` (expected; deprecated data).

---

## 4. Obsolete Headline Strings

**86.37%** appears in:
- `paper/latex_gpt/deprecated/08_appendix.tex` — deprecated file, non-active
- `paper/latex_gpt/cover_letter_v3.tex` — old cover letter version, non-active
- `paper/latex_gpt/sections/03_methodology.tex:52` — **footnote** explaining thesis single-seed headline (86.37%) vs paper 3-seed mean (86.16%). Intentional contrast, not an active claim.
- `paper/latex_gpt/supplementary.tex:309` — single-seed breakdown table (seed123 = 86.37±1.54%), alongside seed456 and seed789. Data transparency, not headline claim.
- `paper/latex_gpt/supplementary.tex:826` — nonlinearity sweep table, canonical NL setting = 86.37. Specific experimental condition.
- `paper/latex_gpt/figures/tikz/figS3_ensemble_hat.tex:113` — TikZ figure annotation.

**Verdict:** 86.37% is retained as historical/single-seed data in supplementary and footnotes. Main-text headline remains 86.16±0.19%. No claim inflation.

---

## 5. Grep Commands Used

```bash
# Drift values
rg -n '0\.03 pp|0\.09 pp|4\.04 pp|0\.04 pp|0\.07 pp|4\.01 pp' \
  paper/latex_gpt/ release_artifacts/paper1_submission_bundle_20260509_final/

# Old 6-bit strings
rg -n "77\.86|77\.88|77\.83|77\.76|78\.49|Pareto midpoint|seed456_full100" \
  paper/latex_gpt/ --type tex --type csv

# Obsolete headlines
rg -n "86\.37|86\.36" paper/latex_gpt/ --type tex

# Drift definition
rg -n "Fresh - 24h|fresh-eval mean minus 24 h" paper/latex_gpt/ --type tex
```

---

## 6. Mismatches Found

| Mismatch | Severity | Action |
|----------|----------|--------|
| None | — | All working-tree values match canonical source data and final bundle |

---

## 7. Verdict

**NO POST-AUDIT SCIENTIFIC DRIFT.**

Working tree, source data, and final submission bundle agree on all locked scientific values. Delta Drift definition is correctly `retention-eval 0s - 24h`. No old-protocol strings in active files.

---

*Report by kimi. Reconciliation executed on 2026-05-09.*
