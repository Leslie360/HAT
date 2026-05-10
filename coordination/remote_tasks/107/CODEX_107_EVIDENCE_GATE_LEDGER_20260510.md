# Codex 107 Evidence Gate Ledger

Date: 2026-05-10
Owner: Codex
Status: Gate ledger integrated after CC harvest; Paper2/107 claims remain blocked.

## Verdict

The current Remote-107 P8 package is useful as an audit candidate index, but it is not claim-bearing evidence. Paper2 manuscript drafting must not use the current tables or figures as locked scientific claims.

Final integrated outcome after CC harvest:

`107 CLAIM LOCK BLOCKED - RERUN/MANIFEST REQUIRED`

Reason: CC recovered family-level protocol/code information, but the local result JSONs still lack the per-row provenance envelope required for claim lock: exact producing commit/command/config, dataset/eval protocol, seed semantics, checkpoint hashes, and a safe old-vs-corrected matched table.

## Current artifacts

| Artifact | Path | Status |
|---|---|---|
| Remote tasklist | `coordination/remote_tasks/107/REMOTE_107_PHASE_P8_CORRECTED_NOISE_WORK2_TASKLIST_20260509.md` | active requirement |
| Strict-review report | `coordination/remote_tasks/107/REMOTE_107_PHASE_P8_CORRECTED_NOISE_REPORT_20260510.md` | draft candidate index |
| Candidate TSV | `paper2/results/FRESH_D2D_SUMMARY_107_20260510.tsv` | audit-only |
| Aggregation script | `paper2/src/aggregate_107_results.py` | audit-only logic |
| Plot script | `paper2/src/plot_107_results.py` | draft/audit visualization only |
| Candidate figures | `paper2/results/fig_107_*.png`, `paper2/results/fig_107_*.pdf` | visual QA only |
| CC metadata report | `coordination/agent_reports/Claude/CC_107_REMOTE_METADATA_HARVEST_20260510.md` | integrated; verdict blocked |
| CC command/code TSV | `coordination/agent_reports/Claude/CC_107_COMMAND_AND_CODE_PATHS_20260510.tsv` | planning-only |
| CC old-vs-corrected TSV | `coordination/agent_reports/Claude/CC_107_OLD_VS_CORRECTED_MAP_20260510.tsv` | planning-only |

## Raw candidate counts

| Check | Result |
|---|---:|
| JSON files inspected under `remote_reviews/107/results/paper2/` | 993 |
| Usable JSON rows with PPL/C2C/D2D | 993 |
| Bad JSON files | 0 |
| Candidate groups in `FRESH_D2D_SUMMARY_107_20260510.tsv` | 217 |
| Candidate groups with at least 5 D2D seeds | 163 |
| Files missing `d2d_seed` | 54 |
| Files missing `commit` | 993 |
| Files missing `command` | 993 |
| Files missing `config` | 993 |
| Files missing `dataset` | 993 |
| Files missing `eval_protocol` | 993 |
| Files missing `checkpoint_sha256` | 993 |

## Gate table

| Gate | Requirement | Current status | Owner | Blocking reason |
|---|---|---|---|---|
| G0 | Keep Paper2/107 separate from Paper1 | PASS | Codex | No Work-2 data is promoted into Paper1 release/source-data paths. |
| G1 | Exact grouping by checkpoint, layer list, C2C, D2D | PARTIAL | Codex | Current TSV groups by strict keys, but it remains audit-only. |
| G2 | Corrected-noise code path and git SHA | PARTIAL | CC -> Codex | Current clone path/SHA recovered (`107-clean` / `cf1d2a2`) and corrected-noise code path identified, but no per-row producing SHA exists in legacy JSONs. |
| G3 | Exact train/eval commands | FAIL | CC -> Codex | Only family-level launcher patterns were recovered; exact per-row commands are absent from legacy JSONs. |
| G4 | Dataset split and eval protocol | FAIL | CC -> Codex | Dataset/script protocol partly recovered, but legacy rows lack context/stride/batch/protocol fields and an eval-stride conflict remains unresolved. |
| G5 | Seed semantics | FAIL | CC -> Codex | D2D semantics are partly source-backed, but train/C2C/eval seed semantics are not complete per row. |
| G6 | Checkpoint paths and hashes | FAIL | CC -> Codex | Some checkpoint path strings exist, but no checkpoint SHA-256 manifest was found. |
| G7 | Old-vs-corrected comparison | FAIL | CC -> Codex | Summary-only comparisons exist, but no claim-lock-safe matched table covers checkpoint family, analog layers, protocol, and seed semantics. |
| G8 | Metadata completeness table | FAIL | Codex | Current raw JSON fails required metadata fields in every usable row; CC confirmed local recovery is insufficient. |
| G9 | Claim-ready figures | FAIL | Codex | Current figures are draft audit plots only; convergence/noise-sweep claims are not locked. |
| G10 | Paper2 manuscript drafting | BLOCKED | Codex | Drafting claim-bearing sections must wait until G2-G9 pass. |

## CC harvest integration

CC completed:

`coordination/agent_reports/Claude/CC_107_REMOTE_METADATA_HARVEST_20260510.md`

Integrated facts:

- Remote clone branch/HEAD: `107-clean` / `cf1d2a2fcc71aae89534ed8c75ea6bab4d9e8532`.
- Existing JSON chronology indicates many result JSONs predate the metadata-envelope patch.
- Corrected-noise implementation is source-visible in the current remote scripts, but the exact code SHA that produced each legacy result row is not embedded.
- Legacy JSONs do not embed exact commands.
- Dataset and stride protocol are only family-level recovered; eval stride remains conflicting between script/metadata patch and v3 summary.
- Checkpoint paths are partial; checkpoint SHA-256 manifest is absent.
- Old-vs-corrected comparison is summary-only and not safe for claim lock.

## Previous CC task

CC has a separate read-only tasklist:

`coordination/remote_tasks/107/CC_107_REMOTE_METADATA_HARVEST_TASKLIST_20260510.md`

CC should write only:

`coordination/agent_reports/Claude/CC_107_REMOTE_METADATA_HARVEST_20260510.md`

Optional CC TSVs may also be written under `coordination/agent_reports/Claude/`.

## Codex integration rule

Codex will not rewrite Paper2 narrative or promote figures/tables until one of the following happens:

1. remote 107 supplies a signed manifest satisfying G2-G8, or
2. the minimal corrected-noise matrix is rerun with the patched metadata envelope and checkpoint hashes.

Current next action: use `coordination/remote_tasks/107/REMOTE_107_METADATA_RECOVERY_OR_MINIMAL_RERUN_REQUEST_20260510.md`.

## Protected boundaries

- Paper1 changes are allowed only under Codex's separate Paper1 author-review/release lane; do not mix Paper2/107 data into Paper1.
- No remote clone edits.
- No checkpoint/data moves.
- No training or GPU jobs.
- No push.
