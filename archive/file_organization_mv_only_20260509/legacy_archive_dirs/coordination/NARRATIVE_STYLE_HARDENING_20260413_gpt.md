# Narrative Style Hardening Dispatch (2026-04-13)

## Accepted direction

Current manuscript revisions should move away from:
- reviewer-response phrasing
- AI-summary cadence
- explicit checklist / contribution-list narration
- over-explicit self-justification

and move toward:
- continuous prose
- literature-style motivation and transition
- restrained claim language
- result-first, implication-second scientific narration

## Reference style

Primary style anchor:
- `report_md/s41467-025-66891-6.pdf`

Secondary style rule:
- write like a published paper explaining what was found and why it matters,
  not like a model defending itself against anticipated criticism.

## Immediate Codex edits already completed

- `paper/latex_gpt/sections/00_abstract.tex`
- `paper/latex_gpt/sections/01_introduction.tex`
- `paper/latex_gpt/sections/02_related_work.tex`
- `paper/latex_gpt/sections/03_methodology.tex`
- `paper/latex_gpt/sections/04_experimental_setup.tex`
- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/sections/06_discussion.tex`
- `paper/latex_gpt/sections/07_conclusion.tex`
- `paper/latex_gpt/cover_letter.tex`

## Remaining style risks

1. Some figure captions and Results lead-ins still sound summary-like rather than paper-like.
2. A few methodology and discussion sentences still read as defensive disclaimers rather than integrated scientific prose.
3. Supplementary text may still retain more coordination/justification tone than the main text.

## Collaboration rule

- Kimi and Gemini should now review the manuscript specifically for narrative tone.
- Suggestions must be source-grounded and use `path:line`.
- Do not recommend new experiments in this pass.
- Do not propose changes that alter locked numbers or conclusions.
