# Kimi P8 Track A: Narrative De-AI-Smell Rewrite

Date: 2026-05-09
Scope: Paper-1 manuscript and Supplementary Information narrative smoothing
Status: COMPLETE

## 1. Files touched

| File | Change type | Scientific values changed? |
|---|---|---|
| `paper/latex_gpt/sections/05_results.tex` | Existing P7/P8 narrative structure retained; inspected target `Iso-Accuracy Operating Envelope` | No |
| `paper/latex_gpt/sections/03_methodology.tex` | Confirmed overview sentence under Methodology | No |
| `paper/latex_gpt/sections/06_discussion.tex` | Added natural opening bridge under Discussion | No |
| `paper/latex_gpt/supplementary.tex` | Confirmed retention comparison paragraph already rewritten into cautious framing | No |
| `paper/latex_gpt/supplementary/S_mechanism_empirical.tex` | Rewrote S-M.2 and S-M.5 bridge text | No |

## 2. Before / after summary

| Location | Before | After |
|---|---|---|
| `sections/06_discussion.tex` | Discussion opened abruptly at subsection level | Added one paragraph explaining the sequence: avoid instance overfitting, then choose precision/drift/readout operating point |
| `supplementary.tex` uniform/state-dependent retention | Short declarative validation wording | Cautious framing: tests whether uniform retention changes the measured trajectory in this setting, not a global claim |
| `S_mechanism_empirical.tex` S-M.2 | Ranking diagnostic sentence read mechanically | Recast as a diagnostic for where mismatch perturbations remain visible after full-network transfer control |
| `S_mechanism_empirical.tex` S-M.5 | “confirms” wording sounded categorical | Recast as interpretation: Ensemble HAT is not ordinary checkpoint smoothing; mismatch-distribution exposure is the key ingredient |
| Main headers | Results/Methodology/Discussion had sufficient orientation after P7/P8 rewrites | Confirmed no extra unsupported overview sentence needed in Results/Methodology beyond existing text |

## 3. Verification

| Check | Result |
|---|---|
| LaTeX rebuild | PASS: `logs/p8_latex_rebuild_after_final_text_20260509_222917.log` |
| Main PDF | `main.pdf` up to date, 14 pages |
| Supplement PDF | `supplementary_main.pdf` rebuilt, 39 pages, 2,826,721 bytes |
| Cover letter | up to date |
| Stale value scan | PASS: no active hits for `68.55`, `0.07 pp`, stale `\notrun{}` 6-bit pattern, or stale `86.37±0.19` aggregate |
| Claim audit | PASS: no numerical, source-data, citation, figure-label, or Paper-1 claim changes were introduced by the final narrative edits |

## 4. Notes

The large `git diff` for manuscript files includes earlier P7/P8 accepted restructuring. The P8 Track A incremental edits are text-only narrative smoothing and preserve frozen values.

## 5. Verdict

Track A COMPLETE. Narrative flow is improved without altering locked Paper-1 scientific content.
