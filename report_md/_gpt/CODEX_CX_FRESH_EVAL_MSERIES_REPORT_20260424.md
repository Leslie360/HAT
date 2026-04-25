# CODEX CX-FRESH-EVAL-MSERIES Report

- Date: 2026-04-24
- Scope: local M1-M6 fresh-instance eval consolidation plus remote parity rows provided in dispatch.
- Protocol: 10 fresh D2D instances x 5 MC eval runs per checkpoint.
- NL: explicit `NL_LTP=2.0`, `NL_LTD=-2.0`; noise mode matched checkpoint provenance.
- Commit: `33bed9cbb8ade7676d71074490ad45e68347950e`; dirty worktree: `True`.
- CUDA device: `NVIDIA GeForce RTX 5070 Ti`; PyTorch: `2.10.0+cu128`.
- CSV: `report_md/_gpt/csv_gpt/cross_host_parity_mseries.csv`
- Provenance guard: `eval_fresh_instances_postfix.py` used checkpoint metadata by default; `allow_eval_nl_override=false` and `eval_provenance_mismatches=[]` for all local M1-M6 JSONs.
- ADC scope: these M-series fresh-eval numbers use the default analog forward path (conductance quantization + D2D/C2C/NL + float output accumulation). Hook-based ADC quantization is a separate ablation, not active in this report.

## Local Fresh Eval

| Run | Config | Seed | Train Best | Fresh Mean | Fresh Std | Range | JSON |
|:--|:--|--:|--:|--:|--:|:--|:--|
| CX-M1 | V3 Standard | 123 | 82.89 | 82.0282 | 0.9416 | 79.51-82.86 | `report_md/_gpt/json_gpt/cx_m1_fresh_eval.json` |
| CX-M2 | V4 Ensemble | 123 | 80.97 | 80.4538 | 0.5835 | 79.26-81.14 | `report_md/_gpt/json_gpt/cx_m2_fresh_eval.json` |
| CX-M3 | V4 Proportional | 123 | 80.88 | 80.7132 | 0.1370 | 80.46-81.00 | `report_md/_gpt/json_gpt/cx_m3_fresh_eval.json` |
| CX-M4 | V4 Proportional | 456 | 81.39 | 80.7532 | 0.4271 | 79.94-81.26 | `report_md/_gpt/json_gpt/cx_m4_fresh_eval.json` |
| CX-M5 | V3 Standard | 456 | 80.69 | 80.4674 | 0.0936 | 80.33-80.58 | `report_md/_gpt/json_gpt/cx_m5_fresh_eval.json` |
| CX-M6 | V4 Ensemble | 456 | 81.87 | 81.1850 | 1.6847 | 78.07-82.54 | `report_md/_gpt/json_gpt/cx_m6_fresh_eval.json` |

## Aggregate Statistics

| Group | n seeds | Fresh mean | Across-seed std |
|:--|--:|--:|--:|
| Local V3 Standard | 2 | 81.2478 | 1.1037 |
| Local V4 Ensemble | 2 | 80.8194 | 0.5170 |
| Local V4 Proportional | 2 | 80.7332 | 0.0283 |
| Remote V3 Standard | 1 | 83.6400 | single-run |
| Remote V4 Proportional | 2 | 84.7950 | 0.0071 |

## Cross-Host Delta

- V3 Standard seed 123: remote R-M1 fresh `83.6400%` - local CX-M1 fresh `82.0282%` = `+1.6118 pp`.
- V4 Proportional seed 123: remote R-M2 s123 fresh `84.8000%` - local CX-M3 fresh `80.7132%` = `+4.0868 pp`.
- V4 Proportional group mean: remote known fresh `84.7950%` - local CX-M3/M4 mean `80.7332%` = `+4.0618 pp`.

Interpretation: the current remote advantage is not a uniform 1-2 pp shift. It is about +1.6 pp for the Standard seed-123 comparison but about +4.1 pp for the known Proportional comparison. This is confounded by host recipe and batch size (local batch 64 vs remote batch 512), so the parity table should be cited as cross-host evidence, not as a clean causal estimate of batch-size effect.

## Anomalies / Caveats

- No checkpoint-corruption signature: every local fresh mean is close to its train-best source accuracy.
- CX-M6 has the widest local fresh spread (`std=1.6847%`, range `78.07-82.54`), so Ensemble-uniform seed 456 should be displayed with an error bar rather than as a single headline number.
- The worktree is dirty because multiple agents are writing coordination artifacts and code patches; commit hash is still `33bed9c`, the required post-fix base.
- Remote rows with `TBD` fresh values are placeholders from the dispatch and must not be cited as measured fresh performance.

## Verdict

CX-FRESH-EVAL-MSERIES is complete for local M1-M6. The paper-safe statement is: true-NL2 local fresh performance sits in the ~80-82% band across Standard, Ensemble-uniform, and Ensemble-proportional routes; the old 90.88% proportional claim remains invalid.
