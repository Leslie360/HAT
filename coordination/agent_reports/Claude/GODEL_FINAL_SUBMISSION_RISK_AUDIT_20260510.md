# Final Submission Risk Audit - 2026-05-10

Scope: active `paper1/release/paper1_submission_bundle_20260509_final`, `thesis/cn`, and `thesis/en` only. Excluded `archive/`, `provenance/`, and `remote_reviews/` from active findings. No experiments, commits, or pushes were run.

## Blocking Findings

| Severity | File:line | Finding | Suggested action |
|---|---:|---|---|
| HIGH | `thesis/cn/main.tex:70` | CN thesis author metadata is still `[作者姓名]`. | Replace with final legal/department-approved author string before submission. |
| HIGH | `thesis/cn/main.tex:71` | CN thesis date metadata is still `[日期]`. | Replace with final defense/submission date. |
| HIGH | `thesis/cn/main.tex:84` | CN title page still has `[学位论文类型]`. | Fill final degree/thesis type. |
| HIGH | `thesis/cn/main.tex:86` | CN title page still has `作者：[作者姓名]`. | Fill final author. |
| HIGH | `thesis/cn/main.tex:88` | CN title page still has `导师：[导师姓名] 教授`. | Fill final advisor name/title. |
| HIGH | `thesis/cn/main.tex:90` | CN title page still has `[学院名称]`. | Fill final school/college. |
| HIGH | `thesis/cn/main.tex:92` | CN title page still has `[大学名称]`. | Fill final university name. |
| HIGH | `thesis/cn/main.tex:94` | CN title page still has `[日期]`. | Fill final date. |
| HIGH | `thesis/cn/front_matter.tex:89` | CN acknowledgements still have `[基金名称]` and `[编号]`. | Fill funding info or remove funding sentence if not applicable. |
| HIGH | `thesis/cn/front_matter.tex:91` | CN acknowledgements still have `[导师姓名]`. | Fill advisor name. |
| HIGH | `thesis/cn/front_matter.tex:93` | CN acknowledgements still have `[合作机构/实验室名称]`. | Fill or delete if not applicable. |
| HIGH | `thesis/cn/front_matter.tex:99` | CN closing signature still has `[作者姓名]`. | Fill final author. |
| HIGH | `thesis/cn/front_matter.tex:100` | CN closing date still has `[日期]`. | Fill final date. |
| HIGH | `thesis/en/main.tex:55` | EN title metadata is still `[THESIS TITLE]`. | Replace with final English thesis title. |
| HIGH | `thesis/en/main.tex:57` | EN date metadata is still `[Date]`. | Replace with final date. |
| HIGH | `thesis/en/main.tex:68` | EN title page still has `[THESIS TITLE]`. | Replace with final English thesis title. |
| HIGH | `thesis/en/main.tex:75` | EN title page still has `[Degree]`. | Fill final degree. |
| HIGH | `thesis/en/main.tex:77` | EN title page still has `[Department]` and `[University]`. | Fill final department/university. |
| HIGH | `thesis/en/main.tex:79` | EN title page still has `[Date]`. | Fill final date. |
| HIGH | `thesis/en/main.tex:87` | EN abstract body is still `[Abstract text goes here.]`. | Replace with final abstract or wire in final `abstract.tex`. |
| HIGH | `thesis/en/acknowledgements.tex:27` | EN acknowledgements still have `[Advisor Name]`. | Fill final advisor name. |
| HIGH | `thesis/en/acknowledgements.tex:30` | EN acknowledgements still have repeated `[Collaborator Name]`. | Fill names or remove placeholders. |
| HIGH | `thesis/en/acknowledgements.tex:32` | EN acknowledgements still have `[Institution]`. | Fill institution or remove clause. |
| HIGH | `thesis/en/acknowledgements.tex:34` | EN funding placeholders remain: `[Funding Agency 1]`, `[Grant Number]`, `[Funding Agency 2]`, `[Fellowship Name]`. | Fill funding details or delete sentence. |
| HIGH | `thesis/en/acknowledgements.tex:44` | EN declaration still has `[Thesis Title]`, `[Advisor Name]`, `[Institution Name]`. | Fill all declaration metadata before final submission. |

## Build Log Findings

| Severity | File:line | Finding | Suggested action |
|---|---:|---|---|
| PASS | `thesis/cn/main.log` | Latest CN log has 0 LaTeX errors, 0 undefined references, 0 undefined citations, and 0 rerun warnings in the scanned patterns. | No citation/ref blocker found. |
| PASS | `thesis/en/main.log` | Latest EN log has 0 LaTeX errors, 0 undefined references, 0 undefined citations, and 0 rerun warnings in the scanned patterns. | No citation/ref blocker found. |
| MED | `thesis/cn/main.log:1187` | Severe overfull hbox: `109.92384pt too wide`, paragraph at source lines 71--76, caused by long JSON filenames in `thesis/cn/chapter_1_introduction.tex:75`. | Break filenames with `\path{}`/`\url{}` or move provenance filenames to footnote/table. |
| MED | `thesis/cn/main.log:1321` | Severe overfull hbox: `104.42639pt too wide`, paragraph at source lines 124--126 in `thesis/cn/chapter_7_deployment.tex`, caused by long JSON filenames. | Wrap filenames or shorten provenance wording. |
| MED | `thesis/cn/main.log:1355` | Severe overfull hbox: `101.82005pt too wide`, table at source lines 295--308 in `thesis/cn/chapter_7_deployment.tex`. | Resize/reformat table, reduce columns, or use `tabularx`/landscape. |
| MED | `thesis/en/main.log:972` | Severe overfull hbox: `144.13898pt too wide`, paragraph/table at source lines 58--67 while compiling Chapter 4. | Inspect Chapter 4 table/paragraph and reflow before final PDF. |
| MED | `thesis/en/main.log:1096` | Severe overfull hbox: `124.28082pt too wide`, source lines 59--69 in `thesis/en/chapter_7_deployment.tex`. | Reformat the table/long math row in that range. |
| LOW | `thesis/cn/main.log:202` | Fontspec warning: FandolSong lacks requested CJK script. | Usually non-blocking if PDF renders; verify visual output. |
| LOW | `thesis/cn/main.log:1167` | Fontspec warning: FandolFang lacks requested CJK script. | Usually non-blocking if PDF renders; verify visual output. |

## Paper1 Release Framing

| Severity | File:line | Finding | Suggested action |
|---|---:|---|---|
| PASS | `paper1/release/paper1_submission_bundle_20260509_final/sections/00_abstract.tex:3` | Main abstract uses current `86.16%` framing and separates idealized algorithmic result from PCM deployment claim. | No action. |
| PASS | `paper1/release/paper1_submission_bundle_20260509_final/sections/01_introduction.tex:9` | Introduction uses `86.16\pm0.19%` and current PCM precision ladder values. | No action. |
| PASS | `paper1/release/paper1_submission_bundle_20260509_final/sections/03_methodology.tex:54` | Methodology explicitly says the main claim uses the 3-seed mean `86.16 ± 0.19%`; single-checkpoint diagnostics are provenance only. | No action. |
| PASS | `paper1/release/paper1_submission_bundle_20260509_final/sections/05_results.tex:22` | Results table uses `86.16 ± 0.19%`. | No action. |
| PASS | `paper1/release/paper1_submission_bundle_20260509_final/sections/07_conclusion.tex:7` | Conclusion uses `86.16\pm0.19%`. | No action. |
| PASS | `paper1/release/paper1_submission_bundle_20260509_final/RELEASE_README.md:26` | Release README canonical table is focused on PCM ladder and does not assert stale `86.37±1.54` as the headline. | No action. |
| PASS | `paper1/release/paper1_submission_bundle_20260509_final/source_data/canonical_json/README.md:9` | Source-data README describes the Ensemble HAT artifact as the 4-bit three-seed fresh-instance result. | No action. |
| LOW | `paper1/release/paper1_submission_bundle_20260509_final/source_data/canonical_json/ensemble_hat_4bit_3seed/r10a_canonical_ensemble_hat_3seed_fresh_eval.json:115` | JSON reporting note still mentions `86.37 +/- 1.54%`, but only as the plotted canonical single-checkpoint fresh-instance distribution, not as the main claim. | Acceptable if intentional; if reviewers may grep numbers, add a README sentence clarifying `86.16±0.19` is the release headline and `86.37±1.54` is single-checkpoint provenance only. |

## Summary

Final-submission blockers are thesis metadata placeholders and EN abstract/acknowledgement placeholders, not missing citations or Paper1 release framing. CN/EN latest logs are ref/citation clean but still have severe overfull hboxes that should be visually checked and fixed before producing final thesis PDFs. Paper1 release bundle appears consistent with the current `86.16±0.19` framing; no active README/manifest/source-text conflict was found.
