# XJTU Submission Migration Report — 2026-05-10

## Evidence grade

- `preview/provisional`: this is a formal-template preview lane, not an official submission build.
- Active sources under `thesis/cn/` and `thesis/en/` were not overwritten.

## What changed

- Created XJTU class preview build under `thesis/xjtu_submission/`.
- Copied required `XJTU-thesis.cls`, `latexmkrc`, and XJTU visual identity PDFs into the submission lane.
- Copied active CN chapters into `Main_Spine/c1.tex` ... `c8.tex`.
- Converted citation commands in copied chapter files from natbib-style `\citep`/`\citet` to biblatex-style `\parencite`/`\textcite`.
- Copied active bibliography to `References/reference.bib` for biber.
- Generated abstract, keywords, acknowledgements, glossary, appendix placeholders, and migration notes.

## Compile validation

Command:

```bash
latexmk -cd -xelatex -interaction=nonstopmode -halt-on-error -outdir=Build thesis/xjtu_submission/main.tex
```

Logs:

- `logs/xjtu_submission_compile_20260510_162811_20260510.log`
- `logs/xjtu_submission_compile_clean_20260510_162904_20260510.log`

Output:

- `thesis/xjtu_submission/Build/main.pdf`
- Build size observed: 937,969 bytes.
- Page count observed in compile log: 98 pages.

## Important caveats

- Advisor, advisor title, reviewer, defense, degree wording, and final date metadata remain placeholders.
- The template is version 1.2.4 from 2021 and must be checked against XJTU 2025+ official requirements before final submission.
- The generated PDF is a preview only; do not treat it as the official degree thesis until metadata and university-format review are complete.
- Build artifacts under `thesis/xjtu_submission/Build/` are local outputs and should normally stay untracked unless a release PDF is explicitly requested.

## Next recommended actions

1. Confirm formal metadata in `thesis/xjtu_submission/METADATA_TODO_20260510.md`.
2. Compare the 98-page preview against current XJTU graduate-school rules.
3. Replace placeholder committee/reviewer pages or enable blind-review mode depending on submission use.
4. Decide whether to track a generated preview PDF or keep only sources tracked.
