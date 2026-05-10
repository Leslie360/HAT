# XJTU Thesis Template Audit — 2026-05-10

## Verdict

The active master thesis content is not currently using the XJTU thesis class.

- Active CN thesis: `thesis/cn/main.tex` uses `ctexbook`.
- Active EN thesis: `thesis/en/main.tex` uses `report`.
- XJTU template asset: `thesis/xjtu_template/XJTU-thesis.cls` exists and is a separate template package.

Do not overwrite `thesis/cn/` or `thesis/en/` during migration. Create a separate formal submission lane first.

## Template facts checked

| Item | Finding |
|---|---|
| Template entry | `thesis/xjtu_template/main.tex` |
| Class file | `thesis/xjtu_template/XJTU-thesis.cls` |
| Class version | `1.2.4`, dated 2021-07-16 |
| Required engine | XeTeX via `\RequireXeTeX` |
| TeXLive note | README says TeXLive >= 2023 |
| Degree options | `master`, `doctor`; also class supports `report`, `bachelor`, `slide` paths |
| Main option for this thesis | `master` |
| Blind-review option | `blind` |
| English-main option | `english` |
| Plagiarism-check option | `plgck` |
| Bibliography backend | `biblatex` with `backend=biber`, `style=gb7714-2015` |
| Reference source macro | `\addreferenceresource{References/reference}` without `.bib` suffix |
| Achievement source macro | `\addachivementresource{References/achievement}` |
| Body include pattern | `\thesisbodybegin`, `\include{Main_Spine/c1}` ... `c8`, `\thesisbodyend` |

## Important caution

The template README says the university released a newer thesis template in 2025 and this repository has not followed that update. Before final submission, compare against the current graduate-school Word/PDF requirements or official LaTeX requirement if available.

## Required metadata before formal migration

Do not invent these values.

- Chinese and English thesis title.
- Degree type and official English degree wording.
- Author name in Chinese and English.
- Advisor name/title in Chinese and English.
- School/department if required by current XJTU rule.
- Subject/major wording in Chinese and English.
- Submission date.
- Defense date/location if needed.
- Committee and reviewer lists if this version will be used beyond blind-review draft.
- Originality/confidentiality requirements.

## Safe migration lane

Recommended target:

- `thesis/xjtu_submission/`

Initial migration steps:

1. Copy the template skeleton structure into `thesis/xjtu_submission/`.
2. Keep `thesis/cn/` as the content source of truth until the XJTU build is stable.
3. Map CN chapters into `Main_Spine/c1` ... `c8` or equivalent files.
4. Move abstract/acknowledgement/glossary/appendix content into `Main_Miscellaneous/`.
5. Create `References/reference.bib` from the active thesis bibliography source.
6. Build with XeLaTeX + biber + XeLaTeX passes.
7. Compare generated PDF against university requirements before treating it as submission-ready.

## Risk notes

- The template is not guaranteed to match 2025+ XJTU rules.
- Active thesis figures and bibliography paths may need path normalization.
- `biblatex`/`biber` differs from simpler BibTeX flows; bibliography conversion must be checked.
- The class configures fonts for Linux via Fandol/XITS under TeXLive; missing local fonts can block compilation.

## Current recommendation

Use the XJTU template for a separate formal-submission build lane, not as a replacement for the current active CN/EN thesis directories.
