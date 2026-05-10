# Rebuttal-Ready Table — Unified (K-M + Gemini G-O)

**Date:** 2026-04-19
**Sources:** `KIMI_REVIEWER_OBJECTION_PREP_20260418.md` (Claude pre-draft) + `GEMINI_REVIEWER_PRE_REBUTTAL_20260418.md` (Gemini)
**Purpose:** Single unified table for Round G rebuttal preparation. Deduplicated, prioritized, cross-referenced to manuscript.

---

## Priority Matrix

| Priority | ID | Objection | Category | Source | Manuscript counter | Residual exposure | Pre-emptive patch? |
|:--:|:--|:--|:--|:--|:--|:--:|:--|
| **P1** | R1 | **Task complexity / ImageNet missing** | Evaluation | K-M #1, G-O 3.1 | §1 scopes to edge vision; §4 lists evaluated datasets. | MEDIUM | No — scope is clearly stated |
| **P1** | R2 | **Energy model unvalidated / placeholder** | Framework/Device | K-M #2, G-O 1.3 | §3, §6 repeatedly qualify as "first-order upper bounds"; cover letter same | LOW-MED | S2 already landed |
| **P2** | R3 | **Fixed Gaussian C2C/D2D vs. spatial correlation & heavy tails** | Framework | K-M #5, G-O 1.1 | §6 Limitations explicitly lists; Outlook defers circuit-aware layer | LOW | No — honestly disclosed |
| **P2** | R4 | **NL=2.0 is gradient-scaling approximation, not materials bound** | Device | K-M #3 | §6.5: "limit of this approximation"; Table SX.N localizes to MLP path | LOW | U1 landed in §6.5 |
| **P2** | R5 | **Ensemble HAT lacks external multi-instance baseline** | Framework | K-M #4 | Manuscript presents Ensemble HAT as novel; external multi-instance baseline comparison is response-only | MEDIUM | No — response-only |
| **P3** | R6 | **STE backward surrogate oversimplifies pulse accumulation** | Framework | G-O 1.2 | §3 methodology discloses STE; Table SX.N provides empirical guardrails | LOW | No — supplementary evidence |
| **P3** | R7 | **OPECT calibration constants arbitrary / not representative** | Device | G-O 2.1 | Parameters anchored to Zhang2025; supplementary sensitivity sweep shows insensitivity | LOW | No — already in supp |
| **P3** | R8 | **Cycle endurance ignored** | Device | G-O 2.2 | Response-only; endurance not mentioned in manuscript. | LOW | No — response-only |
| **P3** | R9 | **Temperature dependence ignored** | Device | G-O 2.3, K-M #5 ext | §6 Limitations lists; T-dependence deferred to next phase | LOW | No — honestly disclosed |
| **P4** | R10 | **Best-checkpoint reporting masks instability** | Evaluation | G-O 3.2 | §5.1 explicitly discloses; standard in noisy HAT literature | LOW | No — already disclosed |
| **P4** | R11 | **Fig 4 mixed deterministic/MC bars** | Evaluation | G-O 3.3, D13 | Caption transparently discloses; cost triaged toward Tiny-ViT depth | LOW | D13 response draft landed |

---

## Manuscript readiness per objection

| ID | Ready for reviewer? | Gap |
|:--|:--|:--|
| R1 | ⚠️ | Scope is clearly stated in §1 and §4, but explicit ImageNet deferral remains a response-only clarification rather than a manuscript claim. |
| R2 | ✅ | Caveats repeated 4× (§3, §6, cover letter, supp energy section) |
| R3 | ✅ | Limitations paragraph explicit |
| R4 | ✅ | U1 patch landed; dual-attention-collapse now mentioned |
| R5 | ⚠️ | Internal controls only; no apples-to-apples external multi-instance baseline. Response-side only. |
| R6 | ✅ | STE disclosed in §3; Table SX.N bounds failure modes |
| R7 | ✅ | Sensitivity sweep in supplementary |
| R8 | ⚠️ | Response-only; endurance is not discussed in the manuscript and should not be represented as manuscript-backed. |
| R9 | ✅ | Limitations paragraph explicit |
| R10 | ✅ | §5.1 disclosure explicit |
| R11 | ✅ | D13 pre-rebuttal landed in response draft |

---

## Pre-emptive vs. response-only split

**Pre-emptive patches already landed (no reviewer push needed):**
- S1: Cover letter page count 14→15
- S2: Cover letter contribution count 6→4 (aligned with §1)
- U1: §6.5 dual-attention-collapse tightening
- T1: Response draft gradient-diagnostic vs. training-reality disclosure

**Response-only (wait for reviewer to raise):**
- R5: External baseline demand
- R8: Cycle endurance push
- R1: ImageNet demand (offer pre-registered pilot as commitment)

---

## Honorable mentions (low probability)

| ID | Objection | Why low priority |
|:--|:--|:--|
| H1 | "Why 4-bit quantization?" | ADC sweep (Fig 3, S2) already covers 2–12 bits |
| H2 | "CrossSim gap means your noise model is wrong" | Response draft frames as profile-driven argument, not bug |
| H3 | "Why three datasets?" | CIFAR-10/100 + Flowers-102 covers complexity spectrum |
| H4 | "No measured-device validation" | Explicitly scoped as "prospective simulation" in abstract + cover letter |

---

**Next step:** When Kimi K-N delivers (or is dropped), this table is the authoritative rebuttal prep. No further integration needed unless Gemini G-R or G-S surfaces new objections.
