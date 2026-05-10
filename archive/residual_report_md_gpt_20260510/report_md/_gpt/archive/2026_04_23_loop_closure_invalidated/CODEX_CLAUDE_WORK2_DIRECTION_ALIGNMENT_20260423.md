# Codex Alignment To Claude Work 2 Direction Lock

**Date:** 2026-04-23 20:05 CST
**Owner:** Codex
**Inputs:** `BROADCAST_ASSIGNMENT_20260421Q.md`, `CLAUDE_WORK2_DIRECTION_LOCK_20260423.md`
**Status:** Direction accepted; Codex CX-L preflight started; no GPU launch while R2 owns GPU.

## Decision Read

Claude locks Work 2 to **Direction C: LLM KV-cache mapping to organic optoelectronic CIM**.

Codex accepts this as the active Work 2 direction unless the user vetoes it.

Important boundary:

- The **Work 2 addendum** in `BROADCAST_ASSIGNMENT_20260421Q.md` is current.
- Earlier Round-Q Work 1 CX-K/J1d sections are historically useful but partly superseded by the 2026-04-23 dual-bug recovery, R1, and live R2. Do not resurrect old J1d/K-series conclusions as active truth.

## Current Work 1 State

Work 1 is still active and owns the GPU:

- R1 first-order clean anchor completed: source best `91.50%`, fresh `34.5612 +- 8.7878%`.
- R2 corrected-SO2 comparison is running on GPU.
- Latest observed R2 trajectory before this memo:
  - epoch 49: best `90.63%`
  - epoch 54: test `89.44%`, best `90.63%`
  - epoch 59: test `90.33%`, best `90.63%`

Therefore Codex will not launch CX-L1/CX-L2 until R2 train+fresh is complete or explicitly paused by the user.

## Work 2 Current Artifact State

### Existing

- Claude lock: `report_md/_gpt/CLAUDE_WORK2_DIRECTION_LOCK_20260423.md`
- Kimi scope lock: `report_md/_gpt/KIMI_WORK2_SCOPE_LOCK_20260423.md`
- Kimi experiment plan: `report_md/_gpt/KIMI_WORK2_EXPERIMENT_PLAN_20260423.md`
- Chinese Work 2 scope stub: `paper/thesis_cn/chapter_6_work2_scope.tex`
- Gemini G-HH21-G-HH25 memos exist:
  - `GEMINI_WORK2_RETENTION_THEORY_20260423.md`
  - `GEMINI_WORK2_QUANTIZATION_FLOOR_20260423.md`
  - `GEMINI_WORK2_BASELINE_COMPARISON_20260423.md`
  - `GEMINI_WORK2_HOSTILE_REVIEW_20260423.md`
  - `GEMINI_WORK2_CONFERENCE_FIT_20260423.md`

### Still missing / incomplete

- `paper/paper2/skeleton_v1/SKELETON.md` is still missing.
- `paper/paper2/skeleton_v1/00_abstract.md` is still missing.
- `KIMI_WORK2_CITATION_CONSOLIDATION_20260423.md` is not present in the first lookup.
- Codex CX-L1 baseline JSON is not present yet.

## Codex CX-L Preflight Result

Created and ran download-free preflight script:

- Script: `scripts/_gpt/cx_l1_env_check.py`
- JSON: `report_md/_gpt/json_gpt/cx_l1_env_preflight.json`

Result:

| Check | Status |
|---|---|
| `torch` | present: `2.10.0+cu128` |
| `numpy` | present: `2.4.2` |
| `transformers` | missing |
| `datasets` | missing |
| `accelerate` | missing |
| `evaluate` | missing |
| `sentencepiece` | missing optional but likely needed |
| TinyLlama HF cache | absent |
| GPT-2-medium HF cache | absent |
| CX-L1 ready | no |

Recommended install command, to run before CX-L1:

```bash
/home/qiaosir/miniconda3/envs/LLM/bin/python -m pip install transformers datasets accelerate evaluate sentencepiece safetensors
```

Model/dataset downloads will also be required unless the user provides a local HF cache.

## Codex Execution Policy

1. Finish R2 train+fresh first. It is the current GPU owner.
2. Do not launch CX-L1 while R2 or any Work 1 GPU run is active.
3. Do non-GPU CX-L prep now:
   - environment checks,
   - script scaffolding,
   - model/dataset cache checks,
   - JSON schema definitions,
   - blocker memos.
4. After R2 completes, install missing dependencies if not already installed, then run CX-L1 baseline.
5. Do not start CX-L2/CX-L3/CX-L4 noise/quantization/retention sweeps until CX-L1 baseline perplexity is validated.
6. If TinyLlama baseline cannot be established within the pre-authorized limit, fall back to GPT-2-medium and alert Claude.

## Immediate Requests To Other Agents

### Kimi

- Finish `paper/paper2/skeleton_v1/SKELETON.md` and `00_abstract.md` using the KV-cache direction.
- Add `KIMI_WORK2_CITATION_CONSOLIDATION_20260423.md` or confirm its path if already written.
- Keep all numbers as placeholders until CX-L1/CX-L2 land.

### Gemini

- G-HH21-G-HH25 are present, but some equations contain formatting artifacts from escaped tabs (e.g. `\tau`, `\text{}` rendered incorrectly). Please clean if these memos are used in synthesis.
- Do not cite the `N >= 4` quantization-floor hypothesis as a result until CX-L3 validates it.

### Claude

- Direction C is accepted by Codex.
- Codex cannot land `cx_l1_tinyllama_baseline.json` until dependencies/model cache are available and R2 releases the GPU.

## Bottom Line

Work 2 direction is clear and good: KV-cache is the strongest organic-specific story. Codex is not blocked conceptually; it is blocked operationally by active R2 GPU ownership plus missing HuggingFace dependencies/cache.
