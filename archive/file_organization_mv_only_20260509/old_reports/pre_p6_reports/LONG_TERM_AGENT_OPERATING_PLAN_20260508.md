# Long-Term Agent Operating Plan

Date: 2026-05-08
Owner: Codex
Scope: Paper-1 closure, local experiment governance, Remote 105/107 coordination, appendix polishing, and Work-2 experiment triage.

## 0. Operating Principle

The team is no longer split by old fixed persona roles. Work is routed by task type.

- Kimi owns high-throughput execution, housekeeping, indexing, repetitive checks, data packaging, and queue maintenance.
- Codex owns precision work: architecture decisions, hard code fixes, reproducibility-critical scripts, final claim arbitration, and difficult figure/script edits.
- DS and Mimo own independent hostile review. They should find bugs, missing controls, weak statistics, and narrative overreach before reviewers do.
- Gemini is reserved for user-directed figure work. Gemini should not independently change claims, task priorities, experiment direction, or source data unless explicitly asked by the user.

This division is mandatory until replaced by a newer dated plan.

## 1. Current North Star

Paper-1 should be closed as a clean, reproducible, visually coherent submission package while experiments continue only where they can strengthen future claims without destabilizing locked Paper-1 conclusions.

Work-2 should remain experiment-first. Remote 107 is the active high-upside line because selective terminal-layer analog KV cache plus HAT has produced the strongest signal. Remote 105 is a validation/data-expansion line, not a writing line.

## 2. Role Boundaries

### Kimi: high-throughput execution and logistics

Kimi should do the work that is broad, repetitive, file-heavy, or bookkeeping-heavy.

Primary responsibilities:
- Maintain data location indices for local, 105, and 107 results.
- Convert returned remote results into normalized Markdown and JSON summaries.
- Keep experiment matrices current: seed, command, commit, dataset, checkpoint path, metric definition, and status.
- Run simple non-destructive checks: missing file scan, manifest scan, figure existence scan, source-data coverage scan, stale placeholder scan.
- Prepare GitHub task packets for 105/107 when Codex defines the experimental question.
- Maintain daily handoff summaries in `report_md/_gpt/` and append concise entries to `AGENT_INTERCOM_HUB_20260428.md`.
- Queue local GPU experiments only after Codex approves priority and kill criteria.

Kimi must not:
- Declare final paper claims without DS/Mimo review and Codex arbitration.
- Rewrite main narrative direction on its own.
- Modify locked canonical numbers unless a provenance-backed correction is approved.
- Launch broad GPU sweeps without a kill criterion and a result-return template.

### Codex: precision implementation and architecture

Codex owns tasks where a small mistake can corrupt the project.

Primary responsibilities:
- Decide experiment priority and stop/continue rules.
- Fix brittle code paths and reproducibility-critical scripts.
- Review and merge external findings from Kimi, DS, Mimo, Gemini, 105, and 107.
- Maintain canonical task packets for remote servers.
- Validate whether a result can support a paper claim or should remain exploratory.
- Perform difficult figure-script edits when the issue is code/layout logic rather than pure aesthetics.
- Run final compile/check gates before any release bundle.
- Keep GitHub usage safe: no broad deletion, no unreviewed main overwrite, no accidental checkpoint/data upload.

Codex must not:
- Spend cycles on large repetitive bookkeeping if Kimi can do it.
- Move Gemini's visual design direction without user request.
- Hide uncertainty; unresolved provenance gaps must be written down.

### DS: hostile technical/statistical review

DS should behave like an adversarial reviewer.

Primary responsibilities:
- Audit code for silent fallback, leakage, seed confusion, metric ambiguity, checkpoint mismatch, and hidden default changes.
- Audit statistics: seed count, confidence/variance, whether differences are meaningful, whether error bars match text.
- Audit experiment protocols: train/test split, fresh-instance semantics, D2D/C2C sampling, MC runs, early stopping, and command reproducibility.
- Review 105/107 result packets before any claim is promoted.
- Produce concise finding lists with severity, file/line when possible, and required remediation.

DS must not:
- Rewrite paper prose as a primary task.
- Launch new experiments unless explicitly assigned.
- Make final strategic calls; DS recommends, Codex arbitrates.

### Mimo: independent reviewer and narrative-risk audit

Mimo should be a second independent review channel, complementary to DS.

Primary responsibilities:
- Read the paper and appendix as a skeptical external reviewer.
- Identify narrative gaps, unclear definitions, acronym problems, unsupported causal language, and over-strong physical claims.
- Check whether figures and captions communicate the intended message without relying on long prose.
- Check whether equations are necessary in the main text or should move to appendix.
- Review final response-to-reviewer style arguments and defense Q&A.

Mimo must not:
- Duplicate DS line-by-line code audit unless asked.
- Make direct large edits to source files without a patch summary.
- Change figures under Gemini/user control.

### Gemini: user-directed visual execution

Gemini is currently a figure specialist under direct user instruction.

Primary responsibilities:
- Iterate main/appendix figures according to user visual feedback.
- Keep visual style consistent: font size, font family, color palette, line weights, legend placement, subplot spacing, panel labels, and vector output where possible.
- Prefer composite top-journal style figures where they improve clarity.
- Maintain figure source scripts and regenerate PDF/PNG outputs as requested.

Gemini must not:
- Change scientific claims or data values without explicit user approval.
- Reprioritize experiments.
- Touch main figures if user says main is locked.
- Perform broad repo cleanup.

## 3. Task Priority Queue

### P0: mandatory stabilization

1. Appendix visual polish under user direction
   - Owner: Gemini.
   - Codex supports only when script-level layout or LaTeX integration is hard.
   - Kimi can maintain a page-by-page appendix issue tracker.
   - DS/Mimo review only after the user says a figure batch is visually acceptable.

2. Paper-1 reproducibility and release hygiene
   - Owner: Kimi for indexing and scans; Codex for final gate.
   - Required outputs:
     - source-data manifest current;
     - figure file coverage current;
     - canonical numbers guard passes;
     - LaTeX compile passes;
     - no stale placeholders;
     - no accidental `.pt`/large data in release bundle;
     - clean README for reproduction.

3. Remote 107 corrected-noise result intake
   - Owner: Kimi normalizes returned files; DS audits protocol; Codex arbitrates claim status.
   - Required fields from 107:
     - Git commit;
     - exact commands;
     - environment;
     - model and tokenizer;
     - dataset split;
     - noise math/code excerpt;
     - D2D/C2C/retention sampling semantics;
     - seed semantics;
     - JSON result paths;
     - aggregate tables;
     - known bug status and whether rerun invalidates prior values.

4. Remote 105 result intake when server returns
   - Owner: Kimi normalizes; DS audits; Codex decides whether it supports Paper-1, Work-2, or only appendix/context.
   - Required fields:
     - same-architecture digital baselines;
     - multi-seed completeness;
     - exact commands;
     - source vs train metric definition;
     - fresh protocol;
     - commit and diff status;
     - JSON/table outputs.

### P1: experiment-forward work

1. Remote 107 selective KV cache route
   - Owner: Codex task design; 107 runs; Kimi records; DS/Mimo review.
   - Near-term experimental priorities:
     - corrected-noise rerun for last1/last2/last4/all-layer;
     - 3-seed stability for best selective setting;
     - fresh-D2D across multiple D2D seeds;
     - C2C and mixed-noise generalization;
     - retention stress if implemented correctly;
     - layer-cost vs PPL trade-off table;
     - exact physical-noise math packet.
   - Promotion criterion: selective setting keeps near-baseline PPL under fresh noise with reproducible metadata and no known noise-math bug.

2. Local Work-2 / PCM line
   - Owner: Codex defines only high-value controls; Kimi may queue; DS audits.
   - Do not burn GPU on broad sweeps without a yes/no question.
   - Good questions:
     - Does a simpler baseline explain the improvement?
     - Does the result hold across seed/checkpoint/device profile?
     - Is precision/drift trade-off still true under corrected code?
   - Bad questions:
     - unbounded hyperparameter search;
     - experiments with no paper decision impact;
     - runs that cannot be reproduced from a command and commit.

3. Paper-1 final review loop
   - Owner: Mimo narrative review, DS technical review, Codex arbitration.
   - Start only after Gemini/user declares figures sufficiently stable.
   - Output should be a short punch list, not a rewrite frenzy.

### P2: optional after P0/P1

- Thesis extraction and bilingual cleanup.
- Reviewer-response boilerplate.
- arXiv companion data package.
- Broader literature update.
- Additional hardware-profile sensitivity after core claims are locked.

## 4. Standard Delivery Format

Every agent report must include this header:

```text
Task ID:
Owner:
Date/time:
Input files read:
Files changed:
Commands run:
Results:
Known caveats:
Next recommended action:
```

For experiment reports, also include:

```text
Git commit:
Git diff status:
Environment:
Dataset and split:
Exact command:
Checkpoint path:
JSON/log paths:
Metric definitions:
Seed semantics:
Early-stop rule:
Kill criterion:
```

For figure reports, also include:

```text
Figure IDs/pages:
Source scripts:
Output PDF/PNG paths:
Style changes:
Compile status:
Visual caveats:
```

## 5. Review Chain

A result is not paper-ready until it passes this chain:

1. Kimi records and normalizes evidence.
2. DS audits protocol and statistics.
3. Mimo audits narrative and reviewer-risk framing.
4. Codex arbitrates final status: `LOCK`, `USE WITH CAVEAT`, `APPENDIX ONLY`, `EXPLORATORY`, or `KILL`.
5. Gemini polishes only the figures that the user chooses to include.

## 6. GPU Policy

GPU time is not automatically valuable. It is useful only if the run answers a decision question.

Allowed GPU run types:
- exact replication of a promising result;
- seed stability of a result already worth promoting;
- controlled ablation that can kill or validate a claim;
- short pilot with explicit kill criterion;
- 107 selective-KV route experiments with clean metadata.

Disallowed GPU run types:
- long sweeps without a claim impact;
- rerunning old bug-contaminated experiments without a corrected protocol;
- runs whose outputs cannot be transferred as compact Markdown/JSON;
- duplicate experiments already assigned to another agent.

## 7. GitHub and Remote Coordination

Codex owns task design and GitHub-facing remote task files. Kimi may prepare drafts after Codex defines the question.

Rules:
- Do not overwrite `main` blindly.
- Do not delete remote-visible files unless the deletion is explicitly listed and justified.
- Do not push large checkpoints unless the user explicitly approves.
- Remote servers should run experiments and return compact Markdown/JSON, not write the local paper.
- Every remote task must include expected output format and minimum metadata.

## 8. Immediate Assignment Snapshot

### Kimi immediate tasks

1. Create/update a single `DATA_LOCATION_INDEX` covering Paper-1 local, 105, and 107.
2. Maintain an appendix figure tracker for S1-S21: page, source script, current status, user complaint, next owner.
3. Normalize any new 105/107 result into tables with exact command/provenance fields.
4. Run non-GPU stale-placeholder/source-data scans after each figure batch.
5. Prepare draft remote task packets only after Codex approves the experimental question.

### Codex immediate tasks

1. Support user/Gemini on hard appendix figure script fixes when requested.
2. Review new 105/107 result packets and decide promotion status.
3. Maintain remote task templates and GitHub safety.
4. Keep final compile/repro gates clean.
5. Arbitrate experiment priority before Kimi queues local GPU runs.

### DS immediate tasks

1. Audit 107 corrected-noise rerun once returned.
2. Audit 105 multi-seed/cross-architecture results once returned.
3. Check whether any Paper-1 figure/table value no longer matches canonical JSON.
4. Flag any remaining silent fallback or metric-definition ambiguity.

### Mimo immediate tasks

1. Review Paper-1 appendix captions after figure layout stabilizes.
2. Identify claims that need softer wording or appendix relocation.
3. Draft reviewer-risk questions for the final locked version.

### Gemini immediate tasks

1. Continue appendix figure visual polish only under user instruction.
2. Do not alter main figures unless explicitly instructed.
3. For each figure batch, report source script, output file, and compile status.

## 9. Conflict Resolution

If two agents conflict:

- Data/provenance conflict: DS investigates first, Codex decides.
- Visual preference conflict: user decides, Gemini implements.
- Experiment priority conflict: Codex decides after DS/Mimo comments.
- Writing/narrative conflict: Mimo reviews, Codex arbitrates, user can override.
- Remote coordination conflict: Codex decides; Kimi records.

## 10. One-Line Rule

Kimi produces throughput, Codex protects correctness, DS and Mimo attack weaknesses, Gemini follows the user on visuals.
