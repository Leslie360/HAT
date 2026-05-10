# CC Thesis EN Completion Tasklist

Date: 2026-05-10
Assigned by: Codex commander
Owner: CC
Status: active

## Objective

Complete the English thesis lane without requiring user relay. Codex owns the Chinese thesis lane and Paper1 release; CC owns English thesis cleanup, consistency review, and build verification.

## Write Scope

CC may edit only:

- `thesis/en/*.tex`
- `thesis/en/README.md`
- `thesis/en/main.pdf` and normal LaTeX build sidecars in `thesis/en/`
- `logs/cc_thesis_en_*`
- `coordination/agent_reports/Claude/CC_THESIS_EN_COMPLETION_20260510.md`

CC must not edit:

- `thesis/cn/`
- `paper1/`
- `paper2/`
- `coordination/remote_tasks/`
- root `BROADCAST.md`
- `/home/qiaosir/projects/remote_reviews/*`

## Required Work

1. Synchronize stale Paper1 claims in `thesis/en/*.tex`.
   - Use current Paper1 main claim framing: Ensemble HAT restores the IdealDevice 4-bit pure-quantization ablation to `86.16\\pm0.19\\%`.
   - Do not keep `86.37\\pm1.54\\%` as the main thesis claim. If it is mentioned at all, label it as an older single-checkpoint/thesis diagnostic, not the Paper1 canonical claim.
   - Update derived deltas where directly attached to the stale number.

2. Normalize toolkit spelling.
   - Use `AIHWKit`, not `AIHWKIT`.

3. Keep Paper2/107 provisional.
   - Do not state 107/KV-cache as claim-locked.
   - Any 107 wording must say pilot/provisional/audit-only until signed manifest or minimal rerun passes.
   - Do not import Paper2/107 numbers into Paper1 claims.

4. Remove "micro-heading" prose style.
   - Avoid a small subsection/subsubsection followed by only one or two short paragraphs.
   - Prefer continuous narrative transitions, paragraph topic sentences, or consolidated larger sections.
   - This applies especially to outlook, discussion, contribution, and Work2/107 sections.

5. Check build dependencies.
   - Keep existing `../latex_gpt` compatibility path unless a build failure proves otherwise.
   - Do not move figures, bibliography files, or large assets.

6. Compile English thesis.
   - Preferred command:
     `cd thesis/en && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex`
   - If that fails due to engine assumptions, try:
     `cd thesis/en && tectonic main.tex`
   - Save logs under `logs/cc_thesis_en_build_20260510.log` or similarly named `logs/cc_thesis_en_*`.

## Required Report

Write:

`coordination/agent_reports/Claude/CC_THESIS_EN_COMPLETION_20260510.md`

Use this structure:

```text
# CC Thesis EN Completion — 2026-05-10

## Verdict
compiled | patched_not_compiled | blocked

## Files Changed
| Path | Summary |

## Claim Sync
| Check | Status | Evidence |

## Build
| Command | Status | Log |

## Remaining Risks
| Risk | Severity | Recommendation |
```

## Coordination Rule

Codex will work in parallel on `thesis/cn/` only. If CC must touch a file outside the English thesis scope, stop and report the need instead of editing.
