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

## Decision: move to drift-aware optimization pilot

The highest-value next local GPU direction is now:

- **TinyViT V4 / CIFAR-100 drift-aware optimization pilot**

Why:

1. It opens a **new scientific axis**, rather than repeating an old one.
2. It fits the current codebase better than local DeiT/Swin analogization.
3. It connects directly to the strongest long-term thesis/Paper3/Paper4 story:
   - robustness should be aligned to the **physical drift direction**, not just generic flatness.
4. We already have the prerequisite profiling artifact:
   - `thesis/results/drift_aware_sam/drift_vectors_profile_20260512_004906.json`

This is the first local lane that can still move the project from "more evidence" toward "new method".

## 4. Recommended Priority Order

### P0. External blocker handling

Keep the boundary explicit:

1. Wait for / request Remote107 p28b/p69b source-data package closure.
2. Do not let provisional p28b/p69b rows leak into Paper2 main claims.

### P1. Local GPU immediate

Run a **drift-aware optimization pilot** on TinyViT V4 / CIFAR-100.

Target output:

- one small pilot matrix comparing:
  - current baseline checkpoint,
  - a simple flatness/regularization baseline if already cheap enough,
  - a drift-aligned intervention or proxy objective.

Success criterion:

- even a negative result is useful if it shows generic flatness is not enough for physical retention.

### P2. Local GPU after drift pilot

If the drift pilot is inconclusive or blocked by implementation cost, the fallback lane is:

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
- spend it on **drift-aware optimization** if we want the best science-per-GPU ratio.

## 6. Short Thesis-Level Interpretation

The project is now at a fork:

- **Paper2 main claim** is bottlenecked by external packaging, not by more local prose.
- **Local GPU value** has shifted from "close architecture gap" to "open the next method/mechanism gap".

So the right move is:

- protect the current Paper2 boundary,
- stop farming low-yield repeats,
- invest the next local GPU wave into a genuinely new robustness mechanism.
