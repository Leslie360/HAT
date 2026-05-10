# Remote 105/107 Long Tasklist — Paper-1 Validation And Work-2 KV Track

Date: 2026-05-09
Owner: Codex
Purpose: one long-running tasklist that can be copied to GitHub/remote agents without repeated user instructions.

## Global Rules

1. Do not mix Paper-1 final claims with Work-2 KV-cache claims.
2. Return small text artifacts only: Markdown summaries, CSV/JSON tables, exact commands, environment packets, and selected logs.
3. No large checkpoints unless explicitly requested.
4. Every result must include: exact command, git SHA, environment, data split, seed, metric definition, and whether it is candidate/main/supplementary/future-only.
5. If a bug is found, label old results as superseded before reporting new results.

## Server 105 — Multi-dataset / Cross-architecture Validation

### Objective
Validate whether proportional HAT generalizes beyond the local Paper-1 TinyViT/PCM core. This is validation evidence, not a main Paper-1 claim unless later accepted by Codex.

### Required Outputs

1. Complete 3-seed table for each available architecture and HAT mode:
   - `deit` and `vit`
   - `digital`, `standard`, `ensemble`, `proportional`
   - source/best test accuracy, fresh mean/std, delta/fresh-source gap
2. Same-architecture digital comparisons:
   - proportional vs digital per seed and averaged
   - flag any seed where proportional does not beat digital
3. Noise-off ablation where available:
   - `noise_off`, `source`, `fresh`, `digital`
   - interpret as regularization vs robustness only if same architecture and seed are controlled
4. Exact reproducibility packet:
   - git SHA, git status, command lines, Python/PyTorch/timm/CUDA/GPU
   - fresh-eval protocol: number of instances, MC runs, D2D/C2C sampling
5. One-page verdict:
   - strong validation / weak validation / inconclusive
   - whether to place in supplement, future work, or exclude

### Kill Criteria

- Stop using a run if source means train accuracy instead of best test accuracy.
- Stop using a comparison if architecture, seed, or data split differs between proportional and digital.
- Do not claim proportional beats digital unless the same-architecture multi-seed comparison supports it.

## Server 107 — Analog KV-cache / Work-2 Track

### Objective
Build a separate Work-2 evidence base for analog KV-cache HAT. Do not feed these results into Paper-1 main claims.

### Required Outputs

1. Corrected-noise rerun report after the reported noise-algorithm bug:
   - old result vs corrected result
   - what changed mathematically
   - whether trends are preserved
2. Core math/code reproducibility packet:
   - exact quantization equation
   - C2C/D2D/retention injection points
   - seed handling
   - sliding-window PPL definition
   - train/test split proof
3. HAT effectiveness summary:
   - pre-HAT vs post-HAT PPL by D2D/C2C setting
   - seed stability table
   - selective-layer vs all-layer table
4. Generalization summary:
   - train noise vs eval noise matrix
   - D2D high-noise training robustness result
   - C2C generalization result
5. One-page Work-2 decision:
   - promising enough for separate paper / only appendix pilot / reject
   - next minimal experiments if promising

### Kill Criteria

- Stop any claim if base+patch PPL is far from clean baseline without explanation.
- Stop any all-layer conclusion if selective-layer setting is not separately reported.
- Stop any HAT claim if train/test split or sliding-window scoring is ambiguous.

## Return Format

Each server should return one Markdown file plus optional CSV/JSON tables:

```text
REMOTE_105_DELIVERY_YYYYMMDD.md
REMOTE_107_DELIVERY_YYYYMMDD.md
```

Required top section:

```text
Verdict: PASS / PARTIAL / FAIL
Use in Paper-1: main / supplement / future-only / exclude
Critical bugs found: yes/no
Exact artifact paths: ...
```
