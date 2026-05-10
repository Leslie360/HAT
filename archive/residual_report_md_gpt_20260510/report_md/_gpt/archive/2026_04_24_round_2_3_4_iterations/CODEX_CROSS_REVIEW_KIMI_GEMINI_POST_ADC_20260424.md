# CODEX Cross-Review: Kimi + Gemini Post-ADC

- Date: 2026-04-24
- Reviewer: Codex
- Scope:
  - [05_results.tex.kimi_draft_v3](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex.kimi_draft_v3)
  - [S_theory_ensemble_hat.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex)
  - [KIMI_THEORY_1_COMPLETE_20260424.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/KIMI_THEORY_1_COMPLETE_20260424.md)
  - [KIMI_CROSS_REVIEW_BROADCAST_20260424.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/KIMI_CROSS_REVIEW_BROADCAST_20260424.md)
  - [GEMINI_AUDIT_KIMI_DRAFT_V3_20260424.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/GEMINI_AUDIT_KIMI_DRAFT_V3_20260424.md)
  - [GEMINI_G_AUDIT_CODE_20260424.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/GEMINI_G_AUDIT_CODE_20260424.md)
  - [DISPATCH_KIMI_ROUND2_20260424.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/DISPATCH_KIMI_ROUND2_20260424.md)
  - [DISPATCH_GEMINI_G_AUDIT_ADC_HOOK_20260424.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/DISPATCH_GEMINI_G_AUDIT_ADC_HOOK_20260424.md)
  - [AGENT_SYNC_gpt.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md)

## Findings

### 1. `05_results.tex.kimi_draft_v3` is still pre-trigger and not integration-ready after the ADC dual report
- Severity: High
- Evidence:
  - [05_results.tex.kimi_draft_v3:103](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex.kimi_draft_v3#L103) still says “ADC-on deployment-fidelity columns to be added after Codex ADC ablation completes.”
  - [05_results.tex.kimi_draft_v3:105](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex.kimi_draft_v3#L105) through [05_results.tex.kimi_draft_v3:114](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex.kimi_draft_v3#L114) remain a single-column ADC-off table.
  - [05_results.tex.kimi_draft_v3:119](/home/qiaosir/projects/compute_vit/paper/latex_gpt/sections/05_results.tex.kimi_draft_v3#L119) still headlines `82.03%` instead of the ADC-on 8-bit headline required by the dispatch.
  - [DISPATCH_KIMI_ROUND2_20260424.md:116](/home/qiaosir/projects/compute_vit/report_md/_gpt/DISPATCH_KIMI_ROUND2_20260424.md#L116) through [DISPATCH_KIMI_ROUND2_20260424.md:127](/home/qiaosir/projects/compute_vit/report_md/_gpt/DISPATCH_KIMI_ROUND2_20260424.md#L127) explicitly require the dual-column table and in-place overwrite after Codex signals completion.
  - [AGENT_SYNC_gpt.md:25926](/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md#L25926) through [AGENT_SYNC_gpt.md:25945](/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md#L25945) show the trigger was issued at 20:39 CST.
- Verdict:
  - Kimi Part B is not done yet. Any claim that §5.7 is integration-ready is currently false.

### 2. Gemini’s required D4 hook audit is still missing
- Severity: High
- Evidence:
  - [DISPATCH_GEMINI_G_AUDIT_ADC_HOOK_20260424.md:89](/home/qiaosir/projects/compute_vit/report_md/_gpt/DISPATCH_GEMINI_G_AUDIT_ADC_HOOK_20260424.md#L89) defines the required deliverable as `report_md/_gpt/GEMINI_G_AUDIT_ADC_HOOK_20260424.md`.
  - The file does not exist in the workspace.
  - [AGENT_SYNC_gpt.md:25944](/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md#L25944) through [AGENT_SYNC_gpt.md:25945](/home/qiaosir/projects/compute_vit/report_md/_gpt/AGENT_SYNC_gpt.md#L25945) show Codex unblocked Gemini, but there is no subsequent `G-AUDIT-ADC-HOOK COMPLETE` status block.
- Verdict:
  - Claude’s D4 gate remains open. ADC-on numbers can be reported, but they are not yet hook-audited to the standard Claude requested.

### 3. Kimi’s coordination summaries still contain stale or incorrect statements that can re-contaminate downstream writing
- Severity: Medium
- Evidence:
  - [KIMI_CROSS_REVIEW_BROADCAST_20260424.md:65](/home/qiaosir/projects/compute_vit/report_md/_gpt/KIMI_CROSS_REVIEW_BROADCAST_20260424.md#L65) and [KIMI_CROSS_REVIEW_BROADCAST_20260424.md:77](/home/qiaosir/projects/compute_vit/report_md/_gpt/KIMI_CROSS_REVIEW_BROADCAST_20260424.md#L77) still use `ADCContext`, but the correct class name is `ADCQuantHookManager`.
  - [KIMI_THEORY_1_COMPLETE_20260424.md:30](/home/qiaosir/projects/compute_vit/report_md/_gpt/KIMI_THEORY_1_COMPLETE_20260424.md#L30) says the Wager analogy is “exact,” and [KIMI_THEORY_1_COMPLETE_20260424.md:31](/home/qiaosir/projects/compute_vit/report_md/_gpt/KIMI_THEORY_1_COMPLETE_20260424.md#L31) reintroduces empirical `-1.76 pp` / `-4.20 pp` numbers into the theory summary log.
  - The source theory deliverable itself, [S_theory_ensemble_hat.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex), is clean; the contamination is in the summary/broadcast layer, not the actual manuscript-side source.
- Verdict:
  - The theory source file passes, but Kimi’s meta-docs are not fully scrubbed. They should not be treated as integration-safe references.

### 4. Gemini’s approval of Kimi’s draft is outdated and overstates readiness
- Severity: Medium
- Evidence:
  - [GEMINI_AUDIT_KIMI_DRAFT_V3_20260424.md:4](/home/qiaosir/projects/compute_vit/report_md/_gpt/GEMINI_AUDIT_KIMI_DRAFT_V3_20260424.md#L4) scopes the abstract audit to `00_abstract.tex.kimi_draft_v2`, not the newer v3 sidecar.
  - [GEMINI_AUDIT_KIMI_DRAFT_V3_20260424.md:47](/home/qiaosir/projects/compute_vit/report_md/_gpt/GEMINI_AUDIT_KIMI_DRAFT_V3_20260424.md#L47) declares the Results skeleton “ready for integration” before Kimi Part B and Gemini Part D4 were complete.
  - [GEMINI_AUDIT_KIMI_DRAFT_V3_20260424.md:36](/home/qiaosir/projects/compute_vit/report_md/_gpt/GEMINI_AUDIT_KIMI_DRAFT_V3_20260424.md#L36) positively endorses bug-retrospective wording that Claude’s Round-2 dispatch explicitly asked Kimi to strip from §5.7 body language.
- Verdict:
  - Gemini’s audit is useful as a snapshot of the pre-ADC-dual-report state, but it is not a current release gate.

## Clean Passes

### Kimi source theory deliverable
- [S_theory_ensemble_hat.tex](/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary/S_theory_ensemble_hat.tex) no longer contains the banned empirical numbers, no longer uses “exact analogy,” and includes the C2C / Gauss-Newton qualification in the manuscript-side source.

### Gemini code audit on the `1 < NL < 2` risk
- [GEMINI_G_AUDIT_CODE_20260424.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/GEMINI_G_AUDIT_CODE_20260424.md) correctly identified the second-order instability.
- That finding has already been patched and validated in [CODEX_NL_GUARD_PATCH_REPORT_20260424.md](/home/qiaosir/projects/compute_vit/report_md/_gpt/CODEX_NL_GUARD_PATCH_REPORT_20260424.md).

## Recommendations

1. Kimi should execute Part B exactly as dispatched:
   - replace the ADC-off-only table with the dual-column table,
   - switch the body headline to ADC-on 8-bit,
   - keep ADC-off as surrogate baseline only.
2. Gemini should deliver the missing D4 report before anyone cites ADC-on as fully hook-audited headline evidence.
3. Kimi should scrub `ADCContext` and stale theory-summary numbers from coordination docs to avoid accidental reuse in manuscript text or broadcasts.
4. Claude should treat Kimi/Gemini current outputs as “directionally aligned but not fully closed” rather than fully integrated.
