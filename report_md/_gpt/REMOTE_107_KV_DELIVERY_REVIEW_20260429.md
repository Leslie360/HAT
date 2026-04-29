# Remote 107 KV-Cache Delivery Review

**Date:** 2026-04-29  
**Reviewer:** Codex  
**Source:** User-transferred remote delivery summary. The transferred text title says "105 server", but user clarified this is 107 KV-cache work. Recorded here as **Remote 107 / Work-2 KV-cache**.

## 1. Received Result Summary

Remote 107 reports that the LLM analog KV-cache task is complete at code/prototype level and has produced WikiText-2 PPL data.

Reported engineering fixes:

1. **LLM PPL evaluator rewrite**
   - Added vectorized sliding-window evaluation.
   - Bypasses GPT-2 1024-token length limit by sliding over WikiText-2.
   - Reported runtime reduced from ~3.5h to ~25min at batch size 64.

2. **Transformers compatibility**
   - Adapted to `transformers==5.7.0` `DynamicCache.layers` structure.
   - Remote claims physical noise is injected into real KV-cache state, not a detached proxy.

3. **Scheduler hardening**
   - `launch_queue.py` now checks `/proc/{pid}/status`.
   - Purpose: avoid zombie-process deadlock in queued runs.

Reported WikiText-2 PPL table, batch=64, retention step=0.1s:

| Profile | Retention | PPL | Remote conclusion |
|---|---:|---:|---|
| PCM, 32 states | off | 107.27 | best static precision |
| Organic | off | 429.05 | larger intrinsic noise, worse initial PPL |
| Organic | on | 683.74 | retention worsens PPL by ~60% |
| PCM, 32 states | on | 751.28 | retention-triggered memory avalanche |

## 2. Codex Assessment

This is a potentially strong Work-2 direction, but it is not yet final-paper-grade evidence.

The useful scientific signal is not simply "PCM vs organic". The stronger narrative is:

> Static analog precision and temporal cache stability can rank devices differently. A high-static-precision PCM cache can be best without retention, yet become worse than organic under read/write lifetime dynamics.

That is an interesting KV-cache-specific claim because KV cache is not a static weight store. It is repeatedly read over a token-dependent lifetime. Therefore retention can dominate the apparent material ranking.

## 3. Required Metadata Before We Trust The Numbers

Remote 107 must return the following in Markdown. No checkpoint transfer is needed.

1. Exact Git SHA and branch.
2. `git diff --stat` and patches for changed files, especially evaluator/cache injection/queue code.
3. Exact model and tokenizer: GPT-2 small/medium or another model; local path if used.
4. Exact `transformers`, `torch`, CUDA, GPU, dtype.
5. WikiText-2 split and preprocessing details.
6. Sliding-window formula:
   - max window length
   - stride
   - how overlapping token losses are counted
   - whether BOS/EOS handling matches common PPL practice
7. Digital baseline PPL with the same evaluator and dataset.
8. No-noise/no-quant analog parity PPL. This should match digital baseline within small tolerance.
9. KV injection scope:
   - all layers or selected layers
   - K only, V only, or both
   - pre-softmax vs post-cache location
10. Profile definitions:
    - PCM 32-state quantization details
    - Organic noise distribution
    - D2D/C2C/retention equations and parameter values
    - clipping/range calibration policy
11. Retention time semantics:
    - what one `0.1s` step means per token/window
    - whether token lifetime grows with distance from current query
    - whether old KV entries decay more than recent entries
12. Repeats/seeds and variance. The current table appears single-run.

## 4. Immediate Validation Gate

Before expanding experiments, 107 should run this minimal sanity matrix:

| Run | Purpose | Expected outcome |
|---|---|---|
| Digital FP baseline | evaluator baseline | plausible WikiText-2 PPL for chosen model |
| Analog cache, no quant, no noise, no retention | injection correctness | PPL ~= digital baseline |
| PCM 32-state, retention off, 3 seeds | static result stability | mean near reported 107.27 if valid |
| PCM 32-state, retention on, 3 seeds | avalanche stability | mean near reported 751.28 if valid |
| Organic retention off/on, 3 seeds | material comparison stability | preserve PCM/Organic rank inversion under retention |

Kill criterion: if no-noise/no-quant analog parity differs from digital by >1% PPL, stop and debug injection/evaluator before interpreting material results.

## 5. Next 107 Task List

Priority order for the 8-card server:

### T107-A: Reproducibility Packet

Return one Markdown file containing:

```bash
git rev-parse HEAD
git status --short
git diff --stat
git diff -- paper2 scripts tests
python - <<'PY'
import torch, transformers, json
print(json.dumps({
  'torch': torch.__version__,
  'transformers': transformers.__version__,
  'cuda': torch.version.cuda,
  'device_count': torch.cuda.device_count(),
  'devices': [torch.cuda.get_device_name(i) for i in range(torch.cuda.device_count())],
}, indent=2))
PY
```

### T107-B: Baseline/Parity Matrix

Run digital baseline and analog no-noise parity with the exact same sliding-window evaluator. Return PPL, token count, total NLL, elapsed time, and exact command.

### T107-C: Retention Time Sweep

For PCM 32-state and Organic, run retention steps:

```text
0, 0.01s, 0.03s, 0.1s, 0.3s, 1.0s
```

Return PPL and, if available, per-position NLL buckets. Objective: determine whether PCM collapse is threshold-like or monotonic.

### T107-D: Noise Source Ablation

Separate these effects:

1. quantization only
2. static programming noise only
3. read/cycle noise only
4. retention only
5. full profile

Run for PCM and Organic. This is needed to support the claim that retention, not quantization alone, causes the rank reversal.

### T107-E: Scope Ablation

Run at least:

1. K only
2. V only
3. K+V
4. last 25% layers only
5. all layers

Objective: locate whether avalanche is driven by key corruption, value corruption, or global all-layer accumulation.

### T107-F: Compact Return Format

Return one `.md` plus small `.json` tables only. Do not send model weights.

Required table columns:

```text
run_id, model, dataset_split, profile, retention_step_s, kv_scope, bit_states, seeds, ppl_mean, ppl_std, token_count, command, git_sha
```

## 6. Narrative Decision

If validation holds, Work-2 should pivot to this claim:

> Analog KV-cache viability is governed by temporal memory stability, not static write precision alone. KV-cache retention can invert the apparent material ranking: PCM is superior for static cache storage but can fail catastrophically under cache lifetime dynamics, while organic-like profiles may be worse statically yet degrade more gradually.

Do not yet phrase this as a universal PCM-vs-organic conclusion. It is currently conditional on the remote profile definitions, model, and retention-time mapping.

## 7. Broadcast Message

Remote 107 has produced an important PPL-level result: PCM 32-state is best without retention (PPL 107.27), but with retention it collapses harder than Organic (PCM 751.28 vs Organic 683.74). Codex recommends treating this as a provisional narrative pivot and immediately validating with digital baseline, no-noise analog parity, 3-seed repeats, retention-time sweep, noise-source ablation, and K/V/layer-scope ablation.
