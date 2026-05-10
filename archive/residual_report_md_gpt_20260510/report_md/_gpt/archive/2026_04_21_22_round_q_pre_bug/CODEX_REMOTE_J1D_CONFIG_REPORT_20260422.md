# J1d / K3 Local Configuration Report for Remote Cross-Check

**Date:** 2026-04-22
**Authoritative scope:** local surviving logs / JSON / source code only
**Purpose:** answer the remote question about why local `J1d` reached `41.53 ± 8.87%` fresh-instance while remote early runs are near chance.

## 0. Historical note

This report reconstructs the **historical canonical local J1d run**.

After the 2026-04-22 local source audit, the local wrapper semantics were corrected:
- `delta_g_eff < 0` now means auto-fill
- `delta_g_eff = 0.0` now means literal zero

So the `--delta-g-eff 0.0` command shown below is a record of the historical run, not the recommended semantics for future reruns.

## 1. Canonical local J1d facts

These are locally verified, not inferred:

- Experiment name: `V4_hybrid_standard_noise_hat_second_order_ste`
- Protected group: `mlp`
- Protected NL: `(NL_LTP, NL_LTD) = (1.0, -1.0)`
- Unprotected global NL: `(2.0, -2.0)`
- Higher-order surrogate: `use_second_order_ste = True`
- `delta_g_eff = 0.0`
- Warm-start: `checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- Dataset: `cifar10`
- Epochs: `100`
- Batch size: `64`
- Learning rate: `5e-4`
- Weight decay: `0.05`
- AMP: `on`
- Best source-domain accuracy: `91.02% @ epoch 78`
- Canonical fresh-instance result: `41.53 ± 8.87%` (`10 fresh instances x 5 MC`)

Primary evidence:
- Training log: `logs/_gpt/cx_j1d_20260421.stdout`
- Training JSON: `report_md/_gpt/json_gpt/second_order_ste.json`
- Fresh eval log: `logs/_gpt/cx_j1d_fresh_eval_20260421.log`
- Fresh eval JSON: `report_md/_gpt/json_gpt/cx_j1d_fresh_eval.json`

## 2. Reconstructed CLI for the canonical local J1d run

The exact live process command line was not preserved verbatim in the surviving training log. The closest authoritative reconstruction comes from:
- the wrapper print in `cx_j1d_20260421.stdout`
- the saved training JSON (`epochs=100`, `batch_size=64`, `lr=5e-4`)
- the local launch template in `report_md/_gpt/GPU_EXTERNAL_TASKLIST_20260421.md`

A faithful reconstruction is:

```bash
python scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
  --protected-group mlp \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --use-second-order-ste \
  --delta-g-eff 0.0 \
  --name-suffix _second_order_ste \
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
  --save-dir checkpoints/_gpt/second_order_ste \
  --log-interval 20 \
  --log-path logs/_gpt/cx_j1d_20260421.log \
  --results-json-path report_md/_gpt/json_gpt/second_order_ste.json \
  --results-csv-path report_md/_gpt/csv_gpt/second_order_ste.csv \
  --results-md-path report_md/_gpt/CODEX_SECOND_ORDER_20260421.md
```

### Important note on `--pretrained`

Older local templates still showed `--pretrained`. Current local policy is:
- if `--warm-start-from checkpoints/V4_hybrid_standard_noise_hat_best.pt` is used,
- do **not** rely on external TIMM pretrained weights.

So for remote parity, the safe reading is:
- **warm-start from the baseline checkpoint is required**
- **external pretrained weights are not**

## 3. First 5 epoch logs for local J1d

This is the key limitation: the surviving local J1d training log was run with `--log-interval 20`, so it does **not** contain per-epoch records for epochs `1..4`.

### What is actually preserved

From `logs/_gpt/cx_j1d_20260421.stdout`:

- Epoch `0/100`
  - `train_loss = 0.3628`
  - `train_acc = 88.05%`
  - `test_acc = 81.86%`
  - `lr = 0.000500`

The next surviving checkpoints are:
- Epoch `19`: `train_acc = 95.81%`, `test_acc = 87.78%`
- Epoch `39`: `train_acc = 97.67%`, `test_acc = 88.56%`
- Epoch `59`: `train_acc = 99.07%`, `test_acc = 89.61%`
- Epoch `79`: `train_acc = 99.77%`, `test_acc = 89.89%`
- Epoch `99`: `train_acc = 99.86%`, `test_acc = 89.49%`

### What is **not** available locally

- Epoch `1`
- Epoch `2`
- Epoch `3`
- Epoch `4`

These were not persisted in the surviving local log.

So the correct conclusion is:
- local evidence supports **epoch 0** and then **epoch 19+**,
- but does **not** support a precise `epoch 1..4` comparison.

## 4. Local DataLoader configuration

Authoritative source: `train_tinyvit_ensemble.py`

### Code behavior

`get_dataloaders()` constructs:

```python
loader_kwargs = {
    "batch_size": batch_size,
    "num_workers": num_workers,
    "pin_memory": resolve_pin_memory(pin_memory_mode),
}
if num_workers > 0:
    loader_kwargs["persistent_workers"] = True
```

Therefore:
- if `num_workers = 0`:
  - `persistent_workers = False` (not set)
- if `num_workers > 0`:
  - `persistent_workers = True`

### Canonical J1d launch interpretation

The surviving launch spec for J1d uses:
- `--num-workers 0`

So the best local reconstruction is:
- `num_workers = 0`
- `persistent_workers = False`
- `pin_memory = auto`

On CUDA, `pin_memory_mode = auto` resolves to `pin_memory = True`.

## 5. Local all-linear source-domain recovery curve

There is a surviving local **all-linear first-order** log:
- `logs/_gpt/train_tinyvit_v4_nl2_all_linear_comp_20260418_144254_queue_all.log`

First 15 epochs from that log:

- Epoch `0/100`
  - `train_acc = 26.59%`
  - `test_acc = 25.04%`
- Epoch `4/100`
  - `train_acc = 49.75%`
  - `test_acc = 52.02%`
- Epoch `9/100`
  - `train_acc = 69.69%`
  - `test_acc = 67.68%`
- Epoch `14/100`
  - `train_acc = 80.14%`
  - `test_acc = 71.33%`

Later milestones:
- Epoch `19`: `81.95%`
- Epoch `59`: `87.49%` best
- Epoch `99`: `84.81%` final

## 6. Important absence: no local surviving all-linear + second-order log

I did **not** find a surviving local artifact for:
- `all-linear + second-order STE`
- `all-linear + delta_g_eff sweep`

So if remote is asking for **"local all-linear + SO2 15-epoch log"**, the correct answer is:
- **there is no authoritative local surviving artifact for that lane**
- the only local all-linear training curve currently available is the **first-order all-linear** lane above

## 7. Most likely causes of the local-vs-remote mismatch

Based on the evidence above, the highest-probability mismatch sources are:

1. **Warm-start mismatch**
   - Local J1d definitely warm-started from `V4_hybrid_standard_noise_hat_best.pt`
   - If remote is effectively cold-starting, early epochs will be dramatically worse

2. **Batch size mismatch**
   - Local canonical J1d used `batch_size = 64`
   - Remote reported `b512` and `b64`; early-epoch dynamics are therefore not directly comparable

3. **Protected-group mismatch**
   - Local J1d is `protected-group = mlp`
   - If remote "SO2" is being applied to attention or globally, that is a different experiment

4. **Fresh-instance vs source-domain confusion**
   - Local `41.53 ± 8.87%` is a **fresh-instance** metric on the best checkpoint
   - It should **not** be compared against remote `epoch 0` source-domain numbers as if they were the same quantity

5. **Missing early-epoch local logs**
   - Local canonical logs do **not** preserve epochs 1–4, so any claim about "local epoch-4 superiority" cannot be made from surviving evidence

## 8. Recommended remote interpretation

Use the following as the local baseline reference:

- Canonical local J1d source-domain training is **strong**:
  - `81.86%` at epoch 0
  - `91.02%` best
- Canonical local fresh-instance transfer is **ambiguous but real**:
  - `41.53 ± 8.87%`
- Canonical local all-linear first-order lane has a standard recovery curve:
  - `25.04% -> 52.02% -> 67.68% -> 71.33%` over epochs `0,4,9,14`
- There is **no** surviving local all-linear + second-order trace to use as a comparator

So the remote side should stop treating `11.54%` vs `41.53%` as a simple random discrepancy and instead check:
- warm-start parity
- batch-size parity
- whether their run is really `mlp-protected second-order`, not `attention-protected` or a different lane
