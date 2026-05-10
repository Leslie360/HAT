# CODEX Empirical Mechanism Report

**Date:** 2026-04-25  
**Scope:** Claude Round-7 `DISPATCH_CODEX_EMPIRICAL_DEEPENING_20260425.md` Phase 2.  
**Constraint:** Existing checkpoints only; no new training; canonical model code unchanged.  

## 1. Provenance

- commit_hash: `cbb5db0759cf981d59f702343097c17fe6d944a1`
- git_worktree_dirty: `True`
- cuda_device_name: `NVIDIA GeForce RTX 5070 Ti`
- pytorch_version: `2.10.0+cu128`
- code_sha256: `64bbbcd1e78f2813806903dcd0b16767465fc9fe43a2a8c9a61f7b8f3a9c3483`
- gpu_resize_eval: `True`
- gpu_resize_protocol: `CIFAR32 ToTensor -> GPU bilinear resize 224 -> GPU normalize`
- Analysis script: `scripts/_gpt/empirical_mechanism_20260425.py`
- Figures directory: `paper/figures/`
- JSON directory: `report_md/_gpt/json_gpt/`

## 2. Per-Job Results

### E1 Hessian Eigenspectrum

| Checkpoint | Params | Batch | Top-1 abs Ritz eigenvalue | JSON |
|:--|:--|--:|--:|:--|
| Ensemble NL=1 | analog | 32 | 221.2984 | `report_md/_gpt/json_gpt/hessian_eigenspectrum_canonical_ensemble.json` |
| Standard NL=1 | analog | 32 | 23.2765 | `report_md/_gpt/json_gpt/hessian_eigenspectrum_canonical_standard.json` |
| M1 Standard | analog | 32 | 30058.3964 | `report_md/_gpt/json_gpt/hessian_eigenspectrum_cx_m1.json` |
| M2 Ensemble | analog | 32 | 5705.5966 | `report_md/_gpt/json_gpt/hessian_eigenspectrum_cx_m2.json` |
| M3 Proportional | analog | 32 | 1764.9653 | `report_md/_gpt/json_gpt/hessian_eigenspectrum_cx_m3.json` |

Standard/Ensemble top-1 ratio: **0.11x**.
**Escalation:** E1 contradicts the simple global-Hessian flat-minima hypothesis: canonical Ensemble HAT has a larger analog-parameter top-1 Ritz value than canonical Standard HAT under this batch-32 Lanczos protocol.
Protocol note: full analog-parameter HVP required disabling CUDA flash/mem-efficient SDPA because fused efficient-attention backward lacks second derivatives in this PyTorch build.
Figure: `paper/figures/figS_hessian_spectrum.{png,pdf}`

### E2 D2D Loss Landscape

| Model | alpha=0 acc | alpha=1 acc | alpha=3 acc |
|:--|--:|--:|--:|
| Standard NL=1 | 94.67 | 10.00 | 9.55 |
| Ensemble NL=1 | 91.25 | 88.39 | 27.06 |
Figure: `paper/figures/figS_d2d_loss_landscape.{png,pdf}`

### E3 CKA M-Series

- Aggregate off-diagonal CKA: **0.455** (mixed/divergent representations).
- Common analog layers: `42`.
Figure: `paper/figures/figS_cka_mseries.{png,pdf}`

### E4 Per-Layer D2D Sensitivity

- Baseline clean accuracy: **89.33%**.
| Rank | Layer | Group | Drop (pp) |
|--:|:--|:--|--:|
| 1 | `stages.2.blocks.4.mlp.fc2` | mlp | 1.38 |
| 2 | `patch_embed.conv1.conv` | patch_embed | 1.18 |
| 3 | `stages.2.blocks.1.mlp.fc1` | mlp | 0.31 |
| 4 | `stages.2.blocks.5.mlp.fc2` | mlp | 0.29 |
| 5 | `stages.2.blocks.2.mlp.fc1` | mlp | 0.28 |
Top-5 groups: `mlp, patch_embed, mlp, mlp, mlp`.
Figure: `paper/figures/figS_per_layer_sensitivity.{png,pdf}`

### E5 Checkpoint Averaging

- Avg(M1 seed123, M5 seed456) fresh mean: **10.00 ± 0.00%**.
- Ensemble reference mean: **86.37%**.
Figure: `paper/figures/figS_checkpoint_avg.{png,pdf}`

## 3. Cross-Job Synthesis

All five requested jobs have landed. The empirical picture is split: D2D-direction robustness is strongly supported, but a simple global-Hessian flatness story is not.

- E1 analog-parameter Hessian is a negative/surprising diagnostic: Ensemble top-1 221.30 exceeds Standard top-1 23.28. Do not claim Ensemble HAT is globally flatter in ordinary parameter space.
- E2 is the positive mechanism result: at alpha=1.0, Ensemble keeps 88.39% while Standard is 10.00% (gap 78.39 pp). This supports flatness specifically along the D2D mismatch direction.
- E3 shows aggregate M-series off-diagonal CKA of 0.455, which tests whether 80-82% severe-NL recovery comes from representational convergence or multiple distinct routes.
- E4 top-5 sensitivity contains 4/5 MLP layers. If this remains after full eval, it supports the MLP-bottleneck wording.
- E2 alpha=3 Ensemble-Standard accuracy gap is 17.52 pp; positive gap supports D2D-direction robustness.

## 4. Paper-Safe Statements

- Use mechanism figures as supplementary diagnostics, not as replacements for frozen source/fresh headline metrics.
- Do not write `Ensemble HAT finds a globally flatter Hessian minimum`; E1 contradicts that simple statement under the analog-parameter protocol.
- Prefer: `Ensemble HAT is robust along device-mismatch directions, while ordinary parameter-space Hessian sharpness is not the explanatory axis.`
- E4 can replace the contaminated historical groupwise table only if the top-layer ranking is stable and post-fix provenance is cited.
- E5, if near chance, supports the statement that per-epoch resampling is not equivalent to naive checkpoint averaging.

