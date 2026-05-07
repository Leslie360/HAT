# Remote 107 Next Tasks — Baseline Reconciliation + EPSC Stress

Date: 2026-05-07
Owner: Remote 107
Priority: P0 before any larger exploration

## 0. Context

Codex reviewed the latest 107 return through `origin/107-clean@a5b89be`.

Current result is strong:

- `last1` terminal-layer analog KV `[23]` is stable across train seeds and fresh D2D seeds.
- `last2` is consistently worse.
- `all24` is catastrophic and should remain a stress/control anchor only.
- Low state counts remain viable.

But two blockers remain before these results can become manuscript-canonical:

1. Digital baseline mismatch: older notes cite **15.68 PPL**, while K107-B reports **22.18 PPL**.
2. HAT fine-tuning gain must be separated from analog hardware overhead.

Do the following in order.

---

## P0-A: Baseline Reconciliation

Run both baseline evaluators, if both are available.

### A1. Current K107 evaluator baseline

Use the exact evaluator used by K107-A/B/C (`p3_hat_train.evaluate_ppl` / `p3_hat_eval.py` path).

Return:

- exact command;
- JSON path;
- PPL;
- `ctx_len`, `stride`, `batch_size`, dataset split;
- git commit and git status.

### A2. Old/vectorized evaluator baseline

If the old evaluator that produced **15.68 PPL** is available, rerun it on `EleutherAI/pythia-410m-deduped`.

Return the same metadata. If unavailable, explicitly state which file/function used to produce 15.68 and why it cannot be rerun.

### A3. Verdict

Write one short section explaining which PPL number is canonical for K107 comparisons and why.

---

## P0-B: Paired HAT Checkpoint Ablations

For each checkpoint:

- `k107_a1_last1_seed42`
- `k107_a1_last1_seed123`
- `k107_a1_last1_seed456`

Run four paired eval modes on WikiText-2 test, same evaluator, same context length, same stride:

| Mode | Analog patch | sigma_c2c | sigma_d2d | Purpose |
|---|---|---:|---:|---|
| B1 | OFF | 0 | 0 | HAT fine-tuned digital checkpoint |
| B2 | ON | 0 | 0 | quantization-only overhead |
| B3 | ON | 0 | 0.02 | nominal D2D hardware overhead |
| B4 | ON | 0 | 0.05 | high D2D hardware overhead |

Eval seeds for B3/B4: `42, 456, 1001`.

For B1/B2, one deterministic eval is enough unless the code is stochastic.

Return an aggregate CSV:

```csv
checkpoint,train_seed,mode,analog_patch,n_states,sigma_c2c,sigma_d2d,eval_d2d_seed,ppl,ctx_len,stride,batch_size,git_commit,json_path
```

Interpretation required:

- `B1 -> B2` = quantization/patch overhead after HAT fine-tuning.
- `B2 -> B3/B4` = physical D2D noise overhead after HAT fine-tuning.
- pretrained baseline vs `B1` = pure fine-tuning gain.

---

## P0-C: Export Train Metadata

The current v3 deliverable contains eval JSONs but not the train JSON / checkpoint metadata required for final archive.

Create:

```text
deliverable/results_v3/train_meta/
```

For every K107-A and K107-C checkpoint, copy or create small metadata files only:

- `hat_config.json`
- train result JSON if available;
- if train JSON is missing, create `train_reconstructed_<checkpoint>.json` from launcher command + checkpoint config.

Required fields:

- checkpoint name;
- train seed;
- train D2D seed;
- analog layers;
- n_states;
- sigma_c2c / sigma_d2d;
- max_steps;
- lr;
- ctx_len;
- train dataset;
- eval dataset;
- exact train command;
- git commit;
- git status short.

Do not upload model weights.

---

## P1: EPSC Proxy Stress Eval

Use DS EPSC proxy only as a stress-test profile, not direct hardware validation.

Checkpoint: start with `k107_a1_last1_seed42`. If PPL is acceptable, repeat the central setting for seeds 123 and 456.

| ID | sigma_c2c | sigma_d2d | Eval D2D seeds | Purpose |
|---|---:|---:|---|---|
| EPSC-e1 | 0.05 | 0.05 | 42, 456, 1001 | low proxy stress |
| EPSC-e2 | 0.10 | 0.10 | 42, 456, 1001 | central EPSC proxy |
| EPSC-e3 | 0.15 | 0.15 | 42, 456, 1001 | high proxy stress |
| EPSC-e4 | 0.00 | 0.20 | 42, 456, 1001 | D2D-only extreme |
| EPSC-e5 | 0.01 | 0.10 | 42, 456, 1001 | HAT-default C2C plus proxy D2D |

Kill criterion:

- If EPSC-e2 exceeds **25 PPL** on any eval seed, do not claim EPSC-proxy compatibility. Report it as a stress limit.

Return:

- JSONs with full metadata;
- `summary.csv`;
- one MD report with pass/fail and interpretation.

---

## P2: Optional Scale Check

Only after P0 and P1.

Run minimal Pythia-1B selective terminal-layer check:

- terminal layer only;
- train seeds: 42, 123;
- sigma_d2d train: 0.02;
- eval sigma_d2d: 0.02 and 0.05;
- eval seeds: 42, 456, 1001;
- same metadata requirements.

Purpose: determine whether the selective terminal-layer result scales beyond 410M.

---

## Return Format

Create a new return file:

```text
coordination/REMOTE107_BASELINE_EPSC_RETURN_20260508.md
```

Include:

1. Branch and commit SHA.
2. Git status short.
3. Environment packet.
4. Exact commands.
5. Tables for P0-A, P0-B, P0-C, P1, optional P2.
6. JSON/CSV paths.
7. Explicit verdict: `LOCK`, `PROVISIONAL`, or `KILL` for each claim.

