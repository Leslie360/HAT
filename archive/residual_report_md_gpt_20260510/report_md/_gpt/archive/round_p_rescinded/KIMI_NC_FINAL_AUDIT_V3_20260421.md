<!-- DEPRECATED 2026-04-24 — 基于 bug-contaminated 数据；analog_layers.py STE 反向传播在 NL≠1 时存在分支映射翻转 + 额外 nl 乘数，已于 commit 33bed9c 修复。详见 BROADCAST_REBUILD_3WEEK_20260424.md。 -->
# NC Submission Packaging Audit v3 (Post-Pivot)

**Date:** 2026-04-21
**Bundle:** `/home/qiaosir/projects/compute_vit/outputs/submission_bundle_20260419/`
**Source (ground truth):** `/home/qiaosir/projects/compute_vit/paper/latex_gpt/`

---

## Audit Items

### 1. Abstract ≤150 words and reflects negative-result framing
**FAIL**

- **Word count:** The source abstract is 122 words (PASS). The bundle abstract is ~118 words split across three paragraphs (within limit).
- **Negative-result framing:** **MISSING in bundle.**
  - *Source* says: "we systematically test and falsify three candidate mitigation strategies, including joint training, which remains pinned at ~30% fresh-instance accuracy" and establishes "a ~30% fresh-instance ceiling under severe nonlinearity, indicating that first-order behavioral surrogates impose a structural generalization barrier in the attention pathway."
  - *Bundle* says: "Severe nonlinear write (NL=2.0) remains a practical recovery bottleneck, limiting accuracy to 27.72±0.82% under the present gradient-scaling approximation." The bundle abstract completely omits the falsification narrative, the 30.53% joint-training result, and the structural-barrier conclusion.
- **Root cause:** The bundle `sections/00_abstract.tex` is a **pre-pivot version**.

---

### 2. Results section has no orphaned forward references
**PASS**

The source `05_results.tex` contains several forward references to methodology sections and equations (`eq:scale-recovery`, `eq:hat-ensemble`, `eq:inverse-gamma`, `eq:sobol-first-order`, `sec:methodology`). All are intentional "later formalized in" / "formally defined in" pointers, and all corresponding `\label{}` definitions exist in `sections/03_methodology.tex`. None are orphaned.

> Note: In the **bundle**, the results section is missing the central negative-result paragraph (lines 74–77 of the source), but the remaining forward references are still valid.

---

### 3. Cover letter fits 1 page
**FAIL**

- The bundle `cover_letter.pdf` is **2 pages** (`Pages: 2` per `pdfinfo`).
- The bundle `cover_letter.tex` is a **pre-pivot revision-response draft** (dated implicitly 2026-04-19). It does not match the post-pivot source `cover_letter.tex`.
- The source cover letter (post-pivot) is shorter and explicitly frames the falsification narrative; the bundle version is longer, lists ResNet backbones in Key Contributions, and buries the negative result.

---

### 4. No placeholders remain (except user-owned fields)
**PASS**

No `PLACEHOLDER`, `TODO`, `FIXME`, `XXX`, `HOLD`, `DRAFT`, `[AUTHOR]`, `[EMAIL]`, `[AFFILIATION]`, `[REVIEWER]`, `[ORCID]`, or `TBD` strings were found in the submission `.tex` or `.bib` files.

> The word "placeholder" appears only in legitimate technical contexts: "analytical placeholders for a first-order edge-node model" (energy-model disclaimer) and "no placeholder panel is inserted for missing architectures" (figure caption).

---

### 5. Locked numbers consistent with updated text (30.53 added to manifest)
**FAIL**

- The number **30.53** is present in source data JSONs (`joint_mlp_linear_ensemble_hat_full_fresh.json`: `30.5324`), but it is **not explicitly documented** in:
  - `source_data_v1_MANIFEST.md`
  - `source_data_v1/README.md`
- More critically, the **bundle `05_results.tex` does not mention 30.53 at all** — the entire joint-training paragraph (lines 74–77 of the source) was dropped during bundle creation. This is the central locked number of the pivot and it is **absent from the compiled manuscript**.

---

### 6. Bundle contains .bbl files
**PASS**

Both `manuscript/main.bbl` and `supplementary/supplementary_main.bbl` are present in the bundle.

---

### 7. Citation keys consistent (2025 not 2026)
**FAIL**

Three citations with **2026** years are actively used in the text:

| Citation key | Year | Used in |
|:---|:---|:---|
| `crosssim2026` | 2026 | `01_introduction.tex`, `02_related_work.tex`, `supplementary.tex` |
| `iconniv2026` | 2026 | `06_discussion.tex` |
| `mia2026trilinear` | 2026 | `02_related_work.tex` |

All three appear in `refs_gpt.bib` with `year = {2026}`. If these are preprints or forthcoming works, 2026 may be intentional, but the audit instruction flags "2025 not 2026" as a consistency check.

---

### 8. Zenodo cross-refs intact
**PASS**

- `07_conclusion.tex` states: "A reproducibility archive ... has been staged for Zenodo deposition and will be assigned a DOI at acceptance."
- No broken Zenodo DOI links are present (no DOI has been issued yet, which is expected).

---

### 9. Supplementary references updated (if any mention of joint-training success)
**PASS**

No mentions of joint-training success appear in `supplementary.tex`. All references to joint training frame it as a negative result:

- Supp. Table SX.N (NL ablation) documents the joint MLP-linear + Ensemble HAT result as `30.53 ± 7.07%` fresh-instance.
- Supp. text: "The all-linear upper-bound control behaves similarly under fresh-instance transfer, reaching only 32.60 ± 9.18%."
- No contradictory positive-success language remains.

---

### 10. Response letter v2 (if any) consistent with pivot
**NOT PRESENT IN BUNDLE**

No response letter (`response_letter_v2.pdf`, `response_to_reviewers.pdf`, etc.) is included in the submission bundle. Response-related files exist outside the bundle (`report_md/_gpt/reviewer_response/MINOR_REVISION_RESPONSE.md`, dated 2026-04-15), but they are **not part of the submission package** and are from the prior minor-revision round rather than the post-pivot revision.

---

## Critical Sync Failure Summary

The submission bundle (`submission_bundle_20260419/`) is **out of sync** with the post-pivot source files (`paper/latex_gpt/`). The bundle contains a **pre-pivot snapshot** of the three most narrative-critical files:

| File | Source (post-pivot) | Bundle (pre-pivot) | Status |
|:---|:---|:---|:---|
| `sections/00_abstract.tex` | Falsification narrative, 30.53% ceiling, structural barrier | Softer "bottleneck" language, no 30.53%, no falsification | **MISMATCH** |
| `sections/05_results.tex` | Contains 30.53 ± 7.07% joint-training paragraph (lines 74–77) | **Missing entire paragraph** | **MISMATCH** |
| `cover_letter.tex` | 1 page, explicit falsification framing, ~30% ceiling | 2 pages, old revision response, ResNet in contributions | **MISMATCH** |

The bundle was assembled **after** the pivot but apparently copied from an older build artifact rather than from the current `paper/latex_gpt/` source tree.

---

## Final Verdict

**Not ready — see items above.**

**Required actions before submission:**

1. **Rebuild the bundle** from the current `paper/latex_gpt/` source tree to ensure `00_abstract.tex`, `05_results.tex`, and `cover_letter.tex` are the post-pivot versions.
2. **Shrink cover letter to 1 page** (remove the old revision-cycle paragraph, tighten contributions, drop novelty-boundary bullet if needed).
3. **Add 30.53 ± 7.07%** to `source_data_v1_MANIFEST.md` and `README.md` under the NL-ablation or joint-training entry.
4. **Verify or update** the three 2026 citation years (`crosssim2026`, `iconniv2026`, `mia2026trilinear`) — if they are preprints that will publish in 2026, retain; otherwise change to 2025.
5. **If a response letter v2 is required**, draft it consistent with the negative-result pivot and include it in the bundle.

Once these are resolved, the submission will be **submission-ready pending user metadata** (author name, email, affiliation, acknowledgements, reviewers, ORCID).
