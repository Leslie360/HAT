# Canonical JSON Evidence for Paper-1

This directory copies the small JSON artifacts needed to verify the locked Paper-1 numbers without committing large `.pt` checkpoints.

Included evidence:

- IdealDevice 8-bit AIHWKit fresh-instance baseline.
- Pure 4-bit AIHWKit collapse baseline.
- Ensemble HAT 4-bit three-seed fresh-instance result.
- PCM UnitCell precision ladder: 8-bit, 6-bit, and 4-bit, three seeds each.
- Per-seed `fresh_eval.json`, `drift_eval.json`, `training_history.json`, and extended/fresh-drift JSONs where available.

Use `manifest_canonical_json_20260501.csv/json` for SHA256 provenance. The original checkpoint `.pt` files are intentionally excluded from release bundles.
