# Paper 2 Closure Plan

> Last updated: 2026-05-11
> Target: Complete, reproducible, claim-locked evidence chain for analog KV cache scale-up.

---

## 1. Evidence Chain Architecture

Paper 2 tells one story: **HAT-trained analog KV cache scales from 410M to 6.9B with negligible degradation, outperforming post-hoc quantization, and holds across diverse noise conditions.**

The chain has four links. No link can be missing.

```
Link 1: Method (410M)      Link 2: Scale-up (2.8B/6.9B)    Link 3: Baseline    Link 4: Robustness
     |                              |                              |                  |
  fixed500                       fixed500                    INT8/INT4 RTN      σ sweep
  selective KV                   selective KV                                    D2D seed
  downstream eval                downstream eval                                 mismatch
  claim-lock (DONE)              claim-lock (TODO)                               n_states
```

---

## 2. Dependency Graph & GPU Schedule

```
Day 0 (2026-05-11, NOW)
├── GPU 4/5: 2.8B lm-eval clean/analog          ─┐
├── GPU 6/7: 6.9B lm-eval clean/analog          ─┤  BLOCKING
│                                                  │  (est. 3-4h remaining)
│                                                  │
Day 0+ (lm-eval finishes)                          │
├── GPU 4/5/6/7: robustness sweep auto-start    ◄─┘  (pipeline_robustness_28b_69b.py)
│   ├─ σ_c2c sweep (6 pts × 2 models)
│   ├─ σ_d2d sweep (6 pts × 2 models)
│   ├─ mismatch scenarios (5 pts × 2 models)
│   ├─ D2D seed cross-instance (5 pts × 2 models)
│   └─ n_states sweep (4 pts × 2 models)
│   Est. total: ~52 eval runs. With 4 GPUs @ ~15 min/run ≈ 3-4h
│
├── GPU X (any free): Qwen3-VL validation        (SHORT, ~10 min)
│   └─ clean vs analog generation on single image
│
Day 1
├── Metadata recovery + claim-lock for 2.8B/6.9B downstream & robustness
├── Generate all figures (layer tradeoff, scale-up curve, algorithm bars, heatmap)
├── Update CONCLUSIONS_20260511.md with final numbers
└── Final audit against ARCHIVE_SUBMISSION_PROTOCOL.md
```

---

## 3. Closure Checklist by Link

### Link 1: 410M Method (CLAIM-LOCKED ✅)

| Checkpoint | SHA256 | Eval JSONs | Manifest | Report |
|---|---|---|---|---|
| combined_layerall_v2_seed42 | ✅ | ✅ | ✅ | ✅ |
| combined_layerlast2_v2_seed42 | ✅ | ✅ | ✅ | ✅ |
| 410m_last1_v2_seed42 | ✅ | ✅ | ✅ | ✅ |
| 410m_last4_v2_seed42 | ✅ | ✅ | ✅ | ✅ |

**Missing:** None.

### Link 2: Scale-up (IN PROGRESS 🔄)

| Model | Training | Downstream | Robustness | Claim-lock |
|---|---|---|---|---|
| 2.8B fixed500 | ✅ | 🔄 GPU 4/5 | ⏳ waiting | ❌ |
| 6.9B fixed500 | ✅ | 🔄 GPU 6/7 | ⏳ waiting | ❌ |

**After lm-eval finishes, before robustness sweep starts:**
- [ ] Record checkpoint SHA256 for p28b_fixed500_seed42 and p69b_fixed500_seed42
- [ ] Save lm-eval JSONs with complete metadata envelope
- [ ] Save training commands and git commit hash

### Link 3: Baseline (COMPLETE ✅)

| Model | HAT PPL | INT8 RTN | INT4 RTN |
|---|---|---|---|
| 6.9B | 11.40 | 12.20 | 12.46 |

**Missing:** None. Data already in HAT_Roadmap.md.

### Link 4: Robustness (WAITING ⏳)

| Scan | 410M | 2.8B | 6.9B |
|---|---|---|---|
| σ_c2c sweep | ✅ | ❌ | ❌ |
| σ_d2d sweep | ✅ | ❌ | ❌ |
| Train-eval mismatch | ✅ | ❌ | ❌ |
| D2D seed cross-instance | ✅ | ❌ | ❌ |
| n_states sweep | ✅ | ❌ | ❌ |

**Missing:** All 2.8B/6.9B scans. Pipeline will auto-fill once lm-eval unblocks.

### Link 5: Multimodal Extension (PARTIAL ✅)

| Task | Status | GPU needed | Result |
|---|---|---|---|
| Qwen3-VL model download | ✅ | N/A | 4.0GB cached |
| Clean vs analog generation (all 28 layers) | ✅ | GPU 3 | **Complete degradation** — outputs only "er" |
| Clean vs analog generation (selective last1, layer 27) | ✅ | GPU 3 | **Negligible degradation** — detailed description intact |

**Key finding:** Selective terminal-layer analog KV works for VLM even without HAT training. Full-model analog KV destroys generation quality. This mirrors the language-model trend and strengthens the selective-KV story.

**Open questions:**
- Does HAT training on Qwen3-VL further improve tolerance (allow last2/last4)?
- Are vision features inherently more robust to conductance noise than text embeddings?
- Quantitative metric needed: CLIPScore / LLM-as-judge instead of human eyeballing.

---

## 4. File-Level Action Items

### Immediate (today)
1. **Monitor lm-eval** on GPU 4/5/6/7 until completion.
2. **Compute SHA256** for p28b and p69b checkpoints if not already done.
3. **Ensure pipeline_robustness_28b_69b.py** is alive (PID 3198609). If it dies, restart.
4. **Run Qwen3-VL validation** on the first GPU that becomes free.

### Short-term (tomorrow)
5. **Collect all robustness JSONs** and run metadata recovery script adapted for 2.8B/6.9B.
6. **Generate figures** using completed data.
7. **Update HAT_Roadmap.md** with final downstream numbers.
8. **Write 2.8B/6.9B claim-lock report** following ARCHIVE_SUBMISSION_PROTOCOL.md.

### Audit gate
9. Run `git ls-tree` verification on all new artifact directories.
10. Confirm every manifest row has a matching JSON.
11. Confirm `json.dump` uses `default=str` in all eval scripts (already fixed in f20c0c8).

---

## 5. Risk Register

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| lm-eval crashes again (dtype or OOM) | Low | High | `default=str` already deployed; OOM unlikely at batch_size=1 |
| robustness sweep takes longer than 4h | Medium | Low | Pipeline auto-polls; no manual intervention needed |
| Qwen3-VL eval reveals severe degradation | Medium | High | If so, document honestly; may become a "limitation" paragraph |
| 6.9B checkpoint SHA256 missing | Low | Medium | Compute now and save to memory |
| GPU 2/3 sweep tasks (#54, #55) never ran | High | Low | pipeline_robustness covers same ground; cancel stale tasks |

---

## 6. Reproducibility Contract

Anyone checking out `origin/107-clean` at the final commit should be able to:

1. Re-run any eval from its `command` field in the JSON.
2. Verify checkpoint integrity via `checkpoint_sha256`.
3. Confirm code state via `commit` + `git_status_short`.
4. Reproduce figures from committed data + scripts.

If any step fails, the packet is not closed.
