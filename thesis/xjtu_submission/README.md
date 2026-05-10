# XJTU Submission Lane — 2026-05-10

## Purpose

This directory is reserved for the formal Xi'an Jiaotong University thesis submission build.

It is intentionally separate from active thesis sources:

- CN active source: `../cn/`
- EN active source: `../en/`
- XJTU template asset: `../xjtu_template/`

Do not overwrite `../cn/` or `../en/` while migrating to the XJTU class.

## Current status

The XJTU template conversion has been generated and compile-validated. The build is structurally complete, but it remains a pre-submission draft until official metadata and university-format review are finalized.

Current build artifacts:

- Source entry: `main.tex`
- Chapter spine: `Main_Spine/c1.tex` ... `Main_Spine/c8.tex`
- Front/back matter: `Main_Miscellaneous/`
- Bibliography: `References/reference.bib`
- Local preview PDF: `Build/main.pdf`

The template audit is recorded at:

`../../coordination/agent_reports/Claude/CC_XJTU_TEMPLATE_AUDIT_20260510.md`

The migration report is recorded at:

`../../coordination/agent_reports/Claude/CC_XJTU_SUBMISSION_MIGRATION_REPORT_20260510.md`

## Blocked metadata

These values must come from the user/university before a submission-ready build:

- Chinese and English final title.
- Degree type and official English degree wording.
- Author name in Chinese and English.
- Advisor name/title in Chinese and English.
- School/department.
- Subject/major wording in Chinese and English.
- Submission date.
- Defense date/location, committee, and reviewer lists if required.
- Originality/confidentiality declaration requirements.

## Migration checklist

- [x] Copy XJTU template class/assets into this lane.
- [x] Create `main.tex` for the XJTU class.
- [x] Map current CN chapters into `Main_Spine/c1.tex` ... `c8.tex`.
- [x] Convert copied chapter citations to the biber/biblatex flow used by the template.
- [x] Copy active bibliography into `References/reference.bib`.
- [x] Generate abstract, acknowledgement, glossary, appendix, and achievement stubs.
- [x] Compile a XeLaTeX draft PDF under `Build/main.pdf`.
- [ ] Replace placeholder metadata with confirmed values.
- [ ] Compare against current XJTU 2025+ graduate-school requirements.
- [ ] Decide blind-review vs normal committee/reviewer pages.
- [ ] Decide whether a generated PDF should be tracked for a release bundle.

## Migration plan

1. Copy the XJTU template skeleton from `../xjtu_template/`.
2. Replace placeholder metadata with confirmed values only.
3. Map current CN chapters from `../cn/chapter_*.tex` into the template spine.
4. Move abstract/front matter/acknowledgement/glossary content into the template's miscellaneous files.
5. Convert or link bibliography into `References/reference.bib`.
6. Build with XeLaTeX + biber flow.
7. Compare the generated PDF against current XJTU 2025+ requirements before treating it as submission-ready.

## Safety rule

No generated PDF in this directory should be treated as official unless the metadata and university-format check are complete.
