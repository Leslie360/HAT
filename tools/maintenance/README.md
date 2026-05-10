# tools/maintenance/

Reusable workspace hygiene helpers.

No active scripts are currently stored here.

## Rules

- Prefer dry-run and manifest-first behavior.
- Do not delete or move data/checkpoints without explicit approval.
- Bulk moves require a manifest and restore script under `archive/reorg_*/restore/`.
