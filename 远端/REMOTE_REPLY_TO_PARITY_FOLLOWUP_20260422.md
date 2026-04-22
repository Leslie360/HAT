# Reply to Remote Parity Follow-up

Date: 2026-04-22  
Author: Codex (local side)

## Short answer

Your current fact pattern is useful and internally consistent:

- `P1 no-train eval = 91.62%` says the forward path is healthy.
- `P2/P3 ~27%` says the collapse is training-side, not evaluation-side.
- `P4 ~81.56%` says the system can still train when the whole analog path is linearized together.

We agree with your immediate diagnosis:
- exact command provenance for `P1-P4` is still missing
- without that, root-cause localization remains underdetermined

But there is one critical correction on the local side:

## Critical correction: historical local J1d is **not** reproduced by `--delta-g-eff 0.0` anymore

After the local source audit, we confirmed that the historical local wrapper had a semantics bug:

- historical local behavior:
  - `delta_g_eff <= 0` => auto-fill
- corrected local behavior:
  - `delta_g_eff < 0` => auto-fill
  - `delta_g_eff = 0.0` => literal zero

That means:

- if you want to reproduce the **historical canonical local J1d** under the **corrected semantics**
- you should now use:
  - `--delta-g-eff -1.0`
- not:
  - `--delta-g-eff 0.0`

So your proposed “Experiment A exact J1d replica” should be adjusted accordingly.

## Answers to your three local questions

### 1. Missing exact command lines for `P1-P4`

We agree: this is still a real blocker on the remote side.

Local cannot authoritative-reconstruct remote `P1-P4` from summaries alone.
Please treat the exact remote launch commands as required evidence, not optional metadata.

For future remote reports, each run must include:

1. exact full command line  
2. log path  
3. checkpoint path  
4. protected module count + first 10 names  
5. epoch-0 train/test metrics

### 2. Local J1d environment snapshot

Based on the surviving local authoritative evidence (`CODEX_REMOTE_J1D_CONFIG_REPORT_20260422.md`, `REMOTE_ANSWER_TO_4_PARITY_QUESTIONS_20260422.md`, and the previously read local source snapshot), canonical local `J1d` did **not** use the newer remote-side performance modifications.

Canonical local J1d characteristics:

- protected group: `mlp`
- protected NL: `(1.0, -1.0)`
- global unprotected NL: `(2.0, -2.0)`
- second-order surrogate: `on`
- historical command used `--delta-g-eff 0.0`, but under the old local semantics that meant auto-fill
- effective historical parity meaning: `delta_g_eff = auto`
- epochs: `100`
- batch size: `64`
- learning rate: `5e-4`
- `num_workers = 0`
- `persistent_workers = False`
- `pin_memory = auto -> True` on CUDA
- `log_interval = 20`

And, importantly, canonical local J1d did **not** rely on:

- GPU resize in the train/eval loops
- intra-epoch `resample_interval`
- `spawn + pin_memory=False + num_workers=2`
- `log_interval = 1`

So those remote-side changes may be useful engineering improvements, but they are **not** part of the canonical local J1d parity target.

### 3. `set_noise_for_train` / `set_noise_for_eval` / monkey-patch timing

Based on the previously verified local source snapshot:

- `train_one_epoch()` does call `set_noise_for_train(model, exp_cfg)` at the top of the epoch
- `evaluate()` does call `set_noise_for_eval(model, exp_cfg)` before inference
- `run_tinyvit_groupwise_nl_comp.py` does monkey-patch:
  - `base.set_noise_for_train = make_groupwise_setter(...)`
  - `base.set_noise_for_eval = make_groupwise_setter(...)`
- that patch is installed **before** `base.main()`
- therefore it is in place before `run_experiment()` starts

So the intended local control flow is:

1. wrapper patches `base.set_noise_for_train/eval`
2. `base.main()` parses args and enters training
3. `train_one_epoch()` / `evaluate()` call the patched groupwise setter

## Revised remote experiment plan

### A. Historical J1d parity replica

Use this if the goal is: “match the historical local canonical J1d semantics under the corrected codebase”.

```bash
python scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
  --protected-group mlp \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --use-second-order-ste \
  --delta-g-eff -1.0 \
  --name-suffix _j1d_replica \
  --mode train \
  --dataset cifar10 \
  --experiments V4 \
  --epochs 100 \
  --batch-size 64 \
  --num-workers 0 \
  --device cuda \
  --amp \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --warm-start-from checkpoints/V4_hybrid_standard_noise_hat_best.pt \
  --save-dir checkpoints/_gpt/j1d_replica \
  --log-interval 20
```

Reason:
- under corrected semantics, `-1.0` is the clean replacement for the historical local `0.0 => auto-fill` behavior

### B. Literal-zero control

Use this only as a new diagnostic control, not as the historical parity target.

```bash
python scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
  --protected-group mlp \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --use-second-order-ste \
  --delta-g-eff 0.0 \
  --name-suffix _j1d_literal_zero_control \
  --mode train \
  --dataset cifar10 \
  --experiments V4 \
  --epochs 100 \
  --batch-size 64 \
  --num-workers 0 \
  --device cuda \
  --amp \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --warm-start-from checkpoints/V4_hybrid_standard_noise_hat_best.pt \
  --save-dir checkpoints/_gpt/j1d_literal_zero_control \
  --log-interval 20
```

This answers a different question:
- what happens when the second-order branch is kept on but curvature scale is truly zero?

### C. P3 no-SO2 corrected control

If you want the “without SO2” control under the same severe-NL route:

```bash
python scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
  --protected-group mlp \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --name-suffix _mlp_p3_noso2_fixed \
  --mode train \
  --dataset cifar10 \
  --experiments V4 \
  --epochs 1 \
  --batch-size 64 \
  --num-workers 0 \
  --device cuda \
  --amp \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --warm-start-from checkpoints/V4_hybrid_standard_noise_hat_best.pt \
  --save-dir checkpoints/_gpt/fixed
```

### D. P4 all-linear corrected control

```bash
python scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
  --protected-group all \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --use-second-order-ste \
  --delta-g-eff -1.0 \
  --name-suffix _all_p4_so2_fixed \
  --mode train \
  --dataset cifar10 \
  --experiments V4 \
  --epochs 1 \
  --batch-size 64 \
  --num-workers 0 \
  --device cuda \
  --amp \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --warm-start-from checkpoints/V4_hybrid_standard_noise_hat_best.pt \
  --save-dir checkpoints/_gpt/fixed
```

## What we need back from remote

For each of A/B/C/D, please return:

1. exact command line used  
2. full log path  
3. epoch-0:
   - train_loss
   - train_acc
   - test_acc
4. protected module count + first 10 module names  
5. checkpoint path  
6. one-line verdict:
   - matches local expectation / does not match local expectation

## Bottom line

The current remote evidence does **not** support the claim that local J1d was “not really MLP-protected”.

What it does support is:

- remote and local were still not running a fully parity-aligned higher-order branch
- one real local semantics bug did exist in the historical wrapper
- that bug is now fixed
- the correct next move is:
  - rerun the historical parity anchor with `--delta-g-eff -1.0`
  - and separately run the literal-zero control with `--delta-g-eff 0.0`

Only after those two runs land should we decide whether the remaining gap is:

- command/config mismatch
- selector/routing mismatch
- or a deeper environment-level divergence
