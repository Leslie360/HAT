# Paper2 / 107: Analog KV-Cache for Decoder-Only LLMs

This directory is the active Work-2 / Paper2 workspace. It is intentionally separate from the Paper1 manuscript and release evidence.

## Current scope

- 107 selective KV-cache is the canonical Paper2 direction.
- Work-2 experiments include analog KV-cache infrastructure, attention/KV-cache path tests, and Standard HAT vs Ensemble HAT style comparisons.
- AIHWKit/PCM baseline work currently lives in sibling `../paper2_aihwkit_baseline/`.

## Active structure

| Path | Purpose |
|:--|:--|
| `src/` | Work-2 implementation code, including analog KV-cache and LLM hybrid scripts. |
| `manuscript/snippets/` | Paper2 manuscript snippets, including `r10e_tex_paragraph.tex`. |
| `results/` | Local Work-2 outputs, driver scripts, PID/exit records, and JSON/TSV summaries. Current `W2_SCOPED_PROBE_SUMMARY_20260425.tsv` is a legacy smoke/probe index, not claim-bearing Paper2 evidence. |
| `sections/` | Draft Paper2 section material. |
| `supplementary/` | Draft supplementary material. |
| `WORK2_TESTBED_DECISION_20260425.md` | Testbed decision snapshot. |
| `WORK2_ARCHITECTURAL_MAPPING_SPEC_20260425.md` | Architecture mapping notes. |
| `WORK2_BENCHMARK_SUITE_20260425.md` | Benchmark suite notes. |

## 107 task/result entrypoints

- Remote 107 tasklist: `../coordination/remote_tasks/107/REMOTE_107_PHASE_P8_CORRECTED_NOISE_WORK2_TASKLIST_20260509.md`
- Paper2 / AIHWKit baseline area: `../paper2_aihwkit_baseline/`
- R10E snippet compatibility path: `../paper2_aihwkit_baseline/r10e_tex_paragraph.tex` -> `../paper2/manuscript/snippets/r10e_tex_paragraph.tex`
- Ideal future lane: `paper2_107/` per `../coordination/active/COMPUTE_VIT_IDEAL_LAYOUT_PLAN_20260510.md`

## 107 evidence status

Current repository-local Paper2 evidence is sufficient for infrastructure provenance but not for manuscript claims:

- `results/w2_scoped_probe_summary_20260425.json` and `results/W2_SCOPED_PROBE_SUMMARY_20260425.tsv` summarize earlier scoped smoke/probe runs.
- These rows use small smoke text batches and archived source logs; they are useful for debugging trends, not for final Paper2 PPL claims.
- `../coordination/remote_tasks/107/REMOTE_107_PHASE_P8_CORRECTED_NOISE_REPORT_20260510.md` and `results/FRESH_D2D_SUMMARY_107_20260510.tsv` are strict-review candidate indexes, not locked claim-bearing evidence.
- `results/fig_107_*.png` and `results/fig_107_*.pdf` are draft audit visualizations generated from the candidate index; they are visual QA aids only, not manuscript figures.
- The 2026-05-10 strict review rejected the earlier claim-lock wording because the first aggregation mixed distinct checkpoints/conditions and the raw JSON lacks required commit, command, config, dataset, evaluation-protocol, and checkpoint-hash metadata.
- Required claim-bearing tables remain: corrected-noise summary with complete metadata, fresh-D2D summary, old-vs-corrected comparison, and metadata completeness; current `results/METADATA_COMPLETENESS_107_20260510.tsv` is a failure inventory showing what is missing, not a pass certificate.

## Provenance

- 107/Paper2 provenance map: `PROVENANCE_107_20260510.tsv`

## Rules

- Keep Paper2/107 evidence separate from Paper1 release/source-data paths.
- Mark invalid, contaminated, or superseded runs visibly; do not silently delete them.
- Large checkpoints/data should stay local-first and indexed before migration.
- Promote only audited results into future Paper2 source-data packages.
