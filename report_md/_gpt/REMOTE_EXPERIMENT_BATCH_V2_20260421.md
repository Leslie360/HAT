# Remote Experiment Batch V2 — 2026-04-21

Purpose:
- Give the remote A100 server one clean batch of work.
- Avoid duplicating local runs that are already authoritative or currently active.
- Use the remote side for **route-finding**, not final manuscript-grade confirmation.

---

## 0. Authoritative local state you should assume

Use these as the current local facts:

- `J1d` authoritative local fresh-instance result:
  - **41.53 ± 8.87%**
- `K2` authoritative local N=30 extension:
  - **38.95 ± 9.85%**
  - range: `22.03% – 61.69%`
- Branch interpretation:
  - **Branch C / ambiguous-bimodal**

Local work that is already done or active:
- `K2` is done locally.
- `K3` is being rerun locally right now.

Therefore, on the remote server:
- **Do not rerun `K2`.**
- **Do not rerun `K3`.**

Remote should take the **orthogonal Branch-C follow-up work**:
- `K4` second-order strength (`alpha`) sweep
- `K5` third-order STE sanity
- optional speculative stretch only if both are negative

---

## 1. General rules

1. Remote is doing **exploratory search**, not final paper numbers.
2. Only return:
   - markdown reports
   - key scalar results
   - short code diff snippets
3. Do **not** return big logs/checkpoints unless explicitly requested later.
4. Do **not** spend time on manuscript editing.
5. Do **not** rerun known-negative attention-side lanes:
   - `QKV-only`
   - `attn_proj-only`
   - `full attention-only`
6. Do **not** spend time on:
   - heavy-tailed D2D
   - temperature drift
   - IR-drop
   - retention
   - ImageNet-scale pilots
   unless explicitly unlocked later.

---

## 2. Remote batch to run

### Task R0 — Bootstrap a remote second-order checkpoint if needed

Why:
- The remote repo already has the baseline checkpoint:
  - `checkpoints/V4_hybrid_standard_noise_hat_best.pt`
- But it may not have the local `second_order_ste_best.pt` artifact.
- `K4` and `K5` are easiest to interpret if they start from a remote second-order route.

If the remote repo does **not** already contain a usable second-order checkpoint, first create one.

Recommended training route:
- model family: `TinyViT V4`
- protect group: `mlp`
- protected surrogate NL: `(+1.0, -1.0)`
- global severe NL: `(+2.0, -2.0)`
- enable second-order STE
- warm-start from baseline checkpoint:
  - `checkpoints/V4_hybrid_standard_noise_hat_best.pt`

Command template:

```bash
python scripts/_gpt/run_tinyvit_groupwise_nl_comp.py \
  --protected-group mlp \
  --protected-nl-ltp 1.0 \
  --protected-nl-ltd -1.0 \
  --use-second-order-ste \
  --name-suffix _remote_j1d2_bootstrap \
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
  --warm-start-from checkpoints/V4_hybrid_standard_noise_hat_best.pt
```

Important:
- If `--warm-start-from` is used, **do not** enable `--pretrained`.
- If the wrapper still assumes `pretrained=True`, patch it to `pretrained=False` and load only `model_state_dict`.

Deliverable:
- one markdown note:
  - `REMOTE_R0_SECOND_ORDER_BOOTSTRAP.md`
- include:
  - best source-domain accuracy
  - checkpoint path created
  - whether this route is stable enough to use for K4/K5

---

### Task R1 — K4 second-order strength (`alpha`) sweep

Goal:
- Test whether the gain from second-order correction is smooth in strength, or whether the current result is just one fragile operating point.

Current local status:
- There are old memo-level `K4` numbers in the repo, but they are **not authoritative**.
- Treat `K4` as unresolved.

Required code change:
- Add a scalar multiplier for the second-order term, e.g.:
  - `--second-order-alpha`
- Default should preserve current behavior:
  - `alpha = 1.0`
- Do **not** overwrite the existing second-order path; extend it.

Recommended staged protocol:

#### R1-A — smoke wave
- alpha values:
  - `0.0`
  - `0.5`
  - `1.0`
- epochs:
  - `15`
- fresh instances:
  - `3`
- eval runs per instance:
  - `3`

Decision rule after smoke:
- If all candidates look weak and clustered below the local ambiguous regime, stop.
- If any candidate looks materially better than the current local center (~39–42%), promote.
- If any candidate crosses `50%` even in smoke, promote immediately.

#### R1-B — confirmation wave
Only run this for the best candidate(s).

- alpha values:
  - keep best from smoke; if needed expand to
    - `0.25`
    - `0.75`
- epochs:
  - `50`
- fresh instances:
  - `5`
- eval runs per instance:
  - `3`

Recommended interpretation questions:
- Is the gain smooth in alpha?
- Does reducing or increasing alpha narrow the cross-instance spread?
- Does alpha only shift the mean slightly, or does it change the mode structure?

Deliverable:
- `REMOTE_R1_K4_ALPHA_20260421.md`
- include:
  - exact code diff snippet
  - exact commands
  - compact results table
  - one-line recommendation:
    - `STOP`
    - `PROMISING`
    - `REPRODUCE LOCALLY NEXT`

---

### Task R2 — K5 third-order STE sanity

Goal:
- Test whether going beyond second-order materially changes the severe-NL outcome.

Current local status:
- There are old memo-level `K5` numbers in the repo, but they are **not authoritative**.
- Treat `K5` as unresolved.

Required code change:
- Add a separate third-order path, e.g.:
  - `--use-third-order-ste`
- Keep second-order intact.
- Do **not** replace the current code path.
- A minimal implementation is fine for exploration.

Recommended staged protocol:

#### R2-A — smoke wave
- one configuration only:
  - `third-order`, MLP-protected severe-NL
- warm-start:
  - use the remote second-order bootstrap checkpoint from `R0` if available
  - otherwise use the baseline checkpoint and state that clearly
- epochs:
  - `15`
- fresh instances:
  - `3`
- eval runs per instance:
  - `3`

Decision rule:
- If third-order is clearly no better than the best `K4` candidate, stop.
- If it looks better by a non-trivial margin, promote.

#### R2-B — confirmation wave
Run only if smoke is promising.

- epochs:
  - `50`
- fresh instances:
  - `5`
- eval runs per instance:
  - `3`

Interpretation questions:
- Does third-order actually move the mean?
- Does it reduce variance?
- Or does it simply saturate near the same regime as second-order?

Deliverable:
- `REMOTE_R2_K5_THIRD_ORDER_20260421.md`
- include:
  - code diff snippet
  - commands
  - result table
  - recommendation:
    - `STOP`
    - `PROMISING`
    - `REPRODUCE LOCALLY NEXT`

---

### Optional stretch task R3 — softmax temperature smoothing

Run this **only if**:
- both `K4` and `K5` are clearly negative, and
- the remote side still has idle capacity.

Why this made the cut:
- Gemini's theory memos repeatedly identify attention sharpness / softmax amplification as a plausible unresolved lever.
- This is speculative and **not** part of the current authoritative Round-Q branch.
- Treat it as a pure route-search experiment.

Protocol:
- keep the best currently available severe-NL route fixed
- sweep softmax temperature:
  - `tau = 1.0`
  - `tau = 1.5`
  - `tau = 2.0`
- smoke only:
  - `15 epochs`
  - `3 fresh instances`
  - `3 eval runs`

Deliverable:
- `REMOTE_R3_SOFTMAX_TEMP_20260421.md`
- mark it explicitly as:
  - `SPECULATIVE / NOT AUTHORITATIVE`

---

## 3. Do-not-run list

Do **not** spend remote time on these now:
- `K2`
- `K3`
- `QKV-only`
- `attn_proj-only`
- `full attention-only`
- heavy-tailed D2D
- temperature drift
- IR-drop geometry
- retention
- cadence
- ImageNet-scale pilots

Those are either:
- already local,
- already sufficiently negative,
- or not on the current mainline.

---

## 4. What to send back

Only send back markdown plus tiny diff snippets.

For every task report, include:
1. what you changed
2. exact command(s)
3. key table
   - config
   - epochs
   - best source-domain acc
   - fresh-instance mean
   - fresh-instance std
4. one-line recommendation
5. whether local reproduction is worth doing next

Preferred files:
- `REMOTE_R0_SECOND_ORDER_BOOTSTRAP.md`
- `REMOTE_R1_K4_ALPHA_20260421.md`
- `REMOTE_R2_K5_THIRD_ORDER_20260421.md`
- `REMOTE_R3_SOFTMAX_TEMP_20260421.md` (optional only)

---

## 5. One-line summary for the remote agent

Do **not** duplicate local `K2` or the local `K3` rerun. Use the remote server for the next unresolved Branch-C work: first bootstrap a remote second-order checkpoint if needed, then do `K4` (alpha sweep), then `K5` (third-order sanity), and only if both fail and capacity remains, try the speculative softmax-temperature sweep.
