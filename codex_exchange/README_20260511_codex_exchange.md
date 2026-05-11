# Codex Exchange Package — 2026-05-11

This package is for local Codex review/editing of manuscript text, figures, plotting scripts, and validated source data from `compute_vit`.

## Archive

- Archive: `20260511_codex_exchange.tar.gz`
- Verify with: `sha256sum -c 20260511_codex_exchange.tar.gz.sha256`
- Unpack with: `tar -xzf 20260511_codex_exchange.tar.gz`

## Included scope

- Paper1 manuscript/release LaTeX, figures, and current reports.
- Paper2 manuscript draft/snippets, figures, plotting scripts, source data, and result TSV/JSON artifacts.
- Thesis CN/XJTU LaTeX lanes, figures, and current result tables.
- Plotting/evaluation scripts needed to regenerate the included figure/data artifacts.
- `report_md/_gpt` evidence reports, especially the canonical evidence ledger.
- Internal `MANIFEST_FILES.txt` and `SHA256SUMS.txt` inside the archive.

## Excluded scope

- Checkpoints and model weights (`checkpoints/`, `*.pt`, `*.pth`, `*.ckpt`).
- Raw datasets (`data/`).
- Files explicitly marked invalid, including `*INVALID_DO_NOT_USE*`.
- Existing large archive bundles and nested template `.git` internals.
- LaTeX auxiliary/build logs unless they are final PDFs/images useful for visual review.

## Evidence boundaries for Codex

- Paper2 claim-bearing selective-KV evidence must come from `paper2/manuscript/source_data/remote107_selective_kv_claim_lock_20260511/` and `paper2/results/REMOTE107_SELECTIVE_KV_LOCK_SUMMARY_20260511.tsv`.
- Paper2 local KV probes, offline reconstruction, refresh scans, and local cache-path checks are engineering/provisional only; do not pool them with Remote107 claim-lock rows.
- CIFAR-100 Ensemble HAT seed456/seed789 results are provisional multi-seed expansion evidence; mention cross-seed variance and do not report a closed canonical mean unless a final seed protocol is later locked.
- Spatial variance / floorplan-aware mapping results are synthetic stress evidence only, not measured floorplan evidence.
- Retention × protection results are simulator-default retention evidence only, not measured retention, refresh, energy, or endurance closure.
- Invalid data are intentionally excluded from the archive; if referenced, cite only the ledger note that marks them invalid.

## Branch workflow

The intended GitHub branch is `codex-exchange-20260511`. Use this branch as a handoff/exchange lane for local Codex edits. Prefer editing unpacked source files locally, then committing reviewable changes back to the branch rather than modifying binary PDFs directly unless the output is the artifact under review.
