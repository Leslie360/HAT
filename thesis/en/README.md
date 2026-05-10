# Thesis — English Source Index

This directory is the active English thesis source lane after the 2026-05-10 workspace reorganization.

## Canonical source policy

- Use the normal `.tex` files in this directory as the current editable thesis sources.
- Historical `.kimi_draft_v3` references in comments or archived template copies are provenance markers, not the current source-of-truth policy.
- Do not compile or ingest old sidecar-only instructions from archived `manuscripts/thesis` mirrors as current guidance.

## Active files

| File | Role |
|:--|:--|
| `main.tex` | English thesis entrypoint. |
| `chapter_1_hat_instance_overfitting.tex` | Paper1/HAT instance-overfitting chapter draft. |
| `chapter_2_framework.tex` | Framework chapter draft. |
| `chapter_3_hat_taxonomy.tex` | HAT taxonomy chapter draft. |
| `chapter_4_failure_modes.tex` | Failure-modes chapter draft. |
| `chapter_5_mitigation.tex` | Mitigation chapter draft. |
| `chapter_6_physical_realism.tex` | Physical-realism chapter draft. |
| `chapter_7_deployment.tex` | Deployment chapter draft. |
| `chapter_8_outlook.tex` | Outlook chapter draft. |
| `XJTU-thesis` | Compatibility/template path. |

## Data discipline

- Paper1-derived claims should trace back to `../paper1` provenance and release manifests.
- Paper2/107 material remains provisional and audit-only until a signed manifest or minimal corrected-noise rerun passes the evidence gate.
- Keep thesis-only assets in `thesis/`; do not write thesis-only material into Paper1 release paths.
