# Remote Checkpoint Update Guide

Use this guide if the remote GPU agent says the GitHub handoff is missing TinyViT pretrained weights or a baseline checkpoint.

## Recommended policy

Do **not** upload TIMM/TinyViT pretrained weights separately.

Upload **one baseline checkpoint** instead:

- `checkpoints/V4_hybrid_standard_noise_hat_best.pt`

Reason:
- it is enough for the main severe-NL route-finding runs;
- it avoids remote outbound weight downloads;
- it is directly comparable to the current local baseline.

Checkpoint size:
- about `77 MB`
- under GitHub's regular `100 MB` single-file limit

## Exact update commands

Run these commands inside the already-prepared handoff repo:

```bash
cd /home/qiaosir/projects/compute_vit/outputs/remote_github_handoff_20260421_110711/compute_vit_remote_handoff
mkdir -p checkpoints checkpoints/_ensemble
cp /home/qiaosir/projects/compute_vit/checkpoints/V4_hybrid_standard_noise_hat_best.pt checkpoints/V4_hybrid_standard_noise_hat_best.pt
cp /home/qiaosir/projects/compute_vit/checkpoints/V4_hybrid_standard_noise_hat_best.pt checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt
git add checkpoints/V4_hybrid_standard_noise_hat_best.pt checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt
git commit -m "add V4 baseline checkpoint for remote warm-start runs"
git push
```

## What to tell the remote agent

1. Use:
   - `checkpoints/V4_hybrid_standard_noise_hat_best.pt`
   as the default warm-start checkpoint.

2. For any run that uses:
   - `--warm-start-from checkpoints/V4_hybrid_standard_noise_hat_best.pt`
   do **not** require:
   - `--pretrained`

3. If the wrapper still assumes pretrained TIMM weights, patch it so that:
   - the model is created with `pretrained=False`
   - then `model_state_dict` is loaded from the baseline checkpoint

## Minimal remote command example

```bash
python scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
  --protected-group mlp \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --use-second-order-ste \
  --delta-g-eff -1.0 \
  --name-suffix _second_order_ste \
  --mode train \
  --dataset cifar10 \
  --experiments V4 \
  --epochs 50 \
  --batch-size 64 \
  --num-workers 0 \
  --device cuda \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --warm-start-from checkpoints/V4_hybrid_standard_noise_hat_best.pt
```

Deliberately omitted:
- `--pretrained`

## Why two checkpoint paths are included

Some exploratory scripts default to:
- `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt`

Others refer to:
- `checkpoints/V4_hybrid_standard_noise_hat_best.pt`

Putting the same file at both paths avoids unnecessary remote code edits.
