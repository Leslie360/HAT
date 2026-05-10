# BROADCAST: Codex Parallel LLM + Reference Authenticity Audit Complete

Date: 2026-04-25 22:25 CST
From: Codex
To: Claude, Kimi, Gemini, Remote

## Summary

Codex completed the user-requested parallel work: LLM GPU smoke jobs ran while `refs_gpt.bib` was audited and repaired for authenticity.

Full report: `report_md/_gpt/CODEX_PARALLEL_LLM_AND_BIB_AUDIT_20260425.md`
Validation JSON: `report_md/_gpt/refs_gpt_validation_20260425.json`

## Reference Status

- `paper/latex_gpt/refs_gpt.bib` now has 58 entries.
- All cited keys resolve: 54 cited keys, 0 missing.
- Machine authenticity validation: 0 unresolved DOI/arXiv/URL entries.
- DOI-title mismatch check: 0 low-similarity DOI/title pairs.
- `main.tex` and `supplementary_main.tex` both compile with `latexmk` RC 0.
- Remaining issue is layout-only: one long IBM URL in bibliography creates an overfull hbox.

High-risk wrong metadata corrected for keys including:
`kim2024sttmram`, `lin2024hardsea`, `lin2023vitptq`, `cui2025multimode`, `jang2023insensor`, `beller2024organicneurons`, `harikesh2024oeneurons`, `yan2025learningaware`, `roberts2022principles`, `wager2013dropout`, `kirkpatrick2017overcoming`.

## LLM Work 2 GPU Smoke

Launcher: `paper2/results/run_llm_parallel_wait_20260425_220737.sh`

Three Pythia 410M high-precision analog last-block 200-step jobs completed:

| Run | Initial | Final | Verdict |
|---|---:|---:|---|
| no noise, lr 1e-5 | 6.4882 | 6.0010 | stable positive control |
| d2d 0.05/c2c 0.02, lr 5e-6, r10 | 12.0682 | 13.8240 | unstable |
| d2d 0.10/c2c 0.05, lr 1e-6, r10 | 13.9156 | 12.5371 | weak improvement but high variance |

## Coordination Notes

- Kimi: safe to rely on the corrected bibliography metadata, but still review whether each citation is rhetorically placed correctly in prose.
- Gemini: please focus future W2 audit on staged mapping risk, not full noisy all-module conversion.
- Claude: Work 2 route should remain staged: no-noise positive control -> per-submodule noisy probes -> KV-cache-specific persistent D2D/fresh C2C split. Do not promote the noisy smoke runs as results.
- Remote: no new remote action required until W2 staged experiment matrix is finalized.
