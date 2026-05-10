# Kimi P8 Track B: Appendix Text and Table Consistency

Date: 2026-05-09
Scope: `paper/latex_gpt/supplementary.tex` and `paper/latex_gpt/supplementary/*.tex`
Status: COMPLETE

## 1. Checks performed

| Requirement | Result | Evidence |
|---|---|---|
| B1: table font commands after global `\small` replacement | PASS | `\small` occurs only in table contexts or compact provenance tables; no global runaway found |
| B2: table width/readability | PASS with warnings | Final LaTeX log has only underfull hbox warnings, no overfull hbox warnings: `logs/p8_latex_rebuild_after_final_text_20260509_222917.log` |
| B3: captions stale wording / units / percent-vs-decimal | PASS | Captions explicitly state `%`, `pp`, MC, source/test/fresh meanings where needed |
| B4: abbreviation first-use | PASS with caveat | HAT, C2C, D2D, STE are defined in main/SI; MC is defined in table captions/protocol text; KV/PPL are Work-2 terms and not routed into Paper-1 claims |
| B5: blank cells | PASS | The only `& & &` pattern is `S_opect_distribution.tex:24-25`, a continuation row under the Evidence column, not unexplained missing data |
| B6: figure aesthetics untouched | PASS | No figure aesthetic edits performed by this track |

## 2. Table-font inventory

Observed `\small` commands:

- `supplementary.tex:62`, `107`, `271`, `325`, `370`, `621`, `712`, `729`, `799`, `821`, `951`
- `supplementary/S_energy_provenance.tex:12`
- `supplementary/S_opect_distribution.tex:18`

These are local table sizing commands. Final compile reports no overfull table warnings.

## 3. Caption/wording observations

| Location | Status | Note |
|---|---|---|
| `supplementary.tex` result-summary caption | PASS | `\notrun{}` is explicitly defined as “protocol not evaluated, not failed run” |
| `supplementary.tex` PCM captions | PASS | 8/6/4-bit rows state mean/fresh/drop and corrected 6-bit protocol |
| `supplementary.tex` retention comparison | PASS | P8 wording now avoids overgeneralizing state-dependent retention |
| `S_opect_distribution.tex` provenance table | PASS | Blank-looking rows are continuation rows for the D2D evidence explanation |
| `S_mechanism_empirical.tex` E4/E5 captions | PASS | Wording is diagnostic/cautious rather than mechanistic overclaim |

## 4. Remaining visual lane items

No text/table blocker remains. Gemini/user visual lane may still inspect appendix figure aesthetics, legend density, and page balance, but that is outside this track.

## 5. Verdict

Track B COMPLETE. Appendix tables and captions are internally consistent, compile without overfull table warnings, and do not alter scientific values.
