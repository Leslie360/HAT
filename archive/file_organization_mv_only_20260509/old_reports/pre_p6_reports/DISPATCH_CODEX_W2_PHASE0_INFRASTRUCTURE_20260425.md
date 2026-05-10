# DISPATCH CODEX W2 PHASE 0+1 — KV-Cache Analog Infrastructure
**Date:** 2026-04-25 22:55 CST
**Issued by:** Claude
**Assignee:** Codex
**Authority:** CLAUDE_ROUND8_WORK2_LAUNCH_PLAN_20260425 §4-§5
**Priority:** HIGH (Round-8 anchor)
**Time budget:** ~2 weeks (W0: 3 days; W1: 10 days)
**Constraint:** Two-track discipline — pause if 8×40GB cross-arch returns or PhD data lands

---

## 0. Mission

Build the analog CIM infrastructure for transformer attention path + KV-cache, validated end-to-end on Pythia 410M local testbed. This is Phase W0 (testbed lock + scope freeze) + Phase W1 (analog wrapper code + smoke test) of Work 2.

---

## 1. Phase W0 — Testbed pick + architectural scope (Days 1-3)

### 1.1 Testbed lock — Pythia 410M (Claude recommended)

**Default**: `EleutherAI/pythia-410m-deduped` (HuggingFace).

Why:
- 410M params fit comfortably on 16GB local GPU (~5GB peak training)
- 24 layers × 16 heads × 1024 hidden dim → realistic decoder-only architecture
- Pre-trained weights publicly available (Apache 2.0 license)
- Established baseline numbers (perplexity, MMLU) for comparison
- Architecture similar to LLaMA-2 family → scaling story credible

If Pythia proves problematic (license, weights, or unexpected blocker), fallback to `EleutherAI/pythia-160m-deduped`.

### 1.2 Architectural mapping spec

Decide and document each:

| Component | Analog or Digital? | Justification |
|:--|:--|:--|
| Token embedding | Digital | One-time lookup, not MAC-heavy |
| RMSNorm | Digital | Numerically sensitive (paper-1 §3 precedent) |
| Q projection (W_q) | **Analog** | MAC-heavy; this is paper-1's MLP-path analog of attention |
| K projection (W_k) | **Analog** | Same |
| V projection (W_v) | **Analog** | Same |
| Output projection (W_o) | **Analog** | Same |
| **KV-cache storage** | **🔥 Analog (NEW for Work 2)** | The signature contribution: K/V tensors stored as conductance, read with D2D+C2C noise per access |
| Attention softmax | Digital | Numerically sensitive |
| Rotary position embedding | Digital | Trigonometric; numerically sensitive |
| MLP (gate/up/down) | **Analog** | Same as paper-1 |
| LM head (W_lm) | Digital (initial) | Tied to embedding; numerical sensitivity |

**The W_q/W_k/W_v + W_o + MLP analog choice mirrors paper-1.** The KV-cache analog wrapper is the new bit.

### 1.3 KV-cache analog spec

Most novel decision. Two design options:

**Option A — Persistent analog KV-cache:**
- K, V matrices for layer ℓ at decode time → stored as analog conductance G_K^ℓ, G_V^ℓ
- Each token's K/V is "written" once into a row of the analog crossbar
- Each subsequent token's attention reads the stored K/V with D2D + C2C noise per read
- D2D mismatch: per-cell, persistent across reads (mismatch is a static property)
- C2C noise: per-read, fresh sample (cycle-to-cycle randomness)
- Implication: noise grows with read count; long context = more reads = more noise accumulation
- This is the **physically realistic** mapping

**Option B — Digital KV-cache + analog projections:**
- K, V computed digitally and stored in regular memory
- Only Q/K/V/O projections analog
- Simpler, but doesn't really test the KV-cache analog claim

**Decision: Option A.** This is the actual Work 2 contribution. Option B would just be paper-1 extended to attention without the KV-cache novelty.

### 1.4 Benchmark suite

Pick the metrics paper-2 will report:
- **Primary**: WikiText-103 perplexity (single-pass) — baseline LLM eval
- **Secondary**: WikiText-103 with sliding-window decode at varying context lengths {128, 512, 1024, 2048} — KV-cache stress test
- **Tertiary** (optional): MMLU 5-shot accuracy (instruction-following degradation)

Don't overshoot W0 — these are targets for W2/W3, not for W0/W1 smoke.

### 1.5 Acceptance criteria

Phase W0 deliverables:
- `WORK2_TESTBED_DECISION_20260425.md` (testbed lock + justification + license note)
- `WORK2_ARCHITECTURAL_MAPPING_SPEC_20260425.md` (the table above + KV-cache option-A spec)
- `WORK2_BENCHMARK_SUITE_20260425.md` (metrics + datasets)

Time budget: 3 days (writing + decision; minimal compute).

---

## 2. Phase W1 — Infrastructure (Days 4-14)

### 2.1 Code extensions

**New files:**

`paper2/src/analog_kv_cache.py` (or co-locate with `analog_layers_ensemble.py`):
- `AnalogKVCache(layer_idx, head_dim, max_seq_len, sigma_d2d, sigma_c2c, ...)` class
- `.write(token_idx, K_token, V_token)` — store one token's K/V into conductance
- `.read(query_seq)` — fetch full K/V for attention with D2D+C2C noise per read
- D2D mask is per-(layer, position) and persistent for the cache lifetime
- C2C noise is per-read fresh

`paper2/src/llm_hybrid.py`:
- `convert_llama_to_hybrid(model, config)` — analog conversion entry point
- Replaces W_q/W_k/W_v/W_o/MLP with `AnalogLinear` instances
- Wires `AnalogKVCache` into attention path

`paper2/src/train_llm_hybrid.py` (analogous to `train_tinyvit_ensemble.py`):
- Loads Pythia, applies hybrid conversion
- Standard HAT and Ensemble HAT training options
- Per-epoch D2D resampling for Ensemble HAT (same discipline as paper-1)

`paper2/src/eval_llm_kv_cache.py`:
- WikiText-103 perplexity entry
- Sliding-window decode entry
- Fresh-instance eval (10 D2D × 5 MC, similar to paper-1 §5.5)

### 2.2 Smoke tests

Required to pass before W1 closes:
- `tests/test_w2_analog_kv_cache.py` — D2D mask is consistent across reads, C2C is fresh
- `tests/test_w2_llm_hybrid_conversion.py` — Pythia loads, conversion runs, no NaN forward pass
- `tests/test_w2_perplexity_baseline.py` — Pythia FP32 perplexity on WikiText-103 sample matches published baseline (within 5%)

### 2.3 Training infrastructure smoke

- Pythia hybrid training for 100 steps (not full epoch) on a small WikiText-103 slice
- Verify loss decreases
- Verify D2D buffers resample per "epoch" (whatever epoch means in LLM finetune context — say, per 1000-step block)

### 2.4 Phase W1 acceptance criteria

- All 3 smoke tests pass
- 100-step training shows loss going down
- `paper2/src/` is a clean, importable Python package
- Codex writes `CODEX_W2_PHASE1_REPORT_20260425.md` with: code locations, test results, any gotchas, baseline FP32 perplexity number, hybrid-converted FP32 perplexity number (no noise yet), GPU memory footprint

---

## 3. Phase W2 (Days 15-28) — preview

After W1 closes (smoke tests green), Phase W2 fires (separate dispatch when W1 lands):
- Standard HAT vs Ensemble HAT training on Pythia
- Fresh-instance eval (10 instances × 5 MC) on attention path
- Compare degradation patterns to paper-1 MLP-path findings
- First Work 2 results table for paper-2 results.tex

---

## 4. Hard constraints

### 4.1 Two-track discipline (CRITICAL)

| Trigger | Action |
|:--|:--|
| 8×40GB cross-arch returns mid-W1 | PAUSE W1 if it needs Codex bandwidth; help Kimi integrate cross-arch first |
| PhD data lands mid-W1 | PAUSE W1; run R-D0 ingest pipeline ASAP; resume W1 after R-D0 |
| User signals "submit paper-1 now" | HALT W2 immediately; shift to paper-1 finish-line polish |
| W1 hits unsolvable infrastructure blocker | ESCALATE to Claude; do not improvise around it |

Paper-1 readiness comes first.

### 4.2 Code hygiene

- All Work 2 code lives in `paper2/src/` (new dir; doesn't pollute paper-1 root)
- `paper2/` becomes the Work 2 working dir (analogous to `paper/` for paper-1)
- New tests in `tests/` directory (workspace doctrine from cleanup pass 3)
- No commits to paper-1 manuscript files unless cross-arch / measured-D2D triggers fire
- Existing paper-1 code (`analog_layers.py`, etc.) can be IMPORTED but not MODIFIED — Work 2 extends, doesn't fork

### 4.3 GPU usage

- Local GPU only (8×40GB is on independent paper-1 cross-arch task)
- Estimate: W0 = ~0 GPU-h (writing/decisions); W1 = ~4-6 GPU-h (smoke tests + 100-step training); W2 = ~20-30 GPU-h (Standard HAT + Ensemble HAT + fresh-instance eval)
- Reserve 30% of local GPU bandwidth for paper-1 trigger response

### 4.4 Numerical discipline

- Same 4-bit weight quantization as paper-1
- Same canonical noise: σ_C2C = 5%, σ_D2D = 10%
- Same NL = 1.0 canonical
- Same 10 fresh instances × 5 MC for eval
- This keeps Work 2 numerically comparable to paper-1, enabling cross-paper claims

---

## 5. Deliverables summary

| Phase | File | Status |
|:--|:--|:--|
| W0 | `WORK2_TESTBED_DECISION_20260425.md` | NEW |
| W0 | `WORK2_ARCHITECTURAL_MAPPING_SPEC_20260425.md` | NEW |
| W0 | `WORK2_BENCHMARK_SUITE_20260425.md` | NEW |
| W1 | `paper2/src/analog_kv_cache.py` | NEW |
| W1 | `paper2/src/llm_hybrid.py` | NEW |
| W1 | `paper2/src/train_llm_hybrid.py` | NEW |
| W1 | `paper2/src/eval_llm_kv_cache.py` | NEW |
| W1 | `tests/test_w2_*.py` (3 smoke tests) | NEW |
| W1 | `CODEX_W2_PHASE1_REPORT_20260425.md` | NEW |

All status reports append to `report_md/_gpt/AGENT_SYNC_gpt.md`.

---

## 6. Success criteria

- W0 testbed locked, mapping spec written, benchmarks chosen, no surprises
- W1 infrastructure code passes 3 smoke tests, training loss decreases, GPU memory under 14GB (5GB headroom on 16GB)
- Sets up W2 for first real numbers within 4 weeks total

---

## 7. What this dispatch is NOT

- Not a request to start W2 (separate dispatch after W1)
- Not a license to modify paper-1 code (extend, don't fork)
- Not a license to use 8×40GB remote (paper-1 cross-arch owns it)
- Not a license to skip smoke tests for speed

---

## 8. Cold-start refs

- `CLAUDE_ROUND8_WORK2_LAUNCH_PLAN_20260425.md` — master plan
- `CLAUDE_WORK2_DIRECTION_LOCK_20260423.md` — original Work 2 scope
- `DISPATCH_KIMI_W2_OUTLOOK_20260424.md` — earlier outlook framing
- `analog_layers.py` — paper-1 analog primitive (DO NOT MODIFY; reuse via import)

**Time budget: 2 weeks for W0+W1. No deadline. Quality over speed.**
