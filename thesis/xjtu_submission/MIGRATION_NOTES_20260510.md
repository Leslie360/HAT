# XJTU Submission Migration Notes — 2026-05-10

## Scope

This lane is a preview migration from `../cn/` into the XJTU class. It does not replace `../cn/` or `../en/`.

## What was migrated

- XJTU class and `latexmkrc` copied from `../xjtu_template/`.
- Required XJTU visual identity PDFs copied under `Materials/VI/`.
- CN chapters copied into `Main_Spine/c1.tex` ... `c8.tex`.
- Active bibliography copied into `References/reference.bib` for biblatex/biber.
- Abstract, keywords, acknowledgements, glossary and appendices prepared under `Main_Miscellaneous/`.

## Placeholder metadata

Advisor, advisor title, defense/reviewer metadata, final degree wording, and 2025+ XJTU compliance still require user/university confirmation.

## Compile target

Run from this directory:

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=Build main.tex
biber Build/main
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=Build main.tex
```

Treat any generated PDF as a preview only.
