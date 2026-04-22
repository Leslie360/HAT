# Remote Experiment Queue — 2026-04-21

Purpose:
- Tell the remote GPU server exactly what experiments are worth doing **now**.
- Avoid duplicating the local Round-Q work that is already running.
- Keep the remote side focused on route-finding, not manuscript-grade reproduction.

## Current local authoritative state

What is already authoritative locally:
- `J1d` fresh-instance result: **41.53 ± 8.87%**
- This is the only trustworthy local Round-Q severe-NL result right now.
- It puts the story in the **ambiguous / bimodal** zone, not clean collapse and not clean ceiling-break.

What is already running locally:
- `CX-K2`: N=30 fresh-instance extension for `J1d`
- Therefore the remote server should **not** spend time duplicating `K2` unless explicitly asked later.

What is *not* locally authoritative yet:
- `K3` (`delta_g_eff` sweep)
- `K4` (second-order strength / `alpha` sweep)
- `K5` (third-order STE sanity)

These are the best remote targets.

---

## Priority order for the remote server

### Priority 1 — K3 smoke sweep (run now)

Goal:
- Test whether non-zero `delta_g_eff` improves the second-order STE route enough to matter.

Why this is the best immediate remote task:
- it is directly on the Round-Q mainline
- it does **not** duplicate the local `K2`
- it uses an already-existing code path
- it does not require new pretrained weights

Recommended settings:
- protect group: `mlp`
- surrogate: `second-order STE`
- checkpoint warm-start: `checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- `delta_g_eff` candidates:
  - `0.0`
  - `0.10`
  - `0.25`

Recommended staged protocol:

#### Stage A — quick smoke
- `epochs = 10-15`
- `fresh instances = 3`
- `eval runs per instance = 3`

Decision:
- if all candidates remain clearly `<35%`: stop and report negative
- if any candidate reaches `35-50%`: continue to Stage B
- if any candidate clearly exceeds `50%`: continue to Stage C immediately

#### Stage B — medium confirmation
- only for the best `delta_g_eff` candidates
- `epochs = 50`
- `fresh instances = 5`
- `eval runs per instance = 3`

#### Stage C — full confirmation
- only for the single best candidate
- `epochs = 100`
- `fresh instances = 10`
- `eval runs per instance = 5`

Suggested command template:

```bash
python scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
  --protected-group mlp \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --use-second-order-ste \
  --delta-g-eff <VALUE> \
  --name-suffix _remote_k3_dgeff_<TAG> \
  --mode train \
  --dataset cifar10 \
  --experiments V4 \
  --epochs <EPOCHS> \
  --batch-size 64 \
  --num-workers 0 \
  --device cuda \
  --nl-ltp 2.0 \
  --nl-ltd -2.0 \
  --warm-start-from checkpoints/V4_hybrid_standard_noise_hat_best.pt
```

Important:
- do **not** add `--pretrained`

---

### Priority 2 — K4 alpha sweep (only after K3 smoke shows promise)

Goal:
- Determine whether the benefit from second-order correction is smooth in strength or all-or-nothing.

This requires a small code patch because the current public wrapper exposes:
- `use_second_order_ste`
- `delta_g_eff`

but does **not** yet expose:
- `alpha` scaling for the second-order term

Remote task:
- patch the analog backward path to accept a scalar `alpha`
- then sweep:
  - `alpha = 0.0`
  - `alpha = 0.5`
  - `alpha = 1.0`

Protocol:
- first do a `10-15 epoch` smoke
- only escalate if a candidate looks better than the current local `41.53 ± 8.87%` zone

Interpretation question:
- Is the gain smooth in `alpha`?
- Or is the recovery just noise around one configuration?

---

### Priority 3 — K5 third-order STE sanity (only if K3/K4 still look ambiguous)

Goal:
- Test whether a higher-order correction beyond second-order materially changes the severe-NL story.

This is a code-modifying task.
Do it only if the remote agent is comfortable safely patching `analog_layers.py` / related backward logic.

Protocol:
- smoke first: `10-15 epochs`, `3 fresh × 3 eval`
- only escalate if the smoke is promising

Interpretation question:
- Does third-order meaningfully move the result?
- Or is second-order already the practical ceiling?

---

## What the remote server should NOT run now

### Do not duplicate local K2
- Do **not** rerun the N=30 `J1d` fresh-instance extension right now.
- Local machine is already doing that.

### Do not rerun known-failed attention-side ablations
- `QKV-only`
- `attn_proj-only`
- `full attention-only`

These directions are already sufficiently negative.

### Do not run Tier-2 robustness yet
- `J2` heavy-tailed D2D
- `J3` temperature drift
- `J4` IR-drop geometry

These are rebuttal/robustness assets, not the current mainline.
Only revisit them after the severe-NL surrogate question is resolved.

### Do not run high-cost side quests
- `J5` cadence
- `J6` retention
- `J8` ImageNet-100

These do not answer the current bottleneck question.

---

## What the remote server should return

Return only markdown and key numbers.

Suggested filenames:
- `REMOTE_K3_DGEFF_WAVE1_20260421.md`
- `REMOTE_K4_ALPHA_WAVE1_20260421.md`
- `REMOTE_K5_THIRD_ORDER_WAVE1_20260421.md`

Each markdown report should contain:
1. exact command(s)
2. any code edits as short diff snippets
3. compact result table:
   - config
   - epochs
   - best source-domain acc
   - fresh-instance mean
   - fresh-instance std
4. clear recommendation:
   - `STOP`
   - `PROMISING`
   - `REPRODUCE LOCALLY NEXT`

---

## One-line summary for the remote agent

Run `K3` first (`delta_g_eff` sweep on the second-order MLP-protected severe-NL route), do **not** duplicate local `K2`, and only move to `K4/K5` if `K3` shows a real chance to move the result beyond the current `~41.5%` ambiguous regime.
