# Remote Experiment Batch V3

Date: 2026-04-22
Audience: remote GPU server
Priority: exploration only

## Local authoritative state (do not duplicate)

These are already established locally:
- `K2` authoritative: `38.95 ± 9.85%`
- `K3` complete and negative:
  - best `delta_g_eff = 0.05 -> 36.21 ± 9.61%`
  - no `delta_g_eff` point beats `K2`
- `K4` local authoritative rerun is now in progress:
  - fixed `delta_g_eff = 0.15`
  - `alpha ∈ {0.0, 0.25, 0.5, 0.75, 1.0}`

## Therefore remote should NOT do
- do **not** rerun `K2`
- do **not** rerun `K3`
- do **not** duplicate local `K4` within `alpha <= 1.0`
- do **not** spend time on `QKV-only`, `attn_proj-only`, retention, ImageNet, or unrelated robustness sweeps

---

## Remote task priority

### R1 — K5 third-order STE sanity

**Goal**
Test whether going beyond second-order changes the severe-NL fresh-instance story at all.

**Target lane**
- TinyViT V4
- severe NL (`NL_LTP=+2.0`, `NL_LTD=-2.0`)
- protected group: `mlp`
- warm-start from baseline checkpoint
- fresh protocol: `10 fresh x 5 eval`

**Reference config**
- batch size: `64`
- epochs: `100`
- workers: `0`
- AMP: `on`
- `delta_g_eff = 0.15`
- second-order alpha baseline: `1.0`

**Question to answer**
- Does third-order materially improve over the current local band (`~39%` K2, `~36%` best K3)?

**What counts as interesting**
- `fresh mean > 45%` : notable
- `fresh mean > 50%` : major signal, immediate local follow-up candidate
- `fresh mean <= 43%` : likely negative / saturation evidence

---

### R2 — Second-order overdrive alpha sweep (beyond local K4 range)

**Goal**
Probe whether the missing region is not `alpha in [0, 1]`, but `alpha > 1`.

**Do this only because local K4 is already covering `0.0–1.0`.**

**Sweep**
- `alpha ∈ {1.25, 1.5, 2.0}`
- fixed `delta_g_eff = 0.15`
- all other settings same as R1

**Question to answer**
- Does overdriving the second-order correction lift fresh-instance performance above local `K2 = 38.95 ± 9.85%`?

**Stop rule**
- If all three points are `<= 40%`, stop and do not expand this line.
- If any point is `> 45%`, report it as a real candidate.

---

### R3 — Sparse 2D rescue grid (only if R1 or R2 looks promising)

Run this only if either:
- third-order beats `45%`, or
- an `alpha > 1` point beats `45%`

**Sparse grid**
- best candidate from R1/R2
- `delta_g_eff ∈ {0.05, 0.15, 0.25}`

**Purpose**
Determine whether the gain is robust or just a single-point artifact.

If nothing from R1/R2 exceeds `45%`, skip R3.

---

## Reporting requirements

Return only markdown with:
1. exact command(s)
2. exact code diff(s), if any
3. result table with:
   - method
   - alpha
   - delta_g_eff
   - best source-domain acc
   - fresh mean ± std
   - runtime
4. one-line verdict per method:
   - `worth local reproduction`
   - `not worth local reproduction`
   - `borderline`

## Decision logic

### If remote sees nothing > 45%
Report:
- third-order does not rescue the severe-NL ceiling
- alpha-overdrive does not rescue it either
- current evidence strengthens the basin-instability / structural-limit reading

### If remote sees 45–50%
Report:
- ambiguous but promising
- name the single best configuration for local reproduction

### If remote sees > 50%
Report:
- this is the first genuinely ceiling-breaking candidate
- provide the exact config first, then all supporting numbers

---

## Short instruction

Do `K5` first. Then do `alpha > 1` overdrive. Do not duplicate local `K4 <= 1.0`. Only do the sparse 2D grid if something first clears `45%`.
