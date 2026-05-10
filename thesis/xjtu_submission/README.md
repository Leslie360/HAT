# XJTU Submission Lane — 2026-05-10

## Purpose

This directory is reserved for the formal Xi'an Jiaotong University thesis submission build.

It is intentionally separate from active thesis sources:

- CN active source: `../cn/`
- EN active source: `../en/`
- XJTU template asset: `../xjtu_template/`

Do not overwrite `../cn/` or `../en/` while migrating to the XJTU class.

## Current status

Planning lane only. No formal XJTU build has been generated here yet.

The template audit is recorded at:

`../../coordination/agent_reports/Claude/CC_XJTU_TEMPLATE_AUDIT_20260510.md`

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
