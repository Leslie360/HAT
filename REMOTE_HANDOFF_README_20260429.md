# Remote Handoff Clean Branch — 2026-04-29

This branch is a curated remote-execution tree for external servers. It intentionally does not mirror the full local working directory.

## Roles

- Remote 105: multi-dataset validation lane. Keep results separate from KV-cache work.
- Remote 107: Work-2 analog KV-cache exploration lane. Start from `paper2/REMOTE_107_KV_TASKLIST_20260429.md`.

## Clone

```bash
git clone -b remote-107-kv-20260429 git@github.com:Leslie360/HAT.git HAT_kv107
cd HAT_kv107
```

HTTPS fallback:

```bash
git clone -b remote-107-kv-20260429 https://github.com/Leslie360/HAT.git HAT_kv107
cd HAT_kv107
```

## Included

- Core HAT analog/TinyViT source needed for local reproduction and code audit.
- Work-2 KV-cache source, tests, benchmark specs, and Remote 107 task list.
- R11D AIHWKit/PCM baseline scripts required for audit/reproduction.
- Current Codex review, audit, and direction documents.

## Excluded By Design

- Checkpoints and model weights.
- Training logs, PID/exit files, and generated JSON output dumps unless explicitly selected.
- LaTeX build artifacts, generated PDFs, and temporary paper edits.
- Historical `_archive/` material and BFG reports.
- Local caches: `__pycache__`, `.pytest_cache`, `.ruff_cache`, data directories.

## Return Protocol

Remote agents should return compact Markdown summaries plus small JSON summaries. Do not send large checkpoints back unless explicitly requested.
