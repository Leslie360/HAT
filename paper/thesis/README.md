# Thesis — Root Index

This directory contains the **original** thesis chapter source files.

> ⚠️ **INGESTION WARNING** — Do not compile or ingest these originals directly.  
> They are contaminated with deprecated data and language artifacts from earlier rounds.

## Canonical Sidecars (Current Round-4)

All sidecars are suffixed `.kimi_draft_v3` and are the **sole authorized** source for:
- Compilation into the final thesis PDF
- Extraction for journal manuscript adaptation
- Reviewer-response cross-referencing

| Chapter | Sidecar | Status |
|---------|---------|--------|
| 1 — HAT Instance Overfitting | `chapter_1_hat_instance_overfitting.tex.kimi_draft_v3` | ✅ Zone-scrubbed |
| 4 — Failure Modes | `chapter_4_failure_modes.tex.kimi_draft_v3` | ✅ Zone-scrubbed |
| 5 — Mitigation | `chapter_5_mitigation.tex.kimi_draft_v3` | ✅ Zone-scrubbed |
| 6 — Physical Realism | *(original is canonical, no sidecar)* | ⚠️ Audit pending |
| 7 — Deployment | `chapter_7_deployment.tex.kimi_draft_v3` | ✅ Energy locked, Stage-2 placeholder |
| 8 — Outlook | `chapter_8_outlook.tex.kimi_draft_v3` | ✅ Zone-scrubbed |

## Chinese Thesis Sidecars

Located under `paper/thesis_cn/`.

## Manuscript Sections

For the journal manuscript, use `paper/latex_gpt/sections/` with their corresponding `.kimi_draft_v3` sidecars where applicable.

## Data Discipline

- Energy: `energy_scale_recovery_sensitivity.json` is sole canonical source.
- Zone taxonomy: 3A (bug-immune), 3B (pre-fix invalidated), 3C (post-fix verified).
- ADC: "hook diagnostic" only — no deployment-fidelity claims.
