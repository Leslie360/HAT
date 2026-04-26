# CLAUDE ROUND-11 — Role Reassignment + Outstanding Work Plan
**Date:** 2026-04-26 16:30 CST
**From:** Claude (Chief Architect)
**Trigger:** User: Codex out of credit; DeepSeek (DS) joins as GPU/training executor; Gemini takes plotting; Kimi continues text+audit. Plus: 1 outstanding "CPU-slow comparison" — turned out to be a 5-min Python fix, not a CPU problem.
**Status:** ACTIVE — Round-11 = role re-mapping + fix-it pass + paper-1 finalization

---

## 0. New agent role chart

| Agent | Status | Owns |
|:--|:--|:--|
| **Codex** | ⛔ RETIRED (out of credit) | — |
| **DeepSeek (DS)** | ✅ ACTIVE | GPU training, code, experiments (former Codex GPU work) |
| **Kimi** | ✅ ACTIVE | Text, theory derivations, audits, manuscript edits |
| **Gemini** | ✅ ACTIVE (expanded) | Plotting/figures (DS doesn't render), audits, hostile review, error-finding |
| **Claude** | ✅ ACTIVE | Architect, integration, decisions, light fix-ups |

DeepSeek is invoked via Claude Code subagent like Kimi. Gemini's role expands from "error-finder" to "figures + plotting + audit". Plotting work that was Codex's becomes Gemini's.

---

## 1. R10E AIHWKit baseline — RESOLVED, not blocked

User said "comparison work needs CPU and is very slow" — that was the Round-10 R10E AIHWKit text-fallback fear (4.4d CPU). Reality:

- Kimi found GPU compile path; AIHWKit baseline trained successfully → **best 87.73% at epoch 95**
- Fresh-eval failed on `_pickle.UnpicklingError` (torch>=2.6 weights_only=True default + InferenceRPUConfig not in safe-globals)
- **5-minute fix applied** by Claude: `torch.load(..., weights_only=False)` + `LD_LIBRARY_PATH` for libopenblas
- Fresh-eval relaunched at 16:35; expected ~30-45 min wall-clock for 10 instances on GPU

**No CPU bottleneck. R10E will finish today.**

---

## 2. Outstanding work after R10E lands

Per Claude self-audit (`CLAUDE_PROJECT_SELF_AUDIT_20260426.md`), there are still these issues:

### CRITICAL — paper data integrity
| # | Issue | Status |
|:--|:--|:--|
| C1 | V6 = 95.82% PHANTOM in supplementary L132 (real 82.58%) | ✅ Claude fixed (this round) |
| C2 | Broken refs: `Supp Note S-Verification`, `figS_resampling_cadence`, `tab:r10d-nl-interpolation` cross-doc | ⌛ Kimi |
| C3 | C2C noise mis-classified as "fixed per instance" | ⌛ Kimi |
| C4 | V7 description contradicts (active vs legacy) | ⌛ Kimi |
| C5 | Introduction MLP-path claim invalidated under revised recipe | ⌛ Kimi |

### HIGH — paper structure
| # | Issue | Status |
|:--|:--|:--|
| H1 | Main 16 pages too long (Nat Elec ~8) — move appendix to supp | ⌛ Kimi |
| H2 | Figure numbering discontinuous (1-3/6-9 only in supp) | ⌛ Kimi+Gemini |
| H3 | 6 duplicate labels | ⌛ Kimi |
| H4 | 4 orphan files (08_appendix.tex, S_energy_provenance.tex, S_opect_distribution.tex, S_theory_ensemble_hat_clean.tex) | ⌛ Kimi |
| H5 | `\branchatag` review macro still active in main.tex:25 | ⌛ Kimi |
| H6 | Conclusion 5pp gap statement misses 15pp digital baseline gap | ⌛ Kimi |

### MEDIUM — Work 2 progress
- W2 KV-cache experiments active (LOW_NOISE_LONG_3SEED, FRESH_D2D_ALL_MLP_3SEED, HELDOUT_FRESH_D2D_3SEED, KV_CACHE_OFFLINE_EVAL all reported by Codex/DS recently)
- Continue per Round-8 plan with DS as GPU executor

---

## 3. Round-11 dispatches (issued)

### R11-A — DeepSeek GPU work onboarding
File: `DISPATCH_DS_R11A_GPU_TAKEOVER_20260426.md`
- Take over Codex's GPU dispatch protocol
- Continue Round-8 W2 Phase 2 (Pythia 410M Ensemble HAT training)
- Continue Round-10 R10D NL sweep if any seeds remain
- AIHWKit fresh-eval is currently running (Claude-launched); DS monitors completion + records JSON
- Provenance discipline: every JSON output documents commit_hash + cuda_device + pytorch_version (matching Codex protocol)

### R11-B — Gemini figure rendering pipeline
File: `DISPATCH_GEMINI_R11B_FIGURE_PIPELINE_20260426.md`
- Take over Codex's figure-rendering role (DS doesn't plot)
- Phase-2 mechanism figures + Round-9 TikZ schematics + paper-1 result figures all become Gemini ownership
- New tasks (per H2 audit): regenerate fig 1-3 with consistent main-text presence; resolve orphan fig11_energy_breakdown
- Ongoing audit role unchanged — G-HOSTILE-V2 still gated on R10E + R11 finishing

### R11-C — Kimi text fix-it pass (issues C2-C5 + H1-H6)
File: `DISPATCH_KIMI_R11C_PAPER_FIXIT_20260426.md`
- C2: fix 3 broken cross-references
- C3: rewrite C2C noise classification in §2.1 / §3
- C4: resolve V7 contradiction (mark legacy or remove)
- C5: rewrite Introduction MLP-path claim
- H1: move 08_appendix to supplementary; trim main to ~8 pages
- H3: rename 6 duplicate labels
- H4: delete 4 orphan files OR \input them properly
- H5: remove \branchatag review macro
- H6: extend Conclusion gap statement

### R11-D — Claude integration + R10E final closure
- Monitor R10E fresh-eval (running)
- When done, integrate AIHWKit comparison number into manuscript
- Coordinate with Kimi on R11C fix-it pass
- Trigger Gemini G-HOSTILE-V2 after R11C + R10E land

---

## 4. R10E paper integration (when fresh-eval lands)

Expected outcome of R10E AIHWKit fresh-eval:
- **Outcome A** (most likely): AIHWKit collapses similarly to our Standard HAT (~10% on fresh instance) → strong novelty win, our framework solves what AIHWKit didn't
- **Outcome B**: AIHWKit retains some accuracy on fresh instance (e.g. 60-80%) → moderate novelty, framework still wins on cross-instance robustness
- **Outcome C** (unlikely): AIHWKit matches Ensemble HAT → reframe novelty as substrate-specific

For each outcome, Kimi has the comparison-table template ready (CODEX_R10E_AIHWKIT_BASELINE_REPORT_20260425 §2.3). Claude integrates the actual numbers + paragraph after fresh-eval JSON lands.

---

## 5. Dispatch sequencing

```
NOW:
  Claude: R10E fresh-eval running (8:35 PM-ish landing)
  Claude: V6 PHANTOM fix already applied (this round)
  Kimi: launches R11C fix-it (paper integrity, ~1 day)
  Gemini: launches R11B figure pipeline + standby
  DS: takes over GPU work; monitors AIHWKit fresh-eval completion

+1 day:
  R10E fresh-eval landed; integrated by Claude
  Kimi finishes R11C fix-it pass
  
+2-3 days:
  All paper integrity issues closed
  Gemini figures regenerated for orphan/discontinuous numbering
  Claude triggers G-HOSTILE-V2

+3-5 days:
  G-HOSTILE-V2 audit complete
  Final paper compile + read-through
  Submission-ready (pending PhD defense gate)
```

---

## 6. What's unchanged

- NARRATIVE_PIVOT (zone partition + 3-scenario evidence spine)
- Nature Electronics venue target
- PhD-graduation submission gate
- All numerical claims preserved (V6 PHANTOM was an OUTLIER fabrication, not a claim)
- Round-8 Work 2 launch (DS continues paper-2 GPU work)
- 8×40GB cross-arch independent

---

## 7. Frozen decisions reaffirmed

All 12 frozen decisions in `CLAUDE_FORWARD_ROADMAP §10` still hold. No narrative changes. R11 is presentation + integrity polish + role re-mapping.

---

## 8. One-line

Round-11 = role reassignment (DS=GPU, Gemini=figures, Kimi=text) + 5-min R10E pickle fix (resolved CPU-slow concern) + V6 PHANTOM paper data fix + 11-issue Kimi fix-it pass; submission-ready in 3-5 days pending PhD gate.
