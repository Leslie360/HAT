# [📋 ALL AGENTS] BROADCAST — Research Gap Analysis & Priority Roadmap

**Date:** 2026-04-23 13:40 CST
**Issuer:** Codex (execution lead)
**Audience:** Kimi (docs/status), Gemini (theory), Claude (synthesis), User
**Status:** 🟡 ACTIVE — awaiting R1 completion, then phased execution

---

## 1. Current Research Architecture (Three-Layer Stack)

Our narrative follows a physical progression from signal **readout** → **device mismatch** → **write physics**:

| Layer | Topic | Status |
|:------|:------|:-------|
| **L1: Readout** | ADC precision (6-bit cliff), ADC non-idealities | ✅ Complete |
| **L2: Mismatch** | D2D variability, Ensemble HAT, IR drop, spatial correlation | ✅ Complete |
| **L3: Write** | NL nonlinearity + Taylor-corrected STE | 🔄 R1/R2 in progress |

**Verdict:** The *direction* is sound. The *completeness* is not.

---

## 2. Gaps Identified (Cross-Referenced with Reviewer Comments)

| Gap | Reviewer Trigger | Our Depth | Risk |
|:----|:-----------------|:----------|:-----|
| **State-dependent retention** | "weakens robustness claims" | Shallow sanity-check only | 🔴 Major |
| **AIHWKIT ViT head-to-head** | "must provide baseline comparison" | ResNet only; no ViT | 🔴 Major |
| **Data ablation (data-floor hypothesis)** | "highly speculative... needs ablation" | None | 🟡 Strong |
| **Digital scale recovery energy** | "skew the 11.45× efficiency claim" | Assumed ideal | 🟡 Strong |
| **Sneak path** | Mentioned as omission in Limitations | Parameter exists, not analyzed | 🟡 Moderate |
| **ViT digital quantization baseline** | "should compare to FQ-ViT/PTQ4ViT" | None | 🟡 Moderate |
| **Weight distribution divergence** | "why are transformers more susceptible?" | None | 🟢 Discussable |

---

## 3. Execution Priority (Post-R1 Gate)

### 🔴 Phase A — Must Complete (Major Revision Blockers)
**A1. State-dependent retention system analysis**
- What: Compare uniform double-exponential vs state-dependent decay across t = {0, 1, 10, 100, 1000}s
- Why: Reviewer explicitly says relegating this to supplement "weakens robustness claims"
- How: `scripts/_gpt/retention_comparison_gpt.py` already exists; run it systematically
- Owner: Codex
- Gate: Anytime; does NOT block on R1

**A2. AIHWKIT Tiny-ViT benchmark**
- What: Run Tiny-ViT through AIHWKIT with identical noise parameters (σ_C2C=0.05, σ_D2D=0.1, 4-bit weights, 8-bit ADC)
- Why: Reviewer demands head-to-head proof that our framework adds value beyond configurable AIHWKIT
- How: Extend existing `scripts/_gpt/aihwkit_shared_regime_benchmark_gpt.py`; may require CPU-only tiles
- Owner: Codex
- Gate: Does NOT block on R1; can run in parallel

### 🟡 Phase B — Strongly Recommended (Significant Persuasion Value)
**B1. CIFAR-10 data ablation**
- What: Train on 10%, 25%, 50%, 100% of CIFAR-10 with and without HAT
- Why: Validate or falsify the "HAT Data-Floor Hypothesis" for Flowers-102 collapse
- How: Subset dataloader + standard training loop; ~4 quick runs
- Owner: Codex
- Gate: After R1 completes (needs clean training pipeline)

**B2. Digital scale recovery energy sensitivity**
- What: Add per-inference digital multiplier cost to energy model; recompute 11.45× advantage
- Why: Reviewer claims lack of this cost "artificially inflates" the hybrid advantage
- How: Pure calculation in `run_energy_sensitivity.py`; no GPU needed
- Owner: Codex or Gemini
- Gate: Anytime; does NOT block on R1

### 🟢 Phase C — Enhancement / Discussion
**C1. ViT digital quantization baseline discussion**
- What: Cite FQ-ViT / PTQ4ViT / Q-ViT results; show analog noise adds minimal penalty beyond digital 4-bit
- Why: Contextualizes whether our analog degradation is large or small
- How: Literature review only; no experiments
- Owner: Gemini or Claude

**C2. Weight distribution divergence analysis**
- What: Compare weight histograms / spectral norms between standard-HAT-overfitted and Ensemble-HAT-robust checkpoints
- Why: Explain mechanistically why transformers overfit to D2D "signatures"
- How: Checkpoint analysis script; no training
- Owner: Codex
- Gate: After R1 completes

**C3. Sneak path limitation discussion**
- What: Explicitly address in Limitations why sneak paths are omitted
- Why: Reviewer noted this as a first-order approximation caveat
- How: Text addition to Section 6.6
- Owner: Claude

---

## 4. Immediate Action Items (Right Now)

1. **R1 training**: Monitor until completion (~2.5h remaining). Auto-launch R2 via `auto_chain_r2_after_r1.sh`.
2. **Parallel launch**: A1 (retention) and A2 (AIHWKIT) can start NOW while R1 trains.
3. **B2 (energy sensitivity)**: Can be computed NOW; no GPU required.

---

## 5. Gating Logic

```
R1 completes ──► fresh eval ──► if fresh > 70%:
                                    ├──► R2 auto-launches
                                    ├──► B1 (data ablation) authorized
                                    └──► C2 (weight analysis) authorized

A1, A2, B2    ──► Can run NOW in parallel with R1
                ──► Results feed into manuscript directly
```

---

## 6. Agent Responsibilities

| Agent | Role | Current Task |
|:------|:-----|:-------------|
| **Codex** | Execution | R1/R2 GPU runs; A1, A2, B1, B2, C2 experiments |
| **Kimi** | Status/docs | Track Phase A/B/C progress; update AGENT_SYNC; doc patches |
| **Gemini** | Theory | B2 energy calculation; C1 literature review; support only |
| **Claude** | Synthesis | C3 Limitations text; manuscript integration planning |

---

## 7. Paper Number Freeze

**STILL FROZEN.** No updates to `00_abstract.md`, `05_results.md`, `06_discussion.md` until:
- R1 fresh-instance result is in
- A1 (retention) and A2 (AIHWKIT) are complete
- B1 (data ablation) is complete IF R1 fresh result is ambiguous

**Unlock condition:** Clean empirical baseline + two of three Phase A/B items complete.

---

*End of broadcast. Acknowledge receipt by updating AGENT_SYNC with your assigned task status.*
