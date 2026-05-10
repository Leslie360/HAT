# Dispatch Superphase P8: Ultra-Long Manuscript, Repo, Remote, and Work-2 Pipeline

Date: 2026-05-09 21:45 Asia/Shanghai
Issued by: Codex
Primary executor: Kimi
Auditors: DS and Mimo
Visual lane: Gemini, user-directed only
Remote lanes: 105 and 107 via task files
Codex role: final arbitration and high-risk edits

## 0. Why P8 Exists

P7 is accepted. The project is now submission-ready, but the workspace and downstream work remain too fragmented. P8 is intentionally large so the user does not need to keep issuing small commands.

P8 must run as one integrated batch. Do not stop after one or two reports.

## 1. Non-Negotiable Rules

| Rule | Meaning |
|---|---|
| Paper-1 numbers are frozen | No numerical value, source CSV, canonical JSON, or scientific caption changes without Codex acceptance. |
| Main figures are frozen unless user asks | Do not touch `main.pdf` figures casually. |
| Narrative edits are allowed | Text can be made more natural if numbers/citations/claims are preserved. |
| Cleanup must be reversible | Use quarantine for uncertain files. |
| Remote 105 is supplement/defense | It does not block Paper-1 submission. |
| Remote 107 is Work-2 | It must not be injected into Paper-1 claims. |
| Every result needs metadata | Commit, command, env, seed, output path. |

## 2. Current State From Broadcast

| Item | Status |
|---|---|
| P7 Kimi package | Complete, Tracks A-I delivered. |
| DS P7 audit | PASS. |
| Mimo P7 audit | PASS. |
| Final bundle | SHA verified, stale values resolved. |
| Cleanup | Planned but not fully executed. |
| Gemini latest item | ACTION_REQUIRED: manuscript has several AI-smell/abrupt narrative transitions. |
| Local GPU | No open-ended Paper-1 GPU work justified. |
| 105 | Waiting for final server recovery/results. |
| 107 | Corrected-noise Work-2 rerun should continue separately. |

## 3. P8 Deliverables Overview

Kimi must produce all of the following before asking for Codex acceptance:

| Track | Deliverable |
|---|---|
| A | `KIMI_P8_TRACK_A_NARRATIVE_DESLOP_REWRITE_20260509.md` |
| B | `KIMI_P8_TRACK_B_APPENDIX_TEXT_AND_TABLE_CONSISTENCY_20260509.md` |
| C | `KIMI_P8_TRACK_C_CLEANUP_EXECUTION_OR_DRYRUN_20260509.md` |
| D | `KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md` |
| E | `KIMI_P8_TRACK_E_FINAL_BUNDLE_REFRESH_IF_NEEDED_20260509.md` |
| F | `KIMI_P8_TRACK_F_REMOTE105_INGESTION_READY_PACKET_20260509.md` |
| G | `KIMI_P8_TRACK_G_REMOTE107_WORK2_READY_PACKET_20260509.md` |
| H | `KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md` |
| I | `KIMI_P8_TRACK_I_LOCAL_GPU_AND_WORK2_OPTIONAL_QUEUE_20260509.md` |
| J | `KIMI_P8_TRACK_J_FINAL_USER_HANDOFF_MAP_20260509.md` |
| Self-audit | `KIMI_P8_SELF_AUDIT_20260509.md` |

DS and Mimo audit after all Kimi tracks are done.

## 4. Track A: Narrative De-AI-Smell Rewrite

Owner: Kimi
Priority: High
Expected duration: 2-4 hours

Gemini reported ACTION_REQUIRED. Kimi should make the manuscript read less mechanical without touching scientific values.

Files/locations to inspect first:

| File | Target |
|---|---|
| `paper/latex_gpt/sections/05_results.tex` | Subsection `Iso-Accuracy Operating Envelope`. |
| `paper/latex_gpt/supplementary.tex` | Subsubsection `Uniform vs. State-Dependent Retention Comparison`. |
| `paper/latex_gpt/supplementary/S_mechanism_empirical.tex` | `S-M.2 Per-layer D2D sensitivity (E4)`. |
| `paper/latex_gpt/supplementary/S_mechanism_empirical.tex` | `S-M.5 Checkpoint averaging ablation (E5)`. |
| Main section headers | Add 1-2 natural overview sentences under `Results`, `Discussion`, and `Methodology` only if absent and useful. |

Rewrite rules:

| Allowed | Forbidden |
|---|---|
| Add connective academic prose. | Change numbers. |
| Merge abrupt 1-sentence paragraphs into smoother argument. | Change table/figure labels unless broken. |
| Reduce AI-like signposting. | Add unsupported claims. |
| Preserve citations. | Move 107/105 into Paper-1 claims. |
| Keep text concise. | Add equations unless needed. |

Verification:

| Check | Required |
|---|---|
| `git diff -- paper/latex_gpt/...` | Diff must show text-only narrative changes. |
| Stale-value grep | 0 hits for old values. |
| LaTeX compile | Rebuild affected PDFs. |
| Claim audit | No new scientific claims. |

Deliverable must include exact before/after summary and compile logs.

## 5. Track B: Appendix Text/Table Consistency Pass

Owner: Kimi
Priority: High
Expected duration: 2-4 hours

Scope is not visual redesign; Gemini/user own the visual lane. Kimi handles text/table consistency.

Tasks:

| Step | Requirement |
|---|---|
| B1 | Check all supplementary table font commands after Gemini's global `\small` replacement. |
| B2 | Confirm no table became too wide or unreadable after font normalization. |
| B3 | Check table captions for stale wording, undefined abbreviations, missing units, percentage vs decimal inconsistency. |
| B4 | Check abbreviation first-use in main and SI: HAT, PCM, C2C, D2D, STE, PPL, KV, MC. |
| B5 | Check whether any table has blank cells without explanation. |
| B6 | Do not touch figure aesthetics unless it is a caption/text issue. |

Deliverable:

`report_md/_gpt/KIMI_P8_TRACK_B_APPENDIX_TEXT_AND_TABLE_CONSISTENCY_20260509.md`

## 6. Track C: Cleanup Execution or Dry Run

Owner: Kimi
Priority: High
Expected duration: 2-5 hours

Use P7 Track I as input. This track should either execute safe cleanup or produce a command-ready dry run if any uncertainty remains.

Tasks:

| Step | Requirement |
|---|---|
| C1 | Re-read `KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md`. |
| C2 | Execute only DELETE_SAFE commands that are objectively disposable: pycache, LaTeX aux/log/fls/fdb_latexmk, temporary extraction folders. |
| C3 | Quarantine uncertain files with `mv` into `archive/cleanup_candidates_20260509/`, not `rm`. |
| C4 | Do not move or delete protected paths from P7. |
| C5 | For the Chinese PPT unknown item, do not delete; make a user-decision note. |
| C6 | After cleanup/quarantine, rerun final bundle SHA check, stale-value grep, and PCM guard. |
| C7 | Write restore commands for every quarantined item. |

If Kimi chooses dry-run only, explain exactly why execution was unsafe.

Deliverable:

`report_md/_gpt/KIMI_P8_TRACK_C_CLEANUP_EXECUTION_OR_DRYRUN_20260509.md`

## 7. Track D: Git Release Branch Preparation

Owner: Kimi
Priority: High
Expected duration: 2-4 hours

Goal: prepare a clean commit/push path without executing push unless user/Codex approves.

Tasks:

| Step | Requirement |
|---|---|
| D1 | Produce final `git status --short` after cleanup/text edits. |
| D2 | Categorize every changed/untracked path into commit, exclude, or user-decision. |
| D3 | Confirm no `.pt`, `.pth`, `.ckpt`, datasets, raw checkpoints, raw huge logs, or private files are in commit scope. |
| D4 | Produce exact branch name proposal: `paper1-final-freeze-20260509` or safer equivalent. |
| D5 | Produce exact non-interactive command block for branch creation, staging, commit, and push. |
| D6 | Do not run `git reset --hard`, `git checkout --`, or destructive cleanup. |

Deliverable:

`report_md/_gpt/KIMI_P8_TRACK_D_GIT_RELEASE_BRANCH_PREP_20260509.md`

## 8. Track E: Final Bundle Refresh If Needed

Owner: Kimi
Priority: High if Track A/B changed LaTeX; otherwise Medium
Expected duration: 1-3 hours

If narrative or appendix text changed, final bundle must be refreshed. If no source changed, prove no refresh is needed.

Tasks:

| Step | Requirement |
|---|---|
| E1 | Rebuild `main.pdf`, `supplementary_main.pdf`, and `cover_letter.pdf` if relevant files changed. |
| E2 | Resync changed source/PDF files into `release_artifacts/paper1_submission_bundle_20260509_final/`. |
| E3 | Refresh `MANIFEST_FILES.txt` and `SHA256SUMS.txt`. |
| E4 | Recreate `paper1_submission_bundle_20260509_final.tar.gz`. |
| E5 | Cold-unpack and verify SHA. |
| E6 | Run stale-value grep/PDF text scan. |
| E7 | Record final tarball hash and size. |

Deliverable:

`report_md/_gpt/KIMI_P8_TRACK_E_FINAL_BUNDLE_REFRESH_IF_NEEDED_20260509.md`

## 9. Track F: Remote 105 Ingestion Ready Packet

Owner: Kimi
Priority: Medium
Expected duration: 1-2 hours now; update after 105 returns

Use remote task file:

`report_md/_gpt/REMOTE_105_PHASE_P8_FINAL_INGESTION_TASKLIST_20260509.md`

Tasks:

| Step | Requirement |
|---|---|
| F1 | Ensure 105 task file exists and is clear enough for server agent. |
| F2 | Prepare a short message the user can paste to 105. |
| F3 | Define exactly what data will be accepted into supplement and what remains defense-only. |
| F4 | Make clear 105 is not a Paper-1 submission blocker. |
| F5 | If latest 105 files are already in local clone, update the local status table. |

Deliverable:

`report_md/_gpt/KIMI_P8_TRACK_F_REMOTE105_INGESTION_READY_PACKET_20260509.md`

## 10. Track G: Remote 107 Work-2 Ready Packet

Owner: Kimi
Priority: High for future research, non-blocking for Paper-1
Expected duration: 2-4 hours

Use remote task file:

`report_md/_gpt/REMOTE_107_PHASE_P8_CORRECTED_NOISE_WORK2_TASKLIST_20260509.md`

Tasks:

| Step | Requirement |
|---|---|
| G1 | Inspect latest local 107 clone/review folders. |
| G2 | Record current branch/commit if available. |
| G3 | Identify corrected-noise results vs old bugged/trend-only results. |
| G4 | List exact missing reruns for last1/last2/last4/all24. |
| G5 | Extract/quote minimal core math code locations, not large files. |
| G6 | Prepare a user-paste message for 107. |
| G7 | Keep all 107 claims labeled Work-2 only. |

Deliverable:

`report_md/_gpt/KIMI_P8_TRACK_G_REMOTE107_WORK2_READY_PACKET_20260509.md`

## 11. Track H: Thesis and Master-Data Extraction Map

Owner: Kimi
Priority: Medium
Expected duration: 2-4 hours

The user mentioned thesis/master documents may contain 105/107 data. We need data extraction only, not thesis writing quality.

Tasks:

| Step | Requirement |
|---|---|
| H1 | Locate thesis/master-data directories under `/home/qiaosir/projects` and `compute_vit`. |
| H2 | Identify tables/figures containing 105/107, PCM, HAT, KV-cache, TinyImageNet, WikiText, or PPL data. |
| H3 | Extract a data-location index: file, page/section if available, dataset, metric, numbers, status. |
| H4 | Mark whether each number is canonical, provisional, bugged/trend-only, or unknown. |
| H5 | Do not rewrite thesis text. |
| H6 | Flag contradictions against Paper-1 locked values. |

Deliverable:

`report_md/_gpt/KIMI_P8_TRACK_H_THESIS_AND_MASTER_DATA_EXTRACTION_MAP_20260509.md`

## 12. Track I: Local GPU and Work-2 Optional Queue

Owner: Kimi
Priority: Low for Paper-1, Medium for Work-2
Expected duration: 1-2 hours planning; execution only if safe

Paper-1 local GPU remains closed. However, Kimi should define optional GPU tasks if GPU is idle and the user wants no resource waste.

Allowed optional jobs:

| Job | Condition | Output |
|---|---|---|
| Paper-1 guard smoke eval | Read-only/temp output only | PASS/FAIL, no source-data mutation |
| 107 local smoke test | Only if 107 code runs locally without large downloads | command + log |
| Figure/source-data regeneration check | CPU preferred | diff/no-diff report |
| Tiny self-contained repro test | No new claims | environment sanity |

Forbidden jobs:

| Job | Reason |
|---|---|
| Open-ended Paper-1 retraining | Frozen claims. |
| Any run that overwrites canonical JSON/CSV | Submission traceability risk. |
| Any run without metadata | Useless for defense. |

Deliverable:

`report_md/_gpt/KIMI_P8_TRACK_I_LOCAL_GPU_AND_WORK2_OPTIONAL_QUEUE_20260509.md`

## 13. Track J: Final User Handoff Map

Owner: Kimi
Priority: High
Expected duration: 1-2 hours

Produce one user-facing map that answers where everything is and what to do next.

Required sections:

| Section | Content |
|---|---|
| Submission package | final bundle/tarball paths, PDF paths, SHA status. |
| If user wants to submit | exact files to upload. |
| If user wants to push GitHub | exact command block, branch, commit message. |
| If user wants to clean files | exact safe commands and restore commands. |
| If user wants to ask 105 | paste-ready message. |
| If user wants to ask 107 | paste-ready message. |
| If user wants Gemini to continue figures | appendix visual issue list. |
| If user wants Codex final check | what to ask. |

Deliverable:

`report_md/_gpt/KIMI_P8_TRACK_J_FINAL_USER_HANDOFF_MAP_20260509.md`

## 14. DS P8 Audit Assignment

DS audits after Kimi completes Tracks A-J.

Deliverable:

`report_md/_gpt/DS_PHASE_P8_HOSTILE_FINALIZATION_AUDIT_20260509.md`

DS must verify:

| Check | Requirement |
|---|---|
| DS1 | Narrative rewrites did not change claims/numbers. |
| DS2 | Final bundle, if refreshed, SHA passes and stale scans clean. |
| DS3 | Cleanup did not touch protected paths. |
| DS4 | Git commit scope excludes large/private/checkpoint files. |
| DS5 | 105/107 remain properly scoped. |
| DS6 | Thesis extraction map labels noncanonical data honestly. |
| DS7 | No Paper-1 GPU reopening happened silently. |

## 15. Mimo P8 Audit Assignment

Mimo audits after Kimi completes Tracks A-J.

Deliverable:

`report_md/_gpt/MIMO_PHASE_P8_USER_READINESS_AUDIT_20260509.md`

Mimo must verify:

| Check | Requirement |
|---|---|
| M1 | User handoff map is understandable. |
| M2 | Narrative edits improve flow and do not sound mechanical. |
| M3 | Cleanup instructions are safe for a non-expert user. |
| M4 | 105/107 paste messages are executable and not vague. |
| M5 | Appendix/table consistency pass improves readability. |
| M6 | Any remaining user decisions are listed explicitly. |

## 16. Gemini Lane

Gemini remains visual/user-directed. It may:

| Allowed | Notes |
|---|---|
| Continue appendix figure aesthetics | Fonts, legends, spacing, colors, panel layout. |
| Report AI-smell issues | Already did; Kimi executes text changes unless user asks Codex directly. |
| Inspect PDFs visually | Should not mutate numbers/captions/source data. |

Gemini must not:

| Forbidden | Reason |
|---|---|
| Change scientific values | Frozen. |
| Change source CSV/JSON | Frozen. |
| Reinterpret drift | Already arbitrated. |
| Add 105/107 to Paper-1 claims | Scope separation. |

## 17. Codex Acceptance Criteria

Codex will accept P8 only if:

| Criterion | Required result |
|---|---|
| Kimi Tracks A-J | All present. |
| DS audit | PASS or resolvable conditional pass. |
| Mimo audit | PASS or resolvable conditional pass. |
| Final bundle | If changed, SHA refreshed and verified. |
| Stale scans | Clean. |
| Paper-1 values | Frozen values preserved. |
| Cleanup | Safe and reversible except disposable residues. |
| Git plan | Command-ready and conservative. |
| 105/107 | Ready to send, scoped correctly. |
| User handoff | Clear enough that the user can act without asking where files are. |

## 18. Final Instruction

Kimi: execute P8 as one large batch. Do not stop after narrative edits or cleanup. Produce all Tracks A-J plus self-audit.

DS/Mimo: wait for Kimi's complete P8 package, then audit independently.

Gemini: continue only user-directed visual work.

Codex: final acceptance after all reports are in.
