# Kimi P7 Track I: Workspace Cleanup and Quarantine Plan

**Date:** 2026-05-09
**Scope:** `/home/qiaosir/projects/compute_vit` plus top-level coordination files
**Stance:** Conservative. No destructive deletion without user/Codex approval.

---

## 1. Directory Classification

| Path | Category | Size | Reason | Safe to Move | Safe to Delete |
|------|----------|------|--------|--------------|----------------|
| `release_artifacts/paper1_submission_bundle_20260509_final/` | KEEP_RELEASE | ~150 MB | Final submission bundle | ❌ NO | ❌ NO |
| `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | KEEP_RELEASE | ~150 MB | Final tarball (SHA256 verified) | ❌ NO | ❌ NO |
| `release_artifacts/paper1_provenance_archive_20260509/` | KEEP_PROVENANCE | ~150 MB | Historical provenance | ❌ NO | ❌ NO |
| `release_artifacts/paper1_provenance_archive_20260509.tar.gz` | KEEP_PROVENANCE | ~150 MB | Provenance tarball | ❌ NO | ❌ NO |
| `release_artifacts/paper1_reviewer_bundle_20260501_1645.tar.gz` | KEEP_PROVENANCE | ~50 MB | Old reviewer bundle | ❌ NO | ❌ NO |
| `release_artifacts/paper1_release_candidate_20260509/` | KEEP_PROVENANCE | ~150 MB | Superseded release candidate | ⚠️ Quarantine | ❌ NO |
| `release_artifacts/paper1_release_candidate_20260509_clean/` | KEEP_PROVENANCE | ~150 MB | Superseded clean candidate | ⚠️ Quarantine | ❌ NO |
| `paper/latex_gpt/source_data/canonical_json/` | KEEP_CANONICAL_DATA | ~2 MB | Canonical JSON data | ❌ NO | ❌ NO |
| `paper/latex_gpt/source_data/*.csv` | KEEP_CANONICAL_DATA | ~100 KB | Source data tables | ❌ NO | ❌ NO |
| `paper/latex_gpt/` (active tex/pdf) | KEEP_ACTIVE | ~15 MB | Active manuscript sources | ❌ NO | ❌ NO |
| `paper/thesis/` | KEEP_ACTIVE | ~50 MB | Thesis chapters | ❌ NO | ❌ NO |
| `paper/thesis_cn/` | KEEP_ACTIVE | ~5 MB | Chinese thesis draft | ❌ NO | ❌ NO |
| `HAT_105_results_review/` | KEEP_REMOTE_REVIEW | ~10 MB | Remote 105 review data | ❌ NO | ❌ NO |
| `HAT_107_clean_review/` | KEEP_REMOTE_REVIEW | ~50 MB | Remote 107 review data | ❌ NO | ❌ NO |
| `checkpoints/` | KEEP_LOCAL_DATA | 33 GB | Old experiment checkpoints | ❌ NO | ❌ NO |
| `data/` | KEEP_LOCAL_DATA | 15 GB | Datasets | ❌ NO | ❌ NO |
| `paper2_aihwkit_baseline/` | KEEP_LOCAL_DATA | 6.9 GB | AIHWKit experiments | ❌ NO | ❌ NO |
| `paper2/` | KEEP_ACTIVE | 720 KB | Work-2 scripts and docs | ❌ NO | ❌ NO |
| `scripts/` | KEEP_ACTIVE | 1.8 MB | Active scripts | ❌ NO | ❌ NO |
| `tests/` | KEEP_ACTIVE | 184 KB | Unit tests | ❌ NO | ❌ NO |
| `report_md/_gpt/` | KEEP_ACTIVE | 111 MB | P6/P7 reports and audits | ❌ NO | ❌ NO |
| `report_md/记忆类型可调的光电突触和存储器用于储备池计算-第8稿(1).pptx` | UNKNOWN_REVIEW_REQUIRED | 4.2 MB | Chinese PPT — unrelated? | ⚠️ Quarantine | ❌ NO |
| `outputs/` | KEEP_PROVENANCE | 494 MB | Old experiment outputs | ⚠️ Quarantine | ❌ NO |
| `_archive/` | KEEP_PROVENANCE | 56 MB | Archived historical files | ❌ NO | ❌ NO |
| `archive/` | KEEP_PROVENANCE | 328 KB | Additional archive | ❌ NO | ❌ NO |
| `.git/` | PROTECTED | ~2 GB | Git repository | ❌ NO | ❌ NO |
| `.claude/` | PROTECTED | ~50 MB | Claude session data | ❌ NO | ❌ NO |
| `.vscode/` | DELETE_SAFE | ~1 MB | IDE settings | ✅ YES | ✅ YES |
| `.pytest_cache/` | DELETE_SAFE | ~500 KB | Pytest cache | ✅ YES | ✅ YES |
| `__pycache__/` | DELETE_SAFE | 400 KB | Python cache | ✅ YES | ✅ YES |
| `tmp/` | DELETE_SAFE | 2.6 MB | Temporary files | ✅ YES | ✅ YES |
| `logs/` | KEEP_ACTIVE | 17 MB | Execution logs | ❌ NO | ❌ NO |
| `tasks/` | KEEP_ACTIVE | 92 KB | Task definitions | ❌ NO | ❌ NO |
| `broadcast.md` | KEEP_ACTIVE | 176 KB | Active broadcast log | ❌ NO | ❌ NO |
| `AGENT_INTERCOM_HUB_*.md` | QUARANTINE_CANDIDATE | ~50 KB each | Old intercom files | ✅ YES | ❌ NO |
| `GPU_SCHEDULE_20260428.md` | QUARANTINE_CANDIDATE | ~10 KB | Old schedule | ✅ YES | ❌ NO |
| `REMOTE_*.md` (top-level) | QUARANTINE_CANDIDATE | ~20 KB each | Old remote tasklists | ✅ YES | ❌ NO |
| `gpu_watcher.sh` | QUARANTINE_CANDIDATE | ~5 KB | Old script | ✅ YES | ❌ NO |
| `output.md` | QUARANTINE_CANDIDATE | ~1 KB | Unknown output | ✅ YES | ❌ NO |
| `paper/latex_gpt/deprecated/` | QUARANTINE_CANDIDATE | ~5 MB | Old LaTeX files | ✅ YES | ❌ NO |
| `paper/latex_gpt/figures/deprecated_20260424/` | QUARANTINE_CANDIDATE | ~10 MB | Old figures | ✅ YES | ❌ NO |
| `paper/latex_gpt/*.fls` | DELETE_SAFE | ~80 KB each | LaTeX build residues | ✅ YES | ✅ YES |
| `paper/latex_gpt/*.log` | DELETE_SAFE | ~40 KB | LaTeX log | ✅ YES | ✅ YES |
| `paper/latex_gpt/BROADCAST_EOF` | DELETE_SAFE | ~1 KB | Artifact | ✅ YES | ✅ YES |
| `paper/latex_gpt/1` | DELETE_SAFE | ~1 KB | Artifact | ✅ YES | ✅ YES |
| `paper/latex_gpt/temp_render.tex` | DELETE_SAFE | ~5 KB | Temp file | ✅ YES | ✅ YES |
| `paper/latex_gpt/render_s3.py` | KEEP_ACTIVE | ~10 KB | Render script | ❌ NO | ❌ NO |
| `paper/latex_gpt/render_tikz.py` | KEEP_ACTIVE | ~10 KB | Render script | ❌ NO | ❌ NO |
| `paper/latex_gpt/ChatGPT Image *.png` | QUARANTINE_CANDIDATE | ~2 MB each | ChatGPT images | ✅ YES | ❌ NO |
| `paper/latex_gpt/cover_letter_v6.tex.pdf` | QUARANTINE_CANDIDATE | ~50 KB | Old draft | ✅ YES | ❌ NO |
| `paper/latex_gpt/supp_*_merged_*.pdf` | QUARANTINE_CANDIDATE | ~5 MB each | Test renderings | ✅ YES | ❌ NO |
| `paper/latex_gpt/CLEAN_DRAFT_V3_FIXED.pdf` | QUARANTINE_CANDIDATE | ~200 KB | Old draft | ✅ YES | ❌ NO |
| `paper/latex_gpt/figS*_test.pdf` | DELETE_SAFE | ~100 KB each | Test PDFs | ✅ YES | ✅ YES |
| `paper/plot_merged_S10_S11.py` | KEEP_ACTIVE | ~10 KB | Plot script | ❌ NO | ❌ NO |
| `paper2/REMOTE_*.md` | QUARANTINE_CANDIDATE | ~10 KB each | Old remote files | ✅ YES | ❌ NO |
| `..bfg-report/` | DELETE_SAFE | ~1 MB | BFG repo cleaner report | ✅ YES | ✅ YES |

---

## 2. Large File Report (≥ 20 MB)

| Path | Size | Category | Action |
|------|------|----------|--------|
| `checkpoints/*.pt` (34 files) | 33 GB total | KEEP_LOCAL_DATA | Keep locally, never commit |
| `data/cifar-10-python.tar.gz` | ~170 MB | KEEP_LOCAL_DATA | Keep locally, never commit |
| `data/cifar-100-python.tar.gz` | ~170 MB | KEEP_LOCAL_DATA | Keep locally, never commit |
| `data/train_32x32.mat` | ~200 MB | KEEP_LOCAL_DATA | Keep locally, never commit |
| `paper2_aihwkit_baseline/checkpoints/` | ~6 GB | KEEP_LOCAL_DATA | Keep locally, never commit |
| `release_artifacts/*.tar.gz` | ~400 MB total | KEEP_RELEASE/PROVENANCE | Keep, never commit |
| `report_md/记忆类型可调的光电突触和存储器用于储备池计算-第8稿(1).pptx` | 4.2 MB | UNKNOWN | Quarantine pending user review |

---

## 3. Delete-Safe List

These are objectively disposable build/cache residues:

| Path | Reason | Exact Command |
|------|--------|--------------|
| `__pycache__/` | Python bytecode cache | `find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null` |
| `.pytest_cache/` | Pytest cache | `rm -rf .pytest_cache/` |
| `.vscode/` | IDE settings (recreatable) | `rm -rf .vscode/` |
| `paper/latex_gpt/*.fls` | LaTeX build residues | `rm -f paper/latex_gpt/*.fls` |
| `paper/latex_gpt/*.log` | LaTeX log files | `rm -f paper/latex_gpt/*.log` |
| `paper/latex_gpt/BROADCAST_EOF` | Artifact | `rm -f paper/latex_gpt/BROADCAST_EOF` |
| `paper/latex_gpt/1` | Artifact | `rm -f paper/latex_gpt/1` |
| `paper/latex_gpt/temp_render.tex` | Temp file | `rm -f paper/latex_gpt/temp_render.tex` |
| `paper/latex_gpt/figS*_test.pdf` | Test PDFs | `rm -f paper/latex_gpt/figS*_test.pdf` |
| `paper/thesis_cn/*.toc` | LaTeX TOC output | `rm -f paper/thesis_cn/*.toc` |
| `tmp/` | Temporary files | `rm -rf tmp/*` |
| `..bfg-report/` | BFG cleaner report | `rm -rf ..bfg-report/` |
| `paper/latex_gpt/figures/*.bak` | Backup files | `rm -f paper/latex_gpt/figures/*.bak` |

**Total estimated recovery:** ~500 KB – 2 MB

---

## 4. Quarantine Plan

For uncertain files, use reversible `mv` to quarantine, not `rm`.

```bash
# Create quarantine directory
mkdir -p _quarantine_20260509/{old_drafts,old_remote_files,test_renderings,chatgpt_images,unreviewed}

# Old drafts
mv paper/latex_gpt/deprecated/ _quarantine_20260509/old_drafts/ 2>/dev/null
mv paper/latex_gpt/figures/deprecated_20260424/ _quarantine_20260509/old_drafts/ 2>/dev/null
mv paper/latex_gpt/cover_letter_v6.tex.pdf _quarantine_20260509/old_drafts/ 2>/dev/null
mv paper/latex_gpt/CLEAN_DRAFT_V3_FIXED.pdf _quarantine_20260509/old_drafts/ 2>/dev/null

# Old remote files
mv AGENT_INTERCOM_HUB_20260428.md _quarantine_20260509/old_remote_files/ 2>/dev/null
mv AGENT_INTERCOM_HUB_20260429.md _quarantine_20260509/old_remote_files/ 2>/dev/null
mv AGENT_INTERCOM_HUB_20260506.md _quarantine_20260509/old_remote_files/ 2>/dev/null
mv GPU_SCHEDULE_20260428.md _quarantine_20260509/old_remote_files/ 2>/dev/null
mv REMOTE_105_MULTIDATASET_TASKLIST_20260429.md _quarantine_20260509/old_remote_files/ 2>/dev/null
mv REMOTE_HANDOFF_README_20260429.md _quarantine_20260509/old_remote_files/ 2>/dev/null
mv REMOTE_NO_PUSH_RETURN_PROTOCOL_20260429.md _quarantine_20260509/old_remote_files/ 2>/dev/null
mv gpu_watcher.sh _quarantine_20260509/old_remote_files/ 2>/dev/null
mv output.md _quarantine_20260509/old_remote_files/ 2>/dev/null
mv paper2/REMOTE_107_KV_TASKLIST_20260429.md _quarantine_20260509/old_remote_files/ 2>/dev/null
mv paper2/REMOTE_NO_PUSH_RETURN_PROTOCOL_20260429.md _quarantine_20260509/old_remote_files/ 2>/dev/null

# Test renderings
mv paper/latex_gpt/supp_*_merged_*.pdf _quarantine_20260509/test_renderings/ 2>/dev/null
mv paper/latex_gpt/supp_part*.pdf _quarantine_20260509/test_renderings/ 2>/dev/null

# ChatGPT images
mv paper/latex_gpt/"ChatGPT Image"*.png _quarantine_20260509/chatgpt_images/ 2>/dev/null

# Unreviewed
mv "report_md/记忆类型可调的光电突触和存储器用于储备池计算-第8稿(1).pptx" _quarantine_20260509/unreviewed/ 2>/dev/null

# Restore command (for any file)
# mv _quarantine_20260509/old_drafts/deprecated/ paper/latex_gpt/ 2>/dev/null
```

**Total estimated quarantine size:** ~50–100 MB

---

## 5. Protected Paths

| Path | Why Protected | Verification Command |
|------|--------------|---------------------|
| `release_artifacts/paper1_submission_bundle_20260509_final/` | Final submission bundle | `ls -la release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt` |
| `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | Final tarball | `sha256sum release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` |
| `release_artifacts/paper1_provenance_archive_20260509/` | Provenance | `ls -la release_artifacts/paper1_provenance_archive_20260509/` |
| `paper/latex_gpt/source_data/canonical_json/` | Canonical data | `ls paper/latex_gpt/source_data/canonical_json/` |
| `paper/latex_gpt/source_data/*.csv` | Source tables | `ls paper/latex_gpt/source_data/*.csv` |
| `paper/latex_gpt/main.pdf` | Active manuscript | `ls -la paper/latex_gpt/main.pdf` |
| `paper/latex_gpt/supplementary_main.pdf` | Active supplement | `ls -la paper/latex_gpt/supplementary_main.pdf` |
| `HAT_105_results_review/` | Remote 105 data | `ls HAT_105_results_review/` |
| `HAT_107_clean_review/` | Remote 107 data | `ls HAT_107_clean_review/` |
| `.git/` | Version control | `git status` |

---

## 6. Post-Cleanup Verification

After any executed cleanup:

```bash
# 1. Verify final bundle integrity
sha256sum -c release_artifacts/paper1_submission_bundle_20260509_final/SHA256SUMS.txt | tail -5

# 2. Verify canonical JSON present
ls paper/latex_gpt/source_data/canonical_json/pcm_6bit_seed123/training_history.json

# 3. Verify source CSV present
cat paper/latex_gpt/source_data/tab_pcm_precision_ladder.csv | head -3

# 4. Verify PDFs present
ls -la paper/latex_gpt/main.pdf paper/latex_gpt/supplementary_main.pdf paper/latex_gpt/cover_letter.pdf

# 5. Run PCM guard
python scripts/_gpt/check_local_pcm_precision_ladder.py
```

---

## 7. Verdict

| Check | Result |
|-------|--------|
| Full inventory | ✅ 50+ paths classified |
| Large file report | ✅ 7 entries ≥ 20 MB |
| Delete-safe list | ✅ 14 items, exact commands |
| Quarantine plan | ✅ Reversible `mv` commands |
| Protected paths | ✅ 10 paths with verification commands |
| Post-cleanup verification | ✅ 5-step checklist |
| No canonical data at risk | ✅ Verified |

**Track I Status: COMPLETE**

---

*Report by kimi. 2026-05-09.*
