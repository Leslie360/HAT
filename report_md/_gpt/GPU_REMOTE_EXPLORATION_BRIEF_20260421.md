# GPU Remote Exploration Brief — 2026-04-21

Purpose:
- This is **not** a full reproducibility handoff.
- The remote server is used only to **search for the best narrative path and the best follow-up experiments**.
- Final paper-grade validation will still be done locally.

Remote constraints:
- Only small markdown/text can be brought back.
- No large checkpoints, logs, or datasets should be assumed transferable.
- Therefore the remote agent should optimize for:
  - information gain
  - branch decision quality
  - identifying promising code paths
  - returning compact markdown summaries only

What the remote agent should return:
- One markdown report per exploration wave
- Each report should contain:
  - exact commands used
  - any code changes as short inline diff snippets or pasted functions
  - a compact result table
  - the recommended next step
  - the narrative implication

Recommended return filename pattern:
- `REMOTE_GPU_EXPLORATION_WAVE<N>_YYYYMMDD.md`

## Core question to answer

We do **not** need the remote server to produce final paper numbers.
We need it to tell us which of these stories is most defensible:

1. **Structural limit story**
- Even stronger surrogates and training tricks do not move severe-NL fresh-instance accuracy much above the `~30%` regime.

2. **Surrogate-limited story**
- First-order gradient scaling is the bottleneck.
- A higher-order surrogate materially lifts severe-NL performance.

3. **Hybrid story**
- Some gains are possible, but only under a narrow mitigation stack.
- The result is not a clean "barrier broken" story, but not a pure structural ceiling either.

## Priority order for remote exploration

### Wave 1 — Highest information gain

Goal:
- Determine whether a higher-order surrogate changes the severe-NL picture enough to alter the narrative.

Explore these variants first:

1. **Second-order STE + MLP linearization**
- This is the direct continuation of current `J1d` logic.
- Interpretation:
  - if it still stays `<35%`, the structural-limit story gets stronger
  - if it lands `35-50%`, we enter ambiguous territory
  - if it exceeds `50%`, the narrative changes materially

2. **Second-order STE + all-linear**
- Tests whether higher-order correction plus full linearization is qualitatively stronger than the current MLP-only route.

3. **Second-order STE + attention-only**
- Use one or both:
  - QKV-only
  - attn_proj-only
- This tells us whether "attention-side collapse" persists even under a stronger surrogate.

Do this as a staged search:
- Stage A: quick triage
  - `10-15 epochs`
  - `3 fresh instances x 3 eval runs`
- Stage B: only for top candidates
  - `50 epochs`
  - `5 fresh instances x 3 eval runs`
- Stage C: only for the best candidate
  - `100 epochs`
  - `10 fresh instances x 5 eval runs`

Report for Wave 1:
- Which candidate is best?
- Does any candidate clearly exceed `35%`?
- Does any candidate clearly exceed `50%`?
- Does any candidate look practically deployment-grade (`>80%`) or is that still unrealistic?

### Wave 2 — Only if Wave 1 is promising or ambiguous

Goal:
- Determine whether more expressive surrogates or warm-start choices change the conclusion.

Explore:

1. **Third-order / cumulant surrogate**
- Only if the remote agent can safely modify the analog-layer backward path.
- This is an exploration task, not a required production implementation.

2. **Warm-start vs cold-start**
- Compare whether the best Wave-1 recipe depends strongly on initialization.

3. **Joint mitigation stack**
- Example:
  - second-order surrogate
  - MLP linearization
  - Ensemble HAT
  - warm-start if helpful

What to decide:
- Is there a realistic path to `>50%` fresh-instance?
- Or are all gains still stuck in the "interesting but non-decisive" zone?

### Wave 3 — Secondary robustness only if the main story is already clear

These do **not** decide the main narrative.
They are useful only after Wave 1 gives a direction.

1. **Heavy-tailed D2D**
- Ask:
  - do heavier tails materially overturn the current D2D robustness story?
  - or do they merely worsen accuracy within the same ranking?

2. **Temperature drift / Arrhenius retention**
- Ask:
  - does temperature mainly shift absolute numbers
  - or does it change the ranking of mitigation strategies?

3. **IR-drop geometry**
- Ask:
  - does geometry create a new dominant bottleneck
  - or is it still secondary to severe write nonlinearity?

## Existing local results the remote agent should treat as priors

Already known:
- `QKV-only linearization` is bad:
  - best about `26.37%`
  - final about `10.18%`
- `full-attention linearization` is also bad:
  - best about `28.09%`
  - final about `9.80%`
- `joint MLP-linear + Ensemble HAT` fresh-instance is still only about `30.53 +/- 7.07%`

Interpretation:
- Pure attention-side fixes have not worked.
- A generic "just add more training" story is not currently supported.
- The remote search should focus on whether a **surrogate-fidelity upgrade** changes that.

## Concrete questions the remote agent must answer

The remote markdown report should explicitly answer:

1. Does second-order STE move the severe-NL fresh-instance result out of the `<35%` zone?
2. If yes, which protection pattern is best:
   - MLP
   - all
   - qkv
   - attn_proj
3. Is the gain large enough to threaten the current structural-limit narrative?
4. If not, what is the next-most-informative follow-up:
   - third-order surrogate
   - heavy-tailed D2D
   - temperature
   - IR-drop
5. Which single experiment should we reproduce locally first?

## Minimal markdown template for the remote server

The remote agent should return something like:

```md
# Remote GPU Exploration Wave 1

## Setup
- branch / commit:
- key code edits:

## Experiments
| ID | recipe | epochs | fresh protocol | best train acc | fresh mean | fresh std | note |
|:--|:--|--:|:--|--:|--:|--:|:--|

## Decision
- best candidate:
- branch classification: `<35` / `35-50` / `>50`
- recommended local reproduction target:

## Narrative implication
- structural-limit strengthened / ambiguous / surrogate-limited

## Code delta
```diff
...short patch snippet...
```
```

## What we do not need from the remote server

Do **not** spend time packaging:
- full checkpoints
- large logs
- publication-ready plots
- LaTeX-ready text rewrites

We only need:
- the best candidate recipe
- the decisive numbers
- the code idea
- the next local reproduction target
