# Dispatch Phase P2 — Paper-1 Release Candidate Bundle And Clean-Room Guard

Date: 2026-05-09
Issued by: Codex
Execution protocol: Kimi-first phased workflow

## Objective

Build a clean Paper-1 release candidate bundle from the now-accepted active manuscript and source-data state. This is a packaging and validation phase only. Do not change scientific claims, numbers, figure semantics, or visual design unless a concrete blocker is found.

## Executor Assignment

- **Kimi**: primary executor. Complete all packaging and guard work end-to-end.
- **DS**: audit after Kimi delivery. Focus on bundle contents, stale artifacts, reproducibility, and accidental large/private files.
- **Mimo**: audit after Kimi delivery. Focus on reviewer-facing completeness: PDF, cover letter, source data, and provenance clarity.
- **Gemini**: no action unless the user requests visual second-pass work.
- **Codex**: final acceptance after Kimi + DS/Mimo reports.

## Inputs

Read first:

1. `report_md/_gpt/CODEX_PHASE_P1_FINAL_ACCEPTANCE_20260509.md`
2. `report_md/_gpt/CODEX_FINAL_ACCEPTANCE_PCM_FREEZE_20260509.md`
3. `report_md/_gpt/KIMI_PHASE_P1_SOURCE_DATA_CANONICALIZATION_REPORT_20260509.md`
4. `paper/latex_gpt/source_data/canonical_json/README.md`
5. `paper/latex_gpt/source_data/canonical_json/manifest_canonical_json_20260509.json`

## Required Work

### 1. Build fresh artifacts

From `paper/latex_gpt/`, rebuild:

```bash
tectonic main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex
```

If `cover_letter.tex` has a supported build path, build it too. If not, record that it remains source-only.

### 2. Create release-candidate directory

Create a timestamped directory under:

`release_artifacts/paper1_release_candidate_20260509/`

Include only release-relevant small artifacts:

- `paper/latex_gpt/main.pdf`
- `paper/latex_gpt/supplementary_main.pdf`
- `paper/latex_gpt/cover_letter.tex`
- active LaTeX source needed to compile main/supplementary
- `paper/latex_gpt/refs_gpt.bib`
- active figures used by main/supplementary
- `paper/latex_gpt/source_data/` including `canonical_json/manifest_canonical_json_20260509.*`
- a generated `RELEASE_README.md` explaining build commands, canonical numbers, and deprecated data status

Do not include:

- `.pt` checkpoint files
- raw training directories outside source-data JSON evidence
- temporary render/test PDFs
- ChatGPT image prompt PNG references unless they are actively included by LaTeX
- old release bundles
- deprecated old-protocol JSON unless explicitly inside `source_data/canonical_json/deprecated_20260501_old_protocol/` and documented as non-active

### 3. Bundle guard

Run and save outputs in the release directory:

```bash
python scripts/_gpt/check_local_pcm_precision_ladder.py
rg -n "77\.86|77\.88|77\.83|77\.76|78\.49|Pareto midpoint|best observed Pareto|critical Pareto|6-bit midpoint|seed456_full100|r11d_6bit_pcm_seed456_full100" <release_dir> \
  --glob '!**/deprecated_20260501_old_protocol/**'
pdftotext <release_dir>/main.pdf - | rg -n "77\.86|75\.43|72\.67|seed456_full100|6-bit midpoint|Pareto midpoint|pending|78\.49" || true
pdftotext <release_dir>/supplementary_main.pdf - | rg -n "77\.86|75\.43|72\.67|seed456_full100|6-bit midpoint|Pareto midpoint|6-bit.*pending|pending.*6-bit|78\.49" || true
find <release_dir> -type f -size +20M -print
find <release_dir> -type f | sort > <release_dir>/MANIFEST_FILES.txt
sha256sum $(find <release_dir> -type f | sort) > <release_dir>/SHA256SUMS.txt
```

Expected:

- stale grep has zero active hits.
- PDF stale scans have zero hits.
- no file larger than 20 MB unless explicitly justified.
- release file manifest and SHA256SUMS exist.

### 4. Deliverable report

Write:

`report_md/_gpt/KIMI_PHASE_P2_RELEASE_CANDIDATE_BUNDLE_REPORT_20260509.md`

Required sections:

1. Bundle path
2. Files included/excluded
3. Build command outputs
4. Guard outputs
5. File-size scan
6. SHA256 manifest status
7. Remaining risks
8. One-line verdict: release-candidate valid or not valid

## Kill Criteria

Stop and broadcast a blocker if:

- active bundle grep finds stale old 6-bit claims outside deprecated folders;
- PDFs cannot be built;
- bundle contains `.pt` checkpoints or raw large training artifacts;
- source-data manifest and manuscript disagree on PCM ladder values;
- any required active figure/source is missing from the bundle.

## Success Criteria

P2 is complete when a clean release-candidate directory exists, guards pass, DS/Mimo can audit it without needing to infer active vs deprecated artifacts, and Codex can accept it without making semantic changes.
