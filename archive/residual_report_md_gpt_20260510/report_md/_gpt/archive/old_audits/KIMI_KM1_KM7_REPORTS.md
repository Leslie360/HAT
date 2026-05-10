<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# Kimi KM1-KM7 Reports (2026-04-11)

---

## [Kimi] 2026-04-11 KM1 — Full Proofreading Pass

### Status
- 完成

### Findings
**00_abstract.tex:** No LaTeX errors, no ?? references, no spelling errors. Terminology consistent.

**01_introduction.tex:** One long sentence in para 5 (~52 words) — acceptable. Hardcoded "Section~6" should ideally be \ref.

**07_conclusion.tex:** All numbers match locked values. No overclaiming.

### Recommended Fixes
1. [LOW] Consider replacing hardcoded "Section~6" in 01_introduction.tex with \ref.

---

## [Kimi] 2026-04-11 KM2 — Abstract Number Check

### Status
- 完成

### Findings
All abstract numbers match Locked Numbers:
- Ensemble HAT: 86.37 ± 1.54% ✓
- Zhang 2026 OPECT: 88.53% ✓
- Proportional-noise HAT: 97.37 ± 0.05% ✓
- Nonlinear write NL=2: 27.72 ± 0.82% ✓
- Fresh-instance collapse: 10.00% ✓
- Energy qualifier: "first-order, upper-bound-like estimate" ✓

### Recommended Fixes
- None required.

---

## [Kimi] 2026-04-11 KM3 — Conclusion vs Results Consistency

### Status
- 完成

### Findings
All 8 major claims in conclusion verified against results:
1. Regime-dependent impact ✓
2. Quantization not dominant under canonical model ✓
3. Ensemble HAT 10.00% → 86.37±1.54% ✓
4. Proportional-noise recovery 97.37±0.05% ✓
5. Nonlinear write stuck at 27.72±0.82% ✓
6. Flowers-102 failure case ✓
7. Zhang 2026 OPECT 88.53% ✓
8. Energy qualifier present ✓

No overclaims. No important results omitted.

---

## [Kimi] 2026-04-11 KM4 — Reference Bib File Audit

### Status
- 完成

### Findings
- 47 entries total
- No "and others" placeholders
- No TODO/FIXME
- All entries have year and journal/booktitle

**FIXED: Malformed li2023ivit entry** — removed orphaned duplicate lines causing BibTeX errors.

### Recommended Fixes
1. [COMPLETED] Fixed li2023ivit trailing corruption.
2. [LOW] Rename riam2025sneakpath to riam2013sneakpath (year mismatch).

---

## [Kimi] 2026-04-11 KM5 — Supplementary Cross-Reference Review

### Status
- 完成

### Findings
**Verified matches:**
- Supplementary Section~\ref{sec:supplementary} ✓
- \ref{subsec:parameter-provenance} ✓
- \ref{subsec:retention-drift} → tab:retention-comparison ✓

**CRITICAL: Missing figure definitions:**
- Supplementary Fig.~S1 (ADC sweep) — NOT defined
- Supplementary Fig.~S2 (Task 12) — NOT defined
- Supplementary Fig.~S3 (attention maps) — NOT defined

### Recommended Fixes
1. [HIGH] Add figure environments for S1, S2, S3 in supplementary.tex OR remove references from 05_results.tex.

---

## [Kimi] 2026-04-11 KM6 — Related Work + Methodology Proofreading

### Status
- 完成

### Findings
**02_related_work.tex:** Clean. All 16 citations resolve. Minor: "our contribution focuses" is forward-looking for Related Work.

**03_methodology.tex:** Clean. All citations resolve. Terminology consistent.

### Recommended Fixes
1. [LOW] Change "our contribution focuses" to "this work focuses" in Sec 2.2.

---

## [Kimi] 2026-04-11 KM7 — Figure Citation Continuity Audit

### Status
- 完成

### Findings
**Order issues:**
- Fig 3 defined in Sec 5.5, but Figs 4-5 in Sec 5.2 — Fig 3 will be numbered AFTER Fig 4/5 in PDF.

**Missing figures:**
- Fig 9 (noise_sensitivity) — NOT defined
- Fig 10 (zero_shot_transfer) — NOT defined
- Fig 12 / attention maps — NOT defined (may be Supplementary S3)

### Recommended Fixes
1. [HIGH] Move fig:snr-curves to before Fig 4, or renumber figures.
2. [HIGH] Add figure environments for Fig 9, 10 if image files exist.
3. [HIGH] Confirm attention maps figure status (Supplementary S3?).

---

## Summary of Critical Issues Found

| Issue | Severity | Location | Recommended Action |
|-------|----------|----------|-------------------|
| Missing Supp Fig S1, S2, S3 definitions | HIGH | supplementary.tex / 05_results.tex | Add figure envs OR remove refs |
| Fig 3 order violation | MED | 05_results.tex Sec 5.5 | Move Fig 3 before Fig 4 OR renumber |
| Missing Fig 9, 10 definitions | HIGH | 05_results.tex | Add figure envs if images exist |
| li2023ivit bib corruption | **FIXED** | refs_gpt.bib | Kimi fixed |

---

Report generated: 2026-04-11
Kimi (Proofreading Agent)
