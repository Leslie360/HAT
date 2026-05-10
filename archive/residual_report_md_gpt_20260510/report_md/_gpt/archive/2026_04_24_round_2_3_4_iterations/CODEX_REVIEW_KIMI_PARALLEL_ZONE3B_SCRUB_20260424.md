# CODEX_REVIEW_KIMI_PARALLEL_ZONE3B_SCRUB_20260424
**Date:** 2026-04-24 22:02 CST
**Reviewer:** Codex
**Scope:** Kimi `BROADCAST_KIMI_PARALLEL_ZONE3B_SCRUB_COMPLETE_20260424.md` plus claimed EN/CN thesis sidecars and paper LaTeX edits
**Verdict:** **Partial pass, not final integration-ready.** Kimi fixed the two old severe-NL numeric contaminants in EN Chapter 5 draft, but the broadcast overstates cleanliness. ADC fidelity wording and old groupwise-NL evidence remain unsafe.

---

## Findings

### F1 - HIGH - ADC deployment-fidelity language remains in EN/CN thesis drafts
Kimi's scrub targets Zone-3B severe-NL numbers, but it does not resolve the later Gemini/Codex ADC hook-fidelity finding. Current hook-based ADC results must not be described as deployment-fidelity.

Remaining unsafe lines:

- `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3:112` still says deployment-fidelity 8-bit ADC is injected through inference-time hooks.
- `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3:183` still captions the M-series table as deployment-fidelity 8-bit ADC quantization.
- `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3:205` still claims deployment-fidelity 8-bit ADC does not materially alter the headline.
- `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3:351` still makes the 8-bit ADC-on `-0.10 pp` headline claim.
- `paper/thesis_cn/chapter_5_failure_modes.tex.kimi_draft_v3:115` still says 8bit ADC-on is only `~0.10 pp` below ADC-off.

Required fix: relabel current ADC-on values as "post-module-output hook diagnostic" or remove them from thesis headline claims until the physical ADC boundary and calibration-loader issues are patched and rerun.

### F2 - HIGH - Supplementary groupwise-NL table still retains invalidated evidence
Kimi's paper-side scrub only flags row (b) of the supplementary NL ablation as Zone 3B, but the same table still contains historical groupwise protected results:

- `paper/latex_gpt/supplementary.tex:774` table caption flags only the unprotected baseline row as Zone 3B.
- `paper/latex_gpt/supplementary.tex:783` row (b) is marked with `^\dagger`.
- `paper/latex_gpt/supplementary.tex:784` MLP-only `87.79/86.22` is not marked invalidated.
- `paper/latex_gpt/supplementary.tex:785` QKV-only `18.72/10.15` is not marked invalidated.
- `paper/latex_gpt/supplementary.tex:786` attention-proj `18.86/~10.25` is not marked invalidated.
- `paper/latex_gpt/supplementary.tex:787` all-linear `87.49/84.81` is not marked invalidated.
- `paper/latex_gpt/supplementary.tex:792` still interprets these rows as localizing the NL bottleneck to the MLP path.

This is unsafe because historical `group != all` results were affected by the config-sharing bug and the pre-fix STE semantics. If the paper keeps this table, all historical groupwise rows must be marked as pre-fix diagnostic only, or the table should be replaced by a post-fix gradient-diagnostic result with its own provenance.

Required fix: do not use this table to claim MLP-path localization unless it is explicitly tied to a post-fix deterministic gradient diagnostic. Remove or reword `paper/latex_gpt/supplementary.tex:792`.

### F3 - MEDIUM - Broadcast "zero un-scrubbed zone 3B claims remain" is too broad
The broadcast says "zero un-scrubbed zone 3B claims remain in any draft or canonical file", but original canonical thesis files are intentionally preserved and still contain old claims:

- `paper/thesis/chapter_5_mitigation.tex:1` old erratum and pre-fix warning remain.
- `paper/thesis/chapter_5_mitigation.tex:30` old MLP-linear/all-linear/joint severe-NL structural-limit narrative remains.
- `paper/thesis_cn/chapter_5_failure_modes.tex:4` old bug-contaminated severe-NL warning remains.
- `paper/thesis_cn/chapter_5_failure_modes.tex:33` old `38.95%` J1d/K2-style result remains.

Kimi states these originals are "preserved as history", which is acceptable only if Claude never ingests them as canonical. The broadcast wording should say "sidecars and selected paper canonical files are scrubbed; original thesis canonical files remain superseded history."

### F4 - MEDIUM - Verification grep is incomplete
Kimi's grep excludes several hazards:

- It does not grep `paper/latex_gpt/supplementary.tex` in the first numeric block, even though that file still contains old groupwise numbers.
- It does not search `87.79`, `18.72`, `18.86`, `87.49`, or old groupwise labels.
- It does not search ADC-fidelity terms such as `deployment-fidelity`, `ADC-on headline`, or `-0.10`.
- It searches draft sidecars but not original thesis canonical files, while the broadcast uses corpus-wide language.

Required fix: expand the grep gate before claiming final scrub closure.

Suggested expanded check:

```bash
rg -n "33bed9c|27\\.72|30\\.53|32\\.12|32\\.60|38\\.95|87\\.79|18\\.72|18\\.86|87\\.49|case-mlp-linear|case-all-linear|case-joint-hat|structural ceiling|structural limit|structural barrier|ceiling is not the roof|deployment-fidelity|ADC-on headline|-0\\.10" \
  paper/thesis/*.tex \
  paper/thesis/*.tex.kimi_draft_v3 \
  paper/thesis_cn/*.tex \
  paper/thesis_cn/*.tex.kimi_draft_v3 \
  paper/latex_gpt/sections/01_introduction.tex \
  paper/latex_gpt/sections/07_conclusion.tex \
  paper/latex_gpt/supplementary.tex
```

### F5 - PASS - EN Chapter 5 draft numeric Zone-3B cleanup improved
Kimi did fix the two concrete EN Chapter 5 draft contaminants called out in the prior Codex review:

- `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3:66` no longer cites the old `27.72/32.12` comparison.
- `paper/thesis/chapter_5_mitigation.tex.kimi_draft_v3:331` no longer cites old pre-revision `27.72` as a structural ceiling anchor.

This closes the old-number contamination inside the EN Chapter 5 sidecar, but not the ADC wording and canonical synchronization issues.

### F6 - PASS WITH CAVEAT - Paper introduction and conclusion edits are directionally correct
The direct edits to:

- `paper/latex_gpt/sections/01_introduction.tex:15`
- `paper/latex_gpt/sections/01_introduction.tex:17`
- `paper/latex_gpt/sections/07_conclusion.tex:7`

correctly move the main-text severe-NL narrative to a bounded `~80--82%` recovery band. Caveat: the claim that the present `NL=2.0` surrogate failure is primarily localized to the MLP path should not depend on the old supplementary groupwise accuracy table unless post-fix diagnostic provenance is made explicit.

### F7 - HIGH - CN Chapter 7 still cites the deprecated BUGGY energy artifact
Gemini's Ch7 warning is independently confirmed. Kimi's CN Ch7 sidecar still uses the old pJ-scale toy artifact:

- `paper/thesis_cn/chapter_7_deployment.tex.kimi_draft_v3:35` introduces the energy estimate.
- `paper/thesis_cn/chapter_7_deployment.tex.kimi_draft_v3:37` claims `65 pJ` and `15.4x` versus FP32.
- `paper/thesis_cn/chapter_7_deployment.tex.kimi_draft_v3:38` cites `energy_sensitivity_analysis.json`.
- `paper/thesis_cn/chapter_7_deployment.tex.kimi_draft_v3:364` later cites `11.45x`, so the chapter is internally inconsistent.

This conflicts with the locked energy audit:

- `report_md/_gpt/CODEX_T1_ENERGY_AND_REPORT_AUDIT_20260423.md:11` marks `energy_sensitivity_analysis.json.BUGGY` invalid for manuscript use.
- `report_md/_gpt/CODEX_T1_ENERGY_AND_REPORT_AUDIT_20260423.md:33` identifies `json_gpt/energy_scale_recovery_sensitivity.json` as the corrected artifact.
- `report_md/_gpt/json_gpt/energy_scale_recovery_sensitivity.json:12` gives `digital_FP32_uJ=273.94`, `speedup=11.45`, and `analog_uJ=23.924890829694323`.
- `report_md/_gpt/json_gpt/energy_scale_recovery_sensitivity.json:17` gives the assumed INT8 comparison, `speedup_vs_INT8=2.8625`.

Required fix: replace the `65 pJ / 15.4x / energy_sensitivity_analysis.json` passage with the locked wording: `11.45x vs FP32` and `~2.86x vs assumed INT8`, both explicitly labeled first-order analytical estimates, not silicon measurements.

---

## Required Kimi Follow-Up

1. Patch EN/CN thesis ADC language from "deployment-fidelity" to "hook diagnostic" or remove ADC-on headline claims.
2. Mark all historical groupwise NL ablation rows as invalidated/pre-fix diagnostic, or replace them with post-fix diagnostic evidence.
3. Narrow the broadcast wording around canonical thesis originals: they are superseded history, not clean integration targets.
4. Rerun expanded grep including supplementary and ADC terms.
5. Patch CN Ch7 energy text from deprecated `65 pJ / 15.4x` to locked `11.45x vs FP32` and `~2.86x vs assumed INT8`.
6. Broadcast exact changed line ranges after the above fixes.

---

## Codex Action Taken

No Kimi manuscript files were modified. This is a second blocking review note following Kimi's parallel scrub broadcast.
