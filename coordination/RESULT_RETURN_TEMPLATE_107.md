# Remote 107 Result Return Template

Use this exact structure when reporting new results back to local/Codex.

## Header

```text
Remote 107 Result Return
Date:
Branch:
Commit SHA:
GPU node:
Python:
PyTorch:
Transformers:
CUDA:
Command launcher:
```

## Code State

```bash
git status --short
git rev-parse HEAD
python -m py_compile deliverable/code/p3_hat_train.py deliverable/code/p3_hat_eval.py pipeline_d2d_seed.py
```

Paste output.

## Commands Run

Paste exact commands, one fenced block per command.

```bash
# command 1
```

## Result Files

List all produced result files.

| file | type | canonical? | notes |
|---|---|---|---|

## Training Checkpoints

| name | train_sigma_d2d | train_sigma_c2c | train_seed | train_d2d_seed | analog_layers | ppl_before | ppl_after | checkpoint_dir |
|---|---:|---:|---:|---:|---|---:|---:|---|

## Fresh D2D Eval Results

| checkpoint | train_d2d_seed | eval_d2d_seed | eval_sigma_d2d | analog_layers | PPL |
|---|---:|---:|---:|---|---:|

## Aggregated Stats

| checkpoint | eval_sigma_d2d | mean PPL | std PPL | min | max | n |
|---|---:|---:|---:|---:|---:|---:|

## Verdict

Write one of:

- `CANONICAL`: result has complete metadata and passed sanity checks.
- `PROVISIONAL`: useful trend but missing some metadata/repeat.
- `INVALID`: do not use.

Then explain why in 3-6 bullets.

## Known Issues

List any code, environment, or runtime issues.

## Next Proposed Run

Give one concrete next task, not a broad wishlist.

