# KIMI Dispatch — Related Work / Citation Finish

Date: 2026-04-18
Repo: /home/qiaosir/projects/compute_vit
Priority: high

## Mission
Use the structured bibliography file and the current manuscript wording to produce final reviewer-safe related-work hardening materials.

Primary source file:
- /home/qiaosir/projects/compute_vit/report_md/bibliography_structured.csv

Current manuscript files to align against:
- /home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/01_introduction.tex
- /home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/02_related_work.tex
- /home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/06_discussion.tex
- /home/qiaosir/projects/compute_vit/paper/latex_gpt/refs_gpt.bib

## Deliverables
Create exactly these files under `report_md/_gpt/`:

1. `KIMI_RELATED_WORK_MAP_20260418.md`
   - Map 8–12 strongest references from `bibliography_structured.csv` into these buckets:
     - simulator positioning
     - variation-aware / hardware-aware training
     - domain-randomization adjacency
     - organic device / array motivation
     - ViT-on-CIM / mixed-signal partitioning
     - ADC / low-bit transformer sensitivity
   - For each entry give:
     - citation key
     - one-sentence relevance
     - exact safest use in our paper
     - one-sentence “do not overclaim” warning if needed

2. `KIMI_RELATED_WORK_DROPINS_20260418.md`
   - Write 3–5 drop-in paragraphs, publication style, conservative, citation-aware.
   - Targets:
     - intro simulator paragraph
     - related-work HAT paragraph
     - related-work organic-array paragraph
     - hybrid-mapping / ViT paragraph
     - discussion sentence on CrossSim / AIHWKIT complementarity
   - Do not invent methods.
   - Do not claim that organic-specific behavior is externally validated.

3. `KIMI_BIB_TAIL_FIXES_20260418.md`
   - Resolve the remaining weak metadata tail if possible:
     - `wei2020voltagedifferential`
     - `joshi2020accurate`
     - `choi2019pact`
   - For each, provide:
     - canonical title
     - canonical author list
     - DOI / URL if available
     - a drop-in BibTeX block
   - If any entry cannot be verified confidently, say so explicitly instead of guessing.

## Constraints
- No fabricated baselines.
- No MI-HAT / SDR-HAT unless you find a real citable source using that exact name.
- No unpublished/private data.
- Prefer journal / conference primary sources over blog or secondary summaries.
- If `bibliography_structured.csv` conflicts with current `refs_gpt.bib`, say which is more trustworthy and why.

## Output style
- Direct, compact, no fluff.
- Reviewer-safe wording only.
