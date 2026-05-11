# Remote 107 Selective KV Lock Report

Date: 2026-05-11
Method: Metadata recovery from existing eval JSONs + source code audit
Recovery commit: 6df8267
Corrected-noise commit: c727a43

## Summary

- Total required rows: 41
- Claim-lockable: 41
- Blocked (audit-only): 0

### Claim-lockable by family

- all24: 10
- last1: 10
- last2: 10
- last4: 10

### Blocked by family

None.

## Blockers

None. Digital reference PPL=23.30 recovered from Pre-HAT eval in train_layer_last1.log.

## Output files

- Claim-lock JSONs: `/home/lisq753/projects/HAT_kv107/paper2/results/remote107/claim_lock_recovery_20260511/` (41 files)
- Manifest: `/home/lisq753/projects/HAT/HAT/coordination/remote_tasks/107/REMOTE_107_SELECTIVE_KV_LOCK_MANIFEST_20260511.tsv`
- Report: `/home/lisq753/projects/HAT/HAT/coordination/remote_tasks/107/REMOTE_107_SELECTIVE_KV_LOCK_REPORT_20260511.md`
