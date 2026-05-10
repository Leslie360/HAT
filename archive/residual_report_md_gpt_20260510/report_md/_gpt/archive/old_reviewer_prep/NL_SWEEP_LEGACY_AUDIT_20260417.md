# Legacy NL Sweep Audit (2026-04-17)

## Purpose

Record what exists from the older `gm_e4_nl_scan` runs and explain why the new `task24` rerun is still justified.

## Historical sweep found

A prior landscape scan exists in:

- `run_nl_landscape_scan.sh`
- `logs/_gpt/gm_e4_nl_1.2.log`
- `logs/_gpt/gm_e4_nl_1.5.log`
- `logs/_gpt/gm_e4_nl_1.8.log`
- `logs/_gpt/gm_e4_nl_2.2.log`
- `logs/_gpt/gm_e4_nl_2.5.log`
- `checkpoints/gm_e4_nl_scan/nl_*/V4_hybrid_standard_noise_hat_{best,last}.pt`

These are real CUDA runs, not placeholders.

## Extracted best accuracies from historical logs

| NL | Best accuracy | Best epoch | Final behavior |
| --- | ---: | ---: | --- |
| 1.2 | 59.46% | 0 | collapses to ~10% by epoch 19 |
| 1.5 | 58.01% | 0 | collapses to ~10% by epoch 19 |
| 1.8 | 56.84% | 0 | collapses to ~10% by epoch 19 |
| 2.2 | 56.43% | 0 | collapses to ~10% by epoch 19 |
| 2.5 | 53.56% | 0 | collapses to ~10% by epoch 19 |

## Why these historical results are not sufficient as the canonical interpolation evidence

1. The historical sweep writes only to the generic `report_md/_gpt/tinyvit_results_gpt.md` sink, not to a dedicated structured JSON/CSV artifact per NL point.
2. The historical sweep predates the current closeout state of the repo and is not referenced in the current paper-facing lock files.
3. The newly launched rerun shows materially different early behavior:
   - current `task24` (`NL=1.5`) starts at `18.86%` test accuracy at epoch 0
   - historical `gm_e4_nl_1.5.log` started at `58.01%` test accuracy at epoch 0
4. Because the early trajectory differs substantially, the old sweep should be treated as legacy evidence, not as the final canonical interpolation result for the current manuscript state.

## Current canonical rerun

The active rerun is:

- script: `run_task24_tinyvit_nl15_interp_gpt.sh`
- log: `logs/_gpt/train_tinyvit_v4_nl_interp15_20260417_022400_gpt.log`
- result targets:
  - `report_md/_gpt/json_gpt/v4_nl_interp15_results_gpt.json`
  - `report_md/_gpt/csv_gpt/v4_nl_interp15_results_gpt.csv`
  - `report_md/_gpt/v4_nl_interp15_results_gpt.md`

This rerun is being executed through host WSL (`wsl.exe`) because the Codex snap-scoped shell masks CUDA visibility in-tool even though the host WSL environment sees the RTX 5070 Ti correctly.

## Working interpretation

- The old `gm_e4` sweep is useful as a historical signal that intermediate NL points were previously explored.
- It is not strong enough to serve as the final paper-facing interpolation evidence without reconciliation.
- The active `task24` rerun is the right artifact to keep tracking.
