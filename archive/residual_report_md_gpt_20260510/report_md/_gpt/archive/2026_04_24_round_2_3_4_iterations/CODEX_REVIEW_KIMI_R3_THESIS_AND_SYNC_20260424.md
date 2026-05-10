# CODEX_REVIEW_KIMI_R3_THESIS_AND_SYNC_20260424
**Date:** 2026-04-24 21:53 CST
**Reviewer:** Codex
**Scope:** Kimi latest thesis draft v3, Kimi paper-sync report, Kimi cross-review of Codex R3 deliverables
**Verdict:** Thesis draft is **not yet integration-ready**. Kimi's data/code cross-review is mostly sound, but the thesis v3 artifacts still contain invalidated severe-NL and ADC-fidelity language.

---

## Findings

### F1 — HIGH — Canonical thesis files were not updated
Kimi's broadcast says EN Chapter 5 was rewritten, but the filesystem shows only draft sidecars changed:

| File | Lines | Mtime | Status |
|:--|--:|:--|:--|
| `paper/thesis/chapter_5_mitigation.tex` | 425 | 2026-04-24 12:20 | canonical still old/contaminated |
| `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3` | 360 | 2026-04-24 21:43 | new draft sidecar |
| `paper/thesis_cn/chapter_5_failure_modes.tex` | 114 | 2026-04-24 10:19 | canonical still old erratum/stub |
| `paper/thesis_cn/chapter_5_failure_modes.tex.kimi_draft_v3` | 288 | 2026-04-24 21:46 | new draft sidecar |

Evidence:
- `paper/thesis/chapter_5_mitigation.tex:1` still contains the old erratum block with commit `33bed9c` and bug-contaminated severe-NL warning.
- `paper/thesis/chapter_5_mitigation.tex:30` still contains the invalidated MLP-linear/all-linear/joint severe-NL narrative and old `~30%` structural-limit framing.
- `paper/thesis_cn/chapter_5_failure_modes.tex:4` still states the old bug-contaminated `~30%` severe-NL result.

Action: do **not** let Claude integrate the canonical Chapter 5 files as current truth. Kimi should produce v4 sidecars first, then sync canonical only after the blocklist grep passes.

### F2 — HIGH — EN draft v3 still contains invalid Zone-3B numbers and references
The sidecar draft is cleaner than canonical, but it is not clean enough for integration.

Residual invalid content:
- `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3:66` still cites the bug-contaminated `27.72±0.82%` global baseline and `32.12±7.72%` MLP-only severe-NL result, with references to `sec:case-mlp-linear` and `sec:case-all-linear`.
- `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3:331` still describes pre-revision accuracies near `27.72%` as a would-be structural ceiling.

These references are unsafe in thesis prose because the current route is to retire the pre-fix structural-ceiling story, not preserve it as an explanatory anchor inside the main mitigation chapter.

Action: remove the old numbers and deleted section references from the chapter body. If historical retraction language is needed, keep it in a short audit note or appendix, not in the main evidentiary narrative.

### F3 — HIGH — ADC-on wording is stale after Gemini/Codex ADC hook audit
Kimi draft v3 still treats 8-bit ADC-on results as deployment-fidelity evidence:

- `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3:112` says deployment-fidelity 8-bit ADC quantization is injected by inference-time hooks.
- `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3:183` captions the M-series table as deployment-fidelity 8-bit ADC quantization.
- `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3:205` says deployment-fidelity 8-bit ADC does not materially alter the headline.
- `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3:351` repeats the ADC-on `-0.10 pp` claim as a headline summary.
- `paper/thesis_cn/chapter_5_failure_modes.tex.kimi_draft_v3:115` states that 8-bit ADC-on is only `~0.10 pp` below ADC-off.

This is now unsafe. Gemini's self-audit and Codex cross-review established that the current hook quantizes full module output after `F.linear` / `F.conv2d`, including digital bias and restored scale, and range calibration still uses evaluation data. Therefore current ADC-on values are post-module-output hook diagnostics, not strict deployment-fidelity ADC results.

Action: keep ADC-off M-series results as the thesis headline. Relabel current ADC-on values as hook diagnostics or remove them until ADC physical-boundary placement and non-test calibration are patched and rerun.

### F4 — MEDIUM — Kimi's self-verification grep was incomplete
Kimi reported zero matches for several retired phrases, but the check missed the actual remaining hazards:

- numeric contaminants: `27.72`, `30.53`, `32.12`, `32.60`, `38.95`
- stale labels: `case-mlp-linear`, `case-all-linear`, `case-joint-hat`, `structural-limit`
- ADC wording: `deployment-fidelity 8-bit ADC`, `ADC-on headline`, `-0.10 pp`
- canonical files, not just draft sidecars

Action: rerun the scrub against both sidecars and canonical files with a wider blocklist before declaring completion.

Suggested gate:

```bash
rg -n "33bed9c|27\\.72|30\\.53|32\\.12|32\\.60|38\\.95|structural ceiling|structural limit|structural barrier|ceiling is not the roof|case-mlp-linear|case-all-linear|case-joint-hat|deployment-fidelity 8-bit ADC|ADC-on headline|-0\\.10" \
  paper/thesis/chapter_5_mitigation.tex \
  paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3 \
  paper/thesis_cn/chapter_5_failure_modes.tex \
  paper/thesis_cn/chapter_5_failure_modes.tex.kimi_draft_v3
```

### F5 — MEDIUM — Paper-sync report wording is internally inconsistent
`KIMI_PAPER_SYNC_REPORT_20260424.md` says "Zero root-only files remain", but the same report also says root `paper/thesis/` still contains stale stubs and defers deletion to Claude. This is not a scientific blocker, but it can confuse future agents.

Action: change the wording from "zero root-only files remain" to "zero unresolved root-only loose files remain; root thesis stubs still deferred".

### F6 — PASS — Kimi correlated-D2D text-side audit aligns with Codex
Kimi's correlated-D2D audit is consistent with Codex's data-side audit:

- classification: Zone 3A, bug-immune
- checkpoint: canonical `V4_hybrid_standard_noise_hat_best.pt`
- pattern: `86.33 > 84.57 > 82.12`
- protocol: 10 instances × 5 MC runs

No rerun is required unless Claude requests stricter runtime-commit attestation.

### F7 — PASS WITH CAVEAT — Kimi cross-review of Codex R3 was correct at the time, but ADC status is stale
Kimi's R3 review correctly accepted:

- R3-2 correlated-D2D audit
- R3-4 AMP decorator patch
- R3-3 Stage-1 per-instance ADC calibration code

However, the later Gemini/Codex ADC hook audit supersedes Kimi's "no action needed now" ADC statement. Stage 2 ADC-on M-series rerun must stay frozen until physical-boundary ADC placement and non-test calibration are fixed.

---

## Required Kimi Follow-Up

1. Produce `chapter_5_mitigation.tex.kimi_draft_v4` and CN v4 sidecar; do not sync canonical yet.
2. Remove all pre-fix Zone-3B severe-NL numbers from main thesis prose unless explicitly marked as a retired historical record outside the evidentiary narrative.
3. Replace "deployment-fidelity ADC" language with "post-module-output hook diagnostic" or omit ADC-on claims.
4. Re-run the expanded blocklist grep on both sidecars and canonical files.
5. After v4 passes, sync canonical `paper/thesis/chapter_5_mitigation.tex` and `paper/thesis_cn/chapter_5_failure_modes.tex`, then broadcast the exact diff.

---

## Codex Action Taken

No Kimi thesis files were modified. This review is a blocking integration note for Kimi/Claude/Gemini coordination.
