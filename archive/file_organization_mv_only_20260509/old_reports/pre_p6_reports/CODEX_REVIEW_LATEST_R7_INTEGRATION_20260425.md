# Codex Review — Latest Round-7 Integration State

**Date:** 2026-04-25 14:00 CST  
**Reviewer:** Codex  
**Scope:** Latest Kimi/Gemini/Claude broadcasts, canonical manuscript, supplementary notes, cover letter, and reproducibility note after Round-7 Phase 3/4 activity.

Validation performed:
- Read latest `AGENT_SYNC_gpt.md` and `AGENT_INTERCOM_HUB_20260423.md`.
- Recompiled `paper/latex_gpt/main.tex` with BibTeX and `paper/latex_gpt/supplementary_main.tex`.
- Grepped canonical `.tex` sources for stale internal-audit terminology and unresolved refs.
- Rechecked the previously reported Codex P0/P1 items in `S_mechanism_empirical.tex`.

Compile status:
- `main.tex`: RC 0 after BibTeX; no undefined refs remain.
- `supplementary_main.tex`: RC 0; layout warnings only.

## Findings

### P0-1: S-Mechanism factual/protocol blockers remain unfixed

**Files:**
- `paper/latex_gpt/supplementary/S_mechanism_empirical.tex:11`
- `paper/latex_gpt/supplementary/S_mechanism_empirical.tex:30`
- `paper/latex_gpt/supplementary/S_mechanism_empirical.tex:94`
- `paper/latex_gpt/supplementary/S_mechanism_empirical.tex:96`

The exact blockers Codex previously reported are still present in the canonical supplementary note:

1. E2 text still says the interpolation used `alpha in {0, 1, 3}`, while the final JSON used seven points: `0, 0.5, 1, 1.5, 2, 2.5, 3`.
2. E2 caption still says shaded regions are across five fresh masks; the final JSON says `masks = 3`.
3. E2 caption still describes accuracy as solid and loss as dashed, but the generated figure uses model-level line styles and loss markers/secondary axis.
4. E1 prose still says severe-NL eigenvalues are `(1,000--30,000x)`, but those are absolute Ritz eigenvalues unless a denominator is explicitly defined.
5. E1 limitation still says fixed eval batch `256`; final E1 JSON says `fixed_batch_size = 32`.
6. E1 limitation still says analog parameter counts exceed `10^5`; final E1 JSON says `param_count = 4,730,016`.

This remains a paper-visible factual mismatch. It must be corrected before Claude Phase-5 integration.

### P0-2: Internal audit terminology has re-entered canonical manuscript/cover-letter files

**Files:**
- `paper/latex_gpt/supplementary/S_mechanism_empirical.tex:7`
- `paper/latex_gpt/supplementary/S_mechanism_empirical.tex:100`
- `paper/latex_gpt/supplementary/S_mechanism_empirical.tex:105`
- `paper/latex_gpt/supplementary/S_reproducibility.tex:36`
- `paper/latex_gpt/supplementary.tex:774`
- `paper/latex_gpt/supplementary.tex:792`
- `paper/latex_gpt/supplementary.tex:798`
- `paper/latex_gpt/cover_letter.tex:30`
- `paper/latex_gpt/cover_letter.tex:40`

Canonical source now contains terms such as `post-fix`, `pre-fix`, `bug-immune`, `Zone 3B`, and `config-sharing bug`. Earlier Claude/Gemini closure doctrine had explicitly scrubbed these terms from canonical paper/cover-letter text. Their reintroduction is risky for a submission package because it exposes internal audit bookkeeping rather than scientific methodology.

Recommended rewrite policy:
- In paper/SI: use neutral scientific language such as `revised gradient-scaling recipe`, `historical diagnostic`, `verified evaluation-only protocol`, or `audited implementation`.
- Keep `bug`, `pre-fix`, `post-fix`, `Zone 3A/3B/3C`, and `bug-immune` in internal provenance reports only, unless the user explicitly chooses a transparent erratum-style cover letter.
- For cover letter specifically, avoid the full internal zone taxonomy. Editors need confidence, not the raw audit ledger.

### P1-1: Reproducibility cookbook has stale test paths after Claude cleanup

**File:** `paper/latex_gpt/supplementary/S_reproducibility.tex:39`, `:42`, `:45`

The note tells readers to run:

```bash
python test_dual_bug_fix.py
python test_groupwise_nl_wrapper.py
python test_adc_perinstance_calibration.py
```

But Claude's workspace cleanup moved tests to `tests/`, and `WORKSPACE_LAYOUT.md` now documents the correct invocation:

```bash
python tests/test_dual_bug_fix.py
python tests/test_groupwise_nl_wrapper.py
python tests/test_adc_perinstance_calibration.py
```

As written, a clean clone following the supplementary note will fail to find those files. This is a reproducibility blocker, not just prose polish.

### P1-2: Reproducibility note still uses placeholder clone URL and old checkpoint commit

**File:** `paper/latex_gpt/supplementary/S_reproducibility.tex:14`, `:16`

The note says:

```bash
git clone https://github.com/USERNAME/REPO_NAME.git
git checkout 33bed9c
```

This is not submission-ready. It should either use the real release/archive URL or an explicit anonymous-review placeholder that matches the submission package. Also verify whether `33bed9c` is still the intended canonical reproducibility commit after Claude's cleanup commits and later Round-7 manuscript/script additions.

### P2-1: Kimi comprehensive review is now stale after later fixes

**File:** `report_md/_gpt/KIMI_COMPREHENSIVE_REVIEW_20260425.md:66-75`, `:110-116`, `:123`

Kimi's report still says four undefined refs remain (`eq:hat-ensemble` and `subsec:methodology-nl`). The canonical manuscript has since fixed those refs, and the current compile has no undefined references. The report also says supplementary has zero warnings; current compile has only layout warnings, which is acceptable, but the statement is no longer exact.

This is not a manuscript blocker, but it can mislead coordination if Claude uses that report as current truth.

## Cleared Items

- The previously undefined references are now fixed in canonical manuscript:
  - `eq:hat-ensemble` -> `eq:hat-ensemble-distribution`
  - `subsec:methodology-nl` -> `subsec:modeling-nonidealities`
- `main.tex` and `supplementary_main.tex` both compile with RC 0.
- `06_discussion.tex` still uses the safe D2D-direction mechanism wording and does not overclaim global Hessian flatness.
- `05_results.tex` correctly keeps ADC-on as hook diagnostic rather than deployment-fidelity.

## Recommendation

Do not proceed to Claude Phase-5 final integration until P0-1 and P0-2 are patched. P1 reproducibility fixes should be handled in the same Kimi writing-polish pass because they are mechanical and low-risk.
