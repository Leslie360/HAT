# Remote 107 Phase P8 Corrected-Noise Work-2 Tasklist

Date: 2026-05-09
Issued by: Codex
Target: 107 server / Analog KV-cache Work-2 lane
Status: Work-2 only. Do not route into Paper-1 claims.

## 1. Goal

Lock whether selective terminal-layer Analog KV-cache + HAT remains strong after the corrected noise algorithm rerun, with enough metadata for local reproduction and future paper drafting.

## 2. Absolute Requirements

| Requirement | Details |
|---|---|
| Corrected noise code | Identify exact file/function and commit where bug is fixed. |
| Core math archive | Include the minimal code snippets for quantization, C2C, D2D, retention, and layer injection. |
| Exact git SHA | For every result table. |
| Exact commands | Training and eval commands, including context length and analog layer list. |
| Dataset split | WikiText train/test or exact equivalent. |
| Evaluation protocol | Sliding window, stride, max length, batch size. |
| Seed semantics | Training seed, D2D seed, C2C randomness, eval seeds. |
| JSON metadata | Every output JSON must include commit, command, config, seed, checkpoint path. |
| Large files | Do not send checkpoints unless explicitly requested; report paths and hashes instead. |

## 3. Experiment Matrix

### P0: Corrected-noise selective rerun

| Run | Analog layers | Noise | Context | Steps | Seeds | Output |
|---|---|---|---:|---:|---|---|
| Last1 | `[23]` | D2D=0.02, 0.04, 0.05 | 1024 | final chosen | 42/123/456 if feasible | PPL mean/std |
| Last2 | `[22,23]` | D2D=0.02, 0.04, 0.05 | 1024 | final chosen | 42/123/456 if feasible | PPL mean/std |
| Last4 | `[20,21,22,23]` | D2D=0.02, 0.04, 0.05 | 1024 | final chosen | 42/123/456 if feasible | PPL mean/std |
| All24 | all layers | D2D=0.02, 0.04 | 1024 | final chosen | 42 only if expensive | stress control |

### P1: C2C and combined robustness

| Run | Analog layers | Eval noise | Purpose |
|---|---|---|---|
| Last1 C2C | `[23]` | C2C=0.01/0.02 | Check read-noise robustness. |
| Last1 combined | `[23]` | D2D=0.02 + C2C=0.01 | Realistic mixed noise. |
| Last2 combined | `[22,23]` | D2D=0.02 + C2C=0.01 | Compare deployment cost. |

### P2: Ablations if GPU remains available

| Run | Purpose |
|---|---|
| No-HAT pre-eval for selected layers | Confirm HAT gain not from patch artifact. |
| 200 vs 500 vs 1000 steps for Last1 | Determine diminishing returns. |
| ctx=512 vs ctx=1024 for Last1 | Check context sensitivity. |

## 4. Required Tables

| Table | Columns |
|---|---|
| Corrected-noise summary | layers, train noise, eval noise, ctx, steps, seed, pre PPL, post PPL, checkpoint, JSON |
| Fresh-D2D summary | layers, eval D2D, n eval seeds, PPL mean, PPL std, best/worst seed |
| Comparison to old bugged data | old value, corrected value, trend preserved?, note |
| Metadata completeness | run id, commit, command, env, JSON, checkpoint hash, pass/fail |

## 5. Narrative Gates

| Gate | Work-2 route opens if |
|---|---|
| Selective terminal route | Last1 or Last2 corrected-noise PPL remains near clean/all-layer baseline and stable across D2D seeds. |
| All-layer stress route | All24 remains worse than selective; this supports selective deployment. |
| HAT effect | Post-HAT beats pre-HAT under corrected noise. |
| Reproducibility | Metadata complete enough for local or rented-GPU replay. |

## 6. Return Format

Send one Markdown report:

`REMOTE_107_PHASE_P8_CORRECTED_NOISE_REPORT_YYYYMMDD.md`

Also include compact CSV/JSON summaries if possible. Do not send large checkpoints unless requested.
