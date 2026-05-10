# BROADCAST — Dispatch #7 Cleanup Complete (2026-04-17)

**From:** Claude
**To:** Codex (primary executor), future agents touching this repo
**Status:** ✅ Committed — `d3f5c54` on `master`

---

## Summary

All seven TX items from `CODEX_DISPATCH_20260417_cleanup_gpt.md` are landed. The working tree is structurally clean and reversible.

| TX | Outcome |
|:--|:--|
| TX-17 | 11 stray root `cover_letter.*` / `main.*` LaTeX artifacts → `tmp/stale_latex_root_20260417/` |
| TX-18 | 3 zero-byte garbage files → `tmp/garbage_root_20260417/` |
| TX-19 | Kimi KM1–KM7 proofreading report rescued to `report_md/_gpt/KIMI_KM1_KM7_REPORTS.md`; empty mirror tree → `tmp/unknown_home_subtree_20260417/` (resolved by Claude after user decision, option A) |
| TX-20 | 33 one-shot helper scripts (`append_*`, `check_resnet_*`, `debug_*`, `diagnose_*`, `watch_*`, `experiment_asymmetry_*`, `experiment_nonideality_gemini.py`) → `scripts/archive_20260417/` |
| TX-21 | 2 stale `pdflatex*.fls` → `tmp/stale_latex_paper_20260417/` |
| TX-22 | Outer-root `.gitignore` expanded with LaTeX / pyc / tmp / logs patterns (no un-tracking of live PDFs) |
| TX-23 | `CLEANUP_MANIFEST_20260417.md` written with per-TX src→dst table and post-check confirmations |

---

## Invariants preserved

- `compute_vit/run_*.py` count: **44 → 44** (experiment driver whitelist intact)
- `paper/latex_gpt/main.pdf` — 16 pages, present
- `paper/latex_gpt/cover_letter.pdf` — 2 pages, present
- `paper/latex_gpt/supplementary_main.pdf` — **16 pages**, present
  - Note: supp was 15pp at TX-13 and is 16pp after the External Review Follow-Up wording pass. User accepted this; no trim required.
- `checkpoints/` (24 GB) untouched.
- No `.tex`, `.md`, `.py`, `.bib`, `.json`, or figure content was edited.
- All moves reversible via a single `mv`.

---

## Where things live now

- Reversible archive: `/home/qiaosir/projects/tmp/{stale_latex_root,garbage_root,stale_latex_paper,unknown_home_subtree}_20260417/`
- One-shot helpers: `compute_vit/scripts/archive_20260417/` (tracked in git — safe to prune later)
- Canonical coordination:
  - Dispatch brief: `report_md/_gpt/CODEX_DISPATCH_20260417_cleanup_gpt.md`
  - Manifest: `report_md/_gpt/CLEANUP_MANIFEST_20260417.md`
  - Rescued Kimi report: `report_md/_gpt/KIMI_KM1_KM7_REPORTS.md`

---

## Standing guidance for future sessions

1. **New one-shot scripts** (`debug_*`, `diagnose_*`, `watch_*`, `append_*`) — place them under `compute_vit/scripts/` from day one, not at the `compute_vit/` top level.
2. **LaTeX compiles** must happen inside `paper/latex_gpt/`. Do not invoke tectonic/pdflatex from the project root — it will strew `.aux`/`.fls`/`.log` at the wrong level again.
3. `tmp/`, `logs/`, and `__pycache__/` are ignored across both repos. Treat them as disposable; never put authored content there.
4. If you encounter another stray `home/qiaosir/...` WSL-mirror path, inspect before moving — a real authored file may be hiding deep inside.

---

## Commit reference

```
d3f5c54 cleanup: archive one-shot scripts and prune stale LaTeX/pycache artifacts
```

Scope: 101 files changed, 16,723 insertions / 2,082 deletions. No content edits outside coordination markdown + this manifest.

---

## Submission-readiness state (informational)

The NC submission package (`main.pdf` 16pp, `supplementary_main.pdf` 16pp, `cover_letter.pdf` 2pp) remains internally consistent with all locked numbers (86.37±1.54 Ensemble HAT, 27.72±0.82 NL=2.0, 88.53 OPECT, S_ADC=0.976, S_D2D=0.922, 81.63/67.20 CrossSim). No further cleanup tasks are queued. Next action is user-driven (submission or further revision).
