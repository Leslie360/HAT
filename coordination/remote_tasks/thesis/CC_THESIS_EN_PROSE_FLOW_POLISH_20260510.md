# CC Thesis EN Prose-Flow Polish Tasklist

Date: 2026-05-10
Assigned by: Codex commander
Owner: CC
Status: active

## Objective

Polish the active English thesis prose structure so it does not read like short AI-generated blocks under many small headings. Preserve the current scientific claims and build-clean state.

## Write Scope

CC may edit only:

- `thesis/en/*.tex`
- `thesis/en/README.md`
- `thesis/en/main.pdf` and normal LaTeX build sidecars in `thesis/en/`
- `logs/cc_thesis_en_style_*`
- `coordination/agent_reports/Claude/CC_THESIS_EN_PROSE_FLOW_POLISH_20260510.md`

CC must not edit:

- `thesis/cn/`
- `paper1/`
- `paper2/`
- `coordination/remote_tasks/`
- root `BROADCAST.md`
- `/home/qiaosir/projects/remote_reviews/*`

## Required Work

1. Remove micro-heading prose in active EN chapters.
   - Avoid `\subsection` blocks that contain only a few sentences.
   - Merge such blocks into larger sections using topic sentences and transitions.
   - Priority files: `chapter_1_hat_instance_overfitting.tex`, `chapter_3_hat_taxonomy.tex`, `chapter_4_failure_modes.tex`, `chapter_6_physical_realism.tex`, and `chapter_7_deployment.tex`.

2. Preserve scientific discipline.
   - Keep Paper1 claim framing at `86.16\pm0.19\%`.
   - Keep 107/KV-cache provisional/audit-only.
   - Do not reintroduce `86.37`, `1.54`, `AIHWKIT`, or locked Paper2 language.

3. Preserve build cleanliness.
   - Latest Codex integration build has no undefined citation/reference/error hits in `thesis/en/main.log`.
   - Do not remove the `sec:heavy-tailed` label or refreshed bibliography state.
   - Rebuild after prose changes.

4. Compile English thesis.
   - Preferred command:
     `latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=/home/qiaosir/projects/compute_vit/thesis/en /home/qiaosir/projects/compute_vit/thesis/en/main.tex`
   - Save logs under `logs/cc_thesis_en_style_build_20260510.log` or similarly named `logs/cc_thesis_en_style_*`.

## Required Report

Write:

`coordination/agent_reports/Claude/CC_THESIS_EN_PROSE_FLOW_POLISH_20260510.md`

Use this structure:

```text
# CC Thesis EN Prose-Flow Polish — 2026-05-10

## Verdict
compiled | patched_not_compiled | blocked

## Files Changed
| Path | Summary |

## Style Checks
| Check | Status | Evidence |

## Claim Discipline
| Check | Status | Evidence |

## Build
| Command | Status | Log |

## Remaining Risks
| Risk | Severity | Recommendation |
```

## Coordination Rule

Codex will not edit `thesis/en/` while this follow-up EN prose-flow task is active. If CC must touch a file outside the English thesis scope, stop and report the need instead of editing.
