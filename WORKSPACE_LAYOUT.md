# `compute_vit/` Workspace Layout

**Last reorganized:** 2026-04-25 (deep cleanup pass 3)
**Purpose:** Authoritative map of where everything lives.

---

## Product lanes

`compute_vit/` is organized around three deliverables. The ideal target layout and migration phases are tracked in `coordination/active/COMPUTE_VIT_IDEAL_LAYOUT_PLAN_20260510.md`.

| Lane | Active home | What belongs here | Notes |
|:--|:--|:--|:--|
| Paper1 | `paper1/manuscript/`, `paper1/release/`, `paper1/provenance/`, `paper1/reports/` | Main manuscript, supplement/appendix, cover letter, final bundle, source data, provenance, near-term reports | Paper1 is near completion; protect main/supplement/letter and final release SHA. |
| Paper2 / 107 KV-cache | `paper2/`, `paper2_aihwkit_baseline/`, `coordination/remote_tasks/107/` | Selective KV-cache / 107 work, Work-2 results, AIHWKit/PCM baselines | Keep separate from Paper1 evidence unless explicitly labeled future-work. |
| Degree thesis | `thesis/`, `manuscripts/thesis/` | Thesis text, XJTU template, reused Paper1 figures/data references | Reuse Paper1 assets via traceable compatibility paths, not ad hoc copies. |

Shared code, data, checkpoints, tools, and archive areas support these lanes but should not obscure them.

---

## Root files

### Documentation (3 .md)
- `README.md` — Project front door
- `PROJECT_INDEX.md` — Root registry and path policy
- `WORKSPACE_LAYOUT.md` — This file

Historical/frozen root documents are isolated under `archive/reorg_20260509/legacy_root_docs_20260510/`, not in active documentation paths.

### Root cleanup status

Root Markdown is clean. Python implementations now live under `src/compute_vit/`; train/eval command wrappers live under `cli/`. See `paper1/reports/P8/audits/Claude/CLAUDE_ROOT_PYTHON_CLEANUP_AUDIT_20260510.md` for the migration rationale.

### Python entry points + libraries (21)
**Training wrappers:**
- `cli/train_tinyvit.py`, `cli/train_tinyvit_ensemble.py`
- `cli/train_convnext.py`, `cli/train_resnet18.py`

**Eval wrappers:**
- `cli/eval_fresh_instances_postfix.py` ← post-fix-aware fresh instance eval
- `cli/eval_fresh_instances.py` ← legacy fresh eval
- `cli/eval_imagenet_analog.py`, `cli/eval_literature_profile.py`
- `cli/eval_measured_profile.py`, `cli/eval_resnet18_checkpoints.py`

**Core implementation modules:**
- `src/compute_vit/analog_layers.py` ← post-bug-fix (commit 33bed9c + NL guard + AMP decorators)
- `src/compute_vit/analog_layers_ensemble.py` ← Ensemble HAT primitives
- `src/compute_vit/inference_analysis_utils.py` ← ADC hook + range calibration
- `src/compute_vit/amp_utils.py`, `src/compute_vit/device_profile_utils.py`
- `src/compute_vit/tinyvit_hybrid_utils.py`, `src/compute_vit/report_asset_paths.py`
- `src/compute_vit/model_profiling.py`, `src/compute_vit/physical_noise_pipeline.py`
- `src/compute_vit/hybrid_calibration.py`, `src/compute_vit/hybrid_runtime_compiler.py`

### Config and compatibility symlinks
- `environment.yml`, `requirements.txt`, `requirements-optional.txt`
- `auto_fitted_profile.json` -> `device_profiles/auto_fitted_profile.json`

### Shell compatibility symlinks
- `download_data.sh` -> `scripts/download_data.sh`

### Other
- `LICENSE`, `.gitignore`

---

## Subdirectories

| Dir | Purpose | Notes |
|:--|:--|:--|
| `src/` | Importable implementation package | `src/compute_vit/README.md`; implementation `.py` files live here |
| `cli/` | Train/eval wrapper entrypoints | `cli/README.md`; run wrappers from project root |
| `configs/` | Stable config scaffold | `configs/README.md`; one-off configs belong in `experiments/configs/` |
| `manuscripts/` | Compatibility manuscript links | Paper-1 source compatibility path: `manuscripts/paper1/src/` -> `../../paper1/manuscript` |
| `paper1/` | Paper-1 manuscript, release, provenance, and reports | Editable source: `paper1/manuscript/`; final submission bundle remains SHA-verifiable under `paper1/release/`; active provenance map: `paper1/provenance/paper1_active_provenance_index_20260510.tsv` |
| `paper/` | Legacy Paper1 compatibility shell | See `paper/README.md` and `PAPER_DIRECTORY_MAP_20260510.md`; do not add new active assets here |
| `paper2/` | Work-2 KV-cache research | Keep 107 work separated from Paper-1 |
| `paper2_aihwkit_baseline/` | Work-2 AIHWKit/PCM baseline | Large payloads remain local-first |
| `thesis/` | Thesis sources and XJTU template | `thesis/latex_gpt` compatibility link points to Paper-1 source |
| `coordination/` | Active dispatches, audits, agent reports | `coordination/active/` is current live coordination |
| `archive/reorg_20260509/legacy_root_docs_20260510/` | Isolated old root docs | Not active; retained for provenance only |
| `tools/` | Validation, plotting, LaTeX, data, maintenance tools | Stable reusable tools only |
| `scripts/` | One-shot scripts + pipelines + monitors | Subdir `_gpt/` retained for compatibility |
| `tests/` | Unit + integration tests | Run from project root |
| `experiments/` | Non-final experiment configs/logs/scratch/manifests | New exploratory jobs start here |
| `checkpoints/` | Model checkpoints | **Protected:** `_ensemble/`, `_gpt/postfix_m_series/`, C/R/V baselines |
| `data/` | Datasets | `.gitignore`d; auto-fetched per `data/README.md` |
| `device_profiles/` | Device profile JSONs | Literature + measured priors |
| `logs/` | Training/eval/cleanup logs | Keep as audit trail; stale logs may be archived |
| `notebooks/` | Jupyter notebooks | Tutorial/exploration |
| `release_artifacts/` | Zenodo bundle staging | Legacy staging area |
| `report_md/` | Current manifests and compatibility coordination paths | Active coordination is split into `coordination/` |
| `archive/` | Workspace-level restorable archive | See `archive/README.md`; bulk moves require restore scripts |
| `internal/` | Internal data requirements docs | Local/internal material |

---

## Where things live (quick reference)

### Coordination + decisions
- Active: `report_md/_gpt/` (65 files)
- Archived: `report_md/_gpt/archive/` (13 subdirs by period)

### Source of truth files
- Narrative: `report_md/_gpt/NARRATIVE_PIVOT_20260424.md`
- Roadmap: `report_md/_gpt/CLAUDE_FORWARD_ROADMAP_20260425.md`
- Index: `report_md/_gpt/INDEX.md`

### Canonical evidence chain (DO NOT DELETE)
- `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` → 86.37% / 88.53% / AR(1)
- `checkpoints/_gpt/postfix_m_series/cx_m{1..6}/` → severe-NL ~80-82% band
- `checkpoints/{C,R,V}{1..8}_*.pt` → paper baselines

### Manuscript files
- LaTeX paper: `paper1/manuscript/main.tex` (`paper/latex_gpt/main.tex` remains a compatibility path)
- Cover letter: `paper1/manuscript/cover_letter.tex`
- Supplementary: `paper1/manuscript/supplementary.tex`
- EN thesis: `paper/thesis/`
- CN thesis: `paper/thesis_cn/`

### Verification suite
- `tests/test_dual_bug_fix.py` (7 tests)
- `tests/test_groupwise_nl_wrapper.py` (9 tests)
- `tests/test_adc_perinstance_calibration.py`

---

## Workspace hygiene standard

`compute_vit/` is maintained as a clean active workbench, not a dump of historical files.

| Asset class | Active location | Backup/deprecated location | Required traceability |
|:--|:--|:--|:--|
| Data JSON / CSV / TSV | `paper1/source_data/`, `paper2/results/`, `report_md/{json,csv}/` when current | `archive/` with manifest | Source script, generation date, and consuming figure/table |
| Device profiles | `device_profiles/` | `archive/` if superseded | Literature/measured source and parameter meaning |
| Checkpoints / weights | `checkpoints/` | `data_local/checkpoints/` or `archive/` only after explicit review | Training script/config, seed, dataset, metric, and paper/thesis use |
| Plot scripts | `tools/plotting/` | `archive/old_scripts/` or `archive/reorg_20260509/` | Input data path and output figure path |
| Validation scripts | `tools/validation/` | `archive/old_scripts/` or `archive/reorg_20260509/` | What claim or artifact they validate |
| LaTeX source | `paper1/manuscript/`, `thesis/` | `archive/` for stale drafts | Figure/table source assets and build path |
| Figures/tables in use | Manuscript source asset dirs and manifests | `paper1/provenance/asset_archive/` for unused candidates | Active / backup / deprecated status |
| Recent agent Markdown | `coordination/active/`, current `paper1/reports/`, current `coordination/{dispatches,audits,agent_reports}/` | `archive/` for old agent MD | Date, owner, phase, and whether it is active |
| Old root docs | `archive/reorg_20260509/legacy_root_docs_20260510/` | Same | Restorable through `archive/reorg_20260509/restore/ROOT_DOCS_CLEANUP_20260510_RESTORE.sh` |

Before moving or adding artifacts, preserve provenance first: write/update an index or manifest, keep active paths small, and isolate stale files instead of leaving them beside current work.

---

## File-management doctrine

These rules govern future maintenance:

| Rule | Applies to |
|:--|:--|
| Root broadcasts → `report_md/_gpt/` | Never `compute_vit/` root |
| One-shot `run_*.py` → `scripts/oneshot_root/` | After experiment closes |
| Pipeline `*.sh` → `scripts/` | Not in root |
| Tests → `tests/` | Not in root |
| Old broadcasts (>5 days) → `report_md/_gpt/archive/<period>/` | Tier by date |
| `.bak`/`.ORIGINAL`/`.SIMULATED` → `tmp/` | Never root |
| `__pycache__/` → free to delete | Auto-regenerable |
| Stale checkpoints with explicit naming → safe delete | `_badscale`, `_suspect`, `_smoke` |
| **Canonical checkpoints** → grep-verify before any move | `_ensemble/`, `postfix_m_series/`, paper baselines |
| Logs >5 days → archive subdir | Don't delete (audit trail) |
| INDEX maintenance: keep <100 active files | Archive aggressively after each round |

---

---

## Zenodo / external hosting policy (added 2026-04-25, cleanup pass 4)

The git repo no longer tracks **model checkpoints** or **datasets**. They live on local disk only and are released via Zenodo for reproducibility.

| Asset | Location | Reproducibility plan |
|:--|:--|:--|
| `checkpoints/_ensemble/V4_*.pt` (canonical 86.37%) | Local + Zenodo | Bundle in `release_artifacts/source_data_v1/` for paper-1 release |
| `checkpoints/{C,R,V}{1..8}*.pt` baselines | Local + Zenodo | Same |
| `checkpoints/_gpt/postfix_m_series/cx_m{1..6}/` | Local + Zenodo | Same |
| `data/cifar-10-batches-py/` etc | Local only | torchvision auto-downloads on first run |

The git repo at GitHub `Leslie360/HAT.git` is now ~700MB (was 17GB pre-cleanup). All checkpoints accessible via Zenodo bundle when paper-1 releases.

Anyone cloning fresh: code is here; for the trained checkpoints, see Zenodo DOI (TBD).


## Cleanup history (recent)

| Date | Pass | Result |
|:--|:--|:--|
| 2026-04-25 11:42 | Pass 1 (deep cleanup) | 459MB stale checkpoints deleted; 36 files relocated; 6 backups deleted |
| 2026-04-25 11:50 | Pass 2 (git + archive) | 4 git commits; ~370 old broadcasts archived to 7 subdirs |
| 2026-04-25 12:30 | **Pass 3 (workspace layout)** | **Root .py: 100 → 21; tests/ created; scripts/oneshot_root/ created; 远端/ archived** |

See `report_md/_gpt/CLAUDE_DEEP_CLEANUP_EXECUTION_20260425.md` for full pass-1 details.
