# Dispatch Superphase P4 — Submission-Grade Finalization

Date: 2026-05-09
Issued by: Codex
Mode: long-running autonomous package
Expected duration: until clean final bundle and provenance archive both pass guards

## Executive Decision

Paper-1 scientific content is frozen. Do not change numbers, claims, figure semantics, or narrative framing. P4 is a packaging, reproducibility, and professionalism phase.

P3 produced a valid release candidate, but not a final submission-grade bundle because deprecated historical artifacts and build residues remain in the reviewer-facing package.

## Agents

- **Kimi**: primary executor for all tracks below.
- **DS**: audit after Kimi delivery, focusing on reproducibility and package hygiene.
- **Mimo**: audit after Kimi delivery, focusing on reviewer-facing clarity and submission completeness.
- **Gemini**: idle unless the user explicitly asks for visual/layout edits.
- **Codex**: final acceptance after Kimi + DS/Mimo.

## Track A — Split Submission Bundle From Provenance Archive

### Goal
Create two separate artifacts:

1. `release_artifacts/paper1_submission_bundle_20260509_final/`
2. `release_artifacts/paper1_provenance_archive_20260509/`

### Submission Bundle Rules

The submission bundle is reviewer-facing. It must contain no historical stale strings or deprecated old-protocol paths.

Include:

- `main.pdf`
- `supplementary_main.pdf`
- `main.tex`
- `supplementary.tex`
- `supplementary_main.tex`
- `cover_letter.tex`
- `cover_letter.pdf` if buildable; if not buildable, record source-only explicitly
- `refs_gpt.bib`
- active `sections/`
- active `supplementary/`
- only figures referenced by active LaTeX plus any explicitly documented graphical abstract if intended for submission
- active source data CSV/JSON/manifests needed for reported claims
- `RELEASE_README.md`
- `MANIFEST_FILES.txt`
- `SHA256SUMS.txt`

Exclude from submission bundle:

- `source_data/canonical_json/deprecated_20260501_old_protocol/`
- `figures/deprecated_20260424/`
- `*.aux`, `*.log`, `*.out`, `*.fls`, `*.fdb_latexmk`, `*.blg`
- `*.bak`, `*.bak_*`, `*draft*`, `*kimi_draft*`, `*temp*`, `*test*`
- checkpoints: `*.pt`, `*.pth`, `*.ckpt`
- old release bundles
- raw training directories
- any file >10 MB unless explicitly justified

### Provenance Archive Rules

The provenance archive may contain deprecated old-protocol JSON and historical manifests, but it must be clearly separate from the submission bundle.

Include:

- old-protocol 6-bit deprecated JSON
- historical manifests
- a `PROVENANCE_README.md` explaining why these are excluded from active claims
- hashes

Do not include large checkpoints unless explicitly approved.

## Track B — Zero-Stale Submission Guard

Run on `paper1_submission_bundle_20260509_final/` with no exclusions except binary PDFs/images if needed:

```bash
rg -n "77\.86|77\.88|77\.83|77\.76|78\.49|Pareto midpoint|best observed Pareto|critical Pareto|6-bit midpoint|seed456_full100|r11d_6bit_pcm_seed456_full100" release_artifacts/paper1_submission_bundle_20260509_final
```

Expected: **zero hits**.

Also run:

```bash
find release_artifacts/paper1_submission_bundle_20260509_final -type f \( -name '*.aux' -o -name '*.log' -o -name '*.out' -o -name '*.fls' -o -name '*.fdb_latexmk' -o -name '*.blg' -o -name '*.bak' -o -name '*draft*' -o -name '*temp*' -o -name '*test*' -o -name '*.pt' -o -name '*.pth' -o -name '*.ckpt' \) -print
find release_artifacts/paper1_submission_bundle_20260509_final -type f -size +10M -print
pdftotext release_artifacts/paper1_submission_bundle_20260509_final/main.pdf - | rg -n "77\.86|75\.43|72\.67|seed456_full100|6-bit midpoint|Pareto midpoint|pending|78\.49|\?\?" || true
pdftotext release_artifacts/paper1_submission_bundle_20260509_final/supplementary_main.pdf - | rg -n "77\.86|75\.43|72\.67|seed456_full100|6-bit midpoint|Pareto midpoint|6-bit.*pending|pending.*6-bit|78\.49|\?\?" || true
```

Expected: no active hits, no build artifacts, no large files, no visible `??` placeholders.

## Track C — Citation And Reference Hardening

### Goal
Final submission should not have unresolved citations or references.

From the final submission bundle, run clean-room builds and inspect logs:

```bash
tectonic main.tex
latexmk -pdf -interaction=nonstopmode -halt-on-error supplementary_main.tex
rg -n "Citation .* undefined|Reference .* undefined|There were undefined|undefined references|undefined citations|LaTeX Warning:.*undefined" *.log *.blg 2>/dev/null || true
```

Expected: no undefined citations/references in final logs.

If undefined warnings appear:

- Add missing BibTeX entries only if real and verifiable from existing `refs_gpt.bib` or already documented sources.
- If a supplementary reference points to a removed/nonexistent label, either add the label or remove the cross-reference phrase.
- Do not invent literature.
- Do not add new scientific claims.

## Track D — Cover Letter Handling

Try to build `cover_letter.pdf` from `cover_letter.tex` using the simplest viable path.

If it cannot build without restructuring, leave source-only but add this to `RELEASE_README.md`:

```text
Cover letter is provided as LaTeX source only; the journal submission system or author may compile it separately.
```

## Track E — Final Archive And Index Update

After all guards pass:

1. Generate `MANIFEST_FILES.txt` and `SHA256SUMS.txt` for both submission bundle and provenance archive.
2. Create compressed archives if size is reasonable:
   - `paper1_submission_bundle_20260509_final.tar.gz`
   - `paper1_provenance_archive_20260509.tar.gz`
3. Update:
   - `report_md/_gpt/PROJECT_MASTER_STATUS_20260509.md`
   - `report_md/_gpt/DATA_LOCATION_INDEX_20260429.md`
   - `report_md/_gpt/REMOTE_105_107_DATA_ACQUISITION_INDEX_20260507.md` only if remote status changed.

## Deliverables

Kimi must write:

1. `report_md/_gpt/KIMI_P4_TRACK_A_BUNDLE_SPLIT_REPORT_20260509.md`
2. `report_md/_gpt/KIMI_P4_TRACK_B_ZERO_STALE_GUARD_REPORT_20260509.md`
3. `report_md/_gpt/KIMI_P4_TRACK_C_CITATION_REFERENCE_REPORT_20260509.md`
4. `report_md/_gpt/KIMI_P4_TRACK_D_COVER_LETTER_REPORT_20260509.md`
5. `report_md/_gpt/KIMI_P4_FINAL_DELIVERY_20260509.md`

DS must audit after Kimi:

- `report_md/_gpt/DS_PHASE_P4_SUBMISSION_BUNDLE_AUDIT_20260509.md`

Mimo must audit after Kimi:

- `report_md/_gpt/MIMO_PHASE_P4_REVIEWER_COMPLETENESS_AUDIT_20260509.md`

## Success Criteria

P4 is complete when:

- submission bundle has zero stale old 6-bit strings globally;
- deprecated data exists only in separate provenance archive;
- no aux/log/build residue in submission bundle;
- no draft/backup/temp/checkpoint files;
- no undefined citations/references in final build logs, or any remaining warning is explicitly justified by Codex-level rationale;
- both PDFs present and pass text scans;
- manifests and SHA256 files pass;
- DS and Mimo audits pass.

## Kill Criteria

Stop and broadcast a blocker if:

- removing deprecated files breaks source-data traceability for active claims;
- citation cleanup requires inventing or guessing references;
- PDFs fail to build;
- global stale grep cannot be made zero without hiding active files;
- a remote 105/107 result attempts to alter Paper-1 claims.
