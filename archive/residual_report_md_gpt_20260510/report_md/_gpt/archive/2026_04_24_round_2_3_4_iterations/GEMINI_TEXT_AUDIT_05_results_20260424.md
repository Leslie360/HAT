# GEMINI TEXT AUDIT: 05_results.tex.kimi_draft_v2
**Date:** 2026-04-24
**Author:** Gemini (Auditor)
**Status:** 2 Issues Found

## Audit Findings

### 1. Extraneous Data Reference
**Text:** `(Supplementary Table~S16)`
**Issue:** The reference to `Supplementary Table~S16` is a leftover from the pre-fix regime (which compared MLP-only vs. all-linear ablations). According to Codex's `CX-AUDIT-1`, these ablation tables are contaminated unless rerun. The current draft cites them as evidence that the "fresh-instance transfer is similarly bounded", but these numbers are currently invalid and should not be cited.

### 2. Contradictory Logic
**Text:** `This falsifies the hypothesis that coupling severe-NL compensation with distributional resampling overcomes the severe-NL barrier.`
**Issue:** This paragraph still concludes that the ceiling *cannot* be overcome, directly contradicting the main post-fix headline introduced two paragraphs earlier ("post-fix retraining with verified code yields [CX-M1 pending]... suggesting the previously reported ~30% floor was a software artifact rather than a physical limit"). The paragraph testing "whether the ceiling is structural" is obsolete narrative architecture that should be completely deleted, not just patched.