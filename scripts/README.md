# scripts/

## Subdirectories

| Subdir | Contents |
|:--|:--|
| `_gpt/` | GPT-coordination-era scripts (sweep / eval / build / ablation) |
| `oneshot_root/` | 40+ `run_*.py` + `plot_*.py` + `visualize_*.py` + `probe_*.py` + `diag_*.py` relocated from project root in 2026-04-25 cleanup pass-3 |

## Top-level scripts (current pipelines)

| Script | Purpose |
|:--|:--|
| `download_data.sh` | Public dataset download/staging stub; root compatibility symlink exists |
| `auto_postfix_pipeline.sh` | Post-bug-fix verification + eval pipeline |
| `run_postfix_eval.sh` | Fresh-instance eval entry |
| `run_proportional_hat_fresh_eval.sh` | Proportional HAT fresh eval |
| `run_standard_hat_fresh_eval.sh` | Standard HAT fresh eval |
| `run_codex_report.sh` | Codex weekly report assembly |
| `_ckpt_monitor.sh` | Checkpoint monitor |
| `_gpu_monitor.sh` | GPU usage monitor |
| `download_imagenet_val.py` | ImageNet val set fetcher |
| `prepare_imagenet_val.py` | ImageNet val staging |
| `monitor_training_health.py` | Training-loop health monitor |
| `debug_math_consistency.py` | Math consistency debugger |
| `experiment_nonideality_sweep.py` | Nonideality sweep |
| `proxy_sensitivity_sweep_gpt.py` | Proxy sensitivity sweep |
| `ablation_ensemble_hat_vs_iid.py` | Ensemble vs i.i.d. ablation |

## Conventions

- Pipelines: `*.sh` in `scripts/` root
- One-shot experiments: `oneshot_root/run_<topic>.py`
- Reusable analyses: `_gpt/` subdir
- Always run from project root: `python scripts/<name>.py`
