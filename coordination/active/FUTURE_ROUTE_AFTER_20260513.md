# Future Route After 2026-05-13

Date: 2026-05-13 21:20 CST  
Owner: Codex  
Purpose: convert the current mixed post-handoff state into a clear next-step decision tree instead of continuing ad hoc experiments.

## 1. What Is Actually Closed

- **Paper1** is no longer the main expansion lane. Treat it as frozen unless a scoped wording/package issue appears.
- **Paper2 canonical evidence** is still the 410M Remote107 claim-lock packet only.
- **Remote107 p28b/p69b** is still externally blocked from promotion by missing local source-data package closure, and p69b still has the checkpoint-SHA problem.
- **Doctor / measured-profile lane** is already strong enough for candidate-grade thesis/Paper3 evidence.
- **Local architecture-generality lane** is no longer just a single ConvNeXt run:
  - ConvNeXt C4 ranking + topK curve exist.
  - ResNet R4 CIFAR-100 now has:
    - first layer-sensitivity run,
    - second independent D2D-seed replicate,
    - first topK curve,
    - second topK replicate.

This matters because the next GPU job should not be chosen as if the local architecture lane were still empty.

## 2. What Is Not Worth Doing Next

### 2.1 More ResNet/ConvNeXt repeats

Not the best next use of GPU time.

Reason:

- The core conclusion is already stable:
  - ResNet needs a large protection budget.
  - ConvNeXt also benefits from architecture-specific protection.
- Another same-family replicate adds confidence but no new scientific axis.

### 2.2 Local DeiT/Swin expansion right now

Also not the best immediate next lane.

Reason:

- The current reusable analog evaluation harnesses (`load_model_bundle`, fresh-instance eval, sensitivity/topK scripts) support **TinyViT** and **ConvNeXt**, not DeiT/Swin.
- There is a digital DeiT training script, but not a ready analog eval/training path.
- Starting this now would be more infrastructure work than science.

## 3. Best Next GPU Lane

## Decision: drift-aware ranking is now the preferred retention heuristic

The highest-value local direction is now split into two layers:

- **closed heuristic lane**: drift-aware protection ranking for retention/protection
- **next method lane**: drift-aware optimization or SAM-style training

Why:

1. It already produced positive protection results under full `10×3` evaluation.
2. It fits the current codebase better than local DeiT/Swin analogization.
3. It connects directly to the strongest long-term thesis/Paper3/Paper4 story:
   - robustness should be aligned to the **physical drift direction**, not just generic flatness.
4. The prerequisite profiling and ranking artifacts already exist.

This is now the first local lane that has already moved from "more evidence" into "promising mechanism."

## 4. Recommended Priority Order

### P0. External blocker handling

Keep the boundary explicit:

1. Wait for / request Remote107 p28b/p69b source-data package closure.
2. Do not let provisional p28b/p69b rows leak into Paper2 main claims.

### P1. Local GPU immediate

Promote the drift-aware ranking into the default local retention/protection heuristic and close one more checkpoint if GPU time is available.

Target output:

- seed789 full `10×3` confirmation
- seed456 full `10×3` confirmation
- optional seed123 background closure for three-checkpoint coverage

Success criterion:

- the ranking should keep beating or matching the older sensitivity-based heuristic without changing the fresh-all baseline.

### P2. Local GPU after heuristic closure

If the ranking direction stays stable, the next lane is:

- **drift-aware optimization / SAM-style training**

If that is blocked by implementation cost, the fallback lane is:

- **TinyViT / ConvNeXt cross-dataset transfer**, not more same-dataset repeats.

Priority datasets:

1. Flowers-102 if we want low-data boundary stress.
2. TinyImageNet/ImageNet-100 only after checking data + path readiness.

### P3. Local GPU later

Only after P1/P2:

- local KV retention/refresh protocol upgrade for Paper2 engineering evidence,
- or local floorplan/profile-ingestion follow-up if measured-device data arrives.

## 5. Concrete Execution Rule

For the next GPU launch:

- do **not** spend it on another ResNet sensitivity or topK rerun;
- do **not** spend it on local DeiT unless we first wire an analog harness;
- spend it on either:
  - **closing the third drift-aware checkpoint**, or
  - **the first drift-aware optimization pilot**.

## 6. Short Thesis-Level Interpretation

The project is now at a cleaner fork:

- **Paper2 main claim** is bottlenecked by external packaging, not by more local prose.
- **Local GPU value** has shifted from "close architecture gap" to "upgrade the retention mechanism."

So the right move is:

- protect the current Paper2 boundary,
- stop farming low-yield repeats,
- treat drift-aware ranking as the current best heuristic,
- invest the next local GPU wave into a genuinely new robustness mechanism.

## 7. 2026-05-14 Full 10x3 Update

The drift-aware route is no longer just a small pilot. The full seed789 `10×3` confirmation finished at:

- `thesis/results/drift_aware_sam/drift_aware_protection_10x3_summary_20260514_000408.tsv`

Matched against the previous D2D-sensitivity-based `10×3` retention/protection lane:

- `fresh_all_analog` is unchanged to within `0.01 pp`
- `top30` improves by:
  - `+1.38 pp` at `0s`
  - `+1.58 pp` at `1000s`
  - `+1.51 pp` at `10000s`
- `top42` improves by:
  - `+2.70 pp` at `0s`
  - `+2.83 pp` at `1000s`
  - `+2.81 pp` at `10000s`

Interpretation:

- The gain is not a baseline artifact.
- It is strongest for the larger protected set, which is consistent with the drift profile concentrating on late-stage MLP/attention layers.
- The drift-informed ranking is therefore now the most promising protection heuristic in the current local retention lane.

Updated immediate recommendation:

1. finish the same drift-aware route on `seed456` for cross-checkpoint confirmation;
2. if `seed456` agrees, promote drift-aware ranking from pilot to the preferred retention-lane heuristic;
3. only after that, invest in the heavier drift-aware optimization / SAM-style training lane.

## 8. 2026-05-14 Seed456 Confirmation

The second full checkpoint confirmation finished at:

- `thesis/results/drift_aware_sam/drift_aware_protection_seed456_10x3_summary_20260514_003908.tsv`

Key numbers:

- `fresh_all_analog`
  - `63.2940 / 61.2480 / 61.2450` at `0 / 1000 / 10000 s`
- `top30`
  - `65.3847 / 63.3120 / 63.1883`
- `top42`
  - `66.6080 / 64.5563 / 64.4913`

Within the same seed456 checkpoint, this means:

- `top30` stays about `+2.09 / +2.06 / +1.94 pp` above `fresh_all`
- `top42` stays about `+3.31 / +3.31 / +3.25 pp` above `fresh_all`

Interpretation:

- The positive drift-aware direction is no longer a one-checkpoint artifact.
- Seed789 showed that the new ranking beats the older D2D-sensitivity ranking under a matched `10×3` protocol.
- Seed456 shows that the same heuristic remains positive on a stronger checkpoint family and across all tested retention times.

Current recommendation after seed456:

1. treat drift-aware ranking as the preferred local retention/protection heuristic;
2. if one more background closure is desired, run seed123 and stop there;
3. otherwise move directly to a first drift-aware optimization or SAM-style training pilot.
