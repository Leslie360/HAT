# `compute_vit/` Workspace Layout

**Last reorganized:** 2026-04-25 (deep cleanup pass 3)
**Purpose:** Authoritative map of where everything lives.

---

## Root files (49 total)

### 📚 Documentation (6 .md)
- `README.md` — Project front door
- `EXPERIMENT_PROTOCOL.md` — Experiment design protocol
- `MASTER_PLAN.md` — High-level roadmap
- `PROJECT_INDEX.md` — Subdir-by-subdir index
- `RELEASE_CHECKLIST.md` — Pre-release checklist
- `REPRODUCIBILITY.md` — Reproducibility guide
- `WORKSPACE_LAYOUT.md` — **This file**

### 🐍 Canonical Python entry points + libraries (21)

**Training entries (4):**
- `train_tinyvit.py`, `train_tinyvit_ensemble.py`
- `train_convnext.py`, `train_resnet18.py`

**Eval entries (6):**
- `eval_fresh_instances_postfix.py` ← post-fix-aware fresh instance eval
- `eval_fresh_instances.py` ← legacy fresh eval
- `eval_imagenet_analog.py`, `eval_literature_profile.py`
- `eval_measured_profile.py`, `eval_resnet18_checkpoints.py`

**Core libraries (11):**
- `analog_layers.py` ← post-bug-fix (commit 33bed9c + NL guard + AMP decorators)
- `analog_layers_ensemble.py` ← Ensemble HAT primitives
- `inference_analysis_utils.py` ← ADC hook + range calibration
- `amp_utils.py`, `device_profile_utils.py`
- `tinyvit_hybrid_utils.py`, `report_asset_paths.py`
- `model_profiling.py`, `physical_noise_pipeline.py`
- `hybrid_calibration.py`, `hybrid_runtime_compiler.py`

### 📦 Config (4)
- `environment.yml`, `requirements.txt`, `requirements-optional.txt`
- `auto_fitted_profile.json`

### 🐚 Shell scripts (1)
- `download_data.sh` ← dataset setup; pipeline scripts moved to `scripts/`

### Other
- `LICENSE`, `.gitignore`

---

## Subdirectories (17)

| Dir | Purpose | Notes |
|:--|:--|:--|
| `paper/` | Manuscript + thesis (EN + CN) | `latex_gpt/` is canonical; `thesis/` and `thesis_cn/` for PhD defense |
| `scripts/` | One-shot scripts + pipelines + monitors | Subdir `_gpt/` for GPT-specific; `oneshot_root/` for root-relocated `run_*.py` |
| `tests/` | Unit + integration tests | Run from project root: `python tests/test_dual_bug_fix.py` |
| `checkpoints/` | Model checkpoints | **Protected:** `_ensemble/` (canonical), `_gpt/postfix_m_series/` (M-series), C/R/V baselines |
| `data/` | Datasets | `.gitignore`d; auto-fetched per `data/README.md` |
| `device_profiles/` | Device profile JSONs (literature + measured priors) | |
| `logs/` | Training/eval logs | `_gpt/archive_pre_20260420/` for old logs |
| `notebooks/` | Jupyter notebooks (tutorial) | |
| `outputs/` | Reviewer archives + submission bundles + remote handoff | |
| `release_artifacts/` | Zenodo bundle staging | |
| `report_md/` | Coordination + reports + JSONs | `_gpt/` is the active coordination layer |
| `archive/` | Workspace-level archive | `scripts/round_p_era/`, `scripts/` (one-shot scripts) |
| `_archive/` | Older legacy archive | Pre-Round-P historical |
| `internal/` | Internal data requirements docs | |
| `tmp/` | Temporary files + backups | `bak_cleanup_*/` for retained rollback |
| `数据_博士/` (PhD data) | PhD measured device data placeholder | Awaiting delivery per DATA_INGEST_PROTOCOL |
| `__pycache__/` | Python bytecode (regenerable) | Auto-deleted on cleanup |

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
- LaTeX paper: `paper/latex_gpt/main.tex`
- Cover letter: `paper/latex_gpt/cover_letter.tex`
- Supplementary: `paper/latex_gpt/supplementary.tex`
- EN thesis: `paper/thesis/`
- CN thesis: `paper/thesis_cn/`

### Verification suite
- `tests/test_dual_bug_fix.py` (7 tests)
- `tests/test_groupwise_nl_wrapper.py` (9 tests)
- `tests/test_adc_perinstance_calibration.py`

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
