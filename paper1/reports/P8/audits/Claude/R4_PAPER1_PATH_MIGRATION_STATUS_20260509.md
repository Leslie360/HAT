# R4 Paper-1 Path Migration Status

Date: 2026-05-09
Scope: Paper-1 release/provenance migration and path preflight
Status: PARTIAL COMPLETE — release/provenance moved; manuscript path intentionally retained

## 1. What moved

| Old path | New path | Status |
|---|---|---|
| `release_artifacts/paper1_submission_bundle_20260509_final/` | `paper1/release/paper1_submission_bundle_20260509_final/` | moved |
| `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | `paper1/release/paper1_submission_bundle_20260509_final.tar.gz` | moved |
| `release_artifacts/paper1_provenance_archive_20260509/` | `paper1/provenance/paper1_provenance_archive_20260509/` | moved |
| `release_artifacts/paper1_provenance_archive_20260509.tar.gz` | `paper1/provenance/paper1_provenance_archive_20260509.tar.gz` | moved |

Restore script:

`archive/reorg_20260509/restore/R4_PAPER1_RELEASE_PROVENANCE_RESTORE.sh`

Execution log:

`logs/reorg_r4_paper1_release_provenance_20260509_231944.log`

## 2. Verification

| Check | Result |
|---|---|
| Final tarball SHA | `32959fac881ad1659d2da0a4ebeba30846dac72986e032dc411ea6e916c6f4a4` |
| Manifest entries | 133 |
| Bundle directory present | PASS |
| Provenance archive present | PASS |

## 3. What did not move yet

`paper/latex_gpt/` remains in place.

Reason: many active LaTeX, script, and report references still assume `paper/latex_gpt`. Moving it now would require a path rewrite/rebuild cycle and could break the currently verified submission bundle. The safer sequence is:

1. submit/use current verified bundle from `paper1/release/`;
2. after acceptance/submission safety, migrate `paper/latex_gpt/` to `paper1/manuscript/`;
3. update scripts and references;
4. rebuild PDFs;
5. rerun SHA/stale/PCM guards.

## 4. Path audit

Hardcoded path audit report:

`report_md/_gpt/R4_PATH_REFERENCE_AUDIT_20260509.md`

Patterns audited:

- `paper/latex_gpt`
- `release_artifacts`
- `report_md/_gpt`
- `paper2_aihwkit_baseline`
- `paper2/`
- `paper/thesis`
- `paper/thesis_cn`
- `数据_博士`
- `checkpoints/`
- `data/`

## 5. Updated reports

Current handoff and self-audit reports now point to:

`paper1/release/paper1_submission_bundle_20260509_final.tar.gz`

instead of the old `release_artifacts/` final bundle path.

## 6. Next recommended R4 step

Before moving `paper/latex_gpt/`, generate a concrete rewrite list:

```bash
grep -R -n "paper/latex_gpt" . --exclude-dir=.git --exclude-dir=archive
```

Then rewrite only active references, rebuild, and re-verify. Until then, keep manuscript path stable.

## 7. Verdict

R4 low-risk migration is complete. Final release/provenance artifacts now live under `paper1/`. Active manuscript migration is deferred for safety.
