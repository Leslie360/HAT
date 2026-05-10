# Kimi Follow-up Dispatch — Final Bib / Prior-Art Hardening

Date: 2026-04-17
Owner: Codex
Goal: Close the remaining literature-quality gaps in the NC manuscript without inventing baselines or overstating prior art.

## Constraints
- Do not invent method names.
- Do not cite review summaries when a primary paper exists.
- Prefer DOI-backed journal/conference metadata.
- If a key in `refs_gpt.bib` is wrong but already widely cited in the manuscript, keep the existing key unless the mismatch is severe; provide a replacement block and note whether key renaming is worth the churn.

## Inputs
- `paper/latex_gpt/refs_gpt.bib`
- `paper/latex_gpt/sections/01_introduction.tex`
- `paper/latex_gpt/sections/02_related_work.tex`
- `report_md/bibliography_structured.csv`
- `report_md/_gpt/KIMI_BIB_REPLACEMENTS_20260417.md`
- `report_md/_gpt/KIMI_COMPARISON_REALITY_CHECK_20260417.md`

## Deliverable 1 — Remaining weak bib entries
Create:
- `report_md/_gpt/KIMI_BIB_FINAL_SWEEP_20260417.md`

Scope:
Check these remaining weak entries and give exact replacement metadata if any field is still weak/placeholder/incomplete:
- `alibart2016physical`
- `zeng2023organicmemristor`
- `jung2024organicfilaments`
- `sun2024survey`
- `wei2020voltagedifferential`
- `kim2024sttmram`
- `lin2024hardsea`
- `wu2023bwq`
- `lin2023vitptq`
- `wang2024epim`
- `ge2024allspark`
- `yoon2025adc`
- `li2022timemultiplexing`
- `gebregiorgis2023organiccim`
- `riam2013sneakpath`
- `fuller2020tempresilient`
- `guo2024hightemp`
- `li2023ivit`
- `zou2025ga2o3`
- `joshi2020accurate`
- `choi2019pact`

For each entry, report only if there is something worth fixing:
- wrong or incomplete authors
- wrong venue / year / pages
- missing DOI / stable URL
- better entry type (`@article` / `@inproceedings` / `@misc`)

## Deliverable 2 — Real prior art for Ensemble-HAT positioning
Create:
- `report_md/_gpt/KIMI_REAL_PRIOR_ART_20260417.md`

Task:
Find 3 to 5 real, citable works that are the closest prior art to our claim:
"fixed spatial mismatch during HAT causes hardware-instance overfitting; epoch-level structured resampling improves fresh-instance transfer."

Important:
- These do NOT have to be exact analog-CIM matches if none exist.
- Include the closest real baselines from:
  - analog HAT / variability-aware training
  - sim-to-real / domain randomization with structured perturbations
  - robustness to static instance-specific perturbations
- For each paper, explain in 2-4 sentences:
  - what it actually does
  - why it is or is not an apples-to-apples baseline
  - the safe one-line way we should cite it in related work or response

## Deliverable 3 — Organic system-level related work shortlist
Create:
- `report_md/_gpt/KIMI_ORGANIC_SYSTEM_SHORTLIST_20260417.md`

Task:
Find 4 to 6 real 2023-2026 papers most worth citing for this statement:
"Recent organic/optoelectronic arrays now provide enough empirical structure to motivate deployment-facing simulation, even though network-level system evaluation remains sparse."

Need:
- primary sources only
- DOI / stable URL
- 1-line note per paper saying whether it supports:
  - array integration
  - visual computing / in-sensor computing
  - optoelectronic plasticity / retention
  - system constraints such as crosstalk / active matrix / stability

## Output style
- Direct, compact, no fluff.
- Use tables where helpful.
- If something cannot be verified, say `unverified` rather than guessing.
