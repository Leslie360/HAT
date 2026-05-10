# CODEX Preflight V2 — 2026-04-20

Triggered after Round M housekeeping landings (Data/Code Availability wording, thesis/rebuttal docs, heavy-tailed stub).

## Results

| Check | Status | Note |
|:--|:--:|:--|
| main pdf opens | PASS | pages=18 |
| supp pdf opens | PASS | pages=23 |
| cover pdf opens | PASS | pages=2 |
| bundle path manuscript/main.pdf | PASS | exists |
| bundle path manuscript/main.tex | PASS | exists |
| bundle path manuscript/sections/07_conclusion.tex | PASS | exists |
| bundle path supplementary/supplementary_main.pdf | PASS | exists |
| bundle path supplementary/supplementary.tex | PASS | exists |
| bundle path cover_letter/cover_letter.pdf | PASS | exists |
| bundle path source_data/source_data_v1.zip | PASS | exists |
| main.log warning scan | PASS | none |
| supplementary_main.log warning scan | PASS | none |
| source_data_v1.zip extracts + contains README/MANIFEST | PASS | entries=77 |
| source_data_v1.zip contains correlated-D2D JSON | PASS | present |

## Summary

- Overall: **PASS**
- Current PDF counts: main 17, supplementary 23, cover 2.
- Remaining submission blocker is still user metadata, not bundle integrity.
