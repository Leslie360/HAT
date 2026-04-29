# Remote 107 KV-Cache Results Review — Selective-Layer Pivot

**Date:** 2026-04-29  
**Reviewer:** Codex  
**Scope:** Remote 107 LLM Analog KV-cache data returned by user.

## 1. Received Core Data

### 1.1 Kill Criterion, seed=42

| Config | PPL | vs digital baseline | Verdict |
|---|---:|---:|---|
| Digital baseline | 15.68 | 1.00x | reference |
| 8-bit all-layer zero-noise | 17.48 | 1.115x | FAIL |

Interpretation: even zero-noise all-layer 8-bit KV cache exceeds the 10% PPL degradation gate. This kills the all-layer route before adding realistic noise.

### 1.2 C2C Sweep, 6-bit, D2D=0, seed=42

| sigma_c2c | 0.0 | 0.005 | 0.01 | 0.015 | 0.02 | 0.03 | 0.05 |
|---|---:|---:|---:|---:|---:|---:|---:|
| PPL | 32.41 | 39.86 | 56.73 | 77.36 | 100.64 | 160.34 | 412.35 |

Interpretation: 6-bit all-layer quantization is already far above baseline even at zero C2C. C2C adds monotonic degradation.

### 1.3 D2D Sweep, 6-bit, C2C=0, seed=42

| sigma_d2d | 0.0 | 0.01 | 0.02 | 0.05 | 0.1 |
|---|---:|---:|---:|---:|---:|
| PPL | 32.41 | 60.30 | 106.48 | 470.92 | 7635.49 |

Interpretation: D2D is much more destructive than C2C for all-layer 6-bit KV cache. Do not spend more GPU on all-layer lower-bit noisy settings.

### 1.4 Selective Layer Probe, 8-bit, seed=42

| Layer scope | Noise | PPL | vs digital baseline | Verdict |
|---|---|---:|---:|---|
| all 24 layers | zero | 17.48 | 1.115x | FAIL |
| layer 23 only | zero | 15.82 | 1.009x | PASS |
| layer 23 only | realistic | 16.72 | 1.066x | PASS |

Interpretation: selective terminal-layer analog KV cache is viable under the current 10% PPL gate. All-layer is not.

### 1.5 HAT Warmup, all-layer, 8-bit, C2C=0.01

| Config | PPL | Loss |
|---|---:|---:|
| pre-HAT | 579.52 | — |
| post-HAT, 50 steps | 142.27 | 7.29 -> 4.41 |

Interpretation: HAT adaptation materially reduces PPL, but all-layer remains far from acceptable after 50 steps. HAT should be moved to the selective-layer path, not used to rescue all-layer.

## 2. Codex Verdict

Remote 107 result changes the Work-2 route:

> All-layer analog KV-cache is rejected. The only viable path is selective terminal-layer KV cache, starting from the last layer and expanding to the last 2/4/6 layers only if the PPL gate remains satisfied. HAT adaptation should be evaluated on selective scopes, not all-layer scopes.

This is now a hard routing decision, not a preference.

## 3. What Can Be Claimed Now

Conservative claim:

> End-to-end LLM KV-cache PPL is extremely sensitive to all-layer analog perturbation. Even zero-noise 8-bit all-layer KV-cache violates the 10% PPL degradation gate, while analogizing only the final layer remains within the gate under realistic noise.

Stronger hypothesis, not yet final:

> Analog KV-cache may be practical only as a selective terminal-layer memory hierarchy, where late-layer KV entries tolerate analog storage better than the full stack.

Do not yet claim last-layer superiority universally until layer-depth and seed repeats are done.

## 4. Immediate Next Tasks For 107

### T107-1: Reproducibility Packet

Return one compact Markdown block with:

```text
git SHA, git diff --stat, exact model/tokenizer, dataset/split, token count,
sliding-window max length, stride, overlap loss accounting, batch size,
transformers/torch/CUDA versions, GPU, dtype, exact commands for the tables above.
```

This is still required before paper use.

### T107-2: Selective Depth Sweep, 8-bit

Run scopes:

```text
last1, last2, last4, last6, last8, all24
```

For each scope:

```text
zero-noise
realistic noise used in the layer23 probe
D2D-only
C2C-only
```

Primary pass criterion:

```text
PPL <= 1.10 * digital_baseline = 17.248
```

Stop expanding depth once two consecutive larger scopes fail under realistic noise.

### T107-3: Selective Depth Sweep, 6-bit

Only run after 8-bit scope is mapped. Use:

```text
last1, last2, last4
```

Run zero-noise first. Only add realistic noise if zero-noise passes the 10% gate.

### T107-4: Selective HAT Warmup

Do not run more all-layer HAT unless explicitly requested. Run HAT only on scopes that are close to or within the gate:

```text
last1 realistic 8-bit
last2 realistic 8-bit
last4 realistic 8-bit, only if last4 is not catastrophically above gate
```

Suggested steps:

```text
0, 50, 100, 200, 500
```

Return PPL after each checkpoint and loss curve.

Kill criteria:

- If a scope is still >1.20x baseline after 200 HAT steps, stop that scope.
- If last1 realistic already passes without HAT, HAT should be used only to recover larger scopes or lower bit-widths.

### T107-5: Seed Repeat For Passing Scope

For the best scope from T107-2/T107-4, repeat seeds:

```text
42, 123, 456
```

Return mean/std PPL and whether the 10% gate is stable.

## 5. GPU Allocation Recommendation

Prioritize 107 GPU time as:

1. 8-bit selective depth sweep.
2. selective HAT warmup.
3. 3-seed repeat for best selective scope.
4. 6-bit selective pilot.

Do **not** run:

- all-layer 6-bit noise sweeps,
- all-layer lower-bit sweeps,
- all-layer HAT beyond the already observed diagnostic,
- retention/material sweeps on all-layer scopes.

Retention/material work should wait until a selective scope passes reproducibly.

## 6. Return Table Format

Ask 107 to return this table:

```text
run_id, seed, model, dataset, baseline_ppl, scope, bit_width, noise_mode,
sigma_d2d, sigma_c2c, hat_steps, ppl, ppl_ratio, gate_pass, command
```

## 7. Broadcast Summary

Remote 107 shows all-layer analog KV-cache fails even at 8-bit zero-noise (`17.48`, `1.115x` baseline), while last-layer-only 8-bit passes both zero-noise (`15.82`, `1.009x`) and realistic noise (`16.72`, `1.066x`). D2D is the dominant failure source in 6-bit all-layer sweeps. HAT helps all-layer but does not rescue it after 50 steps (`579.52 -> 142.27`). Codex decision: abandon all-layer; focus on selective terminal-layer KV + HAT.

## 8. Addendum — Do Not Over-Lock Before HAT Rescue Data (2026-04-30)

User clarified that Remote 107 has evidence that HAT is effective and will return the full validation later. Therefore the route lock is softened:

- **Rejected now:** non-adapted all-layer analog KV-cache and further ordinary all-layer sweeps.
- **Still open:** HAT-rescued all-layer analog KV-cache, pending complete step curve and reproducibility metadata.
- **Still strongest current safe path:** selective terminal-layer KV-cache, especially last-layer-only 8-bit.

Decision rule for the next 107 delivery:

- If HAT-adapted all-layer reaches `PPL <= 1.10x` digital baseline with stable seeds, reopen all-layer as a HAT-dependent route.
- If all-layer remains `>1.20x` after sufficient HAT steps, close all-layer and proceed with selective terminal-layer KV + HAT.
- If selective last2/last4 improves with HAT while all-layer fails, route becomes selective terminal-layer analog KV + HAT.
