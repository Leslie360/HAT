# Context Compact — 2026-05-07

Use this file to restart the project context in a new conversation. It intentionally omits long historical debate and keeps only locked state, current risks, and next actions.

## 0. Repo / Branch Handling

- Local working repo: `/home/qiaosir/projects/compute_vit`
- Main active local branch: `paper1-release-20260501`
- Local worktree is very dirty due to Paper-1 figure/text edits, thesis files, Kimi/Gemini work, and report artifacts.
- Do **not** run `git pull`, merge, reset, or checkout in the dirty worktree without explicit intent.
- Remote branches of interest:
  - `origin/105-remote-results` at `ccf1cf7` — Remote105 TinyImageNet cross-architecture validation.
  - `origin/107-clean` at `e9e7936` — Remote107 K107 analog KV-cache package.
- A clean review worktree for 107 exists at `/home/qiaosir/projects/HAT_107_clean_review`.

## 1. Current Global Direction

There are two main papers/directions:

1. **Paper-1 / analog vision / PCM precision-retention frontier**
   - Main claim: Ensemble HAT solves algorithmic cross-instance robustness; PCM physical precision-retention then selects deployable bit point.
   - Current locked narrative: **6-bit PCM is the observed Pareto midpoint**, not “real PCM 4-bit rescue”.
   - IdealDevice 4-bit rescue (`86.16%`) is only an algorithmic/pure-quantization ablation.
   - Real PCM 4-bit is trainable but drift-limited and violates the 1 pp deployment-drift SLA.

2. **Paper-2 / K107 LLM analog KV-cache**
   - Main claim: selective terminal-layer analog KV is viable and improves with model scale.
   - K107 is separate/companion direction. Do not mix K107 PPL results into Paper-1.

## 2. Paper-1 Manuscript State

Codex applied Kimi hostile-review fixes:

- Title/abstract/introduction/results/conclusion pivoted from “4-bit rescue” to “precision-retention frontier”.
- Fixed-mask HAT is framed as a standard literature protocol pushed to failure, not a fabricated strawman.
- Added 1 pp deployment-drift SLA language for 4-bit PCM drift cliff.
- SI figure counter issue fixed structurally:
  - `fig:supp-asymmetry-concept` = S1
  - `fig:supp-nonideality` = S2
  - weight mapping = S3
  - system architecture = S4
- Recompiled PDFs:
  - `/home/qiaosir/projects/compute_vit/paper/latex_gpt/main.pdf` — 13 pages
  - `/home/qiaosir/projects/compute_vit/paper/latex_gpt/supplementary_main.pdf` — 41 pages
- Critical LaTeX grep was clean after fix: no fatal errors, undefined refs/citations, or overfull hboxes.

Important files touched:

- `paper/latex_gpt/main.tex`
- `paper/latex_gpt/supplementary_main.tex`
- `paper/latex_gpt/supplementary.tex`
- `paper/latex_gpt/sections/00_abstract.tex`
- `paper/latex_gpt/sections/01_introduction.tex`
- `paper/latex_gpt/sections/05_results.tex`
- `paper/latex_gpt/sections/07_conclusion.tex`
- `paper/latex_gpt/supplementary/S_mechanism_empirical.tex`

## 3. Remote105 Latest State — TinyImageNet Cross-Architecture

Branch: `origin/105-remote-results`
Latest commit: `ccf1cf7`
Key return: `docs/handoff/20260508_full_return.md`

Environment:

- Python 3.11.15
- PyTorch 2.4.1+cu121
- CUDA 12.1
- timm 1.0.26
- GPU: 8x NVIDIA PH402 SKU 200
- Dataset: TinyImageNet-200

Canonical Remote105 table, fresh accuracy:

| Arch | Method | seed123 | seed456 | seed789 | Mean signal |
|---|---:|---:|---:|---:|---|
| DeiT digital | digital | 48.22 | 53.61 | 53.58 | baseline |
| DeiT proportional | prop | 50.20 | 54.19 | 56.33 | +1.77 pp vs digital |
| ViT digital | digital | 48.83 | 54.58 | 50.86 | baseline |
| ViT proportional | prop | 49.00 | 53.90 | 55.41 | +1.35 pp vs digital |

Remote105 conclusions:

- DeiT proportional beats digital in all 3 seeds: +1.98, +0.58, +2.75 pp fresh.
- ViT proportional beats digital in 2/3 seeds; seed456 digital is a high outlier.
- Treat proportional HAT as **provisional-cross-architecture**, not DeiT-only.
- Proportional fresh degradation is tiny: max about -0.44 pp.
- Standard mode remains negative control: ~-30 to -34 pp collapse.
- Ensemble is partial recovery, not the main route.

Remote105 useful files:

- `docs/handoff/20260508_full_return.md`
- `results/summary/remote105_tinyimagenet_seed789_summary.csv`
- `results/summary/remote105_tinyimagenet_all_available_summary.csv`

## 4. Remote107 Latest State — K107 Analog KV-Cache

Branch: `origin/107-clean`
Latest commit after task completion: `e9e7936`
Review worktree: `/home/qiaosir/projects/HAT_107_clean_review`

Key files:

- `coordination/REMOTE107_K107_CANONICAL_FREEZE_20260508.md`
- `coordination/REMOTE107_P1_FIGDATA_RETURN_20260508.md`
- `coordination/REMOTE107_SELECTIVE_OPTIMIZER_AUDIT_20260508.md`
- `coordination/REMOTE107_P3_6P9B_FEASIBILITY_20260508.md`
- `deliverable/results_v3/k107_plot_ready.json`
- `deliverable/results_v3/k107_canonical_summary.csv`
- `deliverable/figures/k107_ablation_ladder.pdf/png`
- `deliverable/figures/k107_epsc_stress.pdf/png`
- `deliverable/figures/k107_scale_trend.pdf/png`

### 4.1 K107 Baseline Discipline

Canonical evaluator:

- Model: `EleutherAI/pythia-410m-deduped`
- Dataset: WikiText-2 raw test split
- Context length: 512
- Stride: 256
- Batch size: 1
- Raw digital baseline: **22.1849 PPL**

Deprecated baseline:

- Old/vectorized evaluator used `ctx=1024`, `stride=512`, `batch=8`
- It produced ~15.62/15.68 PPL
- Do **not** mix this value into K107 canonical comparisons.

### 4.2 K107 Paired Ablation

| Step | Meaning | PPL |
|---|---|---:|
| Raw digital baseline | no HAT, no patch | 22.185 |
| B1 | HAT checkpoint, digital/no patch | 19.043 |
| B2 | patch/no noise | 19.060 |
| B3 | D2D=0.02 | 19.483 |
| B4 | D2D=0.05 | 19.644 |

Interpretation:

- Canonical HAT fine-tuning gain is `22.18 -> 19.04`, about **3.14 PPL**.
- Analog patch overhead with no noise is negligible: about +0.017 PPL.
- D2D=0.02 overhead over patch/no-noise is about +0.42 PPL.
- D2D=0.05 overhead is about +0.58 PPL.

### 4.3 K107 Layer Scope

| Scope | D2D=0.02 | D2D=0.04 | D2D=0.05 |
|---|---:|---:|---:|
| last1 | 19.451 ± 0.065 | 19.577 ± 0.063 | 19.621 ± 0.064 |
| last2 | 20.142 ± 0.052 | 20.468 ± 0.051 | 20.586 ± 0.054 |
| all | 37.132 ± 0.878 | 68.478 ± 4.332 | 104.289 ± 8.928 |

Conclusion: terminal-layer-only analog KV is the viable route; all-layer analog KV is catastrophic.

### 4.4 K107 EPSC Proxy Stress

| Config | C2C | D2D | Mean PPL | Max PPL | Verdict |
|---|---:|---:|---:|---:|---|
| e1 | 0.05 | 0.05 | 19.718 | 19.814 | pass |
| e2 | 0.10 | 0.10 | 20.116 | 20.231 | pass |
| e3 | 0.15 | 0.15 | 20.762 | 20.869 | pass |
| e4 | 0.00 | 0.20 | 20.604 | 20.754 | pass |
| e5 | 0.01 | 0.10 | 19.861 | 19.974 | pass |

Kill line: 25 PPL. All pass.

### 4.5 K107 Scale Trend

| Model | D2D=0.02 | D2D=0.05 | Interpretation |
|---|---:|---:|---|
| Pythia-410M | 19.48 | 19.64 | canonical small scale |
| Pythia-1B | 14.60 | 14.82 | strong improvement |
| Pythia-2.8B | 13.34 | 13.44 | best, stable |

Conclusion: analog KV viability improves monotonically with model scale in tested Pythia family.

Pythia-2.8B extra stress:

- C2C=0.10 at D2D=0.02 adds only +0.255 PPL.
- EPSC 0.15/0.15 gives 13.912 PPL, still far below 25 kill line.

### 4.6 Selective Optimizer Audit

- 2.8B used selective optimizer: only target `GPTNeoXAttention` layer parameters are in AdamW.
- Non-target parameters were **not** frozen; they remain `requires_grad=True`, so gradients are still computed, but optimizer state is only for target attention layer.
- Trainable attention parameter ratio:
  - 410M: 4.20M / 405.33M, about 1.04%
  - 1B: 16.79M / 1.01B, about 1.66%
  - 2.8B: 26.22M / 2.78B, about 0.94%
- Current results are valid; no rerun required.
- Future improvement: add `--freeze-non-target-params` to reduce gradient memory.

### 4.7 6.9B Feasibility

- 6.9B is blocked on current 32GB GPU setup under fp32 single-GPU script.
- Estimated memory: ~58GB with current selective optimizer because all gradients still computed.
- Even with freezing, fp32 is ~30-32GB with no headroom.
- Recommendation: skip 6.9B for now; 410M -> 1B -> 2.8B monotonic trend is already strong.
- If 6.9B becomes necessary, add FP16/BF16 + gradient checkpointing or use larger/multi-GPU model parallel setup.

## 5. Current Local/Kimi/Gemini Coordination

### Kimi

Current task queue from Codex:

- Inventory local PCM frontier artifacts: 4/5/6/8-bit, seeds, source/fresh/drift, checkpoint/log/provenance.
- Close missing 5-bit PCM cells only if they can affect the “6-bit Pareto midpoint” claim.
- Re-eval canonical 4/6/8-bit only if provenance is weak.
- Optional IdealDevice 4-bit smoke only if GPU remains idle.
- Avoid flooding single local RTX 5070 Ti; max 1 training job plus optional lightweight eval.

### Gemini

- User and Gemini are polishing Paper-1 main/appendix figures.
- Gemini fixed SI TikZ layout; Codex fixed counter order and compile.
- Gemini should not change scientific numbers unless pulling from locked data tables.

### Codex

- Acts as architect/coordinator.
- Must protect dirty local worktree.
- Should write concise dispatches/reviews and keep baselines consistent.
- Should not over-assign GPU tasks when provenance/data-freeze is the bottleneck.

## 6. Non-Negotiable Numerical Locks / Warnings

1. Paper-1:
   - Do not headline “real PCM 4-bit rescue”.
   - 4-bit IdealDevice 86.16% is algorithmic ablation only.
   - Main PCM deployment statement should emphasize 6-bit Pareto midpoint and 1 pp drift SLA.

2. K107:
   - Use 22.1849 PPL as raw digital baseline under current evaluator.
   - Do not compare current K107 results to old 15.62/15.68 baseline.
   - Use ~3.14 PPL as canonical HAT gain from raw baseline to HAT digital/no patch.
   - Use 19.043 / 19.060 / 19.483 / 19.644 ladder for ablation figure.

3. Remote105:
   - Treat proportional HAT as provisional-cross-architecture.
   - DeiT evidence is strong; ViT evidence is positive on average but seed456 digital outlier should be disclosed.

## 7. Immediate Next Actions

1. Ask Kimi for local PCM frontier inventory/5-bit closure result; decide whether Paper-1 6-bit statement needs refinement.
2. Let Gemini continue Paper-1 figure polish, but ensure captions match locked narrative.
3. For 107, no new GPU needed. Use frozen package and draft figures if building Paper-2 outline.
4. For 105, no immediate rerun unless user wants more ViT seeds to resolve seed456 outlier.
5. If starting a new conversation, first read this file and then latest `BROADCAST.md` tail.

## 8. Useful Paths

- This compact: `report_md/_gpt/CONTEXT_COMPACT_20260507.md`
- Broadcast: `/home/qiaosir/projects/BROADCAST.md`
- Paper-1 LaTeX: `paper/latex_gpt/`
- 107 clean review worktree: `/home/qiaosir/projects/HAT_107_clean_review`
- 107 canonical freeze: `coordination/REMOTE107_K107_CANONICAL_FREEZE_20260508.md` on `origin/107-clean`
- 105 full return: `docs/handoff/20260508_full_return.md` on `origin/105-remote-results`
