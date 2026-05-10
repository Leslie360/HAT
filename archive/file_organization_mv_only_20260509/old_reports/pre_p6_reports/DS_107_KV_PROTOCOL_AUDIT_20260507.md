# DS-107-A: KV Noise/Retention Code Audit

**Date:** 2026-05-07
**Source:** `docs/data/remote_snapshots_20260507/hat_107_clean/`
**Files audited:** `analog_kv_cache.py`, `analog_layers.py`, `p3_hat_train.py`, `p3_hat_eval.py`, `pipeline_runner.py`, `pipeline_fresh_d2d.py`

---

## Audit Results by Question

### Q1: Does C2C resample per forward pass?

**✅ Yes, confirmed in all 3 code paths.**

- `analog_kv_cache.py` L226-230: `torch.randn_like(k)` inside `read()`, called every forward.
- `analog_layers.py` L591-599: `_scaled_noise_from_reference(is_fixed_pattern=False)` generates fresh noise each forward.
- `p3_hat_train.py` L109-124 (`analogize_kv_tensor`): `torch.randn_like(G_pos)` inside monkey-patched attention forward.

No stale buffer or one-time-initialization issue found.

---

### Q2: Does D2D remain fixed per device instance/checkpoint unless eval seed override is passed?

**✅ Yes, correct behavior.**

- `analog_kv_cache.py` L115-119: D2D buffers initialized once in `__init__` via `register_buffer`, fixed for cache lifetime.
- `analog_layers.py` L439-443: D2D buffer initialized once per `AnalogLinear`, fixed for layer lifetime. `resample_d2d_noise()` available but only called explicitly.
- `p3_hat_train.py` L177-194 (`patch_model_for_hat`): D2D noise generated deterministically from `d2d_seed + layer_idx`, stored as `register_buffer`. Eval override creates entirely new buffers with fresh seed.

**Key finding:** D2D semantics are correct — training fixes one device instance, eval override creates a fresh device instance.

---

### Q3: Are train D2D seed and eval D2D seed semantically separated?

**✅ Semantics correct, but metadata ambiguous.**

- `p3_hat_train.py` L358-360: `--d2d-seed` (default `0xD2D`) controls D2D pattern during training.
- `p3_hat_eval.py` L33-34, 47-60: `--d2d-seed` loads from `hat_config.json` by default, but CLI override creates a different D2D pattern → clean fresh-instance eval.
- `pipeline_fresh_d2d.py` L191-203: explicitly passes `--d2d-seed` to override at eval time.

**But:** Both train and eval JSON output store the value under the single key `"d2d_seed"`. When reading eval JSON, it's impossible to distinguish:
- `train_d2d_seed` = what seed was used during training (from hat_config.json)
- `eval_d2d_seed` = what seed was used for this evaluation

This is a **metadata issue** (handled in DS-107-B), not a protocol issue.

---

### Q4: Does `analog_layers=[23]` only patch the terminal layer?

**✅ Yes, correct.**

`patch_model_for_hat()` in `p3_hat_train.py` L146-148:
```python
target_layers = analog_layers if analog_layers is not None else set(range(num_layers))
...
if layer_idx is not None and layer_idx in target_layers:
    # patch only this layer
```

Pythia-410m has 24 layers (0–23). `analog_layers=[23]` patches only layer 23 = terminal layer.

No off-by-one, no accidental all-layer patch. Verified by the README numbers (last1 PPL 18.42 vs all-layer PPL 26.05 at D2D=0.02).

---

### Q5: Is retention applied in conductance domain or only as output perturbation?

**✅ Conductance domain, correctly.**

All three code paths apply retention decay to `G_pos`, `G_neg` (conductance values), not to output logits:

- `analog_kv_cache.py` L220-223: retention decay applied to cached conductance values before scale recovery.
- `analog_layers.py` L541-561: `G_pos_decayed = G_min + (G_pos - G_min) * decay` — correct.
- `p3_hat_train.py` L86-98: decay applied to `G_pos`, `G_neg` before D2D noise and differential read.

The formula `G(t) = G_min + (G_prog - G_min) * decay` with double-exponential `decay = A1*exp(-t/tau1) + A2*exp(-t/tau2) + A0` is consistent across all three implementations.

---

### Q6: Does the model use the same dataset split for all PPL comparisons?

**✅ Yes, all use WikiText-2 test split.**

- `p3_hat_train.py` L324: `load_dataset("wikitext", "wikitext-2-raw-v1", split="test")`
- `p3_hat_eval.py` (same `evaluate_ppl` function): `split="test"`

The `evaluate_ppl()` function is **shared** between train and eval scripts (eval imports it from train module). No split inconsistency possible.

---

### Q7: Is Base+Patch still close enough to the digital baseline after the SDPA fix?

**⚠️ Cannot fully verify statically. Indirect evidence suggests yes.**

The v2 fresh-D2D pipeline completed 62/62 tasks with these values:
- Last1 digital baseline PPL: from RESULTS_SUMMARY.md, `ppl_before` ≈ 15.68 range
- Last1 with D2D=0.02, 5 eval seeds: mean PPL 18.42 (std 0.02)
- The ~2.7 PPL gap from digital is consistent with 4-bit quantization + D2D noise on one layer

**No obvious bug pattern** (e.g., PPL = 300+ would indicate a broken SDPA implementation). The gap is reasonable for 4-bit analog KV.

**Suggestion:** To fully close this question, run a sanity eval: `Base+Patch` (no noise, n_states=256 or as large as possible) → should be within ~0.5 PPL of digital (15.68).

---

### Q8: Are ctx_len, stride, and full WikiText-2 evaluation consistent across runs?

**✅ Yes, internally consistent. Absolute PPL values use no stride though.**

- `ctx_len` = `max_length` = 512, hardcoded across train, eval, and pipeline scripts. ✅
- `max_tokens=999999` effectively evaluates the full WikiText-2 test set. ✅
- All comparisons use the same `evaluate_ppl()` with `use_cache=False`, non-overlapping windows `range(0, seq_len, max_length)`.

**⚠️ No sliding window/stride.** This is the standard GPT-2 non-overlapping evaluation. All comparisons are internally consistent, but absolute PPL values may differ from `lm-eval-harness` numbers (which use stride=512).

**Recommendation:** Document `stride=None` (non-overlapping) in the canonical metadata so future readers know. If you want lm-eval-harness-comparable numbers, stride=512 would be the standard choice.

---

## Summary Table

| Q | Question | Verdict | Notes |
|---|----------|---------|-------|
| 1 | C2C per forward? | ✅ | `torch.randn_like` on every read |
| 2 | D2D fixed per instance? | ✅ | Buffer init once, eval override creates fresh |
| 3 | Train/eval D2D seed separate? | ✅ sem, ⚠️ meta | Semantics clean; JSON key `"d2d_seed"` ambiguous |
| 4 | `[23]` = terminal only? | ✅ | Only layer index 23, confirmed |
| 5 | Retention in conductance? | ✅ | G_pos/G_neg domain, correct formula |
| 6 | Same dataset split? | ✅ | Shared `evaluate_ppl()`, test split |
| 7 | Base+Patch sanity? | ⚠️ | No bug signs, suggest running sanity check |
| 8 | ctx_len/stride consistent? | ✅ | ctx_len=512 all runs; no stride (internally consistent) |

**Overall:** Protocol is sound. One metadata fix needed (DS-107-B) and one optional base+sanity check (Q7).
