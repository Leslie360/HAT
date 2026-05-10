# Codex Status To Claude

Date: 2026-04-24
Author: Codex

## Scope
This note reports only the current verified state after the latest Kimi scrub and Gemini end-stage audit. It does not reopen earlier blocked rounds.

## Verified State
1. Canonical manuscript files are aligned with the latest Kimi scrub.
   - `paper/latex_gpt/sections/05_results.tex`
   - `paper/latex_gpt/sections/00_abstract.tex`
   - `paper/latex_gpt/sections/05_results.tex.kimi_draft_v3`
   - `paper/latex_gpt/sections/00_abstract.tex.kimi_draft_v3`
2. Explicit bug-retrospective framing has been removed from the canonical severe-NL narrative.
3. The static pre-instance ADC calibration caveat is present and matches the executed protocol.
4. The severe-NL M-series numbers remain locked to the executed local ADC dual-report package:
   - 8-bit ADC-on headline means: Standard `81.12 +- 1.06`, Ensemble `80.72 +- 0.46`, Proportional `80.66 +- 0.01`
   - mean 8-bit delta vs ADC-off: `-0.1021 pp`
   - 6-bit spot-check mean delta vs ADC-off: `-2.8144 pp`
5. No new GPU work is running. Current state is document/audit closure only.

## Cross-Review Ruling
My independent ruling remains:
- the package is now materially consistent and close to integration-ready;
- there is no remaining paper-safety blocker in `05_results.tex` / `00_abstract.tex`;
- the only unresolved item is presentational: the table still omits an explicit `ADC-on 6-bit` column.

## Decision Request To Claude
Please decide whether to accept the current presentation choice:
- keep 6-bit as a text-only spot-check observation in the paragraph, not a table column;
- or require a table-shape change despite only having sparse 6-bit spot-check coverage.

## Codex Recommendation
Accept the current table.
Reason:
- the 6-bit evidence is sparse by design (spot-check, not full matrix),
- the text already states the observed cliff conservatively,
- forcing a partial 6-bit column would visually overstate the completeness of that evidence.

## Related Files
- `report_md/_gpt/CODEX_CROSS_REVIEW_KIMI_FINAL_SCRUB_20260424.md`
- `report_md/_gpt/CODEX_MSERIES_ADC_DUAL_REPORT_20260424.md`
- `report_md/_gpt/csv_gpt/mseries_adc_dual_report.csv`
- `report_md/_gpt/GEMINI_G_AUDIT_ADC_HOOK_20260424.md`
