# Dispatch Superphase P7: Final Freeze, Repo Discipline, Remote Bridge, and Work-2 Planning

Date: 2026-05-09 18:40 Asia/Shanghai
Issued by: Codex
Primary executor: Kimi
Auditors: DS and Mimo
Visual lane: Gemini, user-directed only
Codex role: final arbitration and high-risk edits

## 0. Operating Rule

Paper-1 scientific numbers are frozen after P6. No agent may change numerical claims, captions, source data, or PDFs unless the change is explicitly routed through Codex acceptance.

Main manuscript figures are not to be modified unless the user explicitly asks. Appendix visuals may continue, but visual work must not mutate scientific values.

## 1. P7 Goal

P7 should take several hours and reduce future user back-and-forth. It is not a single small report.

Deliver one integrated package that answers:

| Question | Required answer |
|---|---|
| Is Paper-1 ready to submit? | Yes, with final bundle path and exact SHA status. |
| What is safe to push to GitHub? | Clean branch plan with include/exclude list. |
| What must not be deleted? | Canonical data map and final bundle. |
| What remains for 105? | Seed789 closure and exact commands only, not Paper-1 blocker. |
| What remains for 107? | Corrected-noise Work-2 package, not Paper-1 claim. |
| What can local GPU do? | Only bounded non-mutating checks unless Codex reopens experiments. |
| What should Gemini do? | Appendix visual polish only, with frozen data. |
| What should DS/Mimo audit? | Repo hygiene, file cleanup safety, release completeness, claim freeze, remote separation. |

## 2. Track A: Final Freeze Audit

Owner: Kimi
Expected duration: 1-2 hours

Tasks:

| Step | Requirement |
|---|---|
| A1 | Cold-unpack `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` into a temp directory. |
| A2 | Verify SHA256 manifest passes inside the unpacked copy. |
| A3 | Verify `main.pdf`, `supplementary_main.pdf`, and `cover_letter.pdf` exist. |
| A4 | Grep active unpacked sources for stale values: `68.55`, `0.07 pp`, `0.07~pp`, `68.93`, `68.98`, `seed123 training_history missing`. |
| A5 | Extract PDF text and confirm old values are absent, new values are present. |
| A6 | Confirm source CSV values match the P6 locked table. |
| A7 | Write a one-page freeze certificate. |

Deliverable:

`report_md/_gpt/KIMI_P7_TRACK_A_FINAL_FREEZE_CERTIFICATE_20260509.md`

Kill criterion: if any stale value appears in the final bundle, stop and report; do not patch silently.

## 3. Track B: Git/Repo Hygiene Plan and Safe Commit Scope

Owner: Kimi
Expected duration: 2-4 hours

Tasks:

| Step | Requirement |
|---|---|
| B1 | Generate `git status --short` inventory grouped by category: paper active, release bundle, source data, scripts, reports, generated figures, deleted drafts, unrelated legacy. |
| B2 | Identify files safe to commit for Paper-1 final bundle. |
| B3 | Identify files that must remain uncommitted or archived. |
| B4 | Verify no checkpoints, datasets, `.pt`, `.pth`, `.ckpt`, raw large logs, or build residues are in the intended commit set. |
| B5 | Propose a branch name and commit message, but do not push unless user explicitly confirms. |
| B6 | Produce an exact command block for the user if they want to commit/push. |

Deliverable:

`report_md/_gpt/KIMI_P7_TRACK_B_GIT_HYGIENE_AND_COMMIT_SCOPE_20260509.md`

Required stance: conservative. Do not delete files in this track.

## 4. Track C: Canonical Data Location Map v2

Owner: Kimi
Expected duration: 1-2 hours

Tasks:

| Step | Requirement |
|---|---|
| C1 | Update the data map after P6 seed123 closure. |
| C2 | Mark each data source as canonical, provenance-only, deprecated, or remote-only. |
| C3 | Include 105 and 107 clone/result directories under `/home/qiaosir/projects/`. |
| C4 | Include final bundle, provenance archive, canonical JSON, source CSV, and guard scripts. |
| C5 | Add a `DO_NOT_DELETE` column. |

Deliverable:

`report_md/_gpt/KIMI_P7_TRACK_C_CANONICAL_DATA_MAP_V2_20260509.md`

## 5. Track D: Remote 105 Closure Gate

Owner: Kimi
Expected duration: 1-2 hours now, then update when server returns

Context:

105 is supplement/validation only. It must not change Paper-1 locked claims unless Codex explicitly reopens the paper.

Tasks:

| Step | Requirement |
|---|---|
| D1 | Summarize latest 105 status: seed123/456 complete, seed789 delayed by crash. |
| D2 | List exact missing items: final seed789 table, exact commands, environment, git SHA, fresh protocol, JSON/log locations. |
| D3 | Define accept/reject criteria for using 105 in supplement: same-arch digital, multi-seed, no naming ambiguity, source=test_acc not train_acc. |
| D4 | Prepare a GitHub-safe task file for 105 to pull later. |
| D5 | Make clear that 105 data are not required for Paper-1 submission freeze. |

Deliverable:

`report_md/_gpt/KIMI_P7_TRACK_D_REMOTE105_CLOSURE_GATE_20260509.md`

Suggested remote task file:

`report_md/_gpt/REMOTE_105_PHASE_P7_CLOSURE_TASKLIST_20260509.md`

## 6. Track E: Remote 107 Work-2 Gate

Owner: Kimi
Expected duration: 2-4 hours

Context:

107 is the strongest next research direction, but it is Work-2. It must stay separate from Paper-1.

Tasks:

| Step | Requirement |
|---|---|
| E1 | Inspect local clone/review of 107 and record current git commit/branch if available. |
| E2 | Summarize corrected-noise rerun status and identify which previous values are trend-only. |
| E3 | Extract the core mathematical/noise code regions that must be archived for reproducibility. |
| E4 | Require metadata template: commit, env, exact command, dataset split, stride/window, context length, analog layers, noise config, seed semantics, checkpoint, JSON path. |
| E5 | Define Work-2 narrative gate: terminal-layer selective HAT is promising only if corrected-noise rerun preserves last1/last2 robustness. |
| E6 | Prepare a GitHub-safe 107 task file. |

Deliverables:

`report_md/_gpt/KIMI_P7_TRACK_E_REMOTE107_WORK2_GATE_20260509.md`

`report_md/_gpt/REMOTE_107_PHASE_P7_CORRECTED_NOISE_AND_METADATA_TASKLIST_20260509.md`

## 7. Track F: Local GPU Policy

Owner: Kimi
Expected duration: 30-60 minutes now, then execute only if safe

Paper-1 does not need more local GPU training.

Allowed local GPU work:

| Allowed | Condition |
|---|---|
| Reproducibility smoke eval | Must write to sandbox output path, must not update paper source data automatically. |
| Guard-script validation | Must be read-only or temp-output only. |
| Work-2 exploratory dry run | Only if script is isolated from Paper-1 and has kill criteria. |

Disallowed local GPU work:

| Disallowed | Reason |
|---|---|
| Open-ended Paper-1 retraining | Frozen claims would become unstable. |
| Silent overwrite of canonical JSON/CSV | Breaks submission traceability. |
| Any run without exact command and output manifest | Not useful for paper defense. |

Deliverable:

`report_md/_gpt/KIMI_P7_TRACK_F_LOCAL_GPU_POLICY_AND_OPTIONAL_QUEUE_20260509.md`

## 8. Track G: Appendix Visual QA Handoff

Owner: Kimi for audit only; Gemini for user-directed visual edits
Expected duration: 1-2 hours

Tasks:

| Step | Requirement |
|---|---|
| G1 | Do not modify main figures. |
| G2 | Review appendix figures S1-S21 for layout issues only. |
| G3 | Produce a prioritized list of visual issues: overcrowding, small fonts, legend occlusion, inconsistent palettes, empty whitespace, non-vector assets. |
| G4 | Do not change numbers, captions, or claims. |
| G5 | Hand this list to Gemini/user visual lane. |

Deliverable:

`report_md/_gpt/KIMI_P7_TRACK_G_APPENDIX_VISUAL_QA_HANDOFF_20260509.md`

## 9. Track H: Submission Checklist and Reviewer Defense Pack

Owner: Kimi
Expected duration: 2-3 hours

Tasks:

| Step | Requirement |
|---|---|
| H1 | Build a final submission checklist: manuscript, SI, cover letter, source data, README, SHA, BibTeX, figures. |
| H2 | Build a reviewer defense Q&A with the top 12 expected attacks. |
| H3 | Include the exact answer to the 6-bit variance concern. |
| H4 | Include the exact answer to why 107 is not in Paper-1. |
| H5 | Include the exact answer to why 105 is not a blocker. |
| H6 | Include the exact answer to drift definition and why Fresh-minus-24h is wrong. |

Deliverable:

`report_md/_gpt/KIMI_P7_TRACK_H_SUBMISSION_CHECKLIST_AND_DEFENSE_PACK_20260509.md`

## 10. Track I: Workspace Cleanup and Garbage-File Quarantine

Owner: Kimi
Expected duration: 3-6 hours

Context:

The workspace is now too noisy. There are old drafts, build residues, temporary outputs, duplicate bundles, remote clones, deprecated experiment files, and generated artifacts mixed with active submission materials. This is now a project-management risk.

Kimi must not perform destructive cleanup blindly. The first deliverable is a full classification and quarantine plan. Actual deletion is allowed only for clearly disposable build/cache files or after Codex/user acceptance.

Tasks:

| Step | Requirement |
|---|---|
| I1 | Inventory `/home/qiaosir/projects/compute_vit` plus top-level `/home/qiaosir/projects` coordination files. |
| I2 | Group files/directories into: `KEEP_ACTIVE`, `KEEP_CANONICAL_DATA`, `KEEP_RELEASE`, `KEEP_REMOTE_REVIEW`, `KEEP_PROVENANCE`, `QUARANTINE_CANDIDATE`, `DELETE_SAFE`, `UNKNOWN_REVIEW_REQUIRED`. |
| I3 | Produce a size report for large files and directories using `du`/`find`, including any file above 20 MB. |
| I4 | Identify generated LaTeX residues, stale draft files, old temporary reports, duplicate archives, cache folders, and abandoned outputs. |
| I5 | Explicitly protect the final submission bundle, provenance archive, canonical JSON/source data, 105/107 review folders, Git metadata, and active paper sources. |
| I6 | Propose a quarantine directory layout under `archive/cleanup_candidates_20260509/` or equivalent; do not move canonical data there. |
| I7 | If and only if files are obviously disposable build/cache residues, list exact `rm` commands separately under `DELETE_SAFE_COMMANDS`; do not execute them unless the task explicitly says executed. |
| I8 | For every quarantine candidate, explain why it is not needed for active submission or remote continuation. |
| I9 | Produce a reversible cleanup command block using `mkdir -p` and `mv`, not `rm`, for anything uncertain. |
| I10 | After any executed cleanup, rerun final-bundle SHA check and stale-value guard to prove Paper-1 was not damaged. |

Deliverable:

`report_md/_gpt/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md`

Minimum required tables:

| Table | Required columns |
|---|---|
| Directory classification | path, category, reason, safe_to_move, safe_to_delete, owner |
| Large file report | path, size, category, action |
| Delete-safe list | path, reason, exact command |
| Quarantine plan | source, destination, reason, restore command |
| Protected paths | path, why protected, verification command |

Hard protected paths:

| Path | Rule |
|---|---|
| `release_artifacts/paper1_submission_bundle_20260509_final/` | Never delete or mutate without Codex acceptance. |
| `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | Never delete or mutate without Codex acceptance. |
| `release_artifacts/paper1_provenance_archive_20260509/` | Keep as provenance. |
| `paper/latex_gpt/source_data/canonical_json/` | Keep. |
| `paper/latex_gpt/source_data/*.csv` | Keep active source data. |
| `paper/latex_gpt/main.pdf`, `supplementary_main.pdf`, `cover_letter.pdf` | Keep active PDFs. |
| `HAT_105_results_review/` | Keep remote 105 review data. |
| `HAT_107_clean_review/` | Keep remote 107 review data. |
| `.git/` | Never touch. |

## 11. DS Audit Assignment

DS audits after Kimi completes Tracks A-I.

DS must check:

| Check | Requirement |
|---|---|
| DSA1 | Final bundle actually matches P6 locked numbers. |
| DSA2 | Git hygiene plan does not include large binary/checkpoint/data files. |
| DSA3 | 105/107 are correctly separated from Paper-1 claims. |
| DSA4 | No hidden scientific-value mutation by visual work. |
| DSA5 | Reviewer defense pack does not overclaim. |
| DSA6 | Workspace cleanup plan cannot delete canonical data, release artifacts, remote review data, or active paper sources. |
| DSA7 | Any executed cleanup is reversible unless the files are objectively disposable build/cache residues. |

Deliverable:

`report_md/_gpt/DS_PHASE_P7_HOSTILE_RELEASE_AND_REMOTE_AUDIT_20260509.md`

## 12. Mimo Audit Assignment

Mimo audits after Kimi completes Tracks A-I.

Mimo must check:

| Check | Requirement |
|---|---|
| M1 | Submission checklist is complete for a human user. |
| M2 | Data map is understandable and prevents accidental deletion. |
| M3 | Remote task files are executable and not vague. |
| M4 | Defense Q&A is clear and honest. |
| M5 | Appendix visual QA does not drift into scientific edits. |
| M6 | Cleanup plan is understandable to the user and includes restore commands for quarantined files. |

Deliverable:

`report_md/_gpt/MIMO_PHASE_P7_RELEASE_READINESS_AUDIT_20260509.md`

## 13. Gemini Lane

Gemini is visual-only for this phase.

Allowed:

| Allowed | Scope |
|---|---|
| Appendix figure aesthetics | Font size, spacing, legends, palettes, panel layout. |
| Visual prompt generation | For schematic reference images only. |
| PDF visual inspection | Report issues with screenshots or figure names. |

Not allowed:

| Not allowed | Reason |
|---|---|
| Editing source data | Frozen claims. |
| Editing numeric captions | Frozen claims. |
| Changing main scientific values | Frozen claims. |
| Reinterpreting drift definition | Already arbitrated. |

## 14. Codex Acceptance Criteria

Codex will accept P7 only if all are true:

| Criterion | Required result |
|---|---|
| Final freeze certificate | PASS |
| Git commit scope | Conservative and executable |
| Data map v2 | Complete and deletion-safe |
| 105 task file | Specific and non-blocking |
| 107 task file | Specific, metadata-complete, Work-2 only |
| Local GPU policy | No open-ended Paper-1 mutation |
| Appendix visual QA | Clear handoff, no claim drift |
| Reviewer defense pack | Honest and source-supported |
| Workspace cleanup | Protects canonical data and uses quarantine for uncertain files |
| DS audit | PASS or Codex-resolvable conditional pass |
| Mimo audit | PASS or Codex-resolvable conditional pass |

## 15. Final Routing

Kimi should execute P7 as one integrated batch. Do not stop after Track A, Track B, or Track I.

DS and Mimo should wait for Kimi's complete P7 package, then audit independently.

Gemini should continue only the user-directed appendix visual lane.

Codex will perform final acceptance after Kimi + DS + Mimo are complete.
