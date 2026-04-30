# Remote 107 Next Tasks — Corrected D2D Seed / Fresh-Device Matrix

Date: 2026-04-30
Owner: Remote 107 agent
Requester: Codex/local architect
Status: Required before 107 numbers can become canonical

## Goal

Close the remaining ambiguity in the analog KV-cache HAT results:

1. Separate training RNG from physical D2D device-instance seed.
2. Distinguish same-device adaptation from fresh-device generalization.
3. Return result JSONs with enough metadata for local audit and future paper use.

Current v2 trends are useful, but old `deliverable/results_v2/*.json` files do not contain `train_seed` or `d2d_seed`, so those numbers remain provisional.

## Definitions

- `train_seed`: seed for training RNG, model/data stochasticity, C2C sampling stream, etc.
- `train_d2d_seed`: physical D2D offset pattern used during HAT training.
- `eval_d2d_seed`: physical D2D offset pattern used during evaluation.
- Same-instance eval: `eval_d2d_seed == train_d2d_seed`.
- Fresh-instance eval: `eval_d2d_seed != train_d2d_seed`, or a table over multiple eval D2D seeds for one fixed checkpoint.

## P0 — Sanity Before Running

Run from the clean branch checkout.

```bash
git rev-parse --short HEAD
git status --short
python -m py_compile deliverable/code/p3_hat_train.py deliverable/code/p3_hat_eval.py pipeline_d2d_seed.py
```

Return these three outputs in the result report.

## P1 — Minimum Fresh-D2D Generalization Matrix

### Required Checkpoints

If these checkpoints already exist on 107, reuse them. If not, train them first.

| Checkpoint role | Train sigma_d2d | Train sigma_c2c | train_seed | train_d2d_seed | max_steps | analog_layers |
|---|---:|---:|---:|---:|---:|---|
| all-layer D2D=0.02 | 0.02 | 0.0 | 42 | 42 | 500 | all 24 |
| all-layer D2D=0.04 | 0.04 | 0.0 | 42 | 42 | 500 | all 24 |
| selective last1 D2D=0.02 | 0.02 | 0.0 | 42 | 42 | 500 | `23` |
| selective last2 D2D=0.02 | 0.02 | 0.0 | 42 | 42 | 500 | `22,23` |

Training command template:

```bash
python deliverable/code/p3_hat_train.py \
  --name <name> \
  --n_states 256 \
  --sigma_d2d <train_sigma_d2d> \
  --sigma_c2c <train_sigma_c2c> \
  --max_steps 500 \
  --max_length 512 \
  --seed 42 \
  --d2d-seed 42 \
  --output_dir <OUT_DIR> \
  [--analog_layers 23 or --analog_layers 22,23]
```

### Required Fresh Eval

For each checkpoint above, evaluate:

- `eval_sigma_d2d`: `0.02`, `0.04`, `0.05`
- `eval_d2d_seed`: `42`, `123`, `456`, `789`, `1001`
- `eval_sigma_c2c`: `0.0`

Important: pass `--d2d-seed` explicitly to override checkpoint `hat_config.json` when testing fresh-device eval.

Eval command template:

```bash
python deliverable/code/p3_hat_eval.py \
  --checkpoint_dir <CKPT_DIR> \
  --n_states 256 \
  --sigma_d2d <eval_sigma_d2d> \
  --sigma_c2c 0.0 \
  --d2d-seed <eval_d2d_seed> \
  --max_length 512 \
  --output_dir <OUT_DIR>
```

Expected total for P1:

- 4 checkpoints x 3 eval noise levels x 5 eval seeds = 60 eval runs.
- Training only needed if the four required checkpoints do not already exist.

## P2 — Same-Instance Adaptation Table

The current `pipeline_d2d_seed.py` is useful for this, but label it correctly.

It should produce:

| train_sigma_d2d | train_d2d_seed | eval_sigma_d2d | eval_d2d_seed | PPL |
|---:|---:|---:|---:|---:|

For same-instance rows, `eval_d2d_seed == train_d2d_seed`.

Do not call this fresh-device generalization.

## P3 — C2C Stability Confirmation

C2C is re-sampled per forward, so it is less affected by fixed D2D-seed semantics.

Run only if GPU time is available after P1:

| Checkpoint | Eval C2C | Eval D2D | Seeds |
|---|---:|---:|---|
| C2C=0.01 all-layer checkpoint | 0.0, 0.005, 0.01, 0.015, 0.02 | 0.0 | train_seed 42 plus repeat eval 3 times |
| Combined checkpoint | 0.02 | 0.0, 0.02, 0.04 | eval_d2d_seed 42,123,456 |

## Required JSON Metadata

Every new JSON must include at least:

```json
{
  "git_commit": "<short or full SHA>",
  "script": "deliverable/code/p3_hat_train.py or p3_hat_eval.py",
  "mode": "train or eval",
  "model": "EleutherAI/pythia-410m-deduped",
  "dataset_train": "wikitext-2-raw-v1/train or null",
  "dataset_eval": "wikitext-2-raw-v1/test",
  "n_states": 256,
  "sigma_c2c": 0.0,
  "sigma_d2d": 0.02,
  "train_seed": 42,
  "train_d2d_seed": 42,
  "eval_d2d_seed": 123,
  "analog_layers": [23],
  "max_length": 512,
  "max_steps": 500,
  "ppl_before": null,
  "ppl_after": null,
  "ppl": 18.0,
  "checkpoint_dir": "...",
  "command": "exact command line"
}
```

If a field does not apply, set it to `null`, not omitted.

## Required Summary Tables

Return a Markdown summary with these tables.

### Table A — Training Checkpoints

| name | train_sigma_d2d | train_sigma_c2c | train_seed | train_d2d_seed | analog_layers | ppl_before | ppl_after | checkpoint_dir |
|---|---:|---:|---:|---:|---|---:|---:|---|

### Table B — Fresh D2D Eval

| checkpoint | train_d2d_seed | eval_d2d_seed | eval_sigma_d2d | analog_layers | ppl | verdict |
|---|---:|---:|---:|---|---:|---|

### Table C — Aggregated Fresh D2D Stats

Aggregate across eval_d2d_seed for each checkpoint and eval_sigma_d2d.

| checkpoint | eval_sigma_d2d | mean PPL | std PPL | min | max | n |
|---|---:|---:|---:|---:|---:|---:|

### Table D — Same vs Fresh Gap

| checkpoint | eval_sigma_d2d | same-instance PPL | fresh mean PPL | fresh-same delta | interpretation |
|---|---:|---:|---:|---:|---|

## Kill / Escalation Criteria

Stop and report immediately if any of these occurs:

- `p3_hat_eval.py` silently ignores `--d2d-seed` override.
- `hat_config.json` is missing for new checkpoints.
- eval all-layer vs selective `analog_layers` mismatch is observed.
- clean baseline PPL changes by more than 5% without explanation.
- any JSON lacks seed metadata.
- any run produces NaN/inf PPL.

## Interpretation Rules

- If fresh mean is close to same-instance PPL with low std, HAT learned robust D2D tolerance.
- If same-instance is good but fresh eval degrades sharply, HAT is device-instance-specific.
- If selective last1/last2 remains stable across fresh seeds, selective KV remains the safest deployment narrative.
- If all-layer fresh eval is unstable but selective is stable, paper-2 route should prioritize selective terminal-layer HAT.

