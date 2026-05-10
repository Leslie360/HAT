# Codex Phased Workflow Protocol

**Date:** 2026-05-09
**Owner:** Codex
**Status:** Active protocol for future project coordination

## 1. Core Rule

Future work proceeds by **phased tasks**, not by parallel role sprawl.

Codex publishes one bounded phase task. Kimi executes the full implementation workload end-to-end. DS and Mimo audit after Kimi finishes. Gemini performs the user-directed second-pass work. The task then returns to Codex for final acceptance, required revisions, and the next phase decision.

## 2. Agent Responsibilities

| Role | Responsibility |
|---|---|
| Codex | Architect, phase owner, task writer, final reviewer, next-phase decision maker |
| Kimi | Primary executor; does the whole phase unless explicitly scoped otherwise |
| DS | Data/protocol/code integrity audit after Kimi delivery |
| Mimo | Reviewer-risk, narrative, consistency, and hostile-review audit after Kimi delivery |
| Gemini | User-directed visual/format/second-pass refinement after DS/Mimo audit |
| User | Approves direction, gives visual taste decisions, allocates remote/GPU resources |

## 3. Standard Phase Lifecycle

1. **Codex Phase Dispatch**
   - One task file under `report_md/_gpt/`.
   - Must state scope, inputs, outputs, kill criteria, and what not to touch.
   - Kimi is the default executor.

2. **Kimi Execution**
   - Kimi completes the phase implementation or experiment queue.
   - Kimi writes one delivery report with changed files, commands, results, and known gaps.

3. **DS + Mimo Audit**
   - DS audits source data, code path, math/protocol correctness, and reproducibility.
   - Mimo audits reviewer risk, narrative consistency, and paper-facing claims.
   - They do not start new unrelated tasks unless Codex dispatches them.

4. **Gemini Second Pass**
   - Gemini only performs the user-directed second pass, especially visuals/layout/polish.
   - Gemini must not change data semantics unless explicitly instructed.

5. **Codex Acceptance Review**
   - Codex reviews Kimi output + DS/Mimo audits + Gemini changes.
   - Codex decides: accept, require revision, or launch the next phase.
   - Codex broadcasts the decision and any new phase task.

## 4. Anti-Patterns Now Disallowed

- Multiple agents independently editing the same target without a phase owner.
- Starting GPU experiments before the phase task defines expected output tables and kill criteria.
- Letting visual edits change data semantics.
- Keeping stale data in captions/tables after protocol changes.
- Treating old dispatches as active after a superseding dispatch is issued.
- Asking Gemini/DS/Mimo to do primary implementation unless Kimi is unavailable or Codex explicitly reassigns.

## 5. Current State After PCM Cleanup

Latest broadcast status:

- Kimi completed new-protocol 6-bit drift closure.
- Mimo completed main-text PCM narrative rewrite.
- Codex completed appendix content repair.
- Supplementary PDF compiles and old 6-bit stale strings are removed.
- Paper-1 PCM freeze is unblocked, pending Codex final acceptance review of all recent changes.

## 6. Next Codex Action

Codex should run a final acceptance review for the completed PCM cleanup phase:

- Check active main text and supplementary for stale 6-bit claims.
- Confirm source-data CSVs are updated or clearly non-canonical if stale.
- Confirm main and supplementary PDFs compile.
- Decide whether the next phase is paper polish, appendix audit, or new experiment dispatch.
