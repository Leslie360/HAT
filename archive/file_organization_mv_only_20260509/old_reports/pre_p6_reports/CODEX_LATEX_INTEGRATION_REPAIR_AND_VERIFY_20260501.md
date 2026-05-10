# Codex LaTeX Integration Repair And Verify — 2026-05-01

## Verdict

PASS after direct repair.

Gemini's later LaTeX rewrite had already fixed most of the 2026-05-01 narrative blockers. Codex found and repaired the remaining main-text drift points: the Discussion still used the old severe-NL/MLP localization framing as an active main-text narrative, and the Conclusion/Abstract used stronger-than-supported causal wording for PCM UnitCell convergence.

## Files Changed By Codex

- `paper/latex_gpt/sections/00_abstract.tex`
- `paper/latex_gpt/sections/06_discussion.tex`
- `paper/latex_gpt/sections/07_conclusion.tex`
- `paper/latex_gpt/supplementary.tex`

## Repairs Applied

1. Reframed the Abstract from causal PCM wording to tested-regime wording:
   - before: implicit noise/update characteristics enable convergence;
   - after: under the tested PCM UnitCell, models converge across 4/6/8-bit, with precision-dependent retention.

2. Reframed Discussion mechanism paragraph:
   - earlier MLP severe-NL sensitivity is retained as supplementary diagnostic context only;
   - it is not used as a main-text localization claim under the revised precision-ladder narrative.

3. Rewrote Discussion AIHWKit/PCM paragraph:
   - 8-bit IdealDevice robustness and 4-bit collapse remain;
   - Ensemble HAT 4-bit rescue remains;
   - PCM UnitCell becomes a precision-retention deployment frontier, with 6-bit as best tested Pareto midpoint.

4. Rewrote Discussion Outlook:
   - measured-array calibration;
   - cross-architecture validation before main-text promotion;
   - analog KV-cache as separate Work-2 with parity checks and held-out PPL.

5. Rewrote Conclusion:
   - removed strong causal phrasing;
   - kept the locked paper-1 spine: pure 4-bit failure, Ensemble HAT rescue, PCM 4/6/8 precision ladder, 6-bit Pareto midpoint.

6. Removed stale supplementary PCM 8-bit `61.10%` row and compressed the table layout to remove the final overfull warning.

## Verification

Commands run:

```bash
python scripts/_gpt/check_locked_numbers.py
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex
rg -n "undefined references|undefined citations|Reference .* undefined|Citation .* undefined|Label .* multiply defined|! LaTeX Error|Emergency stop|Fatal error|Overfull" paper/latex_gpt/main.log paper/latex_gpt/supplementary_main.log
rg -n "61\\.10|26~?pp|optimal tradeoff|physical tape-out|inherent to PCM-preset|universally better|outperforms digital|tape-out ready|solves the memory wall|proves cross-architecture|main-text severe-NL|natural(ly)? support|fundamental precision-retention|maximum compression|only path" paper/latex_gpt/sections paper/latex_gpt/supplementary.tex paper/latex_gpt/supplementary -g '*.tex'
```

Results:

- Locked-number guard: `22/22 passed`.
- `main.pdf`: compiled, 13 pages.
- `supplementary_main.pdf`: compiled, 41 pages.
- Log grep: no undefined refs/citations, no fatal errors, no overfull warnings.
- Sensitive stale-claim grep: no hits.

## Remaining Boundary

Old OPECT/front-end/severe-NL analyses still exist in the Supplementary Information as historical/supporting diagnostics. This is acceptable only because the main text no longer treats them as the central contribution or current deployment route.
