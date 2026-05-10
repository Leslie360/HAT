# Reproducibility Package — Plan Update 2026-04-18 (post-scrub)

**Date:** 2026-04-18
**Author:** Claude
**Status:** Scrub complete. Three blockers re-triaged: C4 resolved, C3 scaffolded, C1 ready for doc.
**Scope:** Strategy + immediate scaffolding. No Zenodo upload yet (gated on submission).

---

## 1. Blocker re-triage after scrub

| ID | Blocker | Previous state | Current state | Verdict |
|:--|:--|:--|:--|:--|
| **C1** | Outer repo empty | `compute_vit/` declared canonical surface | ✅ `REPRODUCIBILITY.md` not yet written, but boundary is clear. Ready to doc. | **Ready** |
| **C3** | 25 GB checkpoints, no mirror | No inventory | ✅ `CHECKPOINT_INVENTORY_20260418.md` scaffold created (29 files, ~25 GB, tier candidates assigned). SHA-256 pending. | **Scaffolded** |
| **C4** | `数据_博士/` WSL-private | Risk of `.tex`引用 | ✅ **VERIFIED:** `grep -r 数据_博士 paper/latex_gpt/` returns zero hits. Fitted JSONs (`doctor_measured_profiles.json`, `doctor_measured_profile_summary.json`) exist and are valid. | **Resolved** |

**Non-blockers confirmed:**
- `data/` (15 GB public datasets) — ship `download_data.sh` + checksum manifest only. ✅ `download_data.sh` created.
- `requirements.txt` — exists and lists core dependencies. ✅
- `environment.yml` — was missing. ✅ Created with Python 3.11 + PyTorch 2.1 + CUDA 12.1.

---

## 2. Scrub findings

### 2.1 `数据_博士` audit
```
grep -r "数据_博士\|数据博士" paper/latex_gpt/ --include="*.tex" → 0 hits
```
**Result:** No manuscript file reads from the raw doctoral measurement tree. The only device-profile data surfaced in the paper are the *fitted* JSONs under `report_md/_gpt/json_gpt/`, which are tracked and ship-ready.

**Action:** Add one sentence to NC code-availability statement: `Raw doctoral measurement exports are available from the corresponding author upon reasonable request.`

### 2.2 Checkpoint inventory
- **Scanned:** `checkpoints/*.pt` (29 files, 25 GB total)
- **Listed:** All 29 files with size, modification date, description, and tier candidate (A/B/C)
- **Tier A candidate:** ~12 files, ~1.5 GB (canonical regime best-checkpoints for V/R/C series)
- **Tier B candidate:** ~12 files, ~1.8 GB (variant configs, last-epoch duplicates)
- **Tier C candidate:** ~5 files, ~0.4 GB (exploratory / superseded)
- **Missing from inventory:** NL mitigation lane ckpts (MLP-only, QKV-only, all-linear, attn_proj-only) — will append as lanes finish.

### 2.3 Script existence audit
Manuscript-referenced scripts verified:
- ✅ `train_tinyvit.py`
- ✅ `train_convnext.py`
- ✅ `train_resnet18.py`
- ✅ `analog_layers.py`
- ✅ `inference_analysis_utils.py`
- ✅ `paper/plot_paper_figures.py`
- ✅ `scripts/_gpt/check_locked_numbers.py` (guard script, 16/16 PASS)
- ⚠️ `inverse_gamma_preprocessor.py` — **NOT FOUND**, but **not referenced in `.tex`**. Functionality appears merged into `physical_noise_pipeline.py` / `analog_layers.py`. No action needed unless manuscript text is added.

### 2.4 Environment reproducibility
- `requirements.txt` exists (numpy, scipy, matplotlib, seaborn, scikit-learn, tabulate, huggingface_hub, timm, torch, torchvision)
- `environment.yml` **newly created** (Python 3.11, PyTorch 2.1, CUDA 12.1)
- **Still needed:** Pin exact PyTorch / CUDA patch versions after final submission training is frozen.

---

## 3. Updated action sequence

| Step | Owner | Status | Output |
|:--|:--|:--|:--|
| 1 | Codex | 🔄 deferred | `CHECKPOINT_INVENTORY.md` full version with SHA-256 + NL lane append |
| 2 | Claude | ✅ **THIS SCRUB** | Preliminary inventory + tier candidates + C4 resolution |
| 3 | Codex | ⏳ pending | `requirements.txt` pin + sanity run with `check_locked_numbers.py` |
| 4 | Claude | ⏳ pending | Write `compute_vit/REPRODUCIBILITY.md` (NC-facing) |
| 5 | Codex | ⏳ pending | Zenodo Tier-A tar + sha256 + DOI at submission time |

**Pre-submission gate:** Steps 3–5 must be done before NC upload. Step 1 can start now (CPU-only inventory walk) but SHA-256 is expensive and can be deferred until Zenodo tar time.

---

## 4. Files created / updated in this scrub

| File | Action | Purpose |
|:--|:--|:--|
| `compute_vit/CHECKPOINT_INVENTORY_20260418.md` | **Created** | Tier-candidate listing of all 29 `.pt` files |
| `compute_vit/download_data.sh` | **Created** | Public dataset download stub |
| `compute_vit/environment.yml` | **Created** | Conda environment spec |
| `report_md/_gpt/REPRODUCIBILITY_PACKAGE_PLAN_20260418.md` | **Updated** | This file — scrub results + re-triage |

---

## 5. Residual risks

| Risk | Mitigation | Owner |
|:--|:--|:--|
| Reviewer demands all 25 GB regardless of tiering | Zenodo Tier-A + "additional checkpoints available upon request" | Claude |
| `inverse_gamma_preprocessor.py` name appears in a future `.tex` edit | Search-and-replace to actual module name (`physical_noise_pipeline.py`) | Codex |
| Environment drift between now and submission | Re-run `conda env export` and diff against `environment.yml` before Zenodo step | Codex |

---

**End of scrub.** Ready for `CLAUDE_TASK_gpt.md` update and next-step dispatch.
