# CC Paper1 Author-Review Tasklist

Date: 2026-05-10
Owner: CC
Assigned by: Codex commander
Status: active

## Objective

Perform a read-only author-review pass on the active Paper1 manuscript after Codex narrative polish pass 2. The goal is to find remaining narrative, claim, consistency, grammar, caption, and submission-readiness issues before Codex refreshes the final release bundle.

## Read scope

CC may read:

- `paper1/manuscript/main.pdf`
- `paper1/manuscript/main.tex`
- `paper1/manuscript/sections/*.tex`
- `paper1/manuscript/supplementary_main.pdf`
- `paper1/manuscript/supplementary_main.tex`
- `paper1/manuscript/supplementary/*.tex`
- `paper1/reports/P8/CODEX_PAPER1_NARRATIVE_POLISH_20260510.md`
- `paper1/release/paper1_submission_bundle_20260509_final/RELEASE_README.md`
- `paper1/release/paper1_submission_bundle_20260509_final/SHA256SUMS.txt`

## Write scope

CC must write only:

- `coordination/agent_reports/Claude/CC_PAPER1_AUTHOR_REVIEW_20260510.md`

Optional supporting TSVs, if needed, may also be written under:

- `coordination/agent_reports/Claude/`

## Hard boundaries

- Do not edit Paper1 TeX, figures, source data, release files, reports, or manifests.
- Do not edit Paper2/107 files.
- Do not edit `/home/qiaosir/projects/remote_reviews/*`.
- Do not run training, evaluation, figure regeneration, checkpoint hashing, or push commands.
- Do not change scientific numbers unless reporting a possible inconsistency for Codex to verify.

## Review questions

1. Does the main-text narrative cleanly separate the IdealDevice algorithmic ablation from the PCM deployment frontier?
2. Are any claims stronger than the evidence supports?
3. Are any old/stale values or stale wording still visible in the active manuscript?
4. Do the figure/table captions match the text and avoid overclaiming?
5. Does the Discussion state limitations clearly enough for reviewer scrutiny?
6. Does the Supplementary Information introduce contradictions with the main text?
7. Is the active manuscript release-ready after prose polish, or are specific edits still recommended?

## Required report format

Use this structure:

```text
# CC Paper1 Author Review — 2026-05-10

## Verdict
release_ready | minor_edits | major_edits

## Blocking Findings
| Severity | File/page | Issue | Recommended fix |

## Nonblocking Polish Notes
| File/page | Note | Suggested wording or action |

## Claim Consistency Checks
| Check | Status | Evidence |

## Supplement/Main Consistency
| Check | Status | Evidence |

## Release Recommendation
One concise paragraph.
```

## Codex integration rule

Codex will integrate only the report. If CC reports `minor_edits`, Codex may patch the active manuscript and rebuild. If CC reports `release_ready`, Codex will refresh the final release bundle and SHA manifest. If CC reports `major_edits`, Codex will pause Paper1 release refresh and resolve the blockers first.
