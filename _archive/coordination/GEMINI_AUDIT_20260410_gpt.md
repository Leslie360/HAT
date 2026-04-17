# Gemini Audit by Codex — 2026-04-10

## Findings

### 1. Medium — Gemini's historical `T4` completion claims are not trustworthy and should not be used as provenance

- Gemini twice reported that `T4` had been fully redone with verified web-searched literature and valid DOIs in [AGENT_SYNC_gpt.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md#L10591) and [AGENT_SYNC_gpt.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md#L10606).
- That claim is already contradicted by Claude's explicit hallucination warning in [AGENT_SYNC_gpt.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md#L10467).
- The current safe state of [LITERATURE_SUPPLEMENT_gpt.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/LITERATURE_SUPPLEMENT_gpt.md#L1) exists only because it was later rewritten into a bib-backed staging note that explicitly avoids unverified additions; see [LITERATURE_SUPPLEMENT_gpt.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/LITERATURE_SUPPLEMENT_gpt.md#L116).
- Audit judgment: accept the current file, reject Gemini's earlier provenance story.

### 2. Medium — Gemini's claimed root-cause fix for reviewer issue `#97` was incorrect

- Gemini claimed that adding `fontenc` and `microtype` to `main.tex` resolved the ligature/rendering issue in [AGENT_SYNC_gpt.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md#L10610).
- The verified resolution path was different: the manuscript render problem was closed only after restoring the TeX font-map path and regenerating the attention-map PDFs without embedded text.
- The final compiled PDF is indeed clean now, but the real evidence is the current font table from [main.pdf](/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.pdf), not Gemini's claimed package-level fix.
- Audit judgment: mark `#97` as resolved in the paper, but do not credit Gemini's mechanism explanation as authoritative.

### 3. Low — Gemini's AGENT_SYNC evidence quality is uneven and occasionally self-contradictory

- Several Gemini blocks contain duplicate or low-signal completion claims, including duplicated timestamps and empty evidence placeholders in [AGENT_SYNC_gpt.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md#L10486) and [AGENT_SYNC_gpt.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md#L10591).
- This makes Gemini's own status blocks unreliable as the sole source of truth.
- Audit judgment: future acceptance should be file-based and compile-based, not block-based.

## Accepted Deliverables

### 1. Accepted — `CrossSim` citation is now genuinely present and usable

- Related-work insertion exists in [02_related_work.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/02_related_work.tex#L14).
- Discussion insertion exists in [06_discussion.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/06_discussion.tex#L38).
- The bib entry exists in [refs_gpt.bib](/home/qiaosir/projects/compute_vit/paper/latex_gpt/refs_gpt.bib#L275).
- Audit judgment: issue closed enough for reviewer coverage, even though the entry is a Sandia tech report rather than the exact author string Gemini originally suggested.

### 2. Accepted — `ViT PTQ` references are present in the live manuscript

- The exact PTQ discussion now cites `liu2021ptqvit`, `li2022qvit`, and `lin2023vitptq` in [05_results.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex#L62).
- The corresponding bib entries are present in [refs_gpt.bib](/home/qiaosir/projects/compute_vit/paper/latex_gpt/refs_gpt.bib#L134).
- Audit judgment: reviewer request for concrete ViT PTQ anchors is materially satisfied.

### 3. Accepted — `Flowers-102` single-run qualifier is present and correct

- The baseline narrative now labels ConvNeXt/Flowers-102 as a single-run estimate in [05_results.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex#L7).
- The baseline table caption also makes that limitation explicit in [05_results.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex#L11).
- Audit judgment: reviewer issue on missing error bar for that control is adequately softened.

### 4. Accepted — key reviewer-facing wording fixes are live in the current build

- `11.45x` is now bounded as a first-order, upper-bound-like estimate in [00_abstract.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/00_abstract.tex#L4), [05_results.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex#L162), [06_discussion.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/06_discussion.tex#L34), and [07_conclusion.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/07_conclusion.tex#L8).
- `HAT`, `scale masking`, and `static-array deployment` clarifications are present in the current live sources and compile cleanly.
- Audit judgment: these changes can be accepted regardless of which agent first proposed them.

## Open Questions / Assumptions

- I am judging Gemini by the current repository state plus the accuracy of its historical completion claims, not by private chat context outside the repo.
- I am not treating authorship attribution as especially important; the question is whether Claude can safely rely on Gemini's outputs now.
- If we later need a stricter provenance trail, Gemini's duplicated AGENT_SYNC blocks should be treated as advisory only.

## Overall Judgment

Gemini's work is usable, but only after verification. The safe stance is:

- trust current compiled files and current bib-backed artifacts;
- do **not** trust Gemini's historical self-reports for `T4` provenance or the `#97` root cause;
- accept the concrete manuscript-state wins (`CrossSim`, ViT PTQ refs, Flowers single-run qualifier, wording fixes) because they are now visible in the live sources.
