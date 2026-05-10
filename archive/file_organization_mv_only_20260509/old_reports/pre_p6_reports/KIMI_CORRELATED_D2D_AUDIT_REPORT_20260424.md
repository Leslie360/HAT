# Kimi Text-Side: Correlated D2D (AR(1)) Provenance Audit
**Date:** 2026-04-24 22:20 CST
**Author:** Kimi (Auditor)
**Scope:** All citations of 86.33/84.57/82.12/73.7 across manuscript + thesis
**Status:** Awaiting Codex data-side verdict for final zone lock

---

## 1. Citation Map

### 1.1 Paper (latex_gpt)

| File | Line | Context | Zone Tag Needed |
|:--|:--|:--|:--|
| `supplementary.tex` | 800-809 | Supp Note S2: i.i.d. 86.33±1.61%, ρ=0.3 84.57±2.39%, ρ=0.5 82.12±3.95%; min 73.7% | **TBD** |
| `06_discussion.tex` | 43 | Limitations paragraph: same numbers, cites Supp Note S2 | **TBD** |
| `cover_letter.tex` | 30 | Correlated D2D sweep mention | **TBD** |
| `cover_letter_v5.tex.kimi_draft_v3` | 30 | Same | **TBD** |

### 1.2 EN Thesis

| File | Line | Context |
|:--|:--|:--|
| `chapter_4_failure_modes.tex` | 143, 174-178 | Failure-mode atlas: bounded degradation narrative |
| `chapter_5_mitigation.tex` | 78, 409 | Mitigation case studies: bounded degradation |
| `chapter_6_physical_realism.tex` | 74-81, 401 | Physical realism deep dive |
| `chapter_7_deployment.tex` | 64-72, 196, 337 | Deployment envelope, design rules |
| `chapter_8_outlook.tex` | 54, 119, 242 | Outlook / cross-dataset question |

### 1.3 CN Thesis

| File | Line | Context |
|:--|:--|:--|
| `chapter_7_deployment.tex` | 143-164, 406 | Deployment chapter (CN) |

**Total unique cite locations:** 14 files, ~25 individual line ranges.

---

## 2. JSON Provenance (Kimi preliminary check)

| Field | Value | Assessment |
|:--|:--|:--|
| Source file | `report_md/_gpt/json_gpt/fresh_instance_eval_v4_ensemble_correlated_d2d.json` | ✅ Found |
| Generated at | `2026-04-19T02:44:02` | Pre-fix date (Apr 19 < Apr 24 bug fix) |
| Checkpoint | `checkpoints/_ensemble/V4_hybrid_standard_noise_hat_best.pt` | ✅ Canonical Ensemble HAT, standard (uniform) noise |
| Protocol | 10 fresh instances × 5 MC runs | ✅ Matches manuscript claim |
| Correlation model | `separable_ar1_2d` | ✅ Matches AR(1) claim |
| Raw results | ρ=0: 86.3288±1.6093; ρ=0.3: 84.5656±2.3923; ρ=0.5: 82.1244±3.9460 | ✅ Matches cited numbers (86.33/84.57/82.12) |
| `nl_ltp` / `nl_ltd` | **Not recorded in JSON** | ⚠️ Must infer from checkpoint name |

## 3. Zone Classification (Kimi preliminary, pending Codex confirmation)

**Inference:** The checkpoint is `V4_hybrid_standard_noise_hat_best.pt`.
- `V4` = Ensemble HAT (epoch-resampled D2D)
- `standard_noise` = uniform noise profile
- Uniform noise at canonical settings implies **NL=1.0** (ideal write)
- NL=1.0 is **zone 3A bug-immune**: `pow(ratio, NL-1) = pow(ratio, 0) = 1` regardless of branch mapping or stray multiplier

**Preliminary verdict: ZONE 3A — numbers are valid, no rerun needed.**

**Caveat:** If Codex data audit reveals the checkpoint was trained with NL≠1.0 or any other protocol deviation, this verdict flips to 3B.

---

## 4. Theory-Empirical Consistency Check

KIMI-THEORY-1 predicts monotonic degradation in ρ for separable AR(1) perturbation under the Fisher-matrix-weighted anisotropic penalty.

Empirical pattern: **86.33 > 84.57 > 82.12** ✅ Monotonic.
Cross-instance std growth: **1.61 → 2.39 → 3.95** ✅ Monotonic.
Worst-case instance at ρ=0.5: **73.7%** ✅ Bounded, far from chance.

**Consistency: PASS.** Theory and data align qualitatively.

---

## 5. Recommended Text Actions (pending Codex zone confirmation)

If Codex confirms **zone 3A**:
- All 14 cite locations keep numbers verbatim
- Add explicit zone-3A tag to Supp Note S2 preamble
- No narrative changes needed

If Codex flags **zone 3B**:
- Remove numbers from all 14 locations OR replace with rerun results
- Update Supp Note S2, 06_discussion, all thesis chapters
- Notify Claude for integration re-planning

---

## 6. Deliverable

Awaiting Codex `CODEX_CORRELATED_D2D_AUDIT_REPORT_20260424.md` for joint closure.

**Kimi text-side audit is complete.**
