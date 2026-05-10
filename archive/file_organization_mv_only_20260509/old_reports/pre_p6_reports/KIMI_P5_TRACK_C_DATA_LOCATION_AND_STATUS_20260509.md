# Kimi P5 Track C Report: Data Location and Master Status

**Date:** 2026-05-09
**Dispatch:** `DISPATCH_SUPERPHASE_P5_POST_AUDIT_REMOTE_AND_EXPERIMENT_GOVERNANCE_20260509.md`
**Executor:** kimi

---

## 1. Paper-1 Active Submission Artifacts

| What | Where | Safe to delete? |
|------|-------|----------------|
| Final submission bundle (unpacked) | `release_artifacts/paper1_submission_bundle_20260509_final/` | **NO** |
| Final submission bundle (tar.gz) | `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | **NO** |
| Provenance archive (unpacked) | `release_artifacts/paper1_provenance_archive_20260509/` | **NO** |
| Provenance archive (tar.gz) | `release_artifacts/paper1_provenance_archive_20260509.tar.gz` | **NO** |
| Previous release candidate | `release_artifacts/paper1_release_candidate_20260509/` | **NO** (until final acceptance) |
| Clean release candidate | `release_artifacts/paper1_release_candidate_20260509_clean/` | **NO** (until final acceptance) |

## 2. Paper-1 Source Data

| What | Where | Safe to delete? |
|------|-------|----------------|
| LaTeX source (working tree) | `paper/latex_gpt/` | **NO** |
| Main sections | `paper/latex_gpt/sections/` | **NO** |
| Supplementary sections | `paper/latex_gpt/supplementary/` | **NO** |
| Figures | `paper/latex_gpt/figures/` | **NO** |
| Source data CSV/JSON | `paper/latex_gpt/source_data/` | **NO** |
| Bibliography | `paper/latex_gpt/refs_gpt.bib` | **NO** |

## 3. Paper-1 Provenance / Deprecated

| What | Where | Safe to delete? |
|------|-------|----------------|
| Deprecated old-protocol JSON | `paper/latex_gpt/source_data/canonical_json/deprecated_20260501_old_protocol/` | **NO** (historical provenance) |
| Old reviewer bundle | `release_artifacts/paper1_reviewer_bundle_20260501_1645/` | Can archive after P5 acceptance |
| Old reviewer bundle tar.gz | `release_artifacts/paper1_reviewer_bundle_20260501_1645.tar.gz` | Can archive after P5 acceptance |

## 4. Local GPU Experiment Outputs

| What | Where | Safe to delete? |
|------|-------|----------------|
| Training outputs | `outputs/` | **NO** (active experiment data) |
| Clean-room tests | `outputs/cleanroom_paper1_*/` | Can delete after P5 acceptance |
| Cold-unpack tests | `outputs/p5_cold_unpack_*/` | Can delete after P5 acceptance |
| GPU logs | `logs/` (if exists) | Review before deleting |

## 5. 105 Server Results

| What | Where | Safe to delete? |
|------|-------|----------------|
| Stable snapshot | `docs/data/remote_snapshots_20260507/hat_105_results/` | **NO** |
| Generated CSVs | `docs/data/remote_snapshots_20260507/remote105_*.csv` | **NO** |
| Data index | `report_md/_gpt/REMOTE_105_107_DATA_ACQUISITION_INDEX_20260507.md` | **NO** |

## 6. 107 Server Results

| What | Where | Safe to delete? |
|------|-------|----------------|
| Stable snapshot | `docs/data/remote_snapshots_20260507/hat_107_clean/` | **NO** |
| Generated CSVs | `docs/data/remote_snapshots_20260507/remote107_*.csv` | **NO** |
| Deliverable code | `docs/data/remote_snapshots_20260507/hat_107_clean/deliverable/code/` | **NO** |

## 7. GitHub / Remote Task Files

| What | Where | Safe to delete? |
|------|-------|----------------|
| P5 remote tasklist | `report_md/_gpt/REMOTE_105_107_PHASE_P5_TASKLIST_20260509.md` | **NO** |
| Previous remote tasklists | `report_md/_gpt/REMOTE_*_TASKLIST_*.md` | Archive, do not delete |
| Handoff protocols | `report_md/_gpt/REMOTE_HANDOFF_README_*.md` | Archive, do not delete |

## 8. Agent Reports and Broadcasts

| What | Where | Safe to delete? |
|------|-------|----------------|
| All P1-P5 Kimi reports | `report_md/_gpt/KIMI_*.md` | **NO** |
| Codex acceptance reports | `report_md/_gpt/CODEX_*.md` | **NO** |
| DS/Mimo audits | `report_md/_gpt/DS_*.md`, `report_md/_gpt/MIMO_*.md` | **NO** |
| BROADCAST log | `BROADCAST.md` (root) | **NO** |
| Agent intercoms | `report_md/_gpt/BROADCAST_*.md` | **NO** |

## 9. "If the user asks where X is" Lookup

| User asks for | Go here |
|---------------|---------|
| Final submission PDF | `release_artifacts/paper1_submission_bundle_20260509_final/main.pdf` |
| Supplementary PDF | `release_artifacts/paper1_submission_bundle_20260509_final/supplementary_main.pdf` |
| Cover letter PDF | `release_artifacts/paper1_submission_bundle_20260509_final/cover_letter.pdf` |
| LaTeX source | `paper/latex_gpt/` |
| PCM canonical numbers | `paper/latex_gpt/source_data/tab_pcm_precision_ladder.csv` |
| PCM canonical JSON manifest | `paper/latex_gpt/source_data/canonical_json/manifest_canonical_json_20260509.json` |
| Deprecated old-protocol data | `release_artifacts/paper1_provenance_archive_20260509/deprecated_20260501_old_protocol/` |
| 105 remote results | `docs/data/remote_snapshots_20260507/hat_105_results/` |
| 107 remote results | `docs/data/remote_snapshots_20260507/hat_107_clean/` |
| 105/107 index | `report_md/_gpt/REMOTE_105_107_DATA_ACQUISITION_INDEX_20260507.md` |
| GPU status | Run `nvidia-smi` or check `report_md/_gpt/KIMI_P5_TRACK_E_GPU_AND_EXPERIMENT_QUEUE_20260509.md` |
| Agent reports | `report_md/_gpt/KIMI_*.md`, `report_md/_gpt/CODEX_*.md` |
| Broadcast log | `BROADCAST.md` (repo root) |

---

*Report by kimi. Data location index consolidated on 2026-05-09.*
