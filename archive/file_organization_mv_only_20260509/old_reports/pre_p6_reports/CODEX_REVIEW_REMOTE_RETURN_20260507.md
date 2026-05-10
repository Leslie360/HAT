# Codex Review — 2026-05-07 Remote Return + Local Agent Status

## 0. Verdict

**107 is now the strongest active experimental line.** Selective terminal-layer analog KV-cache (`last1`, layer `[23]`) is reproducible across train seeds and fresh D2D seeds. It should remain P0.

**But it is not yet manuscript-lock without two cleanup checks:**

1. Reconcile the digital baseline split: prior documents cite **15.68 PPL**, while K107-B reports **22.18 PPL** under the current evaluator.
2. Separate HAT fine-tuning gain from analog-hardware overhead by evaluating each HAT checkpoint in paired modes: no patch, patch/no-noise, patch/noise.

Paper-1 figure polishing is not the shared-agent bottleneck now. Gemini can continue appendix polish separately. Shared agents should focus on experiment integrity and data packaging.

---

## 1. Local Agent Status

| Agent | Status | Review |
|---|---|---|
| Gemini | Main figures accepted by user; appendix polish ongoing | Main compile has no critical LaTeX errors in `main.log`; appendix remains visual/layout work, not experiment-critical. |
| DS | Completed 107 KV protocol audit, metadata patch design, and EPSC proxy conversion design | Good static review. The EPSC mapping is useful as a stress-test profile, not direct hardware validation. |
| Kimi | Completed local K107-A selective KV run and report | Useful auxiliary check, but not canonical because its PPL scale differs from latest 107 branch results. Use 107 Git branch as canonical. |
| Remote 105 | No new commit beyond Codex task/safety warning | Still waiting for seed789/minimal same-arch TinyImageNet matrix. |
| Remote 107 | New results committed through `origin/107-clean@a5b89be` | Strong signal; needs baseline/provenance cleanup before manuscript use. |

---

## 2. GitHub / Repository Hygiene Check

Checked `origin/107-clean` after fetch.

- Latest commit: `a5b89be remote107: layer-wise analog KV sensitivity sweep`
- No checkpoint-sized files were pushed. Largest files are JSON/code files around 90 KB.
- Codex remote-task commits did not delete files.
- 107 added 1169 small result/script files after the dispatch; this is acceptable for the clean coordination branch.

Checked `origin/105-remote-results`.

- Latest commit remains `e4a14bc remote105: add pull safety warning`
- No new seed789 result has been returned yet.

---

## 3. Remote 107 Result Review

### 3.1 K107-A — Canonical selective KV rerun

Latest 107 branch aggregate, from `deliverable/results_v3/k107_a/summary.csv`:

| Route | Eval D2D | Mean PPL | Std | N |
|---|---:|---:|---:|---:|
| last1 `[23]` | 0.02 | 19.45 | 0.06 | 15 |
| last1 `[23]` | 0.04 | 19.58 | 0.06 | 15 |
| last1 `[23]` | 0.05 | 19.62 | 0.06 | 15 |
| last2 `[22,23]` | 0.02 | 20.14 | 0.05 | 15 |
| last2 `[22,23]` | 0.04 | 20.47 | 0.05 | 15 |
| last2 `[22,23]` | 0.05 | 20.59 | 0.05 | 15 |
| all 24 layers | 0.02 | 37.13 | 0.88 | 5 |
| all 24 layers | 0.04 | 68.48 | 4.33 | 5 |
| all 24 layers | 0.05 | 104.29 | 8.93 | 5 |

**Review:**

- `last1` is stable across train seeds 42/123/456 and eval D2D seeds 42/123/456/789/1001.
- `last1` is consistently better than `last2` by about 0.7-1.0 PPL.
- `all24` is catastrophic and should be treated only as a stress/control anchor, not a fair deployment route.
- This closes Gemini's train-seed variance concern: last1 train-seed variance is far below 0.5 PPL.

**Canonical interpretation:** selective terminal-layer analog KV + HAT is a real route; all-layer analog KV is not.

### 3.2 K107-B — Retention stress

| Route | Eval D2D | Retention step time | PPL |
|---|---:|---:|---:|
| last1 `[23]` | 0.02 | 0 | 19.44 |
| last1 `[23]` | 0.02 | 0.1/1/10 | 19.17 |
| last1 `[23]` | 0.05 | 0 | 19.60 |
| last1 `[23]` | 0.05 | 0.1/1/10 | 19.25 |
| all 24 layers | 0.02 | 0 | 35.81 |
| all 24 layers | 0.02 | 0.1/1/10 | ~176-177 |

**Review:**

- Last1 is retention-tolerant under the current retention model.
- All-layer retention is catastrophic, which strengthens the selective-deployment argument.
- Do **not** overclaim a physical time curve yet: all nonzero step times collapse to nearly identical values because the decay saturates to the persistent fraction. The safe claim is “retention is manageable for last1 under this configured stress,” not “we characterized long-time retention dynamics.”

### 3.3 K107-C — State-count sweep

| n_states | Approx bits | PPL @ D2D=0.02 | PPL @ D2D=0.05 |
|---:|---:|---:|---:|
| 16 | 4-bit | 19.58 | 19.70 |
| 32 | 5-bit | 19.47 | 19.63 |
| 64 | 6-bit | 19.40 | 19.56 |
| 128 | 7-bit | 19.45 | 19.62 |
| 256 | 8-bit | 19.42 | 19.60 |

**Review:**

- Low state counts remain viable; even 16 states is not catastrophic.
- The “64 states sweet spot” should be phrased softly. Differences are around 0.02-0.18 PPL, so this is better framed as “precision beyond 5-6 bits gives negligible return,” not a hard optimum.
- This supports a deployment angle: terminal-layer KV can be analogized at low precision without major loss.

### 3.4 Layer-wise sensitivity sweep

Untrained digital baseline with one analog KV layer at a time:

- Stable shallow plateau: layers 0-10 around 22.2-22.4 PPL.
- High-sensitivity zone: layers 16-19, peak layer 17 at 26.77 PPL.
- Layer 23 raw analog PPL: 23.28; after HAT last1: 19.44.

**Review:**

This is important because it prevents a weak explanation. Layer 23 is not naturally robust. HAT actively compensates terminal-layer analog fragility. That is a stronger mechanism story.

---

## 4. Issues That Must Be Closed Before Manuscript Use

### Issue A — Baseline mismatch

Conflicting baseline values exist:

- 15.68 PPL: cited in prior 107/DS notes as clean or near-clean baseline.
- 22.18 PPL: reported by K107-B digital baseline using current `evaluate_ppl()` path.

Until reconciled, use K107 results as internally consistent **within the same evaluator**, but do not make absolute PPL claims against external benchmarks.

### Issue B — HAT fine-tuning gain vs analog overhead

K107 last1 PPL (~19.45) is lower than the K107-B digital baseline (22.18), which means the checkpoint has a fine-tuning benefit. This is good, but it means the analog overhead cannot be inferred by comparing HAT checkpoint PPL against the untrained pretrained baseline.

Required paired eval for each canonical checkpoint:

1. Same checkpoint, no analog patch.
2. Same checkpoint, analog patch with `sigma_d2d=0`, `sigma_c2c=0`.
3. Same checkpoint, analog patch with `sigma_d2d=0.02/0.05`.

Only this separates fine-tuning, quantization, and physical noise.

### Issue C — Train metadata not fully delivered

The v3 deliverable contains eval JSONs only. Train outputs/checkpoint metadata are referenced through checkpoint paths and launcher code, but not fully shipped as small JSON/MD artifacts.

Also, eval JSON currently has `train_seed: null`; the train seed is recoverable from the checkpoint path but not stored as a first-class field. This is acceptable for interim review, but not for final archive.

### Issue D — Kimi local result scale differs from 107 canonical scale

Kimi local K107-A report shows last1 around 18.3-18.7 PPL, while remote 107 latest canonical branch shows around 19.45-19.62. Do not mix these numbers in one table. Treat Kimi as auxiliary reproduction and 107 branch as canonical until baseline/evaluator differences are resolved.

---

## 5. Next Remote 107 Task Order

### P0 — Baseline reconciliation and paired ablations

Run before any larger exploration.

1. Evaluate pretrained digital baseline using the exact same evaluator used by K107-A/B/C.
2. Evaluate pretrained digital baseline using the old/vectorized evaluator that produced 15.68, if available.
3. For `k107_a1_last1_seed{42,123,456}`, run:
   - no patch / no analog;
   - patch with `sigma_d2d=0`, `sigma_c2c=0`;
   - patch with `sigma_d2d=0.02`, `sigma_c2c=0`;
   - patch with `sigma_d2d=0.05`, `sigma_c2c=0`.
4. Export all train metadata and `hat_config.json` files for K107-A/C checkpoints into `deliverable/results_v3/train_meta/`.

### P1 — EPSC proxy stress eval

Use DS's EPSC proxy mapping as a stress-test profile, not direct hardware validation.

Eval the canonical `last1` checkpoint under:

| ID | sigma_c2c | sigma_d2d | Eval seeds |
|---|---:|---:|---|
| EPSC-e1 | 0.05 | 0.05 | 42, 456, 1001 |
| EPSC-e2 | 0.10 | 0.10 | 42, 456, 1001 |
| EPSC-e3 | 0.15 | 0.15 | 42, 456, 1001 |
| EPSC-e4 | 0.00 | 0.20 | 42, 456, 1001 |
| EPSC-e5 | 0.01 | 0.10 | 42, 456, 1001 |

Kill criterion: if EPSC-e2 exceeds 25 PPL on any eval seed, do not claim EPSC-proxy compatibility; report it as a stress limit.

### P2 — Scale check if GPU remains available

After P0/P1, run a minimal Pythia-1B selective last1 route:

- train seeds: 42 and 123;
- analog layers: terminal layer only;
- eval D2D: 0.02 and 0.05;
- eval seeds: 42, 456, 1001.

Purpose: check whether the selective terminal-layer result scales beyond 410M.

---

## 6. Next Local/Agent Task Order

1. **Kimi:** Do not duplicate 107 GPU experiments locally unless remote is unavailable. Focus on collation, consistency tables, and making sure returned JSON/CSV are copied into stable local snapshots.
2. **DS:** Audit baseline reconciliation and paired-ablation scripts before/after 107 runs. Pay special attention to evaluator stride, dataset split, and whether no-patch truly bypasses analog KV.
3. **Gemini:** Continue appendix figure polish separately. If doing experiment review, focus only on whether P0 paired ablations close the manuscript logic gap.
4. **Codex:** Own remote-task GitHub coordination, result review, and canonical-number arbitration.

---

## 7. Current Route Decision

- **LOCK as active route:** 107 selective terminal-layer analog KV-cache.
- **Provisional narrative:** HAT enables terminal-layer analog KV by compensating a layer that is otherwise fragile; last1 is robust across D2D seeds and low state counts.
- **Not locked yet:** absolute PPL numbers, fine-tuning-vs-hardware decomposition, and EPSC-proxy compatibility.


---

## 8. Late Remote 107 Updates Reviewed After Initial Draft

Remote 107 pushed two additional commits while this review was being written:

- `4a0920c remote107: C2C baseline eval + Pythia-1B eval launcher`
- `d28da30 remote107: Pythia-1B last1 validation results`

### 8.1 C2C baseline eval

For `k107_a1_last1_seed42`, D2D=0.02:

| C2C | Mean PPL | Delta vs C2C=0 baseline |
|---:|---:|---:|
| 0.00 | 19.44 | baseline |
| 0.01 | 19.46 | +0.01 |
| 0.02 | 19.51 | +0.07 |

**Review:** moderate C2C is not the bottleneck for this last1 route. This supports the earlier view that D2D/fresh-instance and retention are the harder risks. It does **not** close EPSC-proxy stress, because DS's central EPSC proxy is closer to `sigma_c2c=0.10`, `sigma_d2d=0.10`.

### 8.2 Pythia-1B last1 validation

Pythia-1B, terminal layer `[15]`, train seed 42, D2D train=0.02:

| Eval D2D | Mean PPL | N |
|---:|---:|---:|
| 0.02 | 14.59 | 3 |
| 0.05 | 14.80 | 3 |

Reported digital baseline: 17.82 PPL; post-HAT train PPL: 14.60.

**Review:** this is a strong scale-up signal. It suggests selective terminal-layer analog KV may improve with model scale. However it is still **provisional** because:

1. only train seed 42 is reported;
2. the PPL improvement vs digital baseline again mixes HAT fine-tuning gain with analog/noise effects;
3. no paired no-patch / patch-no-noise / patch-noise decomposition has been returned.

**Decision:** Keep Pythia-1B as P1-scale evidence, not final manuscript-lock evidence, until the paired ablation protocol is completed.
