# Remote105 Extra ViT Seed Proposal

Date: 2026-05-11  
Branch: `105-remote-results`

| Task | Status | GPU-hours | Changed locked claim? | Verdict |
|---|---:|---:|---:|---|
| 105-E3: extra ViT seed proposal | Proposed only | ~21 | Only if the new seed materially favors digital | Hold by default; run only if local team or review requests more ViT variance coverage |

## Why This Is The Only Worthwhile Extra Run

Current locked state:

- DeiT proportional beats digital in all 3 tested seeds.
- ViT proportional beats digital in 2/3 tested seeds and is positive on average (`+1.35pp` fresh).
- The only unresolved experimental question is whether `vit_small_patch16_224` has enough seed variance that the `seed456` digital outlier should materially weaken the provisional cross-architecture label.

This proposal targets that question only. It does not reopen DeiT, negative controls, or manuscript framing.

## Proposed Scope

Run exactly one new ViT seed pair:

- `vit_small_patch16_224` + `digital` + `seed=2025`
- `vit_small_patch16_224` + `proportional` + `seed=2025`

Then run fresh-instance eval on both best checkpoints using the same `10 instances x 5 MC runs` protocol.

Do not run:

- DeiT
- `ensemble`
- `standard`
- additional seeds beyond `2025` unless the result is clearly adverse to proportional

## Exact Commands

```bash
cd original_repo

conda run -n hat python -u train_vit_tinyimagenet.py \
  --arch vit_small_patch16_224 \
  --hat-type digital \
  --epochs 100 --batch-size 512 --lr 0.002 --warmup-epochs 5 \
  --seed 2025 --device cuda:{gpu_id} --amp --pretrained \
  --data-root ../data/tiny-imagenet-200 \
  --save-dir checkpoints/_gpt/cross_arch_tinyimagenet

conda run -n hat python -u train_vit_tinyimagenet.py \
  --arch vit_small_patch16_224 \
  --hat-type proportional \
  --epochs 100 --batch-size 512 --lr 0.002 --warmup-epochs 5 \
  --seed 2025 --device cuda:{gpu_id} --amp --pretrained \
  --data-root ../data/tiny-imagenet-200 \
  --save-dir checkpoints/_gpt/cross_arch_tinyimagenet

conda run -n hat python -u eval_fresh_instances_vit.py \
  --checkpoint checkpoints/_gpt/cross_arch_tinyimagenet/vit_small_patch16_224_digital_seed2025/best.pt \
  --device cuda:{gpu_id} \
  --output results/json/vit_small_patch16_224_digital_seed2025_best_fresh_eval.json

conda run -n hat python -u eval_fresh_instances_vit.py \
  --checkpoint checkpoints/_gpt/cross_arch_tinyimagenet/vit_small_patch16_224_proportional_seed2025/best.pt \
  --device cuda:{gpu_id} \
  --output results/json/vit_small_patch16_224_proportional_seed2025_best_fresh_eval.json
```

Notes:

- If two GPUs are free, run the two training jobs concurrently to reduce wall-clock time.
- Training has no resume support; a killed run restarts from epoch 0.

## Expected Cost

- Estimated total cost: `~21 GPU-hours`
- Expected wall-clock: about one overnight slot if digital and proportional run in parallel on separate GPUs
- Eval cost is small relative to training and does not change the order-of-magnitude estimate

## What Conclusion This Run Can Change

This run can change only the ViT confidence level.

If `seed2025` shows `proportional >= digital` on fresh eval:

- keep the current manuscript boundary;
- strengthen the ViT story from "provisional but noisy" toward "provisional with one more supporting seed";
- stop further Remote105 work unless a reviewer requests more.

If `seed2025` shows `digital > proportional` again by a clear margin:

- keep DeiT unchanged;
- keep proportional's cross-instance-stability claim unchanged;
- consider exactly one more ViT seed before changing the cross-architecture confidence label.

This run cannot overturn:

- the DeiT result;
- the negative-control result (`standard` collapse);
- the conclusion that proportional has low fresh degradation on tested checkpoints.

## Recommendation

Do not start this run by default. Keep it as a prepared response if:

- the local team wants one more ViT seed before freezing manuscript text; or
- review explicitly asks for more seed coverage on ViT.
