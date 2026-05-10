# Rebuttal Coverage Audit — Manuscript vs. REBUTTAL_READY_TABLE_20260419

**Date:** 2026-04-19
**Auditor:** Kimi Code CLI (subagent)
**Scope:** Main manuscript (`main.tex` + sections) + cover letter + supplementary (`supplementary.tex`)
**Method:** Line-level verification of every claim in the "Manuscript counter" column of the rebuttal table.

---

## Executive Summary

| Category | Count |
|:--|:--:|
| Fully supported by manuscript | 8 / 11 |
| Partially supported / overclaimed | 1 / 11 (R1) |
| Not supported — response-only gap | 2 / 11 (R5, R8) |

**Critical finding:** Two objections (R5, R8) rely on language that **does not exist** in the manuscript. The rebuttal table incorrectly marks R8 as "✅ Ready." R1 contains a minor overclaim about §6 deferring ImageNet.

---

## Detailed Audit Table

| Objection ID | Manuscript support? | Location (file/section) | Gap (if any) | Recommendation |
|:--|:--|:--|:--|:--|
| **R1** — Task complexity / ImageNet missing | **Partial** | §1 Introduction (line 19): scopes to "edge-vision accuracy"; §4 Experimental Setup lists actual datasets (CIFAR-10/100, Flowers-102). | The rebuttal table claims "§6 defers ImageNet." **This is not in the manuscript.** §6.3 discusses "Task Complexity and Data Starvation" and mentions Flowers-102 as the "low-data extreme," but never names ImageNet or says it is deferred. The "cost argument" is also not in the manuscript. | Downgrade readiness from ✅ to ⚠️. Response should anchor on §1 "edge vision" scope + §4 dataset list. Do not cite §6 as deferring ImageNet. |
| **R2** — Energy model unvalidated / placeholder | **Yes** | §3.4 Sensitivity and Energy Metrics (line 89): "first-order analytical model... intended for relative comparison rather than routed-circuit prediction"; §6.4 (line 38): "system-level upper bounds under placeholder constants, not chip-predictive estimates"; §6.5 Limitations (line 43): "Energy parameters are placeholders"; Cover letter (line 26): "first-order system-level upper bounds prior to routed-chip implementation." | None. Caveats appear ≥4× across main text, cover letter, and supplementary energy section. | Keep ✅. Response can cite any of these four locations. |
| **R3** — Fixed Gaussian C2C/D2D vs. spatial correlation & heavy tails | **Yes** | §6.5 Limitations (line 43): "Spatially correlated D2D and heavy-tailed conductance distributions are also absent."; §6.6 Outlook (line 47): "circuit-aware layer that models spatial IR drop, sneak paths, and temperature-dependent coefficients from array geometry---a scope we have explicitly deferred here." | None. Explicitly listed as absent and deferred. | Keep ✅. |
| **R4** — NL=2.0 is gradient-scaling approximation, not materials bound | **Yes** | §6.5 Limitations (line 43): "The $NL=2.0$ limit reflects the present gradient-scaling surrogate, not a materials bound. Group-wise ablation confirms that the bottleneck is concentrated in the MLP analog path..."; Supplementary Table `tab:supp-nl-ablation` and Fig `fig:supp-nl-gradient` localize the failure to the MLP path. | None. Both the approximation disclaimer and the localization evidence are present. | Keep ✅. |
| **R5** — Ensemble HAT lacks external multi-instance baseline | **No** | §6.1 Principal Accuracy Bottlenecks discusses fresh-instance transfer and hardware-instance overfitting, but **never compares Ensemble HAT against any external multi-instance baseline from prior literature**, nor does it distinguish from i.i.d. ensemble methods. | The manuscript presents Ensemble HAT as novel but does not address the absence of external baselines. The rebuttal table admits this is "response-only," yet the "Manuscript counter" column falsely claims "§6.1 distinguishes from i.i.d."—this distinction is not made against prior work, only against the fixed-mask objective in Eq. 1. | **Flag as gap.** Either add a sentence in §6.1 acknowledging the lack of a direct external multi-instance baseline, or ensure the response clearly states this is a response-only argument and does not pretend §6.1 covers it. |
| **R6** — STE backward surrogate oversimplifies pulse accumulation | **Yes** | §3.2 Modeling Physical Non-Idealities (lines 15, 28, 46): discloses STE quantizer, STE backward pass, and state-dependent gradient scaling; Supplementary `tab:supp-nl-ablation` + `fig:supp-nl-gradient` provide empirical guardrails bounding where the surrogate fails. | None. The methodology is transparent and supplementary evidence bounds failure modes. | Keep ✅. |
| **R7** — OPECT calibration constants arbitrary / not representative | **Yes** | §5.6 Case Study (line 77): "literature-anchored reference point... 2025 OPECT array \citep{zhang2026opect}"; §3.3 Profile Interface (line 79): "Representative profile fields and provenance are documented in the Supplementary Information."; Supplementary Section `subsec:parameter-provenance` (lines 253–279): contains the "Proxy Estimate Sensitivity Analysis" sweep (Table `tab:sensitivity`, Fig `fig:supp-contour-map`) showing the conclusion is "insensitive to the exact proxy choice." | None. Anchoring and sensitivity evidence are both present. | Keep ✅. |
| **R8** — Cycle endurance ignored | **No** | **Nowhere in the manuscript.** Neither main text nor supplementary mentions cycle endurance, write cycles, or device lifetime. | The rebuttal table claims "Edge-vision = inference-heavy; retention is primary temporal bottleneck" and marks this ✅ ready. **This language is entirely absent.** The argument that edge vision is inference-heavy and therefore endurance is secondary is a response-only construction. | **Flag as gap.** Either add a 1-sentence caveat in §6.5 Limitations ("Cycle endurance is not modeled because the present edge-vision regime is inference-dominant...") or explicitly reclassify as response-only in the rebuttal table. Do not claim manuscript support that does not exist. |
| **R9** — Temperature dependence ignored | **Yes** | §6.5 Limitations (line 43): "temperature-dependent shifts in photoresponse and mismatch variance" listed as "not yet modeled explicitly"; §6.6 Outlook (line 47): deferred to "circuit-aware layer." | None. Explicitly listed and deferred. | Keep ✅. |
| **R10** — Best-checkpoint reporting masks instability | **Yes** | §5.1 Baseline Digital Performance (line 8): "All accuracy values reported for noisy and HAT deployments are best-checkpoint results unless otherwise stated." | None. Transparently disclosed. The "standard in noisy HAT literature" framing is response-only, but the disclosure itself is manuscript-level. | Keep ✅. |
| **R11** — Fig 4 mixed deterministic/MC bars | **Yes** | §5.2 / Fig 4 caption (line 18): "Error bars denote $\pm 1$ standard deviation where Monte Carlo (MC) statistics are available; bars without visible error bars indicate deterministic baselines or currently available point estimates." | None. Caption transparently discloses mixing. The "cost triaged toward Tiny-ViT depth" rationale is response-only, but the transparency is manuscript-level. | Keep ✅. |

---

## Response-Only Evidence Audit

The rebuttal table's "Pre-emptive vs. response-only split" section correctly identifies R5 and R8 as response-only, but the "Manuscript readiness" table incorrectly marks R8 as ✅. Below is a cross-check:

| Objection | Claimed in rebuttal table as... | Actually in manuscript? | Verdict |
|:--|:--|:--|:--|
| R5 | "Response-side ready" (no external baseline) | No external baseline exists; §6.1 does NOT distinguish from prior i.i.d. work. | Rebuttal table is honest about response-only, but "Manuscript counter" overclaims. |
| R8 | "✅ Inference-heavy argument ready" | **Not mentioned anywhere.** | **Misclassified.** Must be reclassified as response-only. |
| R1 | "Scope clearly stated; no patch needed" | Scope IS stated (§1), but "§6 defers ImageNet" is fabricated. | Minor overclaim; fix citation. |

---

## Recommended Actions

1. **Fix R1 citation in rebuttal table:** Remove "§6 defers ImageNet." Replace with "§1 scopes to edge vision; §4 lists evaluated datasets."
2. **Fix R5 manuscript counter:** Remove "§6.1 distinguishes from i.i.d." Replace with "Manuscript presents Ensemble HAT as novel; external multi-instance baseline comparison is response-only."
3. **Fix R8 readiness:** Change from ✅ to **⚠️ response-only**. Optionally add a 1-sentence endurance caveat in §6.5 Limitations.
4. **All other objections (R2–R4, R6–R7, R9–R11):** No changes needed. Manuscript support is verified and robust.

---

*Audit completed. All line references verified against `01_introduction.tex`, `03_methodology.tex`, `04_experimental_setup.tex`, `05_results.tex`, `06_discussion.tex`, `cover_letter.tex`, and `supplementary.tex`.*
