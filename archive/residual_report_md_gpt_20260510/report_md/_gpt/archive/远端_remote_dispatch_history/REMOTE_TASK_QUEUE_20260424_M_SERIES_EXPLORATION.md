# Remote Task Queue - M-Series Fast Exploration
Date: 2026-04-24
Issuer: Codex
Status: READY TO SEND; DO NOT EXECUTE UNTIL USER RELEASES REMOTE

This packet reconciles two constraints:

- Current coordination says Remote is in holding pattern.
- User wants Remote prepared because 4x A100 can quickly explore once released.

Therefore: prepare the queue now, but Remote should not start until the user explicitly sends this packet and releases the node.

## Preflight Gate R-M0

Before any GPU run, Remote must verify source parity:

- Git source includes the STE branch-mapping fix: positive `grad_output` maps to `ltd_scale`, negative maps to `ltp_scale`.
- Second-order correction has no extraneous outer `nl` multiplier.
- `convert_to_hybrid()` and `convert_resnet_to_analog()` pass `config=copy.copy(config)` for every new analog module.
- `train_tinyvit_ensemble.py` supports `--seed` and writes top-level checkpoint key `"seed"`.
- `eval_fresh_instances_postfix.py` is always called with explicit `--nl-ltp 2.0 --nl-ltd -2.0`.

If any gate fails, stop and report the diff. Do not run GPUs on mismatched source.

## Core Runs

Run these in parallel if all preflight gates pass. Each run is from scratch: no warm-start, no resume.

### R-M1 - Standard HAT V3 True NL=2.0

Purpose: cross-host replicate Codex CX-M1 / local Standard HAT anchor.

```bash
python train_tinyvit_ensemble.py \
  --mode train \
  --experiment V3 \
  --dataset cifar10 \
  --epochs 100 \
  --batch-size 64 \
  --num-workers 0 \
  --device cuda \
  --amp \
  --seed 123 \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --noise-mode uniform \
  --save-dir checkpoints/_gpt/remote_m_series/r_m1_standard_seed123 \
  --log-path logs/_gpt/r_m1_standard_seed123.log \
  --results-json-path report_md/_gpt/json_gpt/r_m1_train_result.json \
  --results-csv-path report_md/_gpt/csv_gpt/r_m1_train_result.csv \
  --results-md-path report_md/_gpt/REMOTE_R_M1_TRAIN_RESULT.md \
  --log-interval 20

python eval_fresh_instances_postfix.py \
  --checkpoint checkpoints/_gpt/remote_m_series/r_m1_standard_seed123/V3_hybrid_standard_noise_standard_train_best.pt \
  --exp-id V3 \
  --model-type tinyvit \
  --device cuda \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --noise-mode uniform \
  --num-instances 10 \
  --mc-runs 5 \
  --output report_md/_gpt/json_gpt/r_m1_fresh_eval.json
```

### R-M2 - Ensemble HAT V4 True NL=2.0

Purpose: cross-host replicate Codex CX-M2 / local Ensemble HAT anchor.

```bash
python train_tinyvit_ensemble.py \
  --mode train \
  --experiment V4 \
  --dataset cifar10 \
  --epochs 100 \
  --batch-size 64 \
  --num-workers 0 \
  --device cuda \
  --amp \
  --seed 123 \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --noise-mode uniform \
  --save-dir checkpoints/_gpt/remote_m_series/r_m2_ensemble_seed123 \
  --log-path logs/_gpt/r_m2_ensemble_seed123.log \
  --results-json-path report_md/_gpt/json_gpt/r_m2_train_result.json \
  --results-csv-path report_md/_gpt/csv_gpt/r_m2_train_result.csv \
  --results-md-path report_md/_gpt/REMOTE_R_M2_TRAIN_RESULT.md \
  --log-interval 20

python eval_fresh_instances_postfix.py \
  --checkpoint checkpoints/_gpt/remote_m_series/r_m2_ensemble_seed123/V4_hybrid_standard_noise_hat_best.pt \
  --exp-id V4 \
  --model-type tinyvit \
  --device cuda \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --noise-mode uniform \
  --num-instances 10 \
  --mc-runs 5 \
  --output report_md/_gpt/json_gpt/r_m2_fresh_eval.json
```

### R-M3 - Proportional HAT V4 True Train/Eval NL=2.0

Purpose: answer whether proportional noise actually beats uniform when trained at true `NL=2.0`.

```bash
python train_tinyvit_ensemble.py \
  --mode train \
  --experiment V4 \
  --dataset cifar10 \
  --epochs 100 \
  --batch-size 64 \
  --num-workers 0 \
  --device cuda \
  --amp \
  --seed 123 \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --noise-mode proportional \
  --save-dir checkpoints/_gpt/remote_m_series/r_m3_proportional_seed123 \
  --log-path logs/_gpt/r_m3_proportional_seed123.log \
  --results-json-path report_md/_gpt/json_gpt/r_m3_train_result.json \
  --results-csv-path report_md/_gpt/csv_gpt/r_m3_train_result.csv \
  --results-md-path report_md/_gpt/REMOTE_R_M3_TRAIN_RESULT.md \
  --log-interval 20

python eval_fresh_instances_postfix.py \
  --checkpoint checkpoints/_gpt/remote_m_series/r_m3_proportional_seed123/V4_hybrid_standard_noise_hat_best.pt \
  --exp-id V4 \
  --model-type tinyvit \
  --device cuda \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --noise-mode proportional \
  --num-instances 10 \
  --mc-runs 5 \
  --output report_md/_gpt/json_gpt/r_m3_fresh_eval.json
```

### R-M4 - Proportional HAT Seed B

Run only if R-M3 fresh mean lands in a plausible useful band, provisionally `>= 75%`.

Same as R-M3, but use `--seed 456` and write to `r_m4_proportional_seed456`.

## Return Package

Remote should return only compact text/JSON evidence:

- exact git commit and dirty diff summary
- source hashes for `analog_layers.py`, `analog_layers_ensemble.py`, `train_tinyvit_ensemble.py`, `eval_fresh_instances_postfix.py`
- exact commands used
- train best accuracy, best epoch, final epoch
- fresh mean/std and all 10 instance means
- paths of logs/checkpoints on Remote
- one-line verdict per run

Do not send large checkpoints unless user explicitly asks.
