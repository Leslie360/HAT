# R4 Path Reference Audit

Date: 2026-05-09
Purpose: preflight before moving Paper-1 manuscript/release paths.

## Pattern `paper/latex_gpt`

```text
WORKSPACE_LAYOUT_V2_20260509.md:201:| `paper/latex_gpt/` | active Paper-1 manuscript | `paper1/manuscript/` |
WORKSPACE_LAYOUT_V2_20260509.md:234:- Move `paper/latex_gpt/` to `paper1/manuscript/`.
RELEASE_CHECKLIST.md:184:- Recompile `paper/latex_gpt/main.tex` and confirm figure references resolve
PROJECT_INDEX.md:42:├── paper/                  manuscript source (LaTeX canonical under paper/latex_gpt/)
PROJECT_INDEX.md:147:### 5.1 Canonical LaTeX — **live** (under `paper/latex_gpt/`)
PROJECT_INDEX.md:151:| `paper/latex_gpt/main.tex` | Main manuscript entry | live |
PROJECT_INDEX.md:152:| `paper/latex_gpt/supplementary.tex` | Supplementary entry | live |
PROJECT_INDEX.md:153:| `paper/latex_gpt/supplementary_main.tex` | Built-out supplementary | live |
PROJECT_INDEX.md:154:| `paper/latex_gpt/cover_letter.tex` | Cover letter | live |
PROJECT_INDEX.md:155:| `paper/latex_gpt/sections/00_abstract.tex` | Abstract | live |
PROJECT_INDEX.md:156:| `paper/latex_gpt/sections/01_introduction.tex` | §1 | live |
PROJECT_INDEX.md:157:| `paper/latex_gpt/sections/02_related_work.tex` | §2 | live |
PROJECT_INDEX.md:158:| `paper/latex_gpt/sections/03_methodology.tex` | §3 | live |
PROJECT_INDEX.md:159:| `paper/latex_gpt/sections/04_experimental_setup.tex` | §4 | live |
PROJECT_INDEX.md:160:| `paper/latex_gpt/sections/05_results.tex` | §5 | live |
PROJECT_INDEX.md:161:| `paper/latex_gpt/sections/06_discussion.tex` | §6 | live |
PROJECT_INDEX.md:162:| `paper/latex_gpt/sections/07_conclusion.tex` | §7 | live |
PROJECT_INDEX.md:163:| `paper/latex_gpt/sections/08_appendix.tex` | Appendix | live |
PROJECT_INDEX.md:164:| `paper/latex_gpt/refs_gpt.bib` | Single canonical bibliography | live |
PROJECT_INDEX.md:165:| `paper/latex_gpt/figures/` | Compiled figures consumed by `.tex` | live |
PROJECT_INDEX.md:166:| `paper/latex_gpt/main.pdf` | 16pp, submission | live (frozen build output) |
PROJECT_INDEX.md:167:| `paper/latex_gpt/supplementary_main.pdf` | 16pp, submission | live |
PROJECT_INDEX.md:168:| `paper/latex_gpt/cover_letter.pdf` | 2pp | live |
PROJECT_INDEX.md:170:### 5.2 `paper/latex_gpt/` supporting markdown — **live**
PROJECT_INDEX.md:174:| `paper/latex_gpt/README_gpt.md` | How to compile | live |
PROJECT_INDEX.md:175:| `paper/latex_gpt/SUBMISSION_PACKET_gpt.md` | What to upload where | live |
PROJECT_INDEX.md:176:| `paper/latex_gpt/CITATION_MAP_gpt.md` | Which `\cite{}` maps to which journal | live |
PROJECT_INDEX.md:177:| `paper/latex_gpt/CITATION_BACKLOG_gpt.md` | Pending citation queue | live |
PROJECT_INDEX.md:178:| `paper/latex_gpt/CLOSEOUT_CHECKLIST_gpt.md` | Pre-submit gates | live |
PROJECT_INDEX.md:179:| `paper/latex_gpt/TEMPLATE_MIGRATION_GUIDE_gpt.md` | npj→NC migration log | frozen |
PROJECT_INDEX.md:329:- `paper/latex_gpt/main.pdf` = 16 pages, `supplementary_main.pdf` = 16 pages, `cover_letter.pdf` = 2 pages.
PROJECT_INDEX.md:330:- `paper/latex_gpt/refs_gpt.bib` is the only bibliography. Do not create a second `.bib`.
ROOT_REORG_PLAN_20260509.md:51:- Keep `paper/latex_gpt/` active until after submission or Codex acceptance.
ROOT_REORG_PLAN_20260509.md:95:paper/latex_gpt/ -> paper1/manuscript/
ROOT_REORG_PLAN_20260509.md:105:- update any scripts that assume `paper/latex_gpt`;
REPRODUCIBILITY.md:11:- `paper/latex_gpt/` — LaTeX source for main manuscript (15 pp), supplementary information (21 pp), and cover letter (2 pp).
.gitignore:25:paper/latex_gpt/*.aux
.gitignore:26:paper/latex_gpt/*.bbl
.gitignore:27:paper/latex_gpt/*.blg
.gitignore:28:paper/latex_gpt/*.fdb_latexmk
.gitignore:29:paper/latex_gpt/*.fls
.gitignore:30:paper/latex_gpt/*.log
.gitignore:31:paper/latex_gpt/*.out
.gitignore:32:paper/latex_gpt/*.synctex.gz
.gitignore:33:paper/latex_gpt/main.pdf
.gitignore:34:paper/latex_gpt/cover_letter.pdf
.gitignore:35:paper/latex_gpt/supplementary_main.pdf
.gitignore:72:paper/latex_gpt/figures/*.png
.gitignore:73:paper/latex_gpt/figures/*.pdf
.gitignore:74:!paper/latex_gpt/figures/fig1_system_architecture.pdf
.gitignore:75:!paper/latex_gpt/figures/fig2_weight_mapping.pdf
.gitignore:76:!paper/latex_gpt/figures/figA.png
.gitignore:77:!paper/latex_gpt/figures/figB.png
.gitignore:78:!paper/latex_gpt/figures/figC.png
.gitignore:79:!paper/latex_gpt/figures/figD.png
.gitignore:80:!paper/latex_gpt/figures/figS1_asymmetry_concept.png
.gitignore:81:!paper/latex_gpt/figures/figS2_nonideality.png
.gitignore:82:!paper/latex_gpt/figures/fig1_paper1_spine.pdf
.gitignore:83:!paper/latex_gpt/figures/fig1_paper1_spine.png
.gitignore:84:!paper/latex_gpt/figures/graphical_abstract.png
README_REPRODUCIBILITY_PAPER1.md:28:Run from `paper/latex_gpt`:
README_REPRODUCIBILITY_PAPER1.md:37:- `paper/latex_gpt/main.pdf`: 14 pages
README_REPRODUCIBILITY_PAPER1.md:38:- `paper/latex_gpt/supplementary_main.pdf`: 41 pages
README_REPRODUCIBILITY_PAPER1.md:45:paper/latex_gpt/source_data/canonical_json/
README_REPRODUCIBILITY_PAPER1.md:53:paper/latex_gpt/source_data/canonical_json/manifest_canonical_json_20260501.csv
README_REPRODUCIBILITY_PAPER1.md:54:paper/latex_gpt/source_data/canonical_json/manifest_canonical_json_20260501.json
README_REPRODUCIBILITY_PAPER1.md:55:paper/latex_gpt/source_data/manifest_all_figures_20260501.csv
README_REPRODUCIBILITY_PAPER1.md:56:paper/latex_gpt/source_data/manifest_bib_key_audit_20260501.json
README_REPRODUCIBILITY_PAPER1.md:57:paper/latex_gpt/source_data/manifest_bib_doi_resolution_20260501.json
WORKSPACE_LAYOUT.md:93:- LaTeX paper: `paper/latex_gpt/main.tex`
WORKSPACE_LAYOUT.md:94:- Cover letter: `paper/latex_gpt/cover_letter.tex`
WORKSPACE_LAYOUT.md:95:- Supplementary: `paper/latex_gpt/supplementary.tex`
broadcast.md:77:1. **Discussion paragraph** (~150 words) — placement target: `paper/latex_gpt/sections/06_discussion.tex` near existing AIHWKit citation if any, otherwise end of comparison subsection
broadcast.md:78:2. **Cover letter sentence** (~30 words) — placement target: `paper/latex_gpt/cover_letter.tex` in the contribution-summary paragraph
broadcast.md:79:3. **Comparison table** (LaTeX) — placement target: `paper/latex_gpt/supplementary.tex` near existing method-comparison section
broadcast.md:91:- `paper/latex_gpt/sections/06_discussion.tex` — Discussion file to edit
broadcast.md:92:- `paper/latex_gpt/cover_letter.tex` — cover letter to edit
broadcast.md:93:- `paper/latex_gpt/supplementary.tex` — supplementary to edit
broadcast.md:131:1. EDIT paper/latex_gpt/sections/06_discussion.tex
broadcast.md:143:2. EDIT paper/latex_gpt/cover_letter.tex
broadcast.md:147:3. EDIT paper/latex_gpt/supplementary.tex
broadcast.md:163:   cd /home/qiaosir/projects/compute_vit/paper/latex_gpt
broadcast.md:220:R11D-1 4-bit Path B review complete. I found and patched two issues before handoff: 1. paper/latex_gpt/cover_letter.tex used a manuscript-style citep in a standalone letter that does not load natbib or a bibliography, so I changed the new AIHWKit sentence to plain text citation: AIHWKit (Rasch et al., 2021). 2. paper/latex_gpt/supplementary.tex said Ensemble HAT maintains robustness at both precisions, but the new table only provides a 4-bit Ensemble HAT row, so I narrowed it to maintains robustness at the 4-bit operating point tested here. I also changed the new supplementary table from unconstrained lccc columns to wrapped p columns to remove the large overfull hbox introduced by the table. Updated output file: outputs/r11d_4bit_pathb_narrative_integration_20260426-213333.md. Verification after patches: main.tex latexmk RC 0; supplementary_main.tex latexmk RC 0; cover_letter.tex latexmk RC 0; locked-number guard 22 of 22 passed, including H12 87.28 and H13 14.64. Numeric provenance checked against the JSON payloads: AIHWKit 8-bit mean 87.282 std 0.1286, AIHWKit 4-bit mean 14.6368 std 0.1059, Ensemble HAT cross-seed mean 86.1587 std 0.1910. Banned wording search clean for post-fix and deployment-fidelity in the edited manuscript files. Remaining nonblocking log notes: main.log still has the pre-existing undefined cross-document reference tab:r10d-nl-interpolation; cover_letter.log has a tiny 0.636 pt overfull hbox in the pre-existing key-contributions paragraph. No blocking issues remain from my review. Please do the adversarial critic pass on narrative overclaim, table framing, and whether the cover-letter plain-text citation is acceptable for the submission package.
broadcast.md:247:- paper/latex_gpt/sections/06_discussion.tex
broadcast.md:248:- paper/latex_gpt/cover_letter.tex
broadcast.md:249:- paper/latex_gpt/supplementary.tex
broadcast.md:275:V6 PHANTOM (C1) is **already fixed** by Claude in `paper/latex_gpt/supplementary.tex` L132 (95.82±0.12 → 82.58 single-seed, real value from `report_md/_gpt/json_gpt/tinyvit_v2v7_results_gpt.json`). Pipeline should verify this stayed fixed and grep for stragglers.
broadcast.md:290:- Verify `paper/latex_gpt/supplementary.tex` L132 reads `82.58 (single-seed)`, not `95.82 ± 0.12`
broadcast.md:291:- Grep `95.82` across `paper/latex_gpt/` — must return zero hits
broadcast.md:294:- File: `paper/latex_gpt/sections/05_results.tex:41`
broadcast.md:299:- File: `paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex:33`
broadcast.md:304:- File: `paper/latex_gpt/sections/05_results.tex:101`
broadcast.md:309:- File: `paper/latex_gpt/sections/02_related_work.tex:7`
broadcast.md:316:- File 1: `paper/latex_gpt/sections/03_methodology.tex:50` — "V7 evaluates retention drift"
broadcast.md:317:- File 2: `paper/latex_gpt/sections/04_experimental_setup.tex:24` — "V7 & Legacy retention-aware model, excluded from canonical claims"
broadcast.md:321:- File: `paper/latex_gpt/sections/01_introduction.tex:9`
broadcast.md:330:- Action: `paper/latex_gpt/sections/08_appendix.tex` (~1,200 words) → move into `paper/latex_gpt/supplementary.tex` as new section §S-Appendix
broadcast.md:339:- Update all `\ref{fig:...}` in `paper/latex_gpt/sections/*.tex` and `paper/latex_gpt/supplementary.tex`
broadcast.md:340:- Verify `fig11_energy_breakdown.pdf` either has a `\ref` or moves to `paper/latex_gpt/figures/deprecated/`
broadcast.md:353:- File: `paper/latex_gpt/main.tex:25`
broadcast.md:357:- File: `paper/latex_gpt/sections/07_conclusion.tex:7`
broadcast.md:369:- `latexmk -pdf paper/latex_gpt/main.tex` returns RC 0 with **zero** undefined refs
broadcast.md:370:- `latexmk -pdf paper/latex_gpt/supplementary_main.tex` returns RC 0
broadcast.md:398:| `paper/latex_gpt/main.tex` | H1 (remove `\include{08_appendix}`), H5 |
broadcast.md:399:| `paper/latex_gpt/sections/01_introduction.tex` | C5 |
broadcast.md:400:| `paper/latex_gpt/sections/02_related_work.tex` | C3 |
broadcast.md:401:| `paper/latex_gpt/sections/03_methodology.tex` | C4 |
broadcast.md:402:| `paper/latex_gpt/sections/04_experimental_setup.tex` | C4 |
broadcast.md:403:| `paper/latex_gpt/sections/05_results.tex` | C2.1, C2.3 |
broadcast.md:404:| `paper/latex_gpt/sections/07_conclusion.tex` | H6 |
broadcast.md:405:| `paper/latex_gpt/sections/08_appendix.tex` | H1 (DELETE / MOVE) |
broadcast.md:406:| `paper/latex_gpt/supplementary.tex` | H1 (absorb 08_appendix), H3, H4, plus per-section H2 ref updates |
broadcast.md:407:| `paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex` | C2.2 |
broadcast.md:408:| `paper/latex_gpt/supplementary/S_theory_ensemble_hat_clean.tex` | H4 (DELETE if duplicate) |
broadcast.md:431:4. **Grep results** — `95.82` hits across `paper/latex_gpt/` (must be zero post-fix)
broadcast.md:460:- Action: grep `95.82` across `paper/latex_gpt/**/*.tex` — must return zero hits. (Build artifacts .fdb_latexmk may still contain it; ignore those.)
broadcast.md:464:- File: `paper/latex_gpt/sections/05_results.tex:41`
broadcast.md:469:- File: `paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex:33`
broadcast.md:476:- File: `paper/latex_gpt/sections/05_results.tex:101`
broadcast.md:481:- File: `paper/latex_gpt/sections/02_related_work.tex:7`
```

## Pattern `release_artifacts`

```text
WORKSPACE_LAYOUT_V2_20260509.md:202:| `release_artifacts/paper1_submission_bundle_20260509_final*` | final Paper-1 release | `paper1/release/` |
WORKSPACE_LAYOUT_V2_20260509.md:203:| `release_artifacts/paper1_provenance_archive_20260509*` | Paper-1 provenance | `paper1/provenance/` |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_E_FINAL_BUNDLE_REFRESH_IF_NEEDED_20260509.md:35:| Final bundle directory | `release_artifacts/paper1_submission_bundle_20260509_final/` | 133 SHA-verified entries |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_E_FINAL_BUNDLE_REFRESH_IF_NEEDED_20260509.md:36:| Final tarball | `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | 9.9M |
ROOT_REORG_PLAN_20260509.md:19:`32959fac881ad1659d2da0a4ebeba30846dac72986e032dc411ea6e916c6f4a4  release_artifacts/paper1_submission_bundle_20260509_final.tar.gz`
ROOT_REORG_PLAN_20260509.md:97:release_artifacts/paper1_submission_bundle_20260509_final* -> paper1/release/
ROOT_REORG_PLAN_20260509.md:98:release_artifacts/paper1_provenance_archive_20260509* -> paper1/provenance/
ROOT_REORG_PLAN_20260509.md:177:- `sha256sum release_artifacts/paper1_submission_bundle_20260509_final.tar.gz`
ROOT_REORG_PLAN_20260509.md:178:- `sha256sum -c release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt`
paper1/reports/P7/KIMI/KIMI_P7_TRACK_H_SUBMISSION_CHECKLIST_AND_DEFENSE_PACK_20260509.md:25:| Final bundle directory | `release_artifacts/paper1_submission_bundle_20260509_final/` | ✅ 135 files |
WORKSPACE_LAYOUT.md:65:| `release_artifacts/` | Zenodo bundle staging | |
WORKSPACE_LAYOUT.md:134:| `checkpoints/_ensemble/V4_*.pt` (canonical 86.37%) | Local + Zenodo | Bundle in `release_artifacts/source_data_v1/` for paper-1 release |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_A_FINAL_FREEZE_CERTIFICATE_20260509.md:5:**Scope:** `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz`
paper1/reports/P7/KIMI/KIMI_P7_TRACK_A_FINAL_FREEZE_CERTIFICATE_20260509.md:13:| Tarball path | `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:13:| `release_artifacts/paper1_submission_bundle_20260509_final/` | KEEP_RELEASE | ~150 MB | Final submission bundle | ❌ NO | ❌ NO |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:14:| `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | KEEP_RELEASE | ~150 MB | Final tarball (SHA256 verified) | ❌ NO | ❌ NO |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:15:| `release_artifacts/paper1_provenance_archive_20260509/` | KEEP_PROVENANCE | ~150 MB | Historical provenance | ❌ NO | ❌ NO |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:16:| `release_artifacts/paper1_provenance_archive_20260509.tar.gz` | KEEP_PROVENANCE | ~150 MB | Provenance tarball | ❌ NO | ❌ NO |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:17:| `release_artifacts/paper1_reviewer_bundle_20260501_1645.tar.gz` | KEEP_PROVENANCE | ~50 MB | Old reviewer bundle | ❌ NO | ❌ NO |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:18:| `release_artifacts/paper1_release_candidate_20260509/` | KEEP_PROVENANCE | ~150 MB | Superseded release candidate | ⚠️ Quarantine | ❌ NO |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:19:| `release_artifacts/paper1_release_candidate_20260509_clean/` | KEEP_PROVENANCE | ~150 MB | Superseded clean candidate | ⚠️ Quarantine | ❌ NO |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:81:| `release_artifacts/*.tar.gz` | ~400 MB total | KEEP_RELEASE/PROVENANCE | Keep, never commit |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:159:| `release_artifacts/paper1_submission_bundle_20260509_final/` | Final submission bundle | `ls -la release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt` |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:160:| `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | Final tarball | `sha256sum release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:161:| `release_artifacts/paper1_provenance_archive_20260509/` | Provenance | `ls -la release_artifacts/paper1_provenance_archive_20260509/` |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:178:sha256sum -c release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt | tail -5
paper1/reports/P6/KIMI/KIMI_P6_TRACK_G_REPO_HYGIENE_EXECUTION_PLAN_20260509.md:52:| `release_artifacts/paper1_provenance_archive_20260509.tar.gz` | ~? | `.gitignore` |
paper1/reports/P6/KIMI/KIMI_P6_TRACK_G_REPO_HYGIENE_EXECUTION_PLAN_20260509.md:53:| `release_artifacts/paper1_reviewer_bundle_20260501_1645.tar.gz` | ~? | `.gitignore` |
paper1/reports/P6/KIMI/KIMI_P6_TRACK_G_REPO_HYGIENE_EXECUTION_PLAN_20260509.md:54:| `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | ~? | `.gitignore` |
paper1/reports/P6/KIMI/KIMI_P6_TRACK_G_REPO_HYGIENE_EXECUTION_PLAN_20260509.md:77:release_artifacts/*.tar.gz
paper1/reports/P6/KIMI/KIMI_P6_TRACK_G_REPO_HYGIENE_EXECUTION_PLAN_20260509.md:86:release_artifacts/paper1_reviewer_bundle_20260501_1645/
paper1/reports/P6/KIMI/KIMI_P6_TRACK_G_REPO_HYGIENE_EXECUTION_PLAN_20260509.md:108:git add release_artifacts/paper1_submission_bundle_20260509_final/
paper1/reports/P6/KIMI/KIMI_P6_TRACK_G_REPO_HYGIENE_EXECUTION_PLAN_20260509.md:109:git add release_artifacts/paper1_provenance_archive_20260509/
paper1/reports/P6/KIMI/KIMI_P6_TRACK_G_REPO_HYGIENE_EXECUTION_PLAN_20260509.md:110:git add release_artifacts/paper1_release_candidate_20260509_clean/
paper1/reports/P6/KIMI/KIMI_P6_TRACK_G_REPO_HYGIENE_EXECUTION_PLAN_20260509.md:122:git rm -r release_artifacts/paper1_reviewer_bundle_20260501_1645/ 2>/dev/null || true
paper1/reports/P6/acceptance/CODEX_PHASE_P6_FINAL_ACCEPTANCE_20260509.md:69:| `release_artifacts/paper1_submission_bundle_20260509_final/` | Resynced from working submission tree. |
paper1/reports/P6/acceptance/CODEX_PHASE_P6_FINAL_ACCEPTANCE_20260509.md:70:| `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | Recreated from repaired final bundle. |
paper1/reports/P6/acceptance/CODEX_PHASE_P6_FINAL_ACCEPTANCE_20260509.md:77:`release_artifacts/paper1_submission_bundle_20260509_final/`
paper1/reports/P6/acceptance/CODEX_PHASE_P6_FINAL_ACCEPTANCE_20260509.md:81:`release_artifacts/paper1_submission_bundle_20260509_final.tar.gz`
broadcast.md:3520:- Final tarball: `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz`.
paper1/reports/P8/audits/Claude/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md:86:| `release_artifacts/paper1_submission_bundle_20260509_final/` | OK |
paper1/reports/P8/audits/Claude/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md:87:| `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | OK |
paper1/reports/P8/audits/Claude/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md:88:| `release_artifacts/paper1_provenance_archive_20260509/` | OK |
paper1/reports/P8/audits/Claude/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md:89:| `release_artifacts/paper1_provenance_archive_20260509.tar.gz` | OK |
paper1/reports/P8/audits/Claude/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md:100:`32959fac881ad1659d2da0a4ebeba30846dac72986e032dc411ea6e916c6f4a4  release_artifacts/paper1_submission_bundle_20260509_final.tar.gz`
paper1/reports/P8/audits/Claude/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md:117:| `release_artifacts/paper1_submission_bundle_20260509_final*` | final submission bundle |
paper1/reports/P8/audits/Claude/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md:118:| `release_artifacts/paper1_provenance_archive_20260509*` | final provenance archive |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:86:| `release_artifacts/paper1_submission_bundle_20260509_final/` | Final submission bundle |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:87:| `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | Final tarball |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:88:| `release_artifacts/paper1_provenance_archive_20260509/` | Provenance archive |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:89:| `release_artifacts/paper1_provenance_archive_20260509.tar.gz` | Provenance tarball |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:151:| `release_artifacts/*.tar.gz` | ~200 MB | Release tarballs | **Do not commit** — keep in `.gitignore` |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_J_FINAL_USER_HANDOFF_MAP_20260509.md:10:| Final bundle dir | `release_artifacts/paper1_submission_bundle_20260509_final/` | SHA verified, 133/133 OK after self-audit repair |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_J_FINAL_USER_HANDOFF_MAP_20260509.md:11:| Final tarball | `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | SHA256 `32959fac881ad1659d2da0a4ebeba30846dac72986e032dc411ea6e916c6f4a4`, size 9.9M |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_J_FINAL_USER_HANDOFF_MAP_20260509.md:20:Upload these files from `release_artifacts/paper1_submission_bundle_20260509_final/`:
paper1/reports/P8/KIMI/KIMI_P8_TRACK_J_FINAL_USER_HANDOFF_MAP_20260509.md:29:`release_artifacts/paper1_submission_bundle_20260509_final.tar.gz`
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:10:| Final submission tarball SHA | `32959fac881ad1659d2da0a4ebeba30846dac72986e032dc411ea6e916c6f4a4  release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` |
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:11:| Bundle manifest entries | `133 release_artifacts/paper1_submission_bundle_20260509_final/MANIFEST_FILES.txt` |
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:45:?? release_artifacts/paper1_provenance_archive_20260509.tar.gz
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:46:?? release_artifacts/paper1_provenance_archive_20260509/
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:47:?? release_artifacts/paper1_submission_bundle_20260509_final.tar.gz
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:48:?? release_artifacts/paper1_submission_bundle_20260509_final/
paper1/reports/P7/audits/DS/DS_PHASE_P7_FINAL_FREEZE_CLEANUP_AUDIT_20260509.md:77:| Final release | `release_artifacts/paper1_submission_bundle_20260509_final/` | KEEP_RELEASE |
paper1/reports/P7/audits/DS/DS_PHASE_P7_FINAL_FREEZE_CLEANUP_AUDIT_20260509.md:78:| Final tarball | `release_artifacts/*.tar.gz` | KEEP_RELEASE |
paper1/reports/P7/audits/DS/DS_PHASE_P7_FINAL_FREEZE_CLEANUP_AUDIT_20260509.md:79:| Provenance | `release_artifacts/paper1_provenance_archive_20260509/` | KEEP_PROVENANCE |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_C_CLEANUP_EXECUTION_OR_DRYRUN_20260509.md:55:| `release_artifacts/paper1_submission_bundle_20260509_final/` | Preserved; refreshed only by Track E |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_C_CLEANUP_EXECUTION_OR_DRYRUN_20260509.md:56:| `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | Preserved/refreshed; SHA verified |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_C_CLEANUP_EXECUTION_OR_DRYRUN_20260509.md:57:| `release_artifacts/paper1_provenance_archive_20260509/` | Not moved |
paper1/reports/P8/audits/Claude/CLAUDE_P8_SELF_AUDIT_20260509.md:16:| `release_artifacts/paper1_submission_bundle_20260509_final/sections/06_discussion.tex.bak_20260425` was included in the bundle | Bundle contained stale backup text and made stale-value scans misleading | Moved to `archive/cleanup_candidates_20260509/bundle_strays/`; regenerated `MANIFEST_FILES.txt`, `SHA256SUMS.txt`, and tarball | Fixed |
paper1/reports/P8/audits/Claude/CLAUDE_P8_SELF_AUDIT_20260509.md:26:| Final tarball | `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:25:| Release bundle | `release_artifacts/paper1_submission_bundle_20260509_final/` and final tarball, if repository policy accepts tarball artifacts |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:37:| Legacy bundles | `release_artifacts/paper1_reviewer_bundle_20260501_1645*`, `paper1_release_candidate_*`, provenance tarballs unless explicitly desired |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:90:  release_artifacts/paper1_submission_bundle_20260509_final \
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:91:  release_artifacts/paper1_submission_bundle_20260509_final.tar.gz \
paper1/reports/P7/KIMI/KIMI_P7_TRACK_C_CANONICAL_DATA_MAP_V2_20260509.md:39:| `release_artifacts/paper1_submission_bundle_20260509_final/` | Release | Active | ✅ YES | Final submission bundle (135 files) |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_C_CANONICAL_DATA_MAP_V2_20260509.md:40:| `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | Release | Active | ✅ YES | Final tarball (SHA256 verified) |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_C_CANONICAL_DATA_MAP_V2_20260509.md:41:| `release_artifacts/paper1_provenance_archive_20260509/` | Provenance | Active | ✅ YES | Historical provenance (73 files) |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_C_CANONICAL_DATA_MAP_V2_20260509.md:42:| `release_artifacts/paper1_provenance_archive_20260509.tar.gz` | Provenance | Active | ✅ YES | Provenance tarball |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_C_CANONICAL_DATA_MAP_V2_20260509.md:43:| `release_artifacts/paper1_release_candidate_20260509/` | Release | Obsolete | ⚠️ REVIEW | Superseded by final bundle |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_C_CANONICAL_DATA_MAP_V2_20260509.md:44:| `release_artifacts/paper1_release_candidate_20260509_clean/` | Release | Obsolete | ⚠️ REVIEW | Superseded by final bundle |
report_md/_gpt/ROOT_ENTRY_PURPOSE_MAP_20260509.md:53:| `release_artifacts` | final submission and provenance artifacts | split into paper1/release and paper1/provenance later |
report_md/_gpt/AGENT_SYNC_gpt.md:21820:  - Wrote `release_artifacts/CODE_SNAPSHOT_LEDGER_20260418.md`
report_md/_gpt/AGENT_SYNC_gpt.md:21822:  - Wrote `release_artifacts/source_data_v0_MANIFEST.md`
report_md/_gpt/AGENT_SYNC_gpt.md:21823:  - Wrote `release_artifacts/source_data_v0.zip`
report_md/_gpt/AGENT_SYNC_gpt.md:22021:  - Added explicit references to `release_artifacts/source_data_v0.zip`, `source_data_v0_MANIFEST.md`, and `release_artifacts/CODE_SNAPSHOT_LEDGER_20260418.md`.
report_md/_gpt/AGENT_SYNC_gpt.md:22158:- `release_artifacts/source_data_v1.zip`: 144 KiB, 76 files (72 JSON + 2 CSV + README + MANIFEST).
report_md/_gpt/AGENT_SYNC_gpt.md:22159:- `release_artifacts/source_data_v1_MANIFEST.md`: Created.
report_md/_gpt/AGENT_SYNC_gpt.md:22165:- `release_artifacts/source_data_v1.zip`
report_md/_gpt/AGENT_SYNC_gpt.md:22166:- `release_artifacts/source_data_v1_MANIFEST.md`
report_md/_gpt/AGENT_SYNC_gpt.md:22886:- Completed `CX-EB`: built `release_artifacts/zenodo_archive_v0/` with `CITATION.cff`, README, SHA256 manifest, code snapshot, and `source_data_v1.zip`.
report_md/_gpt/AGENT_SYNC_gpt.md:26363:- Release mirror: `release_artifacts/source_data_v1/fresh_instance_eval_v4_ensemble_correlated_d2d.json`.
report_md/_gpt/AGENT_SYNC_gpt.md:27124:- `paper/`, `paper_orchestra_input/`, `release_artifacts/`, `report_md/_gpt/`, `device_profiles/`, `tmp/bak_cleanup_20260425/`
report_md/_gpt/AGENT_SYNC_gpt.md:27229:- `paper/`, `paper_orchestra_input/`, `release_artifacts/`
report_md/_gpt/AGENT_SYNC_gpt.md:29413:- `/home/qiaosir` — 80+ files (scripts/_gpt/, release_artifacts/, paper2/results/)
report_md/_gpt/AGENT_SYNC_gpt.md:29414:- `doctor_measured_profile(s)` — 50+ files (scripts/_gpt/, release_artifacts/)
report_md/_gpt/AGENT_SYNC_gpt.md:29415:- `数据_博士` — 5 files (RELEASE_CHECKLIST, REPRODUCIBILITY, WORKSPACE_LAYOUT, release_artifacts/)
report_md/_gpt/AGENT_SYNC_gpt.md:29420:- `scripts/_gpt/` and `release_artifacts/` are internal-only trees per RELEASE_CHECKLIST §3. They will be excluded from public release via branch curation. Matches here are **expected** and not a release risk IF curation is done correctly.
report_md/_gpt/AGENT_SYNC_gpt.md:31554:- `release_artifacts/paper1_reviewer_bundle_20260501_1645/`;
report_md/_gpt/AGENT_SYNC_gpt.md:31555:- `release_artifacts/paper1_reviewer_bundle_20260501_1645.tar.gz` (42 MB).
report_md/_gpt/AGENT_SYNC_gpt.md:31602:- Active submission artifact: `release_artifacts/paper1_submission_bundle_20260509_final/` and `.tar.gz`.
report_md/_gpt/AGENT_SYNC_gpt.md:31603:- Provenance-only artifact: `release_artifacts/paper1_provenance_archive_20260509/` and `.tar.gz`.
report_md/_gpt/AGENT_SYNC_gpt.md:31626:Accepted artifact: `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz`.
report_md/_gpt/AGENT_SYNC_gpt.md:31666:- Final tarball: `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz`.
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:131:## Pattern `release_artifacts`
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:134:WORKSPACE_LAYOUT_V2_20260509.md:202:| `release_artifacts/paper1_submission_bundle_20260509_final*` | final Paper-1 release | `paper1/release/` |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:135:WORKSPACE_LAYOUT_V2_20260509.md:203:| `release_artifacts/paper1_provenance_archive_20260509*` | Paper-1 provenance | `paper1/provenance/` |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:136:paper1/reports/P8/KIMI/KIMI_P8_TRACK_E_FINAL_BUNDLE_REFRESH_IF_NEEDED_20260509.md:35:| Final bundle directory | `release_artifacts/paper1_submission_bundle_20260509_final/` | 133 SHA-verified entries |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:137:paper1/reports/P8/KIMI/KIMI_P8_TRACK_E_FINAL_BUNDLE_REFRESH_IF_NEEDED_20260509.md:36:| Final tarball | `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | 9.9M |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:138:ROOT_REORG_PLAN_20260509.md:19:`32959fac881ad1659d2da0a4ebeba30846dac72986e032dc411ea6e916c6f4a4  release_artifacts/paper1_submission_bundle_20260509_final.tar.gz`
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:139:ROOT_REORG_PLAN_20260509.md:97:release_artifacts/paper1_submission_bundle_20260509_final* -> paper1/release/
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:140:ROOT_REORG_PLAN_20260509.md:98:release_artifacts/paper1_provenance_archive_20260509* -> paper1/provenance/
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:141:ROOT_REORG_PLAN_20260509.md:177:- `sha256sum release_artifacts/paper1_submission_bundle_20260509_final.tar.gz`
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:142:ROOT_REORG_PLAN_20260509.md:178:- `sha256sum -c release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt`
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:143:paper1/reports/P7/KIMI/KIMI_P7_TRACK_H_SUBMISSION_CHECKLIST_AND_DEFENSE_PACK_20260509.md:25:| Final bundle directory | `release_artifacts/paper1_submission_bundle_20260509_final/` | ✅ 135 files |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:144:WORKSPACE_LAYOUT.md:65:| `release_artifacts/` | Zenodo bundle staging | |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:145:WORKSPACE_LAYOUT.md:134:| `checkpoints/_ensemble/V4_*.pt` (canonical 86.37%) | Local + Zenodo | Bundle in `release_artifacts/source_data_v1/` for paper-1 release |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:146:paper1/reports/P7/KIMI/KIMI_P7_TRACK_A_FINAL_FREEZE_CERTIFICATE_20260509.md:5:**Scope:** `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz`
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:147:paper1/reports/P7/KIMI/KIMI_P7_TRACK_A_FINAL_FREEZE_CERTIFICATE_20260509.md:13:| Tarball path | `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:148:paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:13:| `release_artifacts/paper1_submission_bundle_20260509_final/` | KEEP_RELEASE | ~150 MB | Final submission bundle | ❌ NO | ❌ NO |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:149:paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:14:| `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | KEEP_RELEASE | ~150 MB | Final tarball (SHA256 verified) | ❌ NO | ❌ NO |
```

## Pattern `report_md/_gpt`

```text
WORKSPACE_LAYOUT_V2_20260509.md:204:| `report_md/_gpt/` | coordination/report hub | `coordination/` + `paper1/reports/` |
WORKSPACE_LAYOUT_V2_20260509.md:249:- `report_md/_gpt/FILE_PURPOSE_INVENTORY_20260509.tsv`
WORKSPACE_LAYOUT_V2_20260509.md:250:- `report_md/_gpt/FILE_PURPOSE_INVENTORY_SUMMARY_20260509.md`
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:75:| `report_md/_gpt/KIMI_P7_*` | P7 deliverables |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:76:| `report_md/_gpt/CODEX_PHASE_P6_*` | Codex acceptance |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:77:| `report_md/_gpt/DS_PHASE_P6_*` | DS audit |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:78:| `report_md/_gpt/MIMO_PHASE_P6_*` | Mimo audit |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:223:git add report_md/_gpt/KIMI_P7_*.md
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:224:git add report_md/_gpt/CODEX_PHASE_P6_*.md
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:225:git add report_md/_gpt/DS_PHASE_P6_*.md
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:226:git add report_md/_gpt/MIMO_PHASE_P6_*.md
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:266:git add report_md/_gpt/KIMI_P7_*.md
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:267:git add report_md/_gpt/CODEX_PHASE_P6_*.md
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:268:git add report_md/_gpt/DS_PHASE_P6_*.md
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:269:git add report_md/_gpt/MIMO_PHASE_P6_*.md
paper1/reports/P8/KIMI/KIMI_P8_TRACK_J_FINAL_USER_HANDOFF_MAP_20260509.md:35:`report_md/_gpt/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md`
paper1/reports/P8/KIMI/KIMI_P8_TRACK_J_FINAL_USER_HANDOFF_MAP_20260509.md:72:读取任务文件：report_md/_gpt/REMOTE_105_PHASE_P8_FINAL_INGESTION_TASKLIST_20260509.md
paper1/reports/P8/KIMI/KIMI_P8_TRACK_J_FINAL_USER_HANDOFF_MAP_20260509.md:86:读取任务文件：report_md/_gpt/REMOTE_107_PHASE_P8_CORRECTED_NOISE_WORK2_TASKLIST_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:49:?? report_md/_gpt/BROADCAST_CLAUDE_PAPER1_MAIN_APPENDIX_REVIEW_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:50:?? report_md/_gpt/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:51:?? report_md/_gpt/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:52:?? report_md/_gpt/CLAUDE_P8_SELF_AUDIT_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:53:?? report_md/_gpt/CODEX_APPENDIX_CONTENT_REPAIR_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:54:?? report_md/_gpt/CODEX_FINAL_ACCEPTANCE_PCM_FREEZE_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:55:?? report_md/_gpt/CODEX_PHASED_WORKFLOW_PROTOCOL_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:56:?? report_md/_gpt/CODEX_PHASE_P6_FINAL_ACCEPTANCE_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:57:?? report_md/_gpt/CODEX_PHASE_P7_FINAL_ACCEPTANCE_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:58:?? report_md/_gpt/CODEX_REVIEW_CLAUDE_BROADCAST_AND_GPU_STATUS_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:59:?? report_md/_gpt/DISPATCH_KIMI_PCM_CORRECTED_EVAL_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:60:?? report_md/_gpt/DISPATCH_PCM_6BIT_DRIFT_AND_APPENDIX_REPAIR_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:61:?? report_md/_gpt/DISPATCH_SUPERPHASE_P6_EXPERIMENT_COMPLETION_AND_EVIDENCE_GAP_CLOSURE_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:62:?? report_md/_gpt/DISPATCH_SUPERPHASE_P7_FINAL_FREEZE_REPO_AND_WORK2_BRIDGE_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:63:?? report_md/_gpt/DISPATCH_SUPERPHASE_P8_ULTRA_LONG_MANUSCRIPT_REPO_REMOTE_WORK2_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:64:?? report_md/_gpt/DS_IDEALDEVICE_AND_PCM_PROTOCOL_AUDIT_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:65:?? report_md/_gpt/DS_PCM_CORRECTED_EVAL_AUDIT_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:66:?? report_md/_gpt/DS_PHASE_P6_HOSTILE_EXPERIMENT_AUDIT_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:67:?? report_md/_gpt/DS_PHASE_P7_FINAL_FREEZE_CLEANUP_AUDIT_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:68:?? report_md/_gpt/KIMI_6BIT_DRIFT_CLOSURE_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:69:?? report_md/_gpt/KIMI_6BIT_RECONCILIATION_REPORT_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:70:?? report_md/_gpt/KIMI_P6_DEEP_VERIFICATION_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:71:?? report_md/_gpt/KIMI_P6_FINAL_DELIVERY_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:72:?? report_md/_gpt/KIMI_P6_SELF_AUDIT_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:73:?? report_md/_gpt/KIMI_P6_TRACK_A_EVIDENCE_GAP_LEDGER_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:74:?? report_md/_gpt/KIMI_P6_TRACK_B_LOCAL_PCM_GAP_CLOSURE_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:75:?? report_md/_gpt/KIMI_P6_TRACK_C_LOCAL_GPU_EXECUTION_REPORT_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:76:?? report_md/_gpt/KIMI_P6_TRACK_D_STATISTICAL_COMPLETION_PACK_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:77:?? report_md/_gpt/KIMI_P6_TRACK_E_REMOTE105_CLOSURE_PACKAGE_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:78:?? report_md/_gpt/KIMI_P6_TRACK_F_REMOTE107_KV_CLOSURE_PACKAGE_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:79:?? report_md/_gpt/KIMI_P6_TRACK_G_REPO_HYGIENE_EXECUTION_PLAN_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:80:?? report_md/_gpt/KIMI_P6_TRACK_H_FINAL_EXPERIMENT_COMPLETENESS_VERDICT_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:81:?? report_md/_gpt/KIMI_P7_SELF_AUDIT_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:82:?? report_md/_gpt/KIMI_P7_TRACK_A_FINAL_FREEZE_CERTIFICATE_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:83:?? report_md/_gpt/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:84:?? report_md/_gpt/KIMI_P7_TRACK_C_CANONICAL_DATA_MAP_V2_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:85:?? report_md/_gpt/KIMI_P7_TRACK_D_REMOTE105_CLOSURE_GATE_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:86:?? report_md/_gpt/KIMI_P7_TRACK_E_REMOTE107_WORK2_GATE_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:87:?? report_md/_gpt/KIMI_P7_TRACK_F_LOCAL_GPU_POLICY_AND_OPTIONAL_QUEUE_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:88:?? report_md/_gpt/KIMI_P7_TRACK_G_APPENDIX_VISUAL_QA_HANDOFF_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:89:?? report_md/_gpt/KIMI_P7_TRACK_H_SUBMISSION_CHECKLIST_AND_DEFENSE_PACK_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:90:?? report_md/_gpt/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:91:?? report_md/_gpt/KIMI_P8_SELF_AUDIT_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:92:?? report_md/_gpt/KIMI_P8_TRACK_A_NARRATIVE_DESLOP_REWRITE_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:93:?? report_md/_gpt/KIMI_P8_TRACK_B_APPENDIX_TEXT_AND_TABLE_CONSISTENCY_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:94:?? report_md/_gpt/KIMI_P8_TRACK_C_CLEANUP_EXECUTION_OR_DRYRUN_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:95:?? report_md/_gpt/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:96:?? report_md/_gpt/KIMI_P8_TRACK_E_FINAL_BUNDLE_REFRESH_IF_NEEDED_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:97:?? report_md/_gpt/KIMI_P8_TRACK_F_REMOTE105_INGESTION_READY_PACKET_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:98:?? report_md/_gpt/KIMI_P8_TRACK_G_REMOTE107_WORK2_READY_PACKET_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:99:?? report_md/_gpt/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:100:?? report_md/_gpt/KIMI_P8_TRACK_I_LOCAL_GPU_AND_WORK2_OPTIONAL_QUEUE_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:101:?? report_md/_gpt/KIMI_P8_TRACK_J_FINAL_USER_HANDOFF_MAP_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:102:?? report_md/_gpt/MIMO_APPENDIX_REVIEWER_RISK_AUDIT_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:103:?? report_md/_gpt/MIMO_PCM_NARRATIVE_REPAIR_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:104:?? report_md/_gpt/MIMO_PHASE_P6_DEFENSE_READINESS_AUDIT_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:105:?? report_md/_gpt/MIMO_PHASE_P7_RELEASE_READINESS_AUDIT_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:106:?? report_md/_gpt/REMOTE_105_PHASE_P8_FINAL_INGESTION_TASKLIST_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:107:?? report_md/_gpt/REMOTE_107_PHASE_P8_CORRECTED_NOISE_WORK2_TASKLIST_20260509.md
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:115:git add report_md/_gpt/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md report_md/_gpt/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md report_md/_gpt/AGENT_SYNC_gpt.md broadcast.md
eval_fresh_instances.py:55:    output_path = Path("report_md/_gpt/json_gpt/fresh_instance_eval.json")
hybrid_runtime_compiler.py:206:    parser.add_argument("--json-out", default="report_md/_gpt/json_gpt/hybrid_deployment_policy.json")
train_tinyvit.py:48:DEFAULT_REPORT_PATH = "report_md/_gpt/tinyvit_hybrid_dryrun_report_gpt.md"
train_tinyvit.py:50:DEFAULT_RESULTS_JSON_PATH = asset_path("report_md/_gpt", "json", "tinyvit_results_gpt.json")
train_tinyvit.py:51:DEFAULT_RESULTS_CSV_PATH = asset_path("report_md/_gpt", "csv", "tinyvit_results_gpt.csv")
train_tinyvit.py:52:DEFAULT_RESULTS_MD_PATH = "report_md/_gpt/tinyvit_results_gpt.md"
eval_fresh_instances_postfix.py:201:    output_path = args.output or f"report_md/_gpt/json_gpt/{Path(args.checkpoint).stem}_fresh_eval.json"
paper1/reports/P8/audits/Claude/CLAUDE_P8_SELF_AUDIT_20260509.md:37:- `report_md/_gpt/KIMI_P8_TRACK_C_CLEANUP_EXECUTION_OR_DRYRUN_20260509.md`
paper1/reports/P8/audits/Claude/CLAUDE_P8_SELF_AUDIT_20260509.md:38:- `report_md/_gpt/KIMI_P8_TRACK_E_FINAL_BUNDLE_REFRESH_IF_NEEDED_20260509.md`
paper1/reports/P8/audits/Claude/CLAUDE_P8_SELF_AUDIT_20260509.md:39:- `report_md/_gpt/KIMI_P8_TRACK_J_FINAL_USER_HANDOFF_MAP_20260509.md`
paper1/reports/P8/audits/Claude/CLAUDE_P8_SELF_AUDIT_20260509.md:40:- `report_md/_gpt/KIMI_P8_SELF_AUDIT_20260509.md`
paper1/reports/P8/audits/Claude/CLAUDE_P8_SELF_AUDIT_20260509.md:41:- `report_md/_gpt/AGENT_SYNC_gpt.md`
eval_imagenet_analog.py:59:DEFAULT_JSON_PATH = asset_path("report_md/_gpt", "json", "imagenet_eval_results_gpt.json")
eval_imagenet_analog.py:60:DEFAULT_CSV_PATH = asset_path("report_md/_gpt", "csv", "imagenet_eval_results_gpt.csv")
eval_imagenet_analog.py:61:DEFAULT_MD_PATH = "report_md/_gpt/imagenet_eval_results_gpt.md"
eval_literature_profile.py:24:    profiles = load_device_profiles_json("report_md/_gpt/json_gpt/literature_fitted_profile.json")
eval_literature_profile.py:40:    output_path = Path("report_md/_gpt/json_gpt/literature_profile_eval.json")
PROJECT_INDEX.md:21:| Coordination | New dispatches: `dispatch-<topic>.md` under `report_md/_gpt/` | `CODEX_DISPATCH_20260417_cleanup_gpt.md` |
PROJECT_INDEX.md:33:├── AGENT_SYNC/             deprecated, replaced by report_md/_gpt/AGENT_SYNC_gpt.md
PROJECT_INDEX.md:224:### 6.2 `report_md/_gpt/` — live coordination
PROJECT_INDEX.md:252:To list all: `ls report_md/_gpt/*.md`.
PROJECT_INDEX.md:312:| `AGENT_SYNC/` (dir) | 7 files, 2026-04-15 artifact. Superseded by `report_md/_gpt/AGENT_SYNC_gpt.md` but kept in place — has a script caller noted in TIDY_MANIFEST | frozen (do not rename) |
train_tinyvit_ensemble.py:52:DEFAULT_REPORT_PATH = "report_md/_gpt/tinyvit_hybrid_dryrun_report_gpt.md"
train_tinyvit_ensemble.py:54:DEFAULT_RESULTS_JSON_PATH = asset_path("report_md/_gpt", "json", "tinyvit_results_gpt.json")
train_tinyvit_ensemble.py:55:DEFAULT_RESULTS_CSV_PATH = asset_path("report_md/_gpt", "csv", "tinyvit_results_gpt.csv")
train_tinyvit_ensemble.py:56:DEFAULT_RESULTS_MD_PATH = "report_md/_gpt/tinyvit_results_gpt.md"
paper1/reports/P7/KIMI/KIMI_P7_TRACK_E_REMOTE107_WORK2_GATE_20260509.md:112:`report_md/_gpt/REMOTE_107_PHASE_P7_CORRECTED_NOISE_AND_METADATA_TASKLIST_20260509.md`
REPRODUCIBILITY.md:14:- `report_md/_gpt/json_gpt/` — Fitted device-profile JSONs (Zhang2025 OPECT, Vincze2025 standard, and measured-device summaries).
REPRODUCIBILITY.md:47:| OPECT zero-shot 88.53±0.08% | `python eval_measured_profile.py --profile report_md/_gpt/json_gpt/doctor_measured_profiles.json` | Ensemble HAT ckpt |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:26:| P8 reports | `report_md/_gpt/KIMI_P8_TRACK_*_20260509.md`, `KIMI_P8_SELF_AUDIT_20260509.md` |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:27:| Coordination | `broadcast.md`, `report_md/_gpt/AGENT_SYNC_gpt.md`, `CLAUDE_TASK_gpt.md` if the repo tracks coordination state |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:92:  report_md/_gpt/KIMI_P8_TRACK_A_NARRATIVE_DESLOP_REWRITE_20260509.md \
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:93:  report_md/_gpt/KIMI_P8_TRACK_B_APPENDIX_TEXT_AND_TABLE_CONSISTENCY_20260509.md \
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:94:  report_md/_gpt/KIMI_P8_TRACK_C_CLEANUP_EXECUTION_OR_DRYRUN_20260509.md \
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:95:  report_md/_gpt/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md \
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:96:  report_md/_gpt/KIMI_P8_TRACK_E_FINAL_BUNDLE_REFRESH_IF_NEEDED_20260509.md \
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:97:  report_md/_gpt/KIMI_P8_TRACK_F_REMOTE105_INGESTION_READY_PACKET_20260509.md \
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:98:  report_md/_gpt/KIMI_P8_TRACK_G_REMOTE107_WORK2_READY_PACKET_20260509.md \
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:99:  report_md/_gpt/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md \
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:100:  report_md/_gpt/KIMI_P8_TRACK_I_LOCAL_GPU_AND_WORK2_OPTIONAL_QUEUE_20260509.md \
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:101:  report_md/_gpt/KIMI_P8_TRACK_J_FINAL_USER_HANDOFF_MAP_20260509.md \
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:102:  report_md/_gpt/KIMI_P8_SELF_AUDIT_20260509.md
```

## Pattern `paper2_aihwkit_baseline`

```text
README_REPRODUCIBILITY_PAPER1.md:71:paper2_aihwkit_baseline/PCM_PROTOCOL.md
README_REPRODUCIBILITY_PAPER1.md:83:paper2_aihwkit_baseline/r11d4_train_pcm.py
README_REPRODUCIBILITY_PAPER1.md:84:paper2_aihwkit_baseline/eval_aihwkit_fresh.py
README_REPRODUCIBILITY_PAPER1.md:85:paper2_aihwkit_baseline/eval_aihwkit_drift_extended.py
README_REPRODUCIBILITY_PAPER1.md:86:paper2_aihwkit_baseline/run_pcm_multi_seed_validation.sh
README_REPRODUCIBILITY_PAPER1.md:87:paper2_aihwkit_baseline/run_kimi_r11d_6bit_multiseed_20260430.sh
README_REPRODUCIBILITY_PAPER1.md:88:paper2_aihwkit_baseline/run_r11d7_pcm_4bit.sh
README_REPRODUCIBILITY_PAPER1.md:97:paper2_aihwkit_baseline/checkpoints/**/best.pt
README_REPRODUCIBILITY_PAPER1.md:98:paper2_aihwkit_baseline/checkpoints/**/last.pt
paper1/reports/P6/KIMI/KIMI_P6_TRACK_C_LOCAL_GPU_EXECUTION_REPORT_20260509.md:25:| Command | `r11d4_train_pcm.py --run-id r11d_6bit_pcm_seed123 --seed 123 --epochs 100 --batch-size 64 --lr 0.001 --wd 0.05 --momentum 0.0 --device cuda --workers 0 --save-dir paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123 --inp-res 0.015625 --out-res 0.015625 --modifier-std-dev 0.10 --early-stop-patience 10 --early-stop-min-delta 0.01` |
paper1/reports/P6/KIMI/KIMI_P6_TRACK_C_LOCAL_GPU_EXECUTION_REPORT_20260509.md:31:| Backup | `paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123_P6_BACKUP_20260509/` |
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:2:ideal_8bit_sigma010_aihwkit_baseline,paper2_aihwkit_baseline/checkpoints/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/ideal_8bit_sigma010_aihwkit_baseline/fresh_eval.json,1a0f9234677963522cd74cfcf8f47c8f30f6d2031aadbb3dfcbe643f912bb45a,978,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:3:ideal_8bit_sigma010_aihwkit_baseline,paper2_aihwkit_baseline/checkpoints/training_history.json,paper/latex_gpt/source_data/canonical_json/ideal_8bit_sigma010_aihwkit_baseline/training_history.json,b4bc4ba04563a5193f3c6771ed0af86f28eb6b771b5d12ed357869dd8a196a87,20232,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:4:pure_4bit_collapse,paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/pure_4bit_collapse/fresh_eval.json,bc02b808fb73356aebf0f00621d44f6ac7e4ab4c84627a57c3080a6a52537e49,6394,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:5:pure_4bit_collapse,paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/training_history.json,paper/latex_gpt/source_data/canonical_json/pure_4bit_collapse/training_history.json,b7d64161a91c8b6db60f6f1f9002e73c482cb11ee26e4c9e4654867ff1b9c61b,6600,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:7:pcm_8bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed123/drift_eval.json,82077b5b4a9dab3e5238c273d167deb4596feb25bb8986d7100512bee021a0ce,723,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:8:pcm_8bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/extended_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed123/extended_drift_eval.json,f9e5a92c05e98bfd36f6807a46f4482af6e8d459ac327300c95147a018bc2264,1504,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:9:pcm_8bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/fresh_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed123/fresh_drift_eval.json,fc9f1cd6ffbd859546f0c82c07bea68d15612ef348817e9d39f9e4edad122435,23642,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:10:pcm_8bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed123/fresh_eval.json,1387d021694f524c005d02de6412c650947150b15c5be938864c86a91860fe78,21408,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:11:pcm_8bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/training_history.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed123/training_history.json,81e5ac47b306de4dd31d392636c54bf663d3093e4eb4ec84d85c1ab938c0d4f0,22282,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:12:pcm_8bit_seed456,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456/drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed456/drift_eval.json,24833d5d977e4b83467de6259da59d454749ab87076a3c139f72a78ff77dd859,723,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:13:pcm_8bit_seed456,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456/extended_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed456/extended_drift_eval.json,c7d0e047ba7cfa83ace9ad69512029b32e513386dce61af15c57aaa8d8b410fb,1501,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:14:pcm_8bit_seed456,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456/fresh_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed456/fresh_drift_eval.json,16886e4727e7f88a59b2f7c47139508ec0cf97f0e8f3929dd443b2f0b77542d3,23640,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:15:pcm_8bit_seed456,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed456/fresh_eval.json,23b42a8cf363f7d67a8da010b189040d02ae5697573d6123ca139c7fa71a4800,21411,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:16:pcm_8bit_seed456,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456/training_history.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed456/training_history.json,bd699041c26af7c698be6edd913847fa5b4874fd69b4ba5cec0da626e74203c9,22189,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:17:pcm_8bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed789/drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed789/drift_eval.json,e5f7c96b14b8fc4ecbfd6739a0a39ef444140e33d18e7ad4336b7e37f11a359a,723,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:18:pcm_8bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed789/extended_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed789/extended_drift_eval.json,082aa22703975ce5f57983c235b538382559fcc07f5df80161d7d8a5a0580526,1501,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:19:pcm_8bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed789/fresh_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed789/fresh_drift_eval.json,b82e1edb21acaab809802ba6333abb6cd27f10c2d71031c96911211cf5ac711a,23630,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:20:pcm_8bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed789/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed789/fresh_eval.json,de88891eb323b27d080b22355cc135367a5275f3ebeaf90fd34517d8bbc067e9,21413,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:21:pcm_8bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed789/training_history.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed789/training_history.json,a8d600c06f188449b49a4c226d8c1270efc46829e268058a8a880a3445165863,22262,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:22:pcm_6bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123/drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed123/drift_eval.json,32c77b8e419f65dcd72bfc088473b70f22aceaba5ff15d6a89c6edbe82cb1db7,721,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:23:pcm_6bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed123/fresh_eval.json,4dbdfede9a1b007d3cd99b3cca9738c974f1d9c0959376cbbb0f1f18e731afd8,21406,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:24:pcm_6bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123/training_history.json,paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed123/training_history.json,f529ad7c4653634a6ca99430abed252d3036cc5ee3825622678237cf57126af6,22184,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:25:pcm_6bit_seed456_full100,paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456_full100/drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed456_full100/drift_eval.json,129cc6097c8b58493f39f04e8d866a655c2ca1356348f11c8e6a4e99529a702e,728,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:26:pcm_6bit_seed456_full100,paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456_full100/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed456_full100/fresh_eval.json,a972fccda6cccf8a4d6175ea678e6475336616d2a1c001316c17c90c7a9a4423,21414,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:27:pcm_6bit_seed456_full100,paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456_full100/training_history.json,paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed456_full100/training_history.json,10f1ae07637610794117f942d7e4622e56757c87a90602ece6a47e518502ae99,22230,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:28:pcm_6bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed789/drift_eval.json,bc91127b1c2a6ff50dc56942971a8de76eef748f99b533f927e801f98c268abc,721,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:29:pcm_6bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed789/fresh_eval.json,c9c63c903275baa4b53670484afc753236c0ac0deb823f5f5884d9939a84cf8d,21412,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:30:pcm_6bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/training_history.json,paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed789/training_history.json,9e2f9b120d7b7219dfea58d1d659989890405cb205a9c61e7a77d2b576bcfa82,22195,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:31:pcm_4bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed123/drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed123/drift_eval.json,29238ff42a7715a0e86fe79e355f955555f33df73c3d4ee9def628e8e34a122d,719,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:32:pcm_4bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed123/extended_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed123/extended_drift_eval.json,83aefc8264afa2a661ef6f07a3f45444a7a04acf70a9764388c83a848d39b01e,1500,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:33:pcm_4bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed123/fresh_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed123/fresh_drift_eval.json,a74fce7b5b2be29c4d3725368c64401266a837076a8d77e659960b6c53326657,23631,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:34:pcm_4bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed123/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed123/fresh_eval.json,e1308c05eb69bfe5075df087634f8ee64fc4b43852f942d95d512cfb023e0a5a,21404,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:35:pcm_4bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed123/training_history.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed123/training_history.json,06387b9ee4d5efae243c13fe7bd28103f9c32d52e2b3bc45328eb989a616096d,22251,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:36:pcm_4bit_seed456_clean,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed456_clean/drift_eval.json,451a7685f1fef230c1bb3a3b6bc9a97a14892c3fb6dde2317522467014d33b7d,725,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:37:pcm_4bit_seed456_clean,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/extended_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed456_clean/extended_drift_eval.json,7b8a6b5e9a49f4ff9fc662c61176493ba87569049732ee0894506e922d68df69,1506,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:38:pcm_4bit_seed456_clean,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/fresh_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed456_clean/fresh_drift_eval.json,8f610064a3e3e1ff11404d39ae40150d2100b9a9085319f5bd018ea8f533d054,23638,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:39:pcm_4bit_seed456_clean,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed456_clean/fresh_eval.json,01ec26488a405d091428d884a9a4e05852a469ccf67c0f327646c80afbdff5f5,21414,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:40:pcm_4bit_seed456_clean,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/training_history.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed456_clean/training_history.json,01c34ddd6ba6229e72147ccc0266aa617c17eda7e9c511940d65a519086e6fd1,22269,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:41:pcm_4bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789/drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed789/drift_eval.json,a411ad89728424af5bd9045df41de610810b9d7b3518adedfb0da9a4f2d9200b,719,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:42:pcm_4bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789/extended_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed789/extended_drift_eval.json,09ff89e5d8ec5d1e050bcc457edf54bd8a85a40b888d1e1fd689ee60c556e7a6,1499,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:43:pcm_4bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789/fresh_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed789/fresh_drift_eval.json,3f86574dbbe39740a098df46195a338fb9de2e9c4591519c6b79f272d3988598,23625,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:44:pcm_4bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed789/fresh_eval.json,9ff017ed7261053ccb428271a49b4122208342a74c78c3fa3b525782453a2bed,21407,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:45:pcm_4bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789/training_history.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed789/training_history.json,acb204b6a10fc4d3fa57990682af082ae3451fb1499e0ce49e2e5eabea3adf55,22235,copied
paper1/reports/P6/KIMI/KIMI_P6_TRACK_A_EVIDENCE_GAP_LEDGER_20260509.md:21:| 9 | Appendix/defense-only: 5-bit PCM non-frontier | `r11d_5bit_pcm_seed*` checkpoints | `paper2_aihwkit_baseline/checkpoints/r11d_5bit_pcm_seed*/` | 3+ seeds | fresh_mean | **Complete** | None | `exclude/superseded` |
paper1/reports/P6/KIMI/KIMI_P6_TRACK_A_EVIDENCE_GAP_LEDGER_20260509.md:139:| Evidence | `paper2_aihwkit_baseline/checkpoints/r11d_5bit_pcm_seed*/` |
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pure_4bit_collapse/fresh_eval.json:2:  "checkpoint": "paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/best.pt",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_4bit_seed789/training_history.json:915:    "save_dir": "/home/qiaosir/projects/compute_vit/paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_4bit_seed789/training_history.json:949:      "save_dir": "/home/qiaosir/projects/compute_vit/paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789",
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/pcm_6bit_seed123/training_history.json:915:    "save_dir": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123",
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/pcm_6bit_seed123/training_history.json:949:      "save_dir": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/ideal_8bit_sigma010_aihwkit_baseline/training_history.json:914:    "save_dir": "paper2_aihwkit_baseline/checkpoints",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:10:    "paper2_aihwkit_baseline/checkpoints/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:11:    "paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:13:    "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:14:    "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:15:    "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:16:    "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:17:    "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:18:    "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:19:    "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed789/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:20:    "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed789/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:21:    "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed789/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:22:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:23:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:24:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:25:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:26:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:27:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:28:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed457/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:29:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed457/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:30:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed457/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:31:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:32:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:33:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:34:    "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed123/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:35:    "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed123/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:36:    "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed123/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:37:    "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:38:    "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:39:    "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:40:    "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:41:    "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:42:    "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789/drift_eval.json"
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_6bit_seed123/training_history.json:564:    "save_dir": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_6bit_seed123/training_history.json:598:      "save_dir": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_6bit_seed457/fresh_eval.json:2:  "checkpoint": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed457/best.pt",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_8bit_seed123/fresh_drift_eval.json:2:  "checkpoint": "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/best.pt",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_6bit_seed789/training_history.json:501:    "save_dir": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_6bit_seed789/training_history.json:535:      "save_dir": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789",
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:29:| `paper2_aihwkit_baseline/` | KEEP_LOCAL_DATA | 6.9 GB | AIHWKit experiments | ❌ NO | ❌ NO |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:80:| `paper2_aihwkit_baseline/checkpoints/` | ~6 GB | KEEP_LOCAL_DATA | Keep locally, never commit |
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/pcm_6bit_seed789/fresh_eval.json:2:  "checkpoint": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/best.pt",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_6bit_seed457/drift_eval.json:2:  "checkpoint": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed457/best.pt",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_8bit_seed123/fresh_eval.json:2:  "checkpoint": "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/best.pt",
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/pcm_6bit_seed456_full100/drift_eval.json:2:  "checkpoint": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456_full100/best.pt",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_8bit_seed789/fresh_drift_eval.json:2:  "checkpoint": "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed789/best.pt",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_4bit_seed123/extended_drift_eval.json:2:  "checkpoint": "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed123/best.pt",
ROOT_REORG_PLAN_20260509.md:112:paper2_aihwkit_baseline/ -> work2/aihwkit_pcm/
ROOT_REORG_PLAN_20260509.md:118:paper2_aihwkit_baseline/checkpoints/ -> data_local/checkpoints/work2_aihwkit/
ROOT_REORG_PLAN_20260509.md:119:paper2_aihwkit_baseline/data/ -> data_local/datasets/work2_aihwkit/
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:33:| Large data/checkpoints | `checkpoints/`, `data/`, `paper2_aihwkit_baseline/checkpoints/`, any `.pt`, `.pth`, `.ckpt` |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:34:| Raw local experiment tree | most untracked `paper2_aihwkit_baseline/*` scripts/figures unless separately approved for Work-2 |
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/pcm_6bit_seed456_full100/training_history.json:915:    "save_dir": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456_full100",
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/pcm_6bit_seed456_full100/training_history.json:949:      "save_dir": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456_full100",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_4bit_seed456_clean/fresh_eval.json:2:  "checkpoint": "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/best.pt",
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/pcm_6bit_seed789/training_history.json:915:    "save_dir": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789",
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/pcm_6bit_seed789/training_history.json:949:      "save_dir": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789",
WORKSPACE_LAYOUT_V2_20260509.md:206:| `paper2_aihwkit_baseline/` | Work-2 AIHWKit/PCM | `work2/aihwkit_pcm/` |
WORKSPACE_LAYOUT_V2_20260509.md:235:- Move `paper2/` and `paper2_aihwkit_baseline/` into `work2/`.
```

## Pattern `paper2/`

```text
WORKSPACE_LAYOUT_V2_20260509.md:205:| `paper2/` | Work-2 KV-cache | `work2/kv_cache/` |
WORKSPACE_LAYOUT_V2_20260509.md:235:- Move `paper2/` and `paper2_aihwkit_baseline/` into `work2/`.
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:130:| `paper2/REMOTE_107_KV_TASKLIST_20260429.md` | 1 file | Old tasklist |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:131:| `paper2/REMOTE_NO_PUSH_RETURN_PROTOCOL_20260429.md` | 1 file | Old protocol |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:30:| `paper2/` | KEEP_ACTIVE | 720 KB | Work-2 scripts and docs | ❌ NO | ❌ NO |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:67:| `paper2/REMOTE_*.md` | QUARANTINE_CANDIDATE | ~10 KB each | Old remote files | ✅ YES | ❌ NO |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:134:mv paper2/REMOTE_107_KV_TASKLIST_20260429.md _quarantine_20260509/old_remote_files/ 2>/dev/null
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:135:mv paper2/REMOTE_NO_PUSH_RETURN_PROTOCOL_20260429.md _quarantine_20260509/old_remote_files/ 2>/dev/null
ROOT_REORG_PLAN_20260509.md:111:paper2/ -> work2/kv_cache/
paper1/reports/P8/KIMI/KIMI_P8_TRACK_C_CLEANUP_EXECUTION_OR_DRYRUN_20260509.md:43:| `old_remote_files/` | top-level old intercom/tasklist files, old GPU schedule, old `gpu_watcher.sh`, old `paper2/REMOTE_*.md` |
report_md/_gpt/theory_memos/GEMINI_PAPER2_EXP_DESIGN_20260420.md:6:**Sources:** `train_tinyvit_ensemble.py`, `scripts/_gpt/run_tinyvit_groupwise_nl_comp.py`, `analog_layers.py`, `GEMINI_STRUCTURAL_LIMIT_FORMAL_20260420.md` (G-GG1), `GEMINI_HIGHER_ORDER_NL_DESIGN_20260420.md` (G-GG2), `GEMINI_PATHWAY_DECOMPOSITION_20260420.md` (G-GG3), `GEMINI_FIRST_ORDER_LIMIT_20260420.md` (G-GG4), Paper-2 skeleton (`paper/paper2/draft_v0/SKELETON.md`).
report_md/_gpt/theory_memos/GEMINI_PAPER2_EXP_DESIGN_20260420.md:265:All fresh-instance comparisons use the protocol from Paper-1 (see `paper/paper2/draft_v0/03_methods.md`, §Statistical Treatment):
report_md/_gpt/theory_memos/GEMINI_CONFERENCE_FIT_V2_20260420.md:6:**Sources:** `GEMINI_STRUCTURAL_LIMIT_FORMAL_20260420.md` (G-GG1), `GEMINI_HIGHER_ORDER_NL_DESIGN_20260420.md` (G-GG2), `GEMINI_PAPER2_ARCH_MEMO_20260420.md` (G-GG5), `GEMINI_PAPER2_EXP_DESIGN_20260420.md` (G-GG6), Paper-2 skeleton (`paper/paper2/draft_v0/SKELETON.md`), Paper-1 (`paper/latex_gpt/main.tex` and `sections/06_discussion.tex`).
broadcast.md:3575:- Old paper2/R11D run scripts moved to archive.
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:227:report_md/_gpt/AGENT_SYNC_gpt.md:29413:- `/home/qiaosir` — 80+ files (scripts/_gpt/, release_artifacts/, paper2/results/)
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:503:WORKSPACE_LAYOUT_V2_20260509.md:235:- Move `paper2/` and `paper2_aihwkit_baseline/` into `work2/`.
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:506:## Pattern `paper2/`
report_md/_gpt/theory_memos/GEMINI_PAPER2_ARCH_MEMO_20260420.md:6:**Sources:** `GEMINI_STRUCTURAL_LIMIT_FORMAL_20260420.md` (G-GG1), `GEMINI_HIGHER_ORDER_NL_DESIGN_20260420.md` (G-GG2), `GEMINI_PATHWAY_DECOMPOSITION_20260420.md` (G-GG3), `GEMINI_FIRST_ORDER_LIMIT_20260420.md` (G-GG4), Paper-2 skeleton (`paper/paper2/draft_v0/SKELETON.md`), and Paper-1 main text (`paper/latex_gpt/main.tex`).
report_md/_gpt/theory_memos/GEMINI_PAPER2_ARCH_MEMO_20260420.md:163:1. **Adopt the R-A skeleton** (`paper/paper2/draft_v0/SKELETON.md`) as the scaffold. Do not pivot to R-B or R-C as primary narratives.
report_md/_gpt/AGENT_SYNC_gpt.md:23399:- **Paper-2 abstract locked-number scrub**: Kimi must replace `30.53 ± 7.07%` in `paper/paper2/draft_v0/00_abstract.md` with `[J1a result, TBD]` — Rule B protects locked numbers during loop.
report_md/_gpt/AGENT_SYNC_gpt.md:23450:  - only `_gpt/`, `paper/thesis_cn/`, and `paper/paper2/skeleton_v0/` support work assigned
report_md/_gpt/AGENT_SYNC_gpt.md:23577:- §0 forbidden list extended: `paper/paper2/draft_v0/*` (pending route ratification) + `skeleton_v0/` locked numbers.
report_md/_gpt/AGENT_SYNC_gpt.md:24219:- **STOP CONDITION TRIGGERED.** `paper/paper2/skeleton_v1/` directory does not exist yet.
report_md/_gpt/AGENT_SYNC_gpt.md:24978:- Work 2 files live in `paper/paper2/skeleton_v1/*`, `paper/thesis_cn/chapter_6_*.tex`, `chapter_7_*.tex` (all new).
report_md/_gpt/AGENT_SYNC_gpt.md:25070:2. **One rule** — 5 frozen files, nothing else locked. Rule B extensions to paper2/draft_v0 scrapped.
report_md/_gpt/AGENT_SYNC_gpt.md:27632:- W1 (10 days): KV-cache analog wrapper code + 3 smoke tests on `paper2/src/`
report_md/_gpt/AGENT_SYNC_gpt.md:27659:**Git push status:** earlier `git push origin master` confirmed REJECTED (2GB pack limit; historical 445MB blobs). Main repo stays local; public mirror via handoff repo. Work 2 code in `paper2/` will need its own lightweight export path when ready.
report_md/_gpt/AGENT_SYNC_gpt.md:27727:- `paper2/README.md`
report_md/_gpt/AGENT_SYNC_gpt.md:27728:- `paper2/WORK2_TESTBED_DECISION_20260425.md`
report_md/_gpt/AGENT_SYNC_gpt.md:27729:- `paper2/WORK2_ARCHITECTURAL_MAPPING_SPEC_20260425.md`
report_md/_gpt/AGENT_SYNC_gpt.md:27730:- `paper2/WORK2_BENCHMARK_SUITE_20260425.md`
report_md/_gpt/AGENT_SYNC_gpt.md:27740:**Next:** Codex can start W1 scaffold under `paper2/src/` and `tests/test_w2_*.py` unless Paper 1 trigger work arrives.
report_md/_gpt/AGENT_SYNC_gpt.md:27749:- `paper2/src/analog_kv_cache.py`
report_md/_gpt/AGENT_SYNC_gpt.md:27750:- `paper2/src/llm_hybrid.py`
report_md/_gpt/AGENT_SYNC_gpt.md:27751:- `paper2/src/eval_llm_kv_cache.py`
report_md/_gpt/AGENT_SYNC_gpt.md:27752:- `paper2/src/train_llm_hybrid.py`
report_md/_gpt/AGENT_SYNC_gpt.md:27772:- `paper2/src/smoke_pythia_hybrid.py`
report_md/_gpt/AGENT_SYNC_gpt.md:27773:- `paper2/src/train_llm_hybrid.py`
report_md/_gpt/AGENT_SYNC_gpt.md:27774:- `paper2/src/llm_hybrid.py`
report_md/_gpt/AGENT_SYNC_gpt.md:27827:Summary JSON: `paper2/results/w2_scoped_probe_summary_20260425.json`.
report_md/_gpt/AGENT_SYNC_gpt.md:27837:Independent review correctly flagged that previous W2 smoke logs did not provide post-training independent eval, lacked full config logging/seed, and trained on pad tokens. Codex patched `paper2/src/train_llm_hybrid.py` to add seed, full argv/config logging, pad label masking, eval-before/eval-after, and `pre_update_loss` naming. Trusted 6-job matrix launched under corrected protocol.
report_md/_gpt/AGENT_SYNC_gpt.md:28252:Codex added `--eval-text-set {train,heldout}` to `paper2/src/train_llm_hybrid.py` so W2 smoke training can evaluate on a disjoint fixed text set instead of reusing the four training sentences. Syntax check passed. Launched seed1234 held-out+fresh-D2D pilot for the two viable routes, `all` and `mlp`, with the same low-noise protocol and 10 fresh D2D instances x 5 C2C repeats. Logs: `logs/_gpt/w2_heldout_freshd2d_{all,mlp}_n005002_lb1000_seed1234_20260426_112604.log`.
report_md/_gpt/AGENT_SYNC_gpt.md:28309:`paper2/src/eval_llm_kv_cache.py` now loads Pythia, captures real `past_key_values`, supports `DynamicCache`, passes K/V tensors through `AnalogKVCache`, and writes reconstruction metrics. Low-noise results: last-layer maxlen64 effective seq 19, 10 D2D instances x 5 reads, KV relative MSE `2.8038e-5`; all-layer short CUDA smoke KV relative MSE `2.7559e-5`. This supports analog KV-cache storage as the strongest W2 route, but it is still offline tensor reconstruction, not end-to-end perplexity.
report_md/_gpt/AGENT_SYNC_gpt.md:29413:- `/home/qiaosir` — 80+ files (scripts/_gpt/, release_artifacts/, paper2/results/)
report_md/_gpt/AGENT_SYNC_gpt.md:31171:- 107 = Work-2 KV-cache exploration lane, controlled by `paper2/REMOTE_107_KV_TASKLIST_20260429.md`.
report_md/_gpt/AGENT_SYNC_gpt.md:31721:- Old paper2/R11D run scripts moved to archive.
paper2/results/launch_llm_parallel_20260425_220515.sh:6:mkdir -p logs/_gpt paper2/results
paper2/results/launch_llm_parallel_20260425_220515.sh:11:  nohup "$PY" -u paper2/src/train_llm_hybrid.py "$@" > "$log" 2>&1 &
paper2/results/launch_llm_parallel_20260425_220515.sh:13:  echo "$pid" > "paper2/results/${name}.pid"
paper2/WORK2_ARCHITECTURAL_MAPPING_SPEC_20260425.md:65:- `paper2/src/analog_kv_cache.py`: cache storage/read noise primitive.
paper2/WORK2_ARCHITECTURAL_MAPPING_SPEC_20260425.md:66:- `paper2/src/llm_hybrid.py`: Pythia/GPT-NeoX hybrid conversion.
paper2/WORK2_ARCHITECTURAL_MAPPING_SPEC_20260425.md:67:- `paper2/src/train_llm_hybrid.py`: short finetune/smoke training entry point.
paper2/WORK2_ARCHITECTURAL_MAPPING_SPEC_20260425.md:68:- `paper2/src/eval_llm_kv_cache.py`: perplexity and sliding-window decode eval.
paper2/results/run_llm_scoped_nonnoise_20260425_221532.sh:6:mkdir -p logs/_gpt paper2/results
paper2/results/run_llm_scoped_nonnoise_20260425_221532.sh:12:  ("$PY" -u paper2/src/train_llm_hybrid.py     --model EleutherAI/pythia-410m-deduped     --device cuda     --dtype float32     --local-files-only     --hybrid     --analog-scope "$scope"     --high-precision-analog     --train-scope last_block     --max-length 64     --steps 200     --lr 1e-5 > "$log" 2>&1; code=$?; echo "$code" > "paper2/results/${name}.exit"; echo "[exit] $name $code") &
paper2/results/run_llm_scoped_nonnoise_20260425_221532.sh:13:  echo "$!" > "paper2/results/${name}.pid"
paper2/results/run_llm_scoped_nonnoise_20260425_221532.sh:25:  for p in paper2/results/w2_llm_scope_*_${RUN_ID}.pid; do pid=$(cat "$p"); if kill -0 "$pid" 2>/dev/null; then live=1; fi; done
paper2/results/run_w2_heldout_freshd2d_all_mlp_seeds456789_20260426_112930.sh:7:mkdir -p logs/_gpt paper2/results
paper2/results/run_w2_heldout_freshd2d_all_mlp_seeds456789_20260426_112930.sh:18:    timeout 5400 "$PY" -u paper2/src/train_llm_hybrid.py \
paper2/results/run_w2_heldout_freshd2d_all_mlp_seeds456789_20260426_112930.sh:41:    echo "$code" > "paper2/results/${name}.exit"
paper2/results/run_w2_heldout_freshd2d_all_mlp_seeds456789_20260426_112930.sh:45:  echo "$!" > "paper2/results/${name}.pid"
paper2/results/run_llm_next_matrix_20260425_222439.sh:6:mkdir -p logs/_gpt paper2/results
paper2/results/run_llm_next_matrix_20260425_222439.sh:11:  ("$PY" -u paper2/src/train_llm_hybrid.py "$@" > "$log" 2>&1; code=$?; echo "$code" > "paper2/results/${name}.exit"; echo "[exit] $name $code") &
paper2/results/run_llm_next_matrix_20260425_222439.sh:12:  echo "$!" > "paper2/results/${name}.pid"
paper2/results/run_llm_next_matrix_20260425_222439.sh:32:  for p in paper2/results/w2_llm_*_${RUN_ID}.pid; do pid=$(cat "$p"); if kill -0 "$pid" 2>/dev/null; then live=1; fi; done
paper2/README.md:15:Implementation will live in `paper2/src/`. Draft writing owned by Kimi will live in `paper2/sections/` and `paper2/supplementary/`.
paper2/results/run_llm_parallel_wait_20260425_220737.sh:6:mkdir -p logs/_gpt paper2/results
paper2/results/run_llm_parallel_wait_20260425_220737.sh:11:  ("$PY" -u paper2/src/train_llm_hybrid.py "$@" > "$log" 2>&1; code=$?; echo "$code" > "paper2/results/${name}.exit"; echo "[exit] $name $code") &
paper2/results/run_llm_parallel_wait_20260425_220737.sh:12:  echo "$!" > "paper2/results/${name}.pid"
paper2/results/run_llm_parallel_wait_20260425_220737.sh:25:  for p in paper2/results/w2_llm_*_${RUN_ID}.pid; do pid=$(cat "$p"); if kill -0 "$pid" 2>/dev/null; then live=1; fi; done
paper2/results/run_w2_low_noise_long_20260426_105917.sh:7:mkdir -p logs/_gpt paper2/results
paper2/results/run_w2_low_noise_long_20260426_105917.sh:17:    timeout 5400 "$PY" -u paper2/src/train_llm_hybrid.py \
paper2/results/run_w2_low_noise_long_20260426_105917.sh:37:    echo "$code" > "paper2/results/${name}.exit"
paper2/results/run_w2_low_noise_long_20260426_105917.sh:40:  echo "$!" > "paper2/results/${name}.pid"
paper2/results/run_llm_noise_source_20260425_221702.sh:6:mkdir -p logs/_gpt paper2/results
paper2/results/run_llm_noise_source_20260425_221702.sh:16:  ("$PY" -u paper2/src/train_llm_hybrid.py     --model EleutherAI/pythia-410m-deduped     --device cuda     --dtype float32     --local-files-only     --hybrid     --analog-scope "$scope"     --high-precision-analog     --noise-enabled     --sigma-d2d "$d2d"     --sigma-c2c "$c2c"     --resample-every "$resample"     --train-scope last_block     --max-length 64     --steps 200     --lr 5e-6 > "$log" 2>&1; code=$?; echo "$code" > "paper2/results/${name}.exit"; echo "[exit] $name $code") &
paper2/results/run_llm_noise_source_20260425_221702.sh:17:  echo "$!" > "paper2/results/${name}.pid"
paper2/results/run_llm_noise_source_20260425_221702.sh:30:  for p in paper2/results/w2_llm_scope_*_${RUN_ID}.pid; do pid=$(cat "$p"); if kill -0 "$pid" 2>/dev/null; then live=1; fi; done
paper2/results/run_llm_low_noise_threshold_20260425_221843.sh:6:mkdir -p logs/_gpt paper2/results
paper2/results/run_llm_low_noise_threshold_20260425_221843.sh:15:  ("$PY" -u paper2/src/train_llm_hybrid.py     --model EleutherAI/pythia-410m-deduped     --device cuda     --dtype float32     --local-files-only     --hybrid     --analog-scope "$scope"     --high-precision-analog     --noise-enabled     --sigma-d2d "$d2d"     --sigma-c2c "$c2c"     --resample-every 10     --train-scope last_block     --max-length 64     --steps 200     --lr 5e-6 > "$log" 2>&1; code=$?; echo "$code" > "paper2/results/${name}.exit"; echo "[exit] $name $code") &
paper2/results/run_llm_low_noise_threshold_20260425_221843.sh:16:  echo "$!" > "paper2/results/${name}.pid"
paper2/results/run_llm_low_noise_threshold_20260425_221843.sh:34:  for p in paper2/results/w2_llm_scope_*_${RUN_ID}.pid; do pid=$(cat "$p"); if kill -0 "$pid" 2>/dev/null; then live=1; fi; done
paper2/results/run_llm_scoped_noise_20260425_221406.sh:6:mkdir -p logs/_gpt paper2/results
paper2/results/run_llm_scoped_noise_20260425_221406.sh:12:  ("$PY" -u paper2/src/train_llm_hybrid.py     --model EleutherAI/pythia-410m-deduped     --device cuda     --dtype float32     --local-files-only     --hybrid     --analog-scope "$scope"     --high-precision-analog     --noise-enabled     --sigma-d2d 0.05     --sigma-c2c 0.02     --resample-every 10     --train-scope last_block     --max-length 64     --steps 200     --lr 5e-6 > "$log" 2>&1; code=$?; echo "$code" > "paper2/results/${name}.exit"; echo "[exit] $name $code") &
paper2/results/run_llm_scoped_noise_20260425_221406.sh:13:  echo "$!" > "paper2/results/${name}.pid"
paper2/results/run_llm_scoped_noise_20260425_221406.sh:25:  for p in paper2/results/w2_llm_scope_*_${RUN_ID}.pid; do pid=$(cat "$p"); if kill -0 "$pid" 2>/dev/null; then live=1; fi; done
paper2/results/run_llm_trusted_protocol_20260425_222725.sh:6:mkdir -p logs/_gpt paper2/results
paper2/results/run_llm_trusted_protocol_20260425_222725.sh:11:  ("$PY" -u paper2/src/train_llm_hybrid.py "$@" > "$log" 2>&1; code=$?; echo "$code" > "paper2/results/${name}.exit"; echo "[exit] $name $code") &
paper2/results/run_llm_trusted_protocol_20260425_222725.sh:12:  echo "$!" > "paper2/results/${name}.pid"
paper2/results/run_llm_trusted_protocol_20260425_222725.sh:32:  for p in paper2/results/w2_trusted_*_${RUN_ID}.pid; do pid=$(cat "$p"); if kill -0 "$pid" 2>/dev/null; then live=1; fi; done
paper2/results/run_w2_low_noise_long_seed789_20260426_110831.sh:7:mkdir -p logs/_gpt paper2/results
paper2/results/run_w2_low_noise_long_seed789_20260426_110831.sh:17:    timeout 5400 "$PY" -u paper2/src/train_llm_hybrid.py \
paper2/results/run_w2_low_noise_long_seed789_20260426_110831.sh:37:    echo "$code" > "paper2/results/${name}.exit"
paper2/results/run_w2_low_noise_long_seed789_20260426_110831.sh:41:  echo "$!" > "paper2/results/${name}.pid"
paper2/results/run_w2_heldout_freshd2d_pilot_seed1234_20260426_112604.sh:7:mkdir -p logs/_gpt paper2/results
paper2/results/run_w2_heldout_freshd2d_pilot_seed1234_20260426_112604.sh:17:    timeout 5400 "$PY" -u paper2/src/train_llm_hybrid.py \
paper2/results/run_w2_heldout_freshd2d_pilot_seed1234_20260426_112604.sh:40:    echo "$code" > "paper2/results/${name}.exit"
paper2/results/run_w2_heldout_freshd2d_pilot_seed1234_20260426_112604.sh:44:  echo "$!" > "paper2/results/${name}.pid"
paper2/results/launch_llm_parallel_20260425_220453.sh:5:mkdir -p logs/_gpt paper2/results
paper2/results/launch_llm_parallel_20260425_220453.sh:10:  nohup "$PY" -u paper2/src/train_llm_hybrid.py "$@" > "$log" 2>&1 &
paper2/results/launch_llm_parallel_20260425_220453.sh:12:  echo "$pid" > "paper2/results/${name}.pid"
paper2/results/run_w2_fresh_d2d_all_mlp_seeds456789_20260426_111745.sh:7:mkdir -p logs/_gpt paper2/results
paper2/results/run_w2_fresh_d2d_all_mlp_seeds456789_20260426_111745.sh:18:    timeout 5400 "$PY" -u paper2/src/train_llm_hybrid.py \
paper2/results/run_w2_fresh_d2d_all_mlp_seeds456789_20260426_111745.sh:40:    echo "$code" > "paper2/results/${name}.exit"
paper2/results/run_w2_fresh_d2d_all_mlp_seeds456789_20260426_111745.sh:44:  echo "$!" > "paper2/results/${name}.pid"
paper2/results/run_w2_low_noise_long_seed456_20260426_110401.sh:7:mkdir -p logs/_gpt paper2/results
paper2/results/run_w2_low_noise_long_seed456_20260426_110401.sh:17:    timeout 5400 "$PY" -u paper2/src/train_llm_hybrid.py \
paper2/results/run_w2_low_noise_long_seed456_20260426_110401.sh:37:    echo "$code" > "paper2/results/${name}.exit"
paper2/results/run_w2_low_noise_long_seed456_20260426_110401.sh:41:  echo "$!" > "paper2/results/${name}.pid"
paper2/results/run_w2_fresh_d2d_pilot_seed1234_20260426_111403.sh:7:mkdir -p logs/_gpt paper2/results
paper2/results/run_w2_fresh_d2d_pilot_seed1234_20260426_111403.sh:17:    timeout 5400 "$PY" -u paper2/src/train_llm_hybrid.py \
paper2/results/run_w2_fresh_d2d_pilot_seed1234_20260426_111403.sh:39:    echo "$code" > "paper2/results/${name}.exit"
paper2/results/run_w2_fresh_d2d_pilot_seed1234_20260426_111403.sh:43:  echo "$!" > "paper2/results/${name}.pid"
paper/paper2/skeleton_v1/SKELETON.md:5:**Supersedes:** `paper/paper2/skeleton_v0/*` (frozen reference)
```

## Pattern `paper/thesis`

```text
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:23:| `paper/thesis/` | KEEP_ACTIVE | ~50 MB | Thesis chapters | ❌ NO | ❌ NO |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:24:| `paper/thesis_cn/` | KEEP_ACTIVE | ~5 MB | Chinese thesis draft | ❌ NO | ❌ NO |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:101:| `paper/thesis_cn/*.toc` | LaTeX TOC output | `rm -f paper/thesis_cn/*.toc` |
paper1/reports/P8/audits/Claude/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md:116:| `paper/thesis_cn/*`, `paper/thesis/XJTU-thesis/` | thesis work, not Paper-1 submission scope |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:11:| `paper/thesis/` | English thesis draft | HAT, PCM, deployment, failure modes |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:12:| `paper/thesis_cn/` | Chinese thesis draft | Chinese thesis chapters, Work-2 scope chapter |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:13:| `paper/thesis/XJTU-thesis/` | XJTU thesis template/project | Formatting/template; not canonical data by itself |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:23:| `paper/thesis/chapter_1_hat_instance_overfitting.tex` | HAT instance overfitting framing | Paper-1-aligned; verify locked numbers before reuse |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:24:| `paper/thesis/chapter_2_framework.tex` | hybrid framework / CIM stack | Paper-1-aligned |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:25:| `paper/thesis/chapter_3_hat_taxonomy.tex` | HAT taxonomy | likely contains standard/ensemble/proportional distinctions |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:26:| `paper/thesis/chapter_4_failure_modes.tex` | failure modes | likely maps pure quantization collapse / PCM drift |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:27:| `paper/thesis/chapter_5_mitigation.tex` | mitigation | HAT/compensation narrative |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:28:| `paper/thesis/chapter_6_physical_realism.tex` | physical realism | PCM/OPECT/retention/device calibration |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:29:| `paper/thesis/chapter_7_deployment.tex` | deployment | precision-retention, energy, hardware constraints |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:30:| `paper/thesis/chapter_8_outlook.tex` | outlook | likely Work-2 / KV-cache future direction |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:31:| `paper/thesis_cn/chapter_6_work2_scope.tex` | Chinese Work-2 scope | most relevant to 107 analog KV-cache |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:32:| `paper/thesis_cn/chapter_4_benchmarks.tex` | Chinese benchmark chapter | likely contains Paper-1/105 numerical summaries |
ROOT_REORG_PLAN_20260509.md:127:paper/thesis/ -> thesis/en/
ROOT_REORG_PLAN_20260509.md:128:paper/thesis_cn/ -> thesis/cn/
ROOT_REORG_PLAN_20260509.md:129:paper/thesis/XJTU-thesis/ -> thesis/xjtu_template/
WORKSPACE_LAYOUT.md:96:- EN thesis: `paper/thesis/`
WORKSPACE_LAYOUT.md:97:- CN thesis: `paper/thesis_cn/`
WORKSPACE_LAYOUT_V2_20260509.md:207:| `paper/thesis/` | English thesis | `thesis/en/` |
WORKSPACE_LAYOUT_V2_20260509.md:208:| `paper/thesis_cn/` | Chinese thesis | `thesis/cn/` |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:46:| Thesis edits | `paper/thesis/` and `paper/thesis_cn/` changed; include only if this branch is also meant to update thesis drafts |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:48:| `paper/thesis/*.tex` | 8 | Thesis chapters 1-8 |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:49:| `paper/thesis/*.pdf` | 1 | Compiled thesis PDF |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:50:| `paper/thesis/*.bbl`, `*.blg` | 2 | BibTeX outputs |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:140:| `paper/thesis_cn/*.toc` | LaTeX TOC output | `rm -f paper/thesis_cn/*.toc` |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:217:git add paper/thesis/*.tex
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:218:git add paper/thesis/main.pdf
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:219:git add paper/thesis/main.bbl
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:220:git add paper/thesis/main.blg
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:265:git add paper/thesis/*.tex paper/thesis/main.pdf paper/thesis/main.bbl paper/thesis/main.blg
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:40:?? paper/thesis/XJTU-thesis/
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:41:?? paper/thesis_cn/chapter_8_outlook.tex
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:42:?? paper/thesis_cn/main.bbl
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:43:?? paper/thesis_cn/main.pdf
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:44:?? paper/thesis_cn/main.tex
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:529:report_md/_gpt/AGENT_SYNC_gpt.md:23450:  - only `_gpt/`, `paper/thesis_cn/`, and `paper/paper2/skeleton_v0/` support work assigned
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:532:report_md/_gpt/AGENT_SYNC_gpt.md:24978:- Work 2 files live in `paper/paper2/skeleton_v1/*`, `paper/thesis_cn/chapter_6_*.tex`, `chapter_7_*.tex` (all new).
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:625:## Pattern `paper/thesis`
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:628:paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:23:| `paper/thesis/` | KEEP_ACTIVE | ~50 MB | Thesis chapters | ❌ NO | ❌ NO |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:629:paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:24:| `paper/thesis_cn/` | KEEP_ACTIVE | ~5 MB | Chinese thesis draft | ❌ NO | ❌ NO |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:630:paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:101:| `paper/thesis_cn/*.toc` | LaTeX TOC output | `rm -f paper/thesis_cn/*.toc` |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:631:paper1/reports/P8/audits/Claude/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md:116:| `paper/thesis_cn/*`, `paper/thesis/XJTU-thesis/` | thesis work, not Paper-1 submission scope |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:632:paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:11:| `paper/thesis/` | English thesis draft | HAT, PCM, deployment, failure modes |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:633:paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:12:| `paper/thesis_cn/` | Chinese thesis draft | Chinese thesis chapters, Work-2 scope chapter |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:634:paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:13:| `paper/thesis/XJTU-thesis/` | XJTU thesis template/project | Formatting/template; not canonical data by itself |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:635:paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:23:| `paper/thesis/chapter_1_hat_instance_overfitting.tex` | HAT instance overfitting framing | Paper-1-aligned; verify locked numbers before reuse |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:636:paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:24:| `paper/thesis/chapter_2_framework.tex` | hybrid framework / CIM stack | Paper-1-aligned |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:637:paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:25:| `paper/thesis/chapter_3_hat_taxonomy.tex` | HAT taxonomy | likely contains standard/ensemble/proportional distinctions |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:638:paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:26:| `paper/thesis/chapter_4_failure_modes.tex` | failure modes | likely maps pure quantization collapse / PCM drift |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:639:paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:27:| `paper/thesis/chapter_5_mitigation.tex` | mitigation | HAT/compensation narrative |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:640:paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:28:| `paper/thesis/chapter_6_physical_realism.tex` | physical realism | PCM/OPECT/retention/device calibration |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:641:paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:29:| `paper/thesis/chapter_7_deployment.tex` | deployment | precision-retention, energy, hardware constraints |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:642:paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:30:| `paper/thesis/chapter_8_outlook.tex` | outlook | likely Work-2 / KV-cache future direction |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:643:paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:31:| `paper/thesis_cn/chapter_6_work2_scope.tex` | Chinese Work-2 scope | most relevant to 107 analog KV-cache |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:644:paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:32:| `paper/thesis_cn/chapter_4_benchmarks.tex` | Chinese benchmark chapter | likely contains Paper-1/105 numerical summaries |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:645:ROOT_REORG_PLAN_20260509.md:127:paper/thesis/ -> thesis/en/
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:646:ROOT_REORG_PLAN_20260509.md:128:paper/thesis_cn/ -> thesis/cn/
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:647:ROOT_REORG_PLAN_20260509.md:129:paper/thesis/XJTU-thesis/ -> thesis/xjtu_template/
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:648:WORKSPACE_LAYOUT.md:96:- EN thesis: `paper/thesis/`
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:649:WORKSPACE_LAYOUT.md:97:- CN thesis: `paper/thesis_cn/`
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:650:WORKSPACE_LAYOUT_V2_20260509.md:207:| `paper/thesis/` | English thesis | `thesis/en/` |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:651:WORKSPACE_LAYOUT_V2_20260509.md:208:| `paper/thesis_cn/` | Chinese thesis | `thesis/cn/` |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:652:paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:46:| Thesis edits | `paper/thesis/` and `paper/thesis_cn/` changed; include only if this branch is also meant to update thesis drafts |
report_md/_gpt/AGENT_SYNC_gpt.md:22975:  - `paper/thesis/chapter_1_hat_instance_overfitting.tex`
report_md/_gpt/AGENT_SYNC_gpt.md:23263:- 学位论文 is 中文. All thesis files land in `paper/thesis_cn/` as Chinese .tex.
report_md/_gpt/AGENT_SYNC_gpt.md:23269:- New rule: during the GPU loop, forbidden files = paper/00_abstract.md, paper/05_results.md, paper/06_discussion.md, cover_letter*, KIMI_REBUTTAL_MASTER*, paper/thesis/chapter_5_*.tex.
report_md/_gpt/AGENT_SYNC_gpt.md:23406:- Kimi ambiguity on thesis chapter numbering → default to `paper/thesis_cn/` structure already on disk.
report_md/_gpt/AGENT_SYNC_gpt.md:23450:  - only `_gpt/`, `paper/thesis_cn/`, and `paper/paper2/skeleton_v0/` support work assigned
report_md/_gpt/AGENT_SYNC_gpt.md:23520:  - `paper/thesis/chapter_4_failure_modes.tex`: 2 replacements
report_md/_gpt/AGENT_SYNC_gpt.md:23521:  - `paper/thesis/chapter_6_physical_realism.tex`: 1 replacement
report_md/_gpt/AGENT_SYNC_gpt.md:23644:- Do not use `K2–K5` to drive paper/thesis narrative until their provenance is either verified locally or re-imported cleanly from the remote A100 lane.
report_md/_gpt/AGENT_SYNC_gpt.md:24978:- Work 2 files live in `paper/paper2/skeleton_v1/*`, `paper/thesis_cn/chapter_6_*.tex`, `chapter_7_*.tex` (all new).
report_md/_gpt/AGENT_SYNC_gpt.md:26567:- Canonical `paper/thesis/chapter_5_mitigation.tex` and `paper/thesis_cn/chapter_5_failure_modes.tex` were not updated; only `.kimi_draft_v3` sidecars changed.
report_md/_gpt/AGENT_SYNC_gpt.md:26592:- File: `paper/thesis/chapter_6_physical_realism.tex`
report_md/_gpt/AGENT_SYNC_gpt.md:26597:- File: `paper/thesis_cn/chapter_6_work2_scope.tex`
report_md/_gpt/AGENT_SYNC_gpt.md:26627:- Independently confirmed Gemini's Ch7 fail: `paper/thesis_cn/chapter_7_deployment.tex.kimi_draft_v3` still cites `65 pJ / 15.4x` from deprecated `energy_sensitivity_analysis.json`.
report_md/_gpt/AGENT_SYNC_gpt.md:26776:- R4-2 root paper/thesis/ README cleanup — LOW, ~5 min (bundled)
report_md/_gpt/AGENT_SYNC_gpt.md:26967:2. **Narrative Stale (Thesis):** The live \`paper/thesis/chapter_1_hat_instance_overfitting.tex\` still contains the contaminated "32% ceiling" and "87.79%" source-domain claims in its concluding section. Only the sidecar draft is clean.
paper/thesis/XJTU-thesis/Main_Spine/c5.tex:8:% Figures reused from manuscript package (paths relative to paper/thesis/):
paper/thesis/chapter_2_framework.tex:6:% Figures reused from manuscript package (paths relative to paper/thesis/):
paper/thesis/README.md:26:Located under `paper/thesis_cn/`.
paper/thesis/chapter_5_mitigation.tex:6:% Figures reused from manuscript package (paths relative to paper/thesis/):
paper/thesis/XJTU-thesis/Main_Spine/c2.tex:8:% Figures reused from manuscript package (paths relative to paper/thesis/):
paper/thesis_cn/KIMI_THESIS_CN_TEMPLATE_20260420.md:4:> 适用范围：`compute_vit/paper/thesis_cn/` 学位论文编译
```

## Pattern `paper/thesis_cn`

```text
ROOT_REORG_PLAN_20260509.md:128:paper/thesis_cn/ -> thesis/cn/
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:46:| Thesis edits | `paper/thesis/` and `paper/thesis_cn/` changed; include only if this branch is also meant to update thesis drafts |
WORKSPACE_LAYOUT_V2_20260509.md:208:| `paper/thesis_cn/` | Chinese thesis | `thesis/cn/` |
paper1/reports/P8/audits/Claude/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md:116:| `paper/thesis_cn/*`, `paper/thesis/XJTU-thesis/` | thesis work, not Paper-1 submission scope |
WORKSPACE_LAYOUT.md:97:- CN thesis: `paper/thesis_cn/`
paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:12:| `paper/thesis_cn/` | Chinese thesis draft | Chinese thesis chapters, Work-2 scope chapter |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:31:| `paper/thesis_cn/chapter_6_work2_scope.tex` | Chinese Work-2 scope | most relevant to 107 analog KV-cache |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:32:| `paper/thesis_cn/chapter_4_benchmarks.tex` | Chinese benchmark chapter | likely contains Paper-1/105 numerical summaries |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:140:| `paper/thesis_cn/*.toc` | LaTeX TOC output | `rm -f paper/thesis_cn/*.toc` |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:24:| `paper/thesis_cn/` | KEEP_ACTIVE | ~5 MB | Chinese thesis draft | ❌ NO | ❌ NO |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:101:| `paper/thesis_cn/*.toc` | LaTeX TOC output | `rm -f paper/thesis_cn/*.toc` |
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:41:?? paper/thesis_cn/chapter_8_outlook.tex
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:42:?? paper/thesis_cn/main.bbl
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:43:?? paper/thesis_cn/main.pdf
paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:44:?? paper/thesis_cn/main.tex
report_md/_gpt/AGENT_SYNC_gpt.md:23263:- 学位论文 is 中文. All thesis files land in `paper/thesis_cn/` as Chinese .tex.
report_md/_gpt/AGENT_SYNC_gpt.md:23406:- Kimi ambiguity on thesis chapter numbering → default to `paper/thesis_cn/` structure already on disk.
report_md/_gpt/AGENT_SYNC_gpt.md:23450:  - only `_gpt/`, `paper/thesis_cn/`, and `paper/paper2/skeleton_v0/` support work assigned
report_md/_gpt/AGENT_SYNC_gpt.md:24978:- Work 2 files live in `paper/paper2/skeleton_v1/*`, `paper/thesis_cn/chapter_6_*.tex`, `chapter_7_*.tex` (all new).
report_md/_gpt/AGENT_SYNC_gpt.md:26567:- Canonical `paper/thesis/chapter_5_mitigation.tex` and `paper/thesis_cn/chapter_5_failure_modes.tex` were not updated; only `.kimi_draft_v3` sidecars changed.
report_md/_gpt/AGENT_SYNC_gpt.md:26597:- File: `paper/thesis_cn/chapter_6_work2_scope.tex`
report_md/_gpt/AGENT_SYNC_gpt.md:26627:- Independently confirmed Gemini's Ch7 fail: `paper/thesis_cn/chapter_7_deployment.tex.kimi_draft_v3` still cites `65 pJ / 15.4x` from deprecated `energy_sensitivity_analysis.json`.
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:529:report_md/_gpt/AGENT_SYNC_gpt.md:23450:  - only `_gpt/`, `paper/thesis_cn/`, and `paper/paper2/skeleton_v0/` support work assigned
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:532:report_md/_gpt/AGENT_SYNC_gpt.md:24978:- Work 2 files live in `paper/paper2/skeleton_v1/*`, `paper/thesis_cn/chapter_6_*.tex`, `chapter_7_*.tex` (all new).
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:629:paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:24:| `paper/thesis_cn/` | KEEP_ACTIVE | ~5 MB | Chinese thesis draft | ❌ NO | ❌ NO |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:630:paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:101:| `paper/thesis_cn/*.toc` | LaTeX TOC output | `rm -f paper/thesis_cn/*.toc` |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:631:paper1/reports/P8/audits/Claude/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md:116:| `paper/thesis_cn/*`, `paper/thesis/XJTU-thesis/` | thesis work, not Paper-1 submission scope |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:633:paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:12:| `paper/thesis_cn/` | Chinese thesis draft | Chinese thesis chapters, Work-2 scope chapter |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:643:paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:31:| `paper/thesis_cn/chapter_6_work2_scope.tex` | Chinese Work-2 scope | most relevant to 107 analog KV-cache |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:644:paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:32:| `paper/thesis_cn/chapter_4_benchmarks.tex` | Chinese benchmark chapter | likely contains Paper-1/105 numerical summaries |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:646:ROOT_REORG_PLAN_20260509.md:128:paper/thesis_cn/ -> thesis/cn/
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:649:WORKSPACE_LAYOUT.md:97:- CN thesis: `paper/thesis_cn/`
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:651:WORKSPACE_LAYOUT_V2_20260509.md:208:| `paper/thesis_cn/` | Chinese thesis | `thesis/cn/` |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:652:paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:46:| Thesis edits | `paper/thesis/` and `paper/thesis_cn/` changed; include only if this branch is also meant to update thesis drafts |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:656:paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:140:| `paper/thesis_cn/*.toc` | LaTeX TOC output | `rm -f paper/thesis_cn/*.toc` |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:663:paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:41:?? paper/thesis_cn/chapter_8_outlook.tex
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:664:paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:42:?? paper/thesis_cn/main.bbl
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:665:paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:43:?? paper/thesis_cn/main.pdf
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:666:paper1/reports/P8/audits/Claude/CLAUDE_FINAL_WORKSPACE_CLEAN_STATUS_20260509.md:44:?? paper/thesis_cn/main.tex
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:667:report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:529:report_md/_gpt/AGENT_SYNC_gpt.md:23450:  - only `_gpt/`, `paper/thesis_cn/`, and `paper/paper2/skeleton_v0/` support work assigned
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:668:report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:532:report_md/_gpt/AGENT_SYNC_gpt.md:24978:- Work 2 files live in `paper/paper2/skeleton_v1/*`, `paper/thesis_cn/chapter_6_*.tex`, `chapter_7_*.tex` (all new).
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:671:report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:629:paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:24:| `paper/thesis_cn/` | KEEP_ACTIVE | ~5 MB | Chinese thesis draft | ❌ NO | ❌ NO |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:672:report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:630:paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:101:| `paper/thesis_cn/*.toc` | LaTeX TOC output | `rm -f paper/thesis_cn/*.toc` |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:673:report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:631:paper1/reports/P8/audits/Claude/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md:116:| `paper/thesis_cn/*`, `paper/thesis/XJTU-thesis/` | thesis work, not Paper-1 submission scope |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:675:report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:633:paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:12:| `paper/thesis_cn/` | Chinese thesis draft | Chinese thesis chapters, Work-2 scope chapter |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:685:report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:643:paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:31:| `paper/thesis_cn/chapter_6_work2_scope.tex` | Chinese Work-2 scope | most relevant to 107 analog KV-cache |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:686:report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:644:paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:32:| `paper/thesis_cn/chapter_4_benchmarks.tex` | Chinese benchmark chapter | likely contains Paper-1/105 numerical summaries |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:688:report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:646:ROOT_REORG_PLAN_20260509.md:128:paper/thesis_cn/ -> thesis/cn/
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:691:report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:649:WORKSPACE_LAYOUT.md:97:- CN thesis: `paper/thesis_cn/`
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:693:report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:651:WORKSPACE_LAYOUT_V2_20260509.md:208:| `paper/thesis_cn/` | Chinese thesis | `thesis/cn/` |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:694:report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:652:paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:46:| Thesis edits | `paper/thesis/` and `paper/thesis_cn/` changed; include only if this branch is also meant to update thesis drafts |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:696:report_md/_gpt/AGENT_SYNC_gpt.md:23263:- 学位论文 is 中文. All thesis files land in `paper/thesis_cn/` as Chinese .tex.
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:698:report_md/_gpt/AGENT_SYNC_gpt.md:23406:- Kimi ambiguity on thesis chapter numbering → default to `paper/thesis_cn/` structure already on disk.
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:699:report_md/_gpt/AGENT_SYNC_gpt.md:23450:  - only `_gpt/`, `paper/thesis_cn/`, and `paper/paper2/skeleton_v0/` support work assigned
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:703:report_md/_gpt/AGENT_SYNC_gpt.md:24978:- Work 2 files live in `paper/paper2/skeleton_v1/*`, `paper/thesis_cn/chapter_6_*.tex`, `chapter_7_*.tex` (all new).
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:704:report_md/_gpt/AGENT_SYNC_gpt.md:26567:- Canonical `paper/thesis/chapter_5_mitigation.tex` and `paper/thesis_cn/chapter_5_failure_modes.tex` were not updated; only `.kimi_draft_v3` sidecars changed.
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:706:report_md/_gpt/AGENT_SYNC_gpt.md:26597:- File: `paper/thesis_cn/chapter_6_work2_scope.tex`
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:707:report_md/_gpt/AGENT_SYNC_gpt.md:26627:- Independently confirmed Gemini's Ch7 fail: `paper/thesis_cn/chapter_7_deployment.tex.kimi_draft_v3` still cites `65 pJ / 15.4x` from deprecated `energy_sensitivity_analysis.json`.
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:712:paper/thesis/README.md:26:Located under `paper/thesis_cn/`.
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:715:paper/thesis_cn/KIMI_THESIS_CN_TEMPLATE_20260420.md:4:> 适用范围：`compute_vit/paper/thesis_cn/` 学位论文编译
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:718:## Pattern `paper/thesis_cn`
paper/thesis/README.md:26:Located under `paper/thesis_cn/`.
paper/thesis_cn/KIMI_THESIS_CN_TEMPLATE_20260420.md:4:> 适用范围：`compute_vit/paper/thesis_cn/` 学位论文编译
```

## Pattern `数据_博士`

```text
WORKSPACE_LAYOUT.md:71:| `数据_博士/` (PhD data) | PhD measured device data placeholder | Awaiting delivery per DATA_INGEST_PROTOCOL |
paper1/reports/P8/audits/Claude/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md:15:- Raw device data was moved, not deleted: `数据_博士/` is now under `archive/file_organization_mv_only_20260509/raw_device_data/数据_博士`.
paper1/reports/P8/audits/Claude/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md:42:| `raw_device_data/` | raw device data formerly at `数据_博士/` |
WORKSPACE_LAYOUT_V2_20260509.md:211:| `数据_博士/` | raw device data | `data_local/raw_device_data/` |
REPRODUCIBILITY.md:20:- **Raw doctoral measurement exports** (`数据_博士/`) — fitted profiles derived from these measurements are included; raw exports are available from the corresponding author upon reasonable request.
paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:14:| `数据_博士/` | Raw device/master data | EPSC / QIVD / derived profiles; important for thesis and future hardware calibration |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:45:| Raw EPSC/device data | `数据_博士/*.csv`, `数据_博士/20260501/*.qivd`, `数据_博士/derived_profiles/` | EPSC/device profiles | extraction/calibration material; not Paper-1 locked values | unknown/provisional until processed |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:56:| Any raw `数据_博士` EPSC number treated as canonical model accuracy | Do not do this; raw device data needs extraction/fit/provenance before claim use |
paper1/reports/P8/KIMI/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md:63:4. Treat `数据_博士/` as raw calibration material; extract through a separate data provenance notebook/report before citing values.
RELEASE_CHECKLIST.md:41:- `数据_博士/`
RELEASE_CHECKLIST.md:51:- `数据_博士/` is currently untracked, but it will leak immediately if you zip
RELEASE_CHECKLIST.md:131:    '数据_博士',
paper1/reports/P8/KIMI/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md:39:| Raw device data | `数据_博士/` and archives (`.zip`, `.qivd`, raw CSV) should not be swept into Paper-1 commit without a data-policy decision |
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:229:report_md/_gpt/AGENT_SYNC_gpt.md:29415:- `数据_博士` — 5 files (RELEASE_CHECKLIST, REPRODUCIBILITY, WORKSPACE_LAYOUT, release_artifacts/)
report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md:786:## Pattern `数据_博士`
scripts/public_release_export.sh:24:    _archive/*|logs/*|report_md/*|数据_博士/*|internal/*|outputs/*|checkpoints/*|data/*|AGENT_SYNC/*)
scripts/public_release_export.sh:67:      -e '数据_博士' \
report_md/_gpt/AGENT_SYNC_gpt.md:19841:Consumed from `数据_博士`:
report_md/_gpt/AGENT_SYNC_gpt.md:19902:  - `/home/qiaosir/projects/compute_vit/数据_博士/第三页/a/小图_raw_ppf_points.txt`
report_md/_gpt/AGENT_SYNC_gpt.md:19913:### Correction — canonical PPF raw file moved into `数据_博士`
report_md/_gpt/AGENT_SYNC_gpt.md:19917:  - `/home/qiaosir/projects/compute_vit/数据_博士/第三页/a/小图_raw_ppf_points.txt`
report_md/_gpt/AGENT_SYNC_gpt.md:19919:  - `/home/qiaosir/projects/compute_vit/数据_博士/第三页/a/小图.txt`
report_md/_gpt/AGENT_SYNC_gpt.md:19921:  - `/home/qiaosir/projects/compute_vit/数据_博士/README_gpt.md`
report_md/_gpt/AGENT_SYNC_gpt.md:19923:  - `ppf_inset.source = /home/qiaosir/projects/compute_vit/数据_博士/第三页/a/小图_raw_ppf_points.txt`
report_md/_gpt/AGENT_SYNC_gpt.md:20551:- TX-27 Move historical parallel dirs (`AGENT_SYNC/`, `npj_submission_package/`, `paper_zh/`) to `archive/historical_20260417/`. Keep `数据_博士/` (doctor measured-data staging). Confirm NC bundle lives under `outputs/submission_bundle_20260417/` before archiving npj.
report_md/_gpt/AGENT_SYNC_gpt.md:20679:  - `数据_博士/`
report_md/_gpt/AGENT_SYNC_gpt.md:21252:3. **CLAUDE-D** ✅ — `REPRODUCIBILITY_PACKAGE_PLAN_20260418.md` (strategy stub): blockers C1 / C3 / C4 each get a target + recommendation. Outer-repo C1 → **do not** init; declare `compute_vit/` the publishable boundary. C3 → tier checkpoints A/B/C, only ship Tier-A (~1–3 GB) on Zenodo. C4 → ship fitted JSONs, keep raw `数据_博士/` for thesis defense only. 5-step sequence starts only after CX-A NL queue drains.
report_md/_gpt/AGENT_SYNC_gpt.md:21412:| §5 File / project management | 10 items | **M1** TX-32 paper/ legacy `.md` not yet archived (already routed to CX-C), **M3** `_archive/paper-drafts/` not created, M4 outer repo 0 tracked, M5 `数据_博士/` WSL-private, M6 25 GB checkpoints (CX-E now ✅), M7 supp page-count drift, **M8** ledger header still says "Phase 2 修正版", **M9** no `scripts/_gpt/check_locked_numbers.py`, M10 appendix cross-link audit |
report_md/_gpt/AGENT_SYNC_gpt.md:21791:- C4 (`数据_博士` tex引用) ✅ verified zero hits.
report_md/_gpt/AGENT_SYNC_gpt.md:29415:- `数据_博士` — 5 files (RELEASE_CHECKLIST, REPRODUCIBILITY, WORKSPACE_LAYOUT, release_artifacts/)
report_md/_gpt/AGENT_SYNC_gpt.md:29681:4. **Internal term** (Line 20): mentions `数据_博士/` — acceptable if file is internal-only
```

## Pattern `checkpoints/`

```text
eval_fresh_instances.py:44:        "tinyvit", "V4", "checkpoints/V4_hybrid_standard_noise_hat_best.pt", device
eval_fresh_instances.py:50:        "tinyvit", "V4", "checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt", device
REPRODUCIBILITY.md:15:- `checkpoints/` — Trained model checkpoints (see `CHECKPOINT_INVENTORY_20260418.md` for tiered release plan).
REPRODUCIBILITY.md:45:| V4 canonical HAT 87.95% | `python train_tinyvit.py --config configs/tinyvit_v4_standard_noise.json` | `checkpoints/V4_hybrid_standard_noise_hat_best.pt` |
.gitignore:8:checkpoints/
.gitignore:17:.ipynb_checkpoints/
README_REPRODUCIBILITY_PAPER1.md:97:paper2_aihwkit_baseline/checkpoints/**/best.pt
README_REPRODUCIBILITY_PAPER1.md:98:paper2_aihwkit_baseline/checkpoints/**/last.pt
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:27:| `checkpoints/` | KEEP_LOCAL_DATA | 33 GB | Old experiment checkpoints | ❌ NO | ❌ NO |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:76:| `checkpoints/*.pt` (34 files) | 33 GB total | KEEP_LOCAL_DATA | Keep locally, never commit |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md:80:| `paper2_aihwkit_baseline/checkpoints/` | ~6 GB | KEEP_LOCAL_DATA | Keep locally, never commit |
paper1/reports/P6/KIMI/KIMI_P6_TRACK_C_LOCAL_GPU_EXECUTION_REPORT_20260509.md:25:| Command | `r11d4_train_pcm.py --run-id r11d_6bit_pcm_seed123 --seed 123 --epochs 100 --batch-size 64 --lr 0.001 --wd 0.05 --momentum 0.0 --device cuda --workers 0 --save-dir paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123 --inp-res 0.015625 --out-res 0.015625 --modifier-std-dev 0.10 --early-stop-patience 10 --early-stop-min-delta 0.01` |
paper1/reports/P6/KIMI/KIMI_P6_TRACK_C_LOCAL_GPU_EXECUTION_REPORT_20260509.md:31:| Backup | `paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123_P6_BACKUP_20260509/` |
paper1/reports/P6/KIMI/KIMI_P6_TRACK_A_EVIDENCE_GAP_LEDGER_20260509.md:21:| 9 | Appendix/defense-only: 5-bit PCM non-frontier | `r11d_5bit_pcm_seed*` checkpoints | `paper2_aihwkit_baseline/checkpoints/r11d_5bit_pcm_seed*/` | 3+ seeds | fresh_mean | **Complete** | None | `exclude/superseded` |
paper1/reports/P6/KIMI/KIMI_P6_TRACK_A_EVIDENCE_GAP_LEDGER_20260509.md:139:| Evidence | `paper2_aihwkit_baseline/checkpoints/r11d_5bit_pcm_seed*/` |
paper1/reports/P6/audits/DS/DS_IDEALDEVICE_AND_PCM_PROTOCOL_AUDIT_20260509.md:62:| 87.28 ± 0.13% | `checkpoints/best.pt` | `checkpoints/fresh_eval.json` | ✅ mean=87.28% |
WORKSPACE_LAYOUT_V2_20260509.md:12:4. Large datasets/checkpoints/raw hardware data stay local-first and should not be committed blindly.
WORKSPACE_LAYOUT_V2_20260509.md:79:- Large checkpoints may be linked from `data_local/checkpoints/` instead of committed.
WORKSPACE_LAYOUT_V2_20260509.md:107:├── checkpoints/
WORKSPACE_LAYOUT_V2_20260509.md:210:| `checkpoints/` | checkpoints | `data_local/checkpoints/` |
WORKSPACE_LAYOUT_V2_20260509.md:237:- Move datasets/checkpoints/raw device data into `data_local/` or keep as local symlinks.
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/pcm_6bit_seed456_full100/drift_eval.json:2:  "checkpoint": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456_full100/best.pt",
paper1/reports/P7/KIMI/KIMI_P7_TRACK_E_REMOTE107_WORK2_GATE_20260509.md:76:| Checkpoint path | `checkpoints/_gpt/cross_arch_tinyimagenet/...` |
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/pcm_6bit_seed123/training_history.json:915:    "save_dir": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123",
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/pcm_6bit_seed123/training_history.json:949:      "save_dir": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_4bit_seed456_clean/fresh_eval.json:2:  "checkpoint": "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/best.pt",
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:2:ideal_8bit_sigma010_aihwkit_baseline,paper2_aihwkit_baseline/checkpoints/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/ideal_8bit_sigma010_aihwkit_baseline/fresh_eval.json,1a0f9234677963522cd74cfcf8f47c8f30f6d2031aadbb3dfcbe643f912bb45a,978,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:3:ideal_8bit_sigma010_aihwkit_baseline,paper2_aihwkit_baseline/checkpoints/training_history.json,paper/latex_gpt/source_data/canonical_json/ideal_8bit_sigma010_aihwkit_baseline/training_history.json,b4bc4ba04563a5193f3c6771ed0af86f28eb6b771b5d12ed357869dd8a196a87,20232,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:4:pure_4bit_collapse,paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/pure_4bit_collapse/fresh_eval.json,bc02b808fb73356aebf0f00621d44f6ac7e4ab4c84627a57c3080a6a52537e49,6394,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:5:pure_4bit_collapse,paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/training_history.json,paper/latex_gpt/source_data/canonical_json/pure_4bit_collapse/training_history.json,b7d64161a91c8b6db60f6f1f9002e73c482cb11ee26e4c9e4654867ff1b9c61b,6600,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:7:pcm_8bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed123/drift_eval.json,82077b5b4a9dab3e5238c273d167deb4596feb25bb8986d7100512bee021a0ce,723,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:8:pcm_8bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/extended_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed123/extended_drift_eval.json,f9e5a92c05e98bfd36f6807a46f4482af6e8d459ac327300c95147a018bc2264,1504,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:9:pcm_8bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/fresh_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed123/fresh_drift_eval.json,fc9f1cd6ffbd859546f0c82c07bea68d15612ef348817e9d39f9e4edad122435,23642,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:10:pcm_8bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed123/fresh_eval.json,1387d021694f524c005d02de6412c650947150b15c5be938864c86a91860fe78,21408,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:11:pcm_8bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/training_history.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed123/training_history.json,81e5ac47b306de4dd31d392636c54bf663d3093e4eb4ec84d85c1ab938c0d4f0,22282,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:12:pcm_8bit_seed456,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456/drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed456/drift_eval.json,24833d5d977e4b83467de6259da59d454749ab87076a3c139f72a78ff77dd859,723,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:13:pcm_8bit_seed456,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456/extended_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed456/extended_drift_eval.json,c7d0e047ba7cfa83ace9ad69512029b32e513386dce61af15c57aaa8d8b410fb,1501,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:14:pcm_8bit_seed456,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456/fresh_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed456/fresh_drift_eval.json,16886e4727e7f88a59b2f7c47139508ec0cf97f0e8f3929dd443b2f0b77542d3,23640,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:15:pcm_8bit_seed456,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed456/fresh_eval.json,23b42a8cf363f7d67a8da010b189040d02ae5697573d6123ca139c7fa71a4800,21411,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:16:pcm_8bit_seed456,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456/training_history.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed456/training_history.json,bd699041c26af7c698be6edd913847fa5b4874fd69b4ba5cec0da626e74203c9,22189,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:17:pcm_8bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed789/drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed789/drift_eval.json,e5f7c96b14b8fc4ecbfd6739a0a39ef444140e33d18e7ad4336b7e37f11a359a,723,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:18:pcm_8bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed789/extended_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed789/extended_drift_eval.json,082aa22703975ce5f57983c235b538382559fcc07f5df80161d7d8a5a0580526,1501,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:19:pcm_8bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed789/fresh_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed789/fresh_drift_eval.json,b82e1edb21acaab809802ba6333abb6cd27f10c2d71031c96911211cf5ac711a,23630,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:20:pcm_8bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed789/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed789/fresh_eval.json,de88891eb323b27d080b22355cc135367a5275f3ebeaf90fd34517d8bbc067e9,21413,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:21:pcm_8bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed789/training_history.json,paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed789/training_history.json,a8d600c06f188449b49a4c226d8c1270efc46829e268058a8a880a3445165863,22262,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:22:pcm_6bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123/drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed123/drift_eval.json,32c77b8e419f65dcd72bfc088473b70f22aceaba5ff15d6a89c6edbe82cb1db7,721,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:23:pcm_6bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed123/fresh_eval.json,4dbdfede9a1b007d3cd99b3cca9738c974f1d9c0959376cbbb0f1f18e731afd8,21406,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:24:pcm_6bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123/training_history.json,paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed123/training_history.json,f529ad7c4653634a6ca99430abed252d3036cc5ee3825622678237cf57126af6,22184,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:25:pcm_6bit_seed456_full100,paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456_full100/drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed456_full100/drift_eval.json,129cc6097c8b58493f39f04e8d866a655c2ca1356348f11c8e6a4e99529a702e,728,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:26:pcm_6bit_seed456_full100,paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456_full100/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed456_full100/fresh_eval.json,a972fccda6cccf8a4d6175ea678e6475336616d2a1c001316c17c90c7a9a4423,21414,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:27:pcm_6bit_seed456_full100,paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456_full100/training_history.json,paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed456_full100/training_history.json,10f1ae07637610794117f942d7e4622e56757c87a90602ece6a47e518502ae99,22230,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:28:pcm_6bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed789/drift_eval.json,bc91127b1c2a6ff50dc56942971a8de76eef748f99b533f927e801f98c268abc,721,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:29:pcm_6bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed789/fresh_eval.json,c9c63c903275baa4b53670484afc753236c0ac0deb823f5f5884d9939a84cf8d,21412,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:30:pcm_6bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/training_history.json,paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed789/training_history.json,9e2f9b120d7b7219dfea58d1d659989890405cb205a9c61e7a77d2b576bcfa82,22195,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:31:pcm_4bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed123/drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed123/drift_eval.json,29238ff42a7715a0e86fe79e355f955555f33df73c3d4ee9def628e8e34a122d,719,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:32:pcm_4bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed123/extended_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed123/extended_drift_eval.json,83aefc8264afa2a661ef6f07a3f45444a7a04acf70a9764388c83a848d39b01e,1500,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:33:pcm_4bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed123/fresh_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed123/fresh_drift_eval.json,a74fce7b5b2be29c4d3725368c64401266a837076a8d77e659960b6c53326657,23631,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:34:pcm_4bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed123/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed123/fresh_eval.json,e1308c05eb69bfe5075df087634f8ee64fc4b43852f942d95d512cfb023e0a5a,21404,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:35:pcm_4bit_seed123,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed123/training_history.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed123/training_history.json,06387b9ee4d5efae243c13fe7bd28103f9c32d52e2b3bc45328eb989a616096d,22251,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:36:pcm_4bit_seed456_clean,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed456_clean/drift_eval.json,451a7685f1fef230c1bb3a3b6bc9a97a14892c3fb6dde2317522467014d33b7d,725,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:37:pcm_4bit_seed456_clean,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/extended_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed456_clean/extended_drift_eval.json,7b8a6b5e9a49f4ff9fc662c61176493ba87569049732ee0894506e922d68df69,1506,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:38:pcm_4bit_seed456_clean,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/fresh_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed456_clean/fresh_drift_eval.json,8f610064a3e3e1ff11404d39ae40150d2100b9a9085319f5bd018ea8f533d054,23638,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:39:pcm_4bit_seed456_clean,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed456_clean/fresh_eval.json,01ec26488a405d091428d884a9a4e05852a469ccf67c0f327646c80afbdff5f5,21414,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:40:pcm_4bit_seed456_clean,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/training_history.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed456_clean/training_history.json,01c34ddd6ba6229e72147ccc0266aa617c17eda7e9c511940d65a519086e6fd1,22269,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:41:pcm_4bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789/drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed789/drift_eval.json,a411ad89728424af5bd9045df41de610810b9d7b3518adedfb0da9a4f2d9200b,719,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:42:pcm_4bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789/extended_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed789/extended_drift_eval.json,09ff89e5d8ec5d1e050bcc457edf54bd8a85a40b888d1e1fd689ee60c556e7a6,1499,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:43:pcm_4bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789/fresh_drift_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed789/fresh_drift_eval.json,3f86574dbbe39740a098df46195a338fb9de2e9c4591519c6b79f272d3988598,23625,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:44:pcm_4bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789/fresh_eval.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed789/fresh_eval.json,9ff017ed7261053ccb428271a49b4122208342a74c78c3fa3b525782453a2bed,21407,copied
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/manifest_canonical_json_20260501.csv:45:pcm_4bit_seed789,paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789/training_history.json,paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed789/training_history.json,acb204b6a10fc4d3fa57990682af082ae3451fb1499e0ce49e2e5eabea3adf55,22235,copied
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_4bit_seed789/fresh_drift_eval.json:2:  "checkpoint": "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789/best.pt",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_6bit_seed456/training_history.json:375:    "save_dir": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_6bit_seed456/training_history.json:409:      "save_dir": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456",
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:148:| `checkpoints/*.pt` | 33 GB total | Old experiment checkpoints | **Do not commit** — keep in `.gitignore` |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md:159:| `.pt` / `.pth` / `.ckpt` in commit scope | ❌ None — all in `checkpoints/` which is already `.gitignore`d |
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_8bit_seed456/training_history.json:915:    "save_dir": "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_8bit_seed456/training_history.json:949:      "save_dir": "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456",
release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/pcm_6bit_seed123/drift_eval.json:2:  "checkpoint": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123/best.pt",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_6bit_seed457/training_history.json:915:    "save_dir": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed457",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_6bit_seed457/training_history.json:949:      "save_dir": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed457",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_8bit_seed123/extended_drift_eval.json:2:  "checkpoint": "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/best.pt",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/pcm_6bit_seed789/drift_eval.json:2:  "checkpoint": "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/best.pt",
WORKSPACE_LAYOUT.md:59:| `checkpoints/` | Model checkpoints | **Protected:** `_ensemble/` (canonical), `_gpt/postfix_m_series/` (M-series), C/R/V baselines |
WORKSPACE_LAYOUT.md:88:- `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` → 86.37% / 88.53% / AR(1)
WORKSPACE_LAYOUT.md:89:- `checkpoints/_gpt/postfix_m_series/cx_m{1..6}/` → severe-NL ~80-82% band
WORKSPACE_LAYOUT.md:90:- `checkpoints/{C,R,V}{1..8}_*.pt` → paper baselines
WORKSPACE_LAYOUT.md:134:| `checkpoints/_ensemble/V4_*.pt` (canonical 86.37%) | Local + Zenodo | Bundle in `release_artifacts/source_data_v1/` for paper-1 release |
WORKSPACE_LAYOUT.md:135:| `checkpoints/{C,R,V}{1..8}*.pt` baselines | Local + Zenodo | Same |
WORKSPACE_LAYOUT.md:136:| `checkpoints/_gpt/postfix_m_series/cx_m{1..6}/` | Local + Zenodo | Same |
paper1/reports/P8/KIMI/KIMI_P8_SELF_AUDIT_20260509.md:69:4. Confirm Track D staging list excludes raw data/checkpoints/private files.
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:10:    "paper2_aihwkit_baseline/checkpoints/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:11:    "paper2_aihwkit_baseline/checkpoints/r11d_1_4bit/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:13:    "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:14:    "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:15:    "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed123/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:16:    "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:17:    "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:18:    "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed456/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:19:    "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed789/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:20:    "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed789/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:21:    "paper2_aihwkit_baseline/checkpoints/r11d_5a_pcm_seed789/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:22:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:23:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:24:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:25:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:26:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:27:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed456/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:28:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed457/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:29:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed457/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:30:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed457/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:31:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:32:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:33:    "paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed789/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:34:    "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed123/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:35:    "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed123/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:36:    "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed123/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:37:    "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:38:    "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:39:    "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed456_clean/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:40:    "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/manifest_paper1_spine.json:41:    "paper2_aihwkit_baseline/checkpoints/r11d_7_pcm_4bit_seed789/fresh_eval.json",
```

## Pattern `data/`

```text
README.md:82:├── data/                          # Datasets (auto-downloaded)
paper1/reports/P7/KIMI/KIMI_P7_TRACK_H_SUBMISSION_CHECKLIST_AND_DEFENSE_PACK_20260509.md:19:| Source data | `source_data/*.csv`, `source_data/canonical_json/` | ✅ Staged |
paper1/reports/P7/KIMI/KIMI_P7_TRACK_A_FINAL_FREEZE_CERTIFICATE_20260509.md:68:**File:** `source_data/tab_pcm_precision_ladder.csv`
WORKSPACE_LAYOUT_V2_20260509.md:47:├── source_data/
WORKSPACE_LAYOUT_V2_20260509.md:108:├── raw_device_data/
WORKSPACE_LAYOUT_V2_20260509.md:114:- Default: do not commit large raw data/checkpoints.
WORKSPACE_LAYOUT_V2_20260509.md:134:- Outputs become Paper-1 canonical only after audit and migration into `paper1/source_data/`.
WORKSPACE_LAYOUT_V2_20260509.md:209:| `data/` | datasets | `data_local/datasets/` |
WORKSPACE_LAYOUT_V2_20260509.md:211:| `数据_博士/` | raw device data | `data_local/raw_device_data/` |
paper1/reports/P8/audits/Claude/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md:15:- Raw device data was moved, not deleted: `数据_博士/` is now under `archive/file_organization_mv_only_20260509/raw_device_data/数据_博士`.
paper1/reports/P8/audits/Claude/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md:26:| `release_auxiliary/` | older source-data/Zenodo auxiliary packages |
paper1/reports/P8/audits/Claude/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md:42:| `raw_device_data/` | raw device data formerly at `数据_博士/` |
paper1/reports/P8/audits/Claude/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md:112:| `paper/latex_gpt/source_data/canonical_json/manifest_canonical_json_20260509.*` | current canonical manifest |
paper1/reports/P8/audits/Claude/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md:113:| `paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed456/`, `pcm_6bit_seed457/` | current corrected canonical data |
paper1/reports/P8/audits/Claude/CLAUDE_MV_ONLY_FILE_ORGANIZATION_20260509.md:114:| `paper/latex_gpt/source_data/canonical_json/deprecated_20260501_old_protocol/` | provenance archive for old protocol |
PROJECT_INDEX.md:36:├── data/                   CIFAR-10/100, Flowers-102, ImageNet, SVHN, TinyImageNet (gitignored)
PROJECT_INDEX.md:261:| `data/` | CIFAR-10, CIFAR-100, Flowers-102, ImageNet, SVHN, TinyImageNet | live (gitignored) |
PROJECT_INDEX.md:279:| `_archive/old-experiment-data/` | 5 | `exp_asymmetry_*.txt`, `PAPER_METHODS_PARAGRAPH.txt`, `tex_diff.txt` |
PROJECT_INDEX.md:293:| `outputs/reviewer_archive_20260417/` | External reviewer archive (audit/, code_snapshot/, manuscript/, response/, source_data/, INVENTORY.txt) | live |
PROJECT_INDEX.md:333:- `checkpoints/` and `data/` contents: never moved or renamed by agents during active experiments.
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:60:3b6dc09095ed239e2dad31314e5f2063b5f2ec841563c17ba87ba6352b0f1844  ./source_data/canonical_json/README.md
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:61:5a9e0a22aac4fa66068d7a52f3b5b03b66b6f62ebfa19fcaa8c58299c1a2d22e  ./source_data/canonical_json/ensemble_hat_4bit_3seed/r10a_canonical_ensemble_hat_3seed_fresh_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:62:1a0f9234677963522cd74cfcf8f47c8f30f6d2031aadbb3dfcbe643f912bb45a  ./source_data/canonical_json/ideal_8bit_sigma010_aihwkit_baseline/fresh_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:63:b4bc4ba04563a5193f3c6771ed0af86f28eb6b771b5d12ed357869dd8a196a87  ./source_data/canonical_json/ideal_8bit_sigma010_aihwkit_baseline/training_history.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:64:ad6ffcf2d3bc17ae8cfac4f174271f75088e0873490ca134f7781d7e334fc000  ./source_data/canonical_json/manifest_canonical_json_20260509.csv
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:65:325885c2945e9c684a310a70283de71aaf1c41d2f819e5606f9aadf61667489f  ./source_data/canonical_json/manifest_canonical_json_20260509.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:66:29238ff42a7715a0e86fe79e355f955555f33df73c3d4ee9def628e8e34a122d  ./source_data/canonical_json/pcm_4bit_seed123/drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:67:83aefc8264afa2a661ef6f07a3f45444a7a04acf70a9764388c83a848d39b01e  ./source_data/canonical_json/pcm_4bit_seed123/extended_drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:68:a74fce7b5b2be29c4d3725368c64401266a837076a8d77e659960b6c53326657  ./source_data/canonical_json/pcm_4bit_seed123/fresh_drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:69:e1308c05eb69bfe5075df087634f8ee64fc4b43852f942d95d512cfb023e0a5a  ./source_data/canonical_json/pcm_4bit_seed123/fresh_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:70:06387b9ee4d5efae243c13fe7bd28103f9c32d52e2b3bc45328eb989a616096d  ./source_data/canonical_json/pcm_4bit_seed123/training_history.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:71:451a7685f1fef230c1bb3a3b6bc9a97a14892c3fb6dde2317522467014d33b7d  ./source_data/canonical_json/pcm_4bit_seed456_clean/drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:72:7b8a6b5e9a49f4ff9fc662c61176493ba87569049732ee0894506e922d68df69  ./source_data/canonical_json/pcm_4bit_seed456_clean/extended_drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:73:8f610064a3e3e1ff11404d39ae40150d2100b9a9085319f5bd018ea8f533d054  ./source_data/canonical_json/pcm_4bit_seed456_clean/fresh_drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:74:01ec26488a405d091428d884a9a4e05852a469ccf67c0f327646c80afbdff5f5  ./source_data/canonical_json/pcm_4bit_seed456_clean/fresh_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:75:01c34ddd6ba6229e72147ccc0266aa617c17eda7e9c511940d65a519086e6fd1  ./source_data/canonical_json/pcm_4bit_seed456_clean/training_history.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:76:a411ad89728424af5bd9045df41de610810b9d7b3518adedfb0da9a4f2d9200b  ./source_data/canonical_json/pcm_4bit_seed789/drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:77:09ff89e5d8ec5d1e050bcc457edf54bd8a85a40b888d1e1fd689ee60c556e7a6  ./source_data/canonical_json/pcm_4bit_seed789/extended_drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:78:3f86574dbbe39740a098df46195a338fb9de2e9c4591519c6b79f272d3988598  ./source_data/canonical_json/pcm_4bit_seed789/fresh_drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:79:9ff017ed7261053ccb428271a49b4122208342a74c78c3fa3b525782453a2bed  ./source_data/canonical_json/pcm_4bit_seed789/fresh_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:80:acb204b6a10fc4d3fa57990682af082ae3451fb1499e0ce49e2e5eabea3adf55  ./source_data/canonical_json/pcm_4bit_seed789/training_history.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:81:78a3d468f9ebd1d324250fbc58992269d75dbf584d08296dfd606ba974fc5780  ./source_data/canonical_json/pcm_6bit_seed123/drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:82:021cb15e5feb1246d3ebfe871de09b72f6dd60b1f52d79cc686a9e930a4b4a1c  ./source_data/canonical_json/pcm_6bit_seed123/fresh_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:83:26dfd55230b41c71da619a6ed8ce870b1bf7027aa276e3298b5c5483f3b013f4  ./source_data/canonical_json/pcm_6bit_seed123/training_history.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:84:3a32904431fcd08d5d4591c42f085a77cc9f60bf232574b5e7e7abb0ce3ca153  ./source_data/canonical_json/pcm_6bit_seed456/drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:85:0e9251c1a586537d0444772479a559f4a9533d3f0da3673035e55f68402e5917  ./source_data/canonical_json/pcm_6bit_seed456/fresh_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:86:108023c1ab3d6b4006f888080b66e64058d1623add74d35fd07211421642158b  ./source_data/canonical_json/pcm_6bit_seed456/training_history.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:87:7b477eab4463556feb94b2f13a24974ea0367b6a53fe99fb1fbac414e2b7662a  ./source_data/canonical_json/pcm_6bit_seed457/drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:88:924f5ac8f1847b2d531f476cb111d94d06bcdd5487c3f7cf05b196f335373dbf  ./source_data/canonical_json/pcm_6bit_seed457/fresh_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:89:5bf994f3f99945a30419a2c1a8229f5ff09a2d661bc1c5bce4d76be67eb7ea61  ./source_data/canonical_json/pcm_6bit_seed457/training_history.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:90:b04c67dcfaf94fb710e20c38ded371add11f40bc4ff353bf0aea2028d02ec08e  ./source_data/canonical_json/pcm_6bit_seed789/drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:91:4664c5e820708d894cd46d36a7cd98a6f6c2f5caa95128902da7751ba2c953fb  ./source_data/canonical_json/pcm_6bit_seed789/fresh_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:92:a3f56cb17d3aceb041d6b786f1c6445514254e58f31683cdb60bcb99d4f1e638  ./source_data/canonical_json/pcm_6bit_seed789/training_history.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:93:82077b5b4a9dab3e5238c273d167deb4596feb25bb8986d7100512bee021a0ce  ./source_data/canonical_json/pcm_8bit_seed123/drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:94:f9e5a92c05e98bfd36f6807a46f4482af6e8d459ac327300c95147a018bc2264  ./source_data/canonical_json/pcm_8bit_seed123/extended_drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:95:fc9f1cd6ffbd859546f0c82c07bea68d15612ef348817e9d39f9e4edad122435  ./source_data/canonical_json/pcm_8bit_seed123/fresh_drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:96:1387d021694f524c005d02de6412c650947150b15c5be938864c86a91860fe78  ./source_data/canonical_json/pcm_8bit_seed123/fresh_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:97:81e5ac47b306de4dd31d392636c54bf663d3093e4eb4ec84d85c1ab938c0d4f0  ./source_data/canonical_json/pcm_8bit_seed123/training_history.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:98:24833d5d977e4b83467de6259da59d454749ab87076a3c139f72a78ff77dd859  ./source_data/canonical_json/pcm_8bit_seed456/drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:99:c7d0e047ba7cfa83ace9ad69512029b32e513386dce61af15c57aaa8d8b410fb  ./source_data/canonical_json/pcm_8bit_seed456/extended_drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:100:16886e4727e7f88a59b2f7c47139508ec0cf97f0e8f3929dd443b2f0b77542d3  ./source_data/canonical_json/pcm_8bit_seed456/fresh_drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:101:23b42a8cf363f7d67a8da010b189040d02ae5697573d6123ca139c7fa71a4800  ./source_data/canonical_json/pcm_8bit_seed456/fresh_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:102:bd699041c26af7c698be6edd913847fa5b4874fd69b4ba5cec0da626e74203c9  ./source_data/canonical_json/pcm_8bit_seed456/training_history.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:103:e5f7c96b14b8fc4ecbfd6739a0a39ef444140e33d18e7ad4336b7e37f11a359a  ./source_data/canonical_json/pcm_8bit_seed789/drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:104:082aa22703975ce5f57983c235b538382559fcc07f5df80161d7d8a5a0580526  ./source_data/canonical_json/pcm_8bit_seed789/extended_drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:105:b82e1edb21acaab809802ba6333abb6cd27f10c2d71031c96911211cf5ac711a  ./source_data/canonical_json/pcm_8bit_seed789/fresh_drift_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:106:de88891eb323b27d080b22355cc135367a5275f3ebeaf90fd34517d8bbc067e9  ./source_data/canonical_json/pcm_8bit_seed789/fresh_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:107:a8d600c06f188449b49a4c226d8c1270efc46829e268058a8a880a3445165863  ./source_data/canonical_json/pcm_8bit_seed789/training_history.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:108:bc02b808fb73356aebf0f00621d44f6ac7e4ab4c84627a57c3080a6a52537e49  ./source_data/canonical_json/pure_4bit_collapse/fresh_eval.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:109:b7d64161a91c8b6db60f6f1f9002e73c482cb11ee26e4c9e4654867ff1b9c61b  ./source_data/canonical_json/pure_4bit_collapse/training_history.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:110:78001a066a28cdec4256f4da1efcf012240cea9ba591d72f8acc277f4bc11340  ./source_data/fig1_paper1_spine.csv
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:111:4785a23b96d06131a5a9a3ea7108129ca3cbb46ac2aece4b7e3f5167b0f6619c  ./source_data/fig2_paper1_decision_map.csv
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:112:a263ee64053917ce20e23a14f6177532677999fad91d5196bd44e9a2e730050a  ./source_data/manifest_all_figures_20260501.csv
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:113:f28cafa934b53f935f166a573f2d5842537cfd0b7458d9a37de566a8bc17068b  ./source_data/manifest_all_figures_20260501.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:114:5708e60899e8fe86bb18f38ffc78a05e8a1fc0f8bf109c1fbcde1e243b3cf858  ./source_data/manifest_bib_doi_resolution_20260501.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:115:81c497c51f56c131fca31451de1d2f6f34baca50d9a57ed6d45faa0542d66de2  ./source_data/manifest_bib_key_audit_20260501.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:116:003cccbab7e2cdff7c786d066d7891791ee7e4dde515b76e5b7212a73c86a61d  ./source_data/manifest_paper1_spine.json
release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt:117:53b74ba77bd1771c98226a8b5a7c6e59456f90be3d88296b17e6a55d826b8708  ./source_data/tab_pcm_precision_ladder.csv
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:10:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed457/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:17:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed457/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:24:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed457/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:31:      "dest": "paper/latex_gpt/source_data/canonical_json/pure_4bit_collapse/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:38:      "dest": "paper/latex_gpt/source_data/canonical_json/pure_4bit_collapse/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:45:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed456_clean/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:52:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed456_clean/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:59:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed456_clean/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:66:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed456_clean/extended_drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:73:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed456_clean/fresh_drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:80:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed123/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:87:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed123/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:94:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed123/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:101:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed123/extended_drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:108:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed123/fresh_drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:115:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed789/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:122:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed789/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:129:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed789/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:136:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed789/extended_drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:143:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed789/fresh_drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:150:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed789/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:157:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed789/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:164:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed789/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:171:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed789/extended_drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:178:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed789/fresh_drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:185:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed789/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:192:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed789/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:199:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed789/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:206:      "dest": "paper/latex_gpt/source_data/canonical_json/ideal_8bit_sigma010_aihwkit_baseline/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:213:      "dest": "paper/latex_gpt/source_data/canonical_json/ideal_8bit_sigma010_aihwkit_baseline/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:220:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed456/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:227:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed456/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:234:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed456/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:241:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed123/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:248:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed123/training_history.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:255:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed123/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:262:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed123/extended_drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:269:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed123/fresh_drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:276:      "dest": "paper/latex_gpt/source_data/canonical_json/ensemble_hat_4bit_3seed/r10a_canonical_ensemble_hat_3seed_fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:283:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed123/drift_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:290:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed123/fresh_eval.json",
release_artifacts/paper1_submission_bundle_20260509_final/source_data/canonical_json/manifest_canonical_json_20260509.json:297:      "dest": "paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed456/drift_eval.json",
```
