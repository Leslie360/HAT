# PROJECT INDEX — compute_vit/

**Purpose:** One authoritative registry of every path at the `compute_vit/` root (and notable children), what each is for, and whether it's live, frozen, or archived. Read this *before* touching anything. Written 2026-04-17.

---

## 1. Naming convention (effective 2026-04-17, for NEW files)

These rules apply to anything created from now on. We are deliberately **not** renaming live files, because renaming cascades into `.tex` citations, `grep` paths inside coordination notes, plot-script paths, etc. Existing odd names are tolerated; new odd names are not.

| Rule | Do | Don't |
|:--|:--|:--|
| Language | English only in filenames | 中文、拼音 in new filenames |
| Case (code) | `lower_snake_case.py` | `RunCrossSim.py`, `Run-crosssim.py` |
| Case (docs) | `UPPER_SNAKE.md` for fixed docs; `kebab-case.md` for freeform notes | `MixedCase.md` |
| Dates | Only in truly time-anchored files (`manifest_20260417.md`). Never in source code | `train_v2_20260413_gpt.py` |
| Agent suffix | Drop `_gpt` / `_kimi` / `_gemini` on NEW files. The author is in `git blame`, not the filename | `foo_gpt.md`, `bar_kimi.py` |
| Versioning | `foo.py` stays the one name. Do not spawn `foo_v2.py`, `foo_FIXED.py`, `foo_final.py` — edit `foo.py` and commit | `run_ir_drop_sensitivity.py` + `_v2` + `_v3` |
| Synonyms | Pick one per concept: **task** (not plan/brief), **sync** (not log/update), **manifest** (not inventory/ledger), **review** (not audit/check) | Use of all four interchangeably in one week |
| Scratch | Put it under `scripts/`, `tmp/`, `_archive/`, or `internal/` — never at project root | `patch_fig11.py` at root |
| Coordination | New dispatches: `dispatch-<topic>.md` under `report_md/_gpt/` | `CODEX_DISPATCH_20260417_cleanup_gpt.md` |

**Why `_archive/` not `archive/`:** leading underscore sorts to the end in `ls` — visually separated from live trees.

---

## 2. Top-level map

```
compute_vit/
├── README.md, MASTER_PLAN.md, RELEASE_CHECKLIST.md, EXPERIMENT_PROTOCOL.md   live root docs
├── <81 .py at root>                                                            code (see §4)
├── AGENT_SYNC/             deprecated, replaced by report_md/_gpt/AGENT_SYNC_gpt.md
├── _archive/               ← everything retired goes here (§8)
├── checkpoints/            24 GB, .pt model weights, gitignored
├── data/                   CIFAR-10/100, Flowers-102, ImageNet, SVHN, TinyImageNet (gitignored)
├── device_profiles/        3 canonical JSON profiles (measured, literature, synthetic)
├── docs/                   stable hand-written engineering docs
├── internal/               gitignored local scratch
├── logs/                   experiment stdout dumps, gitignored
├── outputs/                submission bundles, reviewer archives
├── paper/                  manuscript source (LaTeX canonical under paper/latex_gpt/)
├── report_md/              long-form reports + live coordination (_gpt/ subtree)
├── scripts/                bash/python helpers (not entry-point experiments)
└── private raw-data tree    omitted from the public repo; pass explicit paths when fitting measured profiles
```

**Status legend used in tables below:**
- **live** — on the submission/reproducibility critical path, actively referenced.
- **frozen** — authoritative snapshot, do not edit (e.g., `CANONICAL_RESULT_LOCK_gpt.md`).
- **draft-superseded** — older markdown draft that has a canonical `.tex` replacement. Keep for history, never edit.
- **scratch** — gitignored or throwaway.
- **archive** — moved to `_archive/`. Reversible via `mv`.

---

## 3. Root markdown (4 live files)

| Path | Purpose | Status |
|:--|:--|:--|
| `README.md` | Project entry point, reproducibility quickstart | live |
| `MASTER_PLAN.md` | 36-task plan, all marked ✅ or optional | frozen |
| `RELEASE_CHECKLIST.md` | Submission gate: numbers, figures, text locks | live |
| `EXPERIMENT_PROTOCOL.md` | Canonical experiment definitions (R1–R6, C1–C9, V1–V6) | frozen |

---

## 4. Root Python — grouped

### 4.1 Training entry points (4) — **live**

| Path | Purpose |
|:--|:--|
| `train_resnet18.py` | ResNet-18 R1–R6 trainer |
| `train_convnext.py` | ConvNeXt-Tiny C1–C9 trainer |
| `train_tinyvit.py` | Tiny-ViT V1–V6 trainer |
| `train_tinyvit_ensemble.py` | Ensemble HAT trainer (paper Fig. 8 driver) |

### 4.2 Evaluation entry points (5) — **live**

| Path | Purpose |
|:--|:--|
| `eval_imagenet_analog.py` | ImageNet-1k analog evaluation |
| `eval_measured_profile.py` | Evaluate checkpoints against a user-supplied measured profile |
| `eval_literature_profile.py` | Evaluate against literature (Zhang 2025) profile |
| `eval_fresh_instances.py` | Instance-variation sweep for Fig. 10 |
| `eval_resnet18_checkpoints.py` | Bulk eval over `checkpoints/R*` |

### 4.3 Experiment drivers — `run_*.py` (39 files, live whitelist)

All are canonical entry points invoked from `scripts/` or documented in `EXPERIMENT_PROTOCOL.md`.

Representative families (see `EXPERIMENT_PROTOCOL.md` for the exact mapping):
- `run_crosssim_*`: CrossSim comparisons
- `run_adc_*`, `run_convnext_adc_sweep.py`, `run_resnet18_adc_sweep.py`, `run_pure_digital_adc_sweep.py`: ADC-bit sweeps
- `run_nl_*`, `run_layer_*`, `run_layer_wise_nl_sensitivity.py`: nonlinearity / layer sensitivity
- `run_ensemble_*`, `run_ensemble_hat_ablation_FIXED.py`, `run_ensemble_hat_fixed.py`: HAT ablations
- `run_ir_drop_sensitivity_v3.py`, `run_retention_sensitivity.py`, `run_noise_sweep.py`, `run_device_comparison.py`, `run_contour_sweep.py`, `run_combined_nonideality.py`, `run_energy_sensitivity.py`, `run_zhang_sensitivity.py`, `run_sobol_analysis.py`, `run_statistical_validation.py`, `run_spatial_ablation.py`: physical/statistical sweeps
- `run_svhn_training.py`, `run_flowers102_training.py`, `run_cifar100_fast.py`, `run_a23_experiments.py`, `run_framework_comparison.py`, `run_visualization_suite.py`, `run_error_analysis.py`, `run_adc_cliff_analysis.py`: dataset / framework / misc

### 4.4 Plotting & reporting (5) — **live**

| Path | Purpose |
|:--|:--|
| `plot_convnext_results.py` | Per-architecture result plots |
| `plot_resnet18_results.py` | Per-architecture result plots |
| `visualize_attention.py` | Fig. 7 attention-map visualization |
| `generate_final_report.py` | Aggregates experiment JSONs into report |
| `report_asset_paths.py` | Enumerates asset → section mapping |

### 4.5 Utilities (9) — **live, library code**

| Path | Purpose |
|:--|:--|
| `analog_layers.py` | Core analog layer primitive (CIM simulation) |
| `analog_layers_ensemble.py` | Ensemble variant for HAT |
| `amp_utils.py` | Mixed-precision helpers |
| `device_profile_utils.py` | JSON profile loader/validator |
| `generate_synthetic_device_profiles_gpt.py` | Synthetic profile generator (keep name — called by notebooks) |
| `inference_analysis_utils.py` | Post-inference stats |
| `physical_noise_pipeline.py` | Noise-injection pipeline |
| `model_profiling.py` | Layer-wise profiling pass |
| `tinyvit_hybrid_utils.py` | Hybrid Tiny-ViT helpers |

### 4.6 Preparation / legacy-named helpers kept at root (7) — **live**

| Path | Purpose | Kept because |
|:--|:--|:--|
| `download_imagenet_val.py` | Pulls ImageNet val split | Reproducibility step in README |
| `prepare_imagenet_val.py` | Preprocesses ImageNet val | Same |
| `probe_resnet_ckpts.py` | Sanity-checks `checkpoints/R*` | Referenced by release checklist |
| `make_appendix.py` | Builds `paper/08_appendix.md` | Still called by paper build |
| `proxy_sensitivity_sweep_gpt.py` | Proxy-parameter sweep | Cited in Discussion |
| `experiment_nonideality_sweep.py` | Legacy-named nonideality sweep wrapper | Kept for backwards-compatible experiment entry |
| `ablation_ensemble_hat_vs_iid.py` | Legacy-named HAT-vs-IID ablation | Kept because rebuttal-side evidence still references it |

### 4.7 Tests (12) — **live**

All `test_*.py` at root are the actual pytest suite. Do not move.

`test_additional_datasets.py`, `test_analog_layers.py`, `test_checkpoint_behavior.py`, `test_device_profile_utils_gpt.py`, `test_eval_imagenet_analog.py`, `test_generate_synthetic_device_profiles_gpt.py`, `test_inference_analysis_utils.py`, `test_run_device_comparison.py`, `test_run_layer_sensitivity.py`, `test_train_convnext.py`, `test_train_tinyvit.py`, `test_visualize_attention.py`.

---

## 5. `paper/` — manuscript tree

### 5.1 Canonical LaTeX — **live** (under `paper/latex_gpt/`)

| Path | Purpose | Status |
|:--|:--|:--|
| `paper/latex_gpt/main.tex` | Main manuscript entry | live |
| `paper/latex_gpt/supplementary.tex` | Supplementary entry | live |
| `paper/latex_gpt/supplementary_main.tex` | Built-out supplementary | live |
| `paper/latex_gpt/cover_letter.tex` | Cover letter | live |
| `paper/latex_gpt/sections/00_abstract.tex` | Abstract | live |
| `paper/latex_gpt/sections/01_introduction.tex` | §1 | live |
| `paper/latex_gpt/sections/02_related_work.tex` | §2 | live |
| `paper/latex_gpt/sections/03_methodology.tex` | §3 | live |
| `paper/latex_gpt/sections/04_experimental_setup.tex` | §4 | live |
| `paper/latex_gpt/sections/05_results.tex` | §5 | live |
| `paper/latex_gpt/sections/06_discussion.tex` | §6 | live |
| `paper/latex_gpt/sections/07_conclusion.tex` | §7 | live |
| `paper/latex_gpt/sections/08_appendix.tex` | Appendix | live |
| `paper/latex_gpt/refs_gpt.bib` | Single canonical bibliography | live |
| `paper/latex_gpt/figures/` | Compiled figures consumed by `.tex` | live |
| `paper/latex_gpt/main.pdf` | 16pp, submission | live (frozen build output) |
| `paper/latex_gpt/supplementary_main.pdf` | 16pp, submission | live |
| `paper/latex_gpt/cover_letter.pdf` | 2pp | live |

### 5.2 `paper/latex_gpt/` supporting markdown — **live**

| Path | Purpose | Status |
|:--|:--|:--|
| `paper/latex_gpt/README_gpt.md` | How to compile | live |
| `paper/latex_gpt/SUBMISSION_PACKET_gpt.md` | What to upload where | live |
| `paper/latex_gpt/CITATION_MAP_gpt.md` | Which `\cite{}` maps to which journal | live |
| `paper/latex_gpt/CITATION_BACKLOG_gpt.md` | Pending citation queue | live |
| `paper/latex_gpt/CLOSEOUT_CHECKLIST_gpt.md` | Pre-submit gates | live |
| `paper/latex_gpt/TEMPLATE_MIGRATION_GUIDE_gpt.md` | npj→NC migration log | frozen |

### 5.3 `paper/` loose files — **mixed**

| Path | Purpose | Status |
|:--|:--|:--|
| `paper/01_introduction.md` … `paper/07_conclusion.md` | Pre-LaTeX markdown drafts | **draft-superseded** (do not edit; LaTeX is source of truth) |
| `paper/08_appendix.md` | Appendix draft — still regenerated by `make_appendix.py` | draft-superseded-but-regenerated |
| `paper/PAPER_OUTLINE.md` | Outline | frozen |
| `paper/CANONICAL_RESULT_LOCK_gpt.md` | Locked numeric results (86.37, 27.72, 88.53, S_ADC=0.976, …) | **frozen — single source of truth for numbers** |
| `paper/FIGURE_CAPTION_LOCK_gpt.md` | Authoritative captions | frozen |
| `paper/FIGURE_PLAN.md` | Figure plan, referenced by `plot_paper_figures.py` | live |
| `paper/FIG1_FIG2_BRIEF_gpt.md` | Fig 1/2 design notes | frozen |
| `paper/FIGURE_CAPTION_DRAFTS_gpt.md` | Caption drafts | frozen |
| `paper/参考文献库.md` | Chinese bibliography notes (superseded by `refs_gpt.bib`) | frozen |
| `paper/plot_paper_figures.py` | Canonical plotter for paper figures | live |
| `paper/fix_plots.py` | One-shot plot fix | live (referenced) |
| `paper/generate_schematic_figures_gpt.py` | Fig 1/2 schematic generator | live |
| `paper/figures/` (43 files) | Source PNG/PDF before latex_gpt/figures/ copy | live |
| `_archive/paper-drafts/BANANA_JOURNAL_SCHEMATIC_PROMPTS_20260408_gpt.md`, `NANOBANANA_SCHEMATIC_PROMPTS_gpt.md`, `PERPLEXITY_TARGETED_CITATION_PROMPTS_gpt.md` | Archived prompt-only figure ideation notes | archive |

---

## 6. `report_md/` — reports tree

### 6.1 Root (non-`_gpt/`)

| Path | Purpose | Status |
|:--|:--|:--|
| `report_md/A1_implementation_plan.md` | Original implementation plan | frozen |
| `report_md/claude-report.md` | Claude's narrative report | live |
| `report_md/claude全栈参考手册.md` | Full-stack reference (Chinese) | frozen |
| `report_md/deep-research-report.md` | Deep-research output | frozen |
| `report_md/Gemini.md` | Gemini coordination landing | live |
| `report_md/a23_physical_compensation_report.md` | A23 report | frozen |
| `report_md/array_mapping_report.md` | Array mapping report | frozen |
| `report_md/convnext_experiment_report.md` | ConvNeXt report | frozen |
| `report_md/physical_noise_report.md` | Noise report | frozen |
| `report_md/resnet18_experiment_report.md` | ResNet-18 report | frozen |
| `report_md/Organic_Optoelectronic_Task_Simulation.pdf`, `report_md/Organic_Optoelectronic_Task_Simulation_(2).pptx` | Current internal presentation assets | live |
| `report_md/*.pdf` (literature PDFs) | Reference papers | reference |
| `report_md/*.docx` | Doctor's 8th-draft manuscript | reference |
| `report_md/csv/`, `report_md/images/`, `report_md/json/` | Report assets | live |
| `report_md/参考文献2.md` | Chinese ref notes | frozen |

### 6.2 `report_md/_gpt/` — live coordination

Canonical live coordination layer. Key entries:

| Path | Purpose | Status |
|:--|:--|:--|
| `AGENT_SYNC_gpt.md` | **The** live multi-agent sync log — append-only | live |
| `CLAUDE_TASK_gpt.md` | Claude's active task ledger (TX-1..TX-29) | live |
| `KIMI_TASK_gpt.md` | Kimi's task ledger (archived copy in `_archive/coordination/`) | frozen |
| `MASTER_DISPATCH_20260415_PHASE3_gpt.md` | Phase-3 master dispatch | frozen |
| `CODEX_DISPATCH_20260417_cleanup_gpt.md` | Dispatch #7 brief | frozen |
| `CODEX_DISPATCH_20260417_tidy_gpt.md` | Dispatch #8 brief | frozen |
| `CLEANUP_MANIFEST_20260417.md` | Dispatch #7 manifest | frozen |
| `TIDY_MANIFEST_20260417.md` | Dispatch #8 manifest | frozen |
| `BROADCAST_CLEANUP_COMPLETE_20260417_gpt.md` | Dispatch #7 closeout | frozen |
| `KIMI_KM1_KM7_REPORTS.md` | Rescued Kimi proofreading | frozen |
| `REVIEWER_COVERAGE_MATRIX_gpt.md` | Reviewer coverage matrix | live |
| `REVIEWER_RESPONSE_DRAFT_gpt.md` | Response draft | live |
| `EXTERNAL_REVIEW_FOLLOWUP_20260417.md` | External reviewer follow-up | live |
| `EXTERNAL_REVIEW_SYNTHESIS_20260417.md` | Synthesis of external reviews | frozen |
| `FIGURE_PROVENANCE_MANIFEST_20260417.md` | Provenance of every figure | frozen |
| `FINAL_ALIGNMENT_CHECKLIST_20260417.md` | Final alignment checklist | live |
| `SUBMISSION_BUNDLE_CHECKLIST_20260417.md` | Submission bundle gate | live |
| `SUBMISSION_PREFLIGHT_20260416.md` | Preflight report | frozen |
| `NUMERIC_CONSISTENCY_AUDIT_20260417.md` | Numbers audit | frozen |
| `REVIEWER_ARCHIVE_MANIFEST_20260417.md` | Reviewer archive manifest | live |
| remaining 50 files | Dispatches, audits, handoffs from 2026-04-12→04-17 | mostly frozen |

To list all: `ls report_md/_gpt/*.md`.

---

## 7. Data & checkpoints

| Path | Contents | Status |
|:--|:--|:--|
| `checkpoints/` (24 GB) | `.pt` weights: R1–R6, C1–C9, V1–V6, HAT variants | live (gitignored) |
| `data/` | CIFAR-10, CIFAR-100, Flowers-102, ImageNet, SVHN, TinyImageNet | live (gitignored) |
| `device_profiles/example_measured_device_profile_gpt.json` | Template profile | live |
| `device_profiles/literature_profiles_gpt.json` | Literature (Zhang 2025) | live |
| `device_profiles/synthetic_profiles_gpt.json` | Synthetic profile set | live |
| private measured raw-data tree | Not versioned in the public repo | excluded from release |

---

## 8. `_archive/` — everything retired (growing tree) — **DO NOT READ UNLESS DEBUGGING HISTORY**

All reversible via `mv`. Nothing here is on the submission path.

| Subdir | Count | Contents |
|:--|:--:|:--|
| `_archive/coordination/` | 179 | Historical dispatches, handoffs, broadcasts, Kimi KX reports, GEMINI_* tasks, old AGENT_SYNC backups |
| `_archive/figure-drafts/` | 12 | Intermediate `banana` / `clean` / `crop` / `enhanced` figure-art variants |
| `_archive/historical-dirs/` | 2 | `npj_submission_package/` (pre-NC repositioning), `paper_zh/` (Chinese mirror) |
| `_archive/logs-pre-april04/` | 11 | `logs/*.log` dated 2026-04-03 |
| `_archive/old-experiment-data/` | 5 | `exp_asymmetry_*.txt`, `PAPER_METHODS_PARAGRAPH.txt`, `tex_diff.txt` |
| `_archive/old-experiment-json/` | 19 | Old JSON dumps (adc_nonideality, ir_drop, retention, combined_stress, etc.) |
| `_archive/paper-drafts/` | 4 | `仿真.tex` plus retired prompt-only paper notes |
| `_archive/scripts-oneshot/` | 51 | one-shot helper scripts and dated shell queues retired from the repo root |
| `_archive/scripts-versions/` | 9 | Older `_v1`/`_v2` siblings superseded by current `_v3`/`_FIXED`/`_fixed` |

---

## 9. `outputs/` — submission & reviewer bundles (live)

| Path | Purpose | Status |
|:--|:--|:--|
| `outputs/submission_bundle_20260417/` | Current NC submission bundle (main.pdf, supp, cover, source data, responses) | **live, submission-facing** |
| `outputs/submission_bundle_20260417.tar.gz` | Tarball of the above | live |
| `outputs/reviewer_archive_20260417/` | External reviewer archive (audit/, code_snapshot/, manuscript/, response/, source_data/, INVENTORY.txt) | live |
| `outputs/reviewer_archive_20260417.tar.gz` | Tarball | live |
| `outputs/measured_profile_runs/` | Measured-profile eval outputs | live |

---

## 10. `scripts/`, `docs/`, `logs/`, `tmp/`, `internal/`

| Path | Purpose | Status |
|:--|:--|:--|
| `scripts/monitor_kimi_ablation_outputs.py` | Watcher for Kimi ablation runs | live |
| `scripts/_gpt/` (17 shell + py) | Multi-seed runners, queue scripts, p13 monitors | live |
| `docs/DEVICE_PROFILE_GUIDE.md` | How to build a device profile | live |
| `docs/EXPERIMENT_REGISTRY.md` | Registry of every experiment | live |
| `docs/PHYSICS_STACK.md` | Physics assumptions | live |
| `docs/README.md`, `docs/REPO_HYGIENE_AND_GIT_POLICY.md` | Policy docs | live |
| `logs/` | `.log` dumps. Pre-2026-04-04 moved to `_archive/logs-pre-april04/`. Active logs remain | live (gitignored) |
| sibling `tmp/` workspace | Cross-repo scratch outside `compute_vit/`. Everything there is disposable | scratch |
| `internal/` | Local scratch, gitignored | scratch |
| `AGENT_SYNC/` (dir) | 7 files, 2026-04-15 artifact. Superseded by `report_md/_gpt/AGENT_SYNC_gpt.md` but kept in place — has a script caller noted in TIDY_MANIFEST | frozen (do not rename) |

---

## 11. What to do if you're unsure

1. **Is it live?** → check §3–§6 above. If listed as `live`, don't move/rename.
2. **Is it duplicated?** → check if the canonical sibling exists (e.g., `run_ir_drop_sensitivity_v3.py` is canonical; v1/v2 are archived).
3. **Does it have date in the name?** → probably frozen. Keep, don't edit.
4. **Is it under `_archive/`?** → history only. Don't reference from live code.
5. **Still unsure?** → `grep -rln "<filename>"` across the repo. If only referenced from `_archive/`, it's dead.

---

## 12. Invariants (these must always hold)

- `compute_vit/run_*.py` count = **39** (experiment driver whitelist).
- `paper/latex_gpt/main.pdf` = 16 pages, `supplementary_main.pdf` = 16 pages, `cover_letter.pdf` = 2 pages.
- `paper/latex_gpt/refs_gpt.bib` is the only bibliography. Do not create a second `.bib`.
- `paper/CANONICAL_RESULT_LOCK_gpt.md` holds the one source of truth for all numbers in the paper. Never edit a number in `.tex` without updating the lock file first.
- `_archive/` content is append-only. Never delete from it without user sign-off.
- `checkpoints/` and `data/` contents: never moved or renamed by agents during active experiments.

---

*Last updated: 2026-04-17 (post Dispatch #7, #8, and `_archive/` consolidation).*
*Next full review due: before NC submission, or on next significant structural change.*
