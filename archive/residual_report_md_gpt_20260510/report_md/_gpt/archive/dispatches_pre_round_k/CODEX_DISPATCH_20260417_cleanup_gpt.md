# Codex Dispatch #7 — File Management & Cleanup

**Date:** 2026-04-17
**From:** Claude (coordinator)
**To:** Codex (executor)
**Scope:** Archival / cleanup only. **No code changes, no LaTeX content changes, no deletions of data or checkpoints.**
**Goal:** Reduce surface noise at project root and `compute_vit/` top level before submission freeze, so the reviewer-accessible archive is easy to navigate.

---

## Inventory summary (read-only audit done by Claude)

- `/home/qiaosir/projects/` root: has stray LaTeX build artifacts (`cover_letter.{aux,fdb_latexmk,fls,log,out,pdf}`, `main.{aux,fdb_latexmk,fls,log,out}`) from an earlier accidental compile outside `paper/latex_gpt/`. The canonical PDFs already live under `paper/latex_gpt/`.
- Garbage/zero-byte files at project root: `tunnel`, `•`, `proxy_sensitivity_sweep_gpt.py` (0 bytes). The non-empty `proxy_sensitivity_sweep_gpt.py` we actually use lives at `compute_vit/proxy_sensitivity_sweep_gpt.py`.
- `/home/qiaosir/projects/home/` — 24 KB accidental subtree. Please inspect before moving; do not delete blindly.
- `compute_vit/` top level: ≥35 one-shot helper scripts (`append_*.py`, `check_resnet_*.py`, `debug_*.py`, `diagnose_*.py`, `watch_*.py`, plus a few `experiment_asymmetry_*.py` / `experiment_nonideality_*.py`). These are session-specific glue, not part of the reproducibility path.
- `paper/latex_gpt/`: two stale compile artifacts `pdflatex51394.fls`, `pdflatex52112.fls`.
- `.gitignore` at project root is minimal (only `back_ISP/`, `.claude/`, `__pycache__/`, `checkpoints/`, `.aider*`). LaTeX build products are not ignored.

---

## TX-17 — Move stray LaTeX build artifacts out of project root

**Do:**
1. Create `/home/qiaosir/projects/tmp/stale_latex_root_20260417/`.
2. Move these files into it (preserve names):
   - `/home/qiaosir/projects/cover_letter.aux`
   - `/home/qiaosir/projects/cover_letter.fdb_latexmk`
   - `/home/qiaosir/projects/cover_letter.fls`
   - `/home/qiaosir/projects/cover_letter.log`
   - `/home/qiaosir/projects/cover_letter.out`
   - `/home/qiaosir/projects/cover_letter.pdf`
   - `/home/qiaosir/projects/main.aux`
   - `/home/qiaosir/projects/main.fdb_latexmk`
   - `/home/qiaosir/projects/main.fls`
   - `/home/qiaosir/projects/main.log`
   - `/home/qiaosir/projects/main.out`
3. Confirm the canonical pair `paper/latex_gpt/main.pdf` and `paper/latex_gpt/cover_letter.pdf` still exist and compile dates are recent (no action needed; just verify).

**Don't:** Do **not** touch anything inside `paper/latex_gpt/*.pdf`, `*.bbl`, `*.aux` — those are the live build products.

---

## TX-18 — Remove empty/garbage root-level files

**Inspect first, then move** to `/home/qiaosir/projects/tmp/garbage_root_20260417/`:
- `/home/qiaosir/projects/tunnel` (0 bytes)
- `/home/qiaosir/projects/•` (0 bytes, non-ASCII filename — use quoted path)
- `/home/qiaosir/projects/proxy_sensitivity_sweep_gpt.py` **only if `wc -c` is 0**. The real version at `compute_vit/proxy_sensitivity_sweep_gpt.py` must stay untouched. If the root copy is non-zero, STOP and report.

---

## TX-19 — Inspect `/home/qiaosir/projects/home/`

- `du -sh` + `ls -R` the directory.
- If it is clearly accidental (e.g. contains a stray WSL home scaffold), move to `/home/qiaosir/projects/tmp/unknown_home_subtree_20260417/` without deleting.
- If it contains anything that looks authored (real `.py`, `.md`, notes), STOP and report in the closeout with the file list — do NOT move.

---

## TX-20 — Archive one-shot scripts under `compute_vit/`

Create `/home/qiaosir/projects/compute_vit/scripts/archive_20260417/` and move these **by name prefix** (do `git mv` if tracked, plain `mv` otherwise):

- `append_*.py` (10 files: `append_batch3.py`, `append_kimi_km14.py`, `append_kimi_km14_part2.py`, `append_kimi_km14_v2.py`, `append_kimi_part2.py`, `append_sync.py`, `append_sync_batch4.py`, `append_sync_final.py`, `append_sync_k5.py`, `append_sync_kimi.py`)
- `check_resnet_keys.py`, `check_resnet_weights.py`
- `debug_*.py` (all 5: `debug_ensemble_deep.py`, `debug_nl_baseline.py`, `debug_resnet18_load.py`, `debug_resnet_issue.py`, `debug_train_eval_mismatch.py`)
- `diagnose_*.py` (all 7)
- `watch_*.py` (all 4)
- `experiment_asymmetry_*.py` (4 files) and `experiment_nonideality_gemini.py`

**Do NOT move** (these are part of the reproducibility path):
- Any `run_*.py` (locked experiment drivers)
- `analog_layers*.py`, `amp_utils.py`, `device_profile_utils.py`, `inference_analysis_utils.py`, `model_profiling.py`, `physical_noise_pipeline.py`
- Any `eval_*.py` that is NOT `eval_resnet18_checkpoints.py`
- `eval_resnet18_checkpoints.py` — **keep**, referenced by the ResNet restore-weight-scale fix audit
- `ablation_*.py`, `generate_*.py`, `make_appendix.py`, `port_05.py`, `probe_resnet_ckpts.py`, `proxy_sensitivity_sweep_gpt.py`, `report_asset_paths.py`, `patch_fig11.py`, `fix_plots.py`, `download_imagenet_val.py`, `prepare_imagenet_val.py`

If you are unsure about any file, STOP and list it in the closeout instead of moving.

---

## TX-21 — Sweep stale LaTeX artifacts inside `paper/latex_gpt/`

Move to `/home/qiaosir/projects/tmp/stale_latex_paper_20260417/`:
- `paper/latex_gpt/pdflatex51394.fls`
- `paper/latex_gpt/pdflatex52112.fls`

**Do NOT** remove `*.aux`, `*.bbl`, `*.fdb_latexmk`, `*.fls`, `*.log`, `*.out`, `*.synctex.gz`, or `*.pdf` that belong to `main`, `cover_letter`, or `supplementary_main`. Those are the live rebuild state.

---

## TX-22 — Expand `.gitignore` at project root

Append (do not delete existing entries) these patterns to `/home/qiaosir/projects/.gitignore`:

```
# LaTeX build products (keep .tex, .bib, figures, and final .pdf under paper/latex_gpt/ intentionally tracked)
*.aux
*.bbl
*.blg
*.fdb_latexmk
*.fls
*.log
*.out
*.synctex.gz
pdflatex*.fls

# Python cache / stale
*.pyc
.ipynb_checkpoints/

# Local scratch
tmp/
logs/
```

Verify that `paper/latex_gpt/main.pdf`, `paper/latex_gpt/cover_letter.pdf`, `paper/latex_gpt/supplementary_main.pdf`, and `paper/latex_gpt/*.tex` remain tracked (`git ls-files paper/latex_gpt/ | head`). If the new rules would un-track them, adjust with explicit `!paper/latex_gpt/*.pdf` unignore lines and re-verify.

---

## TX-23 — Closeout manifest

Write `/home/qiaosir/projects/compute_vit/report_md/_gpt/CLEANUP_MANIFEST_20260417.md` containing:
1. A table per TX-17…TX-22 with: source path → destination path → size → reason.
2. Any item you chose NOT to move and why (especially TX-19 `home/` contents and any ambiguous `compute_vit/*.py`).
3. Final `git status` short output showing only the expected moves/renames.
4. Confirmation lines:
   - `paper/latex_gpt/main.pdf` still exists and is 16 pages.
   - `paper/latex_gpt/cover_letter.pdf` still exists.
   - `paper/latex_gpt/supplementary_main.pdf` still exists and is 15 pages.
   - `compute_vit/run_*.py` count unchanged before/after.

Do **not** commit. The user will review the manifest and decide whether to commit.

---

## Hard constraints

- **No deletions.** Everything goes to `tmp/` subfolders or `scripts/archive_20260417/`. Recovery must be a single `mv`.
- **No content edits** to `.tex`, `.md`, `.py`, `.bib`, `.json`, or figure files. This dispatch is filesystem hygiene only.
- **No touching `checkpoints/`** (24 GB) — separate future dispatch if/when needed.
- **No `git commit`, no `git push`.** Staging via `git mv` is fine; leave the staging for the user to review.
- If any step fails or surfaces an ambiguity, STOP that TX, record it in the manifest's "NOT moved" section, and continue with the next independent TX.

---

## Reporting

When done, update `CLAUDE_TASK_gpt.md` TX-17 → TX-23 rows to `DONE` or `BLOCKED (see manifest §X)`, and append a single block to `AGENT_SYNC_gpt.md` summarizing scope + manifest path.
