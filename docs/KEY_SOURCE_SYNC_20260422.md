# Key Source Sync 2026-04-22

This remote branch now carries a broader local source mirror.

Included:
- top-level execution-relevant source/config files (`*.py`, `*.sh`, `*.md`, `*.txt`, `*.json`, `*.csv`, `*.yml`, `*.yaml`)
- full `scripts/`
- full `docs/`
- full `device_profiles/`
- full `远端/`
- `report_md/_gpt/` top-level markdown/json/csv/txt plus `json_gpt/` and `csv_gpt/`
- lightweight `paper/*.py`
- one approved baseline checkpoint:
  - `checkpoints/V4_hybrid_standard_noise_hat_best.pt`
  - duplicate at `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt`

Excluded intentionally:
- raw datasets
- bulky logs
- manuscript PDFs/PPTX/DOCX
- large checkpoint families beyond the single baseline
- `.git/`, caches, temp outputs

Use this branch as the remote execution mirror. Do not assume the main local worktree is available.
