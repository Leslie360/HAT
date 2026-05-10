# Canonical JSON Evidence for Paper-1

This directory copies the small JSON artifacts needed to verify the locked Paper-1 numbers without committing large `.pt` checkpoints.

Included evidence:

- IdealDevice 8-bit AIHWKit fresh-instance baseline.
- Pure 4-bit AIHWKit collapse baseline.
- Ensemble HAT 4-bit three-seed fresh-instance result.
- PCM UnitCell precision ladder: 8-bit and 4-bit use three seeds; corrected 6-bit uses four fresh/drift seeds.
- Per-seed `fresh_eval.json`, `drift_eval.json`, `training_history.json`, and extended/fresh-drift JSONs where available.

Use `manifest_canonical_json_20260509.csv/json` for SHA256 provenance. The original checkpoint `.pt` files are intentionally excluded from release bundles.

The old 2026-05-01 6-bit protocol artifacts are preserved under `deprecated_20260501_old_protocol/` and are not active release evidence. The corrected 6-bit seed123 run lacks `training_history.json`; this is documented in the manifest and affects source-best aggregation only, not fresh/drift claims.
