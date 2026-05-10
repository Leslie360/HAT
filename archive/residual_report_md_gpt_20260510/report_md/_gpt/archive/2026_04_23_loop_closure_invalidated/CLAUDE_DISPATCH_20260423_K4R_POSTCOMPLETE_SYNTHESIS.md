# Claude Dispatch — K4R Post-Completion Synthesis Prep (2026-04-23)

## Context
- Branch A is canonical.
- K4R is the first live canonical Branch A run.
- Codex is monitoring live runtime and GPU provenance.
- Kimi is handling K4R contamination scrub / completion packet prep.
- Gemini is handling the open second-order coefficient ruling.

## Your role
Do NOT start new scientific review from scratch.
Do NOT reinterpret stale pre-Branch-A numbers.
Prepare the synthesis shell that will be filled once:
1. K4R training completes
2. K4R fresh eval completes
3. Gemini returns the second-order coefficient ruling

## Deliverables
Produce exactly two files.

### 1. `CLAUDE_K4R_SYNTHESIS_TEMPLATE_20260423.md`
Purpose:
- final one-page synthesis shell for project state after K4R

Required sections:
- `Canonical code state`
- `K4R source-domain summary`
- `K4R fresh-instance summary`
- `Second-order theory status`
- `Route decision impact`
- `Required manuscript/rebuttal wording changes`
- `Next GPU action: resume / pause / reroute`

Use placeholders, not invented numbers.

### 2. `CLAUDE_RULE_B_PATCH_MATRIX_20260423.md`
Purpose:
- pre-approve or block likely Branch A-facing document patches once K4R finishes

At minimum classify these as:
- `allowed now`
- `allowed after K4R`
- `frozen / do not touch`

Audit targets:
- `paper/latex_gpt/supplementary.tex`
- `paper/latex_gpt/sections/03_methodology.tex`
- `report_md/_gpt/CODEX_ROUTE_DECISION_20260422.md`
- `远端/REMOTE_ROUTE_DECISION_20260422.md`
- `远端/REMOTE_HANDOFF_PACKET_20260422.md`

## Hard rules
- No new experiment design.
- No new result interpretation beyond current canonical Branch A constraints.
- No reuse of stale `cx_k4_*alpha_0p25` JSON evidence.
