# Kimi P8 Track C: Cleanup Execution or Dry Run

Date: 2026-05-09
Scope: `/home/qiaosir/projects/compute_vit`
Status: COMPLETE — safe cleanup executed; uncertain files quarantined, not deleted

## 1. Inputs

Primary input: `report_md/_gpt/KIMI_P7_TRACK_I_WORKSPACE_CLEANUP_AND_QUARANTINE_PLAN_20260509.md`.

Rules followed:

- Protected paths were not moved or deleted.
- Build/cache residues were deleted only when objectively disposable.
- Uncertain files were moved into `archive/cleanup_candidates_20260509/` by `mv`.
- The Chinese PPT unknown item was not deleted or moved; it remains a user-decision item.

## 2. Commands/logs executed

| Step | Log |
|---|---|
| Initial safe cleanup | `logs/p8_cleanup_20260509_221101.log` |
| Quarantine retry / correction | `logs/p8_cleanup_quarantine_retry_20260509_222746.log` |
| LaTeX rebuild after cleanup/text | `logs/p8_latex_rebuild_after_final_text_20260509_222917.log` |
| Final bundle refresh/SHA check | `logs/p8_trackE_final_bundle_refresh_20260509_223000.log` |
| PCM guard | `logs/p8_pcm_guard_20260509_223000.log` |

## 3. Deleted safe residues

| Category | Action |
|---|---|
| Python bytecode | Removed `__pycache__` directories found under project paths |
| LaTeX residues | Removed selected temporary `.fls`, `.fdb_latexmk`, `.log` and temp-render residues under active LaTeX tree only when covered by cleanup plan |
| Temporary artifacts | Removed/moved obvious one-off artifacts such as `paper/latex_gpt/1`, `BROADCAST_EOF`, `temp_render.tex`, and test PDFs |
| `.pytest_cache` / `tmp` | Removed disposable cache/temp contents where present |

## 4. Quarantine inventory

Quarantine root: `archive/cleanup_candidates_20260509/`

| Subdirectory | Contents |
|---|---|
| `old_remote_files/` | top-level old intercom/tasklist files, old GPU schedule, old `gpu_watcher.sh`, old `paper2/REMOTE_*.md` |
| `old_drafts/` | `paper/latex_gpt/deprecated/`, `paper/latex_gpt/figures/deprecated_20260424/` |
| `test_renderings/` | temporary supplement part PDFs, merged test PDFs, `figS*_test.pdf`, `CLEAN_DRAFT_V3_FIXED.pdf`, `cover_letter_v6.tex.pdf`, temp artifacts |
| `chatgpt_images/` | four ChatGPT image PNG files from `paper/latex_gpt/` |
| `bundle_strays/` | self-audit repair item: `06_discussion.tex.bak_20260425` removed from final bundle |

Post-quarantine count: 44 files under quarantine.

## 5. Protected paths verified untouched

| Path | Status |
|---|---|
| `release_artifacts/paper1_submission_bundle_20260509_final/` | Preserved; refreshed only by Track E |
| `release_artifacts/paper1_submission_bundle_20260509_final.tar.gz` | Preserved/refreshed; SHA verified |
| `release_artifacts/paper1_provenance_archive_20260509/` | Not moved |
| `paper/latex_gpt/source_data/canonical_json/` active canonical data | Not deleted |
| `paper/latex_gpt/source_data/*.csv` | Not deleted |
| `paper/latex_gpt/main.pdf`, `supplementary_main.pdf`, `cover_letter.pdf` | Rebuilt/refreshed, not deleted |
| `/home/qiaosir/projects/remote_reviews/105/` | Not touched |
| `/home/qiaosir/projects/remote_reviews/107/` | Not touched |
| `.git/`, `.claude/` | Not touched |

## 6. Restore commands

```bash
# Restore old remote files
mv archive/cleanup_candidates_20260509/old_remote_files/* .

# Restore old LaTeX drafts
mv archive/cleanup_candidates_20260509/old_drafts/deprecated paper/latex_gpt/
mv archive/cleanup_candidates_20260509/old_drafts/deprecated_20260424 paper/latex_gpt/figures/

# Restore test renderings
mv archive/cleanup_candidates_20260509/test_renderings/* paper/latex_gpt/

# Restore ChatGPT images
mv archive/cleanup_candidates_20260509/chatgpt_images/* paper/latex_gpt/
```

If only one item is needed, restore that single path rather than using the wildcard command.

## 7. Post-cleanup verification

| Check | Result |
|---|---|
| Final bundle SHA cold-unpack | PASS, 133/133 OK in `logs/p8_self_audit_bundle_repair_20260509_224103.log` |
| PCM guard | PASS in `logs/p8_pcm_guard_20260509_223000.log` |
| Stale-value grep | PASS after excluding explicitly deprecated old-protocol archive |
| LaTeX compile | PASS; only underfull hbox warnings, no fatal errors |

## 8. User-decision item

`report_md/记忆类型可调的光电突触和存储器用于储备池计算-第8稿(1).pptx` remains in place. Do not delete until user confirms whether it is thesis/proposal material.

## 9. Verdict

Track C COMPLETE. Cleanup was executed conservatively and is reversible for all uncertain items.
