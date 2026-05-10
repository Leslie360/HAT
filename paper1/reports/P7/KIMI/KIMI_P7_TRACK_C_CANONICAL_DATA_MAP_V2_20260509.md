# Kimi P7 Track C: Canonical Data Location Map v2

**Date:** 2026-05-09
**Scope:** All canonical, provenance, deprecated, and remote-only data sources

---

## 1. Paper-1 Local Canonical Data

| Path | Type | Status | DO_NOT_DELETE | Note |
|------|------|--------|---------------|------|
| `paper/latex_gpt/source_data/canonical_json/` | Canonical | Active | ✅ YES | Master canonical JSON directory |
| `paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed123/` | Canonical | Active | ✅ YES | 8-bit PCM seed123 |
| `paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed456/` | Canonical | Active | ✅ YES | 8-bit PCM seed456 |
| `paper/latex_gpt/source_data/canonical_json/pcm_8bit_seed789/` | Canonical | Active | ✅ YES | 8-bit PCM seed789 |
| `paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed123/` | Canonical | Active | ✅ YES | 6-bit PCM seed123 (rerun complete) |
| `paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed456/` | Canonical | Active | ✅ YES | 6-bit PCM seed456 |
| `paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed457/` | Canonical | Active | ✅ YES | 6-bit PCM seed457 |
| `paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed789/` | Canonical | Active | ✅ YES | 6-bit PCM seed789 |
| `paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed123/` | Canonical | Active | ✅ YES | 4-bit PCM seed123 |
| `paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed456_clean/` | Canonical | Active | ✅ YES | 4-bit PCM seed456 |
| `paper/latex_gpt/source_data/canonical_json/pcm_4bit_seed789/` | Canonical | Active | ✅ YES | 4-bit PCM seed789 |
| `paper/latex_gpt/source_data/canonical_json/pure_4bit_collapse/` | Canonical | Active | ✅ YES | Pure 4-bit collapse baseline |
| `paper/latex_gpt/source_data/canonical_json/ideal_8bit_sigma010_aihwkit_baseline/` | Canonical | Active | ✅ YES | Ideal 8-bit baseline |
| `paper/latex_gpt/source_data/canonical_json/ensemble_hat_4bit_3seed/` | Canonical | Active | ✅ YES | Ensemble HAT 4-bit 3-seed |
| `paper/latex_gpt/source_data/canonical_json/README.md` | Provenance | Active | ✅ YES | Canonical JSON manifest |
| `paper/latex_gpt/source_data/canonical_json/manifest_canonical_json_20260509.csv` | Provenance | Active | ✅ YES | Manifest CSV |
| `paper/latex_gpt/source_data/canonical_json/manifest_canonical_json_20260509.json` | Provenance | Active | ✅ YES | Manifest JSON |
| `paper/latex_gpt/source_data/canonical_json/deprecated_20260501_old_protocol/` | Deprecated | Archived | ⚠️ REVIEW | Old protocol data; keep for provenance |
| `paper/latex_gpt/source_data/*.csv` | Canonical | Active | ✅ YES | Source data tables (tab_pcm_precision_ladder, fig1_spine, fig2_decision_map) |
| `paper/latex_gpt/source_data/manifest_paper1_spine.json` | Provenance | Active | ✅ YES | Figure 1 manifest |

---

## 2. Release Artifacts

| Path | Type | Status | DO_NOT_DELETE | Note |
|------|------|--------|---------------|------|
| `release_artifacts/paper1_submission_bundle_20260509_final/` | Release | Active | ✅ YES | Final submission bundle (135 files) |
| `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | Release | Active | ✅ YES | Final tarball (SHA256 verified) |
| `release_artifacts/paper1_provenance_archive_20260509/` | Provenance | Active | ✅ YES | Historical provenance (73 files) |
| `release_artifacts/paper1_provenance_archive_20260509.tar.gz` | Provenance | Active | ✅ YES | Provenance tarball |
| `release_artifacts/paper1_release_candidate_20260509/` | Release | Obsolete | ⚠️ REVIEW | Superseded by final bundle |
| `release_artifacts/paper1_release_candidate_20260509_clean/` | Release | Obsolete | ⚠️ REVIEW | Superseded by final bundle |

---

## 3. Remote Review Data

| Path | Type | Status | DO_NOT_DELETE | Note |
|------|------|--------|---------------|------|
| `HAT_105_results_review/` | Remote | Active | ✅ YES | Remote 105 data review directory |
| `HAT_107_clean_review/` | Remote | Active | ✅ YES | Remote 107 data review directory |

---

## 4. Scripts and Guards

| Path | Type | Status | DO_NOT_DELETE | Note |
|------|------|--------|---------------|------|
| `scripts/_gpt/check_local_pcm_precision_ladder.py` | Guard | Active | ✅ YES | PCM precision ladder verification |
| `scripts/_gpt/plot_paper1_spine.py` | Tool | Active | ✅ YES | Figure 1 generation |
| `scripts/_gpt/plot_r11d_batch_bcd_figures.py` | Tool | Active | ✅ YES | R11D figure generation |
| `scripts/_gpt/eval_fresh_instance_selective.py` | Tool | Active | ✅ YES | Fresh eval utility |

---

## 5. Deprecated / Old Protocol

| Path | Type | Status | DO_NOT_DELETE | Note |
|------|------|--------|---------------|------|
| `paper/latex_gpt/source_data/canonical_json/deprecated_20260501_old_protocol/` | Deprecated | Archived | ⚠️ REVIEW | Old protocol canonical JSON; keep for provenance until thesis complete |
| `paper2_aihwkit_baseline/checkpoints/r11d_6bit_pcm_seed123_P6_BACKUP_20260509/` | Backup | Temporary | ⚠️ REVIEW | P6 rerun backup; can be moved to archive after verification |

---

## 6. Large Data Exclusions (Already .gitignore'd)

| Path | Size | Type | DO_NOT_DELETE | Note |
|------|------|------|---------------|------|
| `checkpoints/` | 33 GB | Experiment outputs | ✅ YES (local) | Old experiment checkpoints; keep locally, never commit |
| `data/` | 15 GB | Datasets | ✅ YES (local) | CIFAR-10, TinyImageNet; keep locally, never commit |
| `paper2_aihwkit_baseline/checkpoints/` | ~6 GB | AIHWKit outputs | ✅ YES (local) | AIHWKit experiment checkpoints; keep locally |

---

## 7. Summary Table

| Category | Count | DO_NOT_DELETE | Action |
|----------|-------|---------------|--------|
| Canonical JSON (active) | 15 dirs + 3 manifests | ✅ All | Keep active |
| Source data CSV/JSON | 5 files | ✅ All | Keep active |
| Release artifacts (final) | 2 items | ✅ Both | Keep active |
| Release artifacts (obsolete) | 2 dirs | ⚠️ Review | Quarantine after user confirmation |
| Provenance archive | 2 items | ✅ Both | Keep permanently |
| Remote review data | 2 dirs | ✅ Both | Keep until remote work complete |
| Deprecated/old protocol | 2 items | ⚠️ Review | Keep for thesis provenance |
| Large local data | 3 dirs | ✅ (local only) | Keep in .gitignore |

---

## 8. Verdict

| Check | Result |
|-------|--------|
| All canonical sources identified | ✅ YES |
| All provenance sources identified | ✅ YES |
| All deprecated sources flagged | ✅ YES |
| All remote-only sources flagged | ✅ YES |
| DO_NOT_DELETE column complete | ✅ YES |
| 105/107 clone directories included | ✅ YES |
| Final bundle protected | ✅ YES |
| Large files excluded from commit scope | ✅ YES |

**Track C Status: COMPLETE**

---

*Report by kimi. 2026-05-09.*
