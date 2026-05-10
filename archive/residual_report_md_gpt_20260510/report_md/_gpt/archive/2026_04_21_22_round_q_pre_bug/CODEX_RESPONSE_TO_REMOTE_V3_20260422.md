# Codex Response to Remote V3 Summary

Date: 2026-04-22
Audience: remote GPU team
Purpose: clarify what is already informative in the Remote V3 summary, what is still not parity-comparable, and what exact next run is needed.

---

## 1. High-level assessment

Your V3 summary is valuable. It suggests there may be a genuinely useful new line here:
- **intra-epoch D2D resampling** (`r50`, `r10`) may be improving fresh-instance transfer far more than the current local Branch-C line.

That said, the current V3 table is **not yet a clean parity table** against local `J1d`. It mixes three things together:

1. **baseline parity checking**
2. **bug fixes / runtime fixes**
3. **new algorithmic changes** (`resample_interval`, possible MC policy changes)

So we should treat V3 as a **promising exploratory result**, not yet as a direct contradiction of local `J1d`.

---

## 2. What is already established locally

### Local authoritative references

#### Local `K2` / canonical `J1d` follow-up
- `38.95 ± 9.85%`
- protocol: `30 fresh instances x 5 eval runs`
- this is the current authoritative local severe-NL second-order result

#### Local `K3` (`delta_g_eff` sweep)
- `0.05 -> 36.21 ± 9.61%`
- `0.10 -> 30.79 ± 11.59%`
- `0.15 -> 27.85 ± 7.37%`
- `0.20 -> 33.25 ± 10.29%`
- `0.25 -> 30.08 ± 9.07%`
- conclusion: **no `delta_g_eff` point beats local `K2`**

#### Local `J1d` early source-domain reference
- surviving epoch-0 log:
  - `train_acc = 88.05%`
  - `test_acc = 81.86%`
- local source-domain training for this branch is therefore clearly not in the `~10–30%` regime at epoch 0

#### Local code fact that matters a lot
In the local code:
- `NL_LTP / NL_LTD / use_second_order_ste / delta_g_eff` affect the **backward surrogate**
- they do **not** alter the quantizer forward value inside `STE.forward()`

That means a large epoch-0 source-domain mismatch is unlikely to be explained by “second-order curvature” alone. It usually points to one of:
- different checkpoint
- different warm-start logic
- different module matching / protected-group routing
- different forward-path code
- different training metric definition

---

## 3. What in V3 is scientifically interesting

Your table:

| Config | Source | Fresh (single) | Notes |
|--------|--------|---------------|-------|
| SO2 baseline 15ep | 85.80% | 20.99% ± 4.28% | per-epoch resample |
| SO3 50ep | 89.07% | 42.62% ± 5.65% | per-epoch resample, 3rd-order |
| SO2 + r50 50ep | 89.51% | 48.61% ± 7.85% | resample every 50 batches |
| SO2 + r10 50ep | 86.17% | 50.19% ± 7.05% | resample every 10 batches |
| r10 best instance | — | 58.77% | instance 1 |
| K5 MLP SO3 | 27.39% | — | structural dead end |

### My current read

#### 3.1 The strongest signal is **not** SO3 alone
The strongest signal is:
- `SO2 + r50 -> 48.61 ± 7.85%`
- `SO2 + r10 -> 50.19 ± 7.05%`

If these hold, the interesting mechanism is not “third-order fixes everything”, but:

> **more aggressive intra-epoch D2D domain randomization may be the thing that actually lifts fresh-instance transfer.**

That is scientifically important.

#### 3.2 Longer training matters, but does not by itself resolve the parity issue
Your comparison:
- `SO2 baseline 15ep -> 20.99%`
- `SO3 50ep -> 42.62%`

shows that more training clearly helps.

But this is **not yet parity-comparable** to local `J1d`, because local `J1d` was not a `15ep` run. So the `20.99%` row should not be read as “remote reproduced local baseline and got 20.99 instead of 41.53”. It did not yet establish that.

#### 3.3 “MLP-protected = structural dead end” is not yet established from this table alone
Your last row:
- `K5 MLP SO3 = 27.39%`

is interesting, but currently under-specified.

Locally, MLP-protected second-order severe-NL did **not** look like a total source-domain dead end. So before we accept that row as decisive, we need the exact protocol and metric definition.

---

## 4. Why V3 is not yet a clean parity comparison

The biggest issue is that several changes happened at once.

You list these code changes:
1. `delta_g_eff=0.0` override fix in `make_groupwise_setter`
2. `"conv"` layer misclassification removal
3. DataLoader fork+CUDA deadlock fix (`spawn + pin_memory=False`)
4. GPU resize optimization
5. `--resample-interval` intra-epoch D2D randomization

These are not all the same type of change.

### 4.1 Runtime fixes vs scientific changes

#### Mostly runtime / engineering
- DataLoader spawn fix
- `pin_memory=False`
- GPU resize optimization

These mainly affect stability/speed.

#### Scientifically material
- `delta_g_eff=0.0` override fix
- removing wrong `conv` analog matching
- adding `resample_interval`

Those can absolutely change the training dynamics and final fresh-instance behavior.

So at this point, V3 should be interpreted as:

> a new experimental branch with several meaningful code-path differences,

not as:

> a simple rerun of the local canonical `J1d`.

---

## 5. The most important unresolved contradiction

The most important contradiction is still this:

- **Local J1d epoch 0:** `train 88.05 / test 81.86`
- **Remote MLP b64 epoch 0:** `train 27.37 / test 10.86`

That gap is too large to attribute to randomness.

This means the remote run is almost certainly **not functionally equivalent** to the local run, even if the user-facing label says “MLP-protected, batch64”.

Given the local code, the most likely causes are:
1. checkpoint mismatch
2. warm-start not actually loading the same way
3. protected-group routing mismatch
4. forward-path module matching difference (your `conv` fix may be exactly this)
5. local `delta_g_eff=0.0` meaning “auto -> 0.15”, while remote may now mean literal zero

That fifth point matters a lot.

### Important local detail
In the local wrapper, when `use_second_order_ste` is on and `delta_g_eff <= 0`, the code auto-populates:
- `delta_g_eff = sigma_d2d + sigma_c2c`
- effectively `0.10 + 0.05 = 0.15`

So if your “fixed” remote branch now treats `delta_g_eff=0.0` as a literal zero instead of an auto-fill to `0.15`, then the remote “baseline” is **not the same experiment** as the local canonical second-order run.

That alone could explain a major part of the parity gap.

---

## 6. What I think V3 actually means right now

My current interpretation is:

### 6.1 There are two separate stories in your results

#### Story A: parity is still unresolved
The `epoch-0` mismatch says the remote baseline still does not line up with the local canonical branch.

#### Story B: a new algorithmic branch looks promising
The `r50` and `r10` results suggest that **frequent D2D resampling during training** may be a real way to improve fresh-instance transfer.

These are both important, but they should not be conflated.

### 6.2 The most promising line is **domain randomization frequency**, not third-order alone
If I had to prioritize based on V3 only, I would say:

1. `resample_interval` is the most interesting new idea
2. third-order is secondary
3. the real question is whether the gain survives once the parity baseline is truly aligned

In other words:

> V3 currently looks more like a **domain-randomization breakthrough hypothesis** than a pure **higher-order-surrogate breakthrough hypothesis**.

---

## 7. What I need next from the remote side

I do **not** need a giant rerun matrix yet. I need one clean disentangling step.

### Required next run: one true parity anchor
Please run **one anchor experiment** that is as close as possible to the local canonical branch:

- TinyViT V4
- MLP-protected
- second-order only
- `batch_size = 64`
- `epochs = 100`
- same warm-start checkpoint
- per-epoch resample only
- no `r10`
- no `r50`
- no third-order
- and most importantly: **state explicitly whether `delta_g_eff=0.0` means literal zero or auto-filled `0.15`**

I need the result of that one anchor before I treat the rest of the V3 table as parity evidence.

### After that, one clean ablation ladder
Once the anchor is aligned, the next useful ladder is:

1. parity anchor (`SO2`, per-epoch, 100ep)
2. same + `r50`
3. same + `r10`
4. same + `SO3`

That will let us separate:
- training-length effect
- randomization-frequency effect
- surrogate-order effect

---

## 8. What you should report back in the next message

For the next remote update, please give me exactly this table:

| Run | SO2/SO3 | alpha | delta_g_eff | resample interval | epochs | batch | warm-start ckpt | source best | fresh mean ± std |
|--|--|--|--|--|--|--|--|--|--|

And below it, explicitly state:

1. whether `delta_g_eff=0.0` was interpreted as literal `0.0` or auto `0.15`
2. whether the `conv`-matching fix was active
3. whether `gpu_resize` was active
4. whether `Fresh(single)` means:
   - one eval per instance, or
   - cross-instance mean over 10 instances with one eval each, or
   - something else

---

## 9. Bottom line

My bottom-line read of V3 is:

- **Promising:** `r50` / `r10` may be real and important.
- **Not yet parity-clean:** the remote baseline still does not line up with the local canonical `J1d` branch.
- **Most likely next paper-worthy mechanism:** domain-randomization frequency, not third-order alone.
- **Immediate next need:** one clean parity anchor, then one ablation ladder.

So my recommendation is:

> Do not expand the grid yet. First give me one true parity anchor and one small ablation ladder that isolates `resample_interval` from surrogate order.
